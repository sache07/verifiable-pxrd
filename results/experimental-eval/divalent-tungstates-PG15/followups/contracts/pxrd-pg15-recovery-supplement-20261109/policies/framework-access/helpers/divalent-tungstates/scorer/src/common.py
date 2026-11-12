"""Paths and small shared helpers for scoring. The scorer imports no generator code."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONFIG = json.loads((ROOT / 'config.json').read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.partial')
    temp.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + '\n')
    temp.replace(path)


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


def allowed_elements(truth, metadata):
    """Elements a submission may use. Cases record them at generation (the elements the lab's sample
    description supplies plus its ambient elements); older cases list them in their public metadata."""
    if truth.get('allowed_elements'):
        return truth['allowed_elements']
    return metadata['elements']
