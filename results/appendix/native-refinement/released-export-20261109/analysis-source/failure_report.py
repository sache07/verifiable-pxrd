"""Summarize execution failures separately from match regressions and rejected stages."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
from pathlib import Path
import statistics

from common import read_json, write_json


def classify(result, logs=''):
    status = result.get('status', 'pending')
    stage = result.get('failure_stage', '')
    error = result.get('error', '')
    if status == 'completed':
        return ''
    if status == 'timeout' or 'TimeoutError' in error:
        return 'timeout'
    if status == 'crashed':
        return 'worker-crash'
    if status == 'pending':
        return 'pending'
    evidence = (error + '\n' + logs).lower()
    if 'native refinement exceeded' in evidence or 'timeouterror:' in evidence:
        return 'timeout'
    if 'no reflections in data range' in evidence:
        return 'no-reflections-in-observation-range'
    if stage in {'conventional-cell-conversion', 'symmetry-cif-export'}:
        return 'inter-pass-symmetry-conversion'
    if stage in {'read-first-pass-export', 'final-export-validation'} and (
            'no structures' in evidence or 'occupanc' in evidence or 'cif' in error.lower()):
        return 'unreadable-refined-cif'
    if 'export changed elemental proportions' in evidence:
        return 'export-composition-change'
    if 'nonfinite exported geometry' in evidence or 'invalid exported cell' in evidence:
        return 'invalid-exported-geometry'
    if 'no reader' in evidence or 'no structures' in evidence or 'no phases' in evidence:
        return 'cif-import-error'
    if any(t in evidence for t in ('singular matrix', 'svd did not converge', 'math domain error',
                                 'nan or inf', 'infs or nans', 'division by zero',
                                 'underflow encountered', 'overflow encountered')):
        return 'numerical-refinement-error'
    return 'other-refinement-error'


def read_logs(directory):
    chunks = []
    for path in sorted(directory.glob('*.log*')):
        if path.suffix == '.gz':
            chunks.append(gzip.decompress(path.read_bytes()).decode(errors='replace'))
        else:
            chunks.append(path.read_text(errors='replace'))
    return '\n'.join(chunks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--runs', type=Path, nargs='+', help='Optional disjoint raw shards; metrics are read from --results/scores.csv')
    args = parser.parse_args()
    root = args.results
    failures, groups, stage_counts, rejected, diagnostics, rechecks = [], defaultdict(Counter), defaultdict(Counter), defaultdict(Counter), Counter(), Counter()
    paths = sorted(p for run in args.runs or [root] for p in (run / 'candidates').rglob('result.json'))
    seen = set()
    for path in paths:
        result = read_json(path)
        if result['id'] in seen:
            raise ValueError('Duplicate candidate across runs: ' + result['id'])
        seen.add(result['id'])
        method, corpus, case, slot = result['id'].split('/')
        groups[(method, corpus)][result['status']] += 1
        if result.get('paired_profile_error'):
            diagnostics[method] += 1
            p = path.parent/'profile-recheck.json'
            if p.exists():rechecks[(method,read_json(p)['status'])]+=1
        category = classify(result, read_logs(path.parent) if result['status'] != 'completed' else '')
        if category:
            failures.append(dict(id=result['id'], method=method, corpus=corpus, case=case, slot=int(slot),
                status=result['status'], failure_type=category, stage=result.get('failure_stage', ''),
                error=result.get('error', '')))
        for entry in result.get('stages', []):
            if 'accepted' in entry:
                stage_counts[method][entry['stage'] + ('/accepted' if entry['accepted'] else '/rejected')] += 1
                if not entry['accepted']:
                    rejected[method][entry.get('error', 'unspecified')] += 1
    with (root / 'failures.csv').open('w', newline='') as stream:
        fields = ['id', 'method', 'corpus', 'case', 'slot', 'status', 'failure_type', 'stage', 'error']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(failures)
    pairs = defaultdict(list)
    with (root / 'scores.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        if row['status'] == 'completed' and row['slot'] == '1' and row['before_rwp'] and row['after_rwp']:
            pairs[(row['method'], row['corpus'])].append((float(row['before_rwp']), float(row['after_rwp'])))
    profile = []
    for (method, corpus), data in sorted(pairs.items()):
        before, after = zip(*data)
        profile.append(dict(method=method, corpus=corpus, n=len(data), mean_before=statistics.mean(before),
            mean_after=statistics.mean(after), median_before=statistics.median(before), median_after=statistics.median(after),
            median_paired_change=statistics.median(b-a for a,b in data)))
    counts = Counter((r['method'], r['corpus'], r['failure_type']) for r in failures)
    summary = dict(failures=[dict(method=m, corpus=c, failure_type=f, count=n) for (m,c,f),n in sorted(counts.items())],
        rejected_stages={m: dict(v) for m,v in stage_counts.items()},
        stage_rejection_errors={m: dict(v) for m,v in rejected.items()},
        independent_diagnostic_failures=dict(diagnostics), paired_first_candidate_rwp=profile,
        diagnostic_rechecks={m+'/'+s:n for (m,s),n in rechecks.items()},
        notes=['A completed refinement need not be structurally correct.',
               'Stage rejections in the RealPXRD adapter restore the last accepted state; they are not full-run failures.',
               'Failure types are derived from exception, stage, and log records; unreadable exports are not silently repaired.',
               'Original candidates are retained on full failure; missing original submissions remain missing.'])
    write_json(root / 'failure-summary.json', summary)
    print({m:dict(v) for m,v in groups.items()})
    print('Failure types:', dict(Counter(r['failure_type'] for r in failures)))


if __name__ == '__main__':
    main()
