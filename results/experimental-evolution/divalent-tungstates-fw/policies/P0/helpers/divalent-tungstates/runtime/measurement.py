"""Versioned angular-zero generation and evaluator calibration conventions.

Only the evaluator/researcher sees realized calibration. Workers receive nominal
instrument parameters and their calibration status, never seeds or realizations.
"""
from copy import deepcopy
import hashlib
import math
import numpy as np


KNOWN_ZERO = 'known_generating_zero'
LEGACY_ZERO = 'legacy_fitted_zero'


def instrument_settings(protocol):
    settings = protocol['generation'].get('instrument_uncertainty')
    if settings is None:
        return None
    if set(settings) != {'enabled', 'parameters', 'seed'} or type(settings['enabled']) is not bool:
        raise ValueError('Invalid instrument_uncertainty configuration')
    if type(settings['seed']) is not int or not 0 <= settings['seed'] < 2**32:
        raise ValueError('Instrument seed must be uint32')
    if set(settings['parameters']) != {'U', 'W', 'X', 'SH_L', 'polarization'}:
        raise ValueError('Use the audited Cu Kalpha instrumental parameter family')
    for name, spec in settings['parameters'].items():
        if set(spec) != {'distribution', 'range'} or spec['distribution'] not in {'uniform', 'log_uniform'}:
            raise ValueError('Invalid instrumental sampling specification: ' + name)
        bounds = spec['range']
        if (not isinstance(bounds, list) or len(bounds) != 2 or
                any(type(v) not in (int, float) or not math.isfinite(v) for v in bounds) or
                not 0 <= bounds[0] < bounds[1] or
                (spec['distribution'] == 'log_uniform' and bounds[0] <= 0) or
                (name == 'polarization' and bounds[1] > 1)):
            raise ValueError('Invalid instrumental bounds: ' + name)
    if float(protocol['instrument'].get('V', 0)) != 0:
        raise ValueError('Audited random profile uses V=0 and nonnegative U/W/X')
    return settings


def realized_instrument(recipe, protocol):
    """Session-level instrument draw, independent of case/noise/specimen seeds."""
    result = deepcopy(protocol['instrument'])
    settings = instrument_settings(protocol)
    if not settings or not settings['enabled']:
        return result
    session = recipe.get('measurement_session')
    if not isinstance(session, str) or not session.strip() or len(session) > 100:
        raise ValueError('Uncalibrated cases require a private measurement_session identifier')
    digest = hashlib.sha256(session.encode()).digest()
    words = [int.from_bytes(digest[i:i+4], 'little') for i in range(0, 16, 4)]
    rng = np.random.default_rng(np.random.SeedSequence([settings['seed'], *words]))
    for name, spec in sorted(settings['parameters'].items()):
        lo, hi = spec['range']
        result[name] = float(np.exp(rng.uniform(np.log(lo), np.log(hi)))) if spec['distribution'] == 'log_uniform' else float(rng.uniform(lo, hi))
    return result


def offset_settings(protocol):
    settings = protocol['generation'].get('angular_offset')
    if settings is None:
        return None
    if set(settings) - {'enabled', 'distribution', 'range_deg'}:
        raise ValueError('Unknown angular_offset configuration field')
    if type(settings.get('enabled')) is not bool:
        raise ValueError('angular_offset.enabled must be boolean')
    if settings.get('distribution') != 'uniform':
        raise ValueError('Only uniform angular-offset generation is supported')
    bounds = settings.get('range_deg')
    if not isinstance(bounds, list) or len(bounds) != 2:
        raise ValueError('angular_offset.range_deg must contain two bounds')
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in bounds):
        raise ValueError('Angular-offset bounds must be finite degrees in 2theta')
    if not bounds[0] < bounds[1] or not bounds[0] <= 0 <= bounds[1]:
        raise ValueError('Angular-offset bounds must be increasing and include zero')
    return settings


def generate_measurement(recipe, protocol):
    settings = offset_settings(protocol)
    control = recipe.get('angular_offset_control', False)
    if type(control) is not bool:
        raise ValueError('angular_offset_control must be boolean')
    nominal = float(protocol['instrument'].get('zero_deg', 0.))
    if not math.isfinite(nominal):
        raise ValueError('Nonfinite nominal angular zero')
    if settings is None or not settings['enabled']:
        delta = 0.
        source = 'supplied_calibration'
    elif control:
        delta = 0.
        source = 'zero_offset_control'
    else:
        # Independent stream: enabling offsets never consumes the noise RNG.
        rng = np.random.default_rng(np.random.SeedSequence([recipe['seed'], 0x5A45524F]))
        delta = float(rng.uniform(*settings['range_deg']))
        source = 'seeded_uniform_offset'
    result = {'schema_version': 1, 'nominal_zero_deg': nominal,
            'applied_offset_deg': delta, 'true_zero_deg': nominal + delta,
            'source': source, 'units': 'degrees_2theta',
            'convention': 'positive offset shifts reflections to higher recorded 2theta; GSAS-II Zero',
            'public_zero_status': 'unknown' if settings and settings['enabled'] else 'calibrated',
            'rng': 'SeedSequence([noise_seed, 0x5A45524F]); separate from Poisson RNG'}
    instrument = instrument_settings(protocol)
    if instrument is not None:
        actual = realized_instrument(recipe, protocol)
        actual['zero_deg'] = nominal + delta
        result.update(schema_version=2, true_instrument=actual,
                      measurement_session=recipe.get('measurement_session'),
                      public_instrument_status='unknown' if instrument['enabled'] else 'calibrated')
    return result


def uses_known_zero(protocol):
    mode = protocol.get('verification', {}).get('angular_zero_mode', LEGACY_ZERO)
    if mode not in {KNOWN_ZERO, LEGACY_ZERO}:
        raise ValueError('Unknown evaluator angular-zero mode: ' + str(mode))
    return mode == KNOWN_ZERO


def evaluation_protocol(truth):
    """Use true calibration, but no hidden means/structures, to build predictions.

    Legacy cases keep their old +/-0.05 degree nuisance search. New cases fix the
    absolute generating zero and permit no extra shift in the evaluator.
    """
    protocol = deepcopy(truth['protocol'])
    if not uses_known_zero(protocol):
        if offset_settings(protocol) and offset_settings(protocol)['enabled']:
            raise ValueError('Hidden offsets require known-generating-zero evaluation')
        return protocol
    measurement = truth.get('measurement')
    if measurement is None:
        raise ValueError('Known-zero evaluation requires realized measurement provenance')
    zero = float(measurement['true_zero_deg'])
    if not math.isfinite(zero):
        raise ValueError('Invalid generating angular zero')
    forward_zero = float(truth['forward']['instrument']['zero_deg'])
    if zero != forward_zero:
        raise ValueError('Generating zero disagrees with forward-calculation provenance')
    expected = generate_measurement(truth['recipe'], truth['protocol'])
    if measurement != expected:
        raise ValueError('Generating offset disagrees with its frozen seed/configuration')
    if 'true_instrument' in measurement:
        if measurement['true_instrument'] != truth['forward']['instrument']:
            raise ValueError('Generating instrument disagrees with native forward provenance')
        protocol['instrument'] = deepcopy(measurement['true_instrument'])
    else:
        protocol['instrument']['zero_deg'] = zero
    return protocol


def calibration_diagnostic(protocol):
    known = uses_known_zero(protocol)
    return {'mode': KNOWN_ZERO if known else LEGACY_ZERO,
            'generating_zero_used_by_evaluator': known,
            'fixed_zero_deg': float(protocol['instrument'].get('zero_deg', 0.)) if known else None,
            'additional_zero_refined': not known,
            'generating_instrument_used_by_evaluator': bool(known and instrument_settings(protocol)),
            'scope': 'Structures and fractions evaluated under the versioned generating calibration; '
                     'does not certify the solver estimated calibration correctly.' if known else
                     'Historical calibration plus fitted common zero within +/-0.05 degree.'}
