"""Re-evaluate the saved, already-selected PG15 attempts without modifying them.

The panel's analysis/per_attempt.json selects the original scored attempts,
including transport retries. It is not replaced and no solver is run.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import statistics
import warnings
import numpy as np

from evaluate_attempt import evaluate
from common import save_json, sha

PANELS = {
    'P0': 'pxrd-sol-max-p0-eval15-repeat2-20261019',
    'E': 'pxrd-eval15-v6nov-20261104',
    'F': 'pxrd-pg15-framework-access-20261105',
    'FE': 'pxrd-pg15-fwaccess-evolved-20261109',
    'Fv5': 'pxrd-pg15-fwaccess-v5-20261109',
}


def replay_one(task):
    root, old, destination = task
    job = json.loads((root / 'attempts' / old['id'] / 'job.json').read_text())
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        row = evaluate(root, job, destination)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--conditions', nargs='+', choices=PANELS, default=list(PANELS))
    parser.add_argument('--cases', nargs='+', help='Optional pilot case IDs, e.g. case-004 case-012')
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.archive_root = args.archive_root.resolve()
    if args.output.is_relative_to(args.archive_root):
        parser.error('Write the replay to a separate directory, not the frozen archive')
    summary = {}
    for condition in args.conditions:
        root = args.archive_root / PANELS[condition]
        source = root / 'analysis/per_attempt.json'
        original = json.loads(source.read_text())
        selected = [r for r in original if not args.cases or r['case'] in args.cases]
        tasks = [(root, row, args.output / condition / 'attempts' / row['id']) for row in selected]
        rows = []
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            for future in as_completed([pool.submit(replay_one, t) for t in tasks]):
                row = future.result()
                rows.append(row)
                print(f"{condition} {len(rows)}/{len(tasks)} {row['id']}: "
                      f"{row.get('replay_interior_rwp')} {row['errors']}", flush=True)
        rows.sort(key=lambda r: (r['case'], r['replicate']))
        previous = {r['id']: r for r in selected}
        changes = []
        for row in rows:
            before = previous[row['id']].get('replay_interior_rwp')
            after = row.get('replay_interior_rwp')
            comparison = dict(id=row['id'], previous_rwp=before, replayed_rwp=after,
                              difference=None if before is None or after is None else after-before)
            if before is not None and after is not None:
                original_curve = root / 'analysis/attempts' / row['id'] / 'project_replay/prediction.npz'
                replayed_curve = args.output / condition / 'attempts' / row['id'] / 'project_replay/prediction.npz'
                with np.load(original_curve, allow_pickle=False) as old, np.load(replayed_curve, allow_pickle=False) as new:
                    assert np.array_equal(old['x'], new['x'])
                    assert np.array_equal(old['observed'], new['observed'])
                    comparison['maximum_profile_difference_counts'] = float(np.max(np.abs(old['predicted']-new['predicted'])))
                comparison['original_prediction_sha256'] = sha(original_curve)
            changes.append(comparison)
        verified = [r for r in rows if (r.get('replay') or {}).get('status') == 'verified']
        by_case = {}
        for row in verified:
            by_case.setdefault(row['case'], []).append(row['replay_interior_rwp'])
        means = [statistics.mean(v) for v in by_case.values()]
        summary[condition] = dict(
            source_panel=PANELS[condition], source_record_sha256=sha(source),
            attempts=len(rows), verified=len(verified),
            mean_case_rwp=statistics.mean(means) if means else None,
            median_case_rwp=statistics.median(means) if means else None,
            all_sources_unchanged=all(r['protected_sources_unchanged'] for r in rows),
            comparisons=changes)
        save_json(args.output / condition / 'per_attempt.json', rows)
        save_json(args.output / 'summary.json', summary)


if __name__ == '__main__':
    main()
