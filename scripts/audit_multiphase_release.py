"""Check multiphase bundle completeness, provenance and release hygiene.

Read-only by default. --manifest writes an inventory of the released files;
--scan checks plaintext and compressed contents for common credential patterns.
This scanner is a safeguard, not a guarantee that arbitrary text is non-sensitive.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import tarfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = [
    "experiments/experimental-evolution",
    "results/experimental-evolution",
    "results/experimental-eval",
    "pxrd-bench/divalent-tungstates-PG15",
]
EXTRA_FILES = [
    "docs/MULTIPHASE.md",
    "scripts/import_experimental_track.py",
    "scripts/prepare_multiphase_release.py",
    "scripts/summarize_experimental_eval.py",
    "scripts/audit_multiphase_release.py",
    "tests/test_multiphase_release.py",
]
PATTERNS = {
    "api_key": re.compile(rb"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}"),
    "aws_access_key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "bearer_token": re.compile(rb"(?i)Bearer\s+[A-Za-z0-9_.~-]{24,}"),
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})"),
    "google_oauth": re.compile(rb"\bya29\.[A-Za-z0-9_-]{30,}"),
    "jwt": re.compile(rb"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"),
}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check_stream(stream, name, hits):
    tail = b""
    while block := stream.read(1 << 20):
        data = tail + block
        for label, pattern in PATTERNS.items():
            if pattern.search(data):
                hits.add((name, label))
        tail = data[-256:]


def scan(path, hits):
    if path.name.endswith(".tar.gz"):
        with tarfile.open(path, "r|gz") as tar:
            for member in tar:
                if member.isfile():
                    with tar.extractfile(member) as handle:
                        check_stream(handle, str(path.relative_to(ROOT)) + "!" + member.name, hits)
    else:
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rb") as handle:
            check_stream(handle, str(path.relative_to(ROOT)), hits)


def scan_one(path):
    hits = set()
    scan(path, hits)
    return sorted(hits)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path)
    p.add_argument("--report", type=Path)
    p.add_argument("--scan", action="store_true")
    p.add_argument("--workers", type=int, default=4, help="Parallel credential-scan processes")
    a = p.parse_args()
    errors = []
    limitations = []
    counts = {}
    hits = set()
    base = ROOT / "results/experimental-eval/divalent-tungstates-PG15"
    names = [
        "baseline",
        "evolved",
        "framework-access",
        "framework-plus-v6",
        "evolved-framework-v5",
        "baseline-sol-high",
        "baseline-opus",
    ]
    for name in names:
        path = base / name / "per_attempt.json"
        rows = json.loads(path.read_text())
        expected = 15 if name == "baseline-opus" else 45
        counts[name] = len(rows)
        if len(rows) != expected:
            errors.append(f"{name}: {len(rows)} rows, expected {expected}")
        keys = {(r["case"], r["replicate"]) for r in rows}
        if len(keys) != len(rows):
            errors.append(f"{name}: duplicate slots")
        for row in rows:
            attempt = path.parent / "attempts" / f"{row['case']}-r{row['replicate']}"
            detail = json.loads((attempt / "attempt.json").read_text())
            if detail.get("evidence_status") == "assessment_only_source_attempt_unavailable":
                limitations.append(str(attempt.relative_to(ROOT)))
                continue
            for suffix in ["workspace/final.gpx", "workspace/result.json", "workspace/fit.csv"]:
                if not (attempt / suffix).is_file():
                    errors.append(f"Missing {attempt.relative_to(ROOT)}/{suffix}")
            if not list((attempt / "agent-session").glob("*.jsonl.gz")):
                errors.append(f"Missing native agent session: {attempt.relative_to(ROOT)}")
            if not list((attempt / "run").glob("*events.jsonl.gz")):
                errors.append(f"Missing event stream: {attempt.relative_to(ROOT)}")
    follow = []
    for path in (base / "followups").glob("*/per_attempt.json"):
        follow += json.loads(path.read_text())
    counts["followup_records"] = len(follow)
    if len(follow) != 61:
        errors.append("Expected 61 follow-up records, including failures/replacement")
    for name, jobs, attempts in [
        ("divalent-tungstates", 135, 135),
        ("divalent-tungstates-fw", 36, 35),
        ("divalent-tungstates-access", 156, 156),
    ]:
        path = ROOT / "results/experimental-evolution" / name
        status = json.loads((path / "evidence/status.json").read_text())
        counts[name] = len(status["jobs"])
        if len(status["jobs"]) != jobs:
            errors.append(f"Wrong evolution job count: {name}")
        if len(list((path / "evidence/attempts").iterdir())) != attempts:
            errors.append(f"Wrong saved attempt count: {name}")
        if not (path / "researcher/session.jsonl.gz").exists():
            errors.append(f"Missing evolver session: {name}")
    files = []
    scan_paths = []
    release_paths = []
    skipped = {"__pycache__", ".pytest_cache", ".git", ".ruff_cache", ".cache", ".tmp", ".monitor"}
    for part in PARTS + EXTRA_FILES:
        target = ROOT / part
        for path in sorted(target.rglob("*")) if target.is_dir() else [target]:
            if not path.is_file() or any(x in skipped for x in path.parts):
                continue
            if path.suffix == ".pyc" or path == a.manifest or path == a.report:
                continue
            rel = str(path.relative_to(ROOT))
            release_paths.append(rel)
            if path.name in {"auth.json", "credentials", ".credentials.json"} or any(
                x in {".aws", ".ssh"} for x in path.parts
            ):
                errors.append(f"Credential artifact included: {rel}")
            if path.stat().st_size > 100_000_000:
                limitations.append(f"Large file (>100 MB): {rel}")
            if a.manifest:
                files.append(dict(path=rel, bytes=path.stat().st_size, sha256=digest(path)))
            if a.scan:
                scan_paths.append(path)
    git_ignore_checked = False
    if shutil.which("git") and (ROOT / ".git").exists():
        check = subprocess.run(
            ["git", "check-ignore", "--no-index", "--stdin", "-z"],
            input="\0".join(release_paths) + "\0",
            text=True,
            capture_output=True,
            cwd=ROOT,
        )
        if check.returncode not in (0, 1):
            raise RuntimeError("Could not verify Git inclusion: " + check.stderr)
        git_ignore_checked = True
        errors.extend(
            "Release evidence hidden by gitignore: " + p for p in check.stdout.split("\0") if p
        )
    if a.scan:
        with ProcessPoolExecutor(max_workers=a.workers) as pool:
            for matches in pool.map(scan_one, scan_paths, chunksize=16):
                hits.update(matches)
    report = dict(
        status="passed_with_documented_limitations" if not errors and not hits else "failed",
        counts=counts,
        limitations=limitations,
        errors=errors,
        credential_pattern_hits=[dict(path=p, kind=k) for p, k in sorted(hits)],
        credential_scan_performed=a.scan,
        git_ignore_checked=git_ignore_checked,
        files=len(files),
        bytes=sum(f["bytes"] for f in files),
    )
    if a.manifest:
        a.manifest.parent.mkdir(parents=True, exist_ok=True)
        a.manifest.write_text(json.dumps(dict(schema=1, files=files), indent=2) + "\n")
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if errors or hits:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
