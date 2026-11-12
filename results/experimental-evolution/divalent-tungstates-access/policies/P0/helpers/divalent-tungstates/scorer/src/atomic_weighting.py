"""Scattering-weighted population weighting on an already registered common cell.

N_e is the larger occupied count of element e in the two structures and Z_e its atomic
number, a proxy for X-ray scattering power. The weight of element e is Z_e N_e / sum Z N,
so a transported population t of element e contributes t Z_e / sum Z N before the distance
kernel. Positions the pattern barely sees (light atoms, few atoms) therefore carry little
credit, and misplacing them costs little; heavy atoms that shape the pattern carry most of it.
Missing and invented elements stay in the denominator and earn no credit.
"""
from __future__ import annotations
from collections import defaultdict
import math

NAME = 'scattering_population'


def atomic_number(element):
    from pymatgen.core.periodic_table import Element
    return float(Element(element).Z)


def factors(maximum):
    """Per-population credit factor for each element: Z_e / sum_e Z_e N_e."""
    denominator = math.fsum(atomic_number(e) * n for e, n in maximum.items())
    if denominator <= 0:
        raise ValueError('An empty atomic population is not a structure')
    return {e: atomic_number(e) / denominator for e in maximum}


def occupied_counts(sites):
    """Count expanded sites, including fractional occupancies, in a common cell."""
    counts = defaultdict(float)
    for site in sites:
        for element, population in site['species'].items():
            if not math.isfinite(population) or population < 0:
                raise ValueError('Invalid occupied atomic population')
            counts[element] += population
    return dict(counts)


def weighted_populations(reference, submitted, transport):
    """Return normalized transport coefficients and an inspectable breakdown.

    The caller supplies element symbols and capacity-constrained same-element
    transport. Atom labels and oxidation-state labels must be removed upstream.
    This changes grading, not positions, occupancies, or the geometric matching.
    """
    for counts in (reference, submitted):
        if any(not math.isfinite(v) or v < 0 for v in counts.values()):
            raise ValueError('Invalid occupied atomic population')
    elements = sorted(set(reference) | set(submitted))
    maximum = {e: max(reference.get(e, 0.), submitted.get(e, 0.)) for e in elements}
    maximum = {e: n for e, n in maximum.items() if n > 0}
    if not maximum:
        raise ValueError('An empty atomic population is not a structure')
    factor = factors(maximum)
    matched = defaultdict(float)
    out = []
    for row in transport:
        e, population, distance = row['element'], row['population'], row['distance_A']
        if e not in maximum or not math.isfinite(population) or population < 0:
            raise ValueError('Invalid transported atomic population')
        if not math.isfinite(distance) or distance < 0:
            raise ValueError('Invalid atomic distance')
        if population == 0:
            continue
        matched[e] += population
        out.append(dict(element=e, population=population, distance_A=distance,
                        coefficient=population * factor[e]))
    for e, n in matched.items():
        capacity = min(reference.get(e, 0.), submitted.get(e, 0.))
        if n > capacity + 1e-9 * max(capacity, 1e-12):
            raise ValueError('Transport exceeds same-element occupied capacity')
    breakdown = [dict(element=e, reference_population=reference.get(e, 0.),
                      submitted_population=submitted.get(e, 0.), maximum_population=maximum[e],
                      atomic_number=atomic_number(e), element_weight=factor[e] * maximum[e],
                      transported_population=matched[e],
                      population_overlap=matched[e] / maximum[e]) for e in maximum]
    return out, breakdown


def exact_population_feature(counts, cell_error=0., distances=None):
    """Analytic precision fixture: the same populations, optionally displaced."""
    distances = distances or {}
    flow = [dict(element=e, population=n, distance_A=distances.get(e, 0.))
            for e, n in counts.items() if n > 0]
    populations, elements = weighted_populations(counts, counts, flow)
    return dict(cell_error=cell_error, populations=populations,
                element_populations=elements, atomic_weighting=NAME,
                population_overlap=math.fsum(p['coefficient'] for p in populations))
