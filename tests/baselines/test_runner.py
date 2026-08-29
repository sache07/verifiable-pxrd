import json
from pathlib import Path

import pytest

from verifiable_pxrd.baselines.runner import load_runner_options

BASELINES = Path(__file__).parents[2] / "baselines"


def test_runner_loads_paper_condition_defaults(tmp_path: Path) -> None:
    adapter = tmp_path / "adapter.py"
    metadata = tmp_path / "baseline.json"
    metadata.write_text(
        json.dumps({"runner_options": {"composition_mode": "full-cell-oracle"}}),
        encoding="utf-8",
    )
    assert load_runner_options(adapter) == {"composition_mode": "full-cell-oracle"}


def test_runner_rejects_malformed_options(tmp_path: Path) -> None:
    adapter = tmp_path / "adapter.py"
    (tmp_path / "baseline.json").write_text(
        json.dumps({"runner_options": "full-cell-oracle"}), encoding="utf-8"
    )
    with pytest.raises(RuntimeError, match="runner_options must be an object"):
        load_runner_options(adapter)


def test_framework_runners_default_to_the_paper_conditions() -> None:
    decifer = load_runner_options(BASELINES / "decifer" / "adapter.py")
    realpxrd = load_runner_options(BASELINES / "realpxrd-solver" / "adapter.py")
    pxrdgen = load_runner_options(BASELINES / "pxrdgen" / "adapter.py")

    assert decifer["composition_mode"] == "full-cell-oracle"
    assert realpxrd["input_mode"] == "lattice-free-primitive-formula-oracle"
    assert "input_mode" not in pxrdgen
