"""Procedure tests on saved solver projects: request checks, launch and tracking for the broker.

The runner (procedure_runner.py) works outside the broker so a long test never stalls dispatch or
collection. It runs as its own systemd user unit, so a controller restart does not stop it.
"""
from collections import Counter
from pathlib import Path
import os
import shutil
import signal
import subprocess

from common import ROOT, WORK, CORE, read, save, sha, ident, under, timestamp
from progression import require_transfer_complete

SCOPE = 'Researcher diagnostic with access to synthetic truth; excluded from rollout comparisons.'


def ineligible(state, jid):
    """None when the attempt has a completed, collected, verified project; otherwise the reason."""
    job = state['jobs'].get(jid)
    if job is None:
        return 'unknown attempt'
    if job.get('superseded_by'):
        return 'superseded by a recovery'
    if job['status'] != 'complete' or not job.get('collected'):
        return 'not complete and collected'
    try:
        require_transfer_complete(state, job['batch'])
    except ValueError:
        return 'its batch has an unfinished prospective comparison'
    folder = ROOT / 'evidence/attempts' / jid
    gpx = folder / 'workspace/final.gpx'
    if not gpx.is_file() or gpx.is_symlink():
        return 'no saved final.gpx'
    if not (folder / 'score.json').is_file():
        return 'not scored'
    score = read(folder / 'score.json')
    if score.get('profile_status') != 'verified' or score.get('D_poisson') is None:
        return 'its project replay was not verified'
    return None


def select(state, request, cap):
    attempts, cases = request.get('attempts'), request.get('cases')
    if attempts and cases:
        raise ValueError('Select attempts or cases, not both')
    chosen, skipped = [], Counter()
    if attempts:
        if len(set(attempts)) != len(attempts):
            raise ValueError('Duplicate attempt IDs')
        for jid in attempts:
            reason = ineligible(state, ident(jid))
            if reason:
                raise ValueError(jid + ': ' + reason)
            chosen.append(jid)
    else:
        known = {j['case_id'] for j in state['jobs'].values()}
        if cases and any(c not in known for c in cases):
            raise ValueError('Unknown case, or a case without attempts')
        for jid, job in state['jobs'].items():
            if cases and job['case_id'] not in cases:
                continue
            reason = ineligible(state, jid)
            if reason:
                skipped[reason] += 1
            else:
                chosen.append(jid)
    if not chosen:
        raise ValueError('No eligible attempts: a procedure test needs completed, collected attempts with verified projects')
    if len(chosen) > cap:
        if attempts:
            raise ValueError(f'{len(chosen)} attempts exceed the cap of {cap}')
        # Without an explicit list, test the most recent attempts.
        chosen = sorted(chosen, key=lambda j: state['jobs'][j].get('dispatched_at', 0), reverse=True)
        skipped[f'older than the newest {cap}'] = len(chosen) - cap
        chosen = chosen[:cap]
    return chosen, dict(skipped)


def launch(rid, folder):
    prefix = read(ROOT / 'control/settings.json')['service_prefix']
    cmd = [CORE, str(ROOT / 'control/procedure_runner.py'), str(folder / 'request.json')]
    unit = f'{prefix}-ptest-{rid}'
    if shutil.which('systemd-run'):
        p = subprocess.run(['systemd-run', '--user', '--quiet', '--collect', '--unit', unit,
                            '--property', 'Nice=10', *cmd], capture_output=True, text=True)
        if p.returncode == 0:
            return {'kind': 'systemd', 'name': unit}
    with (folder / 'runner.log').open('a') as log:
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    return {'kind': 'process', 'pid': proc.pid}


def alive(unit):
    if unit['kind'] == 'systemd':
        return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', unit['name']]).returncode == 0
    status = Path('/proc') / str(unit['pid']) / 'status'
    try:
        return 'State:\tZ' not in status.read_text()
    except OSError:
        return False


def start(state, r):
    rid = ident(r['id'])
    tests = state.setdefault('procedure_tests', {})
    running = [k for k, v in tests.items() if v['state'] == 'running']
    if running:
        raise ValueError('Procedure test ' + running[0] + ' is still running; one test runs at a time')
    folder = ROOT / 'evidence/procedure-tests' / rid
    if rid in tests or folder.exists():
        raise ValueError('Procedure test exists')
    script = under(WORK, r['script'])
    if script.suffix != '.py' or not script.is_file():
        raise ValueError('The procedure must be a .py file within the evolve folder')
    cfg = read(ROOT / 'control/settings.json')
    chosen, skipped = select(state, r, cfg['procedure_test_max_attempts'])
    timeout = cfg['procedure_test_timeout_seconds']
    if r.get('timeout_minutes') is not None:
        minutes = r['timeout_minutes']
        if type(minutes) is not int or minutes < 1:
            raise ValueError('timeout_minutes must be a positive integer')
        timeout = min(60 * minutes, 2 * cfg['procedure_test_timeout_seconds'])
    # The script and its sibling modules are snapshotted; later edits cannot change a recorded test.
    snapshot = folder / 'procedure'
    snapshot.mkdir(parents=True)
    for p in sorted(script.parent.glob('*.py')):
        if p.is_file() and not p.is_symlink():
            shutil.copy2(p, snapshot / p.name)
    rows = []
    for jid in chosen:
        job = state['jobs'][jid]
        score = read(ROOT / 'evidence/attempts' / jid / 'score.json')
        gpx = ROOT / 'evidence/attempts' / jid / 'workspace/final.gpx'
        rows.append({'attempt': jid, 'case_id': job['case_id'], 'case_path': str(ROOT / 'cases' / job['case_id']),
                     'policy': job['policy'], 'purpose': job['purpose'], 'group': job['group'],
                     'project': str(gpx), 'project_sha256': sha(gpx),
                     'before': {k: score.get(k) for k in ['D_poisson', 'independent_atomic_rwp', 'score_100', 'evaluator_version']}})
    record = {'id': rid, 'script': script.name, 'script_source': str(script.relative_to(WORK)), 'script_sha256': sha(script),
              'snapshot': {p.name: sha(p) for p in sorted(snapshot.iterdir())}, 'attempts': rows, 'skipped': skipped,
              'workers': cfg['procedure_test_workers'], 'timeout_seconds': timeout, 'created_at': timestamp(), 'scope': SCOPE}
    save(folder / 'request.json', record)
    unit = launch(rid, folder)
    tests[rid] = {'state': 'running', 'unit': unit, 'path': str(folder), 'attempts': len(rows), 'started_at': timestamp()}
    return {'state': 'running', 'path': str(folder), 'attempts': len(rows), 'skipped': skipped,
            'workers': record['workers'], 'timeout_seconds': timeout, 'progress': str(folder / 'status.json'),
            'results': str(folder / 'results.json'), 'scope': SCOPE}


def cancel(state, r):
    rid = ident(r['test'])
    test = state.get('procedure_tests', {}).get(rid)
    if not test or test['state'] != 'running':
        raise ValueError('No running procedure test ' + rid)
    unit = test['unit']
    if unit['kind'] == 'systemd':
        subprocess.run(['systemctl', '--user', 'stop', unit['name']], capture_output=True)
    else:
        try:
            os.killpg(unit['pid'], signal.SIGTERM)
        except ProcessLookupError:
            pass
    test.update(state='cancelled', finished_at=timestamp())
    save(ROOT / 'evidence/responses' / (rid + '.json'), {'id': rid, 'status': 'cancelled', 'at': timestamp()})
    return {'test': rid, 'state': 'cancelled'}


def check(state):
    """Close tests whose runner finished; report a runner that stopped without results."""
    for rid, test in state.get('procedure_tests', {}).items():
        if test['state'] != 'running':
            continue
        results = Path(test['path']) / 'results.json'
        if results.exists():
            test.update(state=read(results).get('state', 'complete'), finished_at=timestamp())
        elif not alive(test['unit']):
            test.update(state='error', finished_at=timestamp())
            save(ROOT / 'evidence/responses' / (rid + '.json'),
                 {'id': rid, 'status': 'error', 'at': timestamp(),
                  'error': 'The procedure-test runner stopped before writing results; see ' + str(Path(test['path']) / 'runner.log')})
