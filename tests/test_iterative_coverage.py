import json
from dataclasses import replace
from pathlib import Path

from pymatgen.core import Lattice, Structure

from verifiable_pxrd.benchmark import Problem
from verifiable_pxrd.condition import load_condition
from verifiable_pxrd.coverage import FirstPassAttempt
from verifiable_pxrd.iterative_coverage import (
    _run_chain_attempt,
    evaluate_iterative_coverage,
    render_continuation_prompt,
)

ROOT = Path(__file__).resolve().parents[1]


def write_structure(path: Path, species: list[str]) -> None:
    coordinates = [[0, 0, 0], [0.5, 0.5, 0.5]][: len(species)]
    Structure(Lattice.cubic(4), species, coordinates).to(filename=str(path), fmt="cif")


def condition(tmp_path: Path):
    return replace(
        load_condition(ROOT / "experiments/agent-adaptation/conditions/adapted-codex.toml"),
        auth_home=tmp_path / "empty-auth",
        path_entries=(),
        read_paths=(),
        optional_read_paths=(),
        deny_paths=(),
    )


def problem_and_source(tmp_path: Path) -> tuple[Problem, FirstPassAttempt]:
    pattern = tmp_path / "pattern.csv"
    pattern.write_text("2theta,intensity\n10,100\n", encoding="utf-8")
    reference = tmp_path / "reference.cif"
    write_structure(reference, ["Na", "Cl"])
    source_root = tmp_path / "source"
    submission = source_root / "submission"
    submission.mkdir(parents=True)
    wrong = submission / "selected.cif"
    write_structure(wrong, ["Na", "F"])
    trace = source_root / "codex-events.jsonl"
    trace.write_text("{}\n", encoding="utf-8")
    final = source_root / "final-answer.md"
    final.write_text("first answer\n", encoding="utf-8")
    return (
        Problem("case", "NaCl", pattern, reference, tmp_path / "problem.json"),
        FirstPassAttempt("case", source_root, trace, final, (wrong,)),
    )


def test_continuation_prompt_points_to_blind_current_evidence(tmp_path: Path) -> None:
    active = condition(tmp_path)
    problem, _ = problem_and_source(tmp_path)
    stage = tmp_path / "stage"
    evidence = stage / "evidence"
    candidate = evidence / "first-pass-cifs/selected.cif"
    decision = evidence / "decision.json"
    prompt = render_continuation_prompt(
        "{capability_path}\n{formula}\n{pattern_path}\n{first_trace_path}\n"
        "{first_response_path}\n{first_pass_cifs}\n{decision_json_path}",
        active,
        problem,
        evidence,
        decision,
        (candidate,),
    )
    assert str(stage / "workspace/.vpbench-capability/SKILL.md") in prompt
    assert str(candidate) in prompt
    assert "reference.cif" not in prompt


def test_chain_alternates_fresh_judge_and_continuation(monkeypatch, tmp_path: Path) -> None:
    active = condition(tmp_path)
    problem, source = problem_and_source(tmp_path)
    calls: list[Path] = []

    def fake_run_agent(
        condition,
        workspace,
        codex_home,
        run_dir,
        prompt,
        token,
        timeout_seconds,
    ):
        del condition, codex_home, prompt, token, timeout_seconds
        calls.append(workspace)
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "codex-events.jsonl").write_text("{}\n", encoding="utf-8")
        (run_dir / "final-answer.md").write_text("done\n", encoding="utf-8")
        if "review-00" in workspace.parts:
            (workspace / "decision.json").write_text(
                json.dumps(
                    {
                        "decision": "continue",
                        "reason": "the submitted realization is incomplete",
                        "proposed_branch": "test a distinct ordering",
                    }
                ),
                encoding="utf-8",
            )
        elif "review-01" in workspace.parts:
            (workspace / "decision.json").write_text(
                json.dumps(
                    {
                        "decision": "stop",
                        "reason": "an explicit supported realization now exists",
                        "proposed_branch": None,
                    }
                ),
                encoding="utf-8",
            )
        else:
            write_structure(workspace / "selected.cif", ["Na", "Cl"])
        return {"timed_out": False, "returncode": 0, "elapsed_seconds": 0.01}

    monkeypatch.setattr("verifiable_pxrd.iterative_coverage._run_agent", fake_run_agent)
    run_root = tmp_path / "run"
    (run_root / "attempts").mkdir(parents=True)
    updates = []
    result = _run_chain_attempt(
        run_root,
        active,
        active,
        problem,
        source,
        "{formula}\n{pattern_path}\n{trace_path}\n{final_response_path}\n"
        "{submitted_cifs}\n{rwp_report_path}\n{judge_policy}",
        "Judge it.",
        "{capability_path}\n{formula}\n{pattern_path}\n{first_trace_path}\n"
        "{first_response_path}\n{first_pass_cifs}\n{decision_json_path}",
        7,
        60,
        60,
        updates.append,
    )
    attempt = run_root / "attempts/case"
    assert result["termination"] == "judge-stop"
    assert result["continuations"] == 1
    assert calls == [
        attempt / "rounds/review-00/workspace",
        attempt / "rounds/continuation-01/workspace",
        attempt / "rounds/review-01/workspace",
    ]
    assert (attempt / "submission/selected.cif").is_file()
    assert (attempt / "rounds/review-01/evidence/selected.cif").is_file()
    evaluation = evaluate_iterative_coverage(run_root)
    assert evaluation["initial_candidates_exact"] == 0
    assert evaluation["final_candidates_exact"] == 1
    assert evaluation["recoveries"] == 1
