"""Refresh derived evaluation files in the baseline/evolved public bundles.

Never replaces submitted GPX projects, JSON answers, traces, or archived records.
The only added submission files are previously archived CIFs newly recognized by
the parser. Normalization follows the original public-bundle importer.
"""
import argparse
import csv
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / 'scripts'))
from import_experimental_track import Sanitizer, copy_sanitized, write_json
from replay_panels import PANELS


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--replay-results', type=Path, required=True)
    p.add_argument('--archive-root', type=Path, required=True)
    p.add_argument('--public-root', type=Path, required=True)
    args = p.parse_args()
    for condition, label in [('P0', 'baseline'), ('E', 'evolved')]:
        panel = args.archive_root.resolve() / PANELS[condition]
        destination = args.public_root / label
        source = args.replay_results / condition
        records = json.loads((source / 'per_attempt.json').read_text())
        existing = json.loads((destination / 'per_attempt.json').read_text())
        by_slot = {(r['case'], r['replicate']): r for r in records}
        sanitizer = Sanitizer({'attempt_roots': [[str(panel), '<PANEL>'],
                                  [str(Path.home() / 'workspace' / PANELS[condition]), '<PANEL>']]})
        excluded = {'id', 'condition', 'source_hashes'}
        for public in existing:
            row = by_slot[public['case'], public['replicate']]
            assert row['replay']['status'] == 'verified' and row['protected_sources_unchanged']
            public.update(sanitizer.metadata({k: v for k, v in row.items() if k not in excluded}))
            attempt = destination / 'attempts' / f"{row['case']}-r{row['replicate']}"
            audit = json.loads((attempt / 'attempt.json').read_text())
            audit['replay_interior_rwp_percent'] = row['replay_interior_rwp']
            audit['replay_evaluator_sha256'] = row['evaluator_hashes']
            audit['phases'] = []
            for phase in row['phases']:
                src = Path(phase['cif'])
                dst = attempt / 'workspace' / src.name
                if not dst.exists():
                    # This is a copy of a submitted CIF, never a replay-generated replacement.
                    copy_sanitized(src, dst, sanitizer)
                    audit['workspace']['deliverables'].append(src.name)
                assert dst.read_bytes() == sanitizer.text(src.read_text()).encode()
                audit['phases'].append(dict(formula=phase['formula'],
                    weight_fraction=phase['weight_fraction'], cif=src.name,
                    physical_screen=(phase.get('physical_screen') or {}).get('status')))
            write_json(attempt / 'attempt.json', audit)
            evaluation = source / 'attempts' / row['id']
            for src in sorted(evaluation.rglob('*')):
                if src.is_file():
                    copy_sanitized(src, attempt / 'evaluation' / src.relative_to(evaluation), sanitizer)
            refreshed = sanitizer.metadata(row)
            refreshed['id'], refreshed['condition'] = public['id'], label
            write_json(attempt / 'evaluation/result.json', refreshed)
            write_json(attempt / 'evaluation/assessment.log', {
                'id': public['id'], 'Rwp': row['replay_rwp'],
                'Rwp_10.1_99.9_degrees': row['replay_interior_rwp'],
                'errors': row['errors'], 'evaluator_hashes': row['evaluator_hashes'],
            })
        write_json(destination / 'per_attempt.json', existing)
        with (destination / 'per_attempt.csv').open(newline='') as f:
            reader = csv.DictReader(f)
            fields, summary = reader.fieldnames, list(reader)
        public_by_slot = {(r['case'], r['replicate']): r for r in existing}
        for row in summary:
            score = public_by_slot[row['case_id'], int(row['replicate'])]
            row['replay_interior_rwp_percent'] = score['replay_interior_rwp']
            row['phases'] = ';'.join(ph['formula'] for ph in score['phases'])
        with (destination / 'per_attempt.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(summary)
        print(f'{label}: updated {len(existing)} evaluation records; submissions unchanged')


if __name__ == '__main__':
    main()
