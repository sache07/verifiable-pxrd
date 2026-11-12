"""Shared dataset and support-policy checks for framework target builders."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

SUPPORT_POLICIES = ("manifest", "common-envelope", "require-all")
COMMON_SUPPORT_FIELDS = (
    "common_element_vocabulary",
    "ordered_full_occupancy",
    "primitive_site_count_at_most_20",
)


def corpus_directory_name(corpus_root: Path) -> str:
    """Return the stable on-disk name for one benchmark corpus."""

    name = corpus_root.expanduser().resolve().name.lower()
    if not name or name in {".", ".."}:
        raise ValueError(f"corpus root has no usable directory name: {corpus_root}")
    return name


def framework_target_root(
    repository_root: Path,
    framework_key: str,
    corpus_root: Path,
) -> Path:
    """Locate framework-native inputs beside the framework that consumes them."""

    return (
        repository_root.expanduser().resolve()
        / "baselines"
        / framework_key
        / "targets"
        / corpus_directory_name(corpus_root)
    )


def relative_reference(target: Path, *, from_directory: Path) -> str:
    """Serialize a portable path from one generated bundle to a source file."""

    return Path(os.path.relpath(target.resolve(), from_directory.resolve())).as_posix()


def configure_paths(
    corpus_root: Path,
    framework_key: str,
    output_root: Path | None = None,
) -> dict[str, Path]:
    """Return canonical source and output paths for a target builder.

    The hidden benchmark structures remain under ``pxrd-bench``. Derived,
    framework-native model inputs live with the corresponding public adapter.
    ``output_root`` is an explicit escape hatch for scratch builds and audits.
    """

    corpus = corpus_root.expanduser().resolve()
    output = (
        output_root.expanduser().resolve()
        if output_root is not None
        else framework_target_root(REPOSITORY_ROOT, framework_key, corpus)
    )
    return {
        "corpus": corpus,
        "source_manifest": corpus / "manifest.json",
        "output": output,
        "patterns": output / "patterns",
        "output_manifest": output / "manifest.json",
    }


def validate_source_manifest(
    source: dict[str, Any],
    *,
    expected_cases: int,
    dataset_id: str | None,
    case_prefix: str | None,
) -> tuple[str, list[dict[str, Any]]]:
    """Validate the selected corpus rather than silently accepting another one."""

    actual_dataset_id = source.get("dataset_id")
    if not isinstance(actual_dataset_id, str) or not actual_dataset_id:
        raise RuntimeError("source manifest has no non-empty dataset_id")
    if dataset_id is not None and actual_dataset_id != dataset_id:
        raise RuntimeError(f"expected dataset_id {dataset_id!r}, found {actual_dataset_id!r}")
    cases = source.get("cases")
    if not isinstance(cases, list) or len(cases) != expected_cases:
        found = len(cases) if isinstance(cases, list) else "non-list"
        raise RuntimeError(f"expected {expected_cases} source cases, found {found}")
    case_ids = [case.get("case_id") for case in cases]
    if len(set(case_ids)) != expected_cases or any(not isinstance(item, str) for item in case_ids):
        raise RuntimeError("source case IDs are missing or not unique")
    if case_prefix is not None:
        bad = [item for item in case_ids if not item.startswith(case_prefix)]
        if bad:
            raise RuntimeError(
                f"{len(bad)} source case IDs do not start with {case_prefix!r}; first={bad[0]!r}"
            )
    return actual_dataset_id, cases


def framework_support(case: dict[str, Any], *, framework_key: str, policy: str) -> tuple[str, bool]:
    """Resolve one case's applicability under an explicit support policy.

    ``manifest`` uses the framework-specific exposure label when present.
    ``common-envelope`` evaluates the three cross-framework static
    support gates. ``require-all`` does the same and fails immediately if a case
    falls outside that envelope.
    """

    if policy not in SUPPORT_POLICIES:
        raise ValueError(f"unknown support policy: {policy}")
    exposure = case.get("baseline_exposure", {}).get(framework_key)
    envelope = case.get("baseline_support")
    if policy == "manifest" and exposure is not None:
        supported = not str(exposure).startswith("unsupported")
        return str(exposure), supported
    if isinstance(envelope, dict):
        missing = [field for field in COMMON_SUPPORT_FIELDS if field not in envelope]
        if missing:
            raise RuntimeError(
                f"{case.get('case_id')}: baseline_support lacks {', '.join(missing)}"
            )
        failed = [field for field in COMMON_SUPPORT_FIELDS if envelope[field] is not True]
        supported = not failed
        applicability = (
            "supported_common_envelope"
            if supported
            else "unsupported_common_envelope:" + ",".join(failed)
        )
    elif exposure is not None:
        supported = not str(exposure).startswith("unsupported")
        applicability = str(exposure)
    else:
        raise RuntimeError(
            f"{case.get('case_id')}: no baseline_support or {framework_key} exposure"
        )
    if policy == "require-all" and not supported:
        raise RuntimeError(
            f"{case.get('case_id')}: outside required framework support envelope ({applicability})"
        )
    return applicability, supported
