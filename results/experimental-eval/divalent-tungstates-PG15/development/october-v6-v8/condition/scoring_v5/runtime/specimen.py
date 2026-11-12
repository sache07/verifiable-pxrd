"""Versioned finite-grid and continuous specimen distributions.

Realizations are private; profile bounds are fixed before seeing outcomes.
"""
from itertools import product
from pathlib import Path
import hashlib
import math
import numpy as np


KEYS = {'microstrain', 'preferred_orientation', 'phase_specific_sizes', 'displacement_parameters'}


def effect_settings(protocol):
    settings = protocol['generation'].get('specimen_effects', {})
    if set(settings) - KEYS:
        raise ValueError('Unknown specimen effect')
    for name, spec in settings.items():
        fields = {'enabled'}
        fields |= {'values_ppm'} if name == 'microstrain' else set()
        fields |= {'ratios', 'axes', 'model'} if name == 'preferred_orientation' else set()
        fields |= {'values_A2', 'sampling'} if name == 'displacement_parameters' else set()
        fields |= {'distribution', 'range', 'probability'}
        if set(spec) - fields or type(spec.get('enabled')) is not bool:
            raise ValueError('Invalid specimen-effect configuration: ' + name)
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
    return settings


def enabled(protocol, name):
    return effect_settings(protocol).get(name, {}).get('enabled', False)


def has_profile_effects(protocol):
    return any(enabled(protocol, k) for k in KEYS - {'displacement_parameters'})


def continuous_profiles(protocol):
    settings = effect_settings(protocol)
    return any(s.get('enabled') and 'distribution' in s
               for k, s in settings.items() if k != 'displacement_parameters')


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
        ratio, axis = 1., [0, 0, 1]
        if enabled(protocol, 'preferred_orientation') and not control:
            ratio = draw('preferred_orientation', 'orientation_ratio', settings['preferred_orientation'].get('ratios'), 1.)
            axis = select('orientation_axis', settings['preferred_orientation']['axes'])
        uiso = draw('displacement_parameters', 'uiso', settings.get('displacement_parameters', {}).get('values_A2'),
                    protocol['generation'].get('source_model_Uiso_A2', .005)) if enabled(protocol, 'displacement_parameters') else None
        result.append({'id': phase, 'size_um': float(size), 'microstrain_ppm': float(strain),
                       'md_ratio': float(ratio), 'md_axis': list(axis), 'uiso_A2': None if uiso is None else float(uiso)})
    return result


def forward_spec(row):
    return {k: row[k] for k in ('size_um', 'microstrain_ppm', 'md_ratio', 'md_axis')}


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
