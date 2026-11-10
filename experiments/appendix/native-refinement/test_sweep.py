from concurrent.futures import ThreadPoolExecutor
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import read_json, reservation_usd
from sweep import shard_tasks
from sweep_budget import Budget, completed_charge


def task(i=0):
    return {"id": str(i), "method": "crystalyze", "timeout_seconds": 3600}


def test_shards_cover_without_overlap():
    tasks = [task(i) for i in range(17)]
    a, b = [shard_tasks(tasks, i, 2) for i in range(2)]
    assert not {t['id'] for t in a} & {t['id'] for t in b}
    assert sorted(a + b, key=lambda t: int(t['id'])) == tasks
    with pytest.raises(ValueError):
        shard_tasks(tasks, 2, 2)


def test_budget_releases_only_after_result(tmp_path):
    budget = Budget(tmp_path / "ledger.json", 12)
    assert budget.reserve("a", task())
    assert not budget.reserve("b", task(1))
    budget.settle("a", task(), {"status": "completed", "remote_wall_seconds": 10, "gpu": "Tesla T4"})
    assert budget.reserve("b", task(1))
    with pytest.raises(ValueError):
        budget.reserve("b", task(1))
    assert read_json(budget.path)["accounted_usd"] < 12


def test_unknown_runtime_retains_full_hold():
    assert completed_charge(task(), {"status": "crashed"}) == reservation_usd(task())


def test_shared_budget_atomic(tmp_path):
    path = tmp_path / "ledger.json"
    def reserve(i):
        return Budget(path, 15).reserve(str(i), task(i), profile=f"account-{i % 2}")
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(reserve, range(20)))
    assert sum(results) == 3
    assert read_json(path)["accounted_usd"] <= 15


def test_cap_cannot_silently_change(tmp_path):
    path = tmp_path / "ledger.json"
    Budget(path, 20).records()
    with pytest.raises(ValueError):
        Budget(path, 30).records()
