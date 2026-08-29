"""Build and audit the deterministic pXRD-100 Materials Project corpus.

All 100 structures are selected from the frozen MP-20 training split. The six
large-cell challenge cases have 17--20 sites in their primitive cells, keeping the
entire benchmark within the published MP-20 model envelope.

Build from the repository root with an MP_API_KEY in the environment::

    uv run python pxrd-bench/generation/build_pxrd_100.py build

Audit the committed, fully offline result with::

    uv run python pxrd-bench/generation/build_pxrd_100.py audit
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import math
import os
import re
import shutil
import sqlite3
import sys
import time
import warnings
import zlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from itertools import combinations, pairwise
from pathlib import Path
from typing import Any, Literal

import numpy as np
import requests
from numpy.typing import NDArray
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core import Composition, Element, Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "pXRD-100"
CACHE = ROOT / ".runs" / "pxrd100-v2"
EXPOSURE_INDEX = ROOT / ".runs" / "pxrd-ood" / "indexes" / "exposure.sqlite3"
EXPOSURE_SOURCE_LOCK = ROOT / ".runs" / "pxrd-ood" / "SOURCE.lock.json"
DECIFER_TRAIN_H5 = CACHE / "sources" / "noma" / "serialized" / "train.h5"
PXRD_OOD_MANIFEST = ROOT / "pXRD-ood" / "manifest.json"

SOURCE_COMMIT = "f857f598d6f6cca5dc1ea0582d228f12dcc2c2ea"
SOURCE_BASE = f"https://raw.githubusercontent.com/txie-93/cdvae/{SOURCE_COMMIT}/data/mp_20"
SOURCE_FILES = {
    "train": (
        "train.csv",
        "133bab58dba02d316f9f91174839f17802dce648be4e8659d1a42b32b97fa01d",
        27136,
    ),
    "val": (
        "val.csv",
        "7b5f4085464b3eac9fd2123acee97ec372214004ce7e983b535b33395abc3e29",
        9047,
    ),
    "test": (
        "test.csv",
        "dd605c7543cf95a13e150aed630d0915e74edc8dea17e85301ee6fbfeb7f500a",
        9046,
    ),
}
SELECTION_SEED = 20260720
SELECTION_DATE = "2026-07-20"
CORPUS_REVISION = "v2-fourway-train-20260720"
EXPOSURE_CACHE_REVISION = "v2-fourway-train-20260720"
DATASET_ID = "pXRD-100"
CASE_PREFIX = "pxrd100"
SUPERSEDED_ARCHIVE: str | None = "pXRD-100-v1-mixed-framework-exposure-20260718"
MANDATORY_POLYMORPH_FORMULA: str | None = "TiO2"
SELECTION_EXCLUSION_CORPORA: tuple[Path, ...] = ()
EXPECTED_MP_DB_VERSION = "2026.04.13"
MP_API_ROOT = "https://api.materialsproject.org"
SUMMARY_URL = f"{MP_API_ROOT}/materials/summary/"

FloatArray = NDArray[np.float64]
Panel = Literal["representative", "challenge", "polymorph"]

ATOM_ROW = re.compile(
    r"^\s{2,}([A-Z][a-z]?)\s+\S+\s+\d+\s+"
    r"[-+0-9.eE]+\s+[-+0-9.eE]+\s+[-+0-9.eE]+\s+([-+0-9.eE]+)\s*$",
    re.MULTILINE,
)
VOLUME_ROW = re.compile(r"^_cell_volume\s+([-+0-9.eE]+)\s*$", re.MULTILINE)
NUMERIC_MP_ID = re.compile(r"^mp-\d+$")

STRICT_MATCHER = StructureMatcher(
    ltol=0.2,
    stol=0.3,
    angle_tol=5,
    primitive_cell=True,
    scale=True,
    attempt_supercell=False,
)
LOOSE_MATCHER = StructureMatcher(
    ltol=0.3,
    stol=0.5,
    angle_tol=10,
    primitive_cell=True,
    scale=True,
    attempt_supercell=False,
)


@dataclass(slots=True)
class Record:
    """One source structure and the cheap descriptors needed for selection."""

    split: str
    row_index: int
    source_id: str
    formula: str
    formula_key: str
    anonymous_formula: str
    elements: tuple[str, ...]
    cif: str
    formation_energy_per_atom: float
    energy_above_hull: float
    spacegroup_number: int
    nsites: int
    volume: float
    density: float
    source_kind: str = "mp20"
    structure_cache: Structure | None = field(default=None, repr=False)
    xrd_cache: dict[str, float] | None = field(default=None, repr=False)
    profile_cache: FloatArray | None = field(default=None, repr=False)
    independent_sites_cache: int | None = field(default=None, repr=False)
    primitive_site_count_cache: int | None = field(default=None, repr=False)
    api_doc: dict[str, Any] | None = field(default=None, repr=False)
    training_exposure: dict[str, Any] | None = field(default=None, repr=False)

    @property
    def crystal_system(self) -> str:
        return crystal_system(self.spacegroup_number)

    @property
    def nelements(self) -> int:
        return len(self.elements)

    @property
    def volume_per_atom(self) -> float:
        return self.volume / self.nsites

    @property
    def structure(self) -> Structure:
        if self.structure_cache is None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.structure_cache = Structure.from_str(self.cif, fmt="cif")
        return self.structure_cache

    @property
    def independent_sites(self) -> int:
        if self.independent_sites_cache is None:
            try:
                symmetrized = SpacegroupAnalyzer(
                    self.structure, symprec=0.1, angle_tolerance=5
                ).get_symmetrized_structure()
                self.independent_sites_cache = len(symmetrized.equivalent_indices)
            except Exception:
                self.independent_sites_cache = self.nsites
        return self.independent_sites_cache

    @property
    def primitive_site_count(self) -> int:
        if self.primitive_site_count_cache is None:
            primitive = SpacegroupAnalyzer(
                self.structure, symprec=0.1, angle_tolerance=5
            ).find_primitive()
            self.primitive_site_count_cache = len(primitive or self.structure)
        return self.primitive_site_count_cache

    def xrd(self) -> tuple[dict[str, float], FloatArray]:
        if self.xrd_cache is None or self.profile_cache is None:
            self.xrd_cache, self.profile_cache = xrd_metrics(self.structure)
        return self.xrd_cache, self.profile_cache


@dataclass(frozen=True, slots=True)
class PairOption:
    first: Record
    second: Record
    cosine_similarity: float
    max_absolute_difference: float
    same_spacegroup: bool


@dataclass(slots=True)
class FamilyCandidate:
    formula_key: str
    formula: str
    cluster_count: int
    source_member_count: int
    options: list[PairOption]


@dataclass(slots=True)
class SelectedCase:
    case_id: str
    panel: Panel
    record: Record
    path: str = ""
    primary_axis: str | None = None
    difficulty_percentile: float | None = None
    polymorph_family_id: str | None = None
    polymorph_partner_id: str | None = None
    polymorph_difficulty: str | None = None
    pair_cosine_similarity: float | None = None
    pair_max_absolute_difference: float | None = None
    source_family_clusters: int | None = None
    selection_notes: tuple[str, ...] = ()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_fraction(value: str) -> float:
    raw = hashlib.sha256(f"{SELECTION_SEED}:{value}".encode()).digest()[:8]
    return int.from_bytes(raw, "big") / 2**64


def crystal_system(number: int) -> str:
    if 1 <= number <= 2:
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
    if number <= 230:
        return "cubic"
    raise ValueError(f"invalid space-group number: {number}")


def canonical_formula(value: str | dict[str, float]) -> tuple[str, str, str]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        composition = Composition(value).reduced_composition
        return (
            composition.reduced_formula,
            composition.alphabetical_formula,
            composition.anonymized_formula,
        )


def parse_cif_summary(cif: str) -> tuple[tuple[str, ...], int, float, float]:
    atom_rows = ATOM_ROW.findall(cif)
    if not atom_rows:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structure = Structure.from_str(cif, fmt="cif")
        symbols = tuple(site.specie.symbol for site in structure)
        return symbols, len(structure), float(structure.volume), float(structure.density)
    occupancies = [float(occupancy) for _, occupancy in atom_rows]
    if any(not math.isclose(value, 1.0, abs_tol=1e-8) for value in occupancies):
        raise ValueError("MP-20 candidate contains partial occupancy")
    symbols = tuple(symbol for symbol, _ in atom_rows)
    match = VOLUME_ROW.search(cif)
    if match is None:
        raise ValueError("CIF has no cell volume")
    volume = float(match.group(1))
    mass_amu = sum(float(Element(symbol).atomic_mass) for symbol in symbols)
    density = mass_amu * 1.66053906660 / volume
    return symbols, len(symbols), volume, density


def source_path(split: str) -> Path:
    return CACHE / "source" / SOURCE_FILES[split][0]


def download_sources() -> None:
    (CACHE / "source").mkdir(parents=True, exist_ok=True)
    for split, (filename, expected_hash, _) in SOURCE_FILES.items():
        path = source_path(split)
        if path.is_file() and sha256_file(path) == expected_hash:
            continue
        response = requests.get(f"{SOURCE_BASE}/{filename}", timeout=120)
        response.raise_for_status()
        if sha256_bytes(response.content) != expected_hash:
            raise RuntimeError(f"source digest mismatch for {filename}")
        temporary = path.with_suffix(".partial")
        temporary.write_bytes(response.content)
        temporary.replace(path)


def load_records() -> dict[str, list[Record]]:
    records: dict[str, list[Record]] = {}
    for split, (_, expected_hash, expected_rows) in SOURCE_FILES.items():
        path = source_path(split)
        if sha256_file(path) != expected_hash:
            raise RuntimeError(f"source lock failed for {path}")
        split_records: list[Record] = []
        with path.open(encoding="utf-8", newline="") as stream:
            for row_number, row in enumerate(csv.DictReader(stream)):
                source_id = row["material_id"]
                formula, formula_key, anonymous = canonical_formula(row["pretty_formula"])
                symbols, nsites, volume, density = parse_cif_summary(row["cif"])
                declared_elements = tuple(sorted(ast.literal_eval(row["elements"])))
                if tuple(sorted(set(symbols))) != declared_elements:
                    raise ValueError(f"element mismatch in {source_id}")
                split_records.append(
                    Record(
                        split=split,
                        row_index=int(row.get("") or row_number),
                        source_id=source_id,
                        formula=formula,
                        formula_key=formula_key,
                        anonymous_formula=anonymous,
                        elements=declared_elements,
                        cif=row["cif"].rstrip() + "\n",
                        formation_energy_per_atom=float(row["formation_energy_per_atom"]),
                        energy_above_hull=float(row["e_above_hull"]),
                        spacegroup_number=int(row["spacegroup.number"]),
                        nsites=nsites,
                        volume=volume,
                        density=density,
                    )
                )
        if len(split_records) != expected_rows:
            raise RuntimeError(
                f"{split} row count changed: {len(split_records)} != {expected_rows}"
            )
        records[split] = split_records
    return records


def load_index_structure(row: sqlite3.Row) -> Structure:
    payload = row["payload"]
    if payload is None:
        raise ValueError(f"exposure record has no structure payload: {row['record_id']}")
    raw = zlib.decompress(payload)
    if row["payload_format"] == "cif-zlib":
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return Structure.from_str(raw.decode("utf-8"), fmt="cif")
    if row["payload_format"] == "pymatgen-json-zlib":
        return Structure.from_dict(json.loads(raw))
    raise ValueError(f"unsupported exposure payload: {row['payload_format']}")


def load_decifer_train_names() -> set[str]:
    if not DECIFER_TRAIN_H5.is_file():
        raise RuntimeError(
            f"missing authoritative deCIFer training split: {DECIFER_TRAIN_H5}; "
            "extract train.h5 from the official noma.zip first"
        )
    try:
        import h5py
    except ImportError as exc:
        raise RuntimeError("four-way selection requires h5py") from exc
    names: set[str] = set()
    with h5py.File(DECIFER_TRAIN_H5, "r") as handle:
        if "cif_name" not in handle:
            raise RuntimeError("deCIFer train.h5 has no cif_name dataset")
        dataset = handle["cif_name"]
        for start in range(0, len(dataset), 100_000):
            for value in dataset[start : start + 100_000]:
                names.add(value.decode("utf-8") if isinstance(value, bytes) else str(value))
    if len(names) < 2_000_000:
        raise RuntimeError(f"unexpectedly small deCIFer training split: {len(names)}")
    return names


def exposure_row(connection: sqlite3.Connection, source: str, record_id: str) -> sqlite3.Row | None:
    return connection.execute(
        "SELECT * FROM records WHERE source = ? AND record_id = ?",
        (source, record_id),
    ).fetchone()


def strict_match(record: Record, row: sqlite3.Row) -> bool:
    try:
        return STRICT_MATCHER.fit(record.structure, load_index_structure(row))
    except Exception:
        return False


def matching_row(
    record: Record,
    rows: list[sqlite3.Row],
    *,
    allowed_locators: set[str] | None = None,
) -> sqlite3.Row | None:
    for row in rows:
        if allowed_locators is not None and str(row["locator"]) not in allowed_locators:
            continue
        if strict_match(record, row):
            return row
    return None


def exposure_evidence(row: sqlite3.Row, *, status: str, match_kind: str) -> dict[str, Any]:
    return {
        "status": status,
        "source": str(row["source"]),
        "split": row["split"],
        "record_id": str(row["record_id"]),
        "locator": row["locator"],
        "match_kind": match_kind,
        "matcher": {
            "ltol": 0.2,
            "stol": 0.3,
            "angle_tol_degrees": 5,
            "primitive_cell": True,
            "scale": True,
            "attempt_supercell": False,
        },
    }


def direct_noma_rows(connection: sqlite3.Connection, source_id: str) -> list[sqlite3.Row]:
    prefix = f"MP_{source_id}#"
    return list(
        connection.execute(
            "SELECT * FROM records WHERE source = 'decifer_noma' "
            "AND record_id >= ? AND record_id < ? ORDER BY record_id",
            (prefix, prefix + chr(0x10FFFF)),
        )
    )


def formula_rows(
    connection: sqlite3.Connection,
    *,
    source: str,
    formula_key: str,
    split: str | None = None,
) -> list[sqlite3.Row]:
    if split is None:
        return list(
            connection.execute(
                "SELECT * FROM records WHERE source = ? AND formula_key = ? ORDER BY record_id",
                (source, formula_key),
            )
        )
    return list(
        connection.execute(
            "SELECT * FROM records WHERE source = ? AND split = ? AND formula_key = ? "
            "ORDER BY record_id",
            (source, split, formula_key),
        )
    )


def ood_formula_keys() -> set[str]:
    if not PXRD_OOD_MANIFEST.is_file():
        return set()
    manifest = json.loads(PXRD_OOD_MANIFEST.read_text(encoding="utf-8"))
    return {str(case["reduced_formula_key"]) for case in manifest["cases"]}


def corpus_formula_keys(root: Path) -> set[str]:
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise RuntimeError(f"missing exclusion manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return {str(case["reduced_formula_key"]) for case in manifest["cases"]}


def selection_forbidden_formula_keys() -> set[str]:
    forbidden = ood_formula_keys()
    for root in SELECTION_EXCLUSION_CORPORA:
        forbidden.update(corpus_formula_keys(root))
    return forbidden


def selection_exclusion_metadata() -> list[dict[str, Any]]:
    metadata: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for root in SELECTION_EXCLUSION_CORPORA:
        resolved = root.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        manifest_path = resolved / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        metadata.append(
            {
                "dataset_id": str(manifest.get("dataset_id", resolved.name)),
                "path": str(resolved.relative_to(ROOT)),
                "manifest_sha256": sha256_file(manifest_path),
                "reduced_formula_count": len(corpus_formula_keys(resolved)),
            }
        )
    return metadata


def four_way_training_intersection(train: list[Record]) -> tuple[list[Record], dict[str, Any]]:
    if not EXPOSURE_INDEX.is_file() or not EXPOSURE_SOURCE_LOCK.is_file():
        raise RuntimeError("missing frozen framework-exposure index or source lock")
    cache_path = CACHE / "indexes" / "four-way-training-exposure.json"
    cache_key = {
        "corpus_revision": EXPOSURE_CACHE_REVISION,
        "exposure_index_size": EXPOSURE_INDEX.stat().st_size,
        "decifer_train_h5_size": DECIFER_TRAIN_H5.stat().st_size,
        "pxrd_ood_manifest_sha256": sha256_file(PXRD_OOD_MANIFEST),
    }
    train_by_id = {record.source_id: record for record in train}
    if cache_path.is_file():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if cached.get("cache_key") == cache_key:
            exposed: list[Record] = []
            for source_id, evidence in cached["training_exposure"].items():
                record = train_by_id[source_id]
                record.training_exposure = evidence
                exposed.append(record)
            exposed.sort(key=lambda record: record.source_id)
            return exposed, cached["report"]
    connection = sqlite3.connect(f"file:{EXPOSURE_INDEX}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    train_names = load_decifer_train_names()
    forbidden = ood_formula_keys()
    tio2_key = canonical_formula("TiO2")[1]

    candidate_ids = [
        str(row[0])
        for row in connection.execute(
            """SELECT p.record_id
               FROM records AS p
               JOIN records AS c
                 ON c.source = 'crystalyze_mp20'
                AND c.split = 'train'
                AND c.record_id = p.record_id
               WHERE p.source = 'pxrdgen_mp20'
                 AND p.split = 'train'
                 AND p.record_id GLOB 'mp-[0-9]*'
                 AND EXISTS (
                     SELECT 1 FROM records AS d
                     WHERE d.source = 'diffractgpt_released'
                       AND d.split = 'train'
                       AND d.formula_key = p.formula_key
                 )
                 AND (
                     p.formula_key = ? OR EXISTS (
                         SELECT 1 FROM records AS n
                         WHERE n.source = 'decifer_noma'
                           AND n.record_id >= 'MP_' || p.record_id || '#'
                           AND n.record_id < 'MP_' || p.record_id || '#' || char(1114111)
                     )
                 )
               ORDER BY p.record_id""",
            (tio2_key,),
        )
    ]
    failures: Counter[str] = Counter()
    exposed: list[Record] = []
    for index, source_id in enumerate(candidate_ids, start=1):
        record = train_by_id.get(source_id)
        if record is None or not eligible_mp20(record) or record.formula_key in forbidden:
            failures["base_eligibility_or_ood_formula"] += 1
            continue

        pxrdgen = exposure_row(connection, "pxrdgen_mp20", source_id)
        crystalyze = exposure_row(connection, "crystalyze_mp20", source_id)
        if pxrdgen is None or not strict_match(record, pxrdgen):
            failures["pxrdgen_structure_mismatch"] += 1
            continue
        if (
            crystalyze is None
            or crystalyze["split"] != "train"
            or not strict_match(record, crystalyze)
        ):
            failures["crystalyze_structure_mismatch"] += 1
            continue

        noma = matching_row(
            record,
            direct_noma_rows(connection, source_id),
            allowed_locators=train_names,
        )
        if noma is None:
            noma = matching_row(
                record,
                formula_rows(connection, source="decifer_noma", formula_key=record.formula_key),
                allowed_locators=train_names,
            )
        if noma is None:
            failures["decifer_train_structure_mismatch"] += 1
            continue

        diffractgpt = matching_row(
            record,
            formula_rows(
                connection,
                source="diffractgpt_released",
                formula_key=record.formula_key,
                split="train",
            ),
        )
        if diffractgpt is None:
            failures["diffractgpt_train_structure_mismatch"] += 1
            continue

        record.training_exposure = {
            "pxrdgen": exposure_evidence(
                pxrdgen, status="exact_train", match_kind="exact_id_and_strict_structure"
            ),
            "crystalyze": exposure_evidence(
                crystalyze, status="exact_train", match_kind="exact_id_and_strict_structure"
            ),
            "decifer": exposure_evidence(
                noma, status="exact_train", match_kind="strict_structure_in_public_train_h5"
            ),
            "diffractgpt": exposure_evidence(
                diffractgpt,
                status="released_train_proxy",
                match_kind="strict_structure_in_released_train_parquet",
            ),
        }
        exposed.append(record)
        if index % 500 == 0:
            print(f"checked {index}/{len(candidate_ids)} exposure candidates")
    connection.close()
    report = {
        "candidate_count": len(candidate_ids),
        "qualified_count": len(exposed),
        "excluded_counts": dict(sorted(failures.items())),
        "deCIFer_train_name_count": len(train_names),
        "pxrd_ood_formula_exclusion_count": len(forbidden),
    }
    if len(exposed) < 500:
        raise RuntimeError(f"four-way intersection is unexpectedly small: {report}")
    if sum(17 <= record.primitive_site_count <= 20 for record in exposed) < 30:
        raise RuntimeError("four-way intersection lacks enough 17-20-site structures")
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(
            {
                "cache_key": cache_key,
                "report": report,
                "training_exposure": {
                    record.source_id: record.training_exposure for record in exposed
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return exposed, report


def eligible_mp20(record: Record) -> bool:
    return (
        bool(NUMERIC_MP_ID.fullmatch(record.source_id))
        and 1 <= record.nsites <= 20
        and record.energy_above_hull <= 0.080000001
        and record.formation_energy_per_atom < 2.0
    )


def one_per_formula(records: list[Record]) -> dict[str, Record]:
    grouped: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        if eligible_mp20(record):
            grouped[record.formula_key].append(record)
    return {
        formula: min(group, key=lambda item: (item.energy_above_hull, item.source_id))
        for formula, group in grouped.items()
    }


def cluster_records(records: list[Record]) -> list[list[Record]]:
    clusters: list[list[Record]] = []
    for record in sorted(records, key=lambda item: (item.energy_above_hull, item.source_id)):
        for cluster in clusters:
            if STRICT_MATCHER.fit(cluster[0].structure, record.structure):
                cluster.append(record)
                break
        else:
            clusters.append([record])
    return clusters


def xrd_metrics(structure: Structure) -> tuple[dict[str, float], FloatArray]:
    calculator = XRDCalculator(wavelength="CuKa1")
    pattern = calculator.get_pattern(structure, two_theta_range=(5.0, 90.0))
    positions = np.asarray(pattern.x, dtype=np.float64)
    intensities = np.asarray(pattern.y, dtype=np.float64)
    axis = np.arange(5.0, 90.0000001, 0.05, dtype=np.float64)
    sigma = 0.12
    profile = np.zeros_like(axis)
    for position, intensity in zip(positions, intensities, strict=True):
        profile += intensity * np.exp(-0.5 * np.square((axis - position) / sigma))
    maximum = float(np.max(profile))
    if maximum <= 0:
        raise ValueError("empty pXRD pattern")
    profile /= maximum

    significant = intensities >= 1.0
    selected_positions = positions[significant]
    selected_intensities = intensities[significant]
    peak_count = int(np.count_nonzero(significant))
    if len(selected_positions) > 1:
        separations = np.diff(selected_positions)
        fwhm = 2.0 * math.sqrt(2.0 * math.log(2.0)) * sigma
        flags = np.zeros(len(selected_positions), dtype=bool)
        close = np.flatnonzero(separations < fwhm)
        flags[close] = True
        flags[close + 1] = True
        overlap_fraction = float(selected_intensities[flags].sum() / selected_intensities.sum())
    else:
        overlap_fraction = 0.0
    probabilities = selected_intensities / selected_intensities.sum()
    entropy = float(-np.sum(probabilities * np.log(probabilities + 1e-300)))
    normalized_entropy = entropy / math.log(max(peak_count, 2))
    return (
        {
            "peak_count_above_1pct": float(peak_count),
            "overlap_intensity_fraction": overlap_fraction,
            "normalized_peak_entropy": normalized_entropy,
        },
        profile,
    )


def pair_option(first: Record, second: Record) -> PairOption | None:
    _, first_profile = first.xrd()
    _, second_profile = second.xrd()
    denominator = float(np.linalg.norm(first_profile) * np.linalg.norm(second_profile))
    cosine = float(first_profile @ second_profile / denominator)
    maximum_difference = float(np.max(np.abs(first_profile - second_profile)))
    if cosine >= 0.9999 or maximum_difference <= 0.03:
        return None
    return PairOption(
        first=first,
        second=second,
        cosine_similarity=cosine,
        max_absolute_difference=maximum_difference,
        same_spacegroup=first.spacegroup_number == second.spacegroup_number,
    )


def polymorph_family_candidates(
    train: list[Record], source_train: list[Record], forbidden_formulas: set[str]
) -> list[FamilyCandidate]:
    grouped: dict[str, list[Record]] = defaultdict(list)
    source_grouped: dict[str, list[Record]] = defaultdict(list)
    for record in train:
        if eligible_mp20(record):
            grouped[record.formula_key].append(record)
    for record in source_train:
        if eligible_mp20(record):
            source_grouped[record.formula_key].append(record)

    eligible_groups = [
        group
        for formula, group in grouped.items()
        if formula not in forbidden_formulas
        and len(group) >= 2
        and len(source_grouped[formula]) >= 3
    ]
    mandatory_key = (
        canonical_formula(MANDATORY_POLYMORPH_FORMULA)[1] if MANDATORY_POLYMORPH_FORMULA else None
    )
    mandatory = (
        next(group for group in eligible_groups if group[0].formula_key == mandatory_key)
        if mandatory_key
        else None
    )
    by_complexity: dict[str, list[list[Record]]] = {
        "binary": [],
        "ternary": [],
        "multinary": [],
    }
    for group in eligible_groups:
        if group is mandatory or group[0].nelements == 1:
            continue
        key = (
            "binary"
            if group[0].nelements == 2
            else "ternary"
            if group[0].nelements == 3
            else "multinary"
        )
        by_complexity[key].append(group)
    for groups in by_complexity.values():
        groups.sort(
            key=lambda group: (
                -min(len(group), 12),
                stable_fraction(group[0].formula_key),
            )
        )
    groups_to_process = [mandatory] if mandatory is not None else []
    for index in range(45):
        for key in ("binary", "ternary", "multinary"):
            if index < len(by_complexity[key]):
                groups_to_process.append(by_complexity[key][index])

    families: list[FamilyCandidate] = []
    for family_index, group in enumerate(groups_to_process, start=1):
        source_clusters = cluster_records(source_grouped[group[0].formula_key])
        if len(source_clusters) < 3:
            continue
        exposed_clusters = cluster_records(group)
        if len(exposed_clusters) < 2:
            continue
        representatives = [cluster[0] for cluster in exposed_clusters]
        options = [
            option
            for first, second in combinations(representatives, 2)
            if (option := pair_option(first, second)) is not None
        ]
        if not options:
            continue
        families.append(
            FamilyCandidate(
                formula_key=group[0].formula_key,
                formula=group[0].formula,
                cluster_count=len(source_clusters),
                source_member_count=len(source_grouped[group[0].formula_key]),
                options=options,
            )
        )
        if family_index % 20 == 0:
            print(f"processed {family_index}/{len(groups_to_process)} polymorph families")
    if len(families) < 30:
        raise RuntimeError(f"only {len(families)} usable polymorph families")
    return families


def choose_polymorphs(
    train: list[Record], source_train: list[Record], forbidden_formulas: set[str]
) -> tuple[list[SelectedCase], set[str]]:
    families = polymorph_family_candidates(train, source_train, forbidden_formulas)
    similarities = np.asarray(
        [option.cosine_similarity for family in families for option in family.options]
    )
    lower, upper = (float(value) for value in np.quantile(similarities, [1 / 3, 2 / 3]))

    def difficulty(option: PairOption) -> str:
        if option.cosine_similarity <= lower:
            return "easy"
        if option.cosine_similarity <= upper:
            return "medium"
        return "hard"

    best_by_family: dict[str, dict[str, PairOption]] = {}
    for family in families:
        grouped: dict[str, list[PairOption]] = defaultdict(list)
        for option in family.options:
            grouped[difficulty(option)].append(option)
        best_by_family[family.formula_key] = {}
        for label, options in grouped.items():
            target = {"easy": lower, "medium": (lower + upper) / 2, "hard": upper}[label]
            best_by_family[family.formula_key][label] = min(
                options,
                key=lambda item: (
                    abs(item.cosine_similarity - target),
                    -item.max_absolute_difference,
                    item.first.source_id,
                    item.second.source_id,
                ),
            )

    family_lookup = {family.formula_key: family for family in families}
    quotas = {"easy": 5, "medium": 10, "hard": 5}
    selected: list[tuple[FamilyCandidate, str, PairOption]] = []
    used_formulas: set[str] = set()
    used_elements: Counter[str] = Counter()
    chemistry_counts = {"binary": 0, "ternary": 0, "multinary": 0}

    mandatory_key = (
        canonical_formula(MANDATORY_POLYMORPH_FORMULA)[1] if MANDATORY_POLYMORPH_FORMULA else None
    )
    mandatory_option: PairOption | None = None
    if mandatory_key is not None:
        mandatory_options = best_by_family[mandatory_key]
        mandatory_difficulty = next(
            label for label in ("hard", "medium", "easy") if label in mandatory_options
        )
        mandatory_family = family_lookup[mandatory_key]
        mandatory_option = mandatory_options[mandatory_difficulty]
        selected.append((mandatory_family, mandatory_difficulty, mandatory_option))
        quotas[mandatory_difficulty] -= 1
        used_formulas.add(mandatory_key)
        used_elements.update(mandatory_option.first.elements)
        category = (
            "binary"
            if mandatory_option.first.nelements == 2
            else "ternary"
            if mandatory_option.first.nelements == 3
            else "multinary"
        )
        chemistry_counts[category] += 1

    target_chemistry = {"binary": 6, "ternary": 8, "multinary": 6}
    same_spacegroup_count = int(
        mandatory_option.same_spacegroup if mandatory_option is not None else False
    )
    bin_order = ["hard", "easy", "medium"]
    while sum(quotas.values()):
        label = next(name for name in bin_order if quotas[name] > 0)
        candidates: list[tuple[float, FamilyCandidate, PairOption]] = []
        for family in families:
            if family.formula_key in used_formulas:
                continue
            option = best_by_family[family.formula_key].get(label)
            if option is None:
                continue
            category = (
                "binary"
                if option.first.nelements == 2
                else "ternary"
                if option.first.nelements == 3
                else "multinary"
            )
            chemistry_need = max(target_chemistry[category] - chemistry_counts[category], 0)
            novel_elements = sum(
                1.0 / (1 + used_elements[element]) for element in option.first.elements
            )
            same_sg_need = 1.5 if same_spacegroup_count < 4 and option.same_spacegroup else 0.0
            score = (
                2.0 * chemistry_need
                + novel_elements
                + same_sg_need
                + 0.15 * family.cluster_count
                - stable_fraction(family.formula_key) * 1e-4
            )
            candidates.append((score, family, option))
        if not candidates:
            raise RuntimeError(f"cannot fill polymorph {label} quota")
        _, family, option = max(candidates, key=lambda item: item[0])
        selected.append((family, label, option))
        used_formulas.add(family.formula_key)
        used_elements.update(option.first.elements)
        category = (
            "binary"
            if option.first.nelements == 2
            else "ternary"
            if option.first.nelements == 3
            else "multinary"
        )
        chemistry_counts[category] += 1
        same_spacegroup_count += int(option.same_spacegroup)
        quotas[label] -= 1
        bin_order = bin_order[1:] + bin_order[:1]

    selected.sort(key=lambda item: (item[0].formula, item[0].formula_key))
    cases: list[SelectedCase] = []
    for family_index, (family, label, option) in enumerate(selected, start=1):
        family_id = f"poly-{family_index:02d}"
        members = sorted(
            (option.first, option.second),
            key=lambda item: (item.energy_above_hull, item.source_id),
        )
        member_ids = [f"{CASE_PREFIX}-{family_id}-{suffix}" for suffix in ("a", "b")]
        for member_index, record in enumerate(members):
            cases.append(
                SelectedCase(
                    case_id=member_ids[member_index],
                    panel="polymorph",
                    record=record,
                    polymorph_family_id=family_id,
                    polymorph_partner_id=member_ids[1 - member_index],
                    polymorph_difficulty=label,
                    pair_cosine_similarity=option.cosine_similarity,
                    pair_max_absolute_difference=option.max_absolute_difference,
                    source_family_clusters=family.cluster_count,
                    selection_notes=(
                        f"Source family has {family.source_member_count} MP-20 train records.",
                        "Pair members are StructureMatcher-distinct.",
                    ),
                )
            )
    return cases, used_formulas


def bin_index(value: float, edges: FloatArray) -> int:
    return int(np.searchsorted(edges, value, side="right"))


def representative_features(
    records: list[Record], reference: list[Record]
) -> tuple[FloatArray, FloatArray, list[str], FloatArray]:
    top_elements = [
        element
        for element, _ in Counter(
            element for record in reference for element in record.elements
        ).most_common(20)
    ]
    volume_edges = np.quantile([record.volume_per_atom for record in reference], [0.25, 0.5, 0.75])
    density_edges = np.quantile([record.density for record in reference], [0.25, 0.5, 0.75])
    systems = [
        "triclinic",
        "monoclinic",
        "orthorhombic",
        "tetragonal",
        "trigonal",
        "hexagonal",
        "cubic",
    ]
    labels = (
        [f"crystal_system:{value}" for value in systems]
        + [f"nsites:{value}" for value in ("1-4", "5-8", "9-12", "13-16", "17-20")]
        + [f"nelements:{value}" for value in ("1", "2", "3", "4+")]
        + [f"ehull:{value}" for value in ("0", "0-.01", ".01-.04", ".04-.08")]
        + [f"volume_per_atom:q{index}" for index in range(1, 5)]
        + [f"density:q{index}" for index in range(1, 5)]
        + [f"element:{element}" for element in top_elements]
    )

    def vector(record: Record) -> FloatArray:
        result: list[float] = []
        result.extend(float(record.crystal_system == value) for value in systems)
        site_bin = min((record.nsites - 1) // 4, 4)
        result.extend(float(site_bin == value) for value in range(5))
        element_bin = min(record.nelements, 4) - 1
        result.extend(float(element_bin == value) for value in range(4))
        if math.isclose(record.energy_above_hull, 0.0, abs_tol=1e-12):
            hull_bin = 0
        elif record.energy_above_hull <= 0.01:
            hull_bin = 1
        elif record.energy_above_hull <= 0.04:
            hull_bin = 2
        else:
            hull_bin = 3
        result.extend(float(hull_bin == value) for value in range(4))
        volume_bin = bin_index(record.volume_per_atom, volume_edges)
        density_bin = bin_index(record.density, density_edges)
        result.extend(float(volume_bin == value) for value in range(4))
        result.extend(float(density_bin == value) for value in range(4))
        result.extend(float(element in record.elements) for element in top_elements)
        return np.asarray(result, dtype=np.float64)

    matrix = np.stack([vector(record) for record in records])
    reference_matrix = np.stack([vector(record) for record in reference])
    target = reference_matrix.mean(axis=0)
    weights = np.ones(len(labels), dtype=np.float64)
    weights[-len(top_elements) :] = 0.5
    scale = np.sqrt(target * (1.0 - target) + 0.025)
    return matrix, target, labels, weights / np.square(scale)


def choose_representative(
    all_records: list[Record], train: list[Record], excluded_formulas: set[str]
) -> tuple[list[SelectedCase], dict[str, Any]]:
    reference_by_formula = one_per_formula(all_records)
    candidate_by_formula = one_per_formula(train)
    reference = [
        record
        for formula, record in reference_by_formula.items()
        if formula not in excluded_formulas
    ]
    candidates = [
        record
        for formula, record in candidate_by_formula.items()
        if formula not in excluded_formulas
    ]
    candidates.sort(key=lambda item: item.source_id)
    matrix, target, labels, metric_weights = representative_features(candidates, reference)

    selected_indices: list[int] = []
    selected_mask = np.zeros(len(candidates), dtype=bool)
    current = np.zeros(matrix.shape[1], dtype=np.float64)
    tie_break = np.asarray([stable_fraction(record.source_id) for record in candidates])
    for count in range(30):
        target_partial = target * (count + 1)
        residuals = current[None, :] + matrix - target_partial[None, :]
        scores = np.sum(np.square(residuals) * metric_weights[None, :], axis=1)
        scores[selected_mask] = np.inf
        scores += tie_break * 1e-8
        index = int(np.argmin(scores))
        selected_indices.append(index)
        selected_mask[index] = True
        current += matrix[index]

    target_total = target * 30
    for _ in range(5):
        improved = False
        for position, selected_index in enumerate(tuple(selected_indices)):
            base = current - matrix[selected_index]
            residuals = base[None, :] + matrix - target_total[None, :]
            scores = np.sum(np.square(residuals) * metric_weights[None, :], axis=1)
            scores[selected_mask] = np.inf
            scores[selected_index] = np.sum(np.square(current - target_total) * metric_weights)
            scores += tie_break * 1e-8
            replacement = int(np.argmin(scores))
            old_score = float(np.sum(np.square(current - target_total) * metric_weights))
            new_total = base + matrix[replacement]
            new_score = float(np.sum(np.square(new_total - target_total) * metric_weights))
            if replacement != selected_index and new_score + 1e-10 < old_score:
                selected_mask[selected_index] = False
                selected_mask[replacement] = True
                selected_indices[position] = replacement
                current = new_total
                improved = True
        if not improved:
            break

    selected_records = sorted(
        (candidates[index] for index in selected_indices),
        key=lambda item: (item.formula, item.source_id),
    )
    cases = [
        SelectedCase(
            case_id=f"{CASE_PREFIX}-rep-{index:03d}",
            panel="representative",
            record=record,
            selection_notes=(
                "Selected without baseline outcomes to match capped, "
                "formula-deduplicated MP-20 marginals.",
            ),
        )
        for index, record in enumerate(selected_records, start=1)
    ]
    selected_vector = np.stack(
        [matrix[candidates.index(record)] for record in selected_records]
    ).mean(axis=0)
    report = {
        "reference_formula_count": len(reference),
        "eligible_train_formula_count": len(candidates),
        "feature_diagnostics": [
            {
                "feature": label,
                "reference_fraction": round(float(expected), 8),
                "panel_fraction": round(float(actual), 8),
                "absolute_difference": round(abs(float(actual - expected)), 8),
            }
            for label, expected, actual in zip(labels, target, selected_vector, strict=True)
        ],
    }
    return cases, report


def scattering_ambiguity(record: Record) -> float:
    atomic_numbers = [Element(element).Z for element in record.elements]
    site_numbers = [site.specie.Z for site in record.structure]
    light_fraction = sum(number <= 10 for number in site_numbers) / len(site_numbers)
    heavy_present = max(atomic_numbers) >= 30
    distinct = sorted(set(atomic_numbers))
    adjacent = any(second - first <= 2 for first, second in pairwise(distinct))
    return light_fraction * float(heavy_present) + 0.6 * float(adjacent)


def percentile_ranks(values: list[float]) -> list[float]:
    order = np.argsort(
        np.argsort(np.asarray(values, dtype=np.float64), kind="stable"), kind="stable"
    )
    if len(values) == 1:
        return [1.0]
    return [float(value / (len(values) - 1)) for value in order]


def select_challenge_axis(
    axis: str,
    ranked: list[tuple[Record, float, float]],
    used_formulas: set[str],
    spacegroups: Counter[int],
    anonymous: Counter[str],
) -> list[SelectedCase]:
    selected: list[SelectedCase] = []
    for record, score, percentile in sorted(
        ranked,
        key=lambda item: (-item[1], stable_fraction(item[0].source_id)),
    ):
        if percentile < 0.9 or record.formula_key in used_formulas:
            continue
        if spacegroups[record.spacegroup_number] >= 4:
            continue
        if anonymous[record.anonymous_formula] >= 2:
            continue
        selected.append(
            SelectedCase(
                case_id="",
                panel="challenge",
                record=record,
                primary_axis=axis,
                difficulty_percentile=percentile,
                selection_notes=(f"Primary-axis score: {score:.8g}.",),
            )
        )
        used_formulas.add(record.formula_key)
        spacegroups[record.spacegroup_number] += 1
        anonymous[record.anonymous_formula] += 1
        if len(selected) == 6:
            return selected
    raise RuntimeError(f"could not select six top-decile {axis} challenge cases")


def choose_mp20_challenge(
    all_records: list[Record], train: list[Record], used_formulas: set[str]
) -> list[SelectedCase]:
    reference = list(one_per_formula(all_records).values())
    sg_frequency = Counter(record.spacegroup_number for record in reference)
    candidates = [
        record for formula, record in one_per_formula(train).items() if formula not in used_formulas
    ]
    system_rank = {
        "triclinic": 1.0,
        "monoclinic": 0.8,
        "trigonal": 0.65,
        "hexagonal": 0.5,
        "tetragonal": 0.45,
        "orthorhombic": 0.35,
        "cubic": 0.2,
    }

    rare_shortlist = sorted(
        candidates,
        key=lambda record: (
            sg_frequency[record.spacegroup_number],
            -system_rank[record.crystal_system],
            stable_fraction(record.source_id),
        ),
    )[:300]
    complexity_shortlist = sorted(
        candidates,
        key=lambda record: (
            -(record.nsites / 20 + record.nelements / 5),
            stable_fraction(record.source_id),
        ),
    )[:350]
    congestion_shortlist = sorted(
        candidates,
        key=lambda record: (
            -(record.nsites + 0.05 * record.volume + 4 * system_rank[record.crystal_system]),
            stable_fraction(record.source_id),
        ),
    )[:500]
    scatter_shortlist = sorted(
        candidates,
        key=lambda record: (
            -(
                sum(Element(element).Z <= 10 for element in record.elements)
                + 0.5 * (max(Element(element).Z for element in record.elements) >= 30)
            ),
            -record.nsites,
            stable_fraction(record.source_id),
        ),
    )[:350]

    union = {
        record.source_id: record
        for record in (
            rare_shortlist + complexity_shortlist + congestion_shortlist + scatter_shortlist
        )
    }
    print(f"computing challenge metrics for {len(union)} MP-20 candidates")
    metrics: dict[str, dict[str, float]] = {}
    for index, record in enumerate(union.values(), start=1):
        xrd, _ = record.xrd()
        metrics[record.source_id] = {
            "rare_symmetry": (
                1.0 / math.log2(sg_frequency[record.spacegroup_number] + 2)
                + system_rank[record.crystal_system]
            ),
            "site_chemical_complexity": (
                record.nsites / 20 + record.nelements / 5 + record.independent_sites / record.nsites
            ),
            "peak_congestion": (
                xrd["overlap_intensity_fraction"]
                + xrd["normalized_peak_entropy"]
                + min(xrd["peak_count_above_1pct"] / 50, 1.0)
            ),
            "scattering_ambiguity": scattering_ambiguity(record),
        }
        if index % 200 == 0:
            print(f"computed {index}/{len(union)} challenge profiles")

    axis_shortlists = {
        "rare_symmetry": rare_shortlist,
        "site_chemical_complexity": complexity_shortlist,
        "peak_congestion": congestion_shortlist,
        "scattering_ambiguity": scatter_shortlist,
    }
    spacegroups: Counter[int] = Counter()
    anonymous: Counter[str] = Counter()
    selected: list[SelectedCase] = []
    for axis in (
        "rare_symmetry",
        "site_chemical_complexity",
        "peak_congestion",
        "scattering_ambiguity",
    ):
        available = [record for record in axis_shortlists[axis] if record.source_id in metrics]
        scores = [metrics[record.source_id][axis] for record in available]
        percentiles = percentile_ranks(scores)
        selected.extend(
            select_challenge_axis(
                axis,
                list(zip(available, scores, percentiles, strict=True)),
                used_formulas,
                spacegroups,
                anonymous,
            )
        )
    return selected


def api_headers() -> dict[str, str]:
    api_key = os.environ.get("MP_API_KEY")
    if not api_key:
        raise RuntimeError(f"MP_API_KEY is required to build {DATASET_ID}")
    return {"X-API-KEY": api_key}


def api_get(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            response = requests.get(
                url,
                params=params,
                headers=api_headers(),
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as error:
            last_error = error
            time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"Materials Project API request failed: {last_error}")


def current_mp_versions() -> dict[str, str]:
    heartbeat = api_get(f"{MP_API_ROOT}/heartbeat")
    if heartbeat["db_version"] != EXPECTED_MP_DB_VERSION:
        raise RuntimeError(
            f"MP database changed: {heartbeat['db_version']} != {EXPECTED_MP_DB_VERSION}"
        )
    return {
        "database_version": heartbeat["db_version"],
        "api_version": heartbeat["version"],
        "api_pymatgen_version": heartbeat["pymatgen"],
    }


def fetch_documents(material_ids: list[str], *, structures: bool = True) -> list[dict[str, Any]]:
    fields = [
        "material_id",
        "formula_pretty",
        "composition_reduced",
        "nsites",
        "symmetry",
        "energy_above_hull",
        "formation_energy_per_atom",
        "theoretical",
        "database_IDs",
        "last_updated",
        "density",
        "volume",
    ]
    if structures:
        fields.append("structure")
    documents: list[dict[str, Any]] = []
    for start in range(0, len(material_ids), 90):
        batch = material_ids[start : start + 90]
        payload = api_get(
            SUMMARY_URL,
            {
                "material_ids": ",".join(batch),
                "_limit": 1000,
                "_fields": ",".join(fields),
            },
        )
        documents.extend(payload["data"])
    return documents


def choose_large_challenge(
    train: list[Record],
    used_formulas: set[str],
    existing_challenge: list[SelectedCase],
) -> list[SelectedCase]:
    """Choose six model-supported, top-decile large primitive MP-20 cells."""

    candidates = [
        record for formula, record in one_per_formula(train).items() if formula not in used_formulas
    ]
    site_counts = [record.nsites for record in candidates]
    spacegroups = Counter(case.record.spacegroup_number for case in existing_challenge)
    anonymous = Counter(case.record.anonymous_formula for case in existing_challenge)
    shortlist = [
        record
        for record in candidates
        if 17 <= record.nsites <= 20 and 17 <= record.primitive_site_count <= 20
    ]
    shortlist.sort(
        key=lambda record: (
            -record.primitive_site_count,
            -record.nelements,
            -record.independent_sites,
            record.energy_above_hull,
            stable_fraction(record.source_id),
        )
    )

    selected: list[SelectedCase] = []
    for record in shortlist:
        percentile = sum(value <= record.nsites for value in site_counts) / len(site_counts)
        if percentile < 0.9:
            continue
        if spacegroups[record.spacegroup_number] >= 4:
            continue
        if anonymous[record.anonymous_formula] >= 2:
            continue
        selected.append(
            SelectedCase(
                case_id="",
                panel="challenge",
                record=record,
                primary_axis="large_primitive_cell",
                difficulty_percentile=percentile,
                selection_notes=(
                    "Primitive cell contains 17-20 sites.",
                    "Top-decile MP-20 source-cell site count among unused formulas.",
                    "Exact member of the frozen MP-20 training split.",
                ),
            )
        )
        used_formulas.add(record.formula_key)
        spacegroups[record.spacegroup_number] += 1
        anonymous[record.anonymous_formula] += 1
        if len(selected) == 6:
            return selected
    raise RuntimeError("could not select six compliant 17-20-site challenge cases")


def enrich_mp20_cases(cases: list[SelectedCase]) -> None:
    mp20_cases = [case for case in cases if case.record.source_kind == "mp20"]
    documents = fetch_documents([case.record.source_id for case in mp20_cases])
    by_formula: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for document in documents:
        by_formula[canonical_formula(document["composition_reduced"])[1]].append(document)
    used_current_ids: set[str] = set()
    unmatched_ids: list[str] = []
    for case in mp20_cases:
        matches = by_formula.get(case.record.formula_key, [])
        strict: list[dict[str, Any]] = []
        loose: list[dict[str, Any]] = []
        for document in matches:
            current_id = str(document["material_id"])
            if current_id in used_current_ids:
                continue
            structure = Structure.from_dict(document["structure"])
            if STRICT_MATCHER.fit(case.record.structure, structure):
                strict.append(document)
            elif LOOSE_MATCHER.fit(case.record.structure, structure):
                loose.append(document)
        candidates = strict or loose
        if not candidates:
            unmatched_ids.append(case.record.source_id)
            continue
        document = min(candidates, key=lambda value: str(value["material_id"]))
        case.record.api_doc = document
        document["source_structure_match"] = "strict" if strict else "loose"
        used_current_ids.add(str(document["material_id"]))
    if unmatched_ids:
        print(
            f"retained {len(unmatched_ids)} frozen MP-20 records without a current structure match"
        )


def assign_challenge_ids(cases: list[SelectedCase]) -> None:
    cases.sort(
        key=lambda case: (
            case.primary_axis or "",
            case.record.nsites,
            case.record.formula,
            case.record.source_id,
        )
    )
    for index, case in enumerate(cases, start=1):
        case.case_id = f"{CASE_PREFIX}-challenge-{index:03d}"


def structure_metadata(case: SelectedCase, digest: str) -> dict[str, Any]:
    record = case.record
    xrd, _ = record.xrd()
    api_doc = record.api_doc or {}
    database_ids = api_doc.get("database_IDs") or {}
    if api_doc:
        current_id = str(api_doc["material_id"])
        current_structure_match = str(api_doc["source_structure_match"])
    else:
        current_id: str | None = None
        current_structure_match = "not_found_or_not_structure_matched"
    if record.training_exposure is None:
        raise RuntimeError(f"missing four-way exposure evidence for {record.source_id}")
    exposure = {
        framework: evidence["status"] for framework, evidence in record.training_exposure.items()
    }
    return {
        "case_id": case.case_id,
        "panel": case.panel,
        "path": case.path,
        "sha256": digest,
        "formula": record.formula,
        "reduced_formula_key": record.formula_key,
        "anonymous_formula": record.anonymous_formula,
        "elements": list(record.elements),
        "nelements": record.nelements,
        "cif_site_count": record.nsites,
        "primitive_site_count": record.primitive_site_count,
        "spacegroup_number": record.spacegroup_number,
        "crystal_system": record.crystal_system,
        "volume_angstrom3": round(record.volume, 10),
        "volume_per_atom_angstrom3": round(record.volume_per_atom, 10),
        "density_g_cm3": round(record.density, 10),
        "formation_energy_per_atom_ev": record.formation_energy_per_atom,
        "energy_above_hull_ev_per_atom": record.energy_above_hull,
        "source": {
            "kind": record.source_kind,
            "source_material_id": record.source_id,
            "source_split": record.split,
            "source_row_index": record.row_index,
            "current_material_id": current_id,
            "current_last_updated": api_doc.get("last_updated"),
            "current_structure_match": current_structure_match,
            "database_ids": database_ids,
        },
        "xrd_selection_metrics": {key: round(value, 10) for key, value in xrd.items()},
        "selection": {
            "primary_axis": case.primary_axis,
            "difficulty_percentile": case.difficulty_percentile,
            "notes": list(case.selection_notes),
        },
        "polymorph": (
            {
                "family_id": case.polymorph_family_id,
                "partner_case_id": case.polymorph_partner_id,
                "difficulty": case.polymorph_difficulty,
                "profile_cosine_similarity": case.pair_cosine_similarity,
                "profile_max_absolute_difference": case.pair_max_absolute_difference,
                "source_distinct_cluster_count": case.source_family_clusters,
            }
            if case.panel == "polymorph"
            else None
        ),
        "baseline_exposure": exposure,
        "training_exposure": record.training_exposure,
    }


def write_outputs(
    cases: list[SelectedCase],
    representative_report: dict[str, Any],
    exposure_report: dict[str, Any],
    versions: dict[str, str],
    *,
    replace_existing: bool = False,
) -> None:
    staging = CACHE / f"staging-{DATASET_ID.lower()}"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    (staging / "representative").mkdir()
    (staging / "challenge").mkdir()
    (staging / "polymorph").mkdir()
    (staging / "results").mkdir()

    family_formulas: dict[str, str] = {}
    for case in cases:
        if case.panel == "representative":
            relative = Path("representative") / f"{case.case_id}_{case.record.source_id}.cif"
        elif case.panel == "challenge":
            relative = Path("challenge") / f"{case.case_id}_{case.record.source_id}.cif"
        else:
            assert case.polymorph_family_id is not None
            family_formulas[case.polymorph_family_id] = case.record.formula
            folder = Path("polymorph") / f"{case.polymorph_family_id}_{case.record.formula}"
            (staging / folder).mkdir(exist_ok=True)
            relative = folder / f"{case.case_id}_{case.record.source_id}.cif"
        case.path = relative.as_posix()
        path = staging / relative
        path.write_text(case.record.cif, encoding="utf-8", newline="\n")

    manifest_cases = [
        structure_metadata(case, sha256_file(staging / case.path))
        for case in sorted(cases, key=lambda value: value.case_id)
    ]
    exclusion_metadata = selection_exclusion_metadata()
    manifest = {
        "schema_version": "1.1.0",
        "dataset_id": DATASET_ID,
        "corpus_revision": CORPUS_REVISION,
        "selection_date": SELECTION_DATE,
        "selection_seed": SELECTION_SEED,
        "description": (
            "Single-phase Materials Project structures for pXRD + composition benchmarking."
        ),
        "panel_counts": {"representative": 30, "challenge": 30, "polymorph": 40},
        "source_versions": {
            "mp20_commit": SOURCE_COMMIT,
            **versions,
        },
        "training_intersection": {
            "pxrdgen": "exact MP-20 released training ID and strict structure match",
            "crystalyze": "exact released training ID and strict structure match",
            "decifer": "strict structure match to a record named in public train.h5",
            "diffractgpt": (
                "strict structure match to the later official released train.parquet; "
                "proxy only for the unavailable paper-era split"
            ),
        },
        "selection_exclusions": exclusion_metadata,
        "cases": manifest_cases,
    }
    (staging / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    csv_fields = [
        "case_id",
        "panel",
        "formula",
        "source_material_id",
        "current_material_id",
        "cif_site_count",
        "primitive_site_count",
        "spacegroup_number",
        "crystal_system",
        "primary_axis",
        "polymorph_family_id",
        "polymorph_partner_id",
        "path",
        "sha256",
    ]
    with (staging / "manifest.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=csv_fields)
        writer.writeheader()
        for case in manifest_cases:
            writer.writerow(
                {
                    "case_id": case["case_id"],
                    "panel": case["panel"],
                    "formula": case["formula"],
                    "source_material_id": case["source"]["source_material_id"],
                    "current_material_id": case["source"]["current_material_id"],
                    "cif_site_count": case["cif_site_count"],
                    "primitive_site_count": case["primitive_site_count"],
                    "spacegroup_number": case["spacegroup_number"],
                    "crystal_system": case["crystal_system"],
                    "primary_axis": case["selection"]["primary_axis"],
                    "polymorph_family_id": (case["polymorph"] or {}).get("family_id"),
                    "polymorph_partner_id": (case["polymorph"] or {}).get("partner_case_id"),
                    "path": case["path"],
                    "sha256": case["sha256"],
                }
            )

    challenge_axis_counts = Counter(
        case["selection"]["primary_axis"] for case in manifest_cases if case["panel"] == "challenge"
    )
    difficulty_counts = Counter(
        case["polymorph"]["difficulty"] for case in manifest_cases if case["panel"] == "polymorph"
    )
    difficulty_counts = {key: value // 2 for key, value in difficulty_counts.items()}
    selection_report = {
        "source_row_counts": {split: values[2] for split, values in SOURCE_FILES.items()},
        "source_total_rows": sum(values[2] for values in SOURCE_FILES.values()),
        "training_intersection": exposure_report,
        "selection_exclusions": exclusion_metadata,
        "representative": representative_report,
        "challenge_axis_counts": dict(sorted(challenge_axis_counts.items())),
        "polymorph_pair_difficulty_counts": dict(sorted(difficulty_counts.items())),
        "polymorph_family_formulas": dict(sorted(family_formulas.items())),
        "large_primitive_site_counts": sorted(
            case["primitive_site_count"]
            for case in manifest_cases
            if case["selection"]["primary_axis"] == "large_primitive_cell"
        ),
    }
    (staging / "selection-report.json").write_text(
        json.dumps(selection_report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    exposure_source_lock = json.loads(EXPOSURE_SOURCE_LOCK.read_text(encoding="utf-8"))
    relevant_sources = {
        name: exposure_source_lock["sources"][name]
        for name in (
            "crystalyze_mp20",
            "decifer_noma",
            "diffractgpt_released",
            "pxrdgen_mp20",
        )
    }
    source_lock = {
        "schema_version": "1.1.0",
        "corpus_revision": CORPUS_REVISION,
        "mp20": {
            "repository": "https://github.com/txie-93/cdvae",
            "commit": SOURCE_COMMIT,
            "files": {
                split: {"filename": values[0], "sha256": values[1], "rows": values[2]}
                for split, values in SOURCE_FILES.items()
            },
        },
        "materials_project": {
            **versions,
            "terms": "Materials Project terms of use",
            "api_key_committed": False,
        },
        "framework_training_sources": relevant_sources,
        "exposure_index": exposure_source_lock["index"],
        "decifer_serialized_train": {
            "path": str(DECIFER_TRAIN_H5.relative_to(ROOT)),
            "size_bytes": DECIFER_TRAIN_H5.stat().st_size,
            "sha256": sha256_file(DECIFER_TRAIN_H5),
            "membership_field": "cif_name",
        },
        "diffractgpt_membership_caveat": (
            "The official released train.parquet postdates the paper checkpoint and is "
            "used only as an explicitly labeled proxy for paper-era membership."
        ),
        "pxrd_ood_formula_guard": {
            "manifest": str(PXRD_OOD_MANIFEST.relative_to(ROOT)),
            "manifest_sha256": sha256_file(PXRD_OOD_MANIFEST),
        },
        "selection_exclusions": exclusion_metadata,
        "selection_seed": SELECTION_SEED,
    }
    if SUPERSEDED_ARCHIVE is not None:
        archived_manifest = ROOT / SUPERSEDED_ARCHIVE / "manifest.json"
        active_manifest = ROOT / "pXRD-100" / "manifest.json"
        superseded_manifest = archived_manifest if archived_manifest.is_file() else active_manifest
        source_lock["supersedes"] = {
            "archive": SUPERSEDED_ARCHIVE,
            "manifest_sha256": (
                sha256_file(superseded_manifest) if superseded_manifest.is_file() else None
            ),
        }
    (staging / "SOURCE.lock.json").write_text(
        json.dumps(source_lock, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    exclusion_names = ", ".join(item["path"] for item in exclusion_metadata)
    exclusion_readme = (
        f"- Reduced formulas occurring in `{exclusion_names}` are excluded.\n"
        if exclusion_names
        else ""
    )
    mandatory_readme = (
        f" `{MANDATORY_POLYMORPH_FORMULA}` is the declared mandatory family."
        if MANDATORY_POLYMORPH_FORMULA
        else " No formula is mandatory in this disjoint selection."
    )
    variant_name = "development-v2" if DATASET_ID == "pXRD-100-v2" else "canonical"
    readme = f"""# {DATASET_ID}

This directory contains 100 single-phase Materials Project structures selected for a
powder-XRD-plus-composition benchmark: 30 representative cases, 30 challenge cases,
and 20 two-member polymorph families (40 CIFs). `manifest.json` is authoritative.

## Selection basis

- All 100 cases are exact members of the frozen MP-20 training split at CDVAE commit
  `{SOURCE_COMMIT}`.
- Every case also has an audited strict structure match in the released Crystalyze
  training split, the public deCIFer `train.h5`, and DiffractGPT's later official
  released training split. The latter is explicitly a proxy for the unavailable
  paper-era DiffractGPT split.
{exclusion_readme}- The selection is formula-disjoint from every declared exclusion
  corpus; source IDs and CIF hashes are checked separately by the audit.
- The six `large_primitive_cell` challenge cases have 17--20 primitive sites and are
  in the top decile of the eligible unused MP-20 formula population by site count.
- All selection used seed `{SELECTION_SEED}` and descriptors fixed before running any
  compared framework. CIF targets were not selected using model outcomes.
- Ideal selection profiles use Cu K-alpha-1, 5--90 degrees two-theta, a 0.05-degree
  grid, and 0.12-degree Gaussian sigma, matching sim-bench conventions.

## Important applicability note

Crystalyze has a published 20-site model cap, while PXRDGen was trained on MP-20
primitive cells containing at most 20 sites. Every current case, including the six
large-cell challenges, lies within those respective applicability envelopes.

## Files

- `manifest.json`: complete structure, provenance, selection, exposure, and hash data.
- `manifest.csv`: compact human-readable case index.
- `selection-report.json`: panel diagnostics and exact quota checks.
- `SELECTION.md`: the selection protocol and benchmark applicability rules.
- `SOURCE.lock.json`: source commits, file hashes, API/database versions, and seed.
- `FRAMEWORKS.md`: cross-framework input contracts, readiness, and audit commands.
- `representative/`, `challenge/`, `polymorph/`: the 100 ground-truth CIFs.
- `targets/`: framework-specific diffraction inputs and parameter manifests.
- `results/`: generated candidates and evaluation artifacts, when present.

The CIFs are ground truth and should remain hidden from evaluated methods. Benchmark
inputs should expose only the simulated pXRD pattern and reduced composition.
"""
    (staging / "README.md").write_text(readme, encoding="utf-8", newline="\n")

    frameworks = """# Framework target contracts

This corpus revision is prepared for Crystalyze, deCIFer, PXRDGen, and DiffractGPT.
Each target manifest binds its arrays to the authoritative top-level `manifest.json`
SHA-256. No v1 generations or scores are valid for this revision.

- **Crystalyze:** reduced composition plus its native Caglioti-broadened Cu K-alpha
  profile after encoder interpolation and low-angle masking.
- **deCIFer:** reduced composition for the primary condition and exact full-cell
  composition only for the labeled oracle; both use the clean 1,000-bin Q profile.
- **PXRDGen:** the benchmark oracle receives the exact primitive-cell atom counts and
  the frozen 7,500-bin GSAS-II `ycalc` profile.
- **DiffractGPT:** reduced composition plus the frozen 180-bin, three-decimal input.
  The Gaussian-width detail absent from the released paper/code remains documented
  in the target parameter manifest.

The `results/` directory intentionally contains no inference outputs. Run inference
again before evaluating this revision.
"""
    (staging / "FRAMEWORKS.md").write_text(frameworks, encoding="utf-8", newline="\n")
    (staging / "results" / "README.md").write_text(
        "# Results\n\nNo inference outputs are included for corpus revision "
        f"`{CORPUS_REVISION}`.\n",
        encoding="utf-8",
        newline="\n",
    )

    selection_protocol = f"""# {DATASET_ID} selection protocol

## Fixed sources and eligibility

The primary population is the MP-20 data at CDVAE commit `{SOURCE_COMMIT}`. Source
CSV hashes and row counts are locked in `SOURCE.lock.json`. A selectable MP-20 record
must have a numeric MP identifier, an ordered structure with 1--20 sites, energy
above hull at most 0.08 eV/atom, and formation energy below 2 eV/atom. Every selected
MP-20 structure is an exact member of the frozen **training split**.

Selection candidates must additionally be strict structure matches in Crystalyze's
released train split and deCIFer's public `train.h5`. They must also match the later
official DiffractGPT `train.parquet`, which is recorded as a released-split proxy
because the paper-era split is not public. Matcher tolerances are ltol 0.20, stol
0.30, angle tolerance 5 degrees, primitive-cell comparison, scaling enabled, and no
supercell search. The declared exclusion manifests are hash-bound in
`SOURCE.lock.json`; all of their reduced formulas are excluded.

Selection is deterministic under seed `{SELECTION_SEED}` and never uses the output of
Crystalyze, PXRDGen, deCIFer, diffractGPT, DARA, or AGAPI-XRD.

## Representative panel (30)

The target distribution is a formula-deduplicated, eligibility-filtered view of all
MP-20 splits. One lowest-energy candidate per reduced formula is available from the
training split. Formulas reserved for the polymorph panel are removed. A greedy
moment-matching selection followed by deterministic swaps minimizes disagreement in:

- crystal system;
- source-CIF site bins 1--4, 5--8, 9--12, 13--16, and 17--20;
- element-count and energy-above-hull bins;
- volume-per-atom and density quartiles; and
- incidence of the 20 most frequent elements.

This is a capped natural-distribution estimate: a prolific formula contributes only
one population unit and cannot dominate the panel.

## Challenge panel (30)

Thirty cases are selected from unused MP-20 training formulas, six from the top
decile of each predeclared score:

- `rare_symmetry`: inverse space-group frequency plus a crystal-system rarity prior;
- `site_chemical_complexity`: site count, element count, and independent-site ratio;
- `peak_congestion`: peak overlap, normalized intensity entropy, and peak count; and
- `scattering_ambiguity`: light/heavy-element contrast and nearby atomic numbers;
- `large_primitive_cell`: source-CIF site count, with primitive cells restricted to
  17--20 sites and deterministic preference for chemistry and independent-site count.

Across all five axes, space-group reuse is capped at four, anonymous-formula reuse at
two, and reduced formulas are unique.

Diffraction-based selection descriptors use ideal Cu K-alpha-1 patterns from 5 to 90
degrees two-theta, sampled every 0.05 degree with 0.12-degree Gaussian sigma.

## Polymorph panel (40)

Twenty reduced formulas contribute exactly two structures. A source family must have
at least three training records and at least three StructureMatcher-distinct clusters;
the selected pair must also be distinct.{mandatory_readme} Pair difficulty is based
on cosine similarity of the fixed ideal pXRD profiles, with quotas of 5 easy, 10
medium, and 5 hard pairs. The manifest records partner IDs, similarity, maximum
profile difference, and source cluster count.

## Audit and evaluation rules

`uv run python pxrd-bench/generation/build_pxrd_100.py audit --variant {variant_name}`
works offline and checks all CIF hashes,
ordered structures, panel/axis quotas, site limits, unique paths and IDs, formula
deduplication, polymorph pairing, and structural non-equivalence.

`uv run --with h5py==3.16.0 python pxrd-bench/generation/build_pxrd_100.py audit
--variant {variant_name} --deep-exposure`
additionally re-hashes the 11 GB exposure index and deCIFer
`train.h5`, resolves every recorded training row, and repeats all 400 strict
cross-framework structure comparisons.

The CIFs and selection metadata are ground truth. Evaluated methods receive only the
simulated pXRD and the composition contract declared for each benchmark condition.
Exact training-exposure evidence is recorded per case and is an eligibility rule for
this revision, not a scoring outcome.
"""
    (staging / "SELECTION.md").write_text(selection_protocol, encoding="utf-8", newline="\n")

    audit_directory(staging)
    if OUTPUT.exists():
        if not replace_existing:
            raise RuntimeError(f"refusing to overwrite existing output: {OUTPUT}")
        backup = CACHE / "replaced-21-48-site-corpus"
        if backup.exists():
            raise RuntimeError(f"refusing to overwrite recovery backup: {backup}")
        backup.mkdir(parents=True)
        managed_paths = (
            "representative",
            "challenge",
            "polymorph",
            "manifest.json",
            "manifest.csv",
            "selection-report.json",
            "SOURCE.lock.json",
            "README.md",
            "SELECTION.md",
            "FRAMEWORKS.md",
            "results",
        )
        for name in managed_paths:
            current = OUTPUT / name
            if current.exists():
                current.replace(backup / name)
        for name in managed_paths:
            (staging / name).replace(OUTPUT / name)
        staging.rmdir()
    else:
        staging.replace(OUTPUT)


def deep_exposure_audit(root: Path, cases: list[dict[str, Any]]) -> int:
    train_names = load_decifer_train_names()
    source_lock = json.loads((root / "SOURCE.lock.json").read_text(encoding="utf-8"))
    expected_h5_hash = source_lock["decifer_serialized_train"]["sha256"]
    if sha256_file(DECIFER_TRAIN_H5) != expected_h5_hash:
        raise ValueError("deCIFer train.h5 digest mismatch")
    exposure_lock = json.loads(EXPOSURE_SOURCE_LOCK.read_text(encoding="utf-8"))
    if sha256_file(EXPOSURE_INDEX) != exposure_lock["index"]["sha256"]:
        raise ValueError("framework exposure-index digest mismatch")
    connection = sqlite3.connect(f"file:{EXPOSURE_INDEX}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    expected_sources = {
        "pxrdgen": ("pxrdgen_mp20", "train"),
        "crystalyze": ("crystalyze_mp20", "train"),
        "decifer": ("decifer_noma", None),
        "diffractgpt": ("diffractgpt_released", "train"),
    }
    for case in cases:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structure = Structure.from_file(root / case["path"])
        for framework, (source, split) in expected_sources.items():
            evidence = case["training_exposure"][framework]
            row = exposure_row(connection, source, evidence["record_id"])
            if row is None:
                raise ValueError(f"{case['case_id']}: missing {framework} exposure row")
            if split is not None and row["split"] != split:
                raise ValueError(f"{case['case_id']}: wrong {framework} split")
            if framework == "decifer" and str(row["locator"]) not in train_names:
                raise ValueError(f"{case['case_id']}: deCIFer record is not in train.h5")
            try:
                matched = STRICT_MATCHER.fit(structure, load_index_structure(row))
            except Exception as exc:
                raise ValueError(f"{case['case_id']}: cannot compare {framework} exposure") from exc
            if not matched:
                raise ValueError(f"{case['case_id']}: {framework} structure mismatch")
    connection.close()
    return len(cases)


def audit_directory(root: Path, *, deep_exposure: bool = False) -> dict[str, Any]:
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = manifest["cases"]
    if len(cases) != 100:
        raise ValueError(f"expected 100 cases, found {len(cases)}")
    panel_counts = Counter(case["panel"] for case in cases)
    if panel_counts != Counter({"representative": 30, "challenge": 30, "polymorph": 40}):
        raise ValueError(f"wrong panel counts: {panel_counts}")
    if len({case["case_id"] for case in cases}) != 100:
        raise ValueError("case IDs are not unique")
    if len({case["path"] for case in cases}) != 100:
        raise ValueError("case paths are not unique")
    is_fourway_revision = bool(manifest.get("training_intersection"))
    if is_fourway_revision:
        required_frameworks = {"crystalyze", "pxrdgen", "decifer", "diffractgpt"}
        for case in cases:
            source_id = str(case["source"]["source_material_id"])
            if not NUMERIC_MP_ID.fullmatch(source_id):
                raise ValueError(f"non-numeric Materials Project ID: {source_id}")
            if case["source"]["source_split"] != "train":
                raise ValueError(f"non-training MP-20 source: {case['case_id']}")
            evidence = case.get("training_exposure") or {}
            if set(evidence) != required_frameworks:
                raise ValueError(f"incomplete training exposure: {case['case_id']}")
            expected_status = {
                "crystalyze": "exact_train",
                "pxrdgen": "exact_train",
                "decifer": "exact_train",
                "diffractgpt": "released_train_proxy",
            }
            for framework, status in expected_status.items():
                if evidence[framework].get("status") != status:
                    raise ValueError(f"wrong {framework} exposure status: {case['case_id']}")

    structures: dict[str, Structure] = {}
    for case in cases:
        path = root / case["path"]
        if not path.is_file():
            raise ValueError(f"missing CIF: {case['path']}")
        if sha256_file(path) != case["sha256"]:
            raise ValueError(f"hash mismatch: {case['path']}")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structure = Structure.from_file(path)
        structures[case["case_id"]] = structure
        if not structure.is_ordered or len(structure) != case["cif_site_count"]:
            raise ValueError(f"invalid structure metadata: {case['case_id']}")
        primitive = SpacegroupAnalyzer(structure, symprec=0.1, angle_tolerance=5).find_primitive()
        primitive_count = len(primitive or structure)
        if primitive_count != case["primitive_site_count"]:
            raise ValueError(f"primitive-site metadata mismatch: {case['case_id']}")
        if (
            case["selection"]["primary_axis"] == "large_primitive_cell"
            and not 17 <= primitive_count <= 20
        ):
            raise ValueError(f"large-cell range failed: {case['case_id']}")
        if len(structure) > 20:
            raise ValueError(f"unexpected >20-site case: {case['case_id']}")
        if is_fourway_revision and primitive_count > 20:
            raise ValueError(f"unexpected >20-site primitive: {case['case_id']}")

    challenge_axes = Counter(
        case["selection"]["primary_axis"] for case in cases if case["panel"] == "challenge"
    )
    if set(challenge_axes.values()) != {6} or len(challenge_axes) != 5:
        raise ValueError(f"challenge quotas failed: {challenge_axes}")
    challenge_cases = [case for case in cases if case["panel"] == "challenge"]
    challenge_spacegroups = Counter(case["spacegroup_number"] for case in challenge_cases)
    challenge_anonymous = Counter(case["anonymous_formula"] for case in challenge_cases)
    if max(challenge_spacegroups.values()) > 4:
        raise ValueError(f"challenge space-group cap failed: {challenge_spacegroups}")
    if max(challenge_anonymous.values()) > 2:
        raise ValueError(f"challenge anonymous-formula cap failed: {challenge_anonymous}")
    if any(float(case["selection"]["difficulty_percentile"]) < 0.9 for case in challenge_cases):
        raise ValueError("challenge top-decile requirement failed")

    families: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        if case["panel"] == "polymorph":
            families[case["polymorph"]["family_id"]].append(case)
    if len(families) != 20 or any(len(group) != 2 for group in families.values()):
        raise ValueError("polymorph family count/size failed")
    for family_id, members in families.items():
        first, second = members
        if first["reduced_formula_key"] != second["reduced_formula_key"]:
            raise ValueError(f"formula mismatch in {family_id}")
        if first["polymorph"]["partner_case_id"] != second["case_id"]:
            raise ValueError(f"partner mismatch in {family_id}")
        if STRICT_MATCHER.fit(structures[first["case_id"]], structures[second["case_id"]]):
            raise ValueError(f"polymorph pair is structurally duplicate: {family_id}")
        if int(first["polymorph"]["source_distinct_cluster_count"]) < 3:
            raise ValueError(f"source family too small: {family_id}")

    nonpoly_formulas = [
        case["reduced_formula_key"] for case in cases if case["panel"] != "polymorph"
    ]
    polymorph_formulas = {members[0]["reduced_formula_key"] for members in families.values()}
    if len(nonpoly_formulas) != len(set(nonpoly_formulas)):
        raise ValueError("representative/challenge formulas are not unique")
    if set(nonpoly_formulas) & polymorph_formulas:
        raise ValueError("a polymorph formula leaked into another panel")
    if len(set(nonpoly_formulas) | polymorph_formulas) != 80:
        raise ValueError("expected exactly 80 reduced-formula families")
    if is_fourway_revision and PXRD_OOD_MANIFEST.is_file():
        overlap = (set(nonpoly_formulas) | polymorph_formulas) & ood_formula_keys()
        if overlap:
            raise ValueError(f"formula overlap with pXRD-ood: {sorted(overlap)}")

    selected_formulas = set(nonpoly_formulas) | polymorph_formulas
    selected_source_ids = {str(case["source"]["source_material_id"]) for case in cases}
    selected_hashes = {str(case["sha256"]) for case in cases}
    audited_exclusions = 0
    for exclusion in manifest.get("selection_exclusions", []):
        exclusion_root = ROOT / str(exclusion["path"])
        exclusion_manifest_path = exclusion_root / "manifest.json"
        if sha256_file(exclusion_manifest_path) != exclusion["manifest_sha256"]:
            raise ValueError(f"exclusion manifest hash mismatch: {exclusion_root}")
        exclusion_manifest = json.loads(exclusion_manifest_path.read_text(encoding="utf-8"))
        exclusion_cases = exclusion_manifest["cases"]
        formula_overlap = selected_formulas & {
            str(case["reduced_formula_key"]) for case in exclusion_cases
        }
        source_overlap = selected_source_ids & {
            str(case.get("source", {}).get("source_material_id", "")) for case in exclusion_cases
        }
        hash_overlap = selected_hashes & {str(case.get("sha256", "")) for case in exclusion_cases}
        if formula_overlap or source_overlap or hash_overlap:
            raise ValueError(
                f"overlap with {exclusion_root}: formulas={sorted(formula_overlap)}, "
                f"source_ids={sorted(source_overlap)}, hashes={sorted(hash_overlap)}"
            )
        audited_exclusions += 1

    cif_files = [
        path
        for folder in ("representative", "challenge", "polymorph")
        for path in (root / folder).rglob("*.cif")
    ]
    if len(cif_files) != 100:
        raise ValueError(f"expected 100 CIF files, found {len(cif_files)}")
    deep_exposure_cases = deep_exposure_audit(root, cases) if deep_exposure else 0
    return {
        "cases": len(cases),
        "panels": dict(sorted(panel_counts.items())),
        "challenge_axes": dict(sorted(challenge_axes.items())),
        "polymorph_families": len(families),
        "reduced_formula_families": 80,
        "corpus_revision": manifest.get("corpus_revision", "v1"),
        "four_way_training_exposure_cases": 100 if is_fourway_revision else 0,
        "audited_exclusion_corpora": audited_exclusions,
        "deep_exposure_audit_cases": deep_exposure_cases,
    }


def build(*, replace_existing: bool = False) -> None:
    if OUTPUT.exists() and not replace_existing:
        raise RuntimeError(f"output already exists: {OUTPUT}; run audit instead")
    versions = current_mp_versions()
    download_sources()
    split_records = load_records()
    train = split_records["train"]
    all_records = [record for values in split_records.values() for record in values]
    print(
        f"loaded {len(all_records)} MP-20 rows; "
        f"{sum(eligible_mp20(record) for record in train)} eligible training records"
    )

    exposed_train, exposure_report = four_way_training_intersection(train)
    print(
        f"qualified {len(exposed_train)} MP-20 train structures in the four-way "
        "training intersection"
    )
    forbidden_formulas = selection_forbidden_formula_keys()
    polymorph_cases, used_formulas = choose_polymorphs(exposed_train, train, forbidden_formulas)
    used_formulas.update(forbidden_formulas)
    print(f"selected {len(polymorph_cases) // 2} polymorph families")
    representative_cases, representative_report = choose_representative(
        all_records, exposed_train, used_formulas
    )
    used_formulas.update(case.record.formula_key for case in representative_cases)
    print("selected 30 representative cases")
    mp20_challenge = choose_mp20_challenge(all_records, exposed_train, used_formulas)
    print("selected 24 MP-20 challenge cases")
    large_challenge = choose_large_challenge(exposed_train, used_formulas, mp20_challenge)
    challenge_cases = mp20_challenge + large_challenge
    assign_challenge_ids(challenge_cases)
    print("selected six 17-20-site challenge cases")

    cases = representative_cases + challenge_cases + polymorph_cases
    enrich_mp20_cases(cases)
    print("validated selected MP-20 IDs against the current MP API")
    write_outputs(
        cases,
        representative_report,
        exposure_report,
        versions,
        replace_existing=replace_existing,
    )
    report = audit_directory(OUTPUT)
    print(json.dumps(report, indent=2, sort_keys=True))


def configure_variant(variant: str) -> Path:
    global CASE_PREFIX
    global CORPUS_REVISION
    global DATASET_ID
    global MANDATORY_POLYMORPH_FORMULA
    global SELECTION_DATE
    global SELECTION_EXCLUSION_CORPORA
    global SELECTION_SEED
    global SUPERSEDED_ARCHIVE

    if variant == "canonical":
        return ROOT / "pXRD-100"
    if variant != "development-v2":
        raise ValueError(f"unknown corpus variant: {variant}")

    DATASET_ID = "pXRD-100-v2"
    CASE_PREFIX = "pxrd100v2"
    CORPUS_REVISION = "v2-fourway-disjoint-20260810"
    SELECTION_DATE = "2026-08-10"
    SELECTION_SEED = 20260810
    SUPERSEDED_ARCHIVE = None
    MANDATORY_POLYMORPH_FORMULA = None
    SELECTION_EXCLUSION_CORPORA = (
        ROOT / "pXRD-100",
        ROOT / "pXRD-100-v1-mixed-framework-exposure-20260718",
        ROOT / "pXRD-ood",
        ROOT / "pXRD-ood-v2",
    )
    return ROOT / "pXRD-100-v2"


def main() -> None:
    global OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "rebuild", "audit"))
    parser.add_argument("--variant", choices=("canonical", "development-v2"), default="canonical")
    parser.add_argument("--corpus-root", type=Path)
    parser.add_argument("--deep-exposure", action="store_true")
    args = parser.parse_args()
    default_output = configure_variant(args.variant)
    OUTPUT = (args.corpus_root or default_output).resolve()
    if args.command in {"build", "rebuild"}:
        build(replace_existing=args.command == "rebuild")
    else:
        if not OUTPUT.is_dir():
            raise RuntimeError(f"missing output directory: {OUTPUT}")
        print(
            json.dumps(
                audit_directory(OUTPUT, deep_exposure=args.deep_exposure),
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        raise
