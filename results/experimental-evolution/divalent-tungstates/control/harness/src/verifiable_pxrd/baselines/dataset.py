"""Dataset binding shared by the pXRD Modal inference applications."""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from verifiable_pxrd.baselines.targets import framework_target_root

CORPUS_ENV = "VERIFIABLE_PXRD_CORPUS_ROOT"
DATASET_ID_ENV = "VERIFIABLE_PXRD_DATASET_ID"
CASE_PREFIX_ENV = "VERIFIABLE_PXRD_CASE_PREFIX"
SUPPORT_POLICY_ENV = "VERIFIABLE_PXRD_SUPPORT_POLICY"
SOURCE_SHA_ENV = "VERIFIABLE_PXRD_SOURCE_MANIFEST_SHA256"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _slug(value: str) -> str:
    if value == "pXRD-100":
        return "pxrd100"
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError(f"dataset ID does not produce a safe slug: {value!r}")
    return slug


@dataclass(frozen=True)
class DatasetBinding:
    repository_root: Path
    corpus_root: Path
    dataset_id: str
    case_prefix: str
    support_policy: str
    source_manifest_sha256: str
    slug: str

    def target_root(self, framework: str) -> Path:
        return framework_target_root(self.repository_root, framework, self.corpus_root)

    def request_identity(self) -> dict[str, str]:
        return {
            "source_dataset_id": self.dataset_id,
            "case_prefix": self.case_prefix,
            "support_policy": self.support_policy,
            "source_manifest_sha256": self.source_manifest_sha256,
        }

    def environment(self) -> dict[str, str]:
        return {
            CORPUS_ENV: str(self.corpus_root),
            DATASET_ID_ENV: self.dataset_id,
            CASE_PREFIX_ENV: self.case_prefix,
            SUPPORT_POLICY_ENV: self.support_policy,
            SOURCE_SHA_ENV: self.source_manifest_sha256,
        }


def load_dataset_binding(repository_root: Path) -> DatasetBinding:
    """Resolve and validate the corpus selected before a Modal app is imported."""

    default_root = repository_root / "pxrd-bench" / "pXRD-100"
    corpus_root = Path(os.environ.get(CORPUS_ENV, str(default_root))).expanduser().resolve()
    manifest_path = corpus_root / "manifest.json"
    if not manifest_path.is_file():
        serialized = {
            "dataset_id": os.environ.get(DATASET_ID_ENV),
            "case_prefix": os.environ.get(CASE_PREFIX_ENV),
            "support_policy": os.environ.get(SUPPORT_POLICY_ENV),
            "source_manifest_sha256": os.environ.get(SOURCE_SHA_ENV),
        }
        if all(serialized.values()):
            support_policy = str(serialized["support_policy"])
            if support_policy not in {"manifest", "common-envelope", "require-all"}:
                raise RuntimeError(f"unsupported pXRD support policy: {support_policy!r}")
            source_digest = str(serialized["source_manifest_sha256"])
            if re.fullmatch(r"[0-9a-f]{64}", source_digest) is None:
                raise RuntimeError("serialized pXRD source-manifest digest is invalid")
            return DatasetBinding(
                repository_root=repository_root.expanduser().resolve(),
                corpus_root=corpus_root,
                dataset_id=str(serialized["dataset_id"]),
                case_prefix=str(serialized["case_prefix"]),
                support_policy=support_policy,
                source_manifest_sha256=source_digest,
                slug=_slug(str(serialized["dataset_id"])),
            )
        raise RuntimeError(f"pXRD corpus manifest is missing: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = list(manifest.get("cases", []))
    if not cases:
        raise RuntimeError(f"pXRD corpus has no cases: {manifest_path}")

    dataset_id = os.environ.get(DATASET_ID_ENV) or str(manifest.get("dataset_id") or "")
    if not dataset_id:
        raise RuntimeError(f"pXRD corpus has no dataset_id: {manifest_path}")
    declared_id = manifest.get("dataset_id")
    if declared_id is not None and str(declared_id) != dataset_id:
        raise RuntimeError(
            f"pXRD dataset identity mismatch: requested {dataset_id!r}, manifest {declared_id!r}"
        )

    first_case_id = str(cases[0]["case_id"])
    inferred_prefix = first_case_id.split("-", 1)[0]
    case_prefix = os.environ.get(CASE_PREFIX_ENV) or inferred_prefix
    if any(not str(case["case_id"]).startswith(case_prefix + "-") for case in cases):
        raise RuntimeError(f"case prefix {case_prefix!r} does not cover the selected corpus")

    default_policy = "require-all" if corpus_root.name == "pXRD-ood" else "manifest"
    support_policy = os.environ.get(SUPPORT_POLICY_ENV) or default_policy
    if support_policy not in {"manifest", "common-envelope", "require-all"}:
        raise RuntimeError(f"unsupported pXRD support policy: {support_policy!r}")

    return DatasetBinding(
        repository_root=repository_root.expanduser().resolve(),
        corpus_root=corpus_root,
        dataset_id=dataset_id,
        case_prefix=case_prefix,
        support_policy=support_policy,
        source_manifest_sha256=_sha256(manifest_path),
        slug=_slug(dataset_id),
    )


def validate_target_payload(payload: Mapping[str, Any], binding: DatasetBinding) -> None:
    """Reject a target manifest that is stale or belongs to another corpus."""

    if str(payload.get("source_manifest_sha256")) != binding.source_manifest_sha256:
        raise RuntimeError("framework target manifest is stale for the selected corpus")
    if str(payload.get("source_dataset_id", binding.dataset_id)) != binding.dataset_id:
        raise RuntimeError("framework target dataset identity mismatch")
    if payload.get("case_prefix", binding.case_prefix) != binding.case_prefix:
        raise RuntimeError("framework target case-prefix contract mismatch")
    if payload.get("support_policy", binding.support_policy) != binding.support_policy:
        raise RuntimeError("framework target support-policy contract mismatch")


def validate_request_identity(
    request: Mapping[str, Any], payload: Mapping[str, Any], binding: DatasetBinding
) -> None:
    validate_target_payload(payload, binding)
    expected = binding.request_identity()
    for key, value in expected.items():
        if str(request.get(key, "")) != value:
            raise RuntimeError(
                f"request {key} mismatch: expected {value!r}, found {request.get(key)!r}"
            )
