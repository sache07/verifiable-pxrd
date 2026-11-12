"""Fast release-tool tests; no model, GSAS-II or network calls."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from import_experimental_track import (  # noqa: E402
    Sanitizer,
    copy_sanitized,
    strip_trace,
    walk_files,
)
from prepare_multiphase_release import export_attempt  # noqa: E402


def test_sanitizer_preserves_scientific_values_and_removes_keys():
    s = Sanitizer({})
    text = "Rwp=7.12 Sr2WO5 " + "sk-proj-" + "a" * 32
    assert s.text(text) == "Rwp=7.12 Sr2WO5 <REDACTED_API_KEY>"
    assert strip_trace({"thread_id": "private", "score": 7.12, "encrypted_content": "opaque"}) == {
        "score": 7.12,
        "encrypted_content": "<OMITTED_ENCRYPTED_REASONING>",
    }


def test_credentials_not_walked(tmp_path):
    (tmp_path / ".aws").mkdir()
    (tmp_path / ".aws/credentials").write_text("secret")
    (tmp_path / "auth.json").write_text("secret")
    (tmp_path / "result.json").write_text("{}")
    assert [p.name for p in walk_files(tmp_path)] == ["result.json"]


def test_archived_gitignore_cannot_hide_evidence(tmp_path):
    source = tmp_path / ".gitignore"
    source.write_text("STATE.md\ndrafts/\n")
    dest = tmp_path / "results/experimental-evolution/campaign/evolve/.gitignore"
    copy_sanitized(source, dest, Sanitizer({}))
    assert not dest.exists()
    assert dest.with_name(".gitignore.source").read_bytes() == source.read_bytes()


def test_restored_source_does_not_silently_complete_missing_bundle(tmp_path):
    source = tmp_path / "source"
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    record = {"evidence_status": "assessment_only_source_attempt_unavailable"}
    marker = bundle / "attempt.json"
    marker.write_text(json.dumps(record))
    assert export_attempt(source, bundle, {}, None, Sanitizer({}), condition="test") == record
    source.mkdir()
    with pytest.raises(RuntimeError, match="new recovery bundle"):
        export_attempt(source, bundle, {}, None, Sanitizer({}), condition="test")
    assert json.loads(marker.read_text()) == record


def test_aggregation_is_by_measurement():
    spec = importlib.util.spec_from_file_location(
        "release_reproduction", ROOT / "experiments/experimental-evolution/analysis/reproduce.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = [
        dict(
            case=f"case-{case:03}", replicate=rep, replay_interior_rwp=float(case + rep), minutes=10
        )
        for case in range(1, 16)
        for rep in range(1, 4)
    ]
    stats = module.summarize(rows)
    assert stats["mean_rwp"] == 10
    assert stats["mean_best_of_three_rwp"] == 9
    assert module.recovered({"phases": [{"target_matches": {"Sr2WO5": True}}]})
    assert not module.recovered({"phases": []})
