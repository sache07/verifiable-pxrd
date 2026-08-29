import json
from pathlib import Path

from verifiable_pxrd.benchmark import load_problem_collection
from verifiable_pxrd.continual import (
    _write_panel,
    import_training_run,
    launch_training_baseline,
    launch_training_wave,
    load_harness_config,
    select_baseline_ids,
    select_wave_ids,
    training_status,
)

ROOT = Path(__file__).resolve().parents[1]


def _config(tmp_path: Path) -> Path:
    path = tmp_path / "harness.toml"
    path.write_text(
        "\n".join(
            (
                "schema_version = 1",
                'id = "test-train"',
                f'curriculum = "{ROOT / "experiments/agent-adaptation/curriculum/train-50/manifest.json"}"',
                f'order = "{ROOT / "experiments/agent-adaptation/curriculum/train-50/problem-order.txt"}"',
                f'condition = "{ROOT / "experiments/agent-adaptation/conditions/adapted-codex.toml"}"',
                f'baseline_condition = "{ROOT / "experiments/agent-adaptation/conditions/pxrd-codex.toml"}"',
                f'capability = "{ROOT / "experiments/agent-adaptation/working-package"}"',
                'runtime_environment = ".state/runtime.env"',
                'state_dir = ".state"',
                'run_root = ".runs"',
                "bootstrap_size = 20",
                "wave_size = 4",
                "parallel = 4",
                "",
            )
        ),
        encoding="utf-8",
    )
    return path


def test_wave_panel_is_self_contained(tmp_path: Path) -> None:
    config = load_harness_config(_config(tmp_path))
    panel = tmp_path / ".state/panels/test.json"
    _write_panel(config, ["vp-012", "vp-023"], panel)
    problems = load_problem_collection(panel)
    assert [problem.problem_id for problem in problems] == ["vp-012", "vp-023"]
    assert all(problem.pattern.is_relative_to(panel.parent) for problem in problems)
    assert all(problem.reference.is_relative_to(panel.parent) for problem in problems)


def test_wave_panels_can_restage_the_same_problem(tmp_path: Path) -> None:
    config = load_harness_config(_config(tmp_path))
    first = tmp_path / ".state/panels/first.json"
    second = tmp_path / ".state/panels/second.json"

    _write_panel(config, ["vp-012"], first)
    _write_panel(config, ["vp-012"], second)

    assert load_problem_collection(first)[0].pattern.read_bytes() == (
        load_problem_collection(second)[0].pattern.read_bytes()
    )


def test_dry_run_wave_records_staged_attempts(tmp_path: Path, monkeypatch) -> None:
    config_path = _config(tmp_path)
    monkeypatch.setattr(
        "verifiable_pxrd.continual.harness_doctor",
        lambda _: {"valid": True, "failures": []},
    )
    monkeypatch.setattr(
        "verifiable_pxrd.continual.run_panel",
        lambda *args: {
            "staged": 1,
            "attempts": [{"attempt_id": "vp-012-r1", "status": "staged"}],
        },
    )

    result = launch_training_wave(
        config_path,
        problem_ids=["vp-012"],
        next_count=None,
        parallel=1,
        label="dry-run",
        dry_run=True,
    )

    assert result["wave"]["status"] == "staged"
    assert result["wave"]["attempts"] == 1


def test_dry_run_baseline_uses_no_capability_condition(tmp_path: Path, monkeypatch) -> None:
    config_path = _config(tmp_path)
    calls = []
    monkeypatch.setattr(
        "verifiable_pxrd.continual.harness_doctor",
        lambda _: {"valid": True, "failures": []},
    )

    def fake_run_panel(*args):
        calls.append(args)
        return {"staged": 1, "attempts": [{"attempt_id": "vp-012-r1", "status": "staged"}]}

    monkeypatch.setattr("verifiable_pxrd.continual.run_panel", fake_run_panel)
    result = launch_training_baseline(
        config_path,
        problem_ids=["vp-012"],
        next_count=None,
        all_missing=False,
        parallel=1,
        label="baseline-dry-run",
        dry_run=True,
    )

    assert result["wave"]["role"] == "baseline"
    assert Path(calls[0][0]).name == "pxrd-codex.toml"


def test_imported_bootstrap_is_compact_and_advances_order(tmp_path: Path) -> None:
    config_path = _config(tmp_path)
    source = tmp_path / "source"
    attempt = source / "attempts/001-vp-012"
    (attempt / "run").mkdir(parents=True)
    (attempt / "workspace").mkdir()
    (attempt / "codex-home").mkdir()
    (attempt / "assignment.json").write_text(
        json.dumps({"attempt_id": "vp-012-r1", "case_id": "vp-012"}),
        encoding="utf-8",
    )
    (attempt / "prompt.txt").write_text("solve it\n", encoding="utf-8")
    (attempt / "run/verifier-result.json").write_text(
        json.dumps({"selected_exact": True, "candidates_exact": True}), encoding="utf-8"
    )
    (attempt / "run/codex-events.jsonl").write_text("{}\n", encoding="utf-8")
    (attempt / "workspace/selected.cif").write_text("data_test\n", encoding="utf-8")
    (attempt / "codex-home/state.sqlite").write_text("private state", encoding="utf-8")

    result = import_training_run(config_path, source, "bootstrap")
    assert result["attempts"] == result["exact"] == 1
    assert result["selected_exact"] == result["candidates_exact"] == 1
    imported = tmp_path / ".runs/imports/bootstrap/attempts/001-vp-012"
    assert (imported / "workspace/selected.cif").is_file()
    assert (imported / "control/reference.cif").is_file()
    assert not (imported / "codex-home").exists()

    status = training_status(config_path)
    assert status["baseline"]["attempts"] == status["baseline"]["exact"] == 1
    assert status["baseline"]["selected_exact"] == 1
    assert status["baseline"]["candidates_exact"] == 1
    assert status["baseline"]["problems"] == 1
    assert status["next_unseen"][0] == "vp-023"
    assert select_baseline_ids(load_harness_config(config_path), all_missing=True)[0] == "vp-023"
    assert select_wave_ids(load_harness_config(config_path), next_count=2) == [
        "vp-023",
        "vp-038",
    ]
