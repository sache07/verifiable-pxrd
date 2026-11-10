"""Scheduling tests do not import or start Modal workers."""
from collections import deque
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from continue_sweep import interleave_panels, notify_systemd


def test_interleave_preserves_tasks_and_slots():
    rows = []
    for corpus, prefix in [('pxrd-100', 'pxrd100-challenge'), ('pxrd-100', 'pxrd100-poly'),
                           ('pxrd-100', 'pxrd100-rep'), ('pxrd-ood', 'pxrdood-cf-dec'),
                           ('pxrd-ood', 'pxrdood-cf-sub'), ('pxrd-ood', 'pxrdood-tn-css'),
                           ('pxrd-ood', 'pxrdood-tn-wyc')]:
        for case in range(3):
            for slot in (1, 3, 5, 7):
                case_id = f'{prefix}-{case:03d}' + ('-a' if 'poly' in prefix else '')
                task = dict(corpus=corpus, case_id=case_id, slot=slot)
                rows.append((task, f'{case_id}/{slot}'))
    result = list(interleave_panels(deque(rows)))
    assert len(result) == len(rows)
    assert {key for task, key in result} == {key for task, key in rows}
    assert all(task['slot'] == 1 for task, key in result[:21])
    assert len({task['case_id'].rsplit('-', 1)[0] for task, key in result[:7]}) == 7


def test_notification_optional(monkeypatch):
    monkeypatch.delenv('NOTIFY_SOCKET', raising=False)
    notify_systemd('WATCHDOG=1')
