import runpy
from pathlib import Path

from verifiable_pxrd.benchmark import Problem
from verifiable_pxrd.llm_output import cif_blocks, materialize_cifs

RUNNER = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_llm_only.py"))
archive_request = RUNNER["archive_request"]
response_payload = RUNNER["response_payload"]
serialize_request = RUNNER["serialize_request"]
summarize = RUNNER["summarize"]
prompt_for = RUNNER["prompt_for"]


def test_named_cif_blocks_are_materialized(tmp_path) -> None:
    text = """
`selected.cif`
```cif
data_primary
_cell_length_a 4
```

`alternative-2.cif`
```cif
data_alternative
_cell_length_a 5
```
"""
    assert [name for name, _ in cif_blocks(text)] == ["selected.cif", "alternative-2.cif"]
    assert materialize_cifs(text, tmp_path) == ["selected.cif", "alternative-2.cif"]
    assert (tmp_path / "selected.cif").read_text().startswith("data_primary")


def test_unlabelled_first_block_becomes_selected(tmp_path) -> None:
    text = """```cif
data_one
_cell_length_a 4
```
```cif
data_two
_cell_length_a 5
```"""
    assert materialize_cifs(text, tmp_path) == ["selected.cif", "alternative-1.cif"]


def test_current_template_overrides_stored_problem_prompt(tmp_path) -> None:
    record = tmp_path / "problem.json"
    record.write_text("{}", encoding="utf-8")
    stored = tmp_path / "problem_input/prompt.md"
    stored.parent.mkdir()
    stored.write_text("obsolete prompt", encoding="utf-8")
    problem = Problem(
        problem_id="canary",
        formula="NaCl",
        pattern=tmp_path / "pattern.csv",
        reference=tmp_path / "reference.cif",
        record=record,
    )
    template = "Solve {formula} at {wavelength} angstrom ({radiation})."
    assert prompt_for(problem, template) == "Solve NaCl at 1.5406 angstrom (Cu Kalpha1)."


def test_archived_request_is_the_literal_serialized_api_payload(tmp_path) -> None:
    attempt = tmp_path / "attempt"
    (attempt / "input").mkdir(parents=True)
    (attempt / "run").mkdir()
    pattern = "two_theta,intensity\n5.00,0.25\n5.01,0.50\n"
    (attempt / "input/pattern.csv").write_text(pattern, encoding="utf-8")
    condition = {
        "model": "gpt-5.6-sol",
        "reasoning_effort": "high",
        "input_transport": "inline-text",
        "background": True,
        "store": True,
        "max_output_tokens": 65536,
    }
    payload = response_payload(attempt, "Solve this structure.", condition)
    digest = archive_request(attempt / "run", payload)

    request = attempt / "run/request.json"
    assert request.read_bytes() == serialize_request(payload)
    assert digest
    assert payload["tools"] == []
    assert payload["input"][0]["content"][1]["text"].endswith(f"```csv\n{pattern}```")


def test_summary_reports_primary_alternative_parseability_and_usage() -> None:
    summary = summarize(
        {
            "a": {
                "status": "archived",
                "selected_exact": False,
                "candidates_exact": True,
                "selected_parseable": True,
                "any_candidate_parseable": True,
                "candidate_count": 2,
                "parseable_candidate_count": 2,
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 4,
                    "output_tokens_details": {"reasoning_tokens": 3},
                },
            },
            "b": {
                "status": "archived",
                "selected_exact": True,
                "candidates_exact": True,
                "selected_parseable": True,
                "any_candidate_parseable": True,
                "candidate_count": 1,
                "parseable_candidate_count": 1,
                "usage": {"input_tokens": 9, "output_tokens": 2},
            },
        }
    )
    assert summary["selected_exact"] == 1
    assert summary["candidates_exact"] == 2
    assert summary["parseable_candidate_file_rate"] == 1.0
    assert summary["usage"] == {
        "input_tokens": 19,
        "output_tokens": 6,
        "reasoning_tokens": 3,
        "total_tokens": 25,
    }
