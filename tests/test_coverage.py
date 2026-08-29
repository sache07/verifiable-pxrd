import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

from pymatgen.core import Lattice, Structure

from verifiable_pxrd.benchmark import Problem
from verifiable_pxrd.condition import load_condition
from verifiable_pxrd.coverage import (
    _materialize_submission,
    _render_prompt,
    _run_end_to_end_attempt,
    _validate_decision,
    evaluate_coverage_run,
)

ROOT = Path(__file__).resolve().parents[1]


def write_structure(path: Path, species: list[str]) -> None:
    coordinates = [[0, 0, 0], [0.5, 0.5, 0.5]][: len(species)]
    Structure(Lattice.cubic(4), species, coordinates).to(filename=str(path), fmt="cif")


def test_coverage_prompt_keeps_decision_object_literal(tmp_path: Path) -> None:
    prompt = tmp_path / "prompt.md"
    prompt.write_text(
        "Composition: {formula}\nSubmitted:\n{submitted_cifs}\n"
        '{ "decision": "stop|continue", "reason": "..." }\n',
        encoding="utf-8",
    )
    first_pass = tmp_path / "first-pass"
    (first_pass / "submitted").mkdir(parents=True)
    write_structure(first_pass / "submitted/selected.cif", ["Na", "Cl"])
    problem = Problem(
        problem_id="case",
        formula="NaCl",
        pattern=tmp_path / "pattern.csv",
        reference=tmp_path / "reference.cif",
        record=tmp_path / "problem.json",
    )
    rendered = _render_prompt(SimpleNamespace(prompt=prompt), problem, first_pass)  # type: ignore[arg-type]
    assert "Composition: NaCl" in rendered
    assert str(first_pass / "submitted/selected.cif") in rendered
    assert '{ "decision": "stop|continue", "reason": "..." }' in rendered


def test_materialized_submission_records_first_pass_provenance(tmp_path: Path) -> None:
    attempt = tmp_path / "attempt"
    (attempt / "first-pass/submitted").mkdir(parents=True)
    (attempt / "workspace").mkdir()
    write_structure(attempt / "first-pass/submitted/selected.cif", ["Na", "Cl"])
    manifest = _materialize_submission(
        attempt,
        {"decision": "stop", "reason": "supported", "proposed_branch": None},
    )
    assert manifest["candidates"][0]["origin"] == "first-pass-byte-identical"
    assert (attempt / "submission/selected.cif").is_file()


def test_decision_accepts_open_continuation_plan(tmp_path: Path) -> None:
    path = tmp_path / "decision.json"
    path.write_text(
        json.dumps(
            {
                "decision": "continue",
                "reason": "more work is warranted",
                "continuation_plan": "Reassess the evidence and pursue the best lead.",
            }
        ),
        encoding="utf-8",
    )
    assert _validate_decision(path)["continuation_plan"].startswith("Reassess")


def test_decision_requires_one_continuation_field(tmp_path: Path) -> None:
    path = tmp_path / "decision.json"
    path.write_text(
        json.dumps(
            {
                "decision": "continue",
                "reason": "ambiguous",
                "proposed_branch": "ordering",
                "continuation_plan": "try another route",
            }
        ),
        encoding="utf-8",
    )
    try:
        _validate_decision(path)
    except ValueError as error:
        assert "exactly one continuation field" in str(error)
    else:
        raise AssertionError("ambiguous continuation schema was accepted")


def test_coverage_evaluation_separates_selected_and_alternative(tmp_path: Path) -> None:
    run = tmp_path / "run"
    attempt = run / "attempts/case"
    for directory in (
        attempt / "control",
        attempt / "first-pass/submitted",
        attempt / "submission",
        attempt / "run",
    ):
        directory.mkdir(parents=True, exist_ok=True)
    write_structure(attempt / "control/reference.cif", ["Na", "Cl"])
    write_structure(attempt / "first-pass/submitted/selected.cif", ["Na", "F"])
    write_structure(attempt / "submission/selected.cif", ["Na", "F"])
    write_structure(attempt / "submission/alternative-1.cif", ["Na", "Cl"])
    (attempt / "control/assignment.json").write_text(
        json.dumps({"problem_id": "case", "reference": "reference.cif"}), encoding="utf-8"
    )
    (attempt / "decision.json").write_text(
        json.dumps(
            {"decision": "continue", "reason": "ambiguous", "proposed_branch": "ordering"}
        ),
        encoding="utf-8",
    )
    summary = evaluate_coverage_run(run)
    assert summary["final_selected_exact"] == 0
    assert summary["final_alternative_exact"] == 1
    assert summary["final_declared_exact"] == 1
    assert summary["alternative_only_exact"] == 1
    assert summary["selected_only_exact"] == 0
    assert summary["selected_and_alternative_exact"] == 0
    assert summary["recoveries"] == 1
    assert summary["regressions"] == 0


def test_end_to_end_attempt_runs_fresh_solve_then_review(monkeypatch, tmp_path: Path) -> None:
    pattern = tmp_path / "pattern.csv"
    pattern.write_text("2theta,intensity\n10,100\n", encoding="utf-8")
    reference = tmp_path / "reference.cif"
    write_structure(reference, ["Na", "Cl"])
    problem = Problem(
        problem_id="case",
        formula="NaCl",
        pattern=pattern,
        reference=reference,
        record=tmp_path / "problem.json",
    )
    review_prompt = tmp_path / "review.md"
    review_prompt.write_text("Review the completed solve for {formula}.\n", encoding="utf-8")
    condition = replace(
        load_condition(ROOT / "experiments/agent-adaptation/conditions/adapted-codex.toml"),
        auth_home=tmp_path / "empty-auth",
        review_prompt=review_prompt,
        timeout_seconds=7200,
        first_pass_timeout_seconds=3600,
        path_entries=(),
        read_paths=(),
        optional_read_paths=(),
        deny_paths=(),
    )
    calls: list[tuple[Path, float]] = []

    def fake_run_agent(
        condition,
        workspace,
        codex_home,
        run_dir,
        prompt,
        token,
        timeout_seconds,
    ):
        del condition, codex_home, prompt, token
        calls.append((workspace, timeout_seconds))
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "codex-events.jsonl").write_text("{}\n", encoding="utf-8")
        (run_dir / "final-answer.md").write_text("done\n", encoding="utf-8")
        if "first-pass" in workspace.parts:
            write_structure(workspace / "selected.cif", ["Na", "Cl"])
        else:
            (workspace / "decision.json").write_text(
                json.dumps(
                    {"decision": "stop", "reason": "established", "proposed_branch": None}
                ),
                encoding="utf-8",
            )
        return {
            "timed_out": False,
            "returncode": 0,
            "elapsed_seconds": 0.01,
            "timeout_seconds": timeout_seconds,
        }

    monkeypatch.setattr("verifiable_pxrd.coverage._run_agent", fake_run_agent)
    run_root = tmp_path / "run"
    (run_root / "attempts").mkdir(parents=True)
    updates: list[dict] = []
    result = _run_end_to_end_attempt(run_root, condition, problem, updates.append)
    attempt = run_root / "attempts/case"
    assert result["valid_output"] is True
    assert [path for path, _ in calls] == [
        attempt / "first-pass/workspace",
        attempt / "workspace",
    ]
    assert calls[0][1] <= 3600
    assert calls[1][1] > 3600
    assert (attempt / "first-pass/submitted/selected.cif").is_file()
    assert (attempt / "submission/selected.cif").is_file()
    review_config = (attempt / "codex-home/config.toml").read_text(encoding="utf-8")
    assert str(attempt / "first-pass") in review_config
    assert str(attempt / "control") not in review_config
    assert [update["stage"] for update in updates] == ["first-pass", "review", "review"]
