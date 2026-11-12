"""Case states and the paired comparison with the incumbent: printed in STATUS.md and checked by `promote`."""
import math
import statistics

FRESH = {'baseline', 'development', 'evaluation', 'transfer'}
SOLVES = 3            # fresh solves per package and case
MINIMUM_CASES = 6     # compared cases needed for a promotion
MARGIN = 4.           # Δ must reach max(MARGIN, NOISE_MULTIPLE × noise)
NOISE_MULTIPLE = 2.
REGRESSION = 15.      # no case mean more than this below the incumbent's
RECOVERED_D = 1.      # half profile credit
FLOOR_D = 0.1         # Rwp about 5% above the noise floor
OVERLAP = 90.         # composition overlap of a matched phase, percent


def solve_flags(score):
    """(recovered, at_floor) for one score.json: the hidden phases matched one to one, physical, D ≤ 1; floor if also D ≤ 0.1."""
    d = score.get('D_poisson')
    if not score.get('score_100') or d is None or (score.get('headline_components') or {}).get('physical_gate') == 'fail':
        return False, False
    n = len(score.get('reference_fractions') or [])
    pairs = (score.get('structural_components') or {}).get('assignment') or []
    inventory = (n > 0 and len(pairs) == n and len(score.get('submitted_fractions') or []) == n
                 and all((x.get('composition_occupancy_overlap') or 0) >= OVERLAP for x in pairs))
    recovered = inventory and d <= RECOVERED_D
    return recovered, recovered and d <= FLOOR_D


def fresh(rows):
    """(case, package) -> complete, scored fresh attempts; superseded slots and evaluator errors left out."""
    out = {}
    for r in rows:
        if r.get('superseded_by') or r.get('purpose') not in FRESH or r.get('status') != 'complete':
            continue
        if r.get('score_100') is None or r.get('score_status') == 'verification_error':
            continue
        out.setdefault((r['case_id'], r['policy']), []).append(r)
    return out


def case_state(entries):
    """unrecovered, inconsistent, recovered or at floor, from a package's fresh solves on one case."""
    if not entries:
        return None
    recovered = sum(bool(x.get('recovered')) for x in entries)
    floor = sum(bool(x.get('at_floor')) for x in entries)
    return ('at floor' if floor == len(entries) else 'recovered' if recovered == len(entries)
            else 'inconsistent' if recovered else 'unrecovered')


def paired_comparison(rows, incumbent, cases_by_package):
    """Each package against the incumbent on the cases it ran this cycle.

    Δ is the mean over cases of (package case mean − incumbent case mean). The noise is the standard
    error of Δ from both packages' replicate spread: s, the root-mean-square within-case sample SD,
    times sqrt(Σ(1/n_p + 1/n_i))/k. The rule: every case compared with SOLVES fresh solves of each,
    at least MINIMUM_CASES cases, Δ ≥ max(MARGIN, NOISE_MULTIPLE × noise), no case more than REGRESSION below.
    """
    groups = fresh(rows)
    result = {'incumbent': incumbent, 'rule': {'solves': SOLVES, 'cases': MINIMUM_CASES, 'margin': MARGIN,
              'noise_multiple': NOISE_MULTIPLE, 'regression': REGRESSION}, 'packages': {}}
    for pkg in sorted(cases_by_package):
        cases = sorted(cases_by_package[pkg])
        if pkg == incumbent or not cases:
            continue
        per_case, missing, sds, weights = [], [], [], []
        for c in cases:
            a, b = groups.get((c, pkg), []), groups.get((c, incumbent), [])
            if len(a) < SOLVES or len(b) < SOLVES:
                missing.append(c)
                continue
            sa, sb = [x['score_100'] for x in a], [x['score_100'] for x in b]
            sds += [statistics.stdev(sa), statistics.stdev(sb)]
            weights.append(1. / len(sa) + 1. / len(sb))
            per_case.append({'case': c, 'package_mean': statistics.mean(sa), 'incumbent_mean': statistics.mean(sb),
                             'difference': statistics.mean(sa) - statistics.mean(sb),
                             'package_state': case_state(a), 'incumbent_state': case_state(b), 'solves': [len(sa), len(sb)]})
        entry = {'cases': len(per_case), 'not_comparable': missing, 'per_case': per_case,
                 'delta': None, 'noise': None, 'threshold': None, 'lowest_difference': None, 'meets_rule': False}
        if per_case:
            k = len(per_case)
            s = math.sqrt(sum(x * x for x in sds) / len(sds))
            noise = s * math.sqrt(sum(weights)) / k
            delta = sum(x['difference'] for x in per_case) / k
            lowest = min(x['difference'] for x in per_case)
            threshold = max(MARGIN, NOISE_MULTIPLE * noise)
            entry.update(delta=delta, noise=noise, threshold=threshold, lowest_difference=lowest,
                         meets_rule=not missing and k >= MINIMUM_CASES and delta >= threshold and lowest >= -REGRESSION)
        result['packages'][pkg] = entry
    return result


def comparison_lines(result):
    inc, rule = result['incumbent'], result['rule']
    lines = ['', f'## Comparison with the incumbent ({inc})', '',
             f"Each package run this cycle, on the cases it ran this cycle. Δ is the mean over those cases of (package case mean − {inc} case mean); "
             "the noise is the standard error of Δ from both packages' replicate spread. The promotion rule: "
             f"{rule['solves']} fresh solves of each package on every compared case, at least {rule['cases']} cases, "
             f"Δ ≥ max({rule['margin']:g}, {rule['noise_multiple']:g} × noise), and no case more than {rule['regression']:g} below {inc}.", '']
    if not result['packages']:
        return lines + ['No package has been run this cycle.']
    lines += ['| Package | Cases compared | Not yet comparable | Δ | Noise | Needed | Lowest case difference | Rule met |',
              '|---|---:|---|---:|---:|---:|---:|---|']
    fmt = lambda v, f: format(v, f) if v is not None else '—'
    for pkg, r in result['packages'].items():
        lines.append(f"| {pkg} | {r['cases']} | {', '.join(r['not_comparable']) or 'none'} | {fmt(r['delta'], '+.1f')} | {fmt(r['noise'], '.1f')} | "
                     f"{fmt(r['threshold'], '.1f')} | {fmt(r['lowest_difference'], '+.1f')} | {'yes' if r['meets_rule'] else 'no'} |")
    lines += ['', f'| Package | Case | Package mean | {inc} mean | Difference | Package state | {inc} state |',
              '|---|---|---:|---:|---:|---|---|']
    for pkg, r in result['packages'].items():
        for x in r['per_case']:
            lines.append(f"| {pkg} | {x['case']} | {x['package_mean']:.1f} | {x['incumbent_mean']:.1f} | {x['difference']:+.1f} | "
                         f"{x['package_state']} | {x['incumbent_state']} |")
    return lines
