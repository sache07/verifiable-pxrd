"""Run directly in the app task. Tests effective isolation, not a nested sandbox."""
from pathlib import Path
import errno
import hashlib
import importlib
import json
import os
import socket
import subprocess
import sys
import time

W = Path(__file__).resolve().parent
R = W.parent
manifest = json.loads((W / 'environment.json').read_text())
if manifest.get('status') == 'workshop_not_deployed':
    print(json.dumps({'passed': False, 'checks': {'deployment_complete': False},
        'details': {'deployment': 'This workshop is not deployed. Structural-scoring integration '
                    'and controller/isolation verification must finish before starting research.'}}, indent=2))
    sys.exit(1)
checks = {}
details = {}


def denied_read(path):
    try:
        with open(path, 'rb'):
            return False
    except OSError as e:
        # Bubblewrap hides disallowed mounts; Landlock can instead return EACCES.
        # The host setup records that these canaries really exist outside.
        details['blocked:' + str(path)] = str(e)
        return e.errno in [errno.EACCES, errno.EPERM, errno.ENOENT]


def readonly(path):
    try:
        with open(path, 'r+'):
            return False
    except OSError as e:
        return e.errno in [errno.EACCES, errno.EPERM, errno.EROFS]


for name, path in manifest['blocked'].items():
    checks[name] = manifest['canaries_exist_outside'].get(name) is True and denied_read(path)
for path, digest in manifest['immutable'].items():
    p = Path(path)
    checks['hash:' + p.name] = hashlib.sha256(p.read_bytes()).hexdigest() == digest
    checks['readonly:' + p.name] = readonly(p)
for folder in [W / '.tmp', W / 'drafts', W / 'requests', W / 'investigations']:
    p = folder / 'environment-probe.tmp'
    p.write_text('test')
    checks['write:' + folder.name] = p.read_text() == 'test'
    p.unlink()
for path in [R / 'evidence/status.json', R / 'policies/P0/prompt.md']:
    checks['readonly:' + str(path.relative_to(R))] = readonly(path)
try:
    s = socket.create_connection(('1.1.1.1', 443), timeout=2)
    s.close()
    checks['network_blocked'] = False
except OSError as e:
    checks['network_blocked'] = e.errno in [errno.EACCES, errno.EPERM, errno.ENETUNREACH]
    details['network'] = str(e)
for package in ['numpy', 'scipy', 'pymatgen', 'spglib', 'ase', 'pyxtal', 'matplotlib']:
    try:
        importlib.import_module(package)
        checks[package] = True
    except Exception as e:
        checks[package] = False
        details[package] = str(e)
p = subprocess.run([os.environ['GSAS2_PYTHON'], '-c', 'from GSASII import GSASIIscriptable'], capture_output=True, text=True, timeout=30)
checks['GSASII'] = p.returncode == 0
import shutil
checks['dicvol14'] = bool(shutil.which('dicvol14'))
checks['no_secret_environment'] = not any(k in os.environ for k in ['OPENAI_API_KEY', 'CODEX_API_KEY', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'])
status = json.loads((R / 'evidence/status.json').read_text())
from datetime import datetime, timezone
heartbeat = json.loads((R / 'evidence/heartbeat.json').read_text())
age = (datetime.now(timezone.utc) - datetime.fromisoformat(heartbeat['at'])).total_seconds()
checks['controller_recent'] = age < 120
checks['controller_healthy'] = not status.get('error')
details['controller_age_seconds'] = age
report = {'passed': all(checks.values()), 'checks': checks, 'details': details,
          'scope': 'Effective command filesystem, network and tools. Confirm Sol/max in the app selector separately.'}
(W / 'environment_check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
sys.exit(0 if report['passed'] else 1)
