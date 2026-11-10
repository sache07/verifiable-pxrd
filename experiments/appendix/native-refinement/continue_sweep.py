"""Resume selected lanes from an immutable runner snapshot; drain prior calls.

The old local coordinator must be stopped first. Detached Modal calls remain
running and are reconnected by ID, never resubmitted. Inactive methods retain
their completed outputs but receive no new calls.
"""
import argparse
from collections import Counter, deque
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import fcntl
import json
import os
from pathlib import Path
import socket
import sys
import time


def notify_systemd(message):
    """Optional readiness/heartbeat support; harmless outside a systemd unit."""
    address = os.environ.get('NOTIFY_SOCKET')
    if not address:
        return
    if address.startswith('@'):
        address = '\0' + address[1:]
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as sock:
        sock.connect(address)
        sock.sendall(message.encode())


def interleave_panels(queue):
    """Metadata-only queue ordering; preserve candidate slots and task hashes."""
    panels = {}
    for task, key in queue:
        parts = task['case_id'].split('-')
        panel = parts[1] if task['corpus'] == 'pxrd-100' else '-'.join(parts[1:3])
        panels.setdefault((task['corpus'], panel), []).append((task, key))
    groups = [deque(sorted(items, key=lambda item: (item[0]['slot'], item[0]['case_id'])))
              for _, items in sorted(panels.items())]
    result = deque()
    while any(groups):
        for group in groups:
            if group:
                result.append(group.popleft())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--tasks', type=Path, required=True)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--methods', required=True)
    parser.add_argument('--interleave-panels', action='store_true')
    parser.add_argument('--validation', type=Path, help='Require a passed prefix-equivalence check before dispatch')
    args = parser.parse_args()
    root = args.plan.resolve().parent
    # Hold one coordinator per shard, including while reconnecting old calls.
    coordinator_lock = (root / 'coordinator.lock').open('a')
    try:
        fcntl.flock(coordinator_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print('Another coordinator owns this shard; refusing duplicate dispatch.', flush=True)
        raise SystemExit(78)
    notify_systemd('STATUS=Verifying frozen inputs and reconnecting recorded calls')
    plan = json.loads(args.plan.read_text())
    if args.validation:
        while not args.validation.exists():
            notify_systemd('STATUS=Waiting for stage-1 GPU equivalence control\nWATCHDOG=1')
            time.sleep(10)
        validation = json.loads(args.validation.read_text())
        if not validation.get('passed') or validation.get('source_hash') != plan['source_hash']:
            raise ValueError('GPU prefix-equivalence validation failed or belongs to another runner')
    sys.path.insert(0, str(root / 'runner'))
    os.environ['MODAL_PROFILE'] = plan['profile']
    os.environ['NATIVE_REFINEMENT_SOURCES'] = str(args.sources.resolve())
    os.environ['NATIVE_GPU_CONCURRENCY'] = str(plan['gpu_workers'])
    os.environ['NATIVE_CPU_CONCURRENCY'] = str(plan['cpu_workers'])
    from common import code_hash, fingerprint, read_json, verify_task, write_json
    from sweep_budget import Budget
    import modal
    from remote import app, collect, cpu_worker, gpu_worker, SOURCE_HASH_AT_IMPORT
    if SOURCE_HASH_AT_IMPORT != plan['source_hash']:
        raise ValueError('Immutable runner snapshot does not match original plan')
    tasks = read_json(args.tasks)
    if fingerprint(tasks) != plan['tasks_sha256']:
        raise ValueError('Tasks differ from original plan')
    tasks = [t for i, t in enumerate(tasks) if i % plan['shards'] == plan['shard']]
    if [t['id'] for t in tasks] != plan['ids']:
        raise ValueError('Original shard differs')
    enabled = set(args.methods.split(','))
    budget = Budget(plan['ledger'], plan['budget_usd'])
    records = budget.records()
    queues = {'gpu': deque(), 'cpu': deque()}
    reconnect, deferred, statuses = [], Counter(), Counter()
    for task in tasks:
        verify_task(task)
        key = fingerprint({'task': task, 'source': plan['source_hash']})
        prior = records.get(key)
        path = root / 'candidates' / task['id'] / 'result.json'
        if prior and (prior['profile'] != plan['profile'] or prior['output'] != str(root)):
            raise ValueError('Task belongs to another coordinator')
        if path.exists():
            result = read_json(path)
            if not prior or result.get('task_fingerprint') != key:
                raise ValueError('Untracked or mismatched result')
            budget.settle(key, task, result)
            statuses[(task['method'], result['status'])] += 1
        elif prior:
            if not prior.get('call_id'):
                raise ValueError('Ambiguous reservation; inspect before restarting')
            reconnect.append((task, key, prior['call_id']))
        elif task['method'] in enabled:
            queues['gpu' if task['method'] == 'crystalyze' else 'cpu'].append((task, key))
        else:
            deferred[task['method']] += 1
    limits = {'gpu': 2 * plan['gpu_workers'], 'cpu': 2 * plan['cpu_workers']}
    if args.interleave_panels:
        queues = {kind: interleave_panels(queue) for kind, queue in queues.items()}
    active, pending, abort = Counter(), {}, False

    def progress(state):
        write_json(root / 'continued-progress.json', dict(state=state, updated_unix=time.time(),
            methods=sorted(enabled), deferred=dict(deferred),
            coordinator_pid=os.getpid(), interleave_panels=args.interleave_panels,
            collected={f'{m}/{s}': n for (m, s), n in statuses.items()},
            submitted_pending=dict(active), unsubmitted={k: len(v) for k, v in queues.items()}))
        notify_systemd(f'WATCHDOG=1\nSTATUS={state}; collected={sum(statuses.values())}; pending={sum(active.values())}')

    print(f"Resuming {plan['profile']}: {len(reconnect)} calls; enabled {enabled}; deferred {dict(deferred)}", flush=True)
    progress('starting')
    with modal.enable_output(), app.run(name=plan['campaign'] + '-gpu-continuation', detach=True):
        if code_hash() != plan['source_hash']:
            raise ValueError('Snapshot changed during build')
        notify_systemd('READY=1\nWATCHDOG=1\nSTATUS=Dispatcher ready')
        with ThreadPoolExecutor(max_workers=sum(limits.values()) + len(reconnect)) as pool:
            def track(task, key, call, call_id=None):
                kind = 'gpu' if task['method'] == 'crystalyze' else 'cpu'
                active[kind] += 1
                pending[pool.submit(call.get)] = (task, key, kind, call_id or call.object_id)
            for task, key, call_id in reconnect:
                track(task, key, modal.FunctionCall.from_id(call_id), call_id)
            while pending or any(queues.values()):
                # A recoverable pause: finish submitted calls, leave remaining
                # tasks unreserved. Avoid SIGTERM inside reserve/spawn/update.
                drain_requested = (root / 'DRAIN_REQUESTED').exists()
                if not abort and not drain_requested:
                    for kind, queue in queues.items():
                        while queue and active[kind] < limits[kind]:
                            task, key = queue[0]
                            if not budget.reserve(key, task, profile=plan['profile'], output=str(root),
                                    campaign=plan['campaign'], source_hash=plan['source_hash']):
                                break
                            queue.popleft()
                            try:
                                call = (gpu_worker if kind == 'gpu' else cpu_worker).spawn(
                                    task, plan['campaign'], plan['source_hash'])
                                budget.update(key, call_id=call.object_id, state='submitted')
                                track(task, key, call)
                            except Exception as error:
                                budget.update(key, state='submission_unknown', error=repr(error))
                                abort = True
                                break
                progress('draining_after_error' if abort else 'draining_requested' if drain_requested else 'running')
                if not pending:
                    break
                done, _ = wait(pending, timeout=30, return_when=FIRST_COMPLETED)
                for future in done:
                    task, key, kind, call_id = pending.pop(future)
                    active[kind] -= 1
                    try:
                        payload = future.result()
                        collect(payload, root)
                        budget.settle(key, task, payload['result'])
                        statuses[(task['method'], payload['result']['status'])] += 1
                    except Exception as error:
                        budget.update(key, state='collection_error', error=repr(error))
                        print(f'Collection error {call_id}: {error}', flush=True)
                        abort = True
    state = ('needs_recovery' if abort else 'dispatch_paused' if (root / 'DRAIN_REQUESTED').exists()
             and any(queues.values()) else 'budget_paused' if any(queues.values()) else 'complete')
    progress(state)
    if state == 'needs_recovery':
        raise SystemExit(78)
    if state in {'budget_paused', 'dispatch_paused'}:
        raise SystemExit(75)


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        print(f'Configuration/provenance error; manual recovery required: {error}', flush=True)
        raise SystemExit(78)
