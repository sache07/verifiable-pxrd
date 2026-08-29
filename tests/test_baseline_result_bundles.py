from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
RESULTS = ROOT / "results" / "baselines"
pytestmark = pytest.mark.skipif(
    not (RESULTS / "manifest.json").is_file(),
    reason="release evidence is not included in the Python source distribution",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_baseline_result_manifest_is_complete() -> None:
    manifest = json.loads((RESULTS / "manifest.json").read_text())
    assert manifest["bundle_count"] == 14
    assert len({row["bundle_path"] for row in manifest["bundles"]}) == 14
    assert not any("gpt-5.6" in row["framework"].lower() for row in manifest["bundles"])


def test_bundle_indexes_and_checksums_are_self_consistent() -> None:
    manifest = json.loads((RESULTS / "manifest.json").read_text())
    for record in manifest["bundles"]:
        bundle = RESULTS / record["bundle_path"]
        assert sha256_file(bundle / "artifacts.sha256") == record["artifacts_sha256"]
        run = json.loads((bundle / "run.json").read_text())
        with (bundle / "cases.csv").open(newline="") as stream:
            cases = list(csv.DictReader(stream))
        with (bundle / "candidates.csv").open(newline="") as stream:
            candidates = list(csv.DictReader(stream))
        assert len(cases) == 100
        assert len(candidates) == run["results"]["candidate_record_count"]
        assert sum(row["best_of_1_structure_match"] == "true" for row in cases) == run[
            "results"
        ]["exact_structure_matches_at_1"]
        assert sum(
            row["best_of_reported_k_structure_match"] == "true" for row in cases
        ) == run["results"]["exact_structure_matches_at_reported_k"]

        checksums = {}
        for line in (bundle / "artifacts.sha256").read_text().splitlines():
            digest, name = line.split("  ", 1)
            checksums[name] = digest
            assert sha256_file(bundle / name) == digest
        archive = bundle / "candidates.tar.zst"
        candidate_root = bundle / "candidates"
        candidate_manifest = json.loads((candidate_root / "manifest.json").read_text())
        assert candidate_manifest["case_count"] == 100
        assert candidate_manifest["candidate_record_count"] == len(candidates)
        assert candidate_manifest["verifier_result_file_count"] == 100
        assert len({row["verifier_result_path"] for row in candidates}) == 100
        for row in candidates:
            assert (bundle / row["verifier_result_path"]).is_file()
            if row["candidate_path"]:
                assert sha256_file(bundle / row["candidate_path"]) == row["candidate_sha256"]
        if record["candidate_archive_published"]:
            assert archive.is_file()
            assert "candidates.tar.zst" in checksums
            assert candidate_manifest["candidate_cif_count"] > 0
        else:
            assert record["framework"] == "DiffractGPT"
            assert not archive.exists()
            assert "candidates.tar.zst" not in checksums
            assert candidate_manifest["candidate_cif_count"] == 0
