"""Submit durable experiment requests. Does not launch models inside the app sandbox."""
from pathlib import Path
import argparse
import fcntl
import json
import os
import sys
import time
import uuid

W = Path(__file__).resolve().parent
E = W.parent / 'evidence'
TERMINAL_JOBS = {'complete', 'interrupted', 'infrastructure_error', 'evaluator_error'}


def lookup_progress(identifier, command='wait'):
    """Return (observation, finished). Read public evidence; never dispatch work.

    response retains acknowledgement semantics. wait follows a known worker or
    run group, including a run request whose acknowledgement contains job IDs.
    Unknown IDs are errors, not evidence that something is still running.
    """
    response_path = E / 'responses' / (identifier + '.json')
    response = json.loads(response_path.read_text()) if response_path.exists() else None
    if command == 'wait':
        status_path = E / 'status.json'
        snapshot = json.loads(status_path.read_text()) if status_path.exists() else {}
        rows = snapshot.get('jobs', [])
        jobs = rows if isinstance(rows, dict) else {j['id']: j for j in rows}
        groups = snapshot.get('groups', {})

        def worker(jid):
            row = dict(jobs.get(jid, {'id': jid, 'status': 'awaiting_controller_status'}))
            if row.get('superseded_by'):
                row['status'] = 'superseded'
            return row

        # A just-accepted group can precede the next published status snapshot.
        group = groups.get(identifier)
        group_path = E / 'groups' / (identifier + '.json')
        if group is None and group_path.exists():
            group = json.loads(group_path.read_text())
        result = response.get('result') if response else None
        if group is None and isinstance(result, dict) and result.get('jobs'):
            group = result
        known_worker = identifier in jobs or any(
            identifier in g.get('jobs', []) for g in groups.values())
        if not known_worker and group is None:
            known_worker = any(identifier in json.loads(p.read_text()).get('jobs', [])
                               for p in (E / 'groups').glob('*.json'))
        if known_worker:
            row = worker(identifier)
            return {'kind': 'worker', **row, 'snapshot_at': snapshot.get('at')}, (
                row['status'] in TERMINAL_JOBS or row['status'] == 'superseded')
        if group and group.get('jobs'):
            entries = [worker(jid) for jid in group['jobs']]
            terminal = all(j['status'] in TERMINAL_JOBS or j['status'] == 'superseded'
                           for j in entries)
            state = ('complete' if all(j['status'] == 'complete' for j in entries)
                     else 'finished_with_errors' if terminal else 'running')
            return {'id': identifier, 'kind': 'group', 'status': state,
                    'jobs': entries, 'snapshot_at': snapshot.get('at')}, terminal
    if response is not None:
        return {'kind': 'request', **response}, response['status'] not in ['pending', 'processing', 'running']
    if (W / 'requests' / (identifier + '.json')).exists():
        return {'id': identifier, 'kind': 'request', 'status': 'pending',
                'detail': 'Submitted request awaits controller acknowledgement.'}, False
    return {'id': identifier, 'status': 'unknown_id',
            'error': 'No matching ' + ('request' if command == 'response' else 'request, group, or worker')
                     + '. Read lab.py status --json for valid IDs; nothing was launched.'}, True


def process_monitor():
    """Show each advisory once without altering command JSON or job semantics."""
    folder = W / '.monitor'
    folder.mkdir(exist_ok=True)
    with (folder / 'delivery.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        stamp = {'at_epoch': time.time()}
        tmp = folder / ('activity.' + str(os.getpid()) + '.tmp')
        tmp.write_text(json.dumps(stamp)); tmp.replace(folder / 'activity.json')
        path = E / 'monitor/notice.json'
        if not path.exists():
            return
        status = json.loads((E / 'status.json').read_text())
        if status.get('paused') or status.get('controller_stopped') or (W / 'STOP.md').exists():
            return
        note = json.loads(path.read_text())
        receipt = folder / 'receipt.json'
        received = json.loads(receipt.read_text()).get('id') if receipt.exists() else None
        if note['id'] == received or note['expires_at_epoch'] <= time.time():
            return
        print('\nPROCESS MONITOR — advisory checkpoint\n' + note['message'] + '\n', file=sys.stderr, flush=True)
        tmp = folder / ('receipt.' + str(os.getpid()) + '.tmp')
        tmp.write_text(json.dumps({'id': note['id'], 'shown_at_epoch': time.time()}))
        tmp.replace(receipt)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    s = p.add_subparsers(dest='command', required=True)
    for name in ['freeze-batch', 'freeze-package', 'run', 'recover', 'rescore', 'promote', 'pause', 'resume', 'score-investigation', 'procedure-test', 'cancel-test']:
        c = s.add_parser(name)
        c.add_argument('--id', help='Stable request ID; omit to generate one. Never reuse with changed contents.')
        if name == 'freeze-batch':
            c.add_argument('--batch', required=True); c.add_argument('--manifest', required=True)
            c.add_argument('--pool', required=True); c.add_argument('--notes', required=True)
            c.add_argument('--kind', choices=['learning', 'transfer', 'diagnostic'], default='learning')
            c.add_argument('--incumbent')
        elif name == 'freeze-package':
            c.add_argument('--package', required=True); c.add_argument('--path', required=True); c.add_argument('--notes', required=True)
        elif name == 'run':
            c.add_argument('--batch', required=True); c.add_argument('--policies', nargs='+', required=True)
            c.add_argument('--cases', nargs='+'); c.add_argument('--repeats', type=int, default=1)
            c.add_argument('--purpose', choices=['baseline', 'development', 'transfer', 'evaluation', 'diagnostic'], default='development')
        elif name == 'promote':
            c.add_argument('--package', required=True); c.add_argument('--notes', required=True)
        elif name == 'recover':
            c.add_argument('--parent', required=True)
        elif name == 'rescore':
            c.add_argument('--attempt', required=True, help='an attempt that ended in an evaluator error')
        elif name == 'score-investigation':
            c.add_argument('--case', required=True); c.add_argument('--path', required=True)
        elif name == 'procedure-test':
            c.add_argument('--script', required=True, help='procedure .py within evolve/; called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR')
            c.add_argument('--attempts', nargs='+'); c.add_argument('--cases', nargs='+')
            c.add_argument('--timeout-minutes', type=int, help='per-project limit; settings.json gives the default')
        elif name == 'cancel-test':
            c.add_argument('--test', required=True, help='a running procedure test')
    c = s.add_parser('status'); c.add_argument('--json', action='store_true')
    c = s.add_parser('wait', help='Wait up to 30 minutes for a worker, run group, or request to finish')
    c.add_argument('id'); c.add_argument('--seconds', type=int, default=30)
    c = s.add_parser('response', help='Read a request acknowledgement, not worker completion')
    c.add_argument('id')
    a = vars(p.parse_args())
    try:
        process_monitor()
    except (OSError, ValueError, KeyError) as exc:
        # A process reminder must never break experiment requests or scoring.
        print('Process monitor notice unavailable: ' + str(exc), file=sys.stderr)
    if a['command'] == 'status':
        path = E / ('status.json' if a['json'] else 'STATUS.md')
        print(path.read_text() if path.exists() else 'Controller has not published status yet.')
        return
    if a['command'] in ['wait', 'response']:
        rid = a['id']
        import re
        if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,89}', rid):
            p.error('Invalid ID')
        deadline = time.monotonic() + min(1800, max(0, a.get('seconds', 0)))
        while True:
            d, finished = lookup_progress(rid, a['command'])
            if finished or time.monotonic() >= deadline:
                print(json.dumps(d, indent=2))
                if d['status'] == 'unknown_id':
                    raise SystemExit(2)
                return
            time.sleep(min(2, max(0, deadline - time.monotonic())))
    a = {k: v for k, v in a.items() if v is not None}
    a.setdefault('id', a['command'] + '-' + uuid.uuid4().hex[:12])
    import re
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,89}', a['id']):
        raise ValueError('Invalid request ID')
    folder = W / 'requests'
    folder.mkdir(exist_ok=True)
    path = folder / (a['id'] + '.json')
    text = json.dumps(a, indent=2) + '\n'
    if path.exists():
        if path.read_text() != text:
            raise ValueError('Request ID already used with different content')
        print(json.dumps({'id': a['id'], 'status': 'already_submitted', 'response': str(E / 'responses' / path.name)})); return
    tmp = path.with_suffix('.pending-' + str(os.getpid()))
    tmp.write_text(text)
    # Hard-link publish is atomic and refuses to replace an existing request.
    try:
        os.link(tmp, path)
    finally:
        tmp.unlink()
    print(json.dumps({'id': a['id'], 'status': 'submitted', 'response': str(E / 'responses' / path.name)}))


if __name__ == '__main__':
    main()
