from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from verifiable_pxrd.baselines.dataset import (
    CASE_PREFIX_ENV,
    CORPUS_ENV,
    DATASET_ID_ENV,
    SOURCE_SHA_ENV,
    SUPPORT_POLICY_ENV,
    load_dataset_binding,
    validate_request_identity,
    validate_target_payload,
)


def _write_corpus(root: Path) -> tuple[Path, str]:
    corpus = root / "pXRD-fixture"
    corpus.mkdir()
    payload = {
        "dataset_id": "fixture-v1",
        "cases": [{"case_id": "fixture-001"}, {"case_id": "fixture-002"}],
    }
    manifest = corpus / "manifest.json"
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    return corpus, hashlib.sha256(manifest.read_bytes()).hexdigest()


def test_dataset_binding_and_request_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus, digest = _write_corpus(tmp_path)
    monkeypatch.setenv(CORPUS_ENV, str(corpus))
    monkeypatch.setenv(DATASET_ID_ENV, "fixture-v1")
    monkeypatch.setenv(CASE_PREFIX_ENV, "fixture")
    monkeypatch.setenv(SUPPORT_POLICY_ENV, "require-all")
    binding = load_dataset_binding(tmp_path)
    assert binding.source_manifest_sha256 == digest
    assert binding.target_root("decifer") == (
        tmp_path / "baselines" / "decifer" / "targets" / "pxrd-fixture"
    )
    target = binding.request_identity()
    validate_target_payload(target, binding)
    validate_request_identity(binding.request_identity(), target, binding)


def test_serialized_binding_does_not_require_truth_mount(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    missing = tmp_path / "not-mounted"
    monkeypatch.setenv(CORPUS_ENV, str(missing))
    monkeypatch.setenv(DATASET_ID_ENV, "fixture-v1")
    monkeypatch.setenv(CASE_PREFIX_ENV, "fixture")
    monkeypatch.setenv(SUPPORT_POLICY_ENV, "require-all")
    monkeypatch.setenv(SOURCE_SHA_ENV, "a" * 64)
    binding = load_dataset_binding(tmp_path)
    assert binding.corpus_root == missing.resolve()
    assert binding.source_manifest_sha256 == "a" * 64


def test_stale_target_and_request_are_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus, _digest = _write_corpus(tmp_path)
    monkeypatch.setenv(CORPUS_ENV, str(corpus))
    monkeypatch.setenv(DATASET_ID_ENV, "fixture-v1")
    monkeypatch.setenv(CASE_PREFIX_ENV, "fixture")
    monkeypatch.setenv(SUPPORT_POLICY_ENV, "require-all")
    binding = load_dataset_binding(tmp_path)
    with pytest.raises(RuntimeError, match="stale"):
        validate_target_payload(
            {**binding.request_identity(), "source_manifest_sha256": "0" * 64}, binding
        )
    target = binding.request_identity()
    request = {**binding.request_identity(), "case_prefix": "wrong"}
    with pytest.raises(RuntimeError, match="case_prefix mismatch"):
        validate_request_identity(request, target, binding)
