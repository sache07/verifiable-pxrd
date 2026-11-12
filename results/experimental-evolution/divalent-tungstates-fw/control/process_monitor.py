"""One read-only process review. Scheduled locally; never starts a researcher."""
from pathlib import Path
import argparse
import datetime as dt
import difflib
import fcntl
import hashlib
import json
import re
import os
import shutil
import subprocess
import time

from common import ROOT, save, read, timestamp, frozen_code_ok

CLI = Path('<HOME>/.codex/packages/standalone/releases/0.160.0-x86_64-unknown-linux-musl/bin/codex')
INTERVAL = 1800
COOLDOWN = 3600
NOTICE_LIFETIME = 7200
REMINDER = (
    'Reread the objective in PROMPT.md. '
    'If the development budget is spent, complete the 3-rollout evaluation and new-batch '
    'comparison with the best-supported frozen package. Another local hypothesis '
    'does not postpone that comparison. Keep unresolved mechanisms for research '
    'across cycles and retain regression checks. Let active assessment workers '
    'finish; distinguish an execution blockage from a scientific problem.'
)


def safe_text(path, limit=12000, tail=False):
    """Snapshot only regular experiment files, never symlinked external answers."""
    path = Path(path)
    if not path.is_file() or any(p.is_symlink() for p in [path, *path.parents]):
        return ''
    text = path.read_text(errors='replace')
    if len(text) <= limit:
        return text
    return ('[earlier text omitted]\n' + text[-limit:]) if tail else (text[:limit] + '\n[later text omitted]')


def eligible(root=ROOT, now=None):
    now = time.time() if now is None else now
    for p in [root/'control/STOP_DISPATCH', root/'control/STOP_DISPATCH.json', root/'evolve/STOP.md']:
        if p.exists():
            return False, 'experiment_stopped'
    status_path = root/'evidence/status.json'
    if not status_path.exists():
        return False, 'no_status'
    status = read(status_path)
    if status.get('paused') or status.get('controller_stopped'):
        return False, 'experiment_paused'
    if status.get('error'):
        return False, 'controller_error'
    heartbeat = root/'evidence/heartbeat.json'
    if not heartbeat.exists() or now - dt.datetime.fromisoformat(read(heartbeat)['at']).timestamp() > 120:
        return False, 'controller_not_live'
    activity = root/'evolve/.monitor/activity.json'
    if not activity.exists() or now - read(activity).get('at_epoch', 0) > 2 * INTERVAL:
        return False, 'researcher_not_recently_active'
    if not status.get('batches'):
        return False, 'no_learning_batch_yet'
    return True, None


def pending_notice(root=ROOT, now=None):
    now = time.time() if now is None else now
    path = root/'evidence/monitor/notice.json'
    if not path.exists():
        return False
    notice = read(path)
    receipt = root/'evolve/.monitor/receipt.json'
    received = read(receipt).get('id') if receipt.exists() else None
    return notice.get('expires_at_epoch', 0) > now and notice['id'] != received


def snapshot(root=ROOT):
    status = read(root/'evidence/status.json')
    jobs = [{k: j.get(k) for k in ['id', 'case_id', 'policy', 'group', 'purpose',
             'status', 'score_100', 'score_status', 'score_interval', 'D_poisson', 'independent_atomic_rwp']}
            for j in status.get('jobs', [])]
    guides = sorted((root/'evolve/packages').glob('*/guidance.md'), key=lambda p: p.stat().st_mtime)
    recent = guides[-2:]
    notes = sorted((root/'evolve/investigations').glob('*.md'), key=lambda p: p.stat().st_mtime)[-4:]
    state = read(root/'control/monitor/state.json') if (root/'control/monitor/state.json').exists() else {}
    data = {
        'original_task': safe_text(root/'evolve/PROMPT.md', 16000),
        'lab_scope': safe_text(root/'evolve/LAB.md', 16000),
        'research_state': safe_text(root/'evolve/STATE.md', 18000),
        'investigation_ledger': safe_text(root/'evolve/investigations/ledger.md', 14000, tail=True),
        'recent_notes': {str(p.relative_to(root)): safe_text(p, 4000) for p in notes},
        'batches': status.get('batches', {}),
        'development_cycle': status.get('development_cycle', {}),
        'current_promoted_package': status.get('current_package'),
        'primary_metric': status.get('primary_metric'),
        'recent_attempts': jobs[-120:],
        'attempts_omitted_from_snapshot': max(0, len(jobs)-120),
        'packages': [{'name': p.parent.name, 'guidance_words': len(safe_text(p, 1000000).split()),
                      'helpers': [q.name for q in sorted((p.parent/'helpers').glob('*.py'))]} for p in guides],
        'latest_guidance': safe_text(recent[-1], 17000) if recent else '',
        'latest_guidance_change': ''.join(difflib.unified_diff(
            safe_text(recent[0], 30000).splitlines(True), safe_text(recent[-1], 30000).splitlines(True),
            fromfile=recent[0].parent.name, tofile=recent[-1].parent.name))[:12000] if len(recent)==2 else '',
    }
    # Review history is separate from the change fingerprint, so a quiet decision
    # does not itself trigger another model call on unchanged evidence.
    digest = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    data['previous_checks'] = state.get('history', [])[-4:]
    return data, digest


def prepare_review(run, data, root=ROOT):
    work, monitor_home = run/'workspace', run/'codex-home'
    for p in [work/'.tmp', work/'.cache', monitor_home]:
        p.mkdir(parents=True, exist_ok=True)
    save(work/'snapshot.json', data)
    # Reuse the researcher's disabled integrations and clean shell environment,
    # but grant this reader only its snapshot and scratch directory.
    header = (root/'evolve/.codex/config.toml').read_text().split('[permissions.')[0]
    header = re.sub(r'default_permissions = "[^"]*"', 'default_permissions = "pxrd-process-monitor"', header)
    header = header.replace(str(root/'evolve'), str(work))
    header = 'project_doc_max_bytes = 0\n' + header
    permissions = {'":root"': 'deny', '":minimal"': 'read', '":tmpdir"': 'write', '":slash_tmp"': 'deny'}
    for path in [work, CLI.parent, Path('<HOME>/.local/share/pxrd-baseline/core'),
                 Path('<HOME>/.local/share/uv/python')]:
        permissions[json.dumps(str(path))] = 'read'
    for path in [work/'.tmp', work/'.cache']:
        permissions[json.dumps(str(path))] = 'write'
    config = header + '\n[permissions.pxrd-process-monitor]\nextends = ":read-only"\n'
    config += '[permissions.pxrd-process-monitor.filesystem]\n'
    config += ''.join(f'{key} = {json.dumps(value)}\n' for key, value in permissions.items())
    config += '\n[permissions.pxrd-process-monitor.network]\nenabled = false\n'
    (monitor_home/'config.toml').write_text(config)
    # The CLI authenticates outside tool execution; the command sandbox cannot
    # read this home or the credential target.
    (monitor_home/'auth.json').symlink_to(Path('<HOME>/.codex/auth.json'))
    env = {k: v for k, v in os.environ.items() if k in ['PATH', 'LANG', 'LC_ALL', 'USER', 'HOME', 'XDG_RUNTIME_DIR']}
    env.update(CODEX_HOME=str(monitor_home), TMPDIR=str(work/'.tmp'), PYTHONDONTWRITEBYTECODE='1')
    return work, env


def model_review(run, data, root=ROOT):
    work, env = prepare_review(run, data, root)
    prompt = (root/'control/MONITOR.md').read_text() + '\n\nSnapshot:\n' + json.dumps(data, indent=2)
    (run/'prompt.txt').write_text(prompt)
    command = [str(CLI), 'exec', '-C', str(work), '--skip-git-repo-check', '--strict-config',
               '--json', '--color', 'never', '--output-schema', str(root/'control/monitor_schema.json'),
               '-o', str(run/'decision.json'), '-']
    try:
        with (run/'events.jsonl').open('w') as stdout, (run/'stderr.log').open('w') as stderr:
            p = subprocess.run(command, input=prompt, text=True, env=env, cwd=work,
                               stdout=stdout, stderr=stderr, timeout=300)
        if p.returncode:
            raise RuntimeError(f'monitor model exited {p.returncode}; see {run.name}/stderr.log')
        answer = read(run/'decision.json')
        if (set(answer) != {'action', 'reason'} or answer['action'] not in ['leave_alone', 'nudge']
                or not isinstance(answer['reason'], str) or not 1 <= len(answer['reason']) <= 800):
            raise ValueError('Invalid monitor decision')
        return answer
    finally:
        (run/'codex-home/auth.json').unlink(missing_ok=True)


def record(root, state, entry):
    state['history'] = (state.get('history', []) + [entry])[-4:]
    save(root/'control/monitor/state.json', state)
    public = root/'evidence/monitor'
    public.mkdir(parents=True, exist_ok=True)
    with (public/'decisions.jsonl').open('a') as f:
        f.write(json.dumps(entry) + '\n')
    save(public/'latest.json', entry)


def check(root=ROOT, review=model_review):
    folder = root/'control/monitor'; folder.mkdir(parents=True, exist_ok=True)
    with (folder/'lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'status': 'skipped', 'reason': 'review_already_running'}
        ok, why = eligible(root)
        if not ok:
            return {'status': 'skipped', 'reason': why}
        state = read(folder/'state.json') if (folder/'state.json').exists() else {}
        if pending_notice(root):
            return {'status': 'skipped', 'reason': 'notice_not_yet_delivered'}
        if time.time() - state.get('last_nudge_epoch', 0) < COOLDOWN:
            return {'status': 'skipped', 'reason': 'nudge_cooldown'}
        data, digest = snapshot(root)
        if digest == state.get('last_snapshot_sha256'):
            return {'status': 'skipped', 'reason': 'unchanged_evidence'}
        run_id = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        run = folder/'runs'/run_id; run.mkdir(parents=True)
        try:
            answer = review(run, data, root)
            # A user stop or pause during the model call suppresses delivery.
            ok, why = eligible(root)
            entry = {'id': run_id, 'at': timestamp(), **answer, 'snapshot_sha256': digest,
                     'delivered_notice': False}
            if ok and answer['action'] == 'nudge':
                issued = time.time()
                save(root/'evidence/monitor/notice.json', {
                    'id': run_id, 'message': REMINDER, 'at': timestamp(),
                    'expires_at_epoch': issued + NOTICE_LIFETIME})
                state['last_nudge_epoch'] = issued
                entry['delivered_notice'] = True
            elif not ok:
                entry['suppressed_reason'] = why
            state['last_snapshot_sha256'] = digest
        except Exception as e:
            entry = {'id': run_id, 'at': timestamp(), 'action': 'error', 'reason': str(e),
                     'delivered_notice': False}
        record(root, state, entry)
        return entry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot-only', action='store_true')
    args = parser.parse_args()
    if args.snapshot_only:
        print(json.dumps(snapshot()[0], indent=2))
    else:
        frozen_code_ok()
        print(json.dumps(check()))
