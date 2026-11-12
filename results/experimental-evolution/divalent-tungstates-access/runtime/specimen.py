"""Versioned finite-grid and continuous specimen distributions.

Realizations are private; profile bounds are fixed before seeing outcomes.
Two whole-specimen (case-level) effects of laboratory reflection
measurements: Bragg-Brentano specimen displacement and a low-angle intensity
deficit (Suortti surface roughness). Both use GSAS-II's own sample-parameter
conventions, so a solver can represent them exactly.
"""
from itertools import product
from pathlib import Path
import hashlib
import math
import numpy as np


PHASE_KEYS = {'microstrain', 'preferred_orientation', 'phase_specific_sizes', 'displacement_parameters'}
CASE_KEYS = {'specimen_displacement', 'surface_roughness'}
KEYS = PHASE_KEYS | CASE_KEYS
GONIOMETER_RADIUS_MM = 200.0  # GSAS-II default; a lab's settings give its own radius


def _bounds(value, name, positive=False):
    if (not isinstance(value, list) or len(value) != 2 or
            any(type(v) not in (int, float) or not math.isfinite(v) for v in value) or
            not value[0] < value[1] or (positive and value[0] <= 0)):
        raise ValueError('Invalid bounds: ' + name)
    return value


def _probability(spec, name):
    p = spec.get('probability', 1.)
    if type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('Specimen probability must lie in [0,1]: ' + name)
    return p


def _case_effect(name, spec):
    if type(spec.get('enabled')) is not bool:
        raise ValueError('Invalid specimen-effect configuration: ' + name)
    if not spec['enabled']:
        return  # a switched-off effect needs no distribution
    if name == 'specimen_displacement':
        if set(spec) - {'enabled', 'distribution', 'range_um', 'probability', 'goniometer_radius_mm', 'convention'}:
            raise ValueError('Invalid specimen-effect configuration: ' + name)
        if spec.get('distribution') != 'uniform':
            raise ValueError('Specimen displacement uses a uniform distribution')
        low, high = _bounds(spec.get('range_um'), name)
        if not low <= 0 <= high or max(abs(low), abs(high)) > 2000:
            raise ValueError('Displacement bounds must include zero and stay within +/-2000 um')
        radius = spec.get('goniometer_radius_mm', GONIOMETER_RADIUS_MM)
        if type(radius) not in (int, float) or not 50 <= radius <= 1000:
            raise ValueError('Goniometer radius must be given in mm (50-1000)')
    else:
        if set(spec) - {'enabled', 'probability', 'A_range', 'B_range', 'B_distribution',
                        'max_low_angle_deficit', 'deficit_reference_2theta_deg', 'convention'}:
            raise ValueError('Invalid specimen-effect configuration: ' + name)
        a = _bounds(spec.get('A_range'), name + '.A_range')
        b = _bounds(spec.get('B_range'), name + '.B_range', positive=spec.get('B_distribution') == 'log_uniform')
        if not (0 <= a[0] and a[1] < 1) or b[0] < 0 or b[1] > 2:
            raise ValueError('Suortti parameters need 0 <= A < 1 and 0 <= B <= 2')
        if spec.get('B_distribution') not in {'uniform', 'log_uniform'}:
            raise ValueError('Unknown roughness B distribution')
        cap = spec.get('max_low_angle_deficit')
        ref = spec.get('deficit_reference_2theta_deg')
        if type(cap) not in (int, float) or not 0 < cap < 1 or type(ref) not in (int, float) or not 5 <= ref <= 60:
            raise ValueError('Roughness needs a deficit cap in (0,1) at a 5-60 degree reference angle')
    _probability(spec, name)


def _anisotropy(spec):
    """Uniaxial microstrain: the strain along one lattice direction differs from the strain perpendicular to it."""
    if not isinstance(spec, dict) or set(spec) - {'probability', 'axial_ratio', 'axes'} or not {'axial_ratio', 'axes'} <= set(spec):
        raise ValueError('microstrain.anisotropy needs axial_ratio, axes and an optional probability')
    _probability(spec, 'microstrain.anisotropy')
    ratio = spec['axial_ratio']
    if not isinstance(ratio, dict) or set(ratio) != {'distribution', 'range'} or ratio['distribution'] not in {'uniform', 'log_uniform'}:
        raise ValueError('axial_ratio needs a uniform or log_uniform distribution and range')
    _bounds(ratio['range'], 'microstrain.anisotropy.axial_ratio', positive=True)
    axes = spec['axes']
    if not isinstance(axes, list) or not axes or len(axes) > 6:
        raise ValueError('microstrain.anisotropy needs 1..6 axes')
    for hkl in axes:
        if not isinstance(hkl, list) or len(hkl) != 3 or not any(hkl) or any(type(v) is not int for v in hkl):
            raise ValueError('Microstrain axes must be nonzero integer hkl triples')


def effect_settings(protocol):
    settings = protocol['generation'].get('specimen_effects', {})
    if set(settings) - KEYS:
        raise ValueError('Unknown specimen effect')
    for name, spec in settings.items():
        if name in CASE_KEYS:
            _case_effect(name, spec)
            continue
        fields = {'enabled'}
        fields |= {'values_ppm', 'anisotropy'} if name == 'microstrain' else set()
        fields |= {'ratios', 'axes', 'model'} if name == 'preferred_orientation' else set()
        fields |= {'values_A2', 'sampling'} if name == 'displacement_parameters' else set()
        fields |= {'distribution', 'range', 'probability'}
        if set(spec) - fields or type(spec.get('enabled')) is not bool:
            raise ValueError('Invalid specimen-effect configuration: ' + name)
        if not spec['enabled']:
            continue
        field = {'microstrain':'values_ppm', 'displacement_parameters':'values_A2',
                 'preferred_orientation':'ratios'}.get(name)
        continuous = 'distribution' in spec
        if continuous:
            if spec['distribution'] not in {'uniform', 'log_uniform'}:
                raise ValueError('Unknown continuous specimen distribution')
            bounds = spec.get('range')
            if (not isinstance(bounds, list) or len(bounds) != 2 or
                    any(type(v) not in (int, float) or not math.isfinite(v) for v in bounds) or
                    not 0 <= bounds[0] < bounds[1] or
                    (spec['distribution'] == 'log_uniform' and bounds[0] <= 0)):
                raise ValueError('Invalid continuous specimen bounds: ' + name)
            if name in {'preferred_orientation', 'phase_specific_sizes', 'displacement_parameters'} and bounds[0] <= 0:
                raise ValueError('Positive specimen bounds required: ' + name)
            if name == 'preferred_orientation' and not bounds[0] <= 1 <= bounds[1]:
                raise ValueError('Orientation bounds must include the random-powder limit')
            p = spec.get('probability', 1.)
            if type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1:
                raise ValueError('Specimen probability must lie in [0,1]')
            if field in spec:
                raise ValueError('Do not combine continuous and finite-grid sampling')
        elif any(k in spec for k in ['range', 'probability']):
            raise ValueError('Continuous specimen fields require a distribution')
        if field and not continuous:
            values = spec.get(field)
            if not isinstance(values, list) or not values or len(values) > 9:
                raise ValueError(name + ' needs a nonempty finite grid (at most nine values)')
            if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in values):
                raise ValueError('Nonfinite specimen parameter: ' + name)
            if len(set(values)) != len(values) or min(values) < 0 or (name == 'preferred_orientation' and min(values) <= 0):
                raise ValueError('Invalid/duplicate specimen parameter: ' + name)
        if name == 'displacement_parameters' and spec.get('sampling') != 'per_phase_isotropic':
            raise ValueError('Displacement sampling must be per_phase_isotropic')
        if name == 'preferred_orientation':
            axes = spec.get('axes')
            if spec.get('model') != 'march_dollase' or not isinstance(axes, list) or not axes or len(axes) > 6:
                raise ValueError('Preferred orientation needs March-Dollase and 1..6 axes')
            for hkl in axes:
                if not isinstance(hkl, list) or len(hkl) != 3 or not any(hkl) or any(type(v) is not int for v in hkl):
                    raise ValueError('Preferred-orientation axes must be nonzero integer hkl triples')
        if name == 'microstrain' and 'anisotropy' in spec:
            _anisotropy(spec['anisotropy'])
    return settings


def enabled(protocol, name):
    return effect_settings(protocol).get(name, {}).get('enabled', False)


def has_profile_effects(protocol):
    return any(enabled(protocol, k) for k in KEYS - {'displacement_parameters'})


def has_phase_profile_effects(protocol):
    return any(enabled(protocol, k) for k in PHASE_KEYS - {'displacement_parameters'})


def continuous_profiles(protocol):
    settings = effect_settings(protocol)
    return any(s.get('enabled') and 'distribution' in s
               for k, s in settings.items() if k in PHASE_KEYS - {'displacement_parameters'})


def continuous_bounds(protocol):
    """Versioned evaluator bounds; no realized specimen values are accepted."""
    settings = effect_settings(protocol)
    result = {}
    for name, field, inactive in [('phase_specific_sizes','size_um',None),
                                 ('microstrain','microstrain_ppm',[0.,0.]),
                                 ('preferred_orientation','md_ratio',[1.,1.])]:
        spec = settings.get(name,{})
        if spec.get('enabled'):
            if 'distribution' not in spec:
                raise ValueError('Enabled profile effects must use one common continuous or legacy grid mode')
            result[field] = spec['range']
        else:
            result[field] = inactive
    return result


def _rng(seed, phase_id, effect):
    digest = hashlib.sha256((phase_id + ':' + effect).encode()).digest()
    words = [int.from_bytes(digest[i:i+4], 'little') for i in range(0, 16, 4)]
    return np.random.default_rng(np.random.SeedSequence([seed, *words]))


def realize_specimen(recipe, protocol):
    settings = effect_settings(protocol)
    control = recipe.get('specimen_control', False)
    if type(control) is not bool:
        raise ValueError('specimen_control must be boolean')
    result = []
    for row in recipe['phases']:
        phase = row['id']
        select = lambda effect, values: values[int(_rng(recipe['seed'], phase, effect).integers(len(values)))]
        def draw(name, effect, legacy_values, inactive):
            if control or not enabled(protocol, name):
                return inactive
            spec = settings[name]
            if 'distribution' not in spec:
                return select(effect, legacy_values)
            rng = _rng(recipe['seed'], phase, effect)
            if rng.random() >= spec.get('probability', 1.):
                return inactive
            lo, hi = spec['range']
            return float(np.exp(rng.uniform(np.log(lo), np.log(hi)))) if spec['distribution'] == 'log_uniform' else float(rng.uniform(lo, hi))
        size = draw('phase_specific_sizes', 'size', protocol['generation']['domain_size_um'], recipe['domain_size_um'])
        strain = draw('microstrain', 'strain', settings.get('microstrain', {}).get('values_ppm'), 0.)
        # Uniaxial anisotropy: the axial strain is the equatorial strain times a drawn ratio.
        axial, strain_axis = strain, [0, 0, 1]
        anisotropy = settings.get('microstrain', {}).get('anisotropy')
        if anisotropy and strain > 0 and not control:
            rng = _rng(recipe['seed'], phase, 'strain_anisotropy')
            if rng.random() < anisotropy.get('probability', 1.):
                axial = strain * _draw(rng, anisotropy['axial_ratio'])
                strain_axis = select('strain_axis', anisotropy['axes'])
        ratio, axis = 1., [0, 0, 1]
        if enabled(protocol, 'preferred_orientation') and not control:
            ratio = draw('preferred_orientation', 'orientation_ratio', settings['preferred_orientation'].get('ratios'), 1.)
            axis = select('orientation_axis', settings['preferred_orientation']['axes'])
        uiso = draw('displacement_parameters', 'uiso', settings.get('displacement_parameters', {}).get('values_A2'),
                    protocol['generation'].get('source_model_Uiso_A2', .005)) if enabled(protocol, 'displacement_parameters') else None
        result.append({'id': phase, 'size_um': float(size), 'microstrain_ppm': float(strain),
                       'microstrain_axial_ppm': float(axial), 'microstrain_axis': list(strain_axis),
                       'md_ratio': float(ratio), 'md_axis': list(axis), 'uiso_A2': None if uiso is None else float(uiso)})
    return result


MISMATCH_CAPS = {'cell_strain': .005, 'position_rms_A': .08}


def _mismatch_distribution(dist, name, cap):
    if not isinstance(dist, dict) or set(dist) != {'distribution', 'range'} or dist['distribution'] not in {'uniform', 'log_uniform'}:
        raise ValueError(name + ' needs a uniform or log_uniform distribution and range')
    low, high = _bounds(dist['range'], name, positive=dist['distribution'] == 'log_uniform')
    if low < 0 or high > cap:
        raise ValueError('%s must lie within [0, %g]' % (name, cap))


def mismatch_settings(protocol):
    spec = protocol['generation'].get('reference_mismatch', {'enabled': False})
    if type(spec.get('enabled')) is not bool or set(spec) - {'enabled', 'cell_strain', 'position_rms_A', 'position_rms_A_by_element', 'probability'}:
        raise ValueError('Invalid reference-mismatch configuration')
    if not spec['enabled']:
        return spec
    if spec.get('cell_strain') is None and spec.get('position_rms_A') is None:
        raise ValueError('reference_mismatch needs cell_strain, position_rms_A or both')
    for name, cap in MISMATCH_CAPS.items():
        if spec.get(name) is not None:
            _mismatch_distribution(spec[name], 'reference_mismatch.' + name, cap)
    by_element = spec.get('position_rms_A_by_element')
    if by_element is not None:
        if spec.get('position_rms_A') is None or not isinstance(by_element, dict) or not by_element:
            raise ValueError('position_rms_A_by_element needs a default position_rms_A and at least one element')
        for element, dist in by_element.items():
            if not isinstance(element, str) or not element.isalpha() or not element[0].isupper():
                raise ValueError('position_rms_A_by_element keys are element symbols')
            _mismatch_distribution(dist, 'reference_mismatch.position_rms_A_by_element.' + element, MISMATCH_CAPS['position_rms_A'])
    _probability(spec, 'reference_mismatch')
    return spec


def _draw(rng, dist):
    lo, hi = dist['range']
    if dist['distribution'] == 'log_uniform':
        return float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    return float(rng.uniform(lo, hi))


def realize_mismatch(recipe, protocol):
    """Per-phase difference between the true structure and its registered library model, or None.

    A property of the sample's phases rather than of specimen preparation, so specimen-control
    cases keep it; twins with one seed share it.
    """
    spec = mismatch_settings(protocol)
    result = []
    for row in recipe['phases']:
        rng = _rng(recipe['seed'], row['id'], 'reference_mismatch')
        if not spec['enabled'] or rng.random() >= spec.get('probability', 1.):
            result.append(None)
            continue
        draws = {}
        for name in ['cell_strain', 'position_rms_A']:
            dist = spec.get(name)
            draws[name] = 0. if dist is None else _draw(rng, dist)
        # Element-specific coordinate mismatch (light atoms are usually less well
        # determined in published refinements) is drawn after the defaults.
        draws['position_rms_A_by_element'] = {el: _draw(rng, dist) for el, dist in sorted((spec.get('position_rms_A_by_element') or {}).items())}
        result.append({**draws, 'seed': int(rng.integers(2**31))})
    return result


def forward_spec(row):
    spec = {k: row[k] for k in ('size_um', 'microstrain_ppm', 'md_ratio', 'md_axis')}
    axial = row.get('microstrain_axial_ppm', row['microstrain_ppm'])
    if axial != row['microstrain_ppm']:  # isotropic phases keep the original request form and cache keys
        spec.update(microstrain_axial_ppm=axial, microstrain_axis=list(row['microstrain_axis']))
    return spec


def suortti(A, B, two_theta_deg):
    """GSAS-II SurfaceRough (Suortti 1972): relative intensity, 1 at 2theta=180."""
    s = np.sin(np.deg2rad(np.asarray(two_theta_deg, float) / 2))
    return (A + (1 - A) * np.exp(-B / s)) / (A + (1 - A) * np.exp(-B))


def displacement_shift_deg(shift_um, two_theta_deg, radius_mm=GONIOMETER_RADIUS_MM):
    """GSAS-II Bragg-Brentano peak displacement in degrees 2theta (negative for positive Shift)."""
    theta = np.deg2rad(np.asarray(two_theta_deg, float) / 2)
    return -9e-2 / (np.pi * radius_mm) * 4 * shift_um * np.cos(theta)


def realize_sample(recipe, protocol):
    """Whole-specimen effects shared by every phase of one scan.

    Seeded from the recipe seed with their own tags: enabling them never
    consumes the noise, background, offset or per-phase specimen streams.
    """
    settings = effect_settings(protocol)
    control = recipe.get('specimen_control', False)
    if type(control) is not bool:
        raise ValueError('specimen_control must be boolean')
    radius = float(settings.get('specimen_displacement', {}).get('goniometer_radius_mm', GONIOMETER_RADIUS_MM))
    result = {'shift_um': 0., 'surf_rough_A': 0., 'surf_rough_B': 0., 'transparency': 0.,
              'goniometer_radius_mm': radius}
    if control:
        return result
    spec = settings.get('specimen_displacement', {})
    if spec.get('enabled'):
        rng = _rng(recipe['seed'], '__specimen__', 'displacement')
        if rng.random() < spec.get('probability', 1.):
            result['shift_um'] = float(rng.uniform(*spec['range_um']))
    spec = settings.get('surface_roughness', {})
    if spec.get('enabled'):
        rng = _rng(recipe['seed'], '__specimen__', 'roughness')
        if rng.random() < spec.get('probability', 1.):
            # Bounded rejection keeps the low-angle deficit physically moderate;
            # the stream is deterministic, so the draw is reproducible.
            for _ in range(1000):
                A = float(rng.uniform(*spec['A_range']))
                lo, hi = spec['B_range']
                B = float(np.exp(rng.uniform(np.log(lo), np.log(hi)))) if spec['B_distribution'] == 'log_uniform' else float(rng.uniform(lo, hi))
                if 1 - float(suortti(A, B, spec['deficit_reference_2theta_deg'])) <= spec['max_low_angle_deficit']:
                    result.update(surf_rough_A=A, surf_rough_B=B)
                    break
            else:
                raise ValueError('Roughness bounds admit no draw within the deficit cap')
    return result


def sample_spec(sample):
    """GSAS-II sample-parameter values for the forward calculation."""
    return {k: float(sample[k]) for k in ('shift_um', 'surf_rough_A', 'surf_rough_B', 'transparency', 'goniometer_radius_mm')}


def profile_options(protocol, common_size):
    """Candidate settings independent of truth or submitted phase labels."""
    s = effect_settings(protocol)
    if continuous_profiles(protocol):
        raise ValueError('Continuous specimen profiles require the continuous observed-data evaluator')
    sizes = protocol['generation']['domain_size_um'] if enabled(protocol, 'phase_specific_sizes') else [common_size]
    strains = s['microstrain']['values_ppm'] if enabled(protocol, 'microstrain') else [0.]
    orientations = [(1., [0, 0, 1])]
    if enabled(protocol, 'preferred_orientation'):
        orientations = [(float(r), a) for r in s['preferred_orientation']['ratios']
                        for a in (s['preferred_orientation']['axes'] if r != 1 else [[0, 0, 1]])]
    options = [{'size_um': float(size), 'microstrain_ppm': float(strain), 'md_ratio': float(ratio), 'md_axis': list(axis)}
               for size, strain, (ratio, axis) in product(sizes, strains, orientations)]
    if len(options) > 512:
        raise ValueError('Optional specimen grid exceeds 512 settings per phase; reduce lab grid before generation')
    return options


def apply_uiso(source, destination, value):
    """Change only registered scalar Uiso values, never positions/occupancies."""
    from pymatgen.io.cif import CifFile
    cif = CifFile.from_str(Path(source).read_text())
    for block in cif.data.values():
        tag = '_atom_site_U_iso_or_equiv'
        if tag not in block.data or '_atom_site_aniso_label' in block.data:
            raise ValueError('Thermal variation requires a registered isotropic starting model')
        block.data[tag] = [f'{value:.10f}'] * len(block.data['_atom_site_label'])
    Path(destination).write_text(str(cif) + '\n')
