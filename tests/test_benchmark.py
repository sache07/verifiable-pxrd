from pathlib import Path

from verifiable_pxrd.benchmark import load_problem_collection, validate_corpus

ROOT = Path(__file__).resolve().parents[1]


def test_benchmark_tree_has_one_canonical_root() -> None:
    assert (ROOT / "pxrd-bench").is_dir()
    assert not (ROOT / "benchmarks").exists()


def test_locked_corpora_validate() -> None:
    for name in ("pXRD-100", "pXRD-ood"):
        result = validate_corpus(ROOT / "pxrd-bench" / name)
        assert result["valid"], result["failures"]
        assert result["source_cases"] == result["pattern_cases"] == 100


def test_public_panels_load() -> None:
    paths = {
        ROOT / "pxrd-bench/panels/full-200.json": 200,
        ROOT / "pxrd-bench/panels/inference-scaling-20/manifest.json": 20,
        ROOT / "experiments/agent-adaptation/curriculum/train-50/manifest.json": 50,
    }
    for path, expected in paths.items():
        problems = load_problem_collection(path)
        assert len(problems) == expected
        assert len({problem.problem_id for problem in problems}) == expected
