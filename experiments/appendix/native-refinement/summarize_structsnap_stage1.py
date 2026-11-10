"""Score saved StructSnap first stages without rerunning refinement.

Combines disjoint original two-stage and stage-1-only campaigns. Independently
recalculates first-candidate profile diagnostics in fresh pinned CPU processes;
never substitutes an original two-stage run's final residual for stage 1.
"""
import argparse
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import csv
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import warnings

import numpy as np

from common import REPO, digest, fingerprint, read_json, write_json


def score(item):
    from report import evaluate
    warnings.filterwarnings('ignore')
    entry, directory = item
    directory = Path(directory)
    result = read_json(directory / 'result.json')
    original = REPO / entry['candidate_path']
    reference = REPO / entry['reference_path']
    assert digest(reference.read_bytes()) == entry['reference_sha256']
    assert digest(original.read_bytes()) == result['input_sha256']
    assert digest((directory / 'input.cif').read_bytes()) == result['input_sha256']
    first = directory / 'stage-1.cif'
    assert digest(first.read_bytes()) == result['stages'][0]['cif_sha256']
    before, before_error = evaluate(original, reference)
    after, after_error = evaluate(first, reference)
    if before_error or after_error:
        raise ValueError((entry['id'], before_error, after_error))
    if before != entry['before_structure_match']:
        raise ValueError('Original exact label disagrees: ' + entry['id'])
    second = None
    if len(result['stages']) == 2:
        second, error = evaluate(directory / 'stage-2.cif', reference)
        if error:
            raise ValueError((entry['id'], error))
    _, corpus, case, slot = entry['id'].split('/')
    return dict(id=entry['id'], corpus=corpus, case=case, slot=int(slot),
                before_exact=bool(before), stage1_exact=bool(after), stage2_exact=second,
                before_cosine=-result['native_before_negative_cosine'],
                stage1_cosine=-result['stages'][0]['fresh_negative_cosine'],
                stage1_seconds=result['stages'][0]['wall_seconds'],
                input_sha256=result['input_sha256'], stage1_sha256=digest(first.read_bytes()),
                reference_sha256=entry['reference_sha256'], pattern_sha256=result['pattern_sha256'],
                source_code_sha256=result['code_sha256'],
                result_path=str((directory / 'result.json').relative_to(REPO)))


def profile_worker(request_path):
    from gsas import diagnostic, observation
    request = read_json(request_path)
    task = request['task']
    directory = Path(request['directory'])
    result = read_json(directory / 'result.json')
    assert digest(task['pattern_text'].encode()) == result['pattern_sha256'] == task['pattern_sha256']
    assert digest(task['candidate_cif'].encode()) == result['input_sha256']
    with tempfile.TemporaryDirectory(prefix='structsnap-stage1-profile-') as temp:
        root = Path(temp)
        shutil.copy2(directory / 'input.cif', root / 'input.cif')
        shutil.copy2(directory / 'stage-1.cif', root / 'refined.cif')
        paired = diagnostic(task, root, *observation(task))
    checks = {}
    inline = result.get('paired_profile', {})
    for side in ('before', 'after'):
        if side in inline and (side == 'before' or request['control']):
            delta = abs(paired[side]['rwp_percent'] - inline[side]['rwp_percent'])
            checks[side + '_delta_pp'] = delta
            if delta > 1e-6:
                raise ValueError(f'Independent diagnostic disagrees: {side}, {delta} pp')
    write_json(request['output'], dict(id=task['id'], key=request['key'],
               paired_profile=paired, control=request['control'], checks=checks))


def profile_job(job):
    task, directory, output, control, versions = job
    directory = Path(directory)
    key = fingerprint(dict(task=task,
        result=digest((directory / 'result.json').read_bytes()),
        input=digest((directory / 'input.cif').read_bytes()),
        stage1=digest((directory / 'stage-1.cif').read_bytes()),
        script=digest(Path(__file__).read_bytes()),
        diagnostic=digest(Path(__file__).with_name('gsas.py').read_bytes()), versions=versions))
    if output.exists():
        record = read_json(output)
        if record['key'] == key:
            return record
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='structsnap-stage1-request-') as temp:
        request = Path(temp) / 'request.json'
        write_json(request, dict(task=task, directory=str(directory), output=str(output),
                                key=key, control=control))
        with output.with_suffix('.log').open('w') as log:
            subprocess.run([sys.executable, str(Path(__file__).resolve()),
                            '--profile-request', str(request)],
                           stdout=log, stderr=subprocess.STDOUT, check=True, timeout=120)
    return read_json(output)


def summarize(rows):
    groups = []
    for corpus in ('pxrd-100', 'pxrd-ood', 'overall'):
        members = [r for r in rows if corpus == 'overall' or r['corpus'] == corpus]
        cases = defaultdict(list)
        for row in members:
            cases[row['case']].append(row)
        recovery = {}
        for k in (1, 8):
            selected = [[r for r in group if r['slot'] <= k] for group in cases.values()]
            if any(len(group) != k for group in selected):
                raise ValueError('Incomplete candidate set')
            recovery[f'pass_at_{k}'] = dict(n=len(selected),
                before=sum(any(r['before_exact'] for r in group) for group in selected),
                after=sum(any(r['stage1_exact'] for r in group) for group in selected))
        first = [r for r in members if r['slot'] == 1]
        stats = {}
        for name, subset in (('all_candidates', members), ('first_candidates', first)):
            stats[name] = dict(n=len(subset),
                mean_before=float(np.mean([r['before_cosine'] for r in subset])),
                mean_after=float(np.mean([r['stage1_cosine'] for r in subset])),
                median_before=float(np.median([r['before_cosine'] for r in subset])),
                median_after=float(np.median([r['stage1_cosine'] for r in subset])))
        paired = [r for r in first if r.get('before_rwp') is not None]
        profile = dict(n=len(paired))
        if paired:
            for side in ('before', 'after'):
                profile['mean_' + side] = float(np.mean([r[side + '_rwp'] for r in paired]))
                profile['median_' + side] = float(np.median([r[side + '_rwp'] for r in paired]))
        second = [r for r in members if r['stage2_exact'] is not None]
        groups.append(dict(corpus=corpus, candidates=len(members), recovery=recovery,
            exact_candidates=dict(before=sum(r['before_exact'] for r in members),
                after=sum(r['stage1_exact'] for r in members),
                gained=sum(not r['before_exact'] and r['stage1_exact'] for r in members),
                lost=sum(r['before_exact'] and not r['stage1_exact'] for r in members)),
            native_cosine=stats, first_candidate_diagnostic_rwp=profile,
            mean_stage1_seconds=float(np.mean([r['stage1_seconds'] for r in members])),
            stage2_subset=dict(n=len(second), before=sum(r['before_exact'] for r in second),
                stage1=sum(r['stage1_exact'] for r in second), stage2=sum(r['stage2_exact'] for r in second))))
    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path)
    parser.add_argument('--runs', type=Path, nargs='+')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--structural-only', action='store_true',
                        help='Verify saved CIFs and recovery counts without GSAS-II or profile recalculation')
    parser.add_argument('--profile-request', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.profile_request:
        profile_worker(args.profile_request)
        return
    if not args.inputs or not args.runs or not args.output:
        parser.error('--inputs, --runs, and --output are required')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    entries = [e for e in read_json(args.inputs / 'local-index.json') if e['id'].startswith('crystalyze/')]
    directories = {}
    for run in args.runs:
        for path in (run / 'candidates/crystalyze').glob('**/result.json'):
            result = read_json(path)
            if result['id'] in directories:
                raise ValueError('Duplicate candidate: ' + result['id'])
            if result['status'] != 'completed':
                raise ValueError('Run incomplete: ' + result['id'])
            directories[result['id']] = str(path.parent.resolve())
    if set(directories) != {e['id'] for e in entries} or len(entries) != 1600:
        raise ValueError('Expected precisely all 1,600 benchmark candidates')
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(score, [(e, directories[e['id']]) for e in entries], chunksize=8))
    write_json(output / 'structural-summary.json', summarize(rows))
    print('Structural scoring complete:', summarize(rows), flush=True)
    if args.structural_only:
        return
    versions = {n: importlib.metadata.version(n) for n in ('numpy', 'scipy', 'pymatgen', 'spglib', 'matplotlib', 'PyCifRW')}
    gsas_root = Path(os.environ['GSASII_PATH']).parent
    gsas_commit = subprocess.check_output(['git', '-C', str(gsas_root), 'rev-parse', 'HEAD'], text=True).strip()
    if gsas_commit != '1a0aeec6c61b54f68e6812704730a471187ac393':
        raise ValueError('Wrong GSAS-II checkout')
    versions['gsas_commit'] = gsas_commit
    tasks = {t['id']:t for t in read_json(args.inputs / 'tasks.json') if t['method'] == 'crystalyze'}
    selected = {r['id'] for r in rows if r['slot'] == 1}
    controls = []
    for corpus in ('pxrd-100', 'pxrd-ood'):
        choices = [r['id'] for r in rows if r['corpus'] == corpus and r['stage2_exact'] is None]
        controls.extend(sorted(choices)[:2])
    jobs = [(tasks[i], directories[i], output / 'profile-checks' / (i.replace('/', '__') + '.json'),
             i in controls, versions) for i in sorted(selected | set(controls))]
    profiles = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for record in pool.map(profile_job, jobs):
            profiles[record['id']] = record
            if len(profiles) % 20 == 0:
                print(f'Profile diagnostics: {len(profiles)}/{len(jobs)}', flush=True)
    for row in rows:
        paired = profiles.get(row['id'], {}).get('paired_profile', {})
        for side in ('before', 'after'):
            row[side + '_rwp'] = paired.get(side, {}).get('rwp_percent')
    with (output / 'scores.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = dict(groups=summarize(rows), versions=versions,
        scorer_sha256=digest(Path(__file__).read_bytes()),
        diagnostic_sha256=digest(Path(__file__).with_name('gsas.py').read_bytes()),
        controls=[profiles[i] for i in controls],
        profile_definition='GSAS-II exported-CIF diagnostic against native observation; fixed observation-derived width; unit weights; nonnegative scale and four Chebyshev coefficients',
        refinement_definition='First saved StructSnap stage only; original sampler order; no coordinate optimization; includes native symmetrization and fitted W',
        source_runs=[str(p.resolve().relative_to(REPO)) for p in args.runs])
    write_json(output / 'summary.json', summary)
    print(json.dumps(summary['groups'], indent=2), flush=True)


if __name__ == '__main__':
    main()
