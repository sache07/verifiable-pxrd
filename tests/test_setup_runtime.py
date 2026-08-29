from __future__ import annotations

import os
import sys
from pathlib import Path
from types import SimpleNamespace

from verifiable_pxrd.continual import _activate_runtime_environment
from verifiable_pxrd.setup_runtime import _write_environment, setup_runtime

ROOT = Path(__file__).resolve().parents[1]


def test_setup_runtime_dry_run_is_portable_and_omits_dicvol(tmp_path: Path) -> None:
    result = setup_runtime(
        tmp_path / "runtime",
        codex=Path(sys.executable),
        dry_run=True,
    )

    assert result["valid"]
    assert result["dicvol_included"] is False
    assert set(result["components"]) == {"matsci", "gsasii"}
    assert result["portable_condition"].endswith("conditions/portable/gsas-codex.toml")
    assert not (tmp_path / "runtime").exists()


def test_generated_environment_is_sourceable_and_training_loader_accepts_it(
    monkeypatch, tmp_path: Path
) -> None:
    codex = tmp_path / "Codex App/codex"
    matsci = tmp_path / "Scientific Python"
    gsasii = tmp_path / "GSAS II"
    codex.parent.mkdir(parents=True, exist_ok=True)
    codex.touch()
    matsci.mkdir(parents=True)
    (gsasii / "venv").mkdir(parents=True)
    environment = tmp_path / "runtime.env"

    action = _write_environment(
        environment,
        codex=codex,
        matsci=matsci,
        gsasii=gsasii,
        cod_metadata=None,
        cod_cifs=None,
    )
    assert action == "created"
    assert _write_environment(
        environment,
        codex=codex,
        matsci=matsci,
        gsasii=gsasii,
        cod_metadata=None,
        cod_cifs=None,
    ) == "reused"

    for name in ("VPBENCH_CODEX", "VPBENCH_MATSCI_ENV", "VPBENCH_GSAS_ENV"):
        monkeypatch.delenv(name, raising=False)
    _activate_runtime_environment(SimpleNamespace(runtime_environment=environment))
    assert Path(os.environ["VPBENCH_CODEX"]) == codex.resolve()
    assert Path(os.environ["VPBENCH_MATSCI_ENV"]) == matsci.resolve()
    assert Path(os.environ["VPBENCH_GSAS_ENV"]) == (gsasii / "venv").resolve()


def test_portable_condition_has_gsas_without_dicvol() -> None:
    text = (
        ROOT
        / "experiments/agent-adaptation/conditions/portable/gsas-codex.toml"
    ).read_text(encoding="utf-8")
    assert "GSAS2_PYTHON" in text
    assert "DICVOL" not in text.upper()
