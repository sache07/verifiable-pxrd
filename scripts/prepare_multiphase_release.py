#!/usr/bin/env python3
"""Import frozen multiphase evidence; never launch a model or modify a source run.

This is a maintainer's archive importer, not the reader's reproduction command.
Readers use experiments/experimental-evolution/analysis/reproduce.py and
pxrd-bench/divalent-tungstates-PG15/evaluation/replay_bundle.py.
Existing bundles are checked and skipped; they are never recursively overwritten.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import import_experimental_track as imp

ROOT = Path(__file__).resolve().parents[1]
DATASET = "divalent-tungstates-PG15"
RUNS = {
    "framework-access": "pxrd-pg15-framework-access-20261105",
    "framework-plus-v6": "pxrd-pg15-fwaccess-evolved-20261109",
    "evolved-framework-v5": "pxrd-pg15-fwaccess-v5-20261109",
}
REPLAY_KEYS = {"framework-access": "F", "framework-plus-v6": "FE", "evolved-framework-v5": "Fv5"}
FOLLOWUPS = [
    "pxrd-pg15-recovery-supplement-20261109",
    "pxrd-pg15-recovery-supplement2-20261109",
    "pxrd-pg15-recovery-supplement3-20261111",
]
LABELS = {
    "P0": "baseline",
    "v6nov": "evolved",
    "framework-access": "framework-access",
    "fwaccess-evolved": "framework-plus-v6",
    "fwaccess-v5": "evolved-framework-v5",
}
SUPPORT_DIRS = {"policies", "jobs", "scoring_v5"}
CONTROL_NAMES = {
    "settings.json",
    "input_manifest.json",
    "runner.py",
    "dispatch.py",
    "probe.py",
    "evaluate_attempt.py",
    "score_attempts.py",
    "harness",
    "protocol.json",
    "protocol.md",
    "PROTOCOL.md",
    "prelaunch.json",
    "preflight.json",
}


def read(path):
    return json.loads(Path(path).read_text())


def sanitizer(workspace):
    # Longest roots first; replace host-specific locations, not scientific IDs.
    roots = [
        (str(workspace / "verifiable-pxrd-raw"), "<RAW_ARCHIVE>"),
        (str(workspace / "pxrd-evolution"), "<EVOLUTION_SOURCE>"),
        (str(workspace / "archive"), "<DEVELOPMENT_ARCHIVE>"),
        (str(ROOT), "<REPOSITORY>"),
    ]
    s = imp.Sanitizer({"path_roots": roots})
    s.rules.insert(
        0,
        (
            re.compile(r"/home/ubuntu/workspace/[^/\s\"'<>]+/attempts/[^/\s\"'<>]+/workspace"),
            "<ATTEMPT_WORKSPACE>",
        ),
    )
    s.rules.insert(0, (re.compile(r"\bip-172-(?:26|31)-\d{1,3}-\d{1,3}\b"), "<HOST>"))
    return s


def copy_tree(src, dest, s):
    for f in imp.walk_files(src):
        if f.suffix == ".lock" or f.name.startswith("auth"):
            continue
        imp.copy_sanitized(f, dest / f.relative_to(src), s)


def condition_snapshot(panel, out, s):
    for name in SUPPORT_DIRS:
        if (panel / name).is_dir():
            copy_tree(panel / name, out / name, s)
    for name in CONTROL_NAMES:
        src = panel / "control" / name
        if src.is_dir():
            copy_tree(src, out / "control" / name, s)
        elif src.is_file():
            imp.copy_sanitized(src, out / "control" / name, s)
    for name in ["CONDITIONS.md", "analysis/status.json"]:
        if (panel / name).is_file():
            imp.copy_sanitized(panel / name, out / name, s)


def export_attempt(src, out, row, evaluation, s, *, condition, notes=None):
    marker = out / "attempt.json"
    if marker.exists():
        existing = read(marker)
        prior_status = existing.get("evidence_status")
        if prior_status:
            if prior_status == "assessment_only_source_attempt_unavailable" and src.is_dir():
                raise RuntimeError(
                    f"Previously missing source is now available: {src}. "
                    "Import it into a new recovery bundle; do not relabel an assessment-only export."
                )
            # Availability describes the public bundle, not whether the private
            # archive is still mounted when a later import is requested.
            return existing
        status = (
            "submission_and_trace_available"
            if src.is_dir()
            else "assessment_only_source_attempt_unavailable"
        )
        if existing.get("evidence_status") != status:
            existing["evidence_status"] = status
            if not src.is_dir():
                existing.setdefault("normalization_notes", []).append(
                    "Verified assessment and replay outputs survive; original workspace and trace archive are unavailable locally."
                )
            imp.write_json(marker, existing)
        return existing
    out.mkdir(parents=True, exist_ok=True)
    sources = {}
    for name in ["job.json", "prompt.txt", "dispatch_error.json"]:
        f = src / name
        if f.is_file():
            imp.copy_sanitized(f, out / name, s)
            sources[name] = imp.sha256(f)
    # Keep chronological events, launch records and resumed segments. HTTP proxy
    # logs are transport diagnostics and may contain authentication headers.
    for f in imp.walk_files(src / "run"):
        if "proxy" in f.name or f.name.startswith("auth"):
            continue
        rel = f.relative_to(src)
        imp.copy_sanitized(f, out / rel, s, compress=f.suffix == ".jsonl")
        sources[str(rel)] = imp.sha256(f)
    sessions = imp.find_rollouts(src / "codex-home")
    sessions += sorted((src / "claude-home").glob("projects/**/*.jsonl"))
    for i, f in enumerate(sessions, 1):
        rel = f"agent-session/rollout-{i}.jsonl"
        imp.copy_sanitized(f, out / rel, s, compress=True)
        sources[rel] = imp.sha256(f)
    work = src / "workspace"
    deliverables = {"result.json", "report.md", "fit.csv", "final.gpx", "final.lst"}
    deliverables |= {p.name for p in work.glob("*.cif")}
    ws = imp.export_solver_workspace(
        work, out / "workspace", s, deliverables, exclude_dirs={"inputs", "learned", "resources"}
    )
    # Inputs are deduplicated only after byte checks against the public panel.
    checks = {}
    case = row.get("case") or read(src / "job.json")["case_id"]
    for f in imp.walk_files(work / "inputs"):
        ref = ROOT / "pxrd-bench" / DATASET / "cases" / case / f.name
        if not ref.is_file() or imp.sha256(ref) != imp.sha256(f):
            raise ValueError(f"Input differs from released benchmark: {src.name}/{f.name}")
        checks[f"inputs/{f.name}"] = imp.sha256(f)
    # Never silently discard a learned helper or framework snapshot. Its hash
    # must occur in the immutable package included with this condition.
    package_roots = [src.parents[1] / "policies"]
    known = set()
    for p in package_roots:
        for f in imp.walk_files(p):
            known.add(imp.sha256(f))
    for f in imp.walk_files(work / "learned"):
        digest = imp.sha256(f)
        if digest not in known:
            # Solver-created files belong to the trace, not the frozen package.
            imp.copy_sanitized(
                f, out / "workspace/learned-changes" / f.relative_to(work / "learned"), s
            )
        checks["learned/" + str(f.relative_to(work / "learned"))] = digest
    # resources may contain solver-created evidence. Preserve it, excluding
    # caches/credentials, rather than assuming it is a library duplicate.
    if (work / "resources").is_dir():
        copy_tree(work / "resources", out / "workspace/resources", s)
    for name in deliverables:
        if (work / name).is_file():
            sources["workspace/" + name] = imp.sha256(work / name)
    if evaluation and evaluation.is_dir():
        copy_tree(evaluation, out / "evaluation", s)
    launch = read(src / "run/launch.json") if (src / "run/launch.json").is_file() else {}
    public = s.metadata(row)
    public.update(
        condition=condition,
        bundle_path=str(out.relative_to(ROOT)),
        source_attempt_id=src.name,
        case=case,
        normalization_notes=notes or [],
        source_artifacts_sha256=sources,
        workspace_copy_sha256=checks,
        workspace_export=ws,
        model=launch.get("model"),
        reasoning_effort=launch.get("effort"),
        native_session_segments=len(sessions),
    )
    if not src.is_dir():
        public["evidence_status"] = "assessment_only_source_attempt_unavailable"
        public["normalization_notes"].append(
            "Verified assessment and replay outputs survive; original workspace and trace archive are unavailable locally. This is not a newly executed or reconstructed solve."
        )
    else:
        public["evidence_status"] = "submission_and_trace_available"
    # Runtime in historical Opus summaries includes all resumed segments;
    # the last launch.json alone is not the total runtime.
    imp.write_json(marker, public)
    return public


def export_selection(out, records, s, label):
    # Existing per-attempt markers avoid re-exporting immutable payloads while
    # allowing the derived index to be rebuilt after a metadata correction.
    rows = []
    seen = set()
    for src, evaluation, row, notes in records:
        key = f"{row['case']}-r{row['replicate']}"
        if key in seen:
            raise ValueError(f"Duplicate attempt slot in {label}: {key}")
        seen.add(key)
        public = export_attempt(
            src, out / "attempts" / key, row, evaluation, s, condition=label, notes=notes
        )
        rows.append(public)
        print(f"{label} {len(rows)}/{len(records)} {key}", flush=True)
    imp.write_json(out / "per_attempt.json", rows)


def panels(args, s):
    raw = args.workspace / "verifiable-pxrd-raw/results/experimental-eval" / DATASET
    dest = ROOT / "results/experimental-eval" / DATASET
    for label, name in RUNS.items():
        panel = raw / name
        latest = dest / "replay-validation-20261111" / REPLAY_KEYS[label]
        records = [
            (panel / "attempts" / r["id"], latest / "attempts" / r["id"], r, [])
            for r in read(latest / "per_attempt.json")
        ]
        assert len(records) == 45
        condition_snapshot(panel, dest / label / "condition", s)
        export_selection(dest / label, records, s, label)
        # Preserve excluded transports as a separate lifecycle ledger. Any
        # segment with substantive model work keeps its event stream as well.
        selected = {src.name for src, *_ in records}
        lifecycle = []
        for attempt in sorted((panel / "attempts").iterdir()):
            if attempt.name in selected:
                continue
            launch = attempt / "run/launch.json"
            rec = read(launch) if launch.exists() else {"status": "no_launch_record"}
            event = attempt / "run/codex-events.jsonl"
            rec.update(source_attempt_id=attempt.name, included_in_main_results=False)
            if event.exists():
                imp.copy_sanitized(
                    event,
                    dest / label / "excluded-attempts" / attempt.name / "codex-events.jsonl",
                    s,
                    compress=True,
                )
            lifecycle.append(s.metadata(rec))
        imp.write_json(dest / label / "excluded-attempts.json", lifecycle)


def followups(args, s):
    raw = args.workspace / "verifiable-pxrd-raw/results/experimental-eval" / DATASET
    dest = ROOT / "results/experimental-eval" / DATASET / "followups"
    groups = defaultdict(list)
    for name in FOLLOWUPS:
        panel = raw / name
        for row in read(panel / "analysis/per_attempt.json"):
            label = LABELS[row["condition"]]
            groups[label].append(
                (
                    panel / "attempts" / row["id"],
                    panel / "analysis/attempts" / row["id"],
                    row,
                    [
                        "Outcome-selected follow-up; excluded from initial 15-measurement aggregates."
                    ],
                )
            )
        condition_snapshot(panel, dest / "contracts" / name, s)
    assert sum(map(len, groups.values())) == 61
    for label, records in groups.items():
        export_selection(dest / label, records, s, label)


def model_comparisons(args, s):
    raw = args.workspace / "verifiable-pxrd-raw/results/experimental-eval" / DATASET
    dest = ROOT / "results/experimental-eval" / DATASET
    opus = raw / "pxrd-opus-p0-eval15-20261019"
    high = raw / "pxrd-matched-p0-eval15-20261007"
    master = read(opus / "checks/eval15_all/master.json")
    rows = []
    for f in sorted(
        (opus / "secondary_gridtol/analysis/attempts").glob("OPUS5-P0-exp-*/result.json")
    ):
        r = read(f)
        m = next(x for x in master if x["condition"] == "Opus 5" and x["case"] == r["case"])
        r.update(
            minutes=m["minutes"],
            segments=m["segments"],
            tokens=m.get("tokens"),
            replay_grid_tolerance_degrees=1e-6,
        )
        assert abs(r["replay_interior_rwp"] - m["rwp"]) < 1e-9
        rows.append(
            (
                opus / "attempts" / r["id"],
                f.parent,
                r,
                [
                    "Claude Code; all resumed segments retained; declared 1e-6 degree replay grid tolerance."
                ],
            )
        )
    assert len(rows) == 15
    condition_snapshot(opus, dest / "baseline-opus" / "condition", s)
    export_selection(dest / "baseline-opus", rows, s, "baseline-opus")
    rows = []
    for j in read(high / "analysis/status.json")["jobs"]:
        ident = j["id"]
        src = high / "attempts" / ident
        f = opus / "analysis/attempts" / ident / "result.json"
        if not f.exists():
            matches = list((opus / "checks").glob(f"**/{ident}/result.json"))
            if len(matches) != 1:
                raise FileNotFoundError(f"Cannot uniquely locate high-effort assessment: {ident}")
            f = matches[0]
        notes = []
        if ident == "P0-exp-case-015-r3":
            cancelled = f
            f = opus / "analysis/attempts/P0-exp-case-015-r3-replacement/result.json"
            src = (
                args.workspace
                / "archive/records/pxrd-autonomous-v8-eval15-20261008/attempts/P0-exp-case-015-r3-replacement"
            )
            notes = [
                "Replaces user-cancelled case-015 r3; original cancellation retained separately."
            ]
            export_attempt(
                high / "attempts" / ident,
                dest / "baseline-sol-high/excluded-attempts" / ident,
                read(cancelled),
                cancelled.parent,
                s,
                condition="baseline-sol-high",
                notes=["Cancelled; excluded from published score table."],
            )
        r = read(f)
        r["replacement_for_cancelled"] = bool(notes)
        rows.append((src, f.parent, r, notes))
    assert len(rows) == 45
    condition_snapshot(high, dest / "baseline-sol-high/condition", s)
    export_selection(dest / "baseline-sol-high", rows, s, "baseline-sol-high")


def evolutions(args, s):
    runs = args.workspace / "pxrd-evolution/runs"
    session_roots = [Path.home() / ".codex/sessions", Path.home() / ".codex/archived_sessions"]
    for name in ["divalent-tungstates-fw", "divalent-tungstates-access"]:
        out = ROOT / "results/experimental-evolution" / name
        if (out / "EXPORT.json").exists():
            print(f"Already imported: {name}", flush=True)
            continue
        sessions = []
        for root in session_roots:
            for f in root.glob("**/rollout-*.jsonl"):
                with f.open() as handle:
                    first = json.loads(handle.readline())
                if first.get("payload", {}).get("cwd", "").endswith(f"/{name}/evolve"):
                    sessions.append(f)
        if len(sessions) != 1:
            raise ValueError(f"Expected one evolver session for {name}, found {len(sessions)}")
        print(f"Exporting evolution: {name}", flush=True)
        imp.cmd_evolution(
            SimpleNamespace(
                run=str(runs / name), out=str(out), researcher_session=str(sessions[0]), resume=True
            ),
            s,
        )
        config = runs / name / "evolve/.codex/config.toml"
        if config.exists():
            imp.copy_sanitized(config, out / "evolve/agent-config.toml", s)
        print(f"Completed evolution: {name}", flush=True)


def development(args, s):
    raw = args.workspace / "verifiable-pxrd-raw/results/experimental-eval" / DATASET
    dest = ROOT / "results/experimental-eval" / DATASET / "development"
    for name, short in [
        ("pxrd-pg15-fwaccess-docs-20261109", "framework-documents-only"),
        ("pxrd-eval15-v6v8-20261025", "october-v6-v8"),
    ]:
        panel = raw / name
        condition_snapshot(panel, dest / short / "condition", s)
        records = []
        # Historical development runs can have duplicate case/replicate slots
        # across policies. Preserve native attempt identifiers here.
        for f in sorted((panel / "analysis/attempts").glob("*/result.json")):
            r = read(f)
            src = panel / "attempts" / r["id"]
            if not src.is_dir():
                # Some comparison reports embed results from a different run.
                continue
            records.append(
                export_attempt(
                    src,
                    dest / short / "attempts" / r["id"],
                    r,
                    f.parent,
                    s,
                    condition=short,
                    notes=["Development record; not included in main comparisons."],
                )
            )
        imp.write_json(dest / short / "per_attempt.json", records)
        # The docs-only status snapshot is stale. Record available submissions
        # without inventing outcomes for unassessed attempts.
        selected = {r["source_attempt_id"] for r in records}
        unassessed = []
        for src in sorted((panel / "attempts").iterdir()):
            if src.name in selected:
                continue
            jobfile = src / "job.json"
            if not jobfile.exists():
                continue
            j = read(jobfile)
            r = dict(
                id=src.name,
                case=j["case_id"],
                replicate=j["replicate"],
                execution_status="not_assessed_in_saved_snapshot",
                phases=[],
            )
            unassessed.append(
                export_attempt(
                    src,
                    dest / short / "unassessed" / src.name,
                    r,
                    None,
                    s,
                    condition=short,
                    notes=["No finalized assessment in saved snapshot; no numerical claim."],
                )
            )
        imp.write_json(dest / short / "unassessed.json", unassessed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument(
        "--part",
        choices=["panels", "followups", "models", "evolutions", "development"],
        required=True,
    )
    args = parser.parse_args()
    args.workspace = args.workspace.resolve()
    funcs = dict(
        panels=panels,
        followups=followups,
        models=model_comparisons,
        evolutions=evolutions,
        development=development,
    )
    funcs[args.part](args, sanitizer(args.workspace))


if __name__ == "__main__":
    main()
