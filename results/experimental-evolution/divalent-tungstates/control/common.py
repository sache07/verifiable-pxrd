"""Small, shared infrastructure utilities. No model or scientific policy selection."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'evolve'
CORE = '<HOME>/.local/share/pxrd-baseline/core/bin/python'


def read(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f'.{os.getpid()}.new')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ident(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,89}', value):
        raise ValueError('IDs must be 1–90 letters, numbers, underscores or hyphens')
    return value


def under(root, relative):
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('Use a relative path within the evolve folder')
    root = Path(root).resolve()
    target = root / p
    # Resolve every component; never import agent-provided symlinks.
    if any(q.is_symlink() for q in [target, *target.parents] if q != root.parent):
        raise ValueError('Symlinks are not accepted')
    target = target.resolve()
    if not target.is_relative_to(root):
        raise ValueError('Path escapes its allowed root')
    return target


EXCLUDED = {'.git', '.codex', '.agents', '__pycache__'}


def copy_science(source, dest):
    source, dest = Path(source), Path(dest)
    if source.is_symlink():
        raise ValueError('Symlink source')
    for p in sorted(source.rglob('*')):
        rel = p.relative_to(source)
        if any(x in EXCLUDED for x in rel.parts):
            continue
        if p.is_symlink():
            raise ValueError('Symlink artifact: ' + str(rel))
        if p.is_file():
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)


def hashes(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(Path(root).rglob('*'))
            if p.is_file() and not any(x in EXCLUDED for x in p.relative_to(root).parts)}


def require_scoring_alignment():
    """Never run an inherited evaluator under a different research objective."""
    requested = read(ROOT / 'control/settings.json')['primary_metric']
    config = read(ROOT / 'scorer/config.json')
    implemented = config.get('headline_metric', config.get('rubric', {}).get('score'))
    if implemented != requested:
        raise ValueError(
            f'Scoring deployment incomplete: requested {requested}, but the installed '
            f'evaluator implements {implemented}. Validate and integrate the configured '
            'scorer before deployment; an inherited evaluator is not a fallback.'
        )


def frozen_code_ok():
    require_scoring_alignment()
    freeze = read(ROOT / 'scorer/config_freeze.json')
    if freeze.get('status') != 'frozen_for_synthetic_evaluation':
        raise ValueError('This scorer version is not validated and frozen')
    for name, expected in freeze['code_hashes'].items():
        if sha(ROOT / 'scorer' / name) != expected:
            raise ValueError('Frozen scorer changed: ' + name)
    base = read(ROOT / 'control/infrastructure_freeze.json')
    for name, expected in base['files'].items():
        if sha(ROOT / name) != expected:
            raise ValueError('Frozen infrastructure changed: ' + name)


def register_truth(case):
    import fcntl
    path = ROOT / 'scorer/truth_provenance.json'
    current = {str(p.resolve()): sha(p) for p in
               [*(case / 'inputs').iterdir(), case / 'private/truth.json',
                case / 'private/forward.npz', *(case / 'private/references').glob('*.cif')]}
    with path.with_suffix('.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = read(path) if path.exists() else {}
        key = str(case.resolve())
        if key in data and data[key] != current:
            raise ValueError('Frozen truth was modified')
        data[key] = current
        save(path, data)


def remote(*args, check=True, timeout=60):
    import shlex
    host = read(ROOT / 'control/settings.json')['remote_host']
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', host,
                           shlex.join(map(str, args))], text=True, capture_output=True,
                          check=check, timeout=timeout)


def sync_up(relative):
    host = read(ROOT / 'control/settings.json')['remote_host']
    source = ROOT / relative
    remote('mkdir', '-p', str(source.parent))
    subprocess.run(['rsync', '-a', '--checksum', '--', str(source),
                    host + ':' + str(source.parent) + '/'], check=True, capture_output=True)


def timestamp():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
