"""Render the compact CPU refinement report from scored, audited result records."""
import argparse
from collections import Counter, defaultdict
import csv
from pathlib import Path
from common import read_json


def render(root):
    summary = read_json(root / 'summary.json')
    failures = read_json(root / 'failure-summary.json')
    groups = summary['groups']
    if any(g['status'].get('pending', 0) for g in groups):
        raise ValueError('Refusing a final report with pending candidates')
    if any(g['original_label_disagreements'] for g in groups):
        raise ValueError('Original match labels differ; audit before reporting')
    lines = ['# Released-export CPU refinement results', '',
        'The three CPU experiments refine existing generated candidates; no candidate generation is rerun. '
        'PXRDGen uses the released two-pass functions and default GSAS-II CIF formatting. '
        'Ab uses its released optimizer, with a fitted-phase export added using default GSAS formatting. '
        'RealPXRD-Solver uses our paper-guided GSAS-II adapter, not author-released refinement code. '
        'Reference structures are available only to the local scorer.', '',
        'Crystalyze is a separate GPU campaign and is not included here. The precision-patched pilot and '
        'superseded partial CPU campaign are preserved separately and are not pooled into these results.', '',
        '## Structural recovery', '',
        'Entries are before → after refinement, out of 100 problems per corpus. Candidate order is unchanged. '
        'A full execution/export failure retains the original candidate; a completed refinement is retained '
        'even when it loses a structural match. Missing original submissions remain misses. '
        'Pass@8/20 denotes any matching candidate among those original slots, not Rwp-ranked selection.', '',
        '| Method | Corpus | Pass@1 | Pass@8 | Pass@20 | Completed / available candidates | Missing originals |',
        '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
    names = {'pxrdgen':'PXRDGen', 'ab-pxrd-solver':'Ab-PXRD-Solver', 'realpxrd-solver':'RealPXRD-Solver adapter'}
    for g in groups:
        cells = []
        for k in (1,8,20):
            r=g['recovery'][f'first_{k}']
            cells.append('—' if (g['method']=='ab-pxrd-solver' and k>1) or (g['method']=='pxrdgen' and k>8)
                         else f"{r['before']} → {r['after']}")
        available=g['candidates']-g['status'].get('missing-original',0)
        lines.append(f"| {names[g['method']]} | {g['corpus']} | {' | '.join(cells)} | {g['status'].get('completed',0)} / {available} | {g['status'].get('missing-original',0)} |")
    lines += ['', '### Matches from refined outputs versus failure fallback', '',
        'These counts also use all 100 problems per corpus as the denominator. They distinguish a '
        'matching refined first candidate from a match retained only because refinement failed.', '',
        '| Method | Corpus | Matching refined first candidates | Additional matches from original fallback |',
        '| --- | --- | ---: | ---: |']
    for g in groups:
        r = g['recovery']['first_1']
        lines.append(f"| {names[g['method']]} | {g['corpus']} | {r['after_successful_exports_only']} | {r['fallback_only_matches']} |")
    lines += ['', '## Execution failures', '',
        'Failure types below are candidate-level counts. `failures.csv` preserves the exact candidate ID, '
        'pipeline stage, and exception; the compressed logs retain the underlying messages. '
        'Unreadable exported CIFs are reported as failures rather than repaired by changing export precision.', '',
        '| Method | Corpus | Failure type | Candidates |', '| --- | --- | --- | ---: |']
    for r in failures['failures']:
        lines.append(f"| {names[r['method']]} | {r['corpus']} | {r['failure_type']} | {r['count']} |")
    lines += ['', 'RealPXRD stage rejections are different from full failures: the adapter restores the last accepted '
        'state and attempts later stages. Their counts and exception messages are in `failure-summary.json`. '
        'Failure of the independent profile diagnostic also does not erase an otherwise completed refinement.', '',
        '## Paired profile agreement', '',
        'The same successfully refined first candidates contribute before and after. Here n is the number of '
        'such candidates with both residuals available. Each exported CIF is simulated against its method-specific '
        'observation under an identical fixed profile, fitting only nonnegative scale and four Chebyshev background '
        'coefficients with unit weights. This independently recomputed Rwp is not the optimizer-reported residual '
        'or the clean-reference fixedparams-v1 metric. Absolute values are not comparable across methods.', '',
        '| Method | Corpus | n | Mean Rwp (%) | Median Rwp (%) |', '| --- | --- | ---: | ---: | ---: |']
    for r in failures['paired_first_candidate_rwp']:
        lines.append(f"| {names[r['method']]} | {r['corpus']} | {r['n']} | {r['mean_before']:.2f} → {r['mean_after']:.2f} | {r['median_before']:.2f} → {r['median_after']:.2f} |")
    if failures.get('diagnostic_rechecks'):
        lines += ['', 'Some inline profile diagnostics failed after numerical errors during refinement. '
            'Their residuals were recalculated from the unchanged input/output CIFs in fresh processes. '
            'The original errors remain in `result.json`; separate `profile-recheck.json` records identify '
            'the recalculations and their code/package versions. Successful-diagnostic controls check '
            'agreement with the inline calculation. No optimizer or structural output was changed.', '']
    with (root/'scores.csv').open() as stream:
        rows = {r['id']: r for r in csv.DictReader(stream)}
    px = rows.get('pxrdgen/pxrd-100/pxrd100-poly-02-a/01')
    ab = rows.get('ab-pxrd-solver/pxrd-100/pxrd100-challenge-013/01')
    if px or ab:
        lines += ['', '## Export-related examples', '']
    if px and px['status']=='failed':
        lines += ['PXRDGen `pxrd100-poly-02-a`, candidate 1: the first-pass exporter rounds the '
            'poorly determined fractional coordinates to integers. The next CIF read fails, so the '
            'correct original is retained. The separate precision-patched pilot completed this case '
            'but produced a nonmatch. This illustrates why fallback matches are counted separately.', '']
    if ab and ab['status']=='completed' and ab['before_exact']=='True' and ab['after_exact']=='False':
        lines += ['Ab `pxrd100-challenge-013`: default CIF formatting rounds symmetry-related '
            'coordinates inconsistently; reading the export expands nine sites into 18 nearly '
            'overlapping sites. The file is readable and retains elemental proportions, so this is '
            'a completed export that fails structural validity, rather than a full execution failure. '
            'The historical precision-corrected analysis restored this one match. The released-export '
            'run intentionally retains the uncorrected outcome.', '']
    lines += ['', '## Reproduction and provenance', '',
        'All available original candidates reproduce their released benchmark match labels. '
        'Original/refined/intermediate CIFs, metric records, compressed logs, source snapshots, and pinned '
        'package/source/binary hashes accompany this report. Dense profile arrays remain in the raw run folders; '
        'they can be regenerated from the retained CIFs, original observation manifests, and pinned runner. '
        'The raw arrays were checked before the compact bundle was made.', '',
        'Run `report.py --inputs BUNDLE/inputs --results BUNDLE --workers 4`, then '
        '`failure_report.py --results BUNDLE` and `write_report.py BUNDLE`. '
        'Run `audit_bundle.py BUNDLE` to check artifact and runner hashes. See '
        '`experiments/native-refinement/README.md` for the remote execution procedure.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle',type=Path)
    args=parser.parse_args()
    (args.bundle/'README.md').write_text(render(args.bundle))
