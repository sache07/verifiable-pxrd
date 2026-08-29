"""Shared dataset and support-policy checks for framework target builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

SUPPORT_POLICIES = ("manifest", "common-envelope", "require-all")
COMMON_SUPPORT_FIELDS = (
    "common_element_vocabulary",
    "ordered_full_occupancy",
    "primitive_site_count_at_most_20",
)


def configure_paths(corpus_root: Path, framework_directory: str) -> dict[str, Path]:
    """Return the canonical paths used by every target builder."""

    corpus = corpus_root.expanduser().resolve()
    output = corpus / "targets" / framework_directory
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
        raise RuntimeError(
            f"expected dataset_id {dataset_id!r}, found {actual_dataset_id!r}"
        )
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


def framework_support(
    case: dict[str, Any], *, framework_key: str, policy: str
) -> tuple[str, bool]:
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
            f"{case.get('case_id')}: outside required framework support envelope "
            f"({applicability})"
        )
    return applicability, supported
