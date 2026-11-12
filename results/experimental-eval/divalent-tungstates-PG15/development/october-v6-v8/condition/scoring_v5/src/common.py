"""Paths and immutable forward-physics dependency for retrospective scoring."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime'))
from physics import components, fit_profiles, save_json, sha, compare_structures

CONFIG = json.loads((ROOT / 'config.json').read_text())

def read_json(path):
    return json.loads(Path(path).read_text())

def code_hashes():
    paths = [ROOT / 'config.json', *sorted((ROOT / 'src').glob('*.py')), *sorted((ROOT / 'runtime').glob('*.py'))]
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}

def load_structure(path):
    import warnings
    from pymatgen.core import Structure
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        s = Structure.from_file(path, primitive=False)
    s.remove_oxidation_states()
    return s
