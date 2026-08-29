#!/usr/bin/env python3
"""Run a pXRD panel through the Responses API with no tools.

The model receives one user message containing the task prompt and full CSV.
Inline text avoids the Responses API's 1,000-row spreadsheet preview. CIF
extraction and benchmark evaluation happen only after the response is complete.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time
import tomllib
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from verifiable_pxrd.benchmark import Problem, load_problem_collection
from verifiable_pxrd.llm_output import materialize_cifs, output_text
from verifiable_pxrd.matching import evaluate_workspace, exact_outcomes
from verifiable_pxrd.util import load_json, sha256_file, write_json

TERMINAL_STATUSES = {"completed", "failed", "cancelled", "incomplete"}
RETRYABLE_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}


def now() -> str:
    return datetime.now(UTC).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.rstrip()


def repository_provenance(repository: Path, runner_path: Path) -> dict[str, Any]:
    status = _git(repository, "status", "--porcelain", "--untracked-files=normal")
    return {
        "commit": _git(repository, "rev-parse", "HEAD"),
        "dirty": bool(status),
        "dirty_paths": [line[3:] for line in status.splitlines()],
        "runner_path": str(runner_path.relative_to(repository)),
        "runner_sha256": sha256_file(runner_path),
    }


@contextmanager
def campaign_lock(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as stream:
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError(f"another LLM-only campaign holds {lock_path}") from error
        stream.seek(0)
        stream.truncate()
        stream.write(f"pid={os.getpid()} started_at={now()}\n")
        stream.flush()
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


class OpenAIHTTP:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        delay = 1.0
        for attempt in range(7):
            response = self.session.request(
                method,
                f"{self.base_url}{path}",
                timeout=180,
                **kwargs,
            )
            if response.status_code not in RETRYABLE_STATUS_CODES:
                response.raise_for_status()
                return response.json()
            if attempt == 6:
                response.raise_for_status()
            retry_after = response.headers.get("retry-after")
            time.sleep(float(retry_after) if retry_after else delay)
            delay = min(delay * 2, 30)
        raise AssertionError("unreachable")

    def upload_pattern(self, path: Path) -> dict[str, Any]:
        with path.open("rb") as handle:
            return self.request(
                "POST",
                "/files",
                data={"purpose": "user_data"},
                files={"file": ("pattern.csv", handle, "text/csv")},
            )

    def delete_file(self, file_id: str) -> None:
        response = self.session.delete(
            f"{self.base_url}/files/{file_id}",
            timeout=180,
        )
        if response.status_code not in {200, 404}:
            response.raise_for_status()


def load_condition(path: Path, repository: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        value = tomllib.load(stream)
    if value.get("adapter") != "responses-api":
        raise ValueError("LLM-only runner requires adapter = 'responses-api'")
    if value.get("tools") != []:
        raise ValueError("LLM-only condition must explicitly set tools = []")
    prompt = Path(str(value["prompt"]))
    value["prompt_path"] = prompt if prompt.is_absolute() else repository / prompt
    return value


def prompt_for(problem: Problem, template: str) -> str:
    return template.format(
        formula=problem.formula,
        radiation=problem.radiation,
        wavelength=problem.wavelength,
    ).strip()


def response_payload(
    attempt: Path,
    prompt: str,
    condition: dict[str, Any],
    *,
    file_id: str | None = None,
) -> dict[str, Any]:
    input_transport = str(condition.get("input_transport", "inline-text"))
    content: list[dict[str, Any]] = [{"type": "input_text", "text": prompt}]
    if input_transport == "input-file":
        if not file_id:
            raise ValueError("input-file transport requires a file ID")
        content.append({"type": "input_file", "file_id": file_id})
    elif input_transport == "inline-text":
        pattern = (attempt / "input/pattern.csv").read_text(encoding="utf-8")
        content.append(
            {
                "type": "input_text",
                "text": (
                    "The following is the complete content of `pattern.csv`:\n\n"
                    f"```csv\n{pattern}```"
                ),
            }
        )
    else:
        raise ValueError(f"unsupported input_transport: {input_transport}")
    return {
        "model": condition["model"],
        "reasoning": {"effort": condition["reasoning_effort"]},
        "input": [{"role": "user", "content": content}],
        "tools": [],
        "background": bool(condition.get("background", True)),
        "store": bool(condition.get("store", True)),
        "max_output_tokens": int(condition.get("max_output_tokens", 65536)),
    }


def serialize_request(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def archive_request(run_dir: Path, payload: dict[str, Any]) -> str:
    serialized = serialize_request(payload)
    (run_dir / "request.json").write_bytes(serialized)
    return sha256_bytes(serialized)


def prepare_attempt(
    output: Path,
    problem: Problem,
    prompt: str,
    expected_pattern_sha256: str | None = None,
) -> Path:
    attempt = output / "attempts" / problem.problem_id
    input_dir = attempt / "input"
    run_dir = attempt / "run"
    workspace = attempt / "workspace"
    control = attempt / "control"
    for path in (input_dir, run_dir, workspace, control):
        path.mkdir(parents=True, exist_ok=True)
    prompt_path = input_dir / "prompt.md"
    pattern_path = input_dir / "pattern.csv"
    prompt_path.write_text(prompt + "\n", encoding="utf-8")
    shutil.copy2(problem.pattern, input_dir / "pattern.csv")
    shutil.copy2(problem.reference, control / "reference.cif")
    source_pattern_sha256 = sha256_file(problem.pattern)
    if expected_pattern_sha256 and source_pattern_sha256 != expected_pattern_sha256:
        raise RuntimeError(f"{problem.problem_id}: source pattern hash does not match panel")
    if sha256_file(pattern_path) != source_pattern_sha256:
        raise RuntimeError(f"{problem.problem_id}: staged pattern hash does not match source")
    pattern_text = pattern_path.read_text(encoding="utf-8")
    write_json(
        control / "assignment.json",
        {
            "problem_id": problem.problem_id,
            "formula": problem.formula,
            "pattern_sha256": source_pattern_sha256,
            "pattern_bytes": pattern_path.stat().st_size,
            "pattern_line_count": len(pattern_text.splitlines()),
            "prompt_sha256": sha256_file(prompt_path),
            "prompt_bytes": prompt_path.stat().st_size,
            "reference_sha256": sha256_file(problem.reference),
        },
    )
    return attempt


def stage_attempt(
    output: Path,
    problem: Problem,
    prompt: str,
    condition: dict[str, Any],
    expected_pattern_sha256: str | None,
) -> dict[str, Any]:
    attempt = prepare_attempt(output, problem, prompt, expected_pattern_sha256)
    assignment = load_json(attempt / "control/assignment.json")
    input_transport = str(condition.get("input_transport", "inline-text"))
    request_sha256 = None
    if input_transport == "inline-text":
        payload = response_payload(attempt, prompt, condition)
        request_sha256 = archive_request(attempt / "run", payload)
        wrapper = payload["input"][0]["content"][1]["text"]
        pattern = (attempt / "input/pattern.csv").read_text(encoding="utf-8")
        expected_wrapper = (
            "The following is the complete content of `pattern.csv`:\n\n"
            f"```csv\n{pattern}```"
        )
        if wrapper != expected_wrapper:
            raise RuntimeError(f"{problem.problem_id}: serialized pattern wrapper is incomplete")
    return {
        **assignment,
        "request_sha256": request_sha256,
        "input_transport": input_transport,
    }


def verify_output_extraction() -> dict[str, Any]:
    response = {
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "type": "output_text",
                        "text": (
                            "`selected.cif`\n```cif\ndata_preflight\n_cell_length_a 4\n```\n\n"
                            "`alternative-1.cif`\n```cif\ndata_alternative\n_cell_length_a 5\n```"
                        ),
                    }
                ],
            }
        ]
    }
    with tempfile.TemporaryDirectory(prefix="vpbench-llm-extraction-") as temporary:
        workspace = Path(temporary)
        names = materialize_cifs(output_text(response), workspace)
        if names != ["selected.cif", "alternative-1.cif"]:
            raise RuntimeError(f"output extraction preflight failed: {names}")
        digests = {name: sha256_file(workspace / name) for name in names}
    return {"valid": True, "files": names, "sha256": digests}


def run_attempt(
    output: Path,
    problem: Problem,
    prompt: str,
    condition: dict[str, Any],
    api_key: str,
    base_url: str,
    poll_seconds: float,
) -> dict[str, Any]:
    attempt = output / "attempts" / problem.problem_id
    run_dir = attempt / "run"
    workspace = attempt / "workspace"
    launch_path = run_dir / "launch.json"
    launch = load_json(launch_path) if launch_path.is_file() else {}
    client = OpenAIHTTP(api_key, base_url)
    file_id = launch.get("file_id")
    response_id = launch.get("response_id")
    input_transport = str(condition.get("input_transport", "inline-text"))

    try:
        if not response_id:
            if input_transport == "input-file":
                uploaded = client.upload_pattern(attempt / "input/pattern.csv")
                file_id = str(uploaded["id"])
                payload = response_payload(attempt, prompt, condition, file_id=file_id)
                request_sha256 = archive_request(run_dir, payload)
            else:
                request_path = run_dir / "request.json"
                request_bytes = request_path.read_bytes()
                request_sha256 = sha256_bytes(request_bytes)
            if input_transport == "input-file":
                request_bytes = (run_dir / "request.json").read_bytes()
            response = client.request(
                "POST",
                "/responses",
                data=request_bytes,
                headers={"Content-Type": "application/json"},
            )
            response_id = str(response["id"])
            launch = {
                "problem_id": problem.problem_id,
                "started_at": now(),
                "file_id": file_id,
                "response_id": response_id,
                "model": condition["model"],
                "reasoning_effort": condition["reasoning_effort"],
                "tools": [],
                "input_transport": input_transport,
                "request_sha256": request_sha256,
            }
            write_json(launch_path, launch)
        else:
            response = client.request("GET", f"/responses/{response_id}")

        while response.get("status") not in TERMINAL_STATUSES:
            with (run_dir / "poll.jsonl").open("a", encoding="utf-8") as log:
                log.write(json.dumps({"time": now(), "status": response.get("status")}) + "\n")
            time.sleep(poll_seconds)
            response = client.request("GET", f"/responses/{response_id}")

        write_json(run_dir / "response.json", response)
        text = output_text(response)
        (run_dir / "output.md").write_text(text + "\n", encoding="utf-8")
        candidates = materialize_cifs(text, workspace)
        verifier = evaluate_workspace(
            attempt / "control/reference.cif",
            workspace,
            problem.problem_id,
        )
        write_json(run_dir / "verifier-result.json", verifier)
        selected_exact, candidates_exact = exact_outcomes(verifier)
        parsed = list(verifier.get("artifacts", []))
        launch.update(
            {
                "ended_at": now(),
                "status": response.get("status"),
                "candidates_extracted": candidates,
                "selected_exact": selected_exact,
                "candidates_exact": candidates_exact,
                "exact_success": candidates_exact,
                "usage": response.get("usage"),
                "error": response.get("error"),
                "incomplete_details": response.get("incomplete_details"),
            }
        )
        write_json(launch_path, launch)
        return {
            "attempt_id": problem.problem_id,
            "problem_id": problem.problem_id,
            "status": "archived" if response.get("status") == "completed" else "failed",
            "api_status": response.get("status"),
            "selected_exact": selected_exact,
            "candidates_exact": candidates_exact,
            "exact_success": candidates_exact,
            "matched_candidates": verifier["metrics"]["matched_candidates"],
            "candidate_count": len(candidates),
            "parseable_candidate_count": len(parsed),
            "selected_parseable": "selected.cif" in parsed,
            "any_candidate_parseable": bool(parsed),
            "response_id": response_id,
            "started_at": launch.get("started_at"),
            "ended_at": launch["ended_at"],
            "usage": response.get("usage"),
        }
    finally:
        if file_id:
            try:
                client.delete_file(str(file_id))
            except requests.HTTPError as error:
                (run_dir / "file-cleanup-error.txt").write_text(str(error) + "\n")


def summarize(states: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = list(states.values())
    archived = [row for row in rows if row.get("status") == "archived"]
    selected_exact = [row for row in archived if row.get("selected_exact")]
    candidates_exact = [row for row in archived if row.get("candidates_exact")]
    input_tokens = sum(int((row.get("usage") or {}).get("input_tokens", 0)) for row in archived)
    output_tokens = sum(int((row.get("usage") or {}).get("output_tokens", 0)) for row in archived)
    reasoning_tokens = sum(
        int(((row.get("usage") or {}).get("output_tokens_details") or {}).get("reasoning_tokens", 0))
        for row in archived
    )
    candidate_files = sum(int(row.get("candidate_count", 0)) for row in archived)
    parseable_files = sum(int(row.get("parseable_candidate_count", 0)) for row in archived)
    return {
        "attempts": len(rows),
        "pending": sum(row.get("status") == "pending" for row in rows),
        "running": sum(row.get("status") == "running" for row in rows),
        "archived": len(archived),
        "failed": sum(row.get("status") == "failed" for row in rows),
        "selected_exact": len(selected_exact),
        "selected_exact_rate_completed": len(selected_exact) / len(archived) if archived else None,
        "candidates_exact": len(candidates_exact),
        "candidates_exact_rate_completed": (
            len(candidates_exact) / len(archived) if archived else None
        ),
        "exact": len(candidates_exact),
        "exact_rate_completed": len(candidates_exact) / len(archived) if archived else None,
        "cases_with_selected_parseable": sum(
            bool(row.get("selected_parseable")) for row in archived
        ),
        "cases_with_any_parseable": sum(
            bool(row.get("any_candidate_parseable")) for row in archived
        ),
        "candidate_files": candidate_files,
        "parseable_candidate_files": parseable_files,
        "parseable_candidate_file_rate": (
            parseable_files / candidate_files if candidate_files else None
        ),
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "reasoning_tokens": reasoning_tokens,
            "total_tokens": input_tokens + output_tokens,
        },
        "results": rows,
    }


def run_campaign(args: argparse.Namespace) -> int:
    repository = Path(__file__).resolve().parents[1]
    runner_path = Path(__file__).resolve()
    condition_path = args.condition.resolve()
    panel_path = args.panel.resolve()
    output = args.output.resolve()
    condition = load_condition(condition_path, repository)
    problems = load_problem_collection(panel_path)
    if args.problem_id:
        requested = set(args.problem_id)
        available = {problem.problem_id for problem in problems}
        unknown = requested - available
        if unknown:
            raise SystemExit(f"unknown --problem-id values: {', '.join(sorted(unknown))}")
        problems = [problem for problem in problems if problem.problem_id in requested]

    repository_record = repository_provenance(repository, runner_path)
    if repository_record["dirty"] and not args.dry_run:
        raise SystemExit(
            "refusing a live API launch from a dirty repository; commit or stash all changes first"
        )

    template_path = Path(condition["prompt_path"])
    template = template_path.read_text(encoding="utf-8")
    prompts = {problem.problem_id: prompt_for(problem, template) for problem in problems}
    panel = load_json(panel_path)
    panel_items = panel.get("cases", panel.get("problems", []))
    panel_by_id = {
        str(item.get("problem_id", item.get("case_id"))): item for item in panel_items
    }

    output.mkdir(parents=True, exist_ok=True)
    (output / "attempts").mkdir(exist_ok=True)
    run_path = output / "run.json"
    immutable = {
        "condition_sha256": sha256_file(condition_path),
        "panel_sha256": sha256_file(panel_path),
        "prompt_template_sha256": sha256_file(template_path),
        "runner_sha256": repository_record["runner_sha256"],
    }
    if run_path.exists():
        existing_run = load_json(run_path)
        mismatches = {
            key: (existing_run.get(key), value)
            for key, value in immutable.items()
            if existing_run.get(key) != value
        }
        if mismatches:
            raise RuntimeError(f"output provenance does not match this launch: {mismatches}")
    else:
        shutil.copy2(condition_path, output / "condition.toml")
        shutil.copy2(panel_path, output / "panel.json")
        shutil.copy2(template_path, output / "prompt-template.md")
        shutil.copy2(runner_path, output / "runner.py")

    case_inputs = []
    for problem in problems:
        source = panel_by_id.get(problem.problem_id, {})
        expected_pattern_sha256 = source.get("pattern_sha256")
        record = stage_attempt(
            output,
            problem,
            prompts[problem.problem_id],
            condition,
            str(expected_pattern_sha256) if expected_pattern_sha256 else None,
        )
        record.update(
            {
                "dataset": source.get("dataset"),
                "panel": source.get("panel"),
                "stream": source.get("stream"),
            }
        )
        case_inputs.append(record)
    write_json(output / "input-manifest.json", {"cases": case_inputs})
    extraction = verify_output_extraction()
    preflight = {
        "valid": True,
        "problem_count": len(problems),
        "all_pattern_hashes_verified": True,
        "all_rendered_prompts_archived": True,
        "all_inline_requests_archived": all(
            item["request_sha256"] for item in case_inputs
        ),
        "pattern_line_count_min": min(item["pattern_line_count"] for item in case_inputs),
        "pattern_line_count_max": max(item["pattern_line_count"] for item in case_inputs),
        "output_extraction": extraction,
    }
    write_json(output / "preflight.json", preflight)
    run_record = {
        "schema_version": "2",
        "created_at": load_json(run_path)["created_at"] if run_path.exists() else now(),
        "condition": condition["id"],
        **immutable,
        "problem_count": len(problems),
        "parallel": args.parallel,
        "model": condition["model"],
        "reasoning_effort": condition["reasoning_effort"],
        "tools": [],
        "input_contract": "one user message containing the rendered prompt and complete CSV",
        "input_transport": condition.get("input_transport", "inline-text"),
        "request_serialization": "UTF-8 JSON; sorted keys; compact separators; trailing newline",
        "repository": repository_record,
        "prompt_template_path": str(template_path.relative_to(repository)),
        "input_manifest_sha256": sha256_file(output / "input-manifest.json"),
        "preflight_sha256": sha256_file(output / "preflight.json"),
    }
    write_json(run_path, run_record)

    existing: dict[str, dict[str, Any]] = {}
    progress_path = output / "progress.json"
    if progress_path.is_file():
        existing = {row["problem_id"]: row for row in load_json(progress_path)["attempts"]}
    inputs_by_id = {item["problem_id"]: item for item in case_inputs}
    states = {
        problem.problem_id: existing.get(
            problem.problem_id,
            {
                "attempt_id": problem.problem_id,
                "problem_id": problem.problem_id,
                "status": "pending",
                "selected_exact": False,
                "candidates_exact": False,
                "exact_success": False,
                "dataset": inputs_by_id[problem.problem_id].get("dataset"),
                "panel": inputs_by_id[problem.problem_id].get("panel"),
                "stream": inputs_by_id[problem.problem_id].get("stream"),
            },
        )
        for problem in problems
    }
    lock = threading.Lock()

    def update(problem_id: str, values: dict[str, Any]) -> None:
        with lock:
            states[problem_id].update(values)
            write_json(output / "progress.json", {"attempts": list(states.values())})
            summary = summarize(states)
            print(
                f"archived={summary['archived']} selected={summary['selected_exact']} "
                f"any={summary['candidates_exact']} running={summary['running']} "
                f"pending={summary['pending']} failed={summary['failed']}",
                flush=True,
            )

    write_json(output / "progress.json", {"attempts": list(states.values())})
    if args.dry_run:
        write_json(output / "summary.json", summarize(states))
        print(f"staged and verified {len(problems)} LLM-only attempts in {output}")
        return 0

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    runnable = [problem for problem in problems if states[problem.problem_id]["status"] != "archived"]

    def one(problem: Problem) -> dict[str, Any]:
        update(problem.problem_id, {"status": "running", "started_at": now()})
        try:
            result = run_attempt(
                output,
                problem,
                prompts[problem.problem_id],
                condition,
                api_key,
                base_url,
                args.poll_seconds,
            )
        except Exception as error:
            result = {
                "attempt_id": problem.problem_id,
                "problem_id": problem.problem_id,
                "status": "failed",
                "selected_exact": False,
                "candidates_exact": False,
                "exact_success": False,
                "error": f"{type(error).__name__}: {error}",
                "ended_at": now(),
            }
        update(problem.problem_id, result)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = [executor.submit(one, problem) for problem in runnable]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    summary = summarize(states)
    write_json(output / "summary.json", summary)
    print(
        json.dumps(
            {
                key: summary[key]
                for key in ("archived", "failed", "selected_exact", "candidates_exact")
            },
            indent=2,
        )
    )
    return 0 if summary["failed"] == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", type=Path, required=True)
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--poll-seconds", type=float, default=10)
    parser.add_argument("--problem-id", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--lock-file",
        type=Path,
        default=Path("/tmp/verifiable-pxrd-run-llm-only.lock"),
    )
    args = parser.parse_args()
    if args.parallel < 1:
        raise SystemExit("--parallel must be positive")
    with campaign_lock(args.lock_file.resolve()):
        return run_campaign(args)


if __name__ == "__main__":
    raise SystemExit(main())
