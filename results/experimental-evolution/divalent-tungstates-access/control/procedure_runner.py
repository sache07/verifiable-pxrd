"""Run a researcher procedure on copies of saved solver projects and replay each result with the frozen
scorer. Started by the broker as its own unit so a long test never stalls dispatch; never launches a model.

python procedure_runner.py ROOT/evidence/procedure-tests/ID/request.json

Each project is copied into its own work folder and the procedure runs on the copy in the evaluator's
sandbox (procedure_host.py: GSAS-II, no network, no hidden truth, only the work folder writable). The
output project is replayed by the scorer's own isolated replay and scored against the hidden mean with
the scorer's own D. Saved attempts and their scores are never modified.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import datetime
import fcntl
import json
import os
import shutil
import statistics
import subprocess
import sys
import threading
import time
import traceback

R = Path(__file__).resolve().parents[1]
BACKEND = Path('<HOME>/.local/share/characterizagent/backends/gsas2')
UV = Path('<HOME>/.local/share/uv/python')
LOG_TAIL = 20000


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f'.{os.getpid()}.{threading.get_ident()}.new')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)


def text(value):
    if value is None:
        return ''
    return value.decode(errors='replace') if isinstance(value, bytes) else value


def run_procedure(work, snapshot, inputs, script, timeout):
    cmd = ['bwrap', '--unshare-all', '--die-with-parent', '--new-session',
           '--ro-bind', '/usr', '/usr', '--symlink', 'usr/bin', '/bin', '--symlink', 'usr/lib', '/lib',
           '--symlink', 'usr/lib64', '/lib64', '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
           '--ro-bind', '/etc/ld.so.cache', '/etc/ld.so.cache',
           '--ro-bind', str(BACKEND), str(BACKEND), '--ro-bind', str(UV), str(UV),
           '--ro-bind', str(R / 'control/procedure_host.py'), '/host/procedure_host.py',
           '--ro-bind', str(snapshot), '/procedure', '--ro-bind', str(inputs), '/inputs',
           '--bind', str(work), '/work', '--chdir', '/work',
           '--setenv', 'HOME', '/tmp', '--setenv', 'MPLCONFIGDIR', '/tmp',
           str(BACKEND / 'venv/bin/python'), '/host/procedure_host.py', script]
    env = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1',
           'PYTHONDONTWRITEBYTECODE': '1'}
    started = time.monotonic()
    try:
        p = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=timeout)
        code, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        code, out, err = 'timeout', text(exc.stdout), text(exc.stderr)
    (work / 'procedure.log').write_text('--- stdout\n' + out[-LOG_TAIL:] + '\n--- stderr\n' + err[-LOG_TAIL:])
    return code, time.monotonic() - started, err[-600:]


def replay_and_score(project, case, folder):
    import numpy as np
    from replay import isolated_replay
    from predictive import evaluate_frozen
    from common import load_structure
    from structure_metrics import physical_screen
    report = isolated_replay(project, case / 'inputs/pattern.csv', folder)
    if report['status'] != 'replayed':
        return {'status': report['status'], 'error': report.get('error')}
    with np.load(folder / 'prediction.npz', allow_pickle=False) as z:
        x, y, predicted = z['x'].copy(), z['observed'].copy(), z['predicted'].copy()
    evaluation = evaluate_frozen(str(case), x, y, predicted)
    weights = 1 / np.maximum(y, 1.)
    rwp = float(100 * np.sqrt(np.sum(weights * (y - predicted) ** 2) / np.sum(weights * y * y)))
    phases = []
    for p in report['phases']:
        try:
            screen = physical_screen(load_structure(folder / p['cif']))['status']
        except Exception as exc:
            screen = 'unreadable: ' + str(exc)[:120]
        phases.append({'name': p['name'], 'weight_fraction': p['weight_fraction'], 'physical_screen': screen})
    (folder / 'prediction.npz').unlink(missing_ok=True)   # observed and predicted counts only; not needed after scoring
    return {'status': 'replayed', 'D_poisson': evaluation['D_poisson'], 'D_poisson_infinite': evaluation['D_poisson_infinite'],
            'independent_atomic_rwp': rwp, 'reference_rwp': evaluation['reference_rwp'],
            'profile_review_flags': report.get('profile_review_flags', []), 'phases': phases}


def one(record, row, base):
    jid = row['attempt']
    work = base / 'attempts' / jid
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    source = Path(row['project'])
    shutil.copy2(source, work / 'input.gpx')
    result = {**row, 'project': str(source)}
    code, seconds, tail = run_procedure(work, base / 'procedure', Path(row['case_path']) / 'inputs',
                                        record['script'], record['timeout_seconds'])
    result.update(procedure_exit=code, procedure_seconds=round(seconds, 1), log=str(work / 'procedure.log'))
    output = work / 'output.gpx'
    if code != 0 or not output.is_file() or output.is_symlink():
        result.update(status='procedure_failed', error=('timed out' if code == 'timeout' else
                      ('no output.gpx written' if code == 0 else 'exit ' + str(code))), stderr_tail=tail)
        return result
    try:
        after = replay_and_score(output, Path(row['case_path']), work / 'replay')
    except Exception as exc:
        after = {'status': 'replay_error', 'error': str(exc)[-600:]}
    result.update(status=after['status'] if after['status'] != 'replayed' else 'scored', after=after,
                  output=str(output))
    if after.get('D_poisson') is not None and row['before'].get('D_poisson') is not None:
        result['delta_D'] = after['D_poisson'] - row['before']['D_poisson']
    return result


def summarize(rows):
    scored = [r for r in rows if r.get('status') == 'scored' and r.get('delta_D') is not None]
    before = [r['before']['D_poisson'] for r in scored]
    after = [r['after']['D_poisson'] for r in scored]
    profile = lambda d: 1 / (1 + d)
    # Changes below 0.1% of D are refinement noise, not an effect of the procedure.
    tolerance = lambda r: 1e-3 * max(r['before']['D_poisson'], 0.01)
    out = {'attempts': len(rows), 'scored': len(scored),
           'failed': sum(r.get('status') != 'scored' for r in rows),
           'improved': sum(r['delta_D'] < -tolerance(r) for r in scored),
           'worse': sum(r['delta_D'] > tolerance(r) for r in scored),
           'unchanged': sum(abs(r['delta_D']) <= tolerance(r) for r in scored),
           'physical_flags_after': sum(any(p['physical_screen'] != 'pass' for p in r['after']['phases']) for r in scored)}
    if scored:
        out.update(median_D_before=statistics.median(before), median_D_after=statistics.median(after),
                   mean_profile_term_before=statistics.mean(map(profile, before)),
                   mean_profile_term_after=statistics.mean(map(profile, after)))
    cases = {}
    for r in scored:
        cases.setdefault(r['case_id'], []).append(r)
    out['by_case'] = {c: {'attempts': len(v), 'median_D_before': statistics.median(x['before']['D_poisson'] for x in v),
                          'median_D_after': statistics.median(x['after']['D_poisson'] for x in v)} for c, v in sorted(cases.items())}
    return out


def main(request_path):
    request_path = Path(request_path).resolve()
    base = request_path.parent
    record = json.loads(request_path.read_text())
    rid = record['id']
    log = (base / 'runner.log').open('a')
    sys.stdout = sys.stderr = log
    # Hold the shared evaluator lock like every scoring process, so a deployment cannot swap the scorer mid-test.
    lock = (R / 'control/evaluator.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_SH)
    sys.path.insert(0, str(R / 'scorer/src'))
    rows, done = [], [0]
    progress_lock = threading.Lock()

    def progress(state):
        write(base / 'status.json', {'id': rid, 'state': state, 'done': done[0], 'total': len(record['attempts']), 'at': stamp()})

    def task(row):
        try:
            result = one(record, row, base)
        except Exception:
            result = {**row, 'status': 'runner_error', 'error': traceback.format_exc()[-1500:]}
        with progress_lock:
            rows.append(result)
            done[0] += 1
            progress('running')
        return result

    progress('running')
    try:
        with ThreadPoolExecutor(max(1, int(record['workers']))) as pool:
            list(pool.map(task, record['attempts']))
        order = {r['attempt']: i for i, r in enumerate(record['attempts'])}
        rows.sort(key=lambda r: order[r['attempt']])
        results = {'id': rid, 'state': 'complete', 'finished_at': stamp(), 'script': record['script_source'],
                   'script_sha256': record['script_sha256'], 'scope': record['scope'],
                   'summary': summarize(rows), 'attempts': rows}
        write(base / 'results.json', results)
        response = {'id': rid, 'status': 'complete', 'at': stamp(),
                    'result': {'path': str(base), 'results': str(base / 'results.json'), 'summary': results['summary'],
                               'scope': record['scope']}}
    except Exception:
        write(base / 'results.json', {'id': rid, 'state': 'error', 'finished_at': stamp(), 'error': traceback.format_exc()[-3000:],
                                      'attempts': rows})
        response = {'id': rid, 'status': 'error', 'at': stamp(), 'error': 'Procedure-test runner failed; see ' + str(base / 'runner.log')}
    progress(response['status'])
    write(R / 'evidence/responses' / (rid + '.json'), response)


if __name__ == '__main__':
    main(sys.argv[1])
