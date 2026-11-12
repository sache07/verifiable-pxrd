"""Seeded, positive, broad backgrounds; realizations belong to private truth.

Generation audits know the sampled shape parameters and refit its nonnegative
amplitudes. This is an oracle self-consistency/detectability check, not the solver
evaluation or a claim that an experimental background has a unique form.
"""
import math
import numpy as np

FAMILIES = ('simple', 'exponential', 'power_law')
RNG_TAG = 0x42474E44


def _number(x):
    return type(x) in (int, float) and np.isfinite(x)


def _bounds(config, key, minimum=0.):
    value = config.get(key)
    if (not isinstance(value, list) or len(value) != 2
            or not all(_number(x) for x in value)
            or not minimum <= value[0] < value[1]):
        raise ValueError(f'Invalid background {key}')
    return value


def background_settings(protocol):
    config = protocol['generation']['background']
    if isinstance(config, str):
        return None  # Existing protocols keep their exact Bernstein calculation.
    keys = {'mode', 'family_weights', 'floor_counts', 'high_floor_probability',
            'high_floor_counts', 'tail_counts', 'high_floor_tail_counts',
            'decay_length_deg', 'power_exponent'}
    if (not isinstance(config, dict) or set(config) != keys
            or config['mode'] != 'sampled_families_v1'):
        raise ValueError('Unsupported background configuration')
    weights = config['family_weights']
    if (not isinstance(weights, dict) or set(weights) != set(FAMILIES)
            or not all(_number(x) and x >= 0 for x in weights.values())
            or sum(weights.values()) <= 0):
        raise ValueError('Invalid background family_weights')
    for key in ['floor_counts', 'high_floor_counts']:
        _bounds(config, key, minimum=1.)
    for key in ['tail_counts', 'high_floor_tail_counts']:
        _bounds(config, key)
    # These are broad continuum terms, not additional diffraction peaks.
    _bounds(config, 'decay_length_deg', minimum=5.)
    low, high = _bounds(config, 'power_exponent', minimum=1.)
    if high > 3.:
        raise ValueError('Background power exponents above 3 are outside this lab preset')
    p = config['high_floor_probability']
    if not _number(p) or not 0 <= p <= 1:
        raise ValueError('Invalid background high_floor_probability')
    return config


def realize_background(recipe, protocol):
    config = background_settings(protocol)
    if config is None:
        if 'background_family' in recipe:
            raise ValueError('background_family requires a sampled-background protocol')
        raw = recipe.get('background_counts')
        if (not isinstance(raw, list) or len(raw) != 3
                or not all(_number(v) and 10 <= v <= 500 for v in raw)):
            raise ValueError('background_counts: three Bernstein coefficients in [10,500]')
        return {'version': 0, 'family': 'legacy_quadratic', 'degree': 2,
                'floor_coefficients_counts': list(map(float, raw))}
    if 'background_counts' in recipe:
        raise ValueError('Background counts are sampled automatically; omit background_counts')
    seed = recipe.get('seed')
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError('Background seed must be uint32')
    family = recipe.get('background_family', 'auto')
    if family not in (*FAMILIES, 'auto'):
        raise ValueError('background_family must be auto, simple, exponential, or power_law')
    # Never consume the Poisson, instrument, offset, or specimen random streams.
    rng = np.random.default_rng(np.random.SeedSequence([seed, RNG_TAG]))
    weights = np.array([config['family_weights'][name] for name in FAMILIES], float)
    sampled_family = str(rng.choice(FAMILIES, p=weights/weights.sum()))
    if family == 'auto':
        family = sampled_family
    high_floor = bool(rng.random() < config['high_floor_probability'])
    limits = config['high_floor_counts' if high_floor else 'floor_counts']
    center = float(rng.uniform(*limits))
    span = .25*(limits[1]-limits[0])
    # Correlated coefficients keep the floor gentle while allowing either slope.
    floor = rng.uniform(max(limits[0], center-span), min(limits[1], center+span), 3)
    degree = int(rng.integers(0, 3)) if family == 'simple' else 2
    amplitude = float(rng.uniform(*config['high_floor_tail_counts' if high_floor else 'tail_counts']))
    scale = float(np.exp(rng.uniform(*np.log(config['decay_length_deg']))))
    power = float(rng.uniform(*config['power_exponent']))
    return {'version': 1, 'family': family, 'degree': degree,
            'floor_coefficients_counts': floor[:degree+1].tolist(),
            'high_floor': high_floor,
            'tail_amplitude_counts': amplitude if family != 'simple' else 0.,
            'decay_length_deg': scale if family != 'simple' else None,
            'power_exponent': power if family == 'power_law' else None,
            'rng': 'SeedSequence([recipe.seed, 0x42474E44]); independent of noise and measurement'}


def background_basis(x, realization):
    x = np.asarray(x, float)
    if x.ndim != 1 or len(x) < 2 or not np.all(np.isfinite(x)) or np.any(np.diff(x) <= 0):
        raise ValueError('Background requires a finite increasing one-dimensional grid')
    t = (x-x[0])/(x[-1]-x[0])
    degree = realization['degree']
    if degree not in (0, 1, 2):
        raise ValueError('Unsupported background floor degree')
    columns = [math.comb(degree, k)*t**k*(1-t)**(degree-k) for k in range(degree+1)]
    family = realization['family']
    if family == 'exponential':
        columns.append(np.exp(-(x-x[0])/realization['decay_length_deg']))
    elif family == 'power_law':
        columns.append((1+(x-x[0])/realization['decay_length_deg'])**(-realization['power_exponent']))
    elif family not in ('simple', 'legacy_quadratic'):
        raise ValueError('Unsupported background family')
    return np.column_stack(columns)


def sample_background(x, recipe, protocol):
    realization = realize_background(recipe, protocol)
    basis = background_basis(x, realization)
    coefficients = realization['floor_coefficients_counts'].copy()
    if realization['family'] in ('exponential', 'power_law'):
        coefficients.append(realization['tail_amplitude_counts'])
    counts = basis @ np.asarray(coefficients)
    if not np.all(np.isfinite(counts)) or np.any(counts <= 0):
        raise ValueError('Sampled background must be finite and positive')
    return counts, basis, realization
