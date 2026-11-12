"""Inventory matching without erasing continuous composition errors."""
from functools import lru_cache
from pathlib import Path
import re
import numpy as np
from pymatgen.analysis.structure_matcher import StructureMatcher, ElementComparator
from common import CONFIG, load_structure, read_json

def matcher(primitive=True, **overrides):
    args = dict(CONFIG['matching'])
    args.update(primitive_cell=primitive)
    args.update(overrides)
    return StructureMatcher(**args, comparator=ElementComparator())

def occupancy_vector(site):
    d = {str(e.symbol): float(v) for e, v in site.species.items() if v > 0}
    d['vacancy'] = max(0., 1. - sum(d.values()))
    return d

def occupancy_neutral(st):
    s = st.copy()
    s.add_site_property('original_occupancies', [occupancy_vector(a) for a in st])
    s.add_site_property('original_site_index', list(range(len(st))))
    for i, site in enumerate(st):
        support = sorted({e.symbol for e, v in site.species.items() if v > 0})
        s.replace(i, {e: 1 / len(support) for e in support}, properties=s[i].properties)
    return s

def comp_distance(a, b):
    x = a.composition.fractional_composition.get_el_amt_dict()
    y = b.composition.fractional_composition.get_el_amt_dict()
    return .5 * sum(abs(x.get(e, 0.) - y.get(e, 0.)) for e in set(x) | set(y))

def duplicate_composition_close(a, b):
    x = a.composition.fractional_composition.get_el_amt_dict()
    y = b.composition.fractional_composition.get_el_amt_dict()
    tolerance=CONFIG.get('duplicate_match',{}).get('composition_tolerance',1e-5)
    return set(x) == set(y) and max(abs(x[e] - y[e]) for e in x) <= tolerance

def physical_screen(st):
    """Broad necessary screen, not a complete chemical feasibility certificate."""
    hard = CONFIG['physical_screen']['hard_contact_A']
    oxygen = CONFIG['physical_screen']['oxide_oxygen_contact_review_A']
    centers, neighbors, images, distances = st.get_neighbor_list(max(hard, oxygen))
    contacts = []
    status = 'pass'
    for i, j, image, dist in zip(centers, neighbors, images, distances):
        if i > j or (i == j and tuple(image) <= (0, 0, 0)):
            continue
        a, b = st[int(i)], st[int(j)]
        partial = a.species.num_atoms < .9999 or b.species.num_atoms < .9999
        is_oxygen = set(a.species.get_el_amt_dict()) == set(b.species.get_el_amt_dict()) == {'O'}
        reason = None
        if dist < hard:
            reason = 'short_partially_occupied_contact' if partial else 'impossible_fully_occupied_contact'
            if not partial:
                status = 'fail'
            elif status != 'fail':
                status = 'needs_adjudication'
        elif is_oxygen and dist < oxygen:
            reason = 'close_oxygen_sites_in_oxide_scope'
            if status != 'fail':
                status = 'needs_adjudication'
        if reason:
            contacts.append(dict(site_indices=[int(i), int(j)], image=image.tolist(), distance_A=float(dist),
                                 species=[a.species_string, b.species_string],
                                 occupancies=[float(a.species.num_atoms), float(b.species.num_atoms)], reason=reason))
    if any(s.species.num_atoms > 1.0001 or any(v < 0 for v in s.species.values()) for s in st):
        status = 'fail'
    return dict(status=status, flagged_contact_count=len(contacts), flagged_contacts=contacts[:50],
                scope='Necessary geometry/occupancy screen only; pass does not establish thermodynamic or complete chemical validity.')

def _explicit_unresolved(row):
    """Legacy compatibility, not an inference from a low score or a bad fit."""
    if row.get('model_status') == 'unresolved':
        return True
    status = str(row.get('status', '')).lower()
    if set(re.split(r'[^a-z]+', status)) & {'unresolved', 'unidentified', 'unknown'}:
        return True
    name = str(row.get('name', '')).lower().strip()
    identification = str(row.get('identification', '')).lower()
    return (name.startswith(('unresolved ', 'unidentified ', 'unknown '))
            or 'atomic structure unresolved' in identification
            or identification.startswith('indexed cell'))

def _read_fraction(row):
    key = next((k for k in ['weight_fraction', 'weight_percent', 'wt_percent'] if k in row), None)
    if key is None or row[key] is None:
        return None, 'unknown', None
    try:
        if isinstance(row[key], bool):
            raise ValueError('boolean is not a mass fraction')
        value = float(row[key]) / (100 if key != 'weight_fraction' else 1)
        if not np.isfinite(value) or value <= 0:
            raise ValueError('mass fractions must be positive and finite')
        return value, 'reported', None
    except (ValueError, TypeError, OverflowError) as exc:
        return None, 'invalid', str(exc)


class InvalidAtomicOccupancy(ValueError):
    pass


def check_raw_occupancies(path):
    """Do not let CIF import silently discard negative-occupancy atoms."""
    from pymatgen.io.cif import CifFile, str2float
    for block in CifFile.from_file(path).data.values():
        values = block.data.get('_atom_site_occupancy', [])
        if isinstance(values, str): values = [values]
        for value in values:
            number = str2float(value)
            if not np.isfinite(number) or number < 0 or number > 1.0001:
                raise InvalidAtomicOccupancy('invalid raw CIF site occupancy: '+str(value))

def parse_submission(workspace, allowed_elements):
    workspace = Path(workspace).resolve()
    data = read_json(workspace / 'result.json')
    if not isinstance(data, dict):
        raise ValueError('result.json must be an object')
    rows = data.get('phases', data.get('crystalline_phases', []))
    if not isinstance(rows, list) or len(rows) > 16:
        raise ValueError('result.json must contain at most 16 atomic phase records')
    unresolved = data.get('unresolved_components', [])
    if not isinstance(unresolved, list) or len(unresolved) > 16:
        raise ValueError('unresolved_components must be a list of at most 16 records')
    parsed, notes, invalid, fraction_issues = [], [], [], []
    unresolved = [dict(source='unresolved_components', reported=r) for r in unresolved]
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            invalid.append(dict(source_index=index, fraction=None, error='phase record is not an object', reported=row))
            continue
        fraction, fraction_status, fraction_error = _read_fraction(row)
        if fraction_error:
            fraction_issues.append(dict(source_index=index, error=fraction_error))
        cif = row.get('cif_path', row.get('cif', row.get('structure_file')))
        path = None
        try:
            if not isinstance(cif, str):
                raise ValueError('phase missing CIF path')
            path = (workspace / cif).resolve()
            if not path.is_relative_to(workspace) or not path.is_file() or path.stat().st_size > 10_000_000:
                raise ValueError('missing, external, or excessive CIF')
            check_raw_occupancies(path)
            st = load_structure(path)
            if not len(st):
                raise ValueError('CIF contains no atomic model')
        except Exception as exc:
            record = dict(source_index=index, reported=row, error=str(exc), fraction=fraction,
                          hard_physical_failure=isinstance(exc,InvalidAtomicOccupancy))
            if _explicit_unresolved(row) and fraction_status == 'unknown' and not isinstance(exc,InvalidAtomicOccupancy):
                unresolved.append(dict(source='legacy phases entry', **record))
                notes.append(f'phase record {index} retained as explicitly unresolved, without atomic-model credit')
            else:
                invalid.append(record)
            continue
        # A readable atomic CIF is an asserted model even when its weight is
        # unknown or its name/status expresses uncertainty.
        error, hard_failure = None, False
        if not set(st.composition.get_el_amt_dict()) <= set(allowed_elements):
            error = 'submitted phase introduces unavailable elements'
        elif len(st) > 2000 or not .5 < float(st.density) < 30:
            error = 'structure outside broad size/density validity screen'
        elif any(site.species.num_atoms > 1.0001 for site in st):
            error, hard_failure = 'overoccupied atom site', True
        if error:
            invalid.append(dict(source_index=index, reported=row, fraction=fraction, error=error, hard_physical_failure=hard_failure))
            continue
        parsed.append(dict(path=path, structure=st, fraction=fraction, fraction_status=fraction_status,
                           source_index=index, reported=row, physical=physical_screen(st)))

    # Include invalid asserted models in the quantitative denominator. Dropping
    # their mass and renormalizing the valid subset would reward omissions.
    asserted = parsed + invalid
    complete = bool(asserted) and all(r['fraction'] is not None for r in asserted)
    total = sum(r['fraction'] for r in asserted if r['fraction'] is not None)
    if complete and abs(total - 100) <= .05 and all(isinstance(r['reported'], dict) and 'weight_fraction' in r['reported'] for r in asserted):
        for r in asserted:
            r['fraction'] /= 100
        total /= 100
        notes.append('weight_fraction fields interpreted as percentages because their sum was 100')
    explicit_unallocated = bool(unresolved) and total < 1-.005
    invalid_vector = (complete and abs(total - 1) > .005 and not explicit_unallocated) or (not complete and total > 1 + .005)
    if invalid_vector:
        fraction_issues.append(dict(error='reported fraction vector is not consistently normalized; no quantitative credit'))
        for r in asserted:
            r['fraction'] = None
        notes.append('invalid fraction vector retained as unquantified; atomic models remain evaluable')
    elif (complete and not explicit_unallocated) or total > 1:
        # Preserve the existing rounding normalization. For a partial vector,
        # only round an excess <=0.005 down to one; never scale a deficit up.
        for r in asserted:
            if r['fraction'] is not None:
                r['fraction'] /= total
        if not complete:
            notes.append('rounded small known-fraction excess down to one; unknown weights remain unknown')
    elif explicit_unallocated:
        notes.append('retained reported absolute fractions below one with an explicit unresolved component; no renormalization')
    duplicate=CONFIG.get('duplicate_match',dict(ltol=.001,stol=.005,angle_tol=.1))
    tight = matcher(**{k:duplicate[k] for k in ['ltol','stol','angle_tol']})
    distinct = []
    for r in parsed:
        # Retain each actual exported model for complete-project verification;
        # Structural precision collapses numerical equivalents only, so close
        # but distinguishable lattices are not erased before model comparison.
        r['equivalent_exports']=[{'path':r['path'],'fraction':r['fraction']}]
        same = next((d for d in distinct if duplicate_composition_close(d['structure'], r['structure'])
                     and tight.fit(d['structure'], r['structure'])), None)
        if same is None:
            distinct.append(r)
        else:
            same['equivalent_exports'].extend(r['equivalent_exports'])
            same['fraction'] = (same['fraction'] + r['fraction']
                                if same['fraction'] is not None and r['fraction'] is not None else None)
            notes.append('collapsed effectively identical CIF ' + r['path'].name)
    data = dict(data)
    data['_submission_parsing'] = dict(unresolved_components=unresolved, invalid_model_records=invalid,
        fraction_issues=fraction_issues, asserted_phase_count=len(distinct)+len(invalid),
        quantification_complete=(bool(distinct or invalid) and all(r['fraction'] is not None for r in distinct+invalid)
            and abs(sum(r['fraction'] for r in distinct+invalid if r['fraction'] is not None)-1)<1e-8),
        hard_physical_failure=any(r.get('hard_physical_failure') for r in invalid))
    return data, distinct, notes

def strict_assign_phases(references, predicted):
    refs = [occupancy_neutral(s) for s in references]
    preds = [occupancy_neutral(s) for s in predicted]
    m = matcher()
    edges, matrix = {}, []
    for i, a in enumerate(refs):
        row = []
        for j, b in enumerate(preds):
            matched = bool(m.fit(a, b, symmetric=True))
            row.append(matched)
            if matched:
                rms = m.get_rms_dist(a, b)
                edges[i, j] = (float(rms[0]) if rms else 1., comp_distance(references[i], predicted[j]))
        matrix.append(row)
    # Exact lexicographic objective: cardinality, geometry, composition, indices.
    # With <=16 components a bit-mask DP is bounded; weights never enter it.
    @lru_cache(None)
    def solve(i, used):
        if i == len(refs):
            return (0, 0., 0., ())
        options = [solve(i + 1, used)]
        for j in range(len(preds)):
            if (i, j) not in edges or used & (1 << j):
                continue
            n, g, c, pairs = solve(i + 1, used | (1 << j))
            dg, dc = edges[i, j]
            options.append((n + 1, g + dg, c + dc, ((i, j),) + pairs))
        return min(options, key=lambda z: (-z[0], round(z[1], 10), round(z[2], 10), z[3]))
    pairs = list(solve(0, 0)[3])
    return pairs, matrix, edges

def fraction_metrics(target, predicted, pairs):
    target = np.asarray(target, dtype=float)
    predicted = list(predicted)
    known = {j:float(p) for j,p in enumerate(predicted) if p is not None}
    if any(not np.isfinite(p) or p < 0 for p in known.values()) or sum(known.values()) > 1+1e-8:
        raise ValueError('Invalid partial mass-fraction vector')
    complete = bool(predicted) and len(known)==len(predicted) and abs(sum(known.values())-1)<1e-8
    rr, pp = {i for i, j in pairs}, {j for i, j in pairs}
    errors = [abs(float(target[i] - known[j])) for i, j in pairs if j in known]
    missing = sum(float(target[i]) for i in range(len(target)) if i not in rr)
    extra = sum(p for j,p in known.items() if j not in pp)
    unknown_matched = sum(float(target[i]) for i,j in pairs if j not in known)
    unallocated = max(0., 1-sum(known.values()))
    error = .5 * (sum(errors) + missing + extra + unknown_matched + unallocated)
    credit = sum(min(float(target[i]),known[j]) for i,j in pairs if j in known)
    assert abs((1-error)-credit) < 1e-8
    full = len(pairs) == len(target) == len(predicted)
    max_error = max(errors) if errors else None
    return dict(mass_fraction_error=float(error) if complete else None,
                mass_credit_error=float(error), mass_score=float(1-error),
                quantification_complete=complete, quantified_submitted_mass=sum(known.values()),
                unallocated_submitted_mass=unallocated, unquantified_matched_reference_mass=unknown_matched,
                unknown_fraction_count=len(predicted)-len(known), full_framework_inventory=full,
                max_matched_fraction_error=max_error, missing_reference_mass=missing, extra_submitted_mass=extra,
                matched_errors_percentage_points=[100 * e for e in errors],
                fraction_targets={str(t): bool(full and complete and max_error is not None and max_error <= t + 1e-12) for t in CONFIG['fractions']['sensitivity']})

def _ambiguous_orbits(st):
    # Neutral symmetry can merge sites distinguished only by occupancy; do not
    # invent a uniquely recovered occupancy pattern in this situation.
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    neutral = occupancy_neutral(st)
    try:
        groups = SpacegroupAnalyzer(neutral, symprec=.02).get_symmetrized_structure().equivalent_indices
        for group in groups:
            vectors = {tuple(sorted(occupancy_vector(st[i]).items())) for i in group}
            if len(vectors) > 1:
                return True
    except Exception:
        return True
    return False

def strict_parameter_errors(reference, predicted):
    # Normalize to the reference number of sites, not an arbitrary most-abundant
    # species (whose occupancy may itself be wrong).
    a = reference.composition.get_el_amt_dict()
    scale = len(reference) / len(predicted)
    b = {e: v * scale for e, v in predicted.composition.get_el_amt_dict().items()}
    elements = sorted(set(a) | set(b))
    out = dict(composition_basis='reference expanded cell; predicted coefficients multiplied by reference_site_count/predicted_site_count',
               predicted_cell_multiplier=scale, reference_coefficients=a, aligned_submitted_coefficients=b,
               coefficient_errors={e: b.get(e, 0.) - a.get(e, 0.) for e in elements},
               normalized_element_fraction_TV=comp_distance(reference, predicted),
               occupancy_errors=None, max_site_occupancy_TV=None, coordinate_errors=None)
    if _ambiguous_orbits(reference) or _ambiguous_orbits(predicted):
        out['site_mapping_status'] = 'undefined: neutral symmetry merges distinct occupancy assignments or symmetry audit failed'
        return out
    # Work in the larger original cell. No primitive reduction that would lose
    # site properties or original-site identities.
    swap = len(predicted) > len(reference)
    anchor, moving = (predicted, reference) if swap else (reference, predicted)
    try:
        aligned = matcher(primitive=False).get_s2_like_s1(occupancy_neutral(anchor), occupancy_neutral(moving))
        if aligned is None or len(aligned) != len(anchor):
            raise ValueError('no one-to-one original-cell mapping')
        rows, coords = [], []
        for i, (site, other) in enumerate(zip(anchor, aligned)):
            v1, v2 = occupancy_vector(site), other.properties['original_occupancies']
            r, p = (v2, v1) if swap else (v1, v2)
            tv = .5 * sum(abs(r.get(e, 0.) - p.get(e, 0.)) for e in set(r) | set(p))
            distance = float(anchor.lattice.get_distance_and_image(site.frac_coords, other.frac_coords)[0])
            ref_index = int(other.properties['original_site_index']) if swap else i
            pred_index = i if swap else int(other.properties['original_site_index'])
            rows.append(dict(reference_site=ref_index, submitted_site=pred_index,
                             reference_occupancies=r, submitted_occupancies=p, total_variation=float(tv)))
            coords.append(distance)
        out.update(site_mapping_status='mapped in larger original cell; equivalent copies retained', occupancy_errors=rows,
                   max_site_occupancy_TV=max(r['total_variation'] for r in rows),
                   coordinate_errors=dict(reference_metric='larger-cell lattice metric after lattice basis/origin alignment',
                                          rms_A=float(np.sqrt(np.mean(np.square(coords)))), maximum_A=max(coords), per_site_A=coords))
    except Exception as exc:
        out['site_mapping_status'] = 'undefined: ' + str(exc)
    return out

def cation_only_matrix(references, predicted):
    def cations(s):
        c = occupancy_neutral(s)
        c.remove_sites([i for i, a in enumerate(c) if set(a.species.get_el_amt_dict()) == {'O'}])
        return c
    rr, pp = [cations(s) for s in references], [cations(s) for s in predicted]
    m = matcher()
    return [[bool(len(a) and len(b) and m.fit(a, b, symmetric=True)) for b in pp] for a in rr]


def assign_phases(references, predicted):
    from chemistry_matching import phase_correspondence
    return phase_correspondence(references, predicted)[:3]


def parameter_errors(reference, predicted):
    from chemistry_matching import pair_correspondence
    return pair_correspondence(reference, predicted)
