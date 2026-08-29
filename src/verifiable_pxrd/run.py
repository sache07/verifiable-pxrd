from __future__ import annotations

import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import shutil
import signal
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from .benchmark import Problem, load_problem_collection
from .condition import Condition, load_condition, unresolved_environment
from .matching import evaluate_workspace, exact_outcomes
from .util import load_json, sha256_file, sha256_tree, write_json


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def _quote_toml(value: str) -> str:
    return json.dumps(value)


def doctor(condition_path: Path) -> dict[str, Any]:
    condition = load_condition(condition_path)
    failures: list[str] = []
    for path in (
        condition.codex,
        condition.auth_home,
        *condition.path_entries,
        *condition.read_paths,
        *condition.deny_paths,
    ):
        if unresolved_environment(path):
            failures.append(f"unresolved environment variable: {path}")
        elif not path.exists():
            failures.append(f"missing required path: {path}")
    if not condition.prompt.is_file():
        failures.append(f"missing prompt: {condition.prompt}")
    if condition.review_prompt is not None and not condition.review_prompt.is_file():
        failures.append(f"missing review prompt: {condition.review_prompt}")
    if condition.first_pass_timeout_seconds is not None:
        if condition.first_pass_timeout_seconds <= 0:
            failures.append("first-pass timeout must be positive")
        if condition.timeout_seconds is None:
            failures.append("first-pass timeout requires a total timeout")
        elif condition.first_pass_timeout_seconds >= condition.timeout_seconds:
            failures.append("first-pass timeout must leave time for review")
    if condition.capability:
        if not condition.capability.is_dir():
            failures.append(f"missing capability: {condition.capability}")
        elif not (condition.capability / "SKILL.md").is_file():
            failures.append(f"capability has no SKILL.md: {condition.capability}")
        capability_bin = condition.capability / "bin"
        if capability_bin.is_dir():
            for executable in capability_bin.iterdir():
                if executable.is_file() and not os.access(executable, os.X_OK):
                    failures.append(f"capability executable is not executable: {executable}")
    if condition.adapter != "codex":
        failures.append(f"unsupported adapter: {condition.adapter}")
    if condition.auth_method not in {"api", "chatgpt"}:
        failures.append(f"unsupported Codex auth method: {condition.auth_method}")
    auth = "not checked"
    if condition.adapter == "codex" and condition.codex.is_file():
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(condition.auth_home)
        process = subprocess.run(
            [str(condition.codex), "login", "status"],
            text=True,
            capture_output=True,
            check=False,
            env=environment,
        )
        auth = (process.stdout + process.stderr).strip()
        if process.returncode:
            failures.append("Codex authentication unavailable")
        elif condition.auth_method == "api" and "API key" not in auth:
            failures.append("Codex authentication does not use the required API key")
        elif condition.auth_method == "chatgpt" and "ChatGPT" not in auth:
            failures.append("Codex authentication does not use the required ChatGPT login")
    return {
        "condition": condition.condition_id,
        "adapter": condition.adapter,
        "model": condition.model,
        "auth_method": condition.auth_method,
        "required_paths": len(condition.path_entries) + len(condition.read_paths),
        "installation_components": sorted(condition.installation),
        "denied_structure_paths": len(condition.deny_paths),
        "available_optional_paths": sum(path.exists() for path in condition.optional_read_paths),
        "resource_backend": (
            "systemd" if condition.systemd_scope and shutil.which("systemd-run") else "direct"
        ),
        "resource_limits_enforced": bool(
            condition.systemd_scope and shutil.which("systemd-run")
        ),
        "auth": auth,
        "valid": not failures,
        "failures": failures,
    }


def _config_text(
    condition: Condition,
    workspace: Path,
    extra_read_paths: tuple[Path, ...] = (),
) -> str:
    profile = "vpbench"
    runtime_read_paths = [condition.codex.parent]
    for entry in condition.path_entries:
        python = entry / "python"
        if python.exists():
            resolved = python.resolve()
            if not resolved.is_relative_to(entry):
                runtime_read_paths.append(resolved.parent.parent)
    read_paths = [
        *runtime_read_paths,
        *condition.read_paths,
        *(p for p in condition.optional_read_paths if p.exists()),
        *extra_read_paths,
    ]
    permissions = "\n".join(
        f'{_quote_toml(str(path))} = "read"' for path in dict.fromkeys(read_paths)
    )
    denials = "\n".join(f'{_quote_toml(str(path))} = "deny"' for path in condition.deny_paths)
    capability_bin = workspace / ".vpbench-capability/bin"
    path_entries = [str(item) for item in condition.path_entries]
    if condition.capability is not None and capability_bin.is_dir():
        path_entries.insert(0, str(capability_bin))
    path = os.pathsep.join([*path_entries, "/usr/local/bin", "/usr/bin", "/bin"])
    variables = {
        "PATH": path,
        "HOME": str(workspace),
        "TMPDIR": str(workspace / ".tmp"),
        "XDG_CACHE_HOME": str(workspace / ".cache"),
        "MPLCONFIGDIR": str(workspace / ".cache/matplotlib"),
        "PYTHONNOUSERSITE": "1",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "SHELL": "/bin/bash",
        "OMP_NUM_THREADS": "2",
        "OPENBLAS_NUM_THREADS": "2",
        "MKL_NUM_THREADS": "2",
        "NUMEXPR_NUM_THREADS": "2",
        **condition.variables,
    }
    variable_text = "\n".join(
        f"{key} = {_quote_toml(value)}" for key, value in sorted(variables.items())
    )
    network = "true" if condition.network else "false"
    return f'''forced_login_method = {_quote_toml(condition.auth_method)}
service_tier = "default"
model = {_quote_toml(condition.model)}
model_reasoning_effort = {_quote_toml(condition.reasoning_effort)}
default_permissions = "{profile}"
approval_policy = "never"
web_search = "disabled"

[agents]
enabled = false

[features]
apps = false
browser_use = false
browser_use_external = false
browser_use_full_cdp_access = false
computer_use = false
image_generation = false
in_app_browser = false
multi_agent = false
multi_agent_v2 = false
plugins = false
remote_plugin = false
skill_search = false
workspace_dependencies = false

[shell_environment_policy]
inherit = "none"

[shell_environment_policy.set]
{variable_text}

[permissions.{profile}]
extends = ":workspace"

[permissions.{profile}.filesystem]
":root" = "deny"
":minimal" = "read"
":tmpdir" = "write"
":slash_tmp" = "write"
{permissions}
{denials}
{_quote_toml(str(workspace))} = "write"

[permissions.{profile}.network]
enabled = {network}

[projects.{_quote_toml(str(workspace))}]
trust_level = "trusted"
'''


def _render_prompt(condition: Condition, problem: Problem, workspace: Path) -> str:
    template = condition.prompt.read_text(encoding="utf-8")
    task = (
        template.format(
            pattern_path=workspace / "pattern.csv",
            formula=problem.formula,
            wavelength=problem.wavelength,
            radiation=problem.radiation,
        ).rstrip()
        + "\n"
    )
    if condition.capability is None:
        return task
    skill = workspace / ".vpbench-capability/SKILL.md"
    return (
        "Read and follow the capability instructions in "
        f"{skill}. Work independently and do not search for hidden answers or "
        "benchmark identifiers.\n\nTASK\n" + task
    )


def _clean_environment(codex_home: Path) -> dict[str, str]:
    environment = os.environ.copy()
    for name in tuple(environment):
        if name in {
            "OPENAI_API_KEY",
            "OPENAI_BASE_URL",
            "CODEX_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "PYTHONPATH",
            "VIRTUAL_ENV",
        } or name.startswith(("CHARACTERIZAGENT_", "MODAL_")):
            environment.pop(name, None)
    environment["CODEX_HOME"] = str(codex_home)
    environment["TERM"] = "dumb"
    return environment


def _prepare_attempt(
    run_root: Path,
    condition: Condition,
    problem: Problem,
    replicate: int,
) -> tuple[Path, Path, Path, str]:
    attempt_id = f"{problem.problem_id}-r{replicate}"
    attempt = run_root / "attempts" / attempt_id
    if attempt.exists():
        raise FileExistsError(attempt)
    workspace = attempt / "workspace"
    run_dir = attempt / "run"
    codex_home = attempt / "codex-home"
    for path in (workspace / ".tmp", workspace / ".cache/matplotlib", run_dir, codex_home):
        path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(problem.pattern, workspace / "pattern.csv")
    if condition.capability:
        shutil.copytree(condition.capability, workspace / ".vpbench-capability")
    source_home = condition.auth_home
    for name in ("auth.json", "models_cache.json"):
        source = source_home / name
        if source.exists():
            (codex_home / name).symlink_to(source)
    config = _config_text(condition, workspace)
    (codex_home / "config.toml").write_text(config, encoding="utf-8")
    prompt = _render_prompt(condition, problem, workspace)
    (attempt / "prompt.txt").write_text(prompt, encoding="utf-8")
    control = attempt / "control"
    control.mkdir()
    shutil.copy2(problem.reference, control / "reference.cif")
    write_json(
        control / "assignment.json",
        {
            "attempt_id": attempt_id,
            "problem_id": problem.problem_id,
            "formula": problem.formula,
            "replicate": replicate,
            "reference": "reference.cif",
            "reference_sha256": sha256_file(problem.reference),
            "pattern_sha256": sha256_file(problem.pattern),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "condition": condition.condition_id,
        },
    )
    return attempt, workspace, codex_home, prompt


def _remove_auth_links(codex_home: Path) -> None:
    """Keep credential links out of archived attempt artifacts."""
    for name in ("auth.json", "models_cache.json"):
        path = codex_home / name
        if path.is_symlink():
            path.unlink()


def _launch_command(
    condition: Condition,
    workspace: Path,
    codex_home: Path,
    run_dir: Path,
    token: str,
) -> tuple[list[str], str | None]:
    command = [
        str(condition.codex),
        "exec",
        "-C",
        str(workspace),
        "--skip-git-repo-check",
        "--strict-config",
        "--color",
        "never",
        "-m",
        condition.model,
        "-c",
        f'model_reasoning_effort="{condition.reasoning_effort}"',
        "--json",
        "-o",
        str(run_dir / "final-answer.md"),
        "-",
    ]
    if not condition.systemd_scope or shutil.which("systemd-run") is None:
        return command, None
    unit = f"vpbench-{token}-{int(time.time())}"
    return (
        [
            "systemd-run",
            "--user",
            f"--unit={unit}",
            "--collect",
            "--wait",
            "--pipe",
            f"--working-directory={workspace}",
            f"--setenv=CODEX_HOME={codex_home}",
            "--setenv=TERM=dumb",
            f"--property=CPUQuota={condition.cpu_quota}",
            f"--property=MemoryMax={condition.memory_max}",
            "--property=MemorySwapMax=0",
            f"--property=TasksMax={condition.tasks_max}",
            "--property=PrivateTmp=yes",
            "--property=KillMode=control-group",
            "--property=OOMPolicy=stop",
            "--",
            *command,
        ],
        unit,
    )


def _run_attempt(
    run_root: Path,
    condition: Condition,
    problem: Problem,
    replicate: int,
) -> dict[str, Any]:
    attempt, workspace, codex_home, prompt = _prepare_attempt(
        run_root, condition, problem, replicate
    )
    run_dir = attempt / "run"
    token = hashlib.sha256(str(attempt).encode()).hexdigest()[:10]
    command, unit = _launch_command(condition, workspace, codex_home, run_dir, token)
    launch = {
        "started_at": now(),
        "command": command,
        "systemd_unit": unit,
        "model": condition.model,
        "reasoning_effort": condition.reasoning_effort,
        "timeout_seconds": condition.timeout_seconds,
    }
    write_json(run_dir / "launch.json", launch)
    try:
        process = subprocess.Popen(
            command,
            cwd=workspace,
            env=_clean_environment(codex_home),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        timed_out = False
        try:
            stdout, stderr = process.communicate(prompt, timeout=condition.timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            if unit:
                subprocess.run(
                    ["systemctl", "--user", "stop", unit],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            else:
                os.killpg(process.pid, signal.SIGINT)
            try:
                stdout, stderr = process.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
    finally:
        _remove_auth_links(codex_home)
    (run_dir / "codex-events.jsonl").write_text(stdout, encoding="utf-8")
    (run_dir / "codex-stderr.log").write_text(stderr, encoding="utf-8")
    result = evaluate_workspace(attempt / "control/reference.cif", workspace, problem.problem_id)
    write_json(run_dir / "verifier-result.json", result)
    selected_exact, candidates_exact = exact_outcomes(result)
    launch.update(
        {
            "ended_at": now(),
            "returncode": process.returncode,
            "timed_out": timed_out,
            "exact_success": selected_exact,
            "selected_exact": selected_exact,
            "candidates_exact": candidates_exact,
        }
    )
    write_json(run_dir / "launch.json", launch)
    return {
        "attempt_id": attempt.name,
        "problem_id": problem.problem_id,
        "replicate": replicate,
        "status": "archived",
        "exact_success": selected_exact,
        "selected_exact": selected_exact,
        "candidates_exact": candidates_exact,
        "timed_out": timed_out,
        "returncode": process.returncode,
        "ended_at": now(),
    }


def run_panel(
    condition_path: Path,
    panel_path: Path,
    output: Path,
    parallel: int,
    replicates: int,
    replicate_start: int,
    dry_run: bool,
) -> dict[str, Any]:
    condition_path = condition_path.resolve()
    panel_path = panel_path.resolve()
    output = output.resolve()
    condition = load_condition(condition_path)
    if condition.adapter != "codex":
        raise RuntimeError(
            f"condition {condition.condition_id} uses {condition.adapter}; "
            "interactive chat results must be imported rather than launched"
        )
    health = doctor(condition_path)
    if not health["valid"]:
        raise RuntimeError("condition preflight failed: " + "; ".join(health["failures"]))
    problems = load_problem_collection(panel_path)
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"refusing to overwrite nonempty run: {output}")
    output.mkdir(parents=True, exist_ok=True)
    (output / "attempts").mkdir()
    shutil.copy2(condition_path, output / "condition.toml")
    shutil.copy2(panel_path, output / "panel.json")
    contract = output / "contract"
    contract.mkdir()
    shutil.copy2(condition.prompt, contract / "prompt.md")
    if condition.capability:
        shutil.copytree(condition.capability, contract / "capability")
    run_record = {
        "schema_version": "1",
        "created_at": now(),
        "condition": condition.condition_id,
        "condition_sha256": sha256_file(condition_path),
        "prompt_sha256": sha256_file(condition.prompt),
        "capability_sha256": sha256_tree(condition.capability) if condition.capability else None,
        "panel_sha256": sha256_file(panel_path),
        "panel_source": str(panel_path),
        "problem_count": len(problems),
        "replicates": replicates,
        "replicate_start": replicate_start,
        "parallel": parallel,
        "dry_run": dry_run,
        "model": condition.model,
        "reasoning_effort": condition.reasoning_effort,
        "auth_method": condition.auth_method,
        "resource_limits": {
            "cpu_quota": condition.cpu_quota,
            "memory_max": condition.memory_max,
            "tasks_max": condition.tasks_max,
            "timeout_seconds": condition.timeout_seconds,
        },
    }
    write_json(output / "run.json", run_record)
    jobs = [
        (problem, replicate)
        for replicate in range(replicate_start, replicate_start + replicates)
        for problem in problems
    ]
    if dry_run:
        staged = []
        for problem, replicate in jobs:
            attempt, _, codex_home, _ = _prepare_attempt(output, condition, problem, replicate)
            _remove_auth_links(codex_home)
            staged.append({"attempt_id": attempt.name, "status": "staged"})
        summary = {"staged": len(staged), "attempts": staged}
        write_json(output / "progress.json", summary)
        return summary
    progress_lock = threading.Lock()
    states = {
        f"{problem.problem_id}-r{replicate}": {
            "attempt_id": f"{problem.problem_id}-r{replicate}",
            "problem_id": problem.problem_id,
            "replicate": replicate,
            "status": "pending",
        }
        for problem, replicate in jobs
    }
    write_json(output / "progress.json", {"attempts": list(states.values())})

    def update(attempt_id: str, values: dict[str, Any]) -> None:
        with progress_lock:
            states[attempt_id].update(values)
            write_json(output / "progress.json", {"attempts": list(states.values())})

    def one(problem: Problem, replicate: int) -> dict[str, Any]:
        attempt_id = f"{problem.problem_id}-r{replicate}"
        update(attempt_id, {"status": "running", "started_at": now()})
        try:
            result = _run_attempt(output, condition, problem, replicate)
        except Exception as error:
            result = {
                "attempt_id": attempt_id,
                "problem_id": problem.problem_id,
                "replicate": replicate,
                "status": "failed",
                "exact_success": False,
                "selected_exact": False,
                "candidates_exact": False,
                "error": f"{type(error).__name__}: {error}",
                "ended_at": now(),
            }
        update(attempt_id, result)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = [executor.submit(one, problem, replicate) for problem, replicate in jobs]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    completed = list(states.values())
    selected_exact = sum(bool(item["selected_exact"]) for item in completed)
    candidates_exact = sum(bool(item["candidates_exact"]) for item in completed)
    summary = {
        "attempts": len(completed),
        "archived": sum(item["status"] == "archived" for item in completed),
        "failed": sum(item["status"] == "failed" for item in completed),
        "exact": selected_exact,
        "selected_exact": selected_exact,
        "candidates_exact": candidates_exact,
        "results": completed,
    }
    write_json(output / "summary.json", summary)
    return summary


def evaluate_run(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    rows = []
    for assignment_path in sorted((run_root / "attempts").glob("*/control/assignment.json")):
        assignment = load_json(assignment_path)
        recorded_reference = Path(str(assignment["reference"]))
        reference = (
            recorded_reference.resolve()
            if recorded_reference.is_absolute()
            else (assignment_path.parent / recorded_reference).resolve()
        )
        if not reference.is_file():
            raise FileNotFoundError(
                f"reference for {assignment['attempt_id']} is unavailable: {reference}"
            )
        workspace = assignment_path.parents[1] / "workspace"
        result = evaluate_workspace(reference, workspace, str(assignment["problem_id"]))
        write_json(assignment_path.parents[1] / "run/verifier-result.json", result)
        selected_exact, candidates_exact = exact_outcomes(result)
        rows.append(
            {
                "attempt_id": assignment["attempt_id"],
                "problem_id": assignment["problem_id"],
                "selected_exact": selected_exact,
                "candidates_exact": candidates_exact,
            }
        )
    summary = {
        "attempts": len(rows),
        "exact": sum(bool(row["selected_exact"]) for row in rows),
        "selected_exact": sum(bool(row["selected_exact"]) for row in rows),
        "candidates_exact": sum(bool(row["candidates_exact"]) for row in rows),
        "rows": rows,
    }
    write_json(run_root / "evaluation/summary.json", summary)
    return summary
