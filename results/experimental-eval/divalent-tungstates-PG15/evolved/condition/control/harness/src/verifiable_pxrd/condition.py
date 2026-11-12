from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .util import expand_path


@dataclass(frozen=True, slots=True)
class Condition:
    condition_id: str
    adapter: str
    model: str
    reasoning_effort: str
    prompt: Path
    review_prompt: Path | None
    capability: Path | None
    installation: dict[str, Any]
    path_entries: tuple[Path, ...]
    read_paths: tuple[Path, ...]
    optional_read_paths: tuple[Path, ...]
    deny_paths: tuple[Path, ...]
    variables: dict[str, str]
    cpu_quota: str
    memory_max: str
    tasks_max: int
    timeout_seconds: int | None
    first_pass_timeout_seconds: int | None
    network: bool
    systemd_scope: bool
    codex: Path
    auth_method: str
    auth_home: Path


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def _expanded_string(value: str) -> str:
    return os.path.expanduser(os.path.expandvars(value))


def _repository_root(path: Path) -> Path:
    """Find the repository that owns a condition stored at any nesting depth."""

    for parent in path.parents:
        if (parent / "pyproject.toml").is_file() and (parent / "src/verifiable_pxrd").is_dir():
            return parent
    raise ValueError(f"condition is not inside a verifiable-pxrd checkout: {path}")


def load_condition(path: Path) -> Condition:
    path = path.resolve()
    repository = _repository_root(path)
    raw = _load_toml(path)
    environment_value = raw.get("environment", {})
    if not isinstance(environment_value, dict):
        raise TypeError("environment must be an inline table")
    environment = environment_value
    installation_value = environment.get("installation", {})
    if not isinstance(installation_value, dict):
        raise TypeError("environment.installation must be an inline table")
    capability_value = raw.get("capability")
    review_prompt_value = raw.get("review_prompt")
    return Condition(
        condition_id=str(raw["id"]),
        adapter=str(raw.get("adapter", "codex")),
        model=str(raw.get("model", "")),
        reasoning_effort=str(raw.get("reasoning_effort", "high")),
        prompt=expand_path(str(raw["prompt"]), repository),
        review_prompt=(
            expand_path(str(review_prompt_value), repository) if review_prompt_value else None
        ),
        capability=(expand_path(str(capability_value), repository) if capability_value else None),
        installation=dict(installation_value),
        path_entries=tuple(
            expand_path(str(item), repository) for item in environment.get("path_entries", [])
        ),
        read_paths=tuple(
            expand_path(str(item), repository) for item in environment.get("read_paths", [])
        ),
        optional_read_paths=tuple(
            expand_path(str(item), repository)
            for item in environment.get("optional_read_paths", [])
        ),
        deny_paths=tuple(
            expand_path(str(item), repository) for item in environment.get("deny_paths", [])
        ),
        variables={
            str(key): _expanded_string(str(value))
            for key, value in environment.get("variables", {}).items()
        },
        cpu_quota=str(raw.get("cpu_quota", "200%")),
        memory_max=str(raw.get("memory_max", "5G")),
        tasks_max=int(raw.get("tasks_max", 128)),
        timeout_seconds=(
            int(raw["timeout_seconds"]) if raw.get("timeout_seconds") is not None else None
        ),
        first_pass_timeout_seconds=(
            int(raw["first_pass_timeout_seconds"])
            if raw.get("first_pass_timeout_seconds") is not None
            else None
        ),
        network=bool(raw.get("network", False)),
        systemd_scope=bool(raw.get("systemd_scope", True)),
        codex=Path(_expanded_string(str(raw.get("codex", "/usr/local/bin/codex")))).resolve(),
        auth_method=str(raw.get("auth_method", "chatgpt")),
        auth_home=Path(
            _expanded_string(str(raw.get("auth_home", "~/.codex")))
        ).resolve(),
    )


def unresolved_environment(path: Path | str) -> bool:
    return "$" in str(path)
