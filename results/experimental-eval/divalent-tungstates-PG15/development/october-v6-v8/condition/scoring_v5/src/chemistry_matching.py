"""Pairwise substitution-aware geometry and continuous chemical correspondence.

Only elements actually co-occupying a site in one of the two CIFs are grouped.
The grouping permits alignment, never changes the scored or forward-calculated
model. Original species, vacancies and site indices survive cell transforms.
"""
from functools import lru_cache
import numpy as np
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from structure_metrics import matcher, occupancy_vector, comp_distance


def substitution_neutral_pair(a, b):
    elements = sorted(set(a.composition.get_el_amt_dict()) | set(b.composition.get_el_amt_dict()))
    parent = {e: e for e in elements}

    def root(e):
        while parent[e] != e:
            e = parent[e]
        return e

    for st in (a, b):
        for site in st:
            support = sorted(e.symbol for e, v in site.species.items() if v > 0)
            for e in support[1:]:
                x, y = sorted((root(support[0]), root(e)))
                parent[y] = x
    groups = {e: root(e) for e in elements}
    neutral = []
    for st in (a, b):
        s = st.copy()
        for i, site in enumerate(st):
            support = {groups[e.symbol] for e, v in site.species.items() if v > 0}
            if len(support) != 1:
                raise ValueError('site cannot be assigned a substitution group')
            # Do not overwrite or trust solver-supplied properties with these names.
            s.replace(i, next(iter(support)), properties={
                'original_occupancies': occupancy_vector(site), 'original_site_index': i})
        neutral.append(s)
    return *neutral, groups


def ambiguous_neutral_orbits(original, neutral):
    """Reject a claim of unique occupancies when neutralization erases order."""
    try:
        groups = SpacegroupAnalyzer(neutral, symprec=.02).get_symmetrized_structure().equivalent_indices
        for group in groups:
            vectors = [occupancy_vector(original[i]) for i in group]
            keys = set().union(*(v.keys() for v in vectors))
            if any(max(v.get(e, 0.) for v in vectors) - min(v.get(e, 0.) for v in vectors) > 1e-8 for e in keys):
                return True
    except Exception:
        return True
    return False


def partial_site_omission(reference, predicted, ra, pa):
    """Recognize a dilute/split-site boundary that needs a vacancy-aware audit.

    Do not report a vanished dilute site as an entirely missing phase. This
    conservative fallback grants no automatic structural credit: all unmatched
    anchor sites must be partially occupied and all other atoms must align.
    """
    swap = len(predicted) > len(reference)
    anchor, moving = (predicted,reference) if swap else (reference,predicted)
    na,nm = (pa,ra) if swap else (ra,pa)
    if not any(s.species.num_atoms < 1-1e-8 for s in anchor):
        return False
    try:
        m=matcher(primitive=False,allow_subset=True,supercell_size='volume')
        transformation=m.get_transformation(na,nm)
        if transformation is None:return False
        mapping=transformation[2]
        missing=[i for i,j in enumerate(mapping[:len(anchor)]) if j is None]
        return bool(missing and len(mapping)==len(anchor)
            and all(anchor[i].species.num_atoms < 1-1e-8 for i in missing))
    except (ValueError,RuntimeError):
        return False


def pair_correspondence(reference, predicted):
    a = reference.composition.get_el_amt_dict()
    scale = len(reference) / len(predicted)
    b = {e: v * scale for e, v in predicted.composition.get_el_amt_dict().items()}
    elements = sorted(set(a) | set(b))
    out = dict(composition_basis='reference expanded cell; predicted coefficients multiplied by reference_site_count/predicted_site_count',
               predicted_cell_multiplier=scale, reference_coefficients=a, aligned_submitted_coefficients=b,
               coefficient_errors={e: b.get(e, 0.) - a.get(e, 0.) for e in elements},
               normalized_element_fraction_TV=comp_distance(reference, predicted),
               occupancy_errors=None, max_site_occupancy_TV=None, coordinate_errors=None,
               geometric_correspondence=False, chemical_correspondence=None)
    ra, pa, groups = substitution_neutral_pair(reference, predicted)
    out['substitution_groups'] = sorted([sorted(e for e in groups if groups[e] == g) for g in set(groups.values())])
    m = matcher()
    if not m.fit(ra, pa, symmetric=True):
        if partial_site_omission(reference,predicted,ra,pa):
            out.update(geometric_correspondence=True,geometric_match_distance=1.,
                site_mapping_status='undefined: all other atoms align but partially occupied sites are absent; requires vacancy/split-site adjudication')
            return out
        out['site_mapping_status'] = 'no all-atom geometric correspondence within frozen tolerances'
        return out
    out['geometric_correspondence'] = True
    rms = m.get_rms_dist(ra, pa)
    out['geometric_match_distance'] = float(rms[0]) if rms else 1.
    if ambiguous_neutral_orbits(reference, ra) or ambiguous_neutral_orbits(predicted, pa):
        out['site_mapping_status'] = 'undefined: substitution-neutral symmetry merges distinct occupancy assignments or symmetry audit failed'
        return out
    swap = len(predicted) > len(reference)
    anchor, moving = (predicted, reference) if swap else (reference, predicted)
    neutral_anchor, neutral_moving = (pa, ra) if swap else (ra, pa)
    try:
        aligned = matcher(primitive=False).get_s2_like_s1(neutral_anchor, neutral_moving)
        if aligned is None or len(aligned) != len(anchor):
            raise ValueError('no one-to-one original-cell mapping')
        rows, coords = [], []
        for i, (site, other) in enumerate(zip(anchor, aligned)):
            v1, v2 = occupancy_vector(site), other.properties['original_occupancies']
            r, p = (v2, v1) if swap else (v1, v2)
            tv = .5 * sum(abs(r.get(e, 0.) - p.get(e, 0.)) for e in set(r) | set(p))
            distance = float(anchor.lattice.get_distance_and_image(site.frac_coords, other.frac_coords)[0])
            rows.append(dict(reference_site=int(other.properties['original_site_index']) if swap else i,
                             submitted_site=i if swap else int(other.properties['original_site_index']),
                             reference_occupancies=r, submitted_occupancies=p, total_variation=float(tv)))
            coords.append(distance)
        error = max(r['total_variation'] for r in rows)
        if not -1e-8 <= error <= 1+1e-8:
            raise ValueError('invalid species-plus-vacancy occupancy distance')
        out.update(site_mapping_status='mapped in larger original cell; equivalent copies retained', occupancy_errors=rows,
                   max_site_occupancy_TV=error, chemical_correspondence=max(0., 1-error),
                   coordinate_errors=dict(reference_metric='larger-cell lattice metric after lattice basis/origin alignment',
                                          rms_A=float(np.sqrt(np.mean(np.square(coords)))), maximum_A=max(coords), per_site_A=coords))
    except Exception as exc:
        out['site_mapping_status'] = 'undefined: ' + str(exc)
    return out


class PairDetails(dict):
    """Pair measurements with a global assignment-identifiability audit."""
    assignment_ambiguous = False


def phase_correspondence(references, predicted):
    edges, details, matrix = {}, PairDetails(), []
    for i, a in enumerate(references):
        row = []
        for j, b in enumerate(predicted):
            d = pair_correspondence(a, b)
            details[i, j] = d
            q = d['chemical_correspondence']
            matched = d['geometric_correspondence'] and (q is None or q > 0)
            row.append(matched)
            if matched:
                edges[i, j] = (d['geometric_match_distance'], d['normalized_element_fraction_TV'])
        matrix.append(row)

    def objective(z):
        return -round(z[0],12), -z[1], round(z[2],10)

    ties = {}

    @lru_cache(None)
    def solve(i, used):
        if i == len(references):
            ties[i,used] = 1
            return 0., 0, 0., ()
        skipped = solve(i+1, used)
        options = [(skipped, ties[i+1,used])]
        for j in range(len(predicted)):
            if (i, j) not in edges or used & (1 << j):
                continue
            q, n, g, pairs = solve(i+1, used | (1 << j))
            dq = details[i, j]['chemical_correspondence']
            # Undefined mappings are optimistic only for selecting a provisional
            # correspondence; their existence withholds an official scalar score.
            options.append(((q + (1. if dq is None else dq), n+1, g+edges[i, j][0], ((i,j),)+pairs),ties[i+1,used | (1 << j)]))
        best = min((z for z,_ in options),key=lambda z:(*objective(z),z[3]))
        ties[i,used] = min(2,sum(n for z,n in options if objective(z)==objective(best)))
        return best

    pairs = list(solve(0, 0)[3])
    details.assignment_ambiguous = ties[0,0] > 1
    return pairs, matrix, edges, details


def correspondence_metrics(reference_count, predicted_count, targets, fractions, pairs, details):
    qualities = [details[i,j]['chemical_correspondence'] for i,j in pairs]
    ambiguous = (getattr(details,'assignment_ambiguous',False) or
        any(d['geometric_correspondence'] and d['chemical_correspondence'] is None for d in details.values()))
    known = sum(q for q in qualities if q is not None)
    mass = sum(q*min(float(targets[i]), fractions[j]) for (i,j),q in zip(pairs,qualities)
               if q is not None and fractions[j] is not None)
    denominator = reference_count+predicted_count
    return dict(framework_phase_f1=2*known/denominator,
                framework_phase_precision=known/predicted_count if predicted_count else 0.,
                framework_phase_recall=known/reference_count,
                framework_correspondence_f1=2*len(pairs)/denominator,
                chemistry_adjusted_mass_score=mass, chemistry_adjusted_mass_error=1-mass,
                assignment_ambiguous=getattr(details,'assignment_ambiguous',False),
                matching_requires_adjudication=ambiguous,
                chemical_correspondence_sum=known)
