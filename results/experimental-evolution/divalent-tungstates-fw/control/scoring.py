"""Separate process avoids module-name collisions with the frozen scorer."""
from pathlib import Path
import fcntl
import json
import sys
import time

R = Path(__file__).resolve().parents[1]
if len(sys.argv) > 1 and sys.argv[1] == 'score':
    # Check before importing the scorer's module named common.
    from common import require_scoring_alignment
    require_scoring_alignment()
    del sys.modules['common']
# Shared scoring locks preserve concurrency; deployment takes the exclusive
# lock so an evaluation cannot load a mixture of two implementation versions.
_version_lock=(R / 'control/evaluator.lock').open('a')
fcntl.flock(_version_lock,fcntl.LOCK_SH)
sys.path.insert(0, str(R / 'scorer/src'))
from common import load_structure
from structure_metrics import physical_screen


if sys.argv[1] == 'audit':
    rows = {}
    for case in sorted(Path(sys.argv[2]).iterdir()):
        rows[case.name] = [physical_screen(load_structure(p)) for p in sorted((case / 'private/references').glob('*.cif'))]
    print(json.dumps(rows))
elif sys.argv[1] == 'score':
    from score import score_attempt
    from common import CONFIG, save_json
    record = json.loads(Path(sys.argv[2]).read_text())
    started = time.monotonic()
    result = score_attempt(record)
    result['evaluation_wall_seconds'] = time.monotonic() - started
    result['evaluator_version'] = CONFIG['version']
    save_json(R / 'scorer/scores' / record['id'] / 'score.json', result)
    print(json.dumps({k: result.get(k) for k in ['id', 'score_status', 'score_100', 'score_interval', 'D_poisson', 'independent_atomic_rwp', 'evaluator_version', 'evaluation_wall_seconds']}))
    sys.exit(2 if result['score_status'] == 'verification_error' else 0)
