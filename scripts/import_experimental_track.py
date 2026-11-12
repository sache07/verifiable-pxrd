#!/usr/bin/env python3
"""Normalize agent panels on measured data and an evolution run into public bundles.

The importer is generic: source locations and identifier rewrites come from a private
JSON config, so source-only names never enter the repository. Run it with an interpreter
that has numpy (GSAS-II project files are pickles of numpy-bearing trees).

Subcommands:
  benchmark   measured scans, deposited references, hidden-phase targets and evaluator
  panel       one agent panel on those scans (for example baseline or evolved)
  evolution   the complete record of one evolution run plus its researcher session

Every text artifact passes through the same sanitizer: absolute paths become the
placeholders already used by the other result bundles (<ATTEMPT_WORKSPACE>, <HOME>, ...),
host names are removed, and the config's identifier rules are applied. Codex traces drop
session/thread ids and opaque encrypted reasoning blobs. GSAS-II projects are rewritten
by unpickling, mapping strings and re-pickling; the numerical tree is verified unchanged.
Intermediate GSAS-II projects (every *.gpx except final.gpx, and all *.bakN.gpx) are left
out; the scripts and logs that produced them are kept.
"""

from __future__ import annotations

import argparse
import ast
import csv
import gzip
import hashlib
import io
import json
import os
import pickle
import re
import sys
import tarfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

TEXT_SUFFIXES = {
    ".cif",
    ".csv",
    ".cfg",
    ".err",
    ".ini",
    ".instprm",
    ".json",
    ".jsonl",
    ".log",
    ".lst",
    ".md",
    ".out",
    ".prm",
    ".py",
    ".sh",
    ".stderr",
    ".stdout",
    ".toml",
    ".tsv",
    ".txt",
    ".xy",
    ".xye",
    ".yaml",
    ".yml",
    ".dat",
    ".exp",
    ".pdf_txt",
    ".service",
    ".timer",
}
TRACE_DROP_KEYS = {"thread_id", "session_id", "conversation_id"}
PRIVATE_DIRS = {
    ".git",
    ".aws",
    ".ssh",
    ".codex",
    ".claude",
    ".cache",
    ".tmp",
    ".monitor",
    "auth",
    "probe_home",
    ".venv",
    "__pycache__",
}
SECRET_PATTERNS = [
    (re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}"), "<REDACTED_API_KEY>"),
    (re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"), "<REDACTED_ACCESS_KEY>"),
    (re.compile(r"(?i)(Bearer\s+)[A-Za-z0-9_.~-]{24,}"), r"\1<REDACTED_TOKEN>"),
    (
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})"),
        "<REDACTED_GITHUB_TOKEN>",
    ),
    (re.compile(r"\bya29\.[A-Za-z0-9_-]{30,}"), "<REDACTED_OAUTH_TOKEN>"),
    (
        re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"),
        "<REDACTED_JWT>",
    ),
]
METADATA_DROP_KEYS = {
    "auth",
    "host",
    "panel",
    "session_id",
    "systemd_result",
    "systemd_run_pid",
    "systemd_unit",
    "thread_id",
    "worker_id",
}
INTERMEDIATE_GPX = re.compile(r"\.bak\d+\.gpx$|\.gpx$")


# ----------------------------------------------------------------------------- sanitizer
class Sanitizer:
    def __init__(self, config: dict[str, Any]):
        home = str(Path.home())
        rules: list[tuple[re.Pattern[str], str]] = []
        seg = r"[^/\s\"'<>\\]+"
        for root, label in config.get("attempt_roots", []):
            base = re.escape(root.rstrip("/")) + r"/attempts/" + seg
            for sub, placeholder in (
                ("workspace", "<ATTEMPT_WORKSPACE>"),
                ("codex-home", "<AGENT_HOME>"),
                ("run", "<ATTEMPT_RUN>"),
            ):
                rules.append((re.compile(base + "/" + sub), placeholder))
            rules.append((re.compile(base + r"(?=[/\s\"'<>\\]|$)"), "<ATTEMPT>"))
            rules.append((re.compile(re.escape(root.rstrip("/"))), label))
        for root, label in config.get("path_roots", []):
            rules.append((re.compile(re.escape(root.rstrip("/"))), label))
        rules += [
            (re.compile(re.escape(f"{home}/workspace/")), "<WORKSPACE>/"),
            (re.compile(re.escape(f"{home}/")), "<HOME>/"),
            (re.compile(re.escape(home) + r"(?![A-Za-z0-9_.-])"), "<HOME>"),
            (re.compile(r"\bip-172-31-\d{1,3}-\d{1,3}\b"), "<HOST>"),
            (re.compile(r"\b172\.31\.\d{1,3}\.\d{1,3}\b"), "<HOST_IP>"),
        ]
        for pattern, replacement in config.get("token_rules", []):
            rules.append((re.compile(pattern), replacement))
        rules += [
            (re.compile(r"<WORKSPACE>/[^\s\"'<>),\]\\]+"), "<SOURCE_ARTIFACT>"),
            (re.compile(re.escape(home)), "<HOME>"),
        ]
        self.rules = rules
        self.drop_keys = set(config.get("drop_keys", [])) | METADATA_DROP_KEYS
        self.forbidden = [re.compile(p) for p in config.get("forbidden", [])]

    def binary_needs_rewrite(self, data: bytes) -> bool:
        return b"/home/" in data or any(p.search(data.decode("latin-1")) for p in self.forbidden)

    def text(self, value: str) -> str:
        for pattern, replacement in self.rules:
            value = pattern.sub(replacement, value)
        for pattern, replacement in SECRET_PATTERNS:
            value = pattern.sub(replacement, value)
        return value

    def value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, list):
            return [self.value(item) for item in value]
        if isinstance(value, tuple):
            return tuple(self.value(item) for item in value)
        if isinstance(value, dict):
            return {
                (self.text(k) if isinstance(k, str) else k): self.value(v) for k, v in value.items()
            }
        return value

    def metadata(self, value: Any) -> Any:
        if isinstance(value, list):
            return [self.metadata(item) for item in value]
        if isinstance(value, dict):
            return {
                self.text(k): self.metadata(v) for k, v in value.items() if k not in self.drop_keys
            }
        return self.value(value)


def strip_trace(value: Any, in_session_meta: bool = False) -> Any:
    """Drop session ids and opaque encrypted reasoning from a Codex trace record."""
    if isinstance(value, list):
        return [strip_trace(item, in_session_meta) for item in value]
    if isinstance(value, dict):
        meta = in_session_meta or value.get("type") == "session_meta"
        out = {}
        for key, item in value.items():
            if key in TRACE_DROP_KEYS:
                continue
            if key == "encrypted_content" and isinstance(item, str):
                out[key] = "<OMITTED_ENCRYPTED_REASONING>"
                continue
            if meta and key == "id" and isinstance(item, str):
                continue
            out[key] = strip_trace(item, meta and key == "payload")
        return out
    return value


# ----------------------------------------------------------------------------- io helpers
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def is_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"STOP", "README", "LICENSE"}:
        return True
    try:
        head = path.read_bytes()[:8192]
    except OSError:
        return False
    return b"\x00" not in head and (
        not head or head.decode("utf-8", "ignore").isprintable() or b"\n" in head
    )


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", "surrogateescape")


def to_bytes(text: str) -> bytes:
    return text.encode("utf-8", "surrogateescape")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def gz_bytes(data: bytes) -> bytes:
    raw = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as out:
        out.write(data)
    return raw.getvalue()


def sanitize_jsonl(data: str, s: Sanitizer) -> str:
    lines = []
    for line in data.splitlines():
        if not line.strip():
            continue
        try:
            record = strip_trace(json.loads(line))
            lines.append(s.text(json.dumps(record, ensure_ascii=False, separators=(",", ":"))))
        except json.JSONDecodeError:
            lines.append(s.text(line))
    return "\n".join(lines) + "\n"


def sanitize_file_bytes(path: Path, s: Sanitizer) -> bytes:
    """Return the public bytes of one source file (text sanitized, json normalized)."""
    suffix = path.suffix.lower()
    if suffix == ".gpx":
        return rewrite_gpx_bytes(path, s)
    if not is_text(path):
        data = path.read_bytes()
        if s.binary_needs_rewrite(data):
            try:
                return rewrite_pickle_stream(data, s, path)
            except Exception:
                return None  # binary with embedded paths that cannot be rewritten
        return data
    text = read_text(path)
    if suffix == ".jsonl":
        return to_bytes(sanitize_jsonl(text, s))
    if suffix == ".json":
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            return to_bytes(s.text(text))
        return to_bytes(
            json.dumps(s.metadata(value), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        )
    return to_bytes(s.text(text))


OMITTED: list[str] = []


def put(path: Path, data: bytes | None) -> None:
    if data is None:
        OMITTED.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def copy_sanitized(source: Path, dest: Path, s: Sanitizer, compress: bool = False) -> None:
    if dest.name == ".gitignore" and "results" in dest.parts and any(
        part in {"experimental-evolution", "experimental-eval"} for part in dest.parts
    ):
        # Historical run rules must not hide the evidence in a public checkout.
        dest = dest.with_name(".gitignore.source")
    data = sanitize_file_bytes(source, s)
    if data is None:
        OMITTED.append(str(source))
        return
    if compress:
        dest = dest.with_name(dest.name + ".gz")
        data = gz_bytes(data)
    put(dest, data)


# ----------------------------------------------------------------------------- gpx rewrite
def _map_tree(value: Any, fn: Callable[[str], str]) -> Any:
    try:
        import numpy as np
    except ImportError:  # pragma: no cover - interpreter guard
        np = None
    if isinstance(value, str):
        return fn(value)
    if isinstance(value, bytes):
        return to_bytes(fn(value.decode("utf-8", "surrogateescape")))
    if isinstance(value, list):
        return [_map_tree(v, fn) for v in value]
    if isinstance(value, tuple):
        return tuple(_map_tree(v, fn) for v in value)
    if isinstance(value, dict):
        return {_map_tree(k, fn): _map_tree(v, fn) for k, v in value.items()}
    if np is not None and isinstance(value, np.ndarray) and value.dtype == object:
        out = value.copy()
        for idx, item in np.ndenumerate(value):
            out[idx] = _map_tree(item, fn)
        return out
    return value


def _load_gpx(data: bytes) -> list[Any]:
    stream = io.BytesIO(data)
    items = []
    while True:
        try:
            items.append(pickle.load(stream, encoding="latin-1"))
        except EOFError:
            return items


def _equal(a: Any, b: Any) -> bool:
    import numpy as np

    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        if not (isinstance(a, np.ndarray) and isinstance(b, np.ndarray)):
            return False
        if a.shape != b.shape or a.dtype != b.dtype:
            return False
        if a.dtype == object:
            return all(_equal(x, y) for x, y in zip(a.ravel(), b.ravel(), strict=True))
        return bool(np.array_equal(a, b, equal_nan=a.dtype.kind in "fc"))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_equal(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return (
            type(a) is type(b)
            and len(a) == len(b)
            and all(_equal(x, y) for x, y in zip(a, b, strict=True))
        )
    if isinstance(a, float) and isinstance(b, float) and a != a and b != b:
        return True
    return type(a) is type(b) and a == b


def rewrite_gpx_bytes(path: Path, s: Sanitizer) -> bytes:
    return rewrite_pickle_stream(path.read_bytes(), s, path)


def rewrite_pickle_stream(raw: bytes, s: Sanitizer, path: Path) -> bytes:
    original = _load_gpx(raw)
    if not original:
        raise ValueError(f"not a pickle stream: {path}")
    mapped = [_map_tree(item, s.text) for item in original]
    out = io.BytesIO()
    for item in mapped:
        pickle.dump(item, out, 2)
    data = out.getvalue()
    reloaded = _load_gpx(data)
    if not _equal(reloaded, mapped):
        raise RuntimeError(f"GSAS-II project changed beyond string mapping: {path}")
    return data


# ----------------------------------------------------------------------------- tar helper
def tar_tree(root: Path, files: list[Path], s: Sanitizer) -> bytes:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for path in sorted(files):
            data = sanitize_file_bytes(path, s)
            if data is None:
                OMITTED.append(str(path))
                continue
            info = tarfile.TarInfo(name=s.text(str(path.relative_to(root))))
            info.size, info.mtime, info.mode = len(data), 0, 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    return gz_bytes(raw.getvalue())


def walk_files(root: Path, skip_dirs: set[str] = frozenset()) -> list[Path]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in skip_dirs | PRIVATE_DIRS)
        for name in sorted(filenames):
            if name in {"auth.json", "credentials", ".credentials.json", ".env"} or name.endswith(
                (".pem", ".key", ".pyc")
            ):
                continue
            path = Path(dirpath) / name
            if path.is_file() and not path.is_symlink():
                out.append(path)
    return out


def tokens_from_events(path: Path) -> dict[str, int] | None:
    if not path.exists():
        return None
    total: dict[str, int] = {}
    for line in path.read_text(errors="replace").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("type") == "turn.completed":
            for key, value in (record.get("usage") or {}).items():
                if isinstance(value, int):
                    total[key] = total.get(key, 0) + value
    return total or None


# ----------------------------------------------------------------------------- workspaces
def export_solver_workspace(
    workspace: Path,
    dest: Path,
    s: Sanitizer,
    deliverable_names: set[str],
    exclude_dirs: set[str] = frozenset(),
) -> dict[str, Any]:
    """Deliverables stay plain; every other kept file goes into workspace-files.tar.gz."""
    kept, omitted_gpx, plain = [], 0, []
    for path in walk_files(workspace, set(exclude_dirs)):
        rel = path.relative_to(workspace)
        if INTERMEDIATE_GPX.search(path.name) and not (
            path.name == "final.gpx" and len(rel.parts) == 1
        ):
            omitted_gpx += 1
            continue
        if len(rel.parts) == 1 and path.name in deliverable_names:
            plain.append(path)
        else:
            kept.append(path)
    for path in plain:
        put(dest / path.name, sanitize_file_bytes(path, s))
    if kept:
        put(dest / "workspace-files.tar.gz", tar_tree(workspace, kept, s))
    return {
        "deliverables": sorted(p.name for p in plain),
        "archived_files": len(kept),
        "omitted_intermediate_gsas_projects": omitted_gpx,
        "excluded_directories": sorted(exclude_dirs),
    }


def find_rollouts(agent_home: Path) -> list[Path]:
    return sorted(agent_home.glob("sessions/*/*/*/rollout-*.jsonl")) if agent_home.exists() else []


# ----------------------------------------------------------------------------- benchmark
def cmd_benchmark(args: argparse.Namespace, s: Sanitizer) -> None:
    panel, out = Path(args.panel), Path(args.out)
    if out.exists():
        raise FileExistsError(f"Refusing to overwrite an existing benchmark: {out}")
    input_hashes = {}
    for case in sorted((panel / "cases").iterdir()):
        for f in sorted((case / "inputs").iterdir()):
            put(out / "cases" / case.name / f.name, f.read_bytes())
            input_hashes[f"{case.name}/{f.name}"] = sha256(f)
    for f in walk_files(panel / "references"):
        copy_sanitized(f, out / "references" / f.relative_to(panel / "references"), s)
    copy_sanitized(panel / "control" / "case_labels.json", out / "case-metadata.json", s)
    for f in walk_files(panel / "scoring_v5"):
        copy_sanitized(
            f, out / "evaluation" / "scoring_v5" / f.relative_to(panel / "scoring_v5"), s
        )
    copy_sanitized(
        panel / "control" / "evaluate_attempt.py", out / "evaluation" / "evaluate_attempt.py", s
    )
    assess = (panel / "control" / "assess.py").read_text()
    targets = re.search(r"^TARGETS\s*=\s*(\[.*?\])\s*$", assess, re.M)
    write_json(
        out / "hidden-phase-targets.json",
        [
            {
                "case_id": c,
                "phase": ph,
                "canonical_structure": f"references/diagnostic_structures/{ph}_canonical.cif",
            }
            for c, ph in ast.literal_eval(targets.group(1))
        ],
    )
    for item in args.provenance or []:
        dest, src = item.split("=", 1)
        copy_sanitized(Path(src), out / "provenance" / dest, s)
    write_json(out / "input-hashes.json", input_hashes)


# ----------------------------------------------------------------------------- panel
def cmd_panel(args: argparse.Namespace, s: Sanitizer) -> None:
    panel, out, label = Path(args.panel), Path(args.out), args.condition
    if out.exists():
        raise FileExistsError(f"Refusing to overwrite an existing bundle: {out}")
    rows = json.loads((panel / "analysis" / "per_attempt.json").read_text())
    package_hashes = {}
    if args.package:
        for f in walk_files(Path(args.package)):
            package_hashes[str(f.relative_to(args.package))] = sha256(f)
    benchmark_hashes = (
        json.loads(Path(args.benchmark_hashes).read_text()) if args.benchmark_hashes else {}
    )
    public_rows, summary = [], []
    for row in sorted(rows, key=lambda r: (r["case"], r["replicate"])):
        terminal = row["id"]
        history = row.get("transport_history") or [terminal]
        attempt_id = f"{label}-{row['case']}-r{row['replicate']}"
        src = panel / "attempts" / terminal
        dest = out / "attempts" / f"{row['case']}-r{row['replicate']}"
        # earlier transports must be capacity rejections with no model work
        for earlier in history[:-1]:
            ev = panel / "attempts" / earlier / "run" / "codex-events.jsonl"
            if ev.exists() and ev.stat().st_size > 4096:
                raise RuntimeError(f"earlier transport did model work: {earlier}")
        source_artifacts = {}
        for rel in ("job.json", "prompt.txt"):
            if (src / rel).exists():
                copy_sanitized(src / rel, dest / rel, s)
                source_artifacts[rel] = sha256(src / rel)
        for f in sorted((src / "run").iterdir()):
            compress = f.name == "codex-events.jsonl"
            copy_sanitized(f, dest / "run" / f.name, s, compress=compress)
            source_artifacts[f"run/{f.name}"] = sha256(f)
        rollouts = find_rollouts(src / "codex-home")
        for i, f in enumerate(rollouts):
            name = "rollout.jsonl" if len(rollouts) == 1 else f"rollout-{i + 1}.jsonl"
            copy_sanitized(f, dest / "agent-session" / name, s, compress=True)
            source_artifacts[f"agent-session/{name}"] = sha256(f)
        cif_names = {Path(p.get("cif", "")).name for p in row.get("phases", []) if p.get("cif")}
        deliverables = {"result.json", "report.md", "fit.csv", "final.gpx", "final.lst"} | cif_names
        ws_info = export_solver_workspace(
            src / "workspace",
            dest / "workspace",
            s,
            deliverables,
            exclude_dirs={"inputs", "learned"},
        )
        # inputs and the learned package are byte-identical to the released copies
        checks = {}
        for f in walk_files(src / "workspace" / "inputs"):
            key = f"{row['case']}/{f.name}"
            checks[f"inputs/{f.name}"] = (
                benchmark_hashes.get(key) == sha256(f) if benchmark_hashes else None
            )
        learned = src / "workspace" / "learned"
        if learned.exists():
            for f in walk_files(learned):
                rel = str(f.relative_to(learned))
                checks[f"learned/{rel}"] = any(h == sha256(f) for h in package_hashes.values())
        if not all(v for v in checks.values() if v is not None):
            raise RuntimeError(
                f"workspace copy differs from released inputs/package: {terminal} {checks}"
            )
        ev_dir = panel / "analysis" / "attempts" / terminal
        if ev_dir.exists():
            for f in walk_files(ev_dir):
                copy_sanitized(f, dest / "evaluation" / f.relative_to(ev_dir), s)
        public_row = s.metadata(
            {
                k: v
                for k, v in row.items()
                if k not in {"transport_history", "source_hashes", "slot_status"}
            }
        )
        public_row["id"] = public_row["logical_id"] = attempt_id
        public_row["condition"] = label
        public_row["infrastructure_retries"] = len(history) - 1
        launch = json.loads((src / "run" / "launch.json").read_text())
        tokens = tokens_from_events(src / "run" / "codex-events.jsonl")
        attempt = {
            "attempt_id": attempt_id,
            "condition": label,
            "case_id": row["case"],
            "replicate": row["replicate"],
            "model": launch.get("model"),
            "reasoning_effort": launch.get("effort"),
            "started_at": launch.get("started_at"),
            "ended_at": launch.get("ended_at"),
            "elapsed_seconds": launch.get("elapsed_seconds"),
            "returncode": launch.get("returncode"),
            "timed_out": launch.get("timed_out"),
            "prompt_sha256": launch.get("prompt_sha256"),
            "tokens": tokens,
            "infrastructure_retries": len(history) - 1,
            "infrastructure_retries_note": "capacity rejections before any model work; only the working session is included",
            "execution_status": row.get("execution_status"),
            "replay_interior_rwp_percent": row.get("replay_interior_rwp"),
            "deposited_reference_interior_rwp_percent": row.get("ceder_interior_rwp"),
            "phases": [
                {
                    "formula": p.get("formula"),
                    "weight_fraction": p.get("weight_fraction", p.get("wt")),
                    "physical_screen": (p.get("physical_screen") or {}).get("status"),
                    "cif": Path(p.get("cif", "")).name or None,
                }
                for p in row.get("phases", [])
            ],
            "workspace": ws_info,
            "workspace_copy_checks": checks,
            "source_artifacts_sha256": source_artifacts,
        }
        write_json(dest / "attempt.json", s.metadata(attempt))
        public_rows.append(public_row)
        summary.append(
            {
                "attempt_id": attempt_id,
                "case_id": row["case"],
                "replicate": row["replicate"],
                "execution_status": row.get("execution_status"),
                "replay_interior_rwp_percent": row.get("replay_interior_rwp"),
                "deposited_reference_interior_rwp_percent": row.get("ceder_interior_rwp"),
                "minutes": row.get("minutes"),
                "infrastructure_retries": len(history) - 1,
                "phases": ";".join(f"{p.get('formula')}" for p in row.get("phases", [])),
            }
        )
    write_json(out / "per_attempt.json", public_rows)
    with (out / "per_attempt.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    cond = out / "condition"
    for rel in args.condition_files or []:
        src = panel / rel
        if src.is_dir():
            for f in walk_files(src):
                copy_sanitized(f, cond / s.text(str(f.relative_to(panel))), s)
        elif src.exists():
            copy_sanitized(src, cond / s.text(rel), s)


# ----------------------------------------------------------------------------- evolution
EVOLUTION_SKIP_DIRS = {"monitor", "forward_cache", "staging", "reservations", ".pytest_cache"}


def cmd_evolution(args: argparse.Namespace, s: Sanitizer) -> None:
    run, out = Path(args.run), Path(args.out)
    if out.exists() and not getattr(args, "resume", False):
        raise FileExistsError(f"Refusing to overwrite an existing bundle: {out}")
    stats = {"files": 0, "omitted_intermediate_gsas_projects": 0, "attempts": 0}
    attempts_root = run / "evidence" / "attempts"
    for path in walk_files(run, EVOLUTION_SKIP_DIRS):
        rel = path.relative_to(run)
        parts = rel.parts
        if parts[0] == "control" and len(parts) > 1 and parts[1] in EVOLUTION_SKIP_DIRS:
            continue
        if path.suffix == ".lock" or "auth" in parts or path.name.startswith("auth"):
            continue
        if parts[:2] == ("evidence", "attempts"):
            continue  # handled below
        if INTERMEDIATE_GPX.search(path.name) and path.name != "final.gpx":
            stats["omitted_intermediate_gsas_projects"] += 1
            continue
        copy_sanitized(
            path,
            out / s.text(str(rel)),
            s,
            compress=path.suffix == ".jsonl" and path.stat().st_size > 1_000_000,
        )
        stats["files"] += 1
    for attempt in sorted(p for p in attempts_root.iterdir() if p.is_dir()):
        dest = out / "evidence" / "attempts" / attempt.name
        stats["attempts"] += 1
        for path in walk_files(attempt, {"workspace"}):
            rel = path.relative_to(attempt)
            copy_sanitized(path, dest / rel, s, compress=path.name == "codex-events.jsonl")
        ws = attempt / "workspace"
        if ws.exists():
            cifs = {p.name for p in ws.glob("*.cif")}
            info = export_solver_workspace(
                ws,
                dest / "workspace",
                s,
                {"result.json", "report.md", "fit.csv", "final.gpx", "final.lst"} | cifs,
                exclude_dirs={"inputs", "learned"},
            )
            stats["omitted_intermediate_gsas_projects"] += info[
                "omitted_intermediate_gsas_projects"
            ]
            write_json(dest / "workspace" / "EXPORT.json", info)
    if args.researcher_session:
        f = Path(args.researcher_session)
        copy_sanitized(f, out / "researcher" / "session.jsonl", s, compress=True)
        stats["researcher_session_sha256"] = sha256(f)
    write_json(out / "EXPORT.json", stats)


# ----------------------------------------------------------------------------- tree
def cmd_tree(args: argparse.Namespace, s: Sanitizer) -> None:
    """Copy source trees (framework snapshot, packages) with the same sanitizer."""
    out = Path(args.out)
    for item in args.items:
        dest, src = item.split("=", 1)
        src_path = Path(src)
        files = [src_path] if src_path.is_file() else walk_files(src_path, {".pytest_cache"})
        for f in files:
            if INTERMEDIATE_GPX.search(f.name) or f.suffix in {".pyc", ".lock"}:
                continue
            rel = Path(dest) if src_path.is_file() else Path(dest) / f.relative_to(src_path)
            copy_sanitized(f, out / s.text(str(rel)), s)


# ----------------------------------------------------------------------------- check
def cmd_check(args: argparse.Namespace, s: Sanitizer) -> None:
    """Scan a bundle (including gzip and tar members) for forbidden strings."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    patterns = s.forbidden + [re.compile(p) for p in args.pattern or []]
    hits: dict[str, int] = {}

    def scan(name: str, data: bytes) -> None:
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
            if name.endswith(".tar.gz"):
                with tarfile.open(fileobj=io.BytesIO(data)) as tar:
                    for member in tar.getmembers():
                        if member.isfile():
                            scan(f"{name}!{member.name}", tar.extractfile(member).read())
                return
        text = data.decode("utf-8", "ignore")
        for p in patterns:
            n = len(p.findall(text))
            if n:
                hits[f"{name} :: {p.pattern}"] = hits.get(f"{name} :: {p.pattern}", 0) + n

    for root in args.roots:
        for path in walk_files(Path(root)):
            scan(str(path), path.read_bytes())
    print(json.dumps({"hits": len(hits)}, indent=None))
    for key, n in sorted(hits.items())[: args.limit]:
        print(n, key)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--config", required=True, help="private JSON config with path roots and identifier rules"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("benchmark")
    b.add_argument("--panel", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--provenance", nargs="*", help="DEST=SRC files copied under provenance/")
    p = sub.add_parser("panel")
    p.add_argument("--panel", required=True)
    p.add_argument("--condition", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--package")
    p.add_argument("--benchmark-hashes")
    p.add_argument("--condition-files", nargs="*")
    e = sub.add_parser("evolution")
    e.add_argument("--run", required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--researcher-session")
    tr = sub.add_parser("tree")
    tr.add_argument("--out", required=True)
    tr.add_argument("items", nargs="+", help="DEST=SRC")
    c = sub.add_parser("check")
    c.add_argument("roots", nargs="+")
    c.add_argument("--pattern", action="append")
    c.add_argument("--limit", type=int, default=60)
    args = parser.parse_args()
    sanitizer = Sanitizer(json.loads(Path(args.config).read_text()))
    {
        "benchmark": cmd_benchmark,
        "panel": cmd_panel,
        "evolution": cmd_evolution,
        "tree": cmd_tree,
        "check": cmd_check,
    }[args.command](args, sanitizer)
    if OMITTED:
        print(json.dumps({"omitted_binary_files_with_paths": len(OMITTED)}))
        out = getattr(args, "out", None)
        if out:
            write_json(
                Path(out) / "OMITTED-BINARIES.json", sorted(sanitizer.text(o) for o in OMITTED)
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
