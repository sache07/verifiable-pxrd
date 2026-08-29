import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_migrated_result_counts_are_self_consistent() -> None:
    roots = (
        ROOT / "results/agent-adaptation",
        ROOT / "results/inference-scaling",
    )
    for path in (path for root in roots for path in root.rglob("bundle.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if "cumulative_candidates_exact_count" in payload:
            exact = [item for item in payload["cases"] if item["cumulative_candidates_exact"]]
            assert payload["cumulative_candidates_exact_count"] == len(exact)
        elif "candidates_exact_count" in payload:
            selected = [item for item in payload["cases"] if bool(item["selected_exact"])]
            candidates = [item for item in payload["cases"] if bool(item["candidates_exact"])]
            assert payload["selected_exact_count"] == len(selected)
            assert payload["selected_exact_case_ids"] == [item["case_id"] for item in selected]
            assert payload["candidates_exact_count"] == len(candidates)
            assert payload["candidates_exact_case_ids"] == [item["case_id"] for item in candidates]
            assert {item["case_id"] for item in selected} <= {
                item["case_id"] for item in candidates
            }
        else:
            exact = [item for item in payload["cases"] if bool(item.get("exact_success"))]
            assert payload["exact_count"] == len(exact)
            assert payload["exact_case_ids"] == [item["case_id"] for item in exact]


def test_pxrd_codex_monkey_counts_and_unions() -> None:
    expected = {
        "luna-monkeys/pxrd-codex-luna-max-api-reps1-8": (
            [9, 7, 5, 6, 5, 6, 6, 7],
            12,
        ),
        "sol-monkeys/pxrd-codex-sol-high-api-reps1-8": (
            [10, 11, 9, 9, 10, 11, 12, 12],
            15,
        ),
    }
    for relative, (counts, expected_union) in expected.items():
        bundles = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((ROOT / "results/inference-scaling" / relative).glob("replicate-*/bundle.json"))
        ]
        assert [bundle["exact_count"] for bundle in bundles] == counts
        exact_union = {
            case["case_id"]
            for bundle in bundles
            for case in bundle["cases"]
            if case["exact_success"]
        }
        assert len(exact_union) == expected_union


def test_pxrd_environment_full_benchmark_counts() -> None:
    bundle = json.loads(
        (
            ROOT
            / "results/agent-adaptation/pxrd-codex"
            / "full-200-api-sol-high-r1/bundle.json"
        ).read_text(encoding="utf-8")
    )
    assert bundle["case_count"] == 200
    assert bundle["completed_count"] == 200
    assert bundle["selected_exact_count"] == 114
    assert bundle["exact_count"] == 117

    pxrd100 = [item for item in bundle["cases"] if item["case_id"].startswith("pxrd100")]
    pxrdood = [item for item in bundle["cases"] if item["case_id"].startswith("pxrdood")]
    assert sum(bool(item["selected_exact_success"]) for item in pxrd100) == 58
    assert sum(bool(item["exact_success"]) for item in pxrd100) == 59
    assert sum(bool(item["selected_exact_success"]) for item in pxrdood) == 56
    assert sum(bool(item["exact_success"]) for item in pxrdood) == 58


def test_adapted_environment_full_benchmark_counts() -> None:
    bundle = json.loads(
        (
            ROOT
            / "results/agent-adaptation/adapted-codex"
            / "full-200-chatgpt-sol-high-r1/bundle.json"
        ).read_text(encoding="utf-8")
    )
    assert bundle["case_count"] == 200
    assert bundle["selected_exact_count"] == 138
    assert bundle["candidates_exact_count"] == 141

    pxrd100 = [item for item in bundle["cases"] if item["case_id"].startswith("pxrd100")]
    pxrdood = [item for item in bundle["cases"] if item["case_id"].startswith("pxrdood")]
    assert sum(bool(item["selected_exact"]) for item in pxrd100) == 77
    assert sum(bool(item["candidates_exact"]) for item in pxrd100) == 77
    assert sum(bool(item["selected_exact"]) for item in pxrdood) == 61
    assert sum(bool(item["candidates_exact"]) for item in pxrdood) == 64


def test_full_benchmark_verifier_counts() -> None:
    root = (
        ROOT
        / "results/inference-scaling/verifier-200/adapted-codex-r1"
    )
    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    assert summary["case_count"] == 200
    assert summary["candidate_set_exact_count"] == 141
    assert summary["candidate_set_miss_count"] == 59
    expected = {
        "seed": (126, 1, 73),
        "judge_v1": (155, 7, 38),
        "rwp-1-false-stop": (127, 1, 72),
        "rwp-7-false-stops": (149, 7, 44),
    }
    for name, values in expected.items():
        metrics = summary["metrics"][name]
        assert (
            metrics["correct"],
            metrics["false_stops"],
            metrics["false_continues"],
        ) == values
    assert len(list((root / "attempts").glob("*/seed/decision.json"))) == 200
    assert len(list((root / "attempts").glob("*/judge-v1/decision.json"))) == 200
    assert len(list((root / "attempts").rglob("codex-events.jsonl.gz"))) == 401


def test_matsci_environment_full_benchmark_counts() -> None:
    bundle = json.loads(
        (
            ROOT
            / "results/agent-adaptation/matsci-codex"
            / "full-200-r1/bundle.json"
        ).read_text(encoding="utf-8")
    )
    assert bundle["case_count"] == 200
    assert bundle["completed_count"] == 197
    assert bundle["selected_exact_count"] == 104
    assert bundle["candidates_exact_count"] == 105
    assert sum(item["status"] == "blocked" for item in bundle["cases"]) == 3
    attempts = (
        ROOT
        / "results/agent-adaptation/matsci-codex"
        / "full-200-r1/attempts"
    )
    assert len(list(attempts.iterdir())) == 200


def test_adapted_sol_inference_scaling_counts() -> None:
    root = (
        ROOT
        / "results/inference-scaling/sol-monkeys"
        / "adapted-codex-sol-high-api-reps1-8"
    )
    bundles = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(root.glob("replicate-*/bundle.json"))
    ]
    assert len(bundles) == 8
    assert [bundle["selected_exact_count"] for bundle in bundles] == [
        13,
        13,
        13,
        14,
        15,
        13,
        14,
        12,
    ]
    assert [bundle["candidates_exact_count"] for bundle in bundles] == [
        13,
        13,
        14,
        14,
        16,
        13,
        14,
        13,
    ]
    for metric in ("selected_exact", "candidates_exact"):
        union = {
            case["case_id"]
            for bundle in bundles
            for case in bundle["cases"]
            if case[metric]
        }
        assert len(union) == 18


def test_adapted_luna_inference_scaling_counts() -> None:
    root = (
        ROOT
        / "results/inference-scaling/luna-monkeys"
        / "adapted-codex-luna-max-api-reps1-8"
    )
    bundles = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(root.glob("replicate-*/bundle.json"))
    ]
    assert len(bundles) == 8
    assert [bundle["selected_exact_count"] for bundle in bundles] == [
        6,
        9,
        6,
        8,
        8,
        9,
        9,
        9,
    ]
    assert [bundle["candidates_exact_count"] for bundle in bundles] == [
        8,
        9,
        6,
        9,
        9,
        9,
        9,
        9,
    ]
    assert sum(
        bool(case.get("timed_out"))
        for bundle in bundles
        for case in bundle["cases"]
    ) == 47
    for metric in ("selected_exact", "candidates_exact"):
        union = {
            case["case_id"]
            for bundle in bundles
            for case in bundle["cases"]
            if case[metric]
        }
        assert len(union) == 14
