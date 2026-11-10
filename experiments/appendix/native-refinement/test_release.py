"""Release packaging stays method-scoped and preserves runner snapshots."""
import json
import subprocess
import sys
from pathlib import Path

from common import digest, fingerprint

HERE = Path(__file__).resolve().parent


def test_method_filter_and_multiple_runner_snapshots(tmp_path):
    inputs, run, output = (tmp_path / name for name in ("inputs", "run", "output"))
    inputs.mkdir()
    ids = ["crystalyze/corpus/case/01", "crystalyze/corpus/case/02", "pxrdgen/corpus/case/01"]
    (inputs / "manifest.json").write_text(json.dumps({"pilot": False}))
    (inputs / "local-index.json").write_text(json.dumps([{"id": name} for name in ids]))
    (inputs / "missing.json").write_text(json.dumps([{"id": "pxrdgen/corpus/missing/01"}]))
    snapshots = []
    for number, identifier in enumerate(ids):
        directory = run / "candidates" / identifier
        directory.mkdir(parents=True)
        snapshot = tmp_path / f"runner-{number}"
        snapshot.mkdir()
        source = f"# frozen runner {number}\n".encode()
        (snapshot / "worker.py").write_bytes(source)
        source_hash = fingerprint({"worker.py": digest(source)})
        (directory / "result.json").write_text(json.dumps({"id": identifier, "code_sha256": source_hash}))
        (directory / "input.cif").write_text("input")
        (directory / "stage-1.cif").write_text("stage one")
        (directory / "stage-1-profile.npz").write_bytes(b"not needed in compact export")
        if number < 2:
            snapshots.extend(["--source-snapshot", str(snapshot)])
    subprocess.run([sys.executable, str(HERE / "export_results.py"),
                    "--inputs", str(inputs), "--runs", str(run), "--output", str(output),
                    "--method", "crystalyze", "--omit-profile-arrays", *snapshots], check=True)
    assert len(list((output / "candidates").rglob("result.json"))) == 2
    assert not (output / "candidates/pxrdgen").exists()
    assert not list(output.rglob("*.npz"))
    assert len(list((output / "runners").glob("*.tar.gz"))) == 2
    assert len(json.loads((output / "inputs/local-index.json").read_text())) == 2
    assert json.loads((output / "inputs/missing.json").read_text()) == []
