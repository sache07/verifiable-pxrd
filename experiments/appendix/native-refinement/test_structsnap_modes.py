"""Check the stage-1 prefix without importing CUDA or running refinement."""
import ast
from pathlib import Path
from types import SimpleNamespace

import pytest


def parameters(source, task):
    tree = ast.parse(source)
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'run')
    start = next(i for i, n in enumerate(function.body) if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'stages' for t in n.targets))
    end = next(i for i, n in enumerate(function.body[start:], start) if isinstance(n, ast.ClassDef))
    code = ast.Module(body=function.body[start:end], type_ignores=[])
    env = dict(task=task, torch=SimpleNamespace(tensor=lambda x, **kw: (tuple(x), kw)))
    exec(compile(code, '<stage-parameters>', 'exec'), env)
    return env['stages']


def test_single_stage_only_changes_completion_flag():
    source = Path(__file__).with_name('structsnap.py').read_text()
    original = parameters(source, {})
    single = parameters(source, {'structsnap_mode': 'lattice-stage1'})
    assert len(original) == 2 and len(single) == 1
    assert single[0] == dict(original[0], finished=True)
    assert single[0]['snap_coords'] is False
    assert single[0]['snap_angles'] is False
    assert single[0]['snap_lengths'] is True
    assert original[1]['snap_coords'] is True


def test_unknown_mode_rejected():
    with pytest.raises(ValueError):
        parameters(Path(__file__).with_name('structsnap.py').read_text(), {'structsnap_mode': 'unknown'})


def test_task_mode_validation():
    from common import PROTOCOL, fingerprint, verify_task
    from test_protocol import task
    value = dict(task(), structsnap_mode='lattice-stage1', protocol_sha256=fingerprint(PROTOCOL))
    verify_task(value)
    with pytest.raises(ValueError):
        verify_task(dict(value, method='pxrdgen'))
