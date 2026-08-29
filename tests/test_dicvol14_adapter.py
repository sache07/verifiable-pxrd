import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "experiments/agent-adaptation/artifacts/adapted-codex/package/bin/dicvol14-adapter"


def _backend(path: Path, exit_code: int = 0) -> Path:
    path.write_text(
        """#!/usr/bin/env python3
import sys
from pathlib import Path

source = Path(sys.stdin.readline().strip())
Path(source.stem + ".ind").write_text("index:" + source.read_text())
Path(source.stem + ".ucp").write_text("cells\\n")
print("native stdout")
print("native stderr", file=sys.stderr)
raise SystemExit(EXIT_CODE)
""".replace("EXIT_CODE", str(exit_code)),
        encoding="utf-8",
    )
    path.chmod(0o755)
    return path


def _command(backend: Path, output: Path) -> list[object]:
    return [
        sys.executable,
        ADAPTER,
        "--peak",
        "20.0",
        "--peak",
        "30.0",
        "--input-kind",
        "two-theta",
        "--wavelength",
        "1.5406",
        "--systems",
        "cubic,tetragonal",
        "--output-dir",
        output,
        "--backend",
        backend,
    ]


def test_help_does_not_require_a_backend() -> None:
    result = subprocess.run(
        [sys.executable, ADAPTER, "--help"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "explicit peak input" in result.stdout
    assert "does not extract peaks" in result.stdout


def test_adapter_generates_native_input_and_retains_outputs(tmp_path: Path) -> None:
    backend = _backend(tmp_path / "dicvol14")
    output = tmp_path / "result"
    result = subprocess.run(
        _command(backend, output),
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "native stdout" in result.stdout
    assert "native stderr" in result.stderr
    assert (output / "input.dat").read_text().splitlines()[1] == "2 2 1 1 0 0 0 0 /"
    assert (output / "input.ind").read_text().startswith("index:DICVOL14 adapter run")
    assert (output / "input.ucp").read_text() == "cells\n"

    record = json.loads((output / "provenance.json").read_text())
    assert record["status"] == "backend_completed"
    assert record["backend"]["path"] == str(backend)
    assert record["request"]["systems"] == ["cubic", "tetragonal"]


def test_adapter_returns_native_failure_status(tmp_path: Path) -> None:
    backend = _backend(tmp_path / "dicvol14", exit_code=7)
    output = tmp_path / "result"
    result = subprocess.run(
        _command(backend, output),
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 7
    record = json.loads((output / "provenance.json").read_text())
    assert record["status"] == "backend_error"
    assert record["backend"]["returncode"] == 7
