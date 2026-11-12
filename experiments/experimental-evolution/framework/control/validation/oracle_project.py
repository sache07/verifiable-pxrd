"""Operator validation only: build a GSAS-II project for a frozen synthetic case from its hidden truth.

Run with the GSAS-II interpreter:  python oracle_project.py CASE_DIR OUT_DIR VARIANT

Variants hold the true structures and fractions fixed and differ only in which nuisance physics the
model contains, so the frozen scorer's D shows what each omission costs:
  oracle            all generating physics at the true values; refine scale and background
  no_displacement   Shift = 0; refine zero, cells, scale, background
  no_roughness      no low-angle deficit; refine Uiso, scale, background
  instrument_only   no specimen broadening (size 10 um, strain 0); refine U, V, W, X, scale, background
  no_specimen_model all three omissions; refine zero, U, V, W, X, cells, Uiso, scale, background
  parent_reference  all generating physics, but each mismatched phase as its untouched registered model
  parent_refined_cells   the same, then refine the cells
  parent_refined_xyz     the same, then refine the cells and all atomic coordinates
Never shipped to a solver or researcher; reads private/truth.json.
"""
from pathlib import Path
import json
import sys

import numpy as np
from GSASII import GSASIIscriptable as G2

RUNTIME = Path(__file__).resolve().parents[2] / 'runtime'
sys.path.insert(0, str(RUNTIME))
from gsas_worker_text import instrument_text  # noqa: E402

VARIANTS = {'oracle', 'no_displacement', 'no_roughness', 'instrument_only', 'no_specimen_model',
            'parent_reference', 'parent_refined_cells', 'parent_refined_xyz'}


def build(case, out, variant):
    if variant not in VARIANTS:
        raise ValueError('unknown variant ' + variant)
    G2.SetPrintLevel('error')
    case, out = Path(case), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    truth = json.loads((case / 'private/truth.json').read_text())
    inst = dict(truth['measurement']['true_instrument'])
    (out / 'instrument.instprm').write_text(instrument_text(inst))
    gpx = G2.G2Project(newgpx=str(out / 'final.gpx'))
    x, y = np.loadtxt(case / 'inputs/pattern.csv', delimiter=',', skiprows=1).T
    np.savetxt(out / 'pattern.xye', np.column_stack((x, y, np.sqrt(np.maximum(y, 1)))), fmt='%.10g')
    hist = gpx.add_powder_histogram(str(out / 'pattern.xye'), str(out / 'instrument.instprm'), fmthint='xye')
    sample = truth.get('sample_realization', {})
    sp = hist.data['Sample Parameters']
    sp['Type'] = 'Bragg-Brentano'
    sp['Gonio. radius'] = float(sample.get('goniometer_radius_mm', 200.0))
    displacement = variant not in {'no_displacement', 'no_specimen_model'}
    roughness = variant not in {'no_roughness', 'no_specimen_model'}
    broadening = variant not in {'instrument_only', 'no_specimen_model'}
    sp['Shift'] = [float(sample.get('shift_um', 0.)) if displacement else 0., False]
    sp['SurfRoughA'] = [float(sample.get('surf_rough_A', 0.)) if roughness else 0., False]
    sp['SurfRoughB'] = [float(sample.get('surf_rough_B', 0.)) if roughness else 0., False]
    sp['Transparency'] = [0., False]
    masses = truth['forward']['unit_cell_masses_amu']
    specimen = {r['id']: r for r in truth['specimen_realization']}
    phases = []
    for i, (row, fraction) in enumerate(zip(truth['phases'], truth['true_fractions'])):
        parent = variant.startswith('parent') and row.get('registered_model_path')
        ph = gpx.add_phase(parent or str(case / 'private/references' / (row['id'] + '.cif')), phasename='p%d' % i,
                           histograms=[hist], fmthint='CIF')
        if parent and 'case_uiso_A2' in row:
            for atom in ph.atoms():
                atom.uiso = float(row['case_uiso_A2'])
        hap = ph.data['Histograms'][hist.name]
        spec = specimen[row['id']]
        hap['Scale'] = [float(fraction) / float(masses[i]), False]
        hap['Size'][0] = 'isotropic'
        hap['Size'][1][0] = hap['Size'][1][1] = float(spec['size_um']) if broadening else 10.0
        hap['Size'][2] = [False, False, False]
        axial = spec.get('microstrain_axial_ppm', spec['microstrain_ppm'])
        if broadening and float(axial) != float(spec['microstrain_ppm']):
            hap['Mustrain'][0] = 'uniaxial'
            hap['Mustrain'][1][0], hap['Mustrain'][1][1] = float(spec['microstrain_ppm']), float(axial)
            hap['Mustrain'][3] = list(spec['microstrain_axis'])
        else:
            hap['Mustrain'][0] = 'isotropic'
            hap['Mustrain'][1][0] = hap['Mustrain'][1][1] = float(spec['microstrain_ppm']) if broadening else 0.
        hap['Mustrain'][2] = [False, False, False]
        hap['Pref.Ori.'][0] = 'MD'
        hap['Pref.Ori.'][1] = float(spec['md_ratio'])
        hap['Pref.Ori.'][2] = False
        hap['Pref.Ori.'][3] = list(spec['md_axis'])
        hap['Extinction'] = [0., False]
        phases.append(ph)
    hist.data['Limits'][1] = list(hist.data['Limits'][0])
    hist.SampleParameters['Scale'] = [1.0, True]
    hist.set_refinements({'Background': {'type': 'chebyschev-1', 'no. coeffs': 12, 'refine': True}})
    gpx.set_Controls('cycles', 8)
    gpx.refine()  # scale and background first, all physics fixed
    if variant != 'oracle':
        if not displacement:
            hist.set_refinements({'Instrument Parameters': ['Zero']})
            for ph in phases:
                ph.set_refinements({'Cell': True})
        if not roughness:
            for ph in phases:
                ph.set_refinements({'Atoms': {'all': 'U'}})
        if not broadening:
            hist.set_refinements({'Instrument Parameters': ['U', 'V', 'W', 'X']})
        if variant in {'parent_refined_cells', 'parent_refined_xyz'}:
            for ph in phases:
                ph.set_refinements({'Cell': True})
        if variant == 'parent_refined_xyz':
            for ph in phases:
                ph.set_refinements({'Atoms': {'all': 'X'}})
        gpx.set_Controls('cycles', 15)
        gpx.refine()
    gpx.save()
    h = gpx.histogram(hist.name)
    return {'variant': variant, 'case': case.name, 'gsas_rwp': float(h.get_wR()),
            'refined_zero': float(h.data['Instrument Parameters'][0]['Zero'][1]),
            'U': float(h.data['Instrument Parameters'][0]['U'][1]), 'X': float(h.data['Instrument Parameters'][0]['X'][1])}


if __name__ == '__main__':
    print(json.dumps(build(*sys.argv[1:4])))
