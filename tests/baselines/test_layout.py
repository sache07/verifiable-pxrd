import json
from pathlib import Path

BASELINES = Path(__file__).parents[2] / "baselines"
FRAMEWORKS = {
    "ab-pxrd-solver": "reported",
    "crystalyze": "reported",
    "decifer": "reported",
    "diffractgpt": "reported",
    "pxrdgen": "reported",
    "realpxrd-solver": "reported",
}
REQUIRED_FILES = {
    "README.md",
    "artifacts.lock.json",
    "baseline.json",
    "doctor.py",
    "make_targets.py",
    "prepare.py",
    "run.py",
}


def test_public_framework_folders_are_explicit() -> None:
    public_directories = {
        path.name
        for path in BASELINES.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name != "__pycache__"
    }
    assert public_directories == set(FRAMEWORKS)


def test_every_framework_has_the_common_reproduction_surface() -> None:
    for directory, status in FRAMEWORKS.items():
        root = BASELINES / directory
        assert {path.name for path in root.iterdir() if path.is_file()} >= REQUIRED_FILES

        metadata = json.loads((root / "baseline.json").read_text())
        assert metadata["schema_version"] == "1"
        assert metadata["status"] == status
        assert metadata["target_builder"] == "make_targets.py"
        assert metadata["target_output"] == "targets/{corpus-directory}"
        assert (root / "targets" / "README.md").is_file()
        assert metadata["runner"] == "run.py"
        assert metadata["artifact_lock"] == "artifacts.lock.json"
        assert max(metadata["reported_k"]) <= metadata["generated_candidates"]
        assert metadata["runner_options"]["support_policy"] in {
            "manifest",
            "common-envelope",
            "require-all",
        }
        assert isinstance(metadata["runner_options"]["seed_base"], int)
        json.loads((root / metadata["artifact_lock"]).read_text())


def test_agent_result_is_not_presented_as_a_baseline() -> None:
    assert not any("gpt-5.6" in path.name.lower() for path in BASELINES.iterdir())
