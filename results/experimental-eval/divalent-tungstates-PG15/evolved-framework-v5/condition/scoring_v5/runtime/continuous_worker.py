"""Independent continuous specimen fit using native GSAS-II calculations.

This process receives submitted CIFs, fixed fractions, calibrated evaluator
instrument parameters, bounds, and observed counts. It receives no truth CIFs,
phase-specific realizations, or expected intensities. Atomic parameters never
refine. A separate free-fraction diagnostic cannot select the scored model.
"""
from pathlib import Path
from itertools import product
import json
import sys
import time
import numpy as np
from scipy.optimize import least_squares, nnls, minimize_scalar
from GSASII import GSASIIscriptable as G2
from gsas_worker_text import instrument_text


class NativeProfiles:
    def __init__(self, request, folder):
        G2.SetPrintLevel('error')
        self.request = request
        instrument = folder/'instrument.instprm'
        instrument.write_text(instrument_text(request['instrument']))
        self.project = G2.G2Project(newgpx=str(folder/'continuous.gpx'))
        self.names, self.histograms, self.masses = [], [], []
        for i, path in enumerate(request['cifs']):
            phase = self.project.add_phase(path, phasename=f'phase_{i}', fmthint='CIF')
            mass = float(phase.data['General']['Mass'])
            if not np.isfinite(mass) or mass <= 0:
                raise ValueError('Nonpositive native unit-cell mass')
            hist = self.project.add_simulated_powder_histogram(
                f'profile_{i}', str(instrument), request['grid']['min'], request['grid']['max'],
                Tstep=request['grid']['step'], scale=1., phases=[phase])
            hist.SampleParameters['Scale'] = [1., False]
            hist.SampleParameters['Type'] = 'Bragg-Brentano'
            hist.set_refinements({'Background': {'type': 'chebyschev-1', 'no. coeffs': 3,
                                                'coeffs': [0., 0., 0.], 'refine': False}})
            hap = phase.data['Histograms'][hist.name]
            hap['Scale'] = [10000./mass, False]
            hap['Size'][0] = hap['Mustrain'][0] = 'isotropic'
            hap['Size'][2] = hap['Mustrain'][2] = [False, False, False]
            hap['Pref.Ori.'][0] = 'MD'
            hap['Pref.Ori.'][2] = False
            hap['Extinction'] = [0., False]
            self.names.append(phase.name)
            self.histograms.append(hist.name)
            self.masses.append(mass)
        self.project.set_Controls('cycles', 0)
        self.cache = {}
        self.calls = 0

    def calculate(self, specs):
        key = tuple((s['size_um'], s['microstrain_ppm'], s['md_ratio'], *s['md_axis']) for s in specs)
        if key in self.cache:
            return self.cache[key]
        for name, hist, spec in zip(self.names, self.histograms, specs):
            # refine() reloads the GPX; obtain current wrappers on every call.
            hap = self.project.phase(name).data['Histograms'][hist]
            hap['Size'][1][0:2] = [spec['size_um']]*2
            hap['Mustrain'][1][0:2] = [spec['microstrain_ppm']]*2
            hap['Pref.Ori.'][1] = spec['md_ratio']
            hap['Pref.Ori.'][3] = spec['md_axis']
        self.project.refine()
        if self.project.data.get('Covariance', {}).get('data', {}).get('varyList', []):
            raise ValueError('Independent forward calculation refined a structural parameter')
        profiles = np.asarray([self.project.histogram(h).data['data'][1][3] for h in self.histograms])/10000.
        if not np.isfinite(profiles).all() or profiles.max() <= 0 or profiles.min() < -1e-7*profiles.max():
            raise ValueError('Invalid native continuous profile')
        profiles = np.maximum(profiles, 0)
        self.calls += 1
        if len(self.cache) >= 100:
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = profiles.copy()
        return profiles


def linear_fit(x, y, profiles, fractions):
    t = (x-x[0])/(x[-1]-x[0])
    background = np.column_stack(((1-t)**2, 2*t*(1-t), t*t))
    columns = profiles if fractions is None else np.asarray([np.asarray(fractions)@profiles])
    norm = columns.max()
    if norm <= 0:
        raise ValueError('Zero submitted diffraction')
    design = np.column_stack((columns.T/norm, background))
    root = 1/np.sqrt(np.maximum(y, 1))
    coef, _ = nnls(design*root[:, None], y*root, maxiter=4000)
    calc = design@coef
    amps = coef[:len(columns)]
    weights = (amps/amps.sum()).tolist() if fractions is None and amps.sum() > 0 else fractions
    return (calc-y)*root, calc, background@coef[len(columns):], weights


def fit(request, folder):
    started=time.monotonic()
    table = np.loadtxt(request['observed_path'], delimiter=',', skiprows=1)
    x, y = table[:, 0], table[:, 1]
    policy = request['search']
    from native_memory import MemoryProfiles
    native = MemoryProfiles(NativeProfiles(request, folder), folder)
    n = len(request['cifs'])
    fractions = request['fractions']
    bounds = request['bounds']
    axes = request['axes']
    layout = []
    for i in range(n):
        for field in ['size_um', 'microstrain_ppm', 'md_ratio']:
            if bounds[field][0] != bounds[field][1]:
                layout.append((i, field))

    def decode(z, choices):
        specs = [{'size_um':bounds['size_um'][0], 'microstrain_ppm':bounds['microstrain_ppm'][0],
                  'md_ratio':bounds['md_ratio'][0], 'md_axis':list(axes[c])} for c in choices]
        for value, (i, field) in zip(z, layout):
            lo, hi = bounds[field]
            specs[i][field] = float(np.exp(np.log(lo)+value*np.log(hi/lo))) if field in {'size_um','md_ratio'} else float(lo+value*(hi-lo))
        return specs

    def encode_default():
        values = {'size_um':.3, 'microstrain_ppm':100., 'md_ratio':1.}
        result = []
        for i, field in layout:
            lo, hi = bounds[field]
            value = np.clip(values[field], lo, hi)
            q = np.log(value/lo)/np.log(hi/lo) if field in {'size_um','md_ratio'} else (value-lo)/(hi-lo)
            result.append(float(np.clip(q, 1e-5, 1-1e-5)))
        return np.array(result)

    attempts = []
    rng = np.random.default_rng(policy['seed'])
    texture_trials = 0

    def solve(start, choices):
        def residual(z):
            return linear_fit(x, y, native.calculate(decode(z, choices)), fractions)[0]
        if len(layout):
            result = least_squares(residual, start, bounds=(np.zeros(len(layout)), np.ones(len(layout))),
                diff_step=1e-3, max_nfev=policy['max_nfev'],
                ftol=policy['ftol'], xtol=policy['xtol'], gtol=policy['gtol'])
            values, success, message, nfev = result.x, bool(result.success), str(result.message), int(result.nfev)
        else:
            values, success, message, nfev = np.array([]), True, 'No continuous degrees of freedom', 1
        specs = decode(values, choices)
        residuals, calc, bg, fitted_fractions = linear_fit(x, y, native.calculate(specs), fractions)
        row = {'loss':float(residuals@residuals), 'converged':success, 'message':message,
               'nfev':nfev, 'axes':list(choices), 'parameters':values.tolist(), 'settings':specs,
               'calculated':calc, 'background':bg, 'fractions':fitted_fractions}
        attempts.append(row)
        return row

    def texture_option(current, phase, axis):
        """Screen a texture axis at fixed widths before joint reoptimization.

        Changing an axis does not justify refitting every phase from scratch.
        This one-dimensional fit reuses the same native peak kernels.
        """
        nonlocal texture_trials
        choices=list(current['axes']);choices[phase]=axis
        parameters=np.array(current['parameters'])
        position=layout.index((phase,'md_ratio')) if (phase,'md_ratio') in layout else None
        def evaluate(value):
            z=parameters.copy()
            if position is not None:z[position]=value
            spec=decode(z,choices)
            residuals,calc,bg,fitted=linear_fit(x,y,native.calculate(spec),fractions)
            return dict(loss=float(residuals@residuals),axes=choices,parameters=z.tolist(),settings=spec,
                        calculated=calc,background=bg,fractions=fitted,converged=True,nfev=1,
                        message='axis screening at fixed broadening')
        if position is None:return evaluate(0.)
        grid=np.linspace(0,1,5)
        trials=[evaluate(v) for v in grid]
        best_index=int(np.argmin([a['loss'] for a in trials]))
        lo,hi=grid[max(0,best_index-1)],grid[min(4,best_index+1)]
        opt=minimize_scalar(lambda v:evaluate(v)['loss'],bounds=(lo,hi),method='bounded',
                            options={'xatol':1e-5,'maxiter':40})
        trials.append(evaluate(opt.x))
        texture_trials += len(trials)+int(opt.nfev)
        return min(trials,key=lambda a:a['loss'])

    default = encode_default()
    for start_index in range(policy['starts']):
        choices = tuple(0 for _ in range(n)) if start_index == 0 else tuple(int(rng.integers(len(axes))) for _ in range(n))
        start = default if start_index == 0 else rng.uniform(.1, .9, len(layout))
        current = solve(start, choices)
        # Axis screening refits the ratio, reusing fixed-width kernels. Only
        # the selected axes trigger another full joint continuous fit.
        for _ in range(2):
            previous = current['loss']
            for phase in range(n):
                options = [current]
                for axis in range(len(axes)):
                    if axis == current['axes'][phase]:
                        continue
                    trial_axes = list(current['axes']); trial_axes[phase] = axis
                    options.append(texture_option(current,phase,axis))
                current = min(options, key=lambda r:r['loss'])
            if current['loss'] >= previous-1e-5:
                break
            current=solve(np.clip(current['parameters'],1e-5,1-1e-5),tuple(current['axes']))
    best = min(attempts, key=lambda r:r['loss'])
    native.assert_fixed_model()
    if not best['converged']:
        raise RuntimeError('Best continuous profile fit did not converge; evaluator failure, not solver zero')
    denominator = float(np.sum(y*y/np.maximum(y,1)))
    grid = native.x
    if grid.shape != x.shape or not np.allclose(grid, x, atol=1e-7, rtol=0):
        raise ValueError('Native continuous grid differs from observed counts')
    return {'chi_square':best['loss'], 'rwp_percent':100*np.sqrt(best['loss']/denominator),
            'phase_profile_settings':best['settings'], 'fractions':best['fractions'],
            'unit_cell_masses_amu':native.masses, 'zero_shift_deg':0., 'domain_size_um':None,
            'profile_search':{'method':'bounded native-GSAS continuous variable projection with axis search',
                'starts':policy['starts'], 'native_evaluations':native.calls, 'converged':True,
                'phase_evaluations':native.phase_calls, 'phase_cache_hits':native.cache_hits,
                'elapsed_seconds':time.monotonic()-started, 'in_memory_native':True,
                'texture_screen_evaluations':texture_trials,
                'axis_schedule':'fixed-width 1D ratio screen followed by joint fit; at most two passes per start',
                'global_optimum_guaranteed':False, 'true_specimen_settings_used':False,
                'trials':[{k:r[k] for k in ['loss','converged','nfev','axes']} for r in attempts]},
            '_arrays':{'x':x, 'calculated':best['calculated'], 'background':best['background']}}


if __name__ == '__main__':
    req = json.loads(Path(sys.argv[1]).read_text())
    output = Path(sys.argv[2]); output.parent.mkdir(parents=True, exist_ok=True)
    result = fit(req, output.parent)
    np.savez_compressed(output, **result.pop('_arrays'))
    output.with_suffix('.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
