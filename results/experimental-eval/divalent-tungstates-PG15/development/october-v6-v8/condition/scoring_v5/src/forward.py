"""Verified cache access and lossless import recovery, unchanged from scorer v2."""
from pathlib import Path
import hashlib, json, warnings
import numpy as np
from pymatgen.io.cif import CifWriter
from common import ROOT, read_json, sha, components, load_structure

def cached_components(paths, protocol, size, historical_cache, out):
    """Read historical caches only after checking every forward-input fingerprint."""
    expected = dict(cif_hashes=[sha(p) for p in paths], instrument=protocol['instrument'], grid=protocol['grid'],
                    domain_size_um=float(size), worker_sha256=sha(ROOT/'runtime/gsas_worker.py'),
                    instrument_writer_sha256=sha(ROOT/'runtime/gsas_worker_text.py'), combined_fractions=None)
    token = hashlib.sha256(json.dumps(expected, sort_keys=True).encode()).hexdigest()
    candidates = historical_cache if isinstance(historical_cache, (list,tuple)) else [historical_cache]
    for cache in candidates:
        folder = Path(cache) / token
        if not (folder/'profiles.npz').is_file():
            continue
        req = read_json(folder/'request.json')
        if all(req.get(k) == v for k, v in expected.items()):
            info = read_json(folder/'profiles.json')
            actual = np.array(info['unit_cell_masses_amu'])
            masses = np.array([float(load_structure(p).composition.weight) for p in paths])
            if actual.shape != masses.shape or np.any(np.abs(actual-masses)/masses > .001):
                raise ValueError('GSAS-II/pymatgen CIF interpretation mismatch: unit-cell masses differ')
            with np.load(folder/'profiles.npz') as a:
                x, profiles = a['x'].copy(), a['profiles'].copy()
            return x, profiles, dict(source='verified historical forward cache', path=str(folder),
                                    profiles_sha256=sha(folder/'profiles.npz'))
    x, profiles, info = components(paths, protocol, size, out/'cache')
    return x, profiles, dict(source='fresh immutable-model forward calculation', info=info)

def serialize_without_model_change(paths, out):
    """Recover symmetry-setting import defects only when ADPs cannot be lost.

    Pymatgen's Structure parser does not preserve arbitrary anisotropic CIF
    tensors. Therefore those CIFs are not reserialized by this fallback.
    """
    repaired, evidence = [], []
    for i, path in enumerate(paths):
        text = Path(path).read_text()
        if any(tag in text.lower() for tag in ['_atom_site_u_iso', '_atom_site_b_iso', '_atom_site_aniso']):
            repaired.append(path)
            continue
        before = load_structure(path)
        dest = out/'equivalent_serializations'/f'phase_{i}.cif'
        dest.parent.mkdir(parents=True, exist_ok=True)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            CifWriter(before, symprec=None, significant_figures=12).write_file(dest)
        after = load_structure(dest)
        assert len(before) == len(after) and all(a.species == b.species for a, b in zip(before, after))
        lattice_error = float(np.max(np.abs(before.lattice.matrix-after.lattice.matrix)))
        delta = before.frac_coords-after.frac_coords
        coordinate_error = float(np.max(np.abs(delta-np.round(delta))))
        assert lattice_error < 1e-9 and coordinate_error < 1e-9
        repaired.append(dest)
        evidence.append(dict(source=str(path), source_sha256=sha(path), equivalent_cif=str(dest),
                             maximum_lattice_error_A=lattice_error, maximum_fractional_coordinate_error=coordinate_error,
                             thermal_parameters='absent in both original and equivalent serialization; same GSAS default',
                             action='P1 expansion of supplied operations; no reference information or scientific refinement'))
    if not evidence:
        raise ValueError('CIF import cannot be repaired without auditing thermal parameters')
    return repaired, evidence
