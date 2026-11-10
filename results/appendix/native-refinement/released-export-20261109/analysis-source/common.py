"""Small, dependency-light provenance helpers shared by the experiment commands."""
from __future__ import annotations

import hashlib
import json
import signal
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PROTOCOL = json.loads((HERE / "protocol.json").read_text())


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
    temporary.replace(path)


def fingerprint(value):
    return digest(json.dumps(value, sort_keys=True, allow_nan=False).encode())


def code_hash():
    return fingerprint({p.name: digest(p.read_bytes()) for p in sorted(HERE.glob("*.py"))})


def verify_task(task):
    allowed = {"id", "method", "corpus", "case_id", "slot", "candidate_cif", "candidate_sha256",
               "pattern_text", "pattern_sha256", "intensity_multiplier", "timeout_seconds",
               "wavelength", "protocol_sha256", "self_target", "diagnostic_iterations"}
    if set(task) - allowed:
        raise ValueError(f"Unexpected worker fields: {set(task) - allowed}")
    for name in ("candidate", "pattern"):
        text = task["candidate_cif" if name == "candidate" else "pattern_text"]
        if digest(text.encode()) != task[name + "_sha256"]:
            raise ValueError(f"{name} hash mismatch")
    if task["protocol_sha256"] != fingerprint(PROTOCOL):
        raise ValueError("Task and worker protocols differ")
    if task["method"] not in PROTOCOL["methods"]:
        raise ValueError("Unknown method")
    if Path(task["id"]).is_absolute() or ".." in Path(task["id"]).parts:
        raise ValueError("Unsafe candidate identifier")


@contextmanager
def time_limit(seconds):
    def expired(*_):
        raise TimeoutError(f"Native refinement exceeded {seconds} seconds")
    previous = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def reservation_usd(task):
    """Conservative per-call resource reservation, NOT a claim of an exact invoice."""
    # Nov 2026 Modal rates: L4, 2 physical CPU cores, and 8 GiB. Reserve an
    # additional 300 seconds for startup/export, plus 25% margin.
    rate = 2 * 0.0000131 + 8 * 0.00000222
    if task["method"] == "crystalyze":
        rate += 0.000222
    return (task["timeout_seconds"] + 300) * rate * 1.25
