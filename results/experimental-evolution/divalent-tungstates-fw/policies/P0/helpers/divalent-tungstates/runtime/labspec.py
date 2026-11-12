"""Read the simulated laboratory from LAB.md.

LAB.md carries one fenced code block whose info string is `json lab-settings`. It defines everything
specific to the laboratory: measurement, specimen distributions and the form of the solver inputs.
protocol(LAB.md) combines it with the lab-independent generator_defaults.json into the protocol the
generator uses. Nothing about any particular lab is built into the generator.
"""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
FENCE = re.compile(r'^```json lab-settings[ \t]*\n(.*?)^```[ \t]*$', re.M | re.S)
TOP = {'schema', 'lab_id', 'measurement', 'specimen', 'solver_inputs'}
MEASUREMENT = {'geometry', 'goniometer_radius_mm', 'radiation', 'grid_deg', 'peak_counts', 'zero_offset_deg',
               'instrument_profile', 'background'}
SPECIMEN = {'displacement_um', 'surface_roughness', 'crystallite_size_um', 'microstrain_ppm',
            'preferred_orientation', 'uiso_A2', 'reference_mismatch', 'control_size_um'}
INPUTS = {'pattern_columns', 'line_ending', 'sample_fields', 'element_sources', 'metadata'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def settings(lab_md):
    text = Path(lab_md).read_text()
    blocks = FENCE.findall(text)
    if len(blocks) != 1:
        raise ValueError('LAB.md needs exactly one ```json lab-settings block; found %d' % len(blocks))
    data = json.loads(blocks[0])
    _keys(data, TOP, 'lab settings')
    if data['schema'] != 'pxrd-lab-settings/1':
        raise ValueError('Unknown lab settings schema: ' + str(data['schema']))
    _keys(data['measurement'], MEASUREMENT, 'measurement')
    _keys(data['specimen'], SPECIMEN, 'specimen', required=False)
    _keys(data['solver_inputs'], INPUTS, 'solver_inputs')
    m = data['measurement']
    if m['geometry'] != 'bragg_brentano':
        raise ValueError('Only bragg_brentano geometry is implemented')
    if set(m['radiation']) != {'wavelength_ka1_A', 'wavelength_ka2_A', 'ka2_ka1_ratio'}:
        raise ValueError('radiation needs wavelength_ka1_A, wavelength_ka2_A (null for one wavelength) and ka2_ka1_ratio')
    if set(m['grid_deg']) != {'min', 'max', 'step'}:
        raise ValueError('grid_deg needs min, max and step')
    if set(m['instrument_profile']) != {'U', 'W', 'X', 'SH_L', 'polarization'}:
        raise ValueError('instrument_profile needs distributions for U, W, X, SH_L and polarization')
    return data


def _keys(block, allowed, name, required=True):
    if not isinstance(block, dict):
        raise ValueError(name + ' must be an object')
    unknown, missing = set(block) - allowed, allowed - set(block)
    if unknown:
        raise ValueError('Unknown %s fields: %s' % (name, ', '.join(sorted(unknown))))
    if required and missing:
        raise ValueError('Missing %s fields: %s' % (name, ', '.join(sorted(missing))))


def _middle(spec):
    low, high = spec['range']
    return float((low * high) ** .5 if spec['distribution'] == 'log_uniform' else (low + high) / 2)


def _effect(spec, **fixed):
    """An omitted effect, or one with "enabled": false, is off."""
    if spec is None or spec.get('enabled') is False:
        return {'enabled': False}
    return {'enabled': True, **{k: v for k, v in spec.items() if k != 'enabled'}, **fixed}


def protocol(lab_md):
    lab = settings(lab_md)
    defaults = json.loads((HERE / 'generator_defaults.json').read_text())
    m, s = lab['measurement'], lab['specimen']
    profile = m['instrument_profile']
    radiation = m['radiation']
    instrument = {**radiation, 'polarization': _middle(profile['polarization']), 'V': 0.0, 'zero_deg': 0.0,
                  **{k: _middle(profile[k]) for k in ['U', 'W', 'X', 'SH_L']}}
    if radiation['wavelength_ka2_A'] is None:
        instrument['ka2_ka1_ratio'] = 0.0
    g = defaults['generation']
    roughness = _effect(s.get('surface_roughness'))
    generation = {
        'training_cases': g['training_cases'], 'max_components': g['max_components'], 'noise': g['noise'],
        'source_model_Uiso_A2': g['source_model_Uiso_A2'], 'availability': g['availability'],
        'selection': g['selection'], 'fraction_constraint': g['fraction_constraint'],
        'reference_variation': g['reference_variation'],
        'reference_mismatch': _effect(s.get('reference_mismatch')),
        'peak_counts': m['peak_counts'], 'domain_size_um': s.get('control_size_um', [1.0]),
        'background': m['background'],
        'angular_offset': {'enabled': True, 'distribution': m['zero_offset_deg']['distribution'],
                           'range_deg': m['zero_offset_deg']['range']},
        'instrument_uncertainty': {'enabled': True, 'seed': g['instrument_seed'], 'parameters': profile},
        'specimen_effects': {
            'microstrain': _effect(s.get('microstrain_ppm')),
            'preferred_orientation': _effect(s.get('preferred_orientation')),
            'phase_specific_sizes': _effect(s.get('crystallite_size_um')),
            'displacement_parameters': _effect(s.get('uiso_A2'), sampling='per_phase_isotropic'),
            'specimen_displacement': _effect(s.get('displacement_um'), goniometer_radius_mm=m['goniometer_radius_mm']),
            'surface_roughness': roughness},
        'solver_inputs': lab['solver_inputs'],
    }
    # Validation of the internal schemas happens where each part is used (specimen, measurement, backgrounds).
    eff = generation['specimen_effects']['specimen_displacement']
    if eff['enabled']:
        eff['range_um'] = eff.pop('range')
    return {'schema_version': 1, 'protocol_id': 'lab:' + lab['lab_id'], 'lab_id': lab['lab_id'],
            'lab_sha256': sha(lab_md), 'instrument': instrument,
            'grid': {k: float(v) for k, v in m['grid_deg'].items()}, 'generation': generation,
            'verification': defaults['verification'], 'solver_evaluation': defaults['solver_evaluation']}
