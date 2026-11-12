"""Persistent file-queue controller. Scientific choices belong to the app agent."""
from pathlib import Path
import argparse
import fcntl
import hashlib
import json
import os
import random
import shutil
import statistics
import subprocess
import time
import threading
import traceback

from common import ROOT, WORK, CORE, read, save, sha, ident, under, copy_science, hashes, remote, sync_up, timestamp, frozen_code_ok
from artifacts import freeze_batch, freeze_package
from progression import development_cycle, check_candidate_capacity, require_transfer_complete
from comparison import solve_flags, fresh, case_state, paired_comparison, comparison_lines
from procedure_test import start as start_procedure_test, check as check_procedure_tests, cancel as cancel_procedure_test

TERMINAL = {'complete', 'evaluator_error', 'infrastructure_error', 'interrupted'}
LAUNCHING = ['dispatching', 'dispatched', 'starting']


def load_state():
    return read(ROOT / 'control/state.json')


def persist(state):
    save(ROOT / 'control/state.json', state)


def make_jobs(state, request):
    bid = ident(request['batch'])
    batch = state['batches'][bid]
    policies = request.get('policies', ['P0'])
    cases = request.get('cases') or batch['cases']
    if not policies or len(set(policies)) != len(policies) or not cases or len(set(cases)) != len(cases):
        raise ValueError('Select nonempty unique cases and policies')
    if any(p not in state['packages'] for p in policies) or any(c not in batch['cases'] for c in cases):
        raise ValueError('Unregistered package or case')
    repeats = request.get('repeats', 1)
    if type(repeats) is not int or repeats < 1:
        raise ValueError('repeats must be a positive integer')
    purpose = request.get('purpose', 'development')
    if purpose not in ['baseline', 'development', 'transfer', 'evaluation', 'diagnostic']:
        raise ValueError('Unknown purpose')
    if purpose == 'transfer' and batch['kind'] != 'transfer':
        raise ValueError('Use a frozen transfer batch for a prospective comparison')
    if batch.get('diagnostic_only') and purpose != 'diagnostic':
        raise ValueError('This batch has reference review flags; use diagnostic purpose')
    if batch['kind'] == 'transfer' and not batch.get('transfer_group'):
        if purpose != 'transfer' or set(cases) != set(batch['cases']) or set(policies) != {'P0', batch['incumbent']} or repeats < 3:
            raise ValueError('First transfer comparison requires all cases, P0 and frozen incumbent, at least three fresh attempts each')
    if purpose == 'transfer' and any(j['case_id'] in cases for j in state['jobs'].values()):
        raise ValueError('Cases with prior worker outcomes are development cases, not fresh transfer')
    if purpose != 'transfer':
        require_transfer_complete(state, bid)
    rid = ident(request['id'])
    if rid in state['groups']:
        raise ValueError('Run group exists; inspect it instead of launching duplicates')
    jobs = []
    cfg = read(ROOT / 'control/settings.json')
    rng = random.Random(rid)
    for repeat in range(1, repeats + 1):
        round_jobs = []
        for cid in cases:
            for policy in policies:
                suffix = hashlib.sha256(f'{rid}/{cid}/{policy}/{repeat}'.encode()).hexdigest()[:12]
                jid = ident(rid[:45] + '-' + suffix)
                job = {'id': jid, 'role': 'solver', 'case_id': cid, 'case_path': str(ROOT / 'cases' / cid),
                       'policy': policy, 'replicate': repeat, 'group': rid, 'batch': bid,
                       'purpose': purpose, 'model': cfg['model'], 'effort': cfg['solver_effort'],
                       'timeout_seconds': cfg['solver_timeout_seconds'], 'resource': 'full', 'excluded_ids': []}
                round_jobs.append(job)
        # Fix the entire schedule before any results. Breadth-first: every case and
        # condition once before any repeat. Shuffle each round deterministically to
        # interleave conditions rather than finish one condition before starting another.
        rng.shuffle(round_jobs)
        jobs += round_jobs
    check_candidate_capacity(state, jobs, purpose, cfg['candidates_per_cycle'])
    group = {'id': rid, 'batch': bid, 'cases': cases, 'policies': policies, 'repeats': repeats,
             'purpose': purpose, 'created_at': timestamp(), 'jobs': [j['id'] for j in jobs],
             'comparison_scope': ('baseline-only new batch; no learned-transfer claim' if purpose == 'transfer' and policies == ['P0']
                                  else 'P0 versus frozen incumbent' if purpose == 'transfer' else purpose),
             'package_hashes': {p: sha(ROOT / 'policies' / p / 'prompt.md') for p in policies}}
    return group, jobs


def add_jobs(state, group, jobs):
    for j in jobs:
        if j['id'] in state['jobs']:
            raise ValueError('Duplicate attempt ID')
        save(ROOT / 'control/jobs' / (j['id'] + '.json'), j)
        state['jobs'][j['id']] = {**j, 'status': 'queued'}
    state['groups'][group['id']] = group
    if group.get('purpose') == 'transfer':
        state['batches'][group['batch']]['transfer_group'] = group['id']
    save(ROOT / 'evidence/groups' / (group['id'] + '.json'), group)


def handle(state, r):
    command = r['command']
    if command == 'freeze-batch':
        incumbent = r.get('incumbent', state['current_package'])
        if incumbent not in state['packages']:
            raise ValueError('Freeze the incumbent package first')
        r['incumbent'] = incumbent
        result = freeze_batch(r)
        state['batches'][result['id']] = result
        for cid in result['cases']:
            sync_up('cases/' + cid)
        sync_up('scorer/truth_provenance.json')
        return result
    if command == 'freeze-package':
        result = freeze_package(r)
        state['packages'][result['id']] = result
        sync_up('policies/' + result['id'])
        return result
    if command == 'run':
        group, jobs = make_jobs(state, r)
        add_jobs(state, group, jobs)
        return group
    if command == 'recover':
        parent = state['jobs'][r['parent']]
        if parent['status'] not in ['interrupted', 'infrastructure_error', 'retry_wait'] or parent.get('superseded_by'):
            raise ValueError('Recovery requires an unrecovered infrastructure interruption')
        if state['paused']:
            raise ValueError('Resolve the pause and resume dispatch before requesting recovery')
        mode = json.loads(remote(CORE, ROOT / 'control/remote.py', 'recovery-mode', parent['id']).stdout)
        job = read(ROOT / 'control/jobs' / (parent['id'] + '.json'))
        jid = ident(r['id'])
        job.update(id=jid, recovery_of=parent['id'])
        if r.get('capacity_retry'):
            job['capacity_retry'] = True
        if mode['mode'] == 'resume':
            job.update(continuation_of=parent['id'], infrastructure_recovery=True,
                       continuation_instruction='Resume the interrupted task under the same condition. Preserve your previous work and finish the original scientific task.')
        save(ROOT / 'control/jobs' / (jid + '.json'), job)
        state['jobs'][jid] = {**job, 'status': 'queued'}
        parent['superseded_by'] = jid
        group = state['groups'][parent['group']]
        group.setdefault('recovery_history', []).append({'from': parent['id'], 'to': jid, **mode})
        group['jobs'] = [jid if x == parent['id'] else x for x in group['jobs']]
        persist(state)
        save(ROOT / 'evidence/groups' / (group['id'] + '.json'), group)
        return {'job': jid, **mode, 'counting': 'Replacement of the interrupted slot, not another independent replicate.'}
    if command == 'promote':
        policy = ident(r['package'])
        if policy not in state['packages']:
            raise ValueError('Unknown package')
        notes = under(WORK, r['notes']).read_text()
        cycle = development_cycle(state, read(ROOT / 'control/settings.json')['candidates_per_cycle'])
        result = paired_comparison(score_rows(state), state['current_package'],
                                   {policy: cycle['cycle_cases'].get(policy, [])})
        entry = result['packages'].get(policy)
        if not entry or not entry['meets_rule']:
            raise ValueError(f"{policy} does not meet the promotion rule against {state['current_package']} on the cases "
                             'it ran this cycle: three fresh solves of each on every case, at least six cases, '
                             'Δ ≥ max(4, 2 × noise) and no case more than 15 below. See the comparison in STATUS.md.')
        record = {'at': timestamp(), 'package': policy, 'previous': state['current_package'], 'rationale': notes,
                  'comparison': entry,
                  'scope': 'Researcher selection under the promotion rule, not proof of reliable superiority.'}
        save(ROOT / 'evidence/decisions' / (r['id'] + '.json'), record)
        state['current_package'] = policy
        return record
    if command == 'pause':
        state['paused'] = True
        state['pause_reason'] = 'Requested pause of new dispatch; running solvers continue.'
        return {'paused': True}
    if command == 'resume':
        remote(CORE, ROOT / 'control/remote.py', 'resume')
        state['paused'] = False
        state.pop('pause_reason', None)
        return {'paused': False, 'interrupted_attempts': 'Not automatically replayed'}
    if command == 'score-investigation':
        # Direct researcher calculations are valuable but must not masquerade as
        # independent solver improvement. Preserve their provenance explicitly.
        cid = ident(r['case'])
        if not (ROOT / 'cases' / cid).is_dir():
            raise ValueError('Unknown frozen case')
        for bid, batch in state['batches'].items():
            if cid in batch['cases']:
                require_transfer_complete(state, bid)
        source = under(WORK, r['path'])
        dest = ROOT / 'evidence/investigations' / r['id']
        if dest.exists():
            raise ValueError('Investigation snapshot exists')
        copy_science(source, dest / 'workspace')
        record = {'id': r['id'], 'case_id': cid, 'case_path': str(ROOT / 'cases' / cid),
                  'workspace': str(dest / 'workspace'), 'condition': 'researcher-calculation',
                  'cohort': 'diagnostic', 'split': 'training', 'oracle_access': True}
        save(dest / 'record.json', record)
        p = subprocess.run([CORE, str(ROOT / 'control/scoring.py'), 'score', str(dest / 'record.json')], capture_output=True, text=True)
        (dest / 'scorer.log').write_text(p.stdout + p.stderr)
        score = ROOT / 'scorer/scores' / r['id'] / 'score.json'
        if score.exists():
            shutil.copy2(score, dest / 'score.json')
        return {'path': str(dest), 'score_status': read(score)['score_status'] if score.exists() else 'evaluator_error',
                'scope': 'Researcher diagnostic with access to synthetic truth; excluded from rollout comparisons.'}
    if command == 'procedure-test':
        return start_procedure_test(state, r)
    if command == 'cancel-test':
        return cancel_procedure_test(state, r)
    if command == 'rescore':
        job = state['jobs'][ident(r['attempt'])]
        if job['status'] != 'evaluator_error':
            raise ValueError('Only an attempt that ended in an evaluator error can be rescored')
        result = json.loads(remote(CORE, ROOT / 'control/remote.py', 'rescore', job['id'], timeout=900).stdout)
        # The next poll collects the new score.
        job.update(status=result['status'], collected=False)
        return result
    raise ValueError('Unknown command: ' + str(command))


def requests(state):
    for p in sorted((WORK / 'requests').glob('*.json')):
        if p.is_symlink():
            continue
        try:
            r = read(p)
            rid = ident(r['id'])
            if p.name != rid + '.json':
                raise ValueError('Request ID must match filename')
            digest = sha(p)
            old = state['requests'].get(rid)
            if old:
                if old['sha256'] != digest:
                    save(ROOT / 'evidence/responses' / (rid + '-mutation.json'), {'error': 'Request ID reused with changed contents; original action was not replayed.'})
                continue
            # Reserve before executing. On a crash, operator reconciliation is
            # required; never silently repeat an operation with an unknown outcome.
            state['requests'][rid] = {'status': 'processing', 'sha256': digest, 'at': timestamp()}
            persist(state)
            save(ROOT / 'evidence/responses' / p.name, {'id': rid, 'status': 'processing'})
            frozen_code_ok()
            value = handle(state, r)
            # A procedure test keeps running after acceptance; its runner writes the final response.
            running = isinstance(value, dict) and value.get('state') == 'running'
            answer = {'id': rid, 'status': 'running' if running else 'accepted', 'result': value, 'at': timestamp()}
            state['requests'][rid]['status'] = 'accepted'
        except Exception as e:
            rid = p.stem
            answer = {'id': rid, 'status': 'error', 'error': str(e), 'at': timestamp()}
            with (ROOT / 'control/errors.log').open('a') as f:
                f.write(timestamp() + '\n' + traceback.format_exc() + '\n')
            if rid in state['requests']:
                state['requests'][rid]['status'] = 'error'
        persist(state)
        save(ROOT / 'evidence/responses' / (rid + '.json'), answer)
        # Poll/collect workers between new requests. A series of direct scoring
        # diagnostics must not keep the worker status and dispatch stale for
        # the duration of the whole request queue.
        if rid in state['requests']:
            break


def collect(job):
    jid = ident(job['id'])
    host = read(ROOT / 'control/settings.json')['remote_host']
    dest = ROOT / 'evidence/attempts' / jid
    dest.mkdir(parents=True, exist_ok=True)
    remote_base = ROOT / 'attempts' / jid
    # Includes .tmp; excludes auth, Codex homes, caches and symlinks.
    specs = [(remote_base / 'workspace', dest), (remote_base / 'run', dest),
             (ROOT / 'evidence/attempts' / jid, dest.parent)]
    for src, target in specs:
        p = subprocess.run(['rsync', '-rlt', '--exclude=__pycache__', '--exclude=.codex',
                            '--exclude=.agents', '--exclude=.git', '--', host + ':' + str(src), str(target) + '/'],
                           capture_output=True, text=True)
        if p.returncode != 0 and not (p.returncode == 23 and job['status'] in ['infrastructure_error', 'interrupted']):
            raise RuntimeError('Evidence transfer failed: ' + p.stderr[-1200:])
    # Exact raw worker events and command outputs are in run/codex-events.jsonl.
    if (dest / 'workspace').exists():
        save(dest / 'artifact_hashes.json', hashes(dest / 'workspace'))
    save(dest / 'collection.json', {'at': timestamp(), 'includes_tmp': True, 'job': job,
                                  'scope': 'Scientific files and full worker events; no credentials or other experiments.'})
    # GSAS-II's automatic .bakN.gpx copies are about 40% of an attempt. The collected evidence keeps them;
    # the EC2 copy, which recoveries resume from, does not need them.
    remote('find', str(remote_base / 'workspace'), '-type', 'f', '-name', '*.bak[0-9]*.gpx', '-delete', check=False)
    # The job's viewer window would otherwise keep following a finished attempt indefinitely.
    settings = read(ROOT / 'control/settings.json')
    remote('tmux', '-L', settings['tmux_socket'], 'kill-window', '-t', settings['tmux_session'] + ':' + jid[-16:],
           check=False, timeout=10)


def unconfirmed(job):
    """A launch the service has not yet accepted: no solver item so far. Capacity
    rejections arrive within seconds; a launch silent for 15 minutes has another fault."""
    waiting = job['status'] in LAUNCHING or (job['status'] == 'running' and not job.get('remote_status', {}).get('work_started'))
    return waiting and time.time() - job.get('dispatched_at', 0) < 900


def next_launch(state):
    """Head of the queue: a capacity-rejected slot, retried via normal recovery once its
    interval has passed, then queued jobs in schedule order."""
    pending = [j for j in state['jobs'].values() if j['status'] == 'queued' and j.get('capacity_retry')]
    if pending:
        return pending[0]
    waiting = [j for j in state['jobs'].values() if j['status'] == 'retry_wait' and not j.get('superseded_by')]
    if waiting:
        head = min(waiting, key=lambda j: j['capacity_retry_at'])
        if time.time() < head['capacity_retry_at']:
            return None
        # The replacement ID is deterministic; a restart cannot add another slot.
        rid = 'capacity-' + hashlib.sha256(head['id'].encode()).hexdigest()[:20]
        try:
            return state['jobs'][handle(state, {'command': 'recover', 'id': rid, 'parent': head['id'], 'capacity_retry': True})['job']]
        except Exception as exc:
            head.update(status='infrastructure_error', capacity_retry_blocked=str(exc))
            persist(state)
            return None
    return next((j for j in state['jobs'].values() if j['status'] == 'queued'), None)


def poll_and_dispatch(state):
    retry_seconds = read(ROOT / 'control/settings.json').get('capacity_retry_seconds', 0)
    info = json.loads(remote(CORE, ROOT / 'control/remote.py', 'status').stdout)
    if info['usage_pause']:
        state.update(paused=True, pause_reason=info['usage_pause']['reason'])
    for jid, data in info['jobs'].items():
        if jid not in state['jobs']:
            continue
        job = state['jobs'][jid]
        if job['status'] == 'queued' and data['status'] == 'not_started':
            continue
        if data['status'] in TERMINAL and not job.get('collected'):
            try:
                collect({**job, 'status': data['status']})
            except Exception as exc:
                # Retried on the next poll; other jobs keep moving.
                job['collection_error'] = str(exc)[-500:]
                continue
            job['collected'] = True
            job.pop('collection_error', None)
        job['status'] = data['status']
        job['remote_status'] = data
        detail = data.get('detail', {})
        if (retry_seconds and data['status'] == 'interrupted' and detail.get('capacity_limited')
                and not detail.get('infrastructure_failure') and not job.get('superseded_by')
                and not job.get('capacity_retry_blocked')):
            job.setdefault('capacity_retry_at', time.time() + retry_seconds)
            job['status'] = 'retry_wait'
    busy = sum(j['status'] in LAUNCHING + ['running', 'scoring'] for j in state['jobs'].values())
    limit = read(ROOT / 'control/settings.json')['max_concurrent_solvers']
    # One launch at a time: the next goes once the last has produced solver output, so
    # under a capacity limit one launch is rejected per retry interval, not a burst.
    job = None
    if not state['paused'] and busy < limit and not any(unconfirmed(j) for j in state['jobs'].values()):
        job = next_launch(state)
    if job:
        # Keep payload immutable; dispatch state lives separately.
        sync_up('control/jobs/' + job['id'] + '.json')
        job.update(status='dispatching', dispatched_at=time.time())
        persist(state)
        result = remote(CORE, ROOT / 'control/remote.py', 'launch', job['id'])
        job['status'] = json.loads(result.stdout)['status']
        try:
            settings = read(ROOT / 'control/settings.json')
            remote('tmux', '-L', settings['tmux_socket'], 'new-window', '-d', '-t', settings['tmux_session'], '-n', job['id'][-16:],
                   CORE + ' ' + str(ROOT / 'control/view.py') + ' ' + job['id'], check=False, timeout=10)
        except Exception:
            pass
    persist(state)


def scored(entries, flagged=True):
    """Completed attempts' scores, provisional (†) ones included unless flagged=False; never evaluator errors."""
    skip = ['verification_error'] + ([] if flagged else ['needs_adjudication'])
    return [x['score_100'] for x in entries if x['score_100'] is not None and x['score_status'] not in skip and x['status'] == 'complete']


def score_rows(state):
    rows = []
    for j in state['jobs'].values():
        path = ROOT / 'evidence/attempts' / j['id'] / 'score.json'
        score = read(path) if path.exists() else {}
        recovered, at_floor = solve_flags(score)
        rows.append({k: j.get(k) for k in ['id', 'case_id', 'policy', 'group', 'purpose', 'replicate', 'status', 'superseded_by', 'recovery_of', 'capacity_retry_at', 'capacity_retry_blocked']} |
                    {k: score.get(k) for k in ['score_100', 'score_status', 'score_interval', 'D_poisson', 'independent_atomic_rwp', 'physical_validity']} |
                    {'recovered': recovered, 'at_floor': at_floor})
    return rows


def report(state, error=None):
    evaluator_version = read(ROOT / 'scorer/config.json')['version']
    rows = score_rows(state)
    summary = {'at': timestamp(), 'controller_pid': os.getpid(), 'paused': state['paused'],
               'evaluator_version': evaluator_version,
               'primary_metric': read(ROOT / 'control/settings.json')['primary_metric'],
               'pause_reason': state.get('pause_reason'), 'current_package': state['current_package'],
               'jobs': rows, 'batches': state['batches'], 'groups': state['groups'],
               'requests': state['requests'], 'procedure_tests': state.get('procedure_tests', {}), 'error': error}
    cycle = development_cycle(state, read(ROOT / 'control/settings.json')['candidates_per_cycle'])
    summary['development_cycle'] = cycle
    comparison = paired_comparison(rows, state['current_package'], cycle['cycle_cases'])
    summary['comparison'] = comparison
    save(ROOT / 'evidence/status.json', summary)
    lines = ['# Experiment status', '', 'Current package: ' + state['current_package'], '',
             'Evaluator: ' + evaluator_version + '. Frozen configuration: ../scorer/config_freeze.json; compare scores from the same evaluator.', '',
             'Dispatch paused: ' + str(state['paused']) + ('. ' + state.get('pause_reason', '') if state['paused'] else ''), '',
             '| Group | Case | Condition | Individual scores | Mean | Mean without † | D (lower is better) | Independent Rwp % | Scored / slots | Pending or failed infrastructure |',
             '|---|---|---|---|---:|---:|---|---|---:|---:|']
    lines[4:4] = [f"Development cycle {cycle['cycle']}: {cycle['candidates_used']} of {cycle['candidates_allowed']} package versions evaluated"
                  + (f" ({', '.join(cycle['candidates'])})" if cycle['candidates'] else '') + '. '
                  + ('The next step is a prospective new-batch comparison.' if cycle['candidates_spent'] else 'The comparison may be taken earlier.'),
                  'Pending prospective comparisons: ' + (', '.join(cycle['comparisons_pending']) or 'none') + '.', '']
    groups = {}
    for row in rows:
        if row.get('superseded_by'):
            continue
        groups.setdefault((row['group'], row['case_id'], row['policy']), []).append(row)
    for (gid, cid, policy), entries in groups.items():
        good = scored(entries)
        individual = ', '.join(
            f"{x['score_100']:.1f}" + ('†' if x['score_status'] == 'needs_adjudication' else '')
            if x['score_100'] is not None else
            f"{x['score_interval'][0]:.1f}–{x['score_interval'][1]:.1f}†"
            if x.get('score_interval') is not None else
            (x['score_status'] or x['status']) for x in entries)
        mean = f'{statistics.mean(good):.1f}' if good else '—'
        clean = scored(entries, flagged=False)
        unflagged = f'{statistics.mean(clean):.1f}' if clean else '—'
        rwps = ', '.join(f'{x["independent_atomic_rwp"]:.2f}' if x['independent_atomic_rwp'] is not None else '—' for x in entries)
        discrepancies = ', '.join(f'{x["D_poisson"]:.3f}' if x['D_poisson'] is not None else '—' for x in entries)
        lines.append(f'| {gid} | {cid} | {policy} | {individual} | {mean} | {unflagged} | {discrepancies} | {rwps} | {len(good)}/{len(entries)} | {sum(x["status"] != "complete" for x in entries)} |')
    lines += ['', 'Means include provisional (†) scores; nothing adjudicates them, and most belong to failed attempts, so leaving them out would flatter the condition that failed. Mean without † is shown beside it. Both exclude evaluator errors and show denominators. Scientific failures and invalid submissions remain in both. † Provisional physical/registration review.', '', 'Last update: ' + summary['at']]
    pooled = {}
    for row in rows:
        if not row.get('superseded_by') and row['purpose'] in ['baseline', 'development', 'evaluation', 'transfer']:
            pooled.setdefault((row['case_id'], row['policy']), []).append(row)
    if pooled:
        lines += ['', '## All fresh attempts by case and frozen package', '',
                  'This includes every recorded fresh attempt, not just the best round. Consult the group table to distinguish training, evaluation and prospective transfer.', '',
                  'Recovered: the hidden phases matched one to one, physically valid, D ≤ 1. At floor: recovered with D ≤ 0.1. '
                  'The state uses scored solves: at floor when all are, recovered when all are, inconsistent when some are, otherwise unrecovered.', '',
                  '| Case | Package | Scored / slots | Mean | Mean without † | Minimum | Recovered | At floor | State |',
                  '|---|---|---:|---:|---:|---:|---:|---:|---|']
        states = fresh(rows)
        for (cid, policy), entries in pooled.items():
            good = scored(entries)
            clean = scored(entries, flagged=False)
            mean = f'{statistics.mean(good):.1f}' if good else '—'
            unflagged = f'{statistics.mean(clean):.1f}' if clean else '—'
            minimum = f'{min(good):.1f}' if good else '—'
            counted = states.get((cid, policy), [])
            lines.append(f'| {cid} | {policy} | {len(good)}/{len(entries)} | {mean} | {unflagged} | {minimum} | '
                         f"{sum(x['recovered'] for x in counted)}/{len(counted)} | {sum(x['at_floor'] for x in counted)}/{len(counted)} | "
                         f"{case_state(counted) or '—'} |")
    lines += comparison_lines(comparison)
    if error:
        lines += ['', 'Controller issue: ' + error]
    (ROOT / 'evidence/STATUS.md').write_text('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--once', action='store_true')
    args = parser.parse_args()
    with (ROOT / 'control/broker.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        def heartbeat():
            while True:
                save(ROOT / 'evidence/heartbeat.json', {'at': timestamp(), 'pid': os.getpid()})
                time.sleep(5)
        threading.Thread(target=heartbeat, daemon=True).start()
        state = load_state()
        # Never replay an operation interrupted in the middle of its effects.
        for rid, req in state['requests'].items():
            if req['status'] == 'processing':
                req['status'] = 'needs_reconciliation'
                save(ROOT / 'evidence/responses' / (rid + '.json'), {'id': rid, 'status': 'needs_reconciliation',
                     'error': 'Controller restarted during this request. Inspect frozen artifacts before issuing another request.'})
        while True:
            error = None
            try:
                requests(state)
                check_procedure_tests(state)
                poll_and_dispatch(state)
            except Exception as e:
                error = str(e)
                with (ROOT / 'control/errors.log').open('a') as f:
                    f.write(timestamp() + '\n' + traceback.format_exc() + '\n')
            report(state, error)
            persist(state)
            try:
                sync_up('evidence/STATUS.md')
            except Exception:
                pass  # Local status remains available during a transport outage.
            if args.once:
                return
            time.sleep(10)


if __name__ == '__main__':
    main()
