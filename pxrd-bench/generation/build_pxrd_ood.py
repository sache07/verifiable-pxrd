"""Generate, certify, build, and audit the 100-case pXRD-ood benchmark.

The complete novelty audit is deliberately coupled to the frozen SQLite index
created by ``index_pxrd_ood_sources.py``. No final CIF is written unless every
required public exposure source is complete and the candidate passes the locked
formula and StructureMatcher checks.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import shutil
import sqlite3
import subprocess
import sys
import time
import warnings
import zlib
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import asdict, dataclass
from importlib.metadata import version
from pathlib import Path, PurePosixPath
from typing import Any, Literal

import numpy as np
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core import Composition, Element, Structure
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.cif import CifParser, CifWriter
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".runs" / "pxrd-ood"
INDEX = CACHE / "indexes" / "exposure.sqlite3"
DEFAULT_TOPOLOGY_INDEX = CACHE / "indexes" / "candidate-topology.sqlite3"
TOPOLOGY_INDEX = Path(
    os.environ.get("PXRD_OOD_TOPOLOGY_INDEX", str(DEFAULT_TOPOLOGY_INDEX))
).expanduser().resolve()
SOURCE_LOCK = CACHE / "SOURCE.lock.json"
POOL = CACHE / "candidates"
CERTIFIED = CACHE / "certified"
V1_CERTIFIED_MANIFEST = CERTIFIED / "manifest-v1.json"
TOPOLOGY_MATCH_CACHE = CACHE / "topology-matches" / "current.json"
OUTPUT = ROOT / "pXRD-ood"
PXRD100 = ROOT / "pXRD-100"

SEED = 20260719
SELECTION_DATE = "2026-07-19"
EXPECTED_CASES = 100
COD_MIN_PARSEABLE_RECORDS = 533_000
SITE_BINS = ((1, 4), (5, 8), (9, 12), (13, 16), (17, 20))
STREAMS = (
    "substitution",
    "ordered-decoration",
    "wyckoff-enumeration",
    "crystal-search",
)
PANEL_BY_STREAM = {
    "substitution": "composition-novel-topology-familiar",
    "ordered-decoration": "composition-novel-topology-familiar",
    "wyckoff-enumeration": "topology-novel",
    "crystal-search": "topology-novel",
}
PATH_BY_STREAM = {
    "substitution": "composition-novel-topology-familiar/substitution",
    "ordered-decoration": "composition-novel-topology-familiar/ordered-decoration",
    "wyckoff-enumeration": "topology-novel/wyckoff-enumeration",
    "crystal-search": "topology-novel/crystal-search",
}

LEARNED_SOURCES = (
    "pxrdgen_mp20",
    "crystalyze_mp20",
    "decifer_noma",
    "jarvis_dft_2022",
    "diffractgpt_released",
)
RETRIEVAL_SOURCES = ("dara_cod_2024", "cod_current")
SUPPLEMENTAL_SOURCES = ("materials_project_2026_04_13",)
REQUIRED_SOURCES = (*LEARNED_SOURCES, *RETRIEVAL_SOURCES, *SUPPLEMENTAL_SOURCES)

STRICT_MATCHER = StructureMatcher(
    ltol=0.20,
    stol=0.30,
    angle_tol=5,
    primitive_cell=True,
    scale=True,
    attempt_supercell=False,
)
ANONYMOUS_MATCHER = StructureMatcher(
    ltol=0.20,
    stol=0.30,
    angle_tol=5,
    primitive_cell=True,
    scale=True,
    attempt_supercell=False,
)
GEOMETRY_MATCHER = StructureMatcher(
    ltol=0.15,
    stol=0.20,
    angle_tol=3,
    primitive_cell=False,
    scale=True,
    attempt_supercell=True,
)

MACE_MODEL_NAME = "MACE-MH-1"
MACE_MODEL_HEAD = "omat_pbe"
MACE_MODEL_URL = (
    "https://github.com/ACEsuit/mace-foundations/releases/download/"
    "mace_mh_1/mace-mh-1.model"
)
MACE_MODEL = Path.home() / ".cache/mace/macemh1model"
MACE_SHA256 = "a522eb7f59c7879963d41586528f4980baf33e086c94aa92e3eafdeccad3be47"
MACE_OUTPUT_TAG = "mace-mh-1"
GENERATION_ENV_LOCK = ROOT / "pxrd-bench" / "generation" / "runtime" / "pxrd-ood-uv.lock"

# Isovalent/chemically analogous pools. Radioactive elements and noble gases are
# intentionally absent; every listed element is supported by the locked MACE model.
SUBSTITUTION_GROUPS = (
    ("Li", "Na", "K", "Rb", "Cs"),
    ("Be", "Mg", "Ca", "Sr", "Ba"),
    ("Sc", "Y", "La", "Lu"),
    ("Ti", "Zr", "Hf"),
    ("V", "Nb", "Ta"),
    ("Cr", "Mo", "W"),
    ("Mn", "Re"),
    ("Fe", "Ru", "Os"),
    ("Co", "Rh", "Ir"),
    ("Ni", "Pd", "Pt"),
    ("Cu", "Ag", "Au"),
    ("Zn", "Cd", "Hg"),
    ("B", "Al", "Ga", "In"),
    ("C", "Si", "Ge", "Sn", "Pb"),
    ("N", "P", "As", "Sb", "Bi"),
    ("O", "S", "Se", "Te"),
    ("F", "Cl", "Br", "I"),
    ("La", "Ce", "Pr", "Nd", "Sm", "Gd", "Tb", "Dy", "Ho", "Er", "Yb"),
)
SUPPORTED_ELEMENTS = frozenset(element for group in SUBSTITUTION_GROUPS for element in group)

PYXTAL_GROUPS = {
    "triclinic": (1, 2),
    "monoclinic": (3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15),
    "orthorhombic": (16, 19, 25, 33, 47, 55, 62, 63, 71),
    "tetragonal": (75, 81, 87, 99, 123, 129, 139),
    "trigonal": (143, 147, 148, 156, 160, 166),
    "hexagonal": (168, 174, 176, 186, 191, 194),
    "cubic": (195, 198, 200, 216, 221, 225),
}
LOW_SYMMETRY_TOPUP_GROUPS = (1, 2, 3, 6, 10, 16, 25, 47)

Stream = Literal["substitution", "ordered-decoration", "wyckoff-enumeration", "crystal-search"]


class StructureUnavailableError(ValueError):
    """A frozen catalog record exposes a formula but contains no atomic geometry."""


@dataclass(slots=True)
class Candidate:
    candidate_id: str
    stream: Stream
    site_bin: str
    cif_path: str
    formula: str
    formula_key: str
    anonymous_formula: str
    primitive_site_count: int
    spacegroup_number: int
    crystal_system: str
    parent_id: str
    parent_formula: str
    parent_payload_sha256: str
    generation_seed: int
    generation: dict[str, Any]
    xrd: dict[str, float]
    validation: dict[str, Any]
    mace: dict[str, Any] | None = None
    certificate: dict[str, Any] | None = None


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_hashes(path: Path) -> dict[str, str]:
    return {
        str(item.relative_to(path)): sha256_file(item)
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def stable_int(*parts: str) -> int:
    return seeded_int(SEED, *parts)


def seeded_int(seed: int, *parts: str) -> int:
    raw = hashlib.sha256(":".join((str(seed), *parts)).encode()).digest()[:8]
    return int.from_bytes(raw, "big")


def canonical_formula(value: str | dict[str, float]) -> tuple[str, str, str]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        composition = Composition(value).reduced_composition
    return (
        composition.reduced_formula,
        composition.alphabetical_formula,
        composition.anonymized_formula,
    )


def crystal_system(number: int) -> str:
    if number <= 2:
        return "triclinic"
    if number <= 15:
        return "monoclinic"
    if number <= 74:
        return "orthorhombic"
    if number <= 142:
        return "tetragonal"
    if number <= 167:
        return "trigonal"
    if number <= 194:
        return "hexagonal"
    return "cubic"


def site_bin(count: int) -> str:
    for low, high in SITE_BINS:
        if low <= count <= high:
            return f"{low}-{high}"
    raise ValueError(f"site count outside benchmark envelope: {count}")


def parse_frozen_cif(text: str) -> Structure:
    """Parse a frozen CIF without treating metadata-only deposits as structures.

    Pymatgen's default occupancy tolerance rejects a small number of otherwise
    usable public COD structures (for example an occupancy reported as 1.001).
    The locked fallback first permits and normalizes occupancies up to 2, then
    tries ASE's independent CIF reader.  A record whose atom-site coordinate
    columns contain only CIF missing-value tokens remains formula exposure but
    has no geometry that can participate in a structure match.
    """
    default_error: Exception | None = None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return Structure.from_str(text, fmt="cif")
    except Exception as exc:
        default_error = exc

    parser = CifParser.from_str(text, occupancy_tolerance=2.0)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structures = parser.parse_structures(primitive=False)
        if structures:
            return structures[0]
    except Exception:
        pass

    try:
        from ase.io import read as ase_read

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            atoms = ase_read(io.StringIO(text), format="cif")
        if len(atoms):
            return AseAtomsAdaptor.get_structure(atoms)
    except Exception:
        pass

    has_coordinates = False
    for block in parser.as_dict().values():
        columns = [
            block.get("_atom_site_fract_x", []),
            block.get("_atom_site_fract_y", []),
            block.get("_atom_site_fract_z", []),
        ]
        columns = [value if isinstance(value, list) else [value] for value in columns]
        for coordinate_triplet in zip(*columns, strict=False):
            if all(str(value).strip() not in {"", ".", "?"} for value in coordinate_triplet):
                has_coordinates = True
                break
        if has_coordinates:
            break
    if not has_coordinates:
        raise StructureUnavailableError(
            "frozen CIF exposes formula/cell metadata but no atomic coordinates"
        ) from default_error
    assert default_error is not None
    raise default_error


def load_structure_blob(
    payload_format: str, payload: bytes | None, locator: str | None
) -> Structure:
    if payload_format == "cif-zlib":
        assert payload is not None
        return parse_frozen_cif(zlib.decompress(payload).decode())
    if payload_format == "pymatgen-json-zlib":
        assert payload is not None
        return Structure.from_dict(json.loads(zlib.decompress(payload)))
    if payload_format == "cif-path":
        assert locator is not None
        path = CACHE / "sources" / "cod-current" / PurePosixPath(locator)
        return parse_frozen_cif(path.read_text(encoding="utf-8"))
    raise ValueError(f"source record has no structure payload: {payload_format}")


def primitive(structure: Structure) -> Structure:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        found = SpacegroupAnalyzer(structure, symprec=0.05, angle_tolerance=5).find_primitive()
    return found or structure.copy()


def explicit_p1_cif(structure: Structure) -> str:
    return str(CifWriter(structure, symprec=None, significant_figures=10))


def xrd_metrics(structure: Structure) -> tuple[dict[str, float], np.ndarray]:
    calculator = XRDCalculator(wavelength="CuKa1")
    pattern = calculator.get_pattern(structure, two_theta_range=(5.0, 90.0))
    positions = np.asarray(pattern.x, dtype=np.float64)
    intensities = np.asarray(pattern.y, dtype=np.float64)
    significant = intensities >= 1.0
    peak_count = int(significant.sum())
    axis = np.arange(5.0, 90.0000001, 0.05, dtype=np.float64)
    sigma = 0.12
    profile = np.zeros_like(axis)
    for position, intensity in zip(positions, intensities, strict=True):
        profile += intensity * np.exp(-0.5 * np.square((axis - position) / sigma))
    maximum = float(profile.max(initial=0))
    if maximum <= 0:
        raise ValueError("empty diffraction profile")
    profile /= maximum
    selected_positions = positions[significant]
    selected_intensities = intensities[significant]
    if len(selected_positions) > 1:
        fwhm = 2.0 * math.sqrt(2.0 * math.log(2.0)) * sigma
        resolvable_peak_count = 1 + int(np.sum(np.diff(selected_positions) >= fwhm))
        flags = np.zeros(len(selected_positions), dtype=bool)
        close = np.flatnonzero(np.diff(selected_positions) < fwhm)
        flags[close] = True
        flags[close + 1] = True
        overlap = float(selected_intensities[flags].sum() / selected_intensities.sum())
    else:
        resolvable_peak_count = len(selected_positions)
        overlap = 0.0
    probabilities = selected_intensities / selected_intensities.sum()
    entropy = float(-np.sum(probabilities * np.log(probabilities + 1e-300)))
    normalized_entropy = entropy / math.log(max(peak_count, 2))
    return (
        {
            "peak_count_above_1pct": peak_count,
            "resolvable_peak_count": resolvable_peak_count,
            "overlap_intensity_fraction": overlap,
            "normalized_peak_entropy": normalized_entropy,
        },
        profile,
    )


def minimum_distance(structure: Structure) -> float:
    matrix = np.asarray(structure.distance_matrix, dtype=float)
    np.fill_diagonal(matrix, np.inf)
    return float(matrix.min()) if len(structure) > 1 else float(structure.lattice.abc[0])


def validate_structure(
    structure: Structure,
) -> tuple[Structure, dict[str, Any], dict[str, float], np.ndarray]:
    if not structure.is_ordered:
        raise ValueError("structure is disordered")
    result = primitive(structure)
    if not 1 <= len(result) <= 20:
        raise ValueError(f"primitive site count {len(result)} is outside 1-20")
    if any(site.specie.symbol not in SUPPORTED_ELEMENTS for site in result):
        raise ValueError("structure contains an unsupported element")
    volume_per_atom = float(result.volume / len(result))
    if not 4.0 <= volume_per_atom <= 100.0:
        raise ValueError(f"volume per atom {volume_per_atom:.4f} outside 4-100 A^3")
    distance = minimum_distance(result)
    if distance < 0.75:
        raise ValueError(f"minimum distance {distance:.4f} A is below 0.75 A")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sg_tight = SpacegroupAnalyzer(
            result, symprec=0.01, angle_tolerance=5
        ).get_space_group_number()
        sg_loose = SpacegroupAnalyzer(
            result, symprec=0.05, angle_tolerance=5
        ).get_space_group_number()
    if sg_tight != sg_loose:
        raise ValueError(f"symmetry is tolerance-unstable: {sg_tight} vs {sg_loose}")
    cif = explicit_p1_cif(result)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        roundtrip = Structure.from_str(cif, fmt="cif")
    if not STRICT_MATCHER.fit(result, roundtrip):
        raise ValueError("explicit P1 CIF round trip changed the structure")
    xrd, profile = xrd_metrics(result)
    if xrd["resolvable_peak_count"] < 5:
        raise ValueError("fewer than five resolvable >1% Bragg peaks")
    validation = {
        "ordered_full_occupancy": True,
        "cif_roundtrip": True,
        "minimum_periodic_distance_angstrom": distance,
        "spacegroup_stable_symprec_0p01_to_0p05": True,
        "volume_per_atom_angstrom3": volume_per_atom,
    }
    return result, validation, xrd, profile


def erased_species(structure: Structure) -> Structure:
    erased = structure.copy()
    erased.replace_species({element: "C" for element in erased.composition.elements})
    return erased


def replacement_options(symbol: str) -> tuple[str, ...]:
    options: set[str] = set()
    for group in SUBSTITUTION_GROUPS:
        if symbol in group:
            options.update(group)
    options.discard(symbol)
    return tuple(sorted(options, key=lambda item: stable_int(symbol, item)))


def element_radius(symbol: str) -> float:
    element = Element(symbol)
    value = element.atomic_radius or element.atomic_radius_calculated
    return float(value) if value is not None else 1.25


def scaled_for_mapping(structure: Structure, mapping: dict[str, str]) -> tuple[Structure, float]:
    result = structure.copy()
    result.replace_species(mapping)
    ratios = [element_radius(target) / element_radius(source) for source, target in mapping.items()]
    factor = min(1.20, max(0.85, float(np.median(ratios))))
    result.scale_lattice(structure.volume * factor**3)
    return result, factor


def candidate_path(stream: str, candidate_id: str) -> Path:
    return POOL / stream / f"{candidate_id}.cif"


def save_candidate(candidate: Candidate, structure: Structure) -> None:
    path = ROOT / candidate.cif_path
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".partial")
    temporary.write_text(explicit_p1_cif(structure), encoding="utf-8", newline="\n")
    temporary.replace(path)


def make_candidate(
    *,
    stream: Stream,
    structure: Structure,
    parent_id: str,
    parent_formula: str,
    parent_payload_sha256: str,
    generation_seed: int,
    generation: dict[str, Any],
) -> Candidate:
    final, validation, xrd, _ = validate_structure(structure)
    formula, key, anonymous = canonical_formula(final.composition.as_dict())
    sg = SpacegroupAnalyzer(final, symprec=0.05, angle_tolerance=5).get_space_group_number()
    identity = sha256_bytes(
        json.dumps(
            {
                "stream": stream,
                "parent": parent_id,
                "seed": generation_seed,
                "formula": key,
                "structure": final.as_dict(),
            },
            sort_keys=True,
        ).encode()
    )[:16]
    candidate_id = f"pxrdood-{stream.replace('-', '')}-{identity}"
    path = candidate_path(stream, candidate_id)
    candidate = Candidate(
        candidate_id=candidate_id,
        stream=stream,
        site_bin=site_bin(len(final)),
        cif_path=str(path.relative_to(ROOT)),
        formula=formula,
        formula_key=key,
        anonymous_formula=anonymous,
        primitive_site_count=len(final),
        spacegroup_number=sg,
        crystal_system=crystal_system(sg),
        parent_id=parent_id,
        parent_formula=parent_formula,
        parent_payload_sha256=parent_payload_sha256,
        generation_seed=generation_seed,
        generation=generation,
        xrd=xrd,
        validation=validation,
    )
    save_candidate(candidate, final)
    return candidate


def load_candidate(candidate: Candidate) -> Structure:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return Structure.from_file(ROOT / candidate.cif_path)


def read_pool() -> list[Candidate]:
    path = POOL / "manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Candidate(**item) for item in data["candidates"]]


def open_index() -> sqlite3.Connection:
    if not INDEX.is_file():
        raise RuntimeError("exposure index is missing; run index_pxrd_ood_sources.py")
    connection = sqlite3.connect(INDEX, timeout=120)
    connection.row_factory = sqlite3.Row
    if TOPOLOGY_INDEX.is_file():
        connection.execute("ATTACH DATABASE ? AS topology", (str(TOPOLOGY_INDEX),))
    return connection


def assert_complete_sources(connection: sqlite3.Connection) -> None:
    rows = {
        row["source"]: row
        for row in connection.execute(
            "SELECT source, status, record_count, failed_count FROM source_state"
        )
    }
    missing = [source for source in REQUIRED_SOURCES if source not in rows]
    incomplete = [
        source
        for source in REQUIRED_SOURCES
        if source in rows and rows[source]["status"] != "complete"
    ]
    if missing or incomplete:
        raise RuntimeError(
            f"novelty sources incomplete: missing={missing}, incomplete={incomplete}"
        )
    if rows["cod_current"]["record_count"] < COD_MIN_PARSEABLE_RECORDS:
        raise RuntimeError(
            f"complete COD snapshot has fewer than {COD_MIN_PARSEABLE_RECORDS:,} indexed structures"
        )


def formula_hits(connection: sqlite3.Connection, formula_key: str) -> dict[str, int]:
    counts = dict.fromkeys(REQUIRED_SOURCES, 0)
    for row in connection.execute(
        "SELECT source, COUNT(*) AS count FROM records WHERE formula_key = ? GROUP BY source",
        (formula_key,),
    ):
        if row["source"] in counts:
            counts[row["source"]] = int(row["count"])
    return counts


def anonymous_counts(connection: sqlite3.Connection, anonymous: str) -> dict[str, int]:
    counts = dict.fromkeys(REQUIRED_SOURCES, 0)
    for row in connection.execute(
        "SELECT source, COUNT(*) AS count FROM records WHERE anonymous_formula = ? GROUP BY source",
        (anonymous,),
    ):
        if row["source"] in counts:
            counts[row["source"]] = int(row["count"])
    return counts


def source_records(connection: sqlite3.Connection, *, source: str, field: str, value: str) -> Any:
    if field == "record_id_prefix":
        return connection.execute(
            "SELECT record_id, payload_format, payload, locator FROM records "
            "WHERE source = ? AND record_id >= ? AND record_id < ? ORDER BY record_id",
            (source, value, value + "\uffff"),
        )
    if field not in {"formula_key", "anonymous_formula", "record_id"}:
        raise ValueError(field)
    databases = {str(row[1]) for row in connection.execute("PRAGMA database_list")}
    table = (
        "topology.records"
        if field == "anonymous_formula" and "topology" in databases
        else "main.records"
    )
    indexed = " INDEXED BY records_formula_match_idx" if field == "formula_key" else ""
    return connection.execute(
        f"SELECT record_id, payload_format, payload, locator FROM {table} "
        f"{indexed} "
        f"WHERE source = ? AND {field} = ? ORDER BY record_id",
        (source, value),
    )


def prepare_topology_index(
    connection: sqlite3.Connection, candidates: list[Candidate], *, replace: bool
) -> None:
    """Materialize candidate-relevant topology rows in comparison order.

    The frozen exposure database is physically ordered by source ingestion. An
    anonymous-formula lookup therefore causes scattered reads across an 11 GB
    file. This derived index is built by one authoritative table scan and stores
    only the anonymous formulas needed by the candidate pool. It does not alter
    the source boundary or novelty rule; metadata binds it to both frozen-index
    and candidate-pool hashes, and exact per-formula counts are checked below.
    """
    topology_candidates = [
        candidate
        for candidate in candidates
        if candidate.stream in {"wyckoff-enumeration", "crystal-search"}
    ]
    formulas = sorted({candidate.anonymous_formula for candidate in topology_candidates})
    if not formulas:
        raise RuntimeError("candidate pool has no topology-novel formulas")
    source_lock = json.loads(SOURCE_LOCK.read_text(encoding="utf-8"))
    source_index_sha256 = str(source_lock["index"]["sha256"])
    pool_manifest_sha256 = sha256_file(POOL / "manifest.json")
    formulas_sha256 = sha256_bytes("\n".join(formulas).encode())
    expected_metadata = {
        "source_index_sha256": source_index_sha256,
        "pool_manifest_sha256": pool_manifest_sha256,
        "anonymous_formulas_sha256": formulas_sha256,
        "anonymous_formula_count": str(len(formulas)),
    }

    def metadata(path: Path) -> dict[str, str] | None:
        if not path.is_file():
            return None
        derived = sqlite3.connect(path)
        try:
            return {
                str(key): str(value)
                for key, value in derived.execute("SELECT key, value FROM metadata")
            }
        except sqlite3.DatabaseError:
            return None
        finally:
            derived.close()

    existing_metadata = metadata(TOPOLOGY_INDEX)
    layout_keys = (
        "source_index_sha256",
        "anonymous_formulas_sha256",
        "anonymous_formula_count",
    )
    reusable_layout = bool(
        not replace
        and existing_metadata is not None
        and all(existing_metadata.get(key) == expected_metadata[key] for key in layout_keys)
    )
    if reusable_layout:
        # Candidate relaxation changes the pool-manifest digest but cannot
        # change which reference rows belong to this subset when the anonymous
        # formula-set digest is identical. Refresh only that provenance field;
        # the exact main/subset row-count checks below still prove completeness
        # for every formula before any match is attempted.
        temporary = TOPOLOGY_INDEX.with_suffix(".sqlite3.partial")
        temporary.unlink(missing_ok=True)
        if existing_metadata != expected_metadata:
            derived = sqlite3.connect(TOPOLOGY_INDEX)
            try:
                derived.execute("BEGIN IMMEDIATE")
                derived.execute(
                    "INSERT OR REPLACE INTO metadata(key, value) VALUES (?, ?)",
                    ("pool_manifest_sha256", pool_manifest_sha256),
                )
                derived.commit()
            finally:
                derived.close()
        databases = {str(row[1]) for row in connection.execute("PRAGMA database_list")}
        if "topology" not in databases:
            connection.execute("ATTACH DATABASE ? AS topology", (str(TOPOLOGY_INDEX),))
    else:
        temporary = TOPOLOGY_INDEX.with_suffix(".sqlite3.partial")
        if temporary.exists():
            temporary.unlink()
        derived = sqlite3.connect(temporary)
        try:
            derived.executescript(
                """
                PRAGMA journal_mode=OFF;
                PRAGMA synchronous=OFF;
                PRAGMA temp_store=FILE;
                PRAGMA page_size=65536;
                CREATE TABLE records (
                    source TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    split TEXT,
                    ordinal INTEGER NOT NULL,
                    formula TEXT NOT NULL,
                    formula_key TEXT NOT NULL,
                    anonymous_formula TEXT NOT NULL,
                    declared_spacegroup INTEGER,
                    payload_format TEXT NOT NULL,
                    payload BLOB,
                    locator TEXT,
                    PRIMARY KEY (anonymous_formula, source, record_id)
                ) WITHOUT ROWID;
                CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                """
            )
            derived.execute("ATTACH DATABASE ? AS exposure", (str(INDEX),))
            placeholders = ",".join("?" for _ in formulas)
            # NOT INDEXED deliberately turns this into a sequential authoritative
            # scan instead of 79 sets of random BLOB reads from the large table.
            derived.execute(
                "INSERT INTO records "
                "SELECT source, record_id, split, ordinal, formula, formula_key, "
                "anonymous_formula, declared_spacegroup, payload_format, payload, locator "
                "FROM exposure.records NOT INDEXED "
                f"WHERE anonymous_formula IN ({placeholders}) "
                "ORDER BY anonymous_formula, source, record_id",
                formulas,
            )
            derived.executemany(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                sorted(expected_metadata.items()),
            )
            derived.commit()
        finally:
            derived.close()
        if TOPOLOGY_INDEX.exists():
            backup = CACHE / "backups" / f"candidate-topology-{int(time.time())}.sqlite3"
            backup.parent.mkdir(parents=True, exist_ok=True)
            TOPOLOGY_INDEX.replace(backup)
        temporary.replace(TOPOLOGY_INDEX)
        databases = {str(row[1]) for row in connection.execute("PRAGMA database_list")}
        if "topology" in databases:
            connection.execute("DETACH DATABASE topology")
        connection.execute("ATTACH DATABASE ? AS topology", (str(TOPOLOGY_INDEX),))

    actual_metadata = {
        str(key): str(value)
        for key, value in connection.execute("SELECT key, value FROM topology.metadata")
    }
    if actual_metadata != expected_metadata:
        raise RuntimeError("derived topology index metadata does not match the frozen pool")
    for anonymous_formula in formulas:
        main_count = connection.execute(
            "SELECT COUNT(*) FROM main.records WHERE anonymous_formula = ?",
            (anonymous_formula,),
        ).fetchone()[0]
        subset_count = connection.execute(
            "SELECT COUNT(*) FROM topology.records WHERE anonymous_formula = ?",
            (anonymous_formula,),
        ).fetchone()[0]
        if main_count != subset_count:
            raise RuntimeError(
                f"derived topology index is incomplete for {anonymous_formula}: "
                f"{subset_count} != {main_count}"
            )
    print(
        f"topology subset: {len(formulas)} formulas, "
        f"{connection.execute('SELECT COUNT(*) FROM topology.records').fetchone()[0]:,} records"
    )


def any_match(
    connection: sqlite3.Connection,
    candidate: Structure,
    *,
    source: str,
    field: str,
    value: str,
    anonymous: bool,
) -> tuple[str | None, int, int, int]:
    compared = 0
    unparseable = 0
    structureless = 0
    for row in source_records(connection, source=source, field=field, value=value):
        if row["payload_format"] == "cod-id-only":
            # Every DARA ID is checked structurally through the complete COD source.
            continue
        try:
            reference = load_structure_blob(row["payload_format"], row["payload"], row["locator"])
        except StructureUnavailableError:
            structureless += 1
            continue
        except Exception:
            unparseable += 1
            continue
        compared += 1
        try:
            matched = (
                ANONYMOUS_MATCHER.fit_anonymous(candidate, reference)
                if anonymous
                else STRICT_MATCHER.fit(candidate, reference)
            )
        except Exception:
            unparseable += 1
            continue
        if matched:
            return str(row["record_id"]), compared, unparseable, structureless
    return None, compared, unparseable, structureless


def existing_pxrd100_formulas() -> set[str]:
    manifest = json.loads((PXRD100 / "manifest.json").read_text(encoding="utf-8"))
    return {case["reduced_formula_key"] for case in manifest["cases"]}


def parent_rows(
    connection: sqlite3.Connection, *, require_familiar_exposure: bool
) -> list[sqlite3.Row]:
    familiar_clause = (
        """
                 AND EXISTS (
                     SELECT 1 FROM records AS n
                     WHERE n.source = 'decifer_noma'
                       AND n.record_id >= 'MP_' || p.record_id || '#'
                       AND n.record_id < 'MP_' || p.record_id || '#' || char(1114111)
                 )
                 AND EXISTS (
                     SELECT 1 FROM records AS j
                     WHERE j.source = 'jarvis_dft_2022' AND j.formula_key = p.formula_key
                 )
    """
        if require_familiar_exposure
        else ""
    )
    return list(
        connection.execute(
            f"""SELECT p.record_id, p.formula, p.formula_key, p.anonymous_formula
               FROM records AS p
               JOIN records AS c ON c.source = 'crystalyze_mp20'
                    AND c.split = 'train' AND c.record_id = p.record_id
               WHERE p.source = 'pxrdgen_mp20' AND p.split = 'train'
                 {familiar_clause}
               ORDER BY p.record_id"""
        )
    )


def formula_known_everywhere(connection: sqlite3.Connection, formula_key: str) -> bool:
    learned = connection.execute(
        "SELECT COUNT(DISTINCT source) FROM records "
        "WHERE formula_key = ? AND source IN ({})".format(",".join("?" for _ in LEARNED_SOURCES)),
        (formula_key, *LEARNED_SOURCES),
    ).fetchone()[0]
    retrieval = connection.execute(
        "SELECT COUNT(*) FROM records WHERE formula_key = ? AND source IN (?, ?)",
        (formula_key, *RETRIEVAL_SOURCES),
    ).fetchone()[0]
    return learned == len(LEARNED_SOURCES) and retrieval > 0


def current_formula_absent(connection: sqlite3.Connection, formula_key: str) -> bool:
    return (
        connection.execute(
            "SELECT 1 FROM records WHERE formula_key = ? LIMIT 1", (formula_key,)
        ).fetchone()
        is None
    )


def shuffle_rows(rows: list[sqlite3.Row], *parts: str) -> list[sqlite3.Row]:
    return sorted(rows, key=lambda row: stable_int(*parts, str(row["record_id"])))


def generate_substitution(
    parent: sqlite3.Row, structure: Structure, attempt: int
) -> tuple[Structure, dict[str, Any]] | None:
    symbols = sorted({site.specie.symbol for site in structure})
    source = symbols[attempt % len(symbols)]
    options = replacement_options(source)
    if not options:
        return None
    target = options[(attempt // len(symbols)) % len(options)]
    candidate, factor = scaled_for_mapping(structure, {source: target})
    return candidate, {
        "method": "full-species isovalent substitution",
        "mapping": {source: target},
        "lattice_scale_factor": factor,
    }


def generate_decoration(
    parent: sqlite3.Row, structure: Structure, attempt: int
) -> tuple[Structure, dict[str, Any]] | None:
    analyzer = SpacegroupAnalyzer(structure, symprec=0.05, angle_tolerance=5)
    symmetrized = analyzer.get_symmetrized_structure()
    by_symbol: dict[str, list[int]] = defaultdict(list)
    for index, site in enumerate(structure):
        by_symbol[site.specie.symbol].append(index)
    eligible: list[tuple[str, list[int]]] = []
    for orbit in symmetrized.equivalent_indices:
        indexes = [int(index) for index in orbit]
        symbol = structure[indexes[0]].specie.symbol
        fraction = len(indexes) / len(by_symbol[symbol])
        # Decorating one complete orbit while retaining another orbit of the
        # source species preserves crystallographic order and avoids collapsing
        # the 25-case stream into arbitrary P1 colorings.
        if len(indexes) < len(by_symbol[symbol]) and any(
            math.isclose(fraction, target, abs_tol=1e-9) for target in (0.25, 0.50, 0.75)
        ):
            eligible.append((symbol, indexes))
    if not eligible:
        # Some small parents expose only one orbit. Use a deterministic ordered
        # sub-orbit coloring as a fallback; its lower symmetry is recorded.
        eligible = [
            (symbol, indexes)
            for symbol, indexes in sorted(by_symbol.items())
            if len(indexes) >= 2
            and any(
                math.isclose(len(indexes) * fraction, round(len(indexes) * fraction))
                for fraction in (0.5, 0.25, 0.75)
            )
        ]
    if not eligible:
        return None
    source, indexes = eligible[attempt % len(eligible)]
    options = replacement_options(source)
    if not options:
        return None
    target = options[(attempt // len(eligible)) % len(options)]
    complete_orbit = len(indexes) < len(by_symbol[source])
    if complete_orbit:
        selected = indexes
    else:
        allowed_fractions = tuple(
            fraction
            for fraction in (0.5, 0.25, 0.75)
            if math.isclose(len(indexes) * fraction, round(len(indexes) * fraction))
        )
        fraction = allowed_fractions[(attempt // max(1, len(options))) % len(allowed_fractions)]
        replace_count = round(len(indexes) * fraction)
        selected = sorted(
            indexes,
            key=lambda index: stable_int(str(parent["record_id"]), str(attempt), str(index)),
        )[:replace_count]
    replace_count = len(selected)
    result = structure.copy()
    for index in selected:
        result.replace(index, target)
    source_radius = element_radius(source)
    target_radius = element_radius(target)
    weighted = 1.0 + (target_radius / source_radius - 1.0) * replace_count / len(result)
    factor = min(1.15, max(0.90, weighted))
    result.scale_lattice(structure.volume * factor**3)
    return result, {
        "method": "ordered site decoration",
        "source_species": source,
        "target_species": target,
        "decorated_site_indices": selected,
        "complete_parent_wyckoff_orbit": complete_orbit,
        "target_fraction_within_source_sites": replace_count / len(by_symbol[source]),
        "lattice_scale_factor": factor,
    }


def pyxtal_composition_candidate(
    composition: Composition, *, seed: int, group: int
) -> tuple[Structure, dict[str, Any]] | None:
    try:
        from pyxtal import pyxtal
    except ImportError as exc:
        raise RuntimeError("PyXtal generation requires the generation extra") from exc
    counts = composition.get_el_amt_dict()
    if any(not math.isclose(value, round(value), abs_tol=1e-6) for value in counts.values()):
        return None
    species = sorted(counts)
    ions = [round(counts[item]) for item in species]
    generator = np.random.default_rng(seed)
    crystal = pyxtal(random_state=generator)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            crystal.from_random(
                dim=3,
                group=group,
                species=species,
                numIons=ions,
                conventional=False,
                max_count=80,
                force_pass=False,
                random_state=generator,
            )
    except Exception:
        return None
    if not crystal.valid:
        return None
    result = crystal.to_pymatgen()
    return result, {
        "method": "PyXtal symmetry/Wyckoff constructive generation",
        "requested_spacegroup_number": group,
        "species": species,
        "counts": ions,
        "pyxtal_seed": seed,
    }


def pyxtal_candidate(
    structure: Structure, *, seed: int, group: int
) -> tuple[Structure, dict[str, Any]] | None:
    source = primitive(structure)
    return pyxtal_composition_candidate(source.composition, seed=seed, group=group)


def generate_pool(*, per_bin: int, replace: bool) -> None:
    connection = open_index()
    try:
        assert_complete_sources(connection)
        if POOL.exists():
            if not replace:
                raise RuntimeError(f"candidate pool exists: {POOL}; pass --replace")
            backup = CACHE / "backups" / f"candidates-{int(time.time())}"
            backup.parent.mkdir(parents=True, exist_ok=True)
            POOL.replace(backup)
        POOL.mkdir(parents=True)
        forbidden_formulas = existing_pxrd100_formulas()
        rows = parent_rows(connection, require_familiar_exposure=True)
        if len(rows) < 1000:
            raise RuntimeError(f"only {len(rows)} shared MP20 training parents")
        parsed: dict[str, Structure] = {}
        familiar_parent_evidence: dict[str, dict[str, Any] | None] = {}
        candidates: list[Candidate] = []
        used_ids: set[str] = set()
        formula_seen: set[str] = set(forbidden_formulas)
        proposal_counts: dict[str, int] = {}

        def structure_for(row: sqlite3.Row) -> Structure:
            key = str(row["record_id"])
            if key not in parsed:
                payload = connection.execute(
                    "SELECT payload_format, payload, locator FROM records "
                    "WHERE source = 'pxrdgen_mp20' AND record_id = ?",
                    (key,),
                ).fetchone()
                if payload is None:
                    raise RuntimeError(f"missing MP-20 parent payload: {key}")
                parsed[key] = primitive(
                    load_structure_blob(
                        payload["payload_format"], payload["payload"], payload["locator"]
                    )
                )
            return parsed[key]

        def parent_exposure_evidence(
            row: sqlite3.Row, structure: Structure
        ) -> dict[str, Any] | None:
            parent_id = str(row["record_id"])
            if parent_id in familiar_parent_evidence:
                return familiar_parent_evidence[parent_id]
            evidence: dict[str, Any] = {}
            for source in ("decifer_noma", "jarvis_dft_2022"):
                field = "record_id_prefix" if source == "decifer_noma" else "formula_key"
                value = f"MP_{parent_id}#" if source == "decifer_noma" else str(row["formula_key"])
                match, compared, failures, structureless = any_match(
                    connection,
                    structure,
                    source=source,
                    field=field,
                    value=value,
                    anonymous=False,
                )
                if match is None:
                    familiar_parent_evidence[parent_id] = None
                    return None
                evidence[source] = {
                    "anonymous_match_id": match,
                    "match_mode": "species-aware (therefore also species-erased)",
                    "structures_compared": compared,
                    "unparseable_candidates_before_match": failures,
                    "structureless_catalog_records_before_match": structureless,
                }
            familiar_parent_evidence[parent_id] = evidence
            return evidence

        # Composition-novel streams are screened against the complete formula index
        # before being admitted to the surplus pool.
        for stream, transform in (
            ("substitution", generate_substitution),
            ("ordered-decoration", generate_decoration),
        ):
            counts_by_bin: Counter[str] = Counter()
            proposals = 0
            for row in shuffle_rows(rows, stream):
                if all(counts_by_bin[f"{low}-{high}"] >= per_bin for low, high in SITE_BINS):
                    break
                parent_id = str(row["record_id"])
                if parent_id in used_ids:
                    continue
                try:
                    parent = structure_for(row)
                    target_bin = site_bin(len(parent))
                except Exception:
                    continue
                exposure_evidence = parent_exposure_evidence(row, parent)
                if exposure_evidence is None:
                    continue
                if counts_by_bin[target_bin] >= per_bin:
                    continue
                for attempt in range(80):
                    proposals += 1
                    if proposals > 20_000:
                        raise RuntimeError(f"{stream} exceeded the 20,000-proposal limit")
                    generated = transform(row, parent, attempt)
                    if generated is None:
                        continue
                    proposal, details = generated
                    try:
                        final, _, _, _ = validate_structure(proposal)
                        _, key, _ = canonical_formula(final.composition.as_dict())
                    except Exception:
                        continue
                    if key in formula_seen or not current_formula_absent(connection, key):
                        continue
                    try:
                        candidate = make_candidate(
                            stream=stream,
                            structure=final,
                            parent_id=parent_id,
                            parent_formula=str(row["formula"]),
                            parent_payload_sha256=sha256_bytes(explicit_p1_cif(parent).encode()),
                            generation_seed=stable_int(stream, parent_id, str(attempt)),
                            generation={
                                **details,
                                "familiar_parent_exposure": exposure_evidence,
                            },
                        )
                    except Exception:
                        continue
                    if candidate.site_bin != target_bin:
                        continue
                    candidates.append(candidate)
                    counts_by_bin[target_bin] += 1
                    used_ids.add(parent_id)
                    formula_seen.add(key)
                    break
            expected = {f"{low}-{high}": per_bin for low, high in SITE_BINS}
            if dict(counts_by_bin) != expected:
                raise RuntimeError(f"{stream} pool quota failure: {counts_by_bin} != {expected}")
            proposal_counts[stream] = proposals
            print(f"{stream}: {sum(counts_by_bin.values())} candidates {dict(counts_by_bin)}")

        # Topology streams use formula-familiar parents and deliberately rare
        # anonymous stoichiometries to make the later exhaustive matcher tractable.
        topology_rows: list[sqlite3.Row] = []
        for row in parent_rows(connection, require_familiar_exposure=False):
            key = str(row["formula_key"])
            if key in formula_seen or not formula_known_everywhere(connection, key):
                continue
            counts = anonymous_counts(connection, str(row["anonymous_formula"]))
            if sum(counts.values()) > 12_000:
                continue
            topology_rows.append(row)

        system_cycle = tuple(PYXTAL_GROUPS)
        for stream in ("wyckoff-enumeration", "crystal-search"):
            counts_by_bin = Counter()
            proposals = 0
            stream_index = STREAMS.index(stream)
            for row in shuffle_rows(topology_rows, stream):
                if all(counts_by_bin[f"{low}-{high}"] >= per_bin for low, high in SITE_BINS):
                    break
                parent_id = str(row["record_id"])
                if parent_id in used_ids:
                    continue
                try:
                    parent = structure_for(row)
                    target_bin = site_bin(len(parent))
                except Exception:
                    continue
                if counts_by_bin[target_bin] >= per_bin:
                    continue
                generated_candidate: Candidate | None = None
                for attempt in range(160):
                    proposals += 1
                    if proposals > 20_000:
                        raise RuntimeError(f"{stream} exceeded the 20,000-proposal limit")
                    system = system_cycle[
                        (len(candidates) + attempt + stream_index) % len(system_cycle)
                    ]
                    groups = PYXTAL_GROUPS[system]
                    group = groups[stable_int(stream, parent_id, str(attempt)) % len(groups)]
                    generation_seed = stable_int(stream, parent_id, str(attempt)) % (2**32)
                    generated = pyxtal_candidate(parent, seed=generation_seed, group=group)
                    if generated is None:
                        continue
                    proposal, details = generated
                    try:
                        candidate = make_candidate(
                            stream=stream,
                            structure=proposal,
                            parent_id=parent_id,
                            parent_formula=str(row["formula"]),
                            parent_payload_sha256=sha256_bytes(explicit_p1_cif(parent).encode()),
                            generation_seed=generation_seed,
                            generation=details,
                        )
                    except Exception:
                        continue
                    if candidate.site_bin != target_bin or candidate.formula_key in formula_seen:
                        continue
                    if STRICT_MATCHER.fit(load_candidate(candidate), parent):
                        continue
                    generated_candidate = candidate
                    break
                if generated_candidate is None:
                    continue
                candidates.append(generated_candidate)
                counts_by_bin[target_bin] += 1
                used_ids.add(parent_id)
                formula_seen.add(generated_candidate.formula_key)
            expected = {f"{low}-{high}": per_bin for low, high in SITE_BINS}
            if dict(counts_by_bin) != expected:
                raise RuntimeError(f"{stream} pool quota failure: {counts_by_bin} != {expected}")
            proposal_counts[stream] = proposals
            print(f"{stream}: {sum(counts_by_bin.values())} candidates {dict(counts_by_bin)}")

        write_json(
            POOL / "manifest.json",
            {
                "schema_version": "1.0.0",
                "dataset_id": "pXRD-ood-v1-candidate-pool",
                "selection_seed": SEED,
                "per_stream_site_bin_count": per_bin,
                "candidate_count": len(candidates),
                "proposal_counts": proposal_counts,
                "candidates": [asdict(candidate) for candidate in candidates],
            },
        )
    finally:
        connection.close()


def topup_topology_pool(
    *,
    wyckoff_buffer: int,
    crystal_buffer: int,
    min_certified_per_bin: int = 5,
) -> None:
    """Append deterministic low-symmetry proposals for deficient topology bins.

    The initial broad symmetry sweep is intentionally unbiased and therefore
    loses many small-cell proposals to the complete topology matcher. A top-up
    is driven only by frozen-corpus certificates, never baseline outcomes. It
    uses new composition-familiar formulas, reduced-formula atom counts near the
    top of each site bin, and a deterministic space-group cycle to preserve the
    final diversity constraints.
    """
    if wyckoff_buffer < 0 or crystal_buffer < 0:
        raise ValueError("top-up buffers must be nonnegative")
    if min_certified_per_bin < 5:
        raise ValueError("minimum certified count must preserve the five-case panel quota")
    candidates = read_pool()
    manifest_path = POOL / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pass_counts: Counter[tuple[str, str]] = Counter()
    pending_counts: Counter[tuple[str, str]] = Counter()
    for candidate in candidates:
        certificate_path = CERTIFIED / f"{candidate.candidate_id}.json"
        if not certificate_path.is_file():
            if candidate.generation.get("topup_round"):
                pending_counts[candidate.stream, candidate.site_bin] += 1
            continue
        certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
        if certificate.get("passes_frozen_corpus_rules"):
            pass_counts[candidate.stream, candidate.site_bin] += 1
    additions_needed: dict[tuple[str, str], int] = {}
    for stream, buffer in (
        ("wyckoff-enumeration", wyckoff_buffer),
        ("crystal-search", crystal_buffer),
    ):
        for low, high in SITE_BINS:
            label = f"{low}-{high}"
            deficit = max(0, min_certified_per_bin - pass_counts[stream, label])
            desired_surplus = deficit + buffer if deficit else 0
            additions_needed[stream, label] = max(
                0, desired_surplus - pending_counts[stream, label]
            )
    if not any(additions_needed.values()):
        print(
            "topology pool already has at least "
            f"{min_certified_per_bin} certified cases in every bin"
        )
        return

    connection = open_index()
    try:
        assert_complete_sources(connection)
        # A formula/parent belonging only to a previously rejected candidate may
        # be proposed again with a different geometry. Selection still enforces
        # final formula and parent uniqueness; this avoids discarding scarce
        # small-cell compositions merely because an earlier topology was seen.
        used_formulas = set(existing_pxrd100_formulas())
        used_parents: set[str] = set()
        for candidate in candidates:
            certificate_path = CERTIFIED / f"{candidate.candidate_id}.json"
            unavailable = not certificate_path.is_file()
            if certificate_path.is_file():
                unavailable = bool(
                    json.loads(certificate_path.read_text(encoding="utf-8")).get(
                        "passes_frozen_corpus_rules"
                    )
                )
            if unavailable:
                used_formulas.add(candidate.formula_key)
                used_parents.add(candidate.parent_id)
        # Keep a generous deterministic menu for each bin while avoiding a full
        # parse of all MP-20 parents. Formula counts, not the parent's Z value,
        # determine the new primitive P1/Wyckoff proposal size.
        menus: dict[
            str, list[tuple[sqlite3.Row, Composition, int, int, int]]
        ] = defaultdict(list)
        menu_formula_seen: set[str] = set()
        anonymous_exposure_counts: dict[str, int] = {}
        for row in shuffle_rows(parent_rows(connection, require_familiar_exposure=False), "topup"):
            key = str(row["formula_key"])
            if key in used_formulas or key in menu_formula_seen:
                continue
            try:
                composition = Composition(key).reduced_composition
                amounts = composition.get_el_amt_dict()
                if any(
                    not math.isclose(value, round(value), abs_tol=1e-6)
                    for value in amounts.values()
                ):
                    continue
                atom_count = sum(round(value) for value in amounts.values())
                label = site_bin(atom_count)
            except Exception:
                continue
            if not any(additions_needed[stream, label] for stream in (
                "wyckoff-enumeration",
                "crystal-search",
            )):
                continue
            if any(element.symbol not in SUPPORTED_ELEMENTS for element in composition.elements):
                continue
            if not formula_known_everywhere(connection, key):
                continue
            anonymous_formula = str(row["anonymous_formula"])
            if anonymous_formula not in anonymous_exposure_counts:
                anonymous_exposure_counts[anonymous_formula] = int(
                    connection.execute(
                        "SELECT COUNT(*) FROM records WHERE anonymous_formula=?",
                        (anonymous_formula,),
                    ).fetchone()[0]
                )
            # Prefer anonymous stoichiometries with fewer complete-corpus rows,
            # then richer chemistries and high-end site counts. This affects
            # comparison cost and proposal difficulty, never acceptance.
            menus[label].append(
                (
                    row,
                    composition,
                    len(composition.elements),
                    atom_count,
                    anonymous_exposure_counts[anonymous_formula],
                )
            )
            menu_formula_seen.add(key)
            if all(
                len(menus[f"{low}-{high}"]) >= 300
                or not any(
                    additions_needed[stream, f"{low}-{high}"]
                    for stream in ("wyckoff-enumeration", "crystal-search")
                )
                for low, high in SITE_BINS
            ):
                break
        for label in menus:
            menus[label].sort(
                key=lambda item: (
                    item[4],
                    -item[2],
                    -item[3],
                    stable_int("topup-formula", str(item[0]["record_id"])),
                )
            )

        parsed_parents: dict[str, Structure] = {}

        def load_parent(row: sqlite3.Row) -> Structure:
            parent_id = str(row["record_id"])
            if parent_id not in parsed_parents:
                payload = connection.execute(
                    "SELECT payload_format, payload, locator FROM records "
                    "WHERE source='pxrdgen_mp20' AND record_id=?",
                    (parent_id,),
                ).fetchone()
                if payload is None:
                    raise RuntimeError(f"missing top-up parent {parent_id}")
                parsed_parents[parent_id] = primitive(
                    load_structure_blob(payload[0], payload[1], payload[2])
                )
            return parsed_parents[parent_id]

        group_cycle = LOW_SYMMETRY_TOPUP_GROUPS
        topup_spacegroups: Counter[int] = Counter()
        topup_systems: Counter[str] = Counter()
        topup_round = len(manifest.get("topup_rounds", [])) + 1
        additions: list[Candidate] = []
        proposals = 0
        for stream in ("wyckoff-enumeration", "crystal-search"):
            for low, high in SITE_BINS:
                label = f"{low}-{high}"
                target = additions_needed[stream, label]
                if target == 0:
                    continue
                accepted = 0
                for row, composition, _nelements, atom_count, exposure_count in menus[label]:
                    parent_id = str(row["record_id"])
                    key = str(row["formula_key"])
                    if parent_id in used_parents or key in used_formulas:
                        continue
                    parent = load_parent(row)
                    generated_candidate: Candidate | None = None
                    for attempt in range(len(group_cycle) * 3):
                        proposals += 1
                        if proposals > 20_000:
                            raise RuntimeError("topology top-up exceeded 20,000 proposals")
                        group = group_cycle[(len(additions) + attempt) % len(group_cycle)]
                        generation_seed = stable_int(
                            "topup", stream, parent_id, str(topup_round), str(attempt)
                        ) % (2**32)
                        multiplier = max(1, high // atom_count) if high == 4 else 1
                        proposal_composition = composition * multiplier
                        generated = pyxtal_composition_candidate(
                            proposal_composition, seed=generation_seed, group=group
                        )
                        if generated is None:
                            continue
                        proposal, details = generated
                        try:
                            candidate = make_candidate(
                                stream=stream,
                                structure=proposal,
                                parent_id=parent_id,
                                parent_formula=str(row["formula"]),
                                parent_payload_sha256=sha256_bytes(
                                    explicit_p1_cif(parent).encode()
                                ),
                                generation_seed=generation_seed,
                                generation={
                                    **details,
                                    "topup_round": topup_round,
                                    "target_site_bin": label,
                                    "formula_cell_multiplier": multiplier,
                                    "anonymous_exposure_record_count": exposure_count,
                                    "formula_selection": (
                                        "unused complete-exposure formula; low anonymous-corpus "
                                        "cardinality, then chemistry richness and site count"
                                    ),
                                },
                            )
                        except Exception:
                            continue
                        if candidate.site_bin != label or candidate.formula_key != key:
                            continue
                        if topup_spacegroups[candidate.spacegroup_number] >= 8:
                            continue
                        if topup_systems[candidate.crystal_system] >= 20:
                            continue
                        if STRICT_MATCHER.fit(load_candidate(candidate), parent):
                            continue
                        generated_candidate = candidate
                        break
                    if generated_candidate is None:
                        continue
                    additions.append(generated_candidate)
                    candidates.append(generated_candidate)
                    used_formulas.add(key)
                    used_parents.add(parent_id)
                    topup_spacegroups[generated_candidate.spacegroup_number] += 1
                    topup_systems[generated_candidate.crystal_system] += 1
                    accepted += 1
                    if accepted >= target:
                        break
                if accepted != target:
                    raise RuntimeError(
                        f"top-up generated {accepted}/{target} candidates for {stream}/{label}"
                    )
                print(f"top-up {stream}/{label}: {accepted} candidates")
        manifest["candidate_count"] = len(candidates)
        manifest["candidates"] = [asdict(candidate) for candidate in candidates]
        manifest.setdefault("topup_rounds", []).append(
            {
                "round": topup_round,
                "trigger": (
                    f"fewer than {min_certified_per_bin} complete-corpus-certified "
                    "candidates in a site bin"
                ),
                "minimum_certified_per_bin": min_certified_per_bin,
                "wyckoff_buffer": wyckoff_buffer,
                "crystal_buffer": crystal_buffer,
                "proposal_count": proposals,
                "addition_count": len(additions),
                "addition_counts": {
                    f"{stream}/{label}": count
                    for (stream, label), count in sorted(additions_needed.items())
                    if count
                },
                "spacegroup_counts": dict(sorted(topup_spacegroups.items())),
                "crystal_system_counts": dict(sorted(topup_systems.items())),
            }
        )
        write_json(manifest_path, manifest)
        print(f"topology top-up appended {len(additions)} candidates")
    finally:
        connection.close()


def withdraw_dense_low_bin_topups() -> None:
    """Withdraw the first-round dense ABCD low-bin proposals from the active pool.

    Their 202,645-record anonymous bucket made them a needlessly expensive
    choice after the complete index disclosed the exact cardinality. Files and
    diagnostics remain in the ignored run directory for provenance; only active
    candidate membership changes, and the manifest records every withdrawn ID.
    """
    manifest_path = POOL / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidates = [Candidate(**item) for item in manifest["candidates"]]
    withdrawn = [
        candidate
        for candidate in candidates
        if candidate.generation.get("topup_round") == 1
        and candidate.site_bin == "1-4"
        and candidate.anonymous_formula == "ABCD"
    ]
    if len(withdrawn) != 18:
        raise RuntimeError(f"expected 18 dense low-bin top-ups, found {len(withdrawn)}")
    withdrawn_ids = {candidate.candidate_id for candidate in withdrawn}
    retained = [
        candidate for candidate in candidates if candidate.candidate_id not in withdrawn_ids
    ]
    manifest["candidate_count"] = len(retained)
    manifest["candidates"] = [asdict(candidate) for candidate in retained]
    manifest.setdefault("withdrawals", []).append(
        {
            "reason": (
                "replace low-bin ABCD proposals (202,645 anonymous exposure rows) with "
                "lower-cardinality formulas before certification; novelty rules unchanged"
            ),
            "withdrawn_count": len(withdrawn),
            "withdrawn_candidate_ids": sorted(withdrawn_ids),
            "files_retained_under_runs": True,
        }
    )
    write_json(manifest_path, manifest)
    print(f"withdrew {len(withdrawn)} dense low-bin top-up candidates")


def withdraw_dense_ab_low_bin_topups() -> None:
    """Withdraw active AB fallbacks before their topology certification."""
    manifest_path = POOL / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidates = [Candidate(**item) for item in manifest["candidates"]]
    withdrawn = [
        candidate
        for candidate in candidates
        if candidate.generation.get("topup_round", 0) >= 2
        and candidate.site_bin == "1-4"
        and candidate.anonymous_formula == "AB"
        and not (CERTIFIED / f"{candidate.candidate_id}.json").is_file()
    ]
    if len(withdrawn) not in {6, 17}:
        raise RuntimeError(f"expected 6 or 17 dense AB low-bin top-ups, found {len(withdrawn)}")
    withdrawn_ids = {candidate.candidate_id for candidate in withdrawn}
    retained = [
        candidate for candidate in candidates if candidate.candidate_id not in withdrawn_ids
    ]
    manifest["candidate_count"] = len(retained)
    manifest["candidates"] = [asdict(candidate) for candidate in retained]
    manifest.setdefault("withdrawals", []).append(
        {
            "reason": (
                "replace low-bin AB fallbacks (75,486 anonymous exposure rows) with "
                "new geometries of previously rejected elemental formulas"
            ),
            "withdrawn_count": len(withdrawn),
            "withdrawn_candidate_ids": sorted(withdrawn_ids),
            "files_retained_under_runs": True,
        }
    )
    write_json(manifest_path, manifest)
    print(f"withdrew {len(withdrawn)} dense AB low-bin top-up candidates")


def relax_crystal_search(
    *, replace: bool, limit: int | None = None, workers: int = 2
) -> None:
    candidates = [candidate for candidate in read_pool() if candidate.stream == "crystal-search"]
    if limit is not None:
        candidates = candidates[:limit]
    if workers < 1:
        raise ValueError("MACE worker count must be positive")
    python = ROOT / ".venv" / "bin" / "python"
    helper = Path(__file__).resolve().parent / "relax_pxrd_ood.py"
    if not python.is_file():
        raise RuntimeError(f"MACE runtime missing: {python}")
    if sha256_file(MACE_MODEL) != MACE_SHA256:
        raise RuntimeError("locked MACE-MH-1 checkpoint is missing or corrupt")

    def run_relaxation(
        item: tuple[int, Candidate],
    ) -> tuple[int, Candidate, Path, Path, Path, dict[str, Any] | None, str | None]:
        index, candidate = item
        current = ROOT / candidate.cif_path
        # Always reproduce from the immutable PyXtal proposal. The active pool
        # may still point at the earlier MACE-MP relaxation; retain that file as
        # provenance and write a model-specific MH-1 result beside it.
        source = current.with_name(f"{candidate.candidate_id}.cif")
        if not source.is_file():
            raise RuntimeError(f"immutable PyXtal proposal is missing: {source}")
        output = source.with_name(f"{candidate.candidate_id}-{MACE_OUTPUT_TAG}.cif")
        diagnostics = source.with_name(f"{candidate.candidate_id}-{MACE_OUTPUT_TAG}.json")
        report: dict[str, Any] | None = None
        if output.is_file() and diagnostics.is_file() and not replace:
            report = json.loads(diagnostics.read_text(encoding="utf-8"))
            if not report.get("converged"):
                return (
                    index,
                    candidate,
                    source,
                    output,
                    diagnostics,
                    report,
                    "cached MACE relaxation did not converge",
                )
        else:
            command = [
                str(python),
                str(helper),
                str(source),
                str(output),
                str(diagnostics),
                "--model",
                str(MACE_MODEL),
                "--head",
                MACE_MODEL_HEAD,
                "--fmax",
                "0.10",
                "--steps",
                "1000",
            ]
            completed = subprocess.run(command, text=True, capture_output=True, check=False)
            if completed.returncode != 0:
                if diagnostics.is_file():
                    report = json.loads(diagnostics.read_text(encoding="utf-8"))
                return (
                    index,
                    candidate,
                    source,
                    output,
                    diagnostics,
                    report,
                    f"MACE failed: {completed.stderr[-500:]}",
                )
            report = json.loads(diagnostics.read_text(encoding="utf-8"))
        return index, candidate, source, output, diagnostics, report, None

    work = list(enumerate(candidates, start=1))
    # Each MACE process is isolated and writes a distinct output. Two workers
    # match the two CPU cores provisioned for the reproducible benchmark build.
    # executor.map preserves manifest order even when a later job finishes first.
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(run_relaxation, work)
        for index, candidate, source, output, _diagnostics, report, error in results:
            candidate.mace = report
            if error is not None:
                print(f"{candidate.candidate_id}: {error}")
                active_path = source
            elif report is None or not report.get("converged"):
                active_path = source
            else:
                active_path = output
            try:
                final, validation, xrd, _ = validate_structure(Structure.from_file(active_path))
            except Exception as exc:
                print(f"{candidate.candidate_id}: active structure failed gates: {exc}")
                active_path = source
                final, validation, xrd, _ = validate_structure(Structure.from_file(active_path))
                if candidate.mace is not None:
                    candidate.mace = {
                        **candidate.mace,
                        "post_relaxation_geometry_gates_passed": False,
                        "post_relaxation_geometry_error": str(exc),
                    }
            if active_path == output:
                output.write_text(explicit_p1_cif(final), encoding="utf-8", newline="\n")
                assert candidate.mace is not None
                candidate.mace = {
                    **candidate.mace,
                    "post_relaxation_geometry_gates_passed": True,
                }
            candidate.cif_path = str(active_path.relative_to(ROOT))
            candidate.primitive_site_count = len(final)
            candidate.site_bin = site_bin(len(final))
            candidate.formula, candidate.formula_key, candidate.anonymous_formula = (
                canonical_formula(final.composition.as_dict())
            )
            candidate.spacegroup_number = SpacegroupAnalyzer(
                final, symprec=0.05, angle_tolerance=5
            ).get_space_group_number()
            candidate.crystal_system = crystal_system(candidate.spacegroup_number)
            candidate.validation = validation
            candidate.xrd = xrd
            status = "converged" if candidate.mace and candidate.mace.get("converged") else "reject"
            print(f"{MACE_MODEL_NAME} {index}/{len(candidates)} {status}: {candidate.candidate_id}")
    all_candidates = read_pool()
    updates = {candidate.candidate_id: candidate for candidate in candidates}
    merged = [updates.get(candidate.candidate_id, candidate) for candidate in all_candidates]
    manifest = json.loads((POOL / "manifest.json").read_text(encoding="utf-8"))
    manifest["candidates"] = [asdict(candidate) for candidate in merged]
    manifest["mace_relaxed_count"] = sum(
        bool(
            candidate.mace
            and candidate.mace.get("converged")
            and candidate.mace.get("model_sha256") == MACE_SHA256
            and candidate.mace.get("model_head") == MACE_MODEL_HEAD
            and candidate.mace.get("post_relaxation_geometry_gates_passed")
        )
        for candidate in merged
    )
    manifest["mace_model"] = {
        "name": MACE_MODEL_NAME,
        "head": MACE_MODEL_HEAD,
        "url": MACE_MODEL_URL,
        "sha256": MACE_SHA256,
    }
    write_json(POOL / "manifest.json", manifest)
    crystal_candidates = [
        candidate for candidate in merged if candidate.stream == "crystal-search"
    ]
    compatible = [
        candidate
        for candidate in crystal_candidates
        if candidate.mace
        and candidate.mace.get("model_name") == MACE_MODEL_NAME
        and candidate.mace.get("model_sha256") == MACE_SHA256
        and candidate.mace.get("model_head") == MACE_MODEL_HEAD
    ]
    accepted = [
        candidate
        for candidate in compatible
        if candidate.mace
        and candidate.mace.get("converged")
        and candidate.mace.get("post_relaxation_geometry_gates_passed")
    ]
    write_json(
        CACHE / f"{MACE_OUTPUT_TAG}-relaxation-report.json",
        {
            "schema_version": "1.0.0",
            "model": manifest["mace_model"],
            "optimizer": {
                "name": "ASE FIRE + FrechetCellFilter + FixSymmetry",
                "fmax_ev_per_angstrom": 0.10,
                "max_steps": 1000,
            },
            "proposal_count": len(crystal_candidates),
            "model_diagnostic_count": len(compatible),
            "accepted_relaxation_count": len(accepted),
            "rejected_or_incomplete_count": len(crystal_candidates) - len(accepted),
            "accepted_by_site_bin": dict(
                sorted(Counter(candidate.site_bin for candidate in accepted).items())
            ),
            "rejected_or_incomplete_candidate_ids": sorted(
                candidate.candidate_id
                for candidate in crystal_candidates
                if candidate not in accepted
            ),
            "candidates": [
                {
                    "candidate_id": candidate.candidate_id,
                    "active_cif_path": candidate.cif_path,
                    "site_bin": candidate.site_bin,
                    "diagnostics": candidate.mace,
                }
                for candidate in crystal_candidates
            ],
        },
    )


def certify_candidate(
    connection: sqlite3.Connection,
    candidate: Candidate,
    *,
    anonymous_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    structure = load_candidate(candidate)
    hits = formula_hits(connection, candidate.formula_key)
    strict: dict[str, Any] = {}
    strict_hit = False
    for source in REQUIRED_SOURCES:
        match, compared, failures, structureless = any_match(
            connection,
            structure,
            source=source,
            field="formula_key",
            value=candidate.formula_key,
            anonymous=False,
        )
        strict[source] = {
            "match_id": match,
            "structures_compared": compared,
            "unparseable_candidates": failures,
            "structureless_catalog_records": structureless,
        }
        strict_hit |= match is not None
    strict_unparseable = sum(item["unparseable_candidates"] for item in strict.values())
    certificate: dict[str, Any] = {
        "formula_hits": hits,
        "strict_structure": strict,
        "strict_structure_absent": not strict_hit and strict_unparseable == 0,
        "matcher": {
            "ltol": 0.20,
            "stol": 0.30,
            "angle_tol": 5,
            "primitive_cell": True,
            "scale": True,
            "attempt_supercell": False,
        },
    }
    if candidate.stream in {"substitution", "ordered-decoration"}:
        parent = connection.execute(
            "SELECT payload_format, payload, locator FROM records "
            "WHERE source='pxrdgen_mp20' AND record_id=?",
            (candidate.parent_id,),
        ).fetchone()
        if parent is None:
            raise RuntimeError(f"missing parent {candidate.parent_id}")
        parent_structure = load_structure_blob(parent[0], parent[1], parent[2])
        geometry_match = GEOMETRY_MATCHER.fit(
            erased_species(structure), erased_species(parent_structure)
        )
        parent_evidence = candidate.generation.get("familiar_parent_exposure", {})
        parent_exposed_in_noma_and_jarvis = all(
            parent_evidence.get(source, {}).get("anonymous_match_id")
            for source in ("decifer_noma", "jarvis_dft_2022")
        )
        certificate.update(
            {
                "composition_novel": all(value == 0 for value in hits.values()),
                "topology_familiar": bool(geometry_match and parent_exposed_in_noma_and_jarvis),
                "topology_parent_id": candidate.parent_id,
                "topology_parent_exposed_in_noma_and_jarvis": bool(
                    parent_exposed_in_noma_and_jarvis
                ),
            }
        )
    else:
        if anonymous_result is None:
            anonymous: dict[str, Any] = {}
            for source in REQUIRED_SOURCES:
                match, compared, failures, structureless = any_match(
                    connection,
                    structure,
                    source=source,
                    field="anonymous_formula",
                    value=candidate.anonymous_formula,
                    anonymous=True,
                )
                anonymous[source] = {
                    "match_id": match,
                    "structures_compared": compared,
                    "unparseable_candidates": failures,
                    "structureless_catalog_records": structureless,
                }
        else:
            anonymous = anonymous_result
        anonymous_hit = any(item["match_id"] is not None for item in anonymous.values())
        anonymous_unparseable = sum(item["unparseable_candidates"] for item in anonymous.values())
        certificate.update(
            {
                "composition_familiar": all(hits[source] > 0 for source in LEARNED_SOURCES)
                and sum(hits[source] for source in RETRIEVAL_SOURCES) > 0,
                "anonymous_structure": anonymous,
                "topology_novel": not anonymous_hit and anonymous_unparseable == 0,
                "topology_definition": (
                    "pymatgen StructureMatcher.fit_anonymous equivalence among every frozen "
                    "record with the same anonymized reduced formula"
                ),
            }
        )
    if candidate.stream == "crystal-search":
        certificate["mace_crystal_search_complete"] = bool(
            candidate.mace
            and candidate.mace.get("converged")
            and candidate.mace.get("model_name") == MACE_MODEL_NAME
            and candidate.mace.get("model_sha256") == MACE_SHA256
            and candidate.mace.get("model_head") == MACE_MODEL_HEAD
            and candidate.mace.get("post_relaxation_geometry_gates_passed")
        )
    certificate["passes_frozen_corpus_rules"] = bool(
        certificate["strict_structure_absent"]
        and (
            certificate.get("composition_novel") and certificate.get("topology_familiar")
            if candidate.stream in {"substitution", "ordered-decoration"}
            else certificate.get("composition_familiar") and certificate.get("topology_novel")
        )
        and (certificate.get("mace_crystal_search_complete", True))
    )
    return certificate


def batch_anonymous_matches(
    connection: sqlite3.Connection, candidates: list[Candidate]
) -> dict[str, dict[str, Any]]:
    """Match one anonymous-formula group while parsing each reference once.

    The result is byte-for-byte equivalent to calling ``any_match`` separately:
    candidates stop accumulating comparisons and parse failures after their first
    match, and source records retain their locked record-ID order. This matters for
    common anonymous formulas shared by many generated candidates, where repeated
    CIF parsing would otherwise dominate the complete-corpus audit.
    """
    if not candidates:
        return {}
    anonymous_formula = candidates[0].anonymous_formula
    if any(candidate.anonymous_formula != anonymous_formula for candidate in candidates):
        raise ValueError("batch topology matcher received mixed anonymous formulas")
    # Use the exact private reduction routine invoked by StructureMatcher, but
    # cache its output for the group. The generation environment is hash-locked,
    # and the final audit repeats the public fit_anonymous call independently.
    structures = {
        candidate.candidate_id: ANONYMOUS_MATCHER._get_reduced_structure(
            load_candidate(candidate), primitive_cell=True, niggli=True
        )
        for candidate in candidates
    }
    results: dict[str, dict[str, Any]] = {
        candidate.candidate_id: {} for candidate in candidates
    }
    ordered_ids = [candidate.candidate_id for candidate in candidates]
    for source in REQUIRED_SOURCES:
        states = {
            candidate_id: {
                "match_id": None,
                "structures_compared": 0,
                "unparseable_candidates": 0,
                "structureless_catalog_records": 0,
            }
            for candidate_id in ordered_ids
        }
        active = set(ordered_ids)
        for row in source_records(
            connection,
            source=source,
            field="anonymous_formula",
            value=anonymous_formula,
        ):
            if row["payload_format"] == "cod-id-only":
                continue
            try:
                reference = load_structure_blob(
                    row["payload_format"], row["payload"], row["locator"]
                )
            except StructureUnavailableError:
                for candidate_id in active:
                    states[candidate_id]["structureless_catalog_records"] += 1
                continue
            except Exception:
                for candidate_id in active:
                    states[candidate_id]["unparseable_candidates"] += 1
                continue
            try:
                reduced_reference = ANONYMOUS_MATCHER._get_reduced_structure(
                    reference, primitive_cell=True, niggli=True
                )
            except Exception:
                for candidate_id in active:
                    states[candidate_id]["structures_compared"] += 1
                    states[candidate_id]["unparseable_candidates"] += 1
                continue
            for candidate_id in ordered_ids:
                if candidate_id not in active:
                    continue
                states[candidate_id]["structures_compared"] += 1
                if len(structures[candidate_id]) != len(reduced_reference):
                    continue
                try:
                    matched = ANONYMOUS_MATCHER.fit_anonymous(
                        structures[candidate_id],
                        reduced_reference,
                        niggli=False,
                        skip_structure_reduction=True,
                    )
                except Exception:
                    states[candidate_id]["unparseable_candidates"] += 1
                    continue
                if matched:
                    states[candidate_id]["match_id"] = str(row["record_id"])
                    active.remove(candidate_id)
            if not active:
                break
        for candidate_id in ordered_ids:
            results[candidate_id][source] = states[candidate_id]
    return results


_TOPOLOGY_WORKER_CONNECTION: sqlite3.Connection | None = None


def initialize_topology_worker() -> None:
    global _TOPOLOGY_WORKER_CONNECTION
    _TOPOLOGY_WORKER_CONNECTION = open_index()


def match_topology_group(
    task: tuple[str, list[dict[str, Any]]],
) -> tuple[str, dict[str, dict[str, Any]]]:
    anonymous_formula, raw_candidates = task
    if _TOPOLOGY_WORKER_CONNECTION is None:
        raise RuntimeError("topology worker was not initialized")
    candidates = [Candidate(**item) for item in raw_candidates]
    return anonymous_formula, batch_anonymous_matches(_TOPOLOGY_WORKER_CONNECTION, candidates)


def load_topology_match_cache(candidates: list[Candidate]) -> dict[str, dict[str, Any]]:
    """Load exact externally-sharded matches only when every input remains hash-bound."""

    if not TOPOLOGY_MATCH_CACHE.is_file():
        return {}
    cache = json.loads(TOPOLOGY_MATCH_CACHE.read_text(encoding="utf-8"))
    expected_matcher = {
        "ltol": 0.20,
        "stol": 0.30,
        "angle_tol": 5,
        "primitive_cell": True,
        "scale": True,
        "attempt_supercell": False,
    }
    if cache.get("matcher") != expected_matcher:
        raise RuntimeError("external topology-match cache uses different matcher settings")
    if cache.get("topology_index_sha256") != sha256_file(TOPOLOGY_INDEX):
        raise RuntimeError("external topology-match cache uses a different frozen subset")
    if cache.get("pool_manifest_sha256") != sha256_file(POOL / "manifest.json"):
        raise RuntimeError("external topology-match cache uses a different candidate pool")
    runtime_versions = {
        str(record.get("pymatgen_version")) for record in cache.get("runtime_records", [])
    }
    if runtime_versions != {version("pymatgen")}:
        raise RuntimeError(
            "external topology-match cache was produced by a different pymatgen runtime"
        )

    cached_hashes = cache.get("candidate_cif_sha256", {})
    cached_results = cache.get("results", {})
    results: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        candidate_id = candidate.candidate_id
        if candidate_id not in cached_results:
            continue
        path = ROOT / candidate.cif_path
        if cached_hashes.get(candidate_id) != sha256_file(path):
            raise RuntimeError(f"{candidate_id}: external topology-match CIF digest mismatch")
        result = cached_results[candidate_id]
        if set(result) != set(REQUIRED_SOURCES):
            raise RuntimeError(f"{candidate_id}: incomplete externally-sharded source coverage")
        for source, record in result.items():
            if set(record) != {
                "match_id",
                "structures_compared",
                "unparseable_candidates",
                "structureless_catalog_records",
            }:
                raise RuntimeError(
                    f"{candidate_id}/{source}: malformed externally-sharded match record"
                )
        results[candidate_id] = result
    if results:
        print(
            f"topology cache: {len(results)} exact candidate results from "
            f"{cache.get('worker_count')} Modal workers"
        )
    return results


def certify_pool(
    *, replace: bool, workers: int = 2, use_topology_match_cache: bool = True
) -> None:
    if workers < 1:
        raise ValueError("certification worker count must be positive")
    connection = open_index()
    try:
        assert_complete_sources(connection)
        candidates = read_pool()
        CERTIFIED.mkdir(parents=True, exist_ok=True)
        # Certificate replacement does not invalidate the independently
        # hash-bound physical layout of candidate-relevant exposure rows.
        prepare_topology_index(connection, candidates, replace=False)
        anonymous_results = (
            load_topology_match_cache(candidates) if use_topology_match_cache else {}
        )
        pending_groups: dict[str, list[Candidate]] = defaultdict(list)
        for candidate in candidates:
            path = CERTIFIED / f"{candidate.candidate_id}.json"
            if (
                candidate.stream in {"wyckoff-enumeration", "crystal-search"}
                and (replace or not path.is_file())
                and candidate.candidate_id not in anonymous_results
            ):
                pending_groups[candidate.anonymous_formula].append(candidate)
        topology_tasks = [
            (
                anonymous_formula,
                [asdict(candidate) for candidate in pending_groups[anonymous_formula]],
            )
            for anonymous_formula in sorted(pending_groups)
        ]
        with ProcessPoolExecutor(
            max_workers=workers, initializer=initialize_topology_worker
        ) as executor:
            matched_groups = executor.map(match_topology_group, topology_tasks, chunksize=1)
            for group_index, (anonymous_formula, matched) in enumerate(
                matched_groups, start=1
            ):
                anonymous_results.update(matched)
                print(
                    f"topology group {group_index}/{len(topology_tasks)} "
                    f"{anonymous_formula}: {len(pending_groups[anonymous_formula])} candidates"
                )
        output: list[Candidate] = []
        for index, candidate in enumerate(candidates, start=1):
            path = CERTIFIED / f"{candidate.candidate_id}.json"
            if path.is_file() and not replace:
                candidate.certificate = json.loads(path.read_text(encoding="utf-8"))
            else:
                candidate.certificate = certify_candidate(
                    connection,
                    candidate,
                    anonymous_result=anonymous_results.get(candidate.candidate_id),
                )
                write_json(path, candidate.certificate)
            if candidate.certificate["passes_frozen_corpus_rules"]:
                output.append(candidate)
            print(
                f"certify {index}/{len(candidates)} {candidate.candidate_id}: "
                f"{'PASS' if candidate.certificate['passes_frozen_corpus_rules'] else 'reject'}"
            )
        write_json(
            CERTIFIED / "manifest.json",
            {
                "schema_version": "1.0.0",
                "source_index_sha256": sha256_file(INDEX),
                "candidate_count": len(candidates),
                "certified_count": len(output),
                "candidates": [asdict(candidate) for candidate in output],
            },
        )
    finally:
        connection.close()


def coordination_fingerprint(structure: Structure) -> tuple[tuple[int, int], ...]:
    """Return a deterministic, chemistry-aware near-neighbor histogram."""
    coordination_numbers: list[int] = []
    for site in structure:
        center_radius = element_radius(site.specie.symbol)
        count = 0
        for neighbor in structure.get_neighbors(site, 4.5):
            neighbor_radius = element_radius(neighbor.specie.symbol)
            if neighbor.nn_distance <= 1.25 * (center_radius + neighbor_radius):
                count += 1
        coordination_numbers.append(count)
    return tuple(sorted(Counter(coordination_numbers).items()))


def xrd_signature(profile: np.ndarray) -> tuple[int, ...]:
    """Coarsen the strongest local maxima into a selection-diversity key."""
    if len(profile) < 3:
        return ()
    maxima = np.flatnonzero((profile[1:-1] >= profile[:-2]) & (profile[1:-1] > profile[2:])) + 1
    strongest = sorted(maxima, key=lambda index: (-profile[index], int(index)))[:8]
    # 0.5-degree bins prevent insignificant numerical shifts from creating a
    # distinct signature while retaining the gross powder-pattern topology.
    return tuple(sorted(round((5.0 + 0.05 * int(index)) * 2) for index in strongest))


def selection_exclusions(manifest_path: Path | None) -> dict[str, Any] | None:
    if manifest_path is None:
        return None
    path = manifest_path.expanduser().resolve()
    manifest = json.loads(path.read_text(encoding="utf-8"))
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise RuntimeError(f"exclusion manifest has no cases: {path}")
    candidate_ids = {
        str(case.get("generation", {}).get("candidate_id"))
        for case in cases
        if case.get("generation", {}).get("candidate_id")
    }
    formula_keys = {
        str(case["reduced_formula_key"])
        for case in cases
        if case.get("reduced_formula_key")
    }
    parent_ids = {
        str(case.get("generation", {}).get("parent_id"))
        for case in cases
        if case.get("generation", {}).get("parent_id")
    }
    if len(candidate_ids) != len(cases):
        raise RuntimeError(
            f"exclusion manifest does not identify one candidate per case: {path}"
        )
    return {
        "path": path,
        "dataset_id": manifest.get("dataset_id"),
        "manifest_sha256": sha256_file(path),
        "case_count": len(cases),
        "candidate_ids": candidate_ids,
        "formula_keys": formula_keys,
        "parent_ids": parent_ids,
    }


def selected_candidates(
    *,
    selection_seed: int = SEED,
    exclusions: dict[str, Any] | None = None,
    certified_manifest: Path = CERTIFIED / "manifest.json",
) -> list[Candidate]:
    data = json.loads(certified_manifest.read_text(encoding="utf-8"))
    candidates = [Candidate(**item) for item in data["candidates"]]
    pxrd100_formulas = existing_pxrd100_formulas()
    candidates = [
        candidate
        for candidate in candidates
        if candidate.formula_key not in pxrd100_formulas
    ]
    if exclusions is not None:
        candidates = [
            candidate
            for candidate in candidates
            if candidate.candidate_id not in exclusions["candidate_ids"]
            and candidate.formula_key not in exclusions["formula_keys"]
            and candidate.parent_id not in exclusions["parent_ids"]
        ]
    if not candidates:
        raise RuntimeError("no certified candidates are available")

    structures = [load_candidate(candidate) for candidate in candidates]
    profiles = [xrd_metrics(structure)[1] for structure in structures]
    chemistry_keys = [
        tuple(sorted({site.specie.symbol for site in structure})) for structure in structures
    ]
    coordination_keys = [coordination_fingerprint(structure) for structure in structures]
    xrd_keys = [xrd_signature(profile) for profile in profiles]
    chemistry_frequency = Counter(chemistry_keys)
    coordination_frequency = Counter(coordination_keys)
    xrd_frequency = Counter(xrd_keys)

    spacegroups = sorted({candidate.spacegroup_number for candidate in candidates})
    sg_variable = {
        spacegroup: len(candidates) + index for index, spacegroup in enumerate(spacegroups)
    }
    variable_count = len(candidates) + len(spacegroups)
    coefficient_rows: list[dict[int, float]] = []
    lower: list[float] = []
    upper: list[float] = []

    def add_constraint(coefficients: dict[int, float], low: float, high: float) -> None:
        coefficient_rows.append(coefficients)
        lower.append(low)
        upper.append(high)

    # Exactly five candidates from every stream/site-count bucket.
    for stream in STREAMS:
        for low_site, high_site in SITE_BINS:
            label = f"{low_site}-{high_site}"
            indexes = [
                index
                for index, candidate in enumerate(candidates)
                if candidate.stream == stream and candidate.site_bin == label
            ]
            if len(indexes) < 5:
                raise RuntimeError(f"only {len(indexes)} certified candidates for {stream}/{label}")
            add_constraint({index: 1.0 for index in indexes}, 5.0, 5.0)

    # Unique formulas and parents are hard constraints even though generation
    # normally makes them unique before certification.
    for values in (
        [candidate.formula_key for candidate in candidates],
        [candidate.parent_id for candidate in candidates],
    ):
        groups: dict[str, list[int]] = defaultdict(list)
        for index, value in enumerate(values):
            groups[value].append(index)
        for indexes in groups.values():
            if len(indexes) > 1:
                add_constraint({index: 1.0 for index in indexes}, 0.0, 1.0)

    # No final space group may occur more than four times.  Binary helper
    # variables reward activating additional space groups in the MILP objective.
    for spacegroup in spacegroups:
        indexes = [
            index
            for index, candidate in enumerate(candidates)
            if candidate.spacegroup_number == spacegroup
        ]
        add_constraint({index: 1.0 for index in indexes}, 0.0, 4.0)
        coefficients = {index: -1.0 for index in indexes}
        coefficients[sg_variable[spacegroup]] = 1.0
        add_constraint(coefficients, -np.inf, 0.0)

    # Represent all seven systems and cap each at 20 cases.
    for system in PYXTAL_GROUPS:
        indexes = [
            index
            for index, candidate in enumerate(candidates)
            if candidate.crystal_system == system
        ]
        if not indexes:
            raise RuntimeError(f"certified pool has no {system} candidate")
        add_constraint({index: 1.0 for index in indexes}, 1.0, 20.0)

    # Reject essentially identical powder patterns before optimization.
    normalized_profiles = np.asarray(
        [profile / np.linalg.norm(profile) for profile in profiles], dtype=np.float64
    )
    similarities = normalized_profiles @ normalized_profiles.T
    for left in range(len(candidates)):
        for right in np.flatnonzero(similarities[left, left + 1 :] >= 0.9999):
            actual_right = left + 1 + int(right)
            add_constraint({left: 1.0, actual_right: 1.0}, 0.0, 1.0)

    # Also forbid duplicate species-erased primitive geometries.  Equal
    # primitive site count is a safe prefilter for this no-supercell matcher.
    by_site_count: dict[int, list[int]] = defaultdict(list)
    for index, structure in enumerate(structures):
        by_site_count[len(structure)].append(index)
    erased = [erased_species(structure) for structure in structures]
    for indexes in by_site_count.values():
        for offset, left in enumerate(indexes):
            for right in indexes[offset + 1 :]:
                if STRICT_MATCHER.fit(erased[left], erased[right]):
                    add_constraint({left: 1.0, right: 1.0}, 0.0, 1.0)

    matrix = lil_matrix((len(coefficient_rows), variable_count), dtype=np.float64)
    for row_index, coefficients in enumerate(coefficient_rows):
        for column, value in coefficients.items():
            matrix[row_index, column] = value

    objective = np.zeros(variable_count, dtype=np.float64)
    for index, candidate in enumerate(candidates):
        rarity = (
            10_000.0 / chemistry_frequency[chemistry_keys[index]]
            + 1_000.0 / coordination_frequency[coordination_keys[index]]
            + 100.0 / xrd_frequency[xrd_keys[index]]
        )
        tie_break = (
            seeded_int(selection_seed, candidate.candidate_id) % 1_000_000
        ) / 1_000_000.0
        objective[index] = -rarity + tie_break
    for variable in sg_variable.values():
        objective[variable] = -10_000_000.0

    result = milp(
        c=objective,
        integrality=np.ones(variable_count, dtype=np.int8),
        bounds=Bounds(np.zeros(variable_count), np.ones(variable_count)),
        constraints=LinearConstraint(matrix.tocsr(), np.asarray(lower), np.asarray(upper)),
        options={"time_limit": 300.0, "mip_rel_gap": 0.0},
    )
    if not result.success or result.x is None:
        raise RuntimeError(f"deterministic diversity selection failed: {result.message}")
    selected = [candidate for index, candidate in enumerate(candidates) if result.x[index] >= 0.5]
    selected.sort(
        key=lambda candidate: (
            STREAMS.index(candidate.stream),
            tuple(f"{low}-{high}" for low, high in SITE_BINS).index(candidate.site_bin),
            seeded_int(selection_seed, candidate.candidate_id),
        )
    )
    if len(selected) != EXPECTED_CASES:
        raise RuntimeError(f"MILP selected {len(selected)} candidates, expected 100")
    return selected


def build_output(
    *,
    replace: bool,
    output: Path = OUTPUT,
    dataset_id: str = "pXRD-ood-v1",
    case_prefix: str = "pxrdood",
    selection_seed: int = SEED,
    selection_date: str = SELECTION_DATE,
    exclude_manifest: Path | None = None,
    certified_manifest: Path = CERTIFIED / "manifest.json",
) -> None:
    output = output.expanduser().resolve()
    certified_manifest = certified_manifest.expanduser().resolve()
    exclusions = selection_exclusions(exclude_manifest)
    selected = selected_candidates(
        selection_seed=selection_seed,
        exclusions=exclusions,
        certified_manifest=certified_manifest,
    )
    staging = CACHE / f"staging-{case_prefix}"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    cases: list[dict[str, Any]] = []
    stream_counts: Counter[str] = Counter()
    for candidate in selected:
        stream_counts[candidate.stream] += 1
        index = stream_counts[candidate.stream]
        prefix = {
            "substitution": "cf-sub",
            "ordered-decoration": "cf-dec",
            "wyckoff-enumeration": "tn-wyc",
            "crystal-search": "tn-css",
        }[candidate.stream]
        case_id = f"{case_prefix}-{prefix}-{index:03d}"
        relative_dir = Path(PATH_BY_STREAM[candidate.stream])
        relative = relative_dir / f"{case_id}.cif"
        target = staging / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        structure = load_candidate(candidate)
        target.write_text(explicit_p1_cif(structure), encoding="utf-8", newline="\n")
        # The exported CIF is the benchmark truth. Reparse that exact byte
        # representation and derive every structural/XRD field from it so the
        # manifest cannot retain stale pre-serialization floating-point values.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            serialized = Structure.from_file(target)
        final, final_validation, final_xrd, _ = validate_structure(serialized)
        final_formula, final_formula_key, final_anonymous_formula = canonical_formula(
            final.composition.as_dict()
        )
        final_analyzer = SpacegroupAnalyzer(final, symprec=0.05, angle_tolerance=5)
        final_spacegroup = final_analyzer.get_space_group_number()
        digest = sha256_file(target)
        cases.append(
            {
                "case_id": case_id,
                "panel": PANEL_BY_STREAM[candidate.stream],
                "stream": candidate.stream,
                "path": relative.as_posix(),
                "sha256": digest,
                "formula": final_formula,
                "reduced_formula_key": final_formula_key,
                "anonymous_formula": final_anonymous_formula,
                "elements": sorted(element.symbol for element in serialized.composition.elements),
                "nelements": len(serialized.composition.elements),
                "cif_site_count": len(serialized),
                "primitive_site_count": len(final),
                "spacegroup_number": final_spacegroup,
                "crystal_system": crystal_system(final_spacegroup),
                "volume_angstrom3": float(serialized.volume),
                "volume_per_atom_angstrom3": float(serialized.volume / len(serialized)),
                "density_g_cm3": float(serialized.density),
                "xrd_selection_metrics": final_xrd,
                "generation": {
                    **candidate.generation,
                    "candidate_id": candidate.candidate_id,
                    "generation_seed": candidate.generation_seed,
                    "parent_id": candidate.parent_id,
                    "parent_formula": candidate.parent_formula,
                    "parent_payload_sha256": candidate.parent_payload_sha256,
                    "mace": candidate.mace,
                },
                "validation": final_validation,
                "novelty": candidate.certificate,
                "baseline_support": {
                    "common_element_vocabulary": True,
                    "primitive_site_count_at_most_20": True,
                    "ordered_full_occupancy": True,
                },
            }
        )
    manifest = {
        "schema_version": "1.0.0",
        "dataset_id": dataset_id,
        "selection_date": selection_date,
        "selection_seed": selection_seed,
        "description": "100 newly generated, complete-frozen-corpus-certified pXRD OOD crystals",
        "panel_counts": dict(Counter(case["panel"] for case in cases)),
        "stream_counts": dict(stream_counts),
        "source_lock_sha256": sha256_file(SOURCE_LOCK),
        "source_index_sha256": sha256_file(INDEX),
        "derived_topology_index_sha256": sha256_file(TOPOLOGY_INDEX),
        "certified_pool_manifest_path": str(certified_manifest.relative_to(ROOT)),
        "certified_pool_manifest_sha256": sha256_file(certified_manifest),
        "cases": cases,
    }
    if exclusions is not None:
        try:
            exclusion_path = exclusions["path"].relative_to(output)
        except ValueError:
            exclusion_path = Path(os.path.relpath(exclusions["path"], output))
        manifest["selection_exclusion"] = {
            "dataset_id": exclusions["dataset_id"],
            "manifest_path": exclusion_path.as_posix(),
            "manifest_sha256": exclusions["manifest_sha256"],
            "case_count": exclusions["case_count"],
            "candidate_overlap_allowed": False,
            "formula_overlap_allowed": False,
            "parent_overlap_allowed": False,
        }
    write_json(staging / "manifest.json", manifest)
    with (staging / "manifest.csv").open("w", encoding="utf-8", newline="") as stream:
        fields = [
            "case_id",
            "panel",
            "stream",
            "formula",
            "primitive_site_count",
            "spacegroup_number",
            "crystal_system",
            "path",
            "sha256",
        ]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: case[key] for key in fields} for case in cases)
    shutil.copy2(SOURCE_LOCK, staging / "SOURCE.lock.json")
    selected_mace = [
        case["generation"]["mace"]
        for case in cases
        if case["stream"] == "crystal-search" and case["generation"].get("mace")
    ]
    generation_lock = {
        "schema_version": "1.0.0",
        "selection_seed": selection_seed,
        "environment_lock_path": str(GENERATION_ENV_LOCK.relative_to(ROOT)),
        "environment_lock_sha256": sha256_file(GENERATION_ENV_LOCK),
        "python": sys.version.split()[0],
        "packages": {
            package: version(package)
            for package in (
                "ase",
                "numpy",
                "pyarrow",
                "pymatgen",
                "pyxtal",
                "scipy",
                "spglib",
            )
        },
        "mace": {
            "model": MACE_MODEL_NAME,
            "head": MACE_MODEL_HEAD,
            "model_url": MACE_MODEL_URL,
            "model_sha256": MACE_SHA256,
            "fmax_ev_per_angstrom": 0.10,
            "max_steps": 1000,
            "optimizer": "ASE FIRE + FrechetCellFilter + FixSymmetry",
            "execution": {
                "backends": sorted(
                    {str(record.get("execution_backend", "local")) for record in selected_mace}
                ),
                "device_names": sorted(
                    {
                        str(record["device_name"])
                        for record in selected_mace
                        if record.get("device_name")
                    }
                ),
                "modal_run_ids": sorted(
                    {
                        str(record["modal"]["run_id"])
                        for record in selected_mace
                        if record.get("modal")
                    }
                ),
                "modal_gpu_types": sorted(
                    {
                        str(record["modal"]["gpu_type"])
                        for record in selected_mace
                        if record.get("modal")
                    }
                ),
                "modal_worker_counts": sorted(
                    {
                        int(record["modal"]["worker_count"])
                        for record in selected_mace
                        if record.get("modal")
                    }
                ),
            },
        },
        "derived_topology_index": {
            "path": str(TOPOLOGY_INDEX.relative_to(ROOT)),
            "sha256": manifest["derived_topology_index_sha256"],
            "role": (
                "candidate-keyed physical-layout cache; frozen exposure index remains "
                "authoritative"
            ),
        },
        "structure_matcher": manifest["cases"][0]["novelty"]["matcher"],
    }
    write_json(staging / "GENERATION.lock.json", generation_lock)
    novelty_report = {
        "certificate_status": "complete",
        "scope": list(REQUIRED_SOURCES),
        "case_count": len(cases),
        "composition_novel_count": sum(
            bool(case["novelty"].get("composition_novel")) for case in cases
        ),
        "topology_novel_count": sum(bool(case["novelty"].get("topology_novel")) for case in cases),
        "strict_structure_absent_count": sum(
            bool(case["novelty"]["strict_structure_absent"]) for case in cases
        ),
        "definition": (
            "Novelty is relative to the exact hashes in SOURCE.lock.json and the declared "
            "pymatgen StructureMatcher tolerances; it is not a universal mathematical claim."
        ),
    }
    write_json(staging / "novelty-report.json", novelty_report)
    selection_report = {
        "selection_seed": selection_seed,
        "certified_pool_manifest_sha256": manifest["certified_pool_manifest_sha256"],
        "stream_counts": dict(stream_counts),
        "site_bin_counts_by_stream": {
            stream: dict(
                Counter(
                    site_bin(case["primitive_site_count"])
                    for case in cases
                    if case["stream"] == stream
                )
            )
            for stream in STREAMS
        },
        "spacegroup_counts": dict(
            sorted(Counter(case["spacegroup_number"] for case in cases).items())
        ),
        "crystal_system_counts": dict(
            sorted(Counter(case["crystal_system"] for case in cases).items())
        ),
    }
    if exclusions is not None:
        selection_report["excluded_panel"] = {
            "dataset_id": exclusions["dataset_id"],
            "manifest_sha256": exclusions["manifest_sha256"],
            "excluded_case_count": exclusions["case_count"],
            "selected_candidate_overlap_count": 0,
            "selected_formula_overlap_count": 0,
            "selected_parent_overlap_count": 0,
        }
    write_json(staging / "selection-report.json", selection_report)
    exclusion_readme = (
        ""
        if exclusions is None
        else (
            f"\nThis panel excludes every candidate, reduced formula, and generation "
            f"parent in `{exclusions['dataset_id']}`; the source manifest and digest "
            "are recorded in `manifest.json`.\n"
        )
    )
    (staging / "README.md").write_text(
        f"""# {dataset_id}

This directory contains 100 newly generated, ordered periodic structures for a
composition-plus-powder-XRD out-of-distribution benchmark. The four generation
streams contain 25 cases each. `manifest.json` is authoritative and every case
contains a frozen-corpus novelty certificate.
{exclusion_readme}

The truth layout is:

- `composition-novel-topology-familiar/substitution/`: 25 isovalent substitutions;
- `composition-novel-topology-familiar/ordered-decoration/`: 25 ordered decorations;
- `topology-novel/wyckoff-enumeration/`: 25 PyXtal symmetry/Wyckoff candidates; and
- `topology-novel/crystal-search/`: 25 MACE-MH-1-relaxed crystal-search candidates.

Each stream has exactly five primitive structures in each site-count bin 1--4,
5--8, 9--12, 13--16, and 17--20. Formulas and familiar-topology parents are unique,
all seven crystal systems occur, no final space group occurs more than four times,
and no formula overlaps `pXRD-100`.

`SOURCE.lock.json` records the frozen exposure boundary and source/index hashes;
`GENERATION.lock.json` records software and model hashes; `novelty-report.json` and
`selection-report.json` summarize the machine-audited certificates and quotas.

The crystals are geometrically valid but are not claimed to be thermodynamically
stable, dynamically stable, synthesizable, or universally novel. Ground-truth CIFs
and provenance must remain hidden from evaluated agents; use `export-blind`.
""",
        encoding="utf-8",
    )
    (staging / "SELECTION.md").write_text(
        """# Selection and novelty protocol

All candidate formulas and structures are checked against the complete frozen
source boundary in `SOURCE.lock.json`. Composition-novel cases have zero reduced-
formula hits and retain a species-erased match to a known parent. Topology-novel
cases use formulas exposed in every learned-model corpus and at least one retrieval
catalog, but have no `StructureMatcher.fit_anonymous` match under the locked
tolerances. Baseline outputs never participate in selection.

The exposure union covers the exact Crystalyze and PXRDGen MP-20 releases, every
tuple in the released deCIFer NOMA archive, the official and released DiffractGPT
JARVIS datasets, DARA's bundled public-COD index, a complete official COD rsync
mirror snapshot dated 2026-07-06 plus every official live-only CIF through
2026-07-19, and a complete Materials Project 2026.04.13 snapshot. DARA's licensed
ICSD corpus and the unpublished AGAPI-XRD server revision remain explicitly
unchecked; the public JARVIS/COD stores reported for AGAPI-XRD are frozen here.

Strict structure absence uses `StructureMatcher` with `ltol=0.20`, `stol=0.30`,
`angle_tol=5`, primitive reduction and scale normalization. Topology novelty uses
`fit_anonymous` over every reference with the same anonymized reduced formula.
Every final audit recomputes formula, strict-structure, and topology certificates
from the frozen SQLite index rather than trusting the copied manifest result.
""",
        encoding="utf-8",
    )
    (staging / "FRAMEWORKS.md").write_text(
        """# Framework exposure and input contract

The novelty boundary covers Crystalyze, PXRDGen, deCIFer, DiffractGPT, DARA, and
AGAPI-XRD as classified in `SOURCE.lock.json`. A certificate is relative to those
locked public artifacts and matcher tolerances, not a claim of universal novelty.

Evaluated systems receive reduced composition plus the blind Cu K-alpha-1 powder
pattern only. Do not mount this truth directory, parent IDs, generation metadata,
or novelty evidence into an agent or baseline environment. Run
`build_pxrd_ood.py export-blind DESTINATION` to create the permissible input tree.
""",
        encoding="utf-8",
    )
    (staging / "targets").mkdir()
    (staging / "targets" / "README.md").write_text(
        f"""# Framework-native targets

After the truth corpus passes its complete novelty audit, the pinned target
builders populate `crystalyze/`, `pxrdgen/`, `decifer/`, and `diffractgpt/`.
Every adapter is bound to dataset ID `{dataset_id}`, case prefix `{case_prefix}`, and
the `require-all` common support policy; each framework manifest records the
source-manifest digest and all generated-file digests.
""",
        encoding="utf-8",
    )
    (staging / "results").mkdir()
    (staging / "results" / "README.md").write_text(
        "Evaluation results are generated separately from the locked truth and targets.\n",
        encoding="utf-8",
    )
    audit_directory(
        staging,
        require_source_index=False,
        verify_selection_exclusion=False,
    )
    if output.exists():
        if not replace:
            raise RuntimeError(f"refusing to overwrite {output}; pass --replace")
        backup = CACHE / "backups" / f"{output.name}-{int(time.time())}"
        backup.parent.mkdir(parents=True, exist_ok=True)
        output.replace(backup)
    staging.replace(output)


def audit_directory(
    root: Path,
    *,
    require_source_index: bool = True,
    workers: int = 2,
    verify_selection_exclusion: bool = True,
) -> None:
    if workers < 1:
        raise ValueError("audit worker count must be positive")
    root = root.resolve()
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    cases = manifest["cases"]
    errors: list[str] = []
    connection: sqlite3.Connection | None = None
    if require_source_index:
        connection = open_index()
        assert_complete_sources(connection)
    novelty_audits: list[tuple[str, Candidate, dict[str, Any]]] = []
    if len(cases) != EXPECTED_CASES:
        errors.append(f"case count {len(cases)} != {EXPECTED_CASES}")
    if Counter(case["stream"] for case in cases) != Counter({stream: 25 for stream in STREAMS}):
        errors.append("stream counts are not 25/25/25/25")
    if len({case["case_id"] for case in cases}) != EXPECTED_CASES:
        errors.append("duplicate case IDs")
    if len({case["reduced_formula_key"] for case in cases}) != EXPECTED_CASES:
        errors.append("reduced formulas are not unique")
    overlap = {case["reduced_formula_key"] for case in cases} & existing_pxrd100_formulas()
    if overlap:
        errors.append(f"formula overlap with pXRD-100: {sorted(overlap)}")
    if len({case["generation"]["parent_id"] for case in cases}) != EXPECTED_CASES:
        errors.append("parents are not unique")
    exclusion = manifest.get("selection_exclusion")
    if exclusion and verify_selection_exclusion:
        exclusion_path = root / PurePosixPath(str(exclusion["manifest_path"]))
        if not exclusion_path.is_file():
            errors.append(f"selection exclusion manifest is missing: {exclusion_path}")
        elif sha256_file(exclusion_path) != exclusion.get("manifest_sha256"):
            errors.append("selection exclusion manifest digest mismatch")
        else:
            excluded_manifest = json.loads(exclusion_path.read_text(encoding="utf-8"))
            excluded_cases = list(excluded_manifest.get("cases", []))
            excluded_candidates = {
                str(case.get("generation", {}).get("candidate_id"))
                for case in excluded_cases
                if case.get("generation", {}).get("candidate_id")
            }
            excluded_formulas = {
                str(case["reduced_formula_key"])
                for case in excluded_cases
                if case.get("reduced_formula_key")
            }
            excluded_parents = {
                str(case.get("generation", {}).get("parent_id"))
                for case in excluded_cases
                if case.get("generation", {}).get("parent_id")
            }
            candidate_overlap = {
                str(case["generation"]["candidate_id"]) for case in cases
            } & excluded_candidates
            formula_overlap = {
                str(case["reduced_formula_key"]) for case in cases
            } & excluded_formulas
            parent_overlap = {
                str(case["generation"]["parent_id"]) for case in cases
            } & excluded_parents
            if candidate_overlap:
                errors.append(
                    f"candidate overlap with excluded panel: {sorted(candidate_overlap)}"
                )
            if formula_overlap:
                errors.append(
                    f"formula overlap with excluded panel: {sorted(formula_overlap)}"
                )
            if parent_overlap:
                errors.append(
                    f"parent overlap with excluded panel: {sorted(parent_overlap)}"
                )
    if max(Counter(case["spacegroup_number"] for case in cases).values(), default=0) > 4:
        errors.append("space-group cap exceeds four")
    system_counts = Counter(case["crystal_system"] for case in cases)
    if set(system_counts) != set(PYXTAL_GROUPS) or max(system_counts.values(), default=0) > 20:
        errors.append(f"crystal-system balance invalid: {system_counts}")
    for stream in STREAMS:
        bins = Counter(
            site_bin(case["primitive_site_count"]) for case in cases if case["stream"] == stream
        )
        if bins != Counter({f"{low}-{high}": 5 for low, high in SITE_BINS}):
            errors.append(f"{stream}: site-bin quotas invalid: {bins}")
    structures: list[tuple[str, Structure, np.ndarray]] = []
    try:
        for case in cases:
            path = root / PurePosixPath(case["path"])
            if not path.is_file():
                errors.append(f"{case['case_id']}: missing CIF")
                continue
            if sha256_file(path) != case["sha256"]:
                errors.append(f"{case['case_id']}: CIF digest mismatch")
                continue
            try:
                structure = Structure.from_file(path)
                final, validation, xrd, profile = validate_structure(structure)
            except Exception as exc:
                errors.append(f"{case['case_id']}: invalid structure: {exc}")
                continue
            formula, key, anonymous = canonical_formula(final.composition.as_dict())
            if (formula, key, anonymous) != (
                case["formula"],
                case["reduced_formula_key"],
                case["anonymous_formula"],
            ):
                errors.append(f"{case['case_id']}: formula metadata mismatch")
            analyzer = SpacegroupAnalyzer(final, symprec=0.05, angle_tolerance=5)
            recomputed_spacegroup = analyzer.get_space_group_number()
            if recomputed_spacegroup != case["spacegroup_number"]:
                errors.append(f"{case['case_id']}: space-group metadata mismatch")
            if crystal_system(recomputed_spacegroup) != case["crystal_system"]:
                errors.append(f"{case['case_id']}: crystal-system metadata mismatch")
            if (
                len(structure) != case["cif_site_count"]
                or len(final) != case["primitive_site_count"]
            ):
                errors.append(f"{case['case_id']}: site-count metadata mismatch")
            numeric_checks = {
                "volume_angstrom3": float(structure.volume),
                "volume_per_atom_angstrom3": float(structure.volume / len(structure)),
                "density_g_cm3": float(structure.density),
            }
            for field_name, recomputed in numeric_checks.items():
                if not math.isclose(
                    float(case[field_name]), recomputed, rel_tol=1e-9, abs_tol=1e-9
                ):
                    errors.append(f"{case['case_id']}: {field_name} metadata mismatch")
            if xrd != case["xrd_selection_metrics"]:
                errors.append(f"{case['case_id']}: XRD metrics mismatch")
            if validation != case["validation"]:
                errors.append(f"{case['case_id']}: validation metadata mismatch")
            novelty = case["novelty"]
            if not novelty.get("passes_frozen_corpus_rules"):
                errors.append(f"{case['case_id']}: novelty certificate does not pass")
            if connection is not None:
                generation = case["generation"]
                audit_candidate = Candidate(
                    candidate_id=str(generation["candidate_id"]),
                    stream=case["stream"],
                    site_bin=site_bin(len(final)),
                    cif_path=str(path.relative_to(ROOT)),
                    formula=formula,
                    formula_key=key,
                    anonymous_formula=anonymous,
                    primitive_site_count=len(final),
                    spacegroup_number=recomputed_spacegroup,
                    crystal_system=crystal_system(recomputed_spacegroup),
                    parent_id=str(generation["parent_id"]),
                    parent_formula=str(generation["parent_formula"]),
                    parent_payload_sha256=str(generation["parent_payload_sha256"]),
                    generation_seed=int(generation["generation_seed"]),
                    generation=generation,
                    xrd=xrd,
                    validation=validation,
                    mace=generation.get("mace"),
                    certificate=novelty,
                )
                novelty_audits.append((case["case_id"], audit_candidate, novelty))
            structures.append((case["case_id"], final, profile))
        if connection is not None:
            audit_anonymous_results: dict[str, dict[str, Any]] = {}
            topology_groups: dict[str, list[Candidate]] = defaultdict(list)
            for _case_id, audit_candidate, _novelty in novelty_audits:
                if audit_candidate.stream in {"wyckoff-enumeration", "crystal-search"}:
                    topology_groups[audit_candidate.anonymous_formula].append(audit_candidate)
            topology_tasks = [
                (
                    anonymous_formula,
                    [asdict(candidate) for candidate in topology_groups[anonymous_formula]],
                )
                for anonymous_formula in sorted(topology_groups)
            ]
            with ProcessPoolExecutor(
                max_workers=workers, initializer=initialize_topology_worker
            ) as executor:
                for _anonymous_formula, matched in executor.map(
                    match_topology_group, topology_tasks, chunksize=1
                ):
                    audit_anonymous_results.update(matched)
            for case_id, audit_candidate, novelty in novelty_audits:
                recomputed_novelty = certify_candidate(
                    connection,
                    audit_candidate,
                    anonymous_result=audit_anonymous_results.get(
                        audit_candidate.candidate_id
                    ),
                )
                if recomputed_novelty != novelty:
                    errors.append(
                        f"{case_id}: novelty certificate recomputation mismatch"
                    )
        for index, (case_id, structure, profile) in enumerate(structures):
            for other_id, other, other_profile in structures[:index]:
                if STRICT_MATCHER.fit(structure, other):
                    errors.append(f"duplicate species-aware structures: {case_id} and {other_id}")
                if len(structure) == len(other) and STRICT_MATCHER.fit(
                    erased_species(structure), erased_species(other)
                ):
                    errors.append(f"duplicate species-erased structures: {case_id} and {other_id}")
                similarity = float(
                    profile
                    @ other_profile
                    / (np.linalg.norm(profile) * np.linalg.norm(other_profile))
                )
                if similarity >= 0.9999:
                    errors.append(
                        f"near-identical pXRD profiles: {case_id} and {other_id} ({similarity:.8f})"
                    )
    finally:
        if connection is not None:
            connection.close()
    novelty_report = json.loads((root / "novelty-report.json").read_text(encoding="utf-8"))
    if novelty_report.get("certificate_status") != "complete":
        errors.append("novelty report is not complete")
    if require_source_index:
        if manifest["source_lock_sha256"] != sha256_file(root / "SOURCE.lock.json"):
            errors.append("source lock digest mismatch")
        if not INDEX.is_file() or manifest["source_index_sha256"] != sha256_file(INDEX):
            errors.append("live source index digest mismatch")
        if (
            not TOPOLOGY_INDEX.is_file()
            or manifest.get("derived_topology_index_sha256") != sha256_file(TOPOLOGY_INDEX)
        ):
            errors.append("derived topology index digest mismatch")
        lock = json.loads((root / "SOURCE.lock.json").read_text(encoding="utf-8"))
        if lock.get("index", {}).get("sha256") != manifest["source_index_sha256"]:
            errors.append("source lock and manifest index digests disagree")
        state_connection = open_index()
        try:
            states = {
                row[0]: (row[1], row[2], row[3], row[4])
                for row in state_connection.execute(
                    "SELECT source, status, record_count, failed_count, source_sha256 "
                    "FROM source_state"
                )
            }
        finally:
            state_connection.close()
        for source, locked in lock.get("sources", {}).items():
            actual = states.get(source)
            expected = (
                locked["status"],
                locked["record_count"],
                locked["failed_count"],
                locked["sha256"],
            )
            if actual != expected:
                errors.append(f"source lock state mismatch for {source}")
    if errors:
        raise RuntimeError("pXRD-ood audit failed:\n- " + "\n- ".join(errors))
    print(f"OK: {len(cases)} complete-novelty pXRD-ood CIFs")


def export_blind(*, destination: Path, replace: bool) -> None:
    audit_directory(OUTPUT)
    if destination.exists():
        if not replace:
            raise RuntimeError(f"blind export exists: {destination}; pass --replace")
        shutil.rmtree(destination)
    patterns = destination / "patterns"
    patterns.mkdir(parents=True)
    manifest = json.loads((OUTPUT / "manifest.json").read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    calculator = XRDCalculator(wavelength="CuKa1")
    for case in manifest["cases"]:
        structure = Structure.from_file(OUTPUT / case["path"])
        pattern = calculator.get_pattern(structure, two_theta_range=(5.0, 90.0))
        path = patterns / f"{case['case_id']}.xy"
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write("two_theta_deg,intensity\n")
            maximum = max(pattern.y)
            for angle, intensity in zip(pattern.x, pattern.y, strict=True):
                stream.write(f"{angle:.8f},{intensity / maximum:.10f}\n")
        rows.append(
            {
                "case_id": case["case_id"],
                "composition": case["formula"],
                "pattern_path": f"patterns/{path.name}",
                "pattern_sha256": sha256_file(path),
                "radiation": "Cu K-alpha-1",
                "wavelength_angstrom": calculator.wavelength,
            }
        )
    write_json(
        destination / "manifest.json",
        {
            "schema_version": "1.0.0",
            "dataset_id": "pXRD-ood-v1-blind",
            "ground_truth_included": False,
            "case_count": len(rows),
            "cases": rows,
        },
    )


def main() -> None:
    global TOPOLOGY_INDEX
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser("generate")
    generate.add_argument("--per-bin", type=int, default=20)
    generate.add_argument("--replace", action="store_true")
    topup = subparsers.add_parser("topup")
    topup.add_argument("--wyckoff-buffer", type=int, default=3)
    topup.add_argument("--crystal-buffer", type=int, default=5)
    topup.add_argument("--min-certified-per-bin", type=int, default=5)
    subparsers.add_parser("withdraw-dense-low-bin-topups")
    subparsers.add_parser("withdraw-dense-ab-low-bin-topups")
    relax = subparsers.add_parser("relax")
    relax.add_argument("--replace", action="store_true")
    relax.add_argument("--limit", type=int)
    relax.add_argument("--workers", type=int, default=2)
    certify = subparsers.add_parser("certify")
    certify.add_argument("--replace", action="store_true")
    certify.add_argument("--workers", type=int, default=2)
    certify.add_argument("--topology-index", type=Path, default=DEFAULT_TOPOLOGY_INDEX)
    certify.add_argument("--ignore-topology-match-cache", action="store_true")
    build = subparsers.add_parser("build")
    build.add_argument("--replace", action="store_true")
    build.add_argument("--verify-repeat", action="store_true")
    build.add_argument("--output", type=Path, default=OUTPUT)
    build.add_argument("--dataset-id", default="pXRD-ood-v1")
    build.add_argument("--case-prefix", default="pxrdood")
    build.add_argument("--selection-seed", type=int, default=SEED)
    build.add_argument("--selection-date", default=SELECTION_DATE)
    build.add_argument("--exclude-manifest", type=Path)
    build.add_argument("--certified-manifest", type=Path)
    build.add_argument("--topology-index", type=Path, default=DEFAULT_TOPOLOGY_INDEX)
    audit = subparsers.add_parser("audit")
    audit.add_argument("--root", type=Path, default=OUTPUT)
    audit.add_argument("--workers", type=int, default=2)
    audit.add_argument("--topology-index", type=Path, default=DEFAULT_TOPOLOGY_INDEX)
    blind = subparsers.add_parser("export-blind")
    blind.add_argument("destination", type=Path)
    blind.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    if hasattr(args, "topology_index"):
        TOPOLOGY_INDEX = args.topology_index.expanduser().resolve()
    if args.command == "generate":
        generate_pool(per_bin=args.per_bin, replace=args.replace)
    elif args.command == "topup":
        topup_topology_pool(
            wyckoff_buffer=args.wyckoff_buffer,
            crystal_buffer=args.crystal_buffer,
            min_certified_per_bin=args.min_certified_per_bin,
        )
    elif args.command == "withdraw-dense-low-bin-topups":
        withdraw_dense_low_bin_topups()
    elif args.command == "withdraw-dense-ab-low-bin-topups":
        withdraw_dense_ab_low_bin_topups()
    elif args.command == "relax":
        relax_crystal_search(
            replace=args.replace, limit=args.limit, workers=args.workers
        )
    elif args.command == "certify":
        certify_pool(
            replace=args.replace,
            workers=args.workers,
            use_topology_match_cache=not args.ignore_topology_match_cache,
        )
    elif args.command == "build":
        output = args.output.expanduser().resolve()
        certified_manifest = (
            args.certified_manifest.expanduser().resolve()
            if args.certified_manifest is not None
            else (
                V1_CERTIFIED_MANIFEST
                if args.dataset_id == "pXRD-ood-v1" and V1_CERTIFIED_MANIFEST.is_file()
                else CERTIFIED / "manifest.json"
            )
        )
        build_output(
            replace=args.replace,
            output=output,
            dataset_id=args.dataset_id,
            case_prefix=args.case_prefix,
            selection_seed=args.selection_seed,
            selection_date=args.selection_date,
            exclude_manifest=args.exclude_manifest,
            certified_manifest=certified_manifest,
        )
        if args.verify_repeat:
            first_hashes = directory_hashes(output)
            build_output(
                replace=True,
                output=output,
                dataset_id=args.dataset_id,
                case_prefix=args.case_prefix,
                selection_seed=args.selection_seed,
                selection_date=args.selection_date,
                exclude_manifest=args.exclude_manifest,
                certified_manifest=certified_manifest,
            )
            second_hashes = directory_hashes(output)
            if first_hashes != second_hashes:
                differing = sorted(
                    path
                    for path in set(first_hashes) | set(second_hashes)
                    if first_hashes.get(path) != second_hashes.get(path)
                )
                raise RuntimeError(
                    "repeat pXRD-ood build was not hash-identical: " + ", ".join(differing)
                )
            print(f"OK: repeat build reproduced {len(second_hashes)} files byte-for-byte")
        audit_directory(output)
    elif args.command == "audit":
        audit_directory(args.root, workers=args.workers)
    else:
        export_blind(destination=args.destination, replace=args.replace)


if __name__ == "__main__":
    main()
