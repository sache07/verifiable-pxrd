import gzip
import json
from pathlib import Path

from verifiable_pxrd.util import sha256_file, sha256_tree

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "experiments/agent-adaptation"
TRAINING = ROOT / "results/agent-adaptation/adapted-codex/training"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_frozen_adapted_capability_matches_manifest() -> None:
    root = HARNESS / "artifacts/adapted-codex"
    manifest = _load(root / "manifest.json")
    package = root / "package"

    assert sha256_tree(package) == manifest["package_sha256"]
    for relative, expected in manifest["files"].items():
        assert sha256_file(package / relative) == expected

    evaluation = manifest["evaluation_condition"]
    assert sha256_file(ROOT / evaluation["path"]) == evaluation["condition_sha256"]
    assert sha256_file(HARNESS / "prompts/solve.md") == evaluation["prompt_sha256"]
    assert sha256_file(HARNESS / "prompt.md") == manifest["trainer_prompt_sha256"]
    assert sha256_file(HARNESS / "trainer-skill/SKILL.md") == manifest["trainer_skill_sha256"]
    assert sha256_file(
        TRAINING / "pxrd-codex-baseline-50/trainer-notes/baseline-synthesis.md"
    ) == manifest["trainer_notes"]["baseline_synthesis_sha256"]
    assert sha256_file(
        TRAINING / "adapted-codex-r1-validation/trainer-notes/revision-001-freeze.md"
    ) == manifest["trainer_notes"]["wave_assessment_sha256"]


def test_training_bundles_are_complete_and_explicit() -> None:
    curriculum = _load(HARNESS / "curriculum/train-50/manifest.json")
    expected_ids = {item["problem_id"] for item in curriculum["problems"]}
    baseline = _load(TRAINING / "pxrd-codex-baseline-50/bundle.json")
    validation = _load(TRAINING / "adapted-codex-r1-validation/bundle.json")
    judge_source = _load(TRAINING / "adapted-codex-first-pass-50/bundle.json")

    baseline_ids = {item["case_id"] for item in baseline["cases"]}
    assert baseline_ids == expected_ids
    assert baseline["completed_count"] == baseline["case_count"] == 50
    assert baseline["selected_exact_count"] == baseline["candidates_exact_count"] == 30

    baseline_misses = {item["case_id"] for item in baseline["cases"] if not item["selected_exact"]}
    validation_ids = {item["case_id"] for item in validation["cases"]}
    controls = {"vp-012", "vp-014", "vp-029"}
    assert validation_ids == baseline_misses | controls
    assert validation["completed_count"] == validation["case_count"] == 23
    assert validation["selected_exact_count"] == validation["candidates_exact_count"] == 9
    assert all(
        next(item for item in validation["cases"] if item["case_id"] == case_id)[
            "selected_exact"
        ]
        for case_id in controls
    )

    assert judge_source["completed_count"] == judge_source["case_count"] == 50
    assert judge_source["selected_exact_count"] == 34
    assert judge_source["candidates_exact_count"] == 36
    assert judge_source["traces_included"] is True

    for bundle in (baseline, validation):
        for record in bundle["cases"]:
            assert isinstance(record["selected_exact"], bool)
            assert isinstance(record["candidates_exact"], bool)
            assert not {"success", "reward"} & record.keys()
            if "selected_exact_success" in record:
                assert record["selected_exact_success"] == record["selected_exact"]
            if "exact_success" in record:
                assert record["exact_success"] == record["candidates_exact"]


def test_training_traces_are_readable_jsonl() -> None:
    for path in TRAINING.glob("*/attempts/*/codex-events.jsonl.gz"):
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                json.loads(line)
