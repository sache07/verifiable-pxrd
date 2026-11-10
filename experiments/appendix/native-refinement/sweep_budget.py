"""Process-safe shared resource budget for a multi-workspace sweep.

This is an intentionally conservative resource estimate, not a Modal invoice.
Unfinished/unknown calls keep their full timeout reservation. Completed calls
release the unused reservation, retaining runtime + 20 s and a 25% margin.
"""
from contextlib import contextmanager
import fcntl
from pathlib import Path
import time

from common import read_json, reservation_usd, write_json


def completed_charge(task, result):
    seconds = result.get("remote_wall_seconds")
    if seconds is None or seconds < 0:
        return reservation_usd(task)
    rate = 2 * .0000131 + 8 * .00000222
    if task["method"] == "crystalyze":
        rate += .000164 if "T4" in result.get("gpu", "") else .000222
    return (seconds + 20) * rate * 1.25


class Budget:
    def __init__(self, path, cap):
        self.path, self.cap = Path(path), cap
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def transaction(self):
        with self.path.with_suffix(".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            value = read_json(self.path) if self.path.exists() else {
                "schema": 2, "cap_usd": self.cap, "overhead_allowance_usd": 10., "calls": {}}
            if value.get("schema") != 2 or value["cap_usd"] != self.cap:
                raise ValueError("Budget schema/cap differs; do not silently replace an existing ledger")
            yield value
            value["accounted_usd"] = self.total(value)
            value["updated_unix"] = time.time()
            write_json(self.path, value)

    @staticmethod
    def total(value):
        return value["overhead_allowance_usd"] + sum(
            r.get("charged_estimate_usd", r["reservation_usd"]) for r in value["calls"].values())

    def records(self):
        with self.transaction() as value:
            return dict(value["calls"])

    def reserve(self, key, task, **metadata):
        with self.transaction() as value:
            if key in value["calls"]:
                raise ValueError("Task already reserved; reconnect to its recorded call instead")
            amount = reservation_usd(task)
            if self.total(value) + amount > self.cap:
                return False
            value["calls"][key] = dict(metadata, id=task["id"], reservation_usd=amount,
                                      state="reserved", reserved_unix=time.time())
            return True

    def update(self, key, **fields):
        with self.transaction() as value:
            value["calls"][key].update(fields)

    def settle(self, key, task, result):
        self.update(key, state="collected", charged_estimate_usd=completed_charge(task, result),
                    result_status=result["status"], settled_unix=time.time())
