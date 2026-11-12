"""EC2-side commands. Called by the trusted local controller, never by a solver."""
from pathlib import Path
import argparse
import gzip
import json
import os
import shutil
import subprocess
import sys
import traceback

from common import ROOT, CORE, read, save, sha, ident, hashes, frozen_code_ok, timestamp


def mask_case(cid):
    import fcntl
    folder = ROOT / 'resources'
    folder.mkdir(exist_ok=True)
    with (folder / (ident(cid) + '.lock')).open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return _mask_case(cid)


def _mask_case(cid):
    from pymatgen.core import Composition
    from pymatgen.io.cif import CifParser
    import warnings
    import runner
    if sha(runner.INDEX) != read(ROOT / 'control/settings.json')['source_index_sha256']:
        raise ValueError('Frozen source database index changed')
    case = ROOT / 'cases' / ident(cid)
    truth = read(case / 'private/truth.json')
    wanted = truth['withhold_composition']
    listed = set(truth.get('withhold_ids') or [])
    if wanted is None and not listed:
        return {'resource': 'full', 'excluded_ids': []}
    folder = ROOT / 'resources' / cid
    if (folder / 'mask.json').exists():
        return read(folder / 'mask.json')
    folder.mkdir(parents=True, exist_ok=True)
    with gzip.open(runner.INDEX, 'rt') as f:
        source = json.load(f)
    key = lambda c: '|'.join(f'{e}:{v:.6f}' for e, v in sorted(c.fractional_composition.get_el_amt_dict().items()))
    elements = {part.split(':')[0] for part in wanted.split('|')} if wanted else set()
    excluded, unparsed, cif_disagreements = set(), [], []
    filtered = {}
    # Most index entries need no chemical parsing. Relevant failed formulas are
    # conservatively excluded rather than accidentally leaking the hidden phase.
    for system, rows in source.items():
        kept = []
        for row in rows:
            hide = str(row[1]) in listed
            if not hide and wanted and set(system.split('-')) == elements:
                try:
                    hide = key(Composition(row[0])) == wanted
                except Exception:
                    hide = True
                    unparsed.append(str(row[1]))
                record_id = str(row[1])
                path = runner.CIFS / record_id[0] / record_id[1:3] / record_id[3:5] / (record_id + '.cif')
                if not hide and path.exists():
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore')
                            st = CifParser(path, occupancy_tolerance=1, frac_tolerance=0).parse_structures(primitive=False)[0]
                        if key(st.composition) == wanted:
                            hide = True
                            cif_disagreements.append(record_id)
                    except Exception:
                        hide = True
                        unparsed.append(record_id)
            if hide:
                excluded.add(str(row[1]))
            else:
                kept.append(row)
        if kept:
            filtered[system] = kept
    with gzip.open(folder / 'index.json.gz', 'wt') as f:
        json.dump(filtered, f)
    cifs = folder / 'cif'
    for p in runner.CIFS.rglob('*.cif'):
        if p.stem in excluded:
            continue
        dst = cifs / p.relative_to(runner.CIFS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            os.link(p, dst)
    missing = sorted(listed - excluded)
    if missing:
        raise ValueError('withhold_ids not found in the frozen library index: ' + ', '.join(missing))
    record = {'resource': cid, 'composition_key': wanted, 'withhold_ids': sorted(listed), 'excluded_ids': sorted(excluded),
              'unparsed_same_system_excluded': sorted(unparsed), 'index_sha256': sha(folder / 'index.json.gz'),
              'occupied_composition_additional_exclusions': sorted(cif_disagreements),
              'original_index_sha256': sha(runner.INDEX)}
    save(folder / 'mask.json', record)
    return record


def launch(jid):
    ident(jid)
    job = read(ROOT / 'control/jobs' / (jid + '.json'))
    status = ROOT / 'control/job_status' / (jid + '.json')
    if status.exists():
        print(json.dumps(read(status)))
        return
    unit = read(ROOT / 'control/settings.json')['service_prefix'] + '-' + jid
    exists = subprocess.run(['systemctl', '--user', 'show', unit, '--property=LoadState', '--value'], capture_output=True, text=True)
    if exists.stdout.strip() not in ['', 'not-found']:
        print(json.dumps({'id': jid, 'status': 'dispatched', 'unit': unit}))
        return
    p = subprocess.run(['systemd-run', '--user', '--quiet', '--unit=' + unit,
                        '--property=Type=exec', '--property=RemainAfterExit=yes',
                        '--property=WorkingDirectory=' + str(ROOT), '--',
                        CORE, str(Path(__file__)), 'work', jid], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    print(json.dumps({'id': jid, 'status': 'dispatched', 'unit': unit}))


def work(jid):
    import runner
    from common import register_truth
    job = read(ROOT / 'control/jobs' / (ident(jid) + '.json'))
    status = ROOT / 'control/job_status' / (jid + '.json')
    if status.exists() and read(status).get('status') not in ['starting']:
        return
    save(status, {'id': jid, 'status': 'starting', 'at': timestamp()})
    try:
        frozen_code_ok()
        case = ROOT / 'cases' / job['case_id']
        register_truth(case)
        mask = mask_case(job['case_id'])
        job.update(resource=mask['resource'], excluded_ids=mask['excluded_ids'])
        if mask['resource'] != 'full':
            job['extra_forbidden'] = [str(runner.INDEX)]
            for i in mask['excluded_ids']:
                job['extra_forbidden'].append(str(runner.CIFS / i[0] / i[1:3] / i[3:5] / (i + '.cif')))
        # Check all immutable package bytes immediately before deployment.
        f = ROOT / 'policies' / job['policy'] / 'frozen.json'
        if f.exists():
            for rel, digest in read(f)['files'].items():
                if sha(f.parent / rel) != digest:
                    raise ValueError('Package changed after freeze')
        save(status, {'id': jid, 'status': 'running', 'at': timestamp()})
        result = runner.run(job)
        dest = ROOT / 'evidence/attempts' / jid
        dest.mkdir(parents=True, exist_ok=True)
        save(dest / 'launch.json', result)
        if result.get('inputs_unchanged') is not True or result.get('infrastructure_failure'):
            save(status, {'id': jid, 'status': 'infrastructure_error', 'detail': result, 'at': timestamp()})
            return
        # A run stopped at the solver time limit is a scientific outcome: score what it saved.
        if result['status'] not in ('finished', 'timed_out'):
            save(status, {'id': jid, 'status': 'interrupted', 'detail': result, 'at': timestamp()})
            return
        record = {**job, 'condition': job['policy'], 'dataset': 'autonomous_synthetic',
                  'workspace': str(ROOT / 'attempts' / jid / 'workspace'),
                  'cohort': job.get('purpose', 'development'), 'split': 'development'}
        save(dest / 'record.json', record)
        score_job(jid)
    except Exception as e:
        save(status, {'id': jid, 'status': 'infrastructure_error', 'error': str(e), 'traceback': traceback.format_exc(), 'at': timestamp()})


def score_job(jid):
    dest = ROOT / 'evidence/attempts' / jid
    status = ROOT / 'control/job_status' / (jid + '.json')
    save(status, {'id': jid, 'status': 'scoring', 'at': timestamp()})
    env = dict(os.environ, OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2', PYTHONDONTWRITEBYTECODE='1')
    p = subprocess.run([CORE, str(ROOT / 'control/scoring.py'), 'score', str(dest / 'record.json')],
                       capture_output=True, text=True, env=env)
    (dest / 'scorer.stdout').write_text(p.stdout)
    (dest / 'scorer.stderr').write_text(p.stderr)
    score = ROOT / 'scorer/scores' / jid / 'score.json'
    if not score.exists():
        raise RuntimeError('Evaluator produced no score artifact: ' + p.stderr[-1500:])
    shutil.copy2(score, dest / 'score.json')
    fit = score.parent / 'independent_fit.csv'
    if fit.exists():
        shutil.copy2(fit, dest / fit.name)
    save(status, {'id': jid, 'status': 'complete' if p.returncode == 0 else 'evaluator_error',
                  'score_status': read(score)['score_status'], 'at': timestamp()})


def rescore(jid):
    """Score an attempt again after an evaluator error; the solver's files are unchanged."""
    status = ROOT / 'control/job_status' / (ident(jid) + '.json')
    if read(status)['status'] != 'evaluator_error':
        raise ValueError('Only an attempt that ended in an evaluator error can be rescored')
    frozen_code_ok()
    try:
        score_job(jid)
    except Exception as e:
        save(status, {'id': jid, 'status': 'evaluator_error', 'error': str(e), 'at': timestamp()})
    print(json.dumps(read(status)))


def work_started(jid):
    """True once the solver produced an item. Capacity rejections fail before any."""
    events = ROOT / 'attempts' / ident(jid) / 'run/codex-events.jsonl'
    if events.exists():
        with events.open() as f:
            for line in f:
                try:
                    if json.loads(line).get('type', '').startswith('item.'):
                        return True
                except ValueError:
                    pass
    return False


def status_all():
    rows = {}
    for p in (ROOT / 'control/jobs').glob('*.json'):
        jid = p.stem
        path = ROOT / 'control/job_status' / p.name
        row = read(path) if path.exists() else {'id': jid, 'status': 'not_started'}
        if row['status'] in ['starting', 'running', 'scoring', 'not_started']:
            unit = read(ROOT / 'control/settings.json')['service_prefix'] + '-' + jid
            p = subprocess.run(['systemctl', '--user', 'show', unit, '--property=ActiveState', '--value'], capture_output=True, text=True)
            active = p.stdout.strip()
            if active in ['active', 'activating']:
                if row['status'] == 'not_started':
                    row['status'] = 'starting'
            elif row['status'] != 'not_started' or active == 'failed':
                row = {**row, 'status': 'interrupted', 'reason': 'Worker service ended without a terminal record; no automatic duplicate will be launched.'}
                save(path, row)
        if row['status'] == 'running':
            row = {**row, 'work_started': work_started(jid)}
        rows[jid] = row
    print(json.dumps({'jobs': rows, 'usage_pause': read(ROOT / 'control/STOP_DISPATCH.json') if (ROOT / 'control/STOP_DISPATCH.json').exists() else None}))


def recovery_mode(jid):
    base = ROOT / 'attempts' / ident(jid)
    status = read(ROOT / 'control/job_status' / (jid + '.json'))
    if status['status'] not in ['infrastructure_error', 'interrupted']:
        raise ValueError('Cannot recover an active or scientifically completed job')
    # Guard against a crashed supervisor leaving its scientific scope alive.
    launch_path = base / 'run/launch.json'
    launch = read(launch_path) if launch_path.exists() else {}
    unit = launch.get('systemd_unit')
    if unit:
        p = subprocess.run(['systemctl', '--user', 'show', unit, '--property=ActiveState', '--value'], capture_output=True, text=True)
        if p.stdout.strip() in ['active', 'activating']:
            raise ValueError('Scientific scope is still active; do not duplicate it')
    scientific = work_started(jid)
    sessions = list((base / 'codex-home/sessions').rglob('*.jsonl'))
    if scientific and sessions and launch_path.exists():
        result = {'mode': 'resume', 'parent': jid}
    elif not scientific:
        result = {'mode': 'fresh_transport_retry', 'parent': jid, 'reason': 'No solver item or scientific action occurred.'}
    else:
        raise ValueError('Scientific actions occurred but resumable history is missing; preserve as interrupted, request a new explicitly independent attempt if needed')
    print(json.dumps(result))


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'launch': launch(sys.argv[2])
    elif command == 'work': work(sys.argv[2])
    elif command == 'status': status_all()
    elif command == 'mask': print(json.dumps(mask_case(sys.argv[2])))
    elif command == 'recovery-mode': recovery_mode(sys.argv[2])
    elif command == 'rescore': rescore(sys.argv[2])
    elif command == 'resume': (ROOT / 'control/STOP_DISPATCH.json').unlink(missing_ok=True)
    else: raise ValueError(command)
