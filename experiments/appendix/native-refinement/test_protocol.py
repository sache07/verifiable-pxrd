import ast
import runpy
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PROTOCOL, REPO, digest, fingerprint, reservation_usd, time_limit, verify_task
from install_runtime import replace_once


def test_repository_root_after_relocation():
    assert REPO == Path(__file__).resolve().parents[3]
    assert (REPO / "results/appendix/native-refinement").is_dir()


def test_standalone_worker_root(tmp_path):
    source = Path(__file__).resolve().parent
    worker = tmp_path / "opt/refinement"
    worker.mkdir(parents=True)
    for name in ("common.py", "protocol.json"):
        (worker / name).write_bytes((source / name).read_bytes())
    assert runpy.run_path(str(worker / "common.py"))["REPO"] == Path("/")


def task():
    return {"id": "crystalyze/pxrd-100/case/01", "method": "crystalyze", "candidate_cif": "cif",
            "candidate_sha256": digest(b"cif"), "pattern_text": "pattern", "pattern_sha256": digest(b"pattern"),
            "protocol_sha256": fingerprint(PROTOCOL), "timeout_seconds": 3600}


def test_reference_fields_rejected():
    value = task()
    verify_task(value)
    value["reference_cif"] = "truth"
    with pytest.raises(ValueError):
        verify_task(value)


def test_changed_inputs_rejected():
    value = task()
    value["pattern_text"] += "changed"
    with pytest.raises(ValueError):
        verify_task(value)


def test_path_escape_rejected():
    value = task()
    value["id"] = "../../oops"
    with pytest.raises(ValueError):
        verify_task(value)


def test_reservation_covers_full_timeout_and_margin():
    assert reservation_usd(task()) > 3600 * (.000222 + 2 * .0000131 + 8 * .00000222)


def test_timeout():
    import time
    with pytest.raises(TimeoutError):
        with time_limit(.01):
            time.sleep(.1)


def test_patch_fails_closed(tmp_path):
    path = tmp_path / "source.py"
    path.write_text("a = 1\n")
    replace_once(path, "a = 1", "a = 2")
    ast.parse(path.read_text())
    with pytest.raises(ValueError):
        replace_once(path, "a = 1", "a = 3")


def test_pxrdgen_preserves_released_export():
    tree = ast.parse((Path(__file__).parent / 'gsas.py').read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'pxrdgen')
    assert 'precise_export' not in ast.unparse(function)
    assert 'symprec=0.5' in ast.unparse(function)


def test_failure_types():
    from failure_report import classify
    assert classify(dict(status='failed', failure_stage='read-first-pass-export',
                         error='ValueError: Invalid CIF file with no structures!')) == 'unreadable-refined-cif'
    assert classify(dict(status='failed', error='no reflections in data range')) == 'no-reflections-in-observation-range'
    assert classify(dict(status='failed', failure_stage='symmetry-cif-export', error='NoneType')) == 'inter-pass-symmetry-conversion'
    assert classify(dict(status='completed')) == ''
