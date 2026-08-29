"""Build the frozen exposure index used to certify pXRD-ood novelty.

Large source archives remain under ``.runs/pxrd-ood/sources``.  The SQLite
index stores normalized formula keys and compressed structure payloads so each
candidate can receive an exact, reproducible StructureMatcher audit without
loading a multi-million-record corpus into memory.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import os
import pickletools
import re
import sqlite3
import sys
import time
import warnings
import zipfile
import zlib
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import requests
import zstandard as zstd
from fastparquet import ParquetFile, core, parquet_thrift
from fastparquet.cencoding import NumpyIO, ThriftObject
from pymatgen.core import Composition, Lattice, Structure

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".runs" / "pxrd-ood"
SOURCES = CACHE / "sources"
INDEX = CACHE / "indexes" / "exposure.sqlite3"
LOCK = CACHE / "SOURCE.lock.json"
COD_DELTA = SOURCES / "cod-current-delta-2026-07-19"
COD_INVENTORY = SOURCES / "cod-official-rsync-inventory-2026-07-19.jsonl.gz"
COD_INVENTORY_REPORT = SOURCES / "cod-official-rsync-inventory-2026-07-19.json"
MP_API_ROOT = "https://api.materialsproject.org"
MP_EXPECTED_DB_VERSION = "2026.04.13"
MP_EXPECTED_RECORDS = 154_377
COD_MIN_PARSEABLE_RECORDS = 533_000
FREEZE_DATE = "2026-07-19"

FRAMEWORK_BOUNDARIES = {
    "Crystalyze": {
        "classification": "exact",
        "sources": ["crystalyze_mp20"],
        "boundary": "all 45,052 records in the exact released MP-20 split archive",
    },
    "PXRDGen": {
        "classification": "exact",
        "sources": ["pxrdgen_mp20"],
        "boundary": "all 45,229 records in the standard CDVAE MP-20 split",
    },
    "deCIFer": {
        "classification": "conservative_superset",
        "sources": ["decifer_noma"],
        "boundary": (
            "all 2,285,914 unique records in the released NOMA pickle, including "
            "2,568 records above the 2,283,346 count stated in the paper"
        ),
    },
    "DiffractGPT": {
        "classification": "conservative_superset",
        "sources": ["jarvis_dft_2022", "diffractgpt_released"],
        "boundary": (
            "union of the official 75,993-entry JARVIS snapshot and 75,997 released examples"
        ),
    },
    "DARA": {
        "classification": "exact_public_plus_licensed_unchecked",
        "sources": ["dara_cod_2024", "cod_current"],
        "boundary": (
            "exact bundled public-COD index plus the complete 2026-07-06 active "
            "snapshot and every official live-only CIF through 2026-07-19; ICSD unchecked"
        ),
    },
    "AGAPI-XRD": {
        "classification": "inferred_conservative",
        "sources": ["jarvis_dft_2022", "cod_current"],
        "boundary": (
            "frozen JARVIS plus the 2026-07-06 active COD snapshot and every official "
            "live-only CIF through 2026-07-19, conservatively approximating the reported stores"
        ),
    },
    "Materials Project supplemental guard": {
        "classification": "dynamic_frozen",
        "sources": ["materials_project_2026_04_13"],
        "boundary": "all structures returned by MP database release 2026.04.13",
    },
}

MP20_FILES = {
    "train": (
        "train.csv",
        "133bab58dba02d316f9f91174839f17802dce648be4e8659d1a42b32b97fa01d",
        27136,
    ),
    "val": ("val.csv", "7b5f4085464b3eac9fd2123acee97ec372214004ce7e983b535b33395abc3e29", 9047),
    "test": ("test.csv", "dd605c7543cf95a13e150aed630d0915e74edc8dea17e85301ee6fbfeb7f500a", 9046),
}
CRYSTALYZE_SPLITS = {
    "train": (
        "mp_20_final/train.csv",
        "2cf5ddd5398e061f4d6e2b2c0e79c516b07bb06da5dda481036a72a8b420f2c0",
        36006,
    ),
    "val": (
        "mp_20_final/val.csv",
        "600224c223dd45846fbad4ccd766ea1add6ac98ef8804900fd39ff49328da6bc",
        4523,
    ),
    "test": (
        "mp_20_final/test.csv",
        "2b73586819290b31f80faf8810196ce2c34048d0753fd61dfd276cee71cd3d4a",
        4523,
    ),
}
ASSETS = {
    "crystalyze_mp20": {
        "path": SOURCES / "crystalyze-mp_20_final.zip",
        "expected_size": 3_419_310_082,
        "expected_sha256": "b96ec2c56c80f1569d4e16674836014a9b5b45585d72c164a44165dd8805ae93",
        "boundary": "exact_released_full_corpus",
    },
    "noma": {
        "path": SOURCES / "noma_cifs_raw.pkl.gz",
        "expected_size": 418_137_968,
        "expected_sha256": "ec5d0a08ef63d33db3ecf8f6407df01f184d961ec0721a12d5abac097aaea328",
        # The frozen archive contains 2,285,914 serialized tuples with 2,285,914
        # unique source IDs, 2,568 more than the paper's stated count.  We index
        # the exact released archive as a conservative checkpoint-exposure bound.
        "expected_raw_tuples": 2_285_914,
        "expected_unique_ids": 2_285_914,
        "paper_reported_records": 2_283_346,
        "boundary": "exact_released_full_corpus_conservative_documented_count_superset",
    },
    "jarvis_2022": {
        "path": SOURCES / "jdft_3d-12-12-2022.json.zip",
        "expected_sha256": "d4c64660e9e1fa45c82bd8868a96ec10162195eed69636445972c05550d8d0d6",
        "expected_records": 75_993,
        "boundary": "official_snapshot_conservative_full_corpus",
    },
    "diffractgpt_train": {
        "path": SOURCES / "diffractgpt-train.parquet",
        "expected_sha256": "62784a3e4f516a20a424ab865a607845f45365d4c421a372c60cf3e84b1cae81",
        "expected_records": 72_198,
        "boundary": "exact_released_split",
    },
    "diffractgpt_test": {
        "path": SOURCES / "diffractgpt-test.parquet",
        "expected_sha256": "1016af848b4b88e9c746ea0f9407d99ae9fd1fc543982249f8a131de7238e9fb",
        "expected_records": 3_799,
        "boundary": "exact_released_split",
    },
    "dara_cod_index": {
        "path": SOURCES / "dara-cod_filtered_info_2024.json.gz",
        "expected_sha256": "03599f54f03f04420523dca36cc06927b74ce0070a4a80e6d859faa38a6c5aed",
        "expected_unique_records": 62_098,
        "boundary": "exact_released_retrieval_index",
    },
    "cod_current": {
        "path": SOURCES / "cod-full-2026-07-06.parquet",
        "expected_size": 30_397_863_592,
        "expected_sha256": "bd87b1279c2d17278b037cb35e052cc252c84c80b56ceaedd13e0c6d42822a88",
        "expected_records": 533_486,
        "boundary": "complete_active_public_cod_snapshot_2026_07_06",
    },
}

FORMULA_SUM = re.compile(
    r"^_chemical_formula_sum\s+(?:'([^']+)'|\"([^\"]+)\"|(\S.*))$", re.MULTILINE
)
FORMULA_STRUCTURAL = re.compile(
    r"^_chemical_formula_structural\s+(?:'([^']+)'|\"([^\"]+)\"|(\S.*))$",
    re.MULTILINE,
)
SG_NUMBER = re.compile(
    r"^_(?:symmetry_Int_Tables_number|space_group_IT_number)\s+(\d+)", re.MULTILINE
)
DIFFRACTGPT_FORMULA = re.compile(r"The chemical formula is:\s*([^\.\n]+)")
COD_EMBEDDED_FILE = re.compile(r"(?ms)^_(?:shelx_res_file|shelx_hkl_file)\s*\n;.*?^;[ \t]*\r?$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_stream(stream: Any) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def canonical_formula(value: str | dict[str, float]) -> tuple[str, str, str]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        composition = Composition(value).reduced_composition
    return (
        composition.reduced_formula,
        composition.alphabetical_formula,
        composition.anonymized_formula,
    )


def formula_from_cif(cif: str) -> tuple[str, str, str]:
    for regex in (FORMULA_SUM, FORMULA_STRUCTURAL):
        match = regex.search(cif)
        if match is None:
            continue
        raw = next(group for group in match.groups() if group is not None).strip()
        raw = raw.split("#", 1)[0].strip()
        try:
            return canonical_formula(raw)
        except (TypeError, ValueError):
            continue
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        structure = Structure.from_str(cif, fmt="cif")
    return canonical_formula(structure.composition.as_dict())


def sg_from_cif(cif: str) -> int | None:
    match = SG_NUMBER.search(cif)
    return int(match.group(1)) if match else None


def compress_text(value: str) -> bytes:
    return zlib.compress(value.encode("utf-8"), level=6)


class LimitedReader:
    """Expose exactly one compressed Parquet page to a streaming decoder."""

    def __init__(self, stream: Any, size: int) -> None:
        self.stream = stream
        self.remaining = size

    def read(self, size: int = -1) -> bytes:
        if self.remaining <= 0:
            return b""
        if size < 0 or size > self.remaining:
            size = self.remaining
        result = self.stream.read(size)
        self.remaining -= len(result)
        return result

    def readable(self) -> bool:
        return True


def read_exact(stream: Any, size: int) -> bytes:
    result = bytearray()
    while len(result) < size:
        chunk = stream.read(size - len(result))
        if not chunk:
            raise EOFError(f"needed {size} bytes, found {len(result)}")
        result.extend(chunk)
    return bytes(result)


def skip_exact(stream: Any, size: int) -> None:
    while size:
        chunk = stream.read(min(size, 4 * 1024 * 1024))
        if not chunk:
            raise EOFError(f"needed {size} more bytes")
        size -= len(chunk)


def compact_cod_cif(raw: bytes) -> tuple[str, int]:
    cif = raw.decode("utf-8", errors="replace")
    compact = COD_EMBEDDED_FILE.sub("", cif).rstrip() + "\n"
    return compact, len(raw) - len(compact.encode("utf-8"))


def iter_cod_row_group_cifs(
    stream: Any,
    fast_parquet: ParquetFile,
    row_group_number: int,
) -> Iterator[tuple[str, int]]:
    """Yield compact CIFs without expanding a multi-gigabyte Parquet row group."""
    row_group = fast_parquet.row_groups[row_group_number]
    metadata = next(
        column.meta_data
        for column in row_group.columns
        if column.meta_data.path_in_schema == ["cif_text"]
    )
    if metadata.statistics is None or metadata.statistics.null_count != 0:
        raise RuntimeError(f"COD row group {row_group_number} has null CIF values")
    offset = metadata.dictionary_page_offset or metadata.data_page_offset
    end = offset + metadata.total_compressed_size
    dictionary: list[tuple[str, int]] | None = None
    yielded = 0
    while offset < end:
        stream.seek(offset)
        header_stream = NumpyIO(stream.read(65_536))
        page_header = ThriftObject.from_buffer(header_stream, "PageHeader")
        header_size = header_stream.tell()
        content_offset = offset + header_size
        offset = content_offset + page_header.compressed_page_size
        stream.seek(content_offset)
        if page_header.type == parquet_thrift.PageType.DICTIONARY_PAGE:
            value_count = page_header.dictionary_page_header.num_values
            dictionary = []
            with zstd.ZstdDecompressor().stream_reader(
                LimitedReader(stream, page_header.compressed_page_size),
                closefd=False,
            ) as reader:
                for _ in range(value_count):
                    value_size = int.from_bytes(read_exact(reader, 4), "little")
                    dictionary.append(compact_cod_cif(read_exact(reader, value_size)))
            continue
        data_header = page_header.data_page_header
        if data_header is None:
            raise RuntimeError(f"unsupported COD Parquet page type: {page_header.type}")
        if data_header.encoding == parquet_thrift.Encoding.PLAIN:
            with zstd.ZstdDecompressor().stream_reader(
                LimitedReader(stream, page_header.compressed_page_size),
                closefd=False,
            ) as reader:
                definition_size = int.from_bytes(read_exact(reader, 4), "little")
                skip_exact(reader, definition_size)
                for _ in range(data_header.num_values):
                    value_size = int.from_bytes(read_exact(reader, 4), "little")
                    yield compact_cod_cif(read_exact(reader, value_size))
                    yielded += 1
        elif data_header.encoding in {
            parquet_thrift.Encoding.PLAIN_DICTIONARY,
            parquet_thrift.Encoding.RLE_DICTIONARY,
        }:
            if dictionary is None:
                raise RuntimeError("COD dictionary data page precedes its dictionary")
            _, _, indices = core.read_data_page(
                stream,
                fast_parquet.helper,
                page_header,
                metadata,
            )
            for index in indices:
                yield dictionary[int(index)]
                yielded += 1
        else:
            raise RuntimeError(f"unsupported COD CIF encoding: {data_header.encoding}")
    expected = row_group.num_rows
    if offset != end or yielded != expected:
        raise RuntimeError(
            f"COD row group {row_group_number}: yielded={yielded}, expected={expected}"
        )


def connect() -> sqlite3.Connection:
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(INDEX, timeout=120)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=NORMAL")
    connection.execute("PRAGMA temp_store=FILE")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS records (
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
            PRIMARY KEY (source, record_id)
        );
        CREATE TABLE IF NOT EXISTS source_state (
            source TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            record_count INTEGER NOT NULL,
            failed_count INTEGER NOT NULL,
            source_sha256 TEXT,
            details_json TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS records_formula_idx
            ON records(formula_key, source);
        CREATE INDEX IF NOT EXISTS records_formula_match_idx
            ON records(formula_key, source, record_id);
        CREATE INDEX IF NOT EXISTS records_anonymous_idx
            ON records(anonymous_formula, source);
        CREATE INDEX IF NOT EXISTS records_source_ordinal_idx
            ON records(source, ordinal);
        """
    )
    return connection


def source_done(connection: sqlite3.Connection, source: str, expected: int) -> bool:
    row = connection.execute(
        "SELECT status, record_count FROM source_state WHERE source = ?", (source,)
    ).fetchone()
    return bool(row and row[0] == "complete" and row[1] == expected)


def clear_source(connection: sqlite3.Connection, source: str) -> None:
    connection.execute("DELETE FROM records WHERE source = ?", (source,))
    connection.execute("DELETE FROM source_state WHERE source = ?", (source,))
    connection.commit()


def finish_source(
    connection: sqlite3.Connection,
    source: str,
    *,
    count: int,
    failed: int,
    digest: str | None,
    details: dict[str, Any],
) -> None:
    connection.execute(
        """INSERT OR REPLACE INTO source_state
           (source, status, record_count, failed_count, source_sha256, details_json)
           VALUES (?, 'complete', ?, ?, ?, ?)""",
        (source, count, failed, digest, json.dumps(details, sort_keys=True)),
    )
    connection.commit()


def insert_batch(connection: sqlite3.Connection, rows: list[tuple[Any, ...]]) -> None:
    connection.executemany(
        """INSERT OR REPLACE INTO records
           (source, record_id, split, ordinal, formula, formula_key,
            anonymous_formula, declared_spacegroup, payload_format, payload, locator)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    connection.commit()
    rows.clear()


def validate_asset(name: str) -> dict[str, Any]:
    spec = ASSETS[name]
    path = spec["path"]
    if not path.exists():
        raise FileNotFoundError(f"missing frozen source: {path}")
    result = {"path": str(path.relative_to(ROOT)), "boundary": spec["boundary"]}
    if path.is_file():
        size = path.stat().st_size
        result["size_bytes"] = size
        if (expected := spec.get("expected_size")) and size != expected:
            raise RuntimeError(f"{name}: size {size} != {expected}")
        digest = sha256_file(path)
        result["sha256"] = digest
        if (expected := spec.get("expected_sha256")) and digest != expected:
            raise RuntimeError(f"{name}: SHA-256 {digest} != {expected}")
    return result


def index_mp20(connection: sqlite3.Connection) -> None:
    source = "pxrdgen_mp20"
    expected_total = sum(item[2] for item in MP20_FILES.values())
    if source_done(connection, source, expected_total):
        print(f"{source}: already complete")
        return
    clear_source(connection, source)
    rows: list[tuple[Any, ...]] = []
    count = 0
    hashes: dict[str, str] = {}
    base = ROOT / ".runs" / "pxrd100" / "source"
    for split, (filename, expected_hash, expected_rows) in MP20_FILES.items():
        path = base / filename
        digest = sha256_file(path)
        if digest != expected_hash:
            raise RuntimeError(f"MP20 {split} digest mismatch")
        hashes[split] = digest
        split_count = 0
        with path.open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream):
                formula, key, anonymous = canonical_formula(row["pretty_formula"])
                cif = row["cif"].rstrip() + "\n"
                record_id = row["material_id"]
                rows.append(
                    (
                        source,
                        record_id,
                        split,
                        count,
                        formula,
                        key,
                        anonymous,
                        int(row["spacegroup.number"]),
                        "cif-zlib",
                        compress_text(cif),
                        f"{filename}:{split_count}",
                    )
                )
                count += 1
                split_count += 1
                if len(rows) >= 2000:
                    insert_batch(connection, rows)
        if split_count != expected_rows:
            raise RuntimeError(f"MP20 {split} rows {split_count} != {expected_rows}")
    if rows:
        insert_batch(connection, rows)
    finish_source(
        connection,
        source,
        count=count,
        failed=0,
        digest=None,
        details={"commit": "f857f598d6f6cca5dc1ea0582d228f12dcc2c2ea", "files": hashes},
    )
    print(f"{source}: indexed {count}")


def index_crystalyze(connection: sqlite3.Connection) -> None:
    source = "crystalyze_mp20"
    expected_total = sum(item[2] for item in CRYSTALYZE_SPLITS.values())
    if source_done(connection, source, expected_total):
        print(f"{source}: already complete")
        return
    asset = validate_asset("crystalyze_mp20")
    clear_source(connection, source)
    archive = ASSETS["crystalyze_mp20"]["path"]
    rows: list[tuple[Any, ...]] = []
    count = 0
    split_hashes: dict[str, str] = {}
    with zipfile.ZipFile(archive) as bundle:
        for split, (member, expected_hash, expected_rows) in CRYSTALYZE_SPLITS.items():
            with bundle.open(member) as raw:
                digest = sha256_stream(raw)
            if digest != expected_hash:
                raise RuntimeError(f"Crystalyze {split} digest mismatch: {digest}")
            split_hashes[split] = digest
            split_count = 0
            with bundle.open(member) as raw:
                stream = io.TextIOWrapper(raw, encoding="utf-8", newline="")
                for row in csv.DictReader(stream):
                    formula, key, anonymous = canonical_formula(row["pretty_formula"])
                    cif = row["cif"].rstrip() + "\n"
                    record_id = row.get("material_id") or f"{split}-{split_count:06d}"
                    rows.append(
                        (
                            source,
                            record_id,
                            split,
                            count,
                            formula,
                            key,
                            anonymous,
                            int(row["spacegroup.number"]),
                            "cif-zlib",
                            compress_text(cif),
                            f"{member}:{split_count}",
                        )
                    )
                    count += 1
                    split_count += 1
                    if len(rows) >= 1000:
                        insert_batch(connection, rows)
            if split_count != expected_rows:
                raise RuntimeError(f"Crystalyze {split} rows {split_count} != {expected_rows}")
    if rows:
        insert_batch(connection, rows)
    finish_source(
        connection,
        source,
        count=count,
        failed=0,
        digest=asset["sha256"],
        details={"archive": asset, "split_hashes": split_hashes},
    )
    print(f"{source}: indexed {count}")


def noma_pairs(path: Path) -> Iterator[tuple[str, str]]:
    pending: list[str] = []
    string_opcodes = {"SHORT_BINUNICODE", "BINUNICODE", "BINUNICODE8"}
    with gzip.open(path, "rb") as stream:
        for opcode, argument, _ in pickletools.genops(stream):
            if opcode.name in string_opcodes:
                pending.append(str(argument))
            elif opcode.name == "TUPLE2":
                if len(pending) != 2:
                    raise RuntimeError(f"NOMA tuple has {len(pending)} streamed string operands")
                yield pending[0], pending[1]
                pending.clear()
    if pending:
        raise RuntimeError("NOMA pickle ended with an incomplete record tuple")


def index_noma(connection: sqlite3.Connection) -> None:
    source = "decifer_noma"
    expected = int(ASSETS["noma"]["expected_raw_tuples"])
    expected_unique = int(ASSETS["noma"]["expected_unique_ids"])
    if source_done(connection, source, expected):
        print(f"{source}: already complete")
        return
    asset = validate_asset("noma")
    existing = connection.execute(
        "SELECT COUNT(*) FROM records WHERE source = ?", (source,)
    ).fetchone()[0]
    if existing == expected:
        finish_source(
            connection,
            source,
            count=existing,
            failed=0,
            digest=asset["sha256"],
            details={
                "archive": asset,
                "pickle_parser": "pickletools TUPLE2 opcode stream",
                "raw_tuple_count": existing,
                "unique_source_id_count": expected_unique,
                "records_above_paper_reported_count": (
                    existing - int(ASSETS["noma"]["paper_reported_records"])
                ),
                "recovered_after_completed_insert_audit": True,
            },
        )
        print(f"{source}: finalized {existing} already-indexed records")
        return
    clear_source(connection, source)
    rows: list[tuple[Any, ...]] = []
    count = 0
    raw_count = 0
    failed = 0
    started = time.monotonic()
    for raw_record_id, cif in noma_pairs(ASSETS["noma"]["path"]):
        ordinal = raw_count
        raw_count += 1
        try:
            formula, key, anonymous = formula_from_cif(cif)
        except Exception as exc:
            failed += 1
            if failed <= 10:
                print(f"NOMA formula failure {raw_record_id}: {exc}", file=sys.stderr)
            continue
        # The raw ordinal makes the physical index key unambiguous while the
        # original released source ID remains available as its locator.
        record_id = f"{raw_record_id}#raw-{ordinal:07d}"
        rows.append(
            (
                source,
                record_id,
                None,
                ordinal,
                formula,
                key,
                anonymous,
                sg_from_cif(cif),
                "cif-zlib",
                compress_text(cif),
                raw_record_id,
            )
        )
        count += 1
        if len(rows) >= 5000:
            insert_batch(connection, rows)
            if raw_count % 100_000 == 0:
                elapsed = time.monotonic() - started
                print(f"NOMA {raw_count:,}/{expected:,} ({raw_count / elapsed:,.0f} records/s)")
    if rows:
        insert_batch(connection, rows)
    if raw_count != expected or count + failed != expected:
        raise RuntimeError(
            f"NOMA raw={raw_count}, indexed={count}, failed={failed}, expected={expected}"
        )
    if failed:
        raise RuntimeError(f"NOMA has {failed} unindexable records; complete novelty requires zero")
    unique_ids = connection.execute(
        "SELECT COUNT(DISTINCT locator) FROM records WHERE source = ?", (source,)
    ).fetchone()[0]
    if unique_ids != expected_unique:
        raise RuntimeError(f"NOMA unique IDs {unique_ids} != {expected_unique}")
    finish_source(
        connection,
        source,
        count=count,
        failed=failed,
        digest=asset["sha256"],
        details={
            "archive": asset,
            "pickle_parser": "pickletools TUPLE2 opcode stream",
            "raw_tuple_count": raw_count,
            "unique_source_id_count": unique_ids,
            "records_above_paper_reported_count": (
                raw_count - int(ASSETS["noma"]["paper_reported_records"])
            ),
        },
    )
    print(f"{source}: indexed {count}")


def structure_from_jarvis(entry: dict[str, Any]) -> Structure:
    atoms = entry["atoms"]
    lattice = Lattice([[float(value) for value in row] for row in atoms["lattice_mat"]])
    coordinates = [[float(value) for value in row] for row in atoms["coords"]]
    cartesian = bool(atoms.get("cartesian", False))
    return Structure(
        lattice,
        atoms["elements"],
        coordinates,
        coords_are_cartesian=cartesian,
        to_unit_cell=True,
    )


def index_jarvis(connection: sqlite3.Connection) -> None:
    source = "jarvis_dft_2022"
    expected = int(ASSETS["jarvis_2022"]["expected_records"])
    if source_done(connection, source, expected):
        print(f"{source}: already complete")
        return
    asset = validate_asset("jarvis_2022")
    clear_source(connection, source)
    rows: list[tuple[Any, ...]] = []
    failed = 0
    count = 0
    archive = ASSETS["jarvis_2022"]["path"]
    # The official snapshot contains non-standard NaN tokens. Python's stdlib
    # decoder intentionally accepts them, while strict streaming JSON parsers do
    # not. The 209 MB member fits comfortably in the dedicated indexing runtime.
    with zipfile.ZipFile(archive) as bundle, bundle.open("jdft_3d-12-12-2022.json") as raw:
        entries = json.load(io.TextIOWrapper(raw, encoding="utf-8"))
        for ordinal, entry in enumerate(entries):
            try:
                structure = structure_from_jarvis(entry)
                formula, key, anonymous = canonical_formula(structure.composition.as_dict())
                payload = zlib.compress(
                    json.dumps(structure.as_dict(), separators=(",", ":")).encode(), level=6
                )
            except Exception as exc:
                failed += 1
                if failed <= 10:
                    print(f"JARVIS failure {entry.get('jid')}: {exc}", file=sys.stderr)
                continue
            rows.append(
                (
                    source,
                    str(entry["jid"]),
                    None,
                    ordinal,
                    formula,
                    key,
                    anonymous,
                    None,
                    "pymatgen-json-zlib",
                    payload,
                    f"json-ordinal:{ordinal}",
                )
            )
            count += 1
            if len(rows) >= 1000:
                insert_batch(connection, rows)
    if rows:
        insert_batch(connection, rows)
    if count + failed != expected or failed:
        raise RuntimeError(f"JARVIS indexed={count}, failed={failed}, expected={expected}")
    finish_source(
        connection,
        source,
        count=count,
        failed=failed,
        digest=asset["sha256"],
        details={"archive": asset, "member": "jdft_3d-12-12-2022.json"},
    )
    print(f"{source}: indexed {count}")


def structure_from_diffractgpt(output: str) -> Structure:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    lengths = [float(value) for value in lines[0].split()]
    angles = [float(value) for value in lines[1].split()]
    if len(lengths) != 3 or len(angles) != 3:
        raise ValueError("invalid DiffractGPT lattice header")
    species: list[str] = []
    coordinates: list[list[float]] = []
    for line in lines[2:]:
        fields = line.split()
        if len(fields) != 4:
            raise ValueError("invalid DiffractGPT site line")
        species.append(fields[0])
        coordinates.append([float(value) for value in fields[1:]])
    lattice = Lattice.from_parameters(*lengths, *angles)
    return Structure(lattice, species, coordinates, to_unit_cell=True)


def index_diffractgpt(connection: sqlite3.Connection) -> None:
    source = "diffractgpt_released"
    expected = sum(
        int(ASSETS[name]["expected_records"]) for name in ("diffractgpt_train", "diffractgpt_test")
    )
    if source_done(connection, source, expected):
        print(f"{source}: already complete")
        return
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise RuntimeError("index_diffractgpt requires pyarrow; run with --with pyarrow") from exc
    clear_source(connection, source)
    rows: list[tuple[Any, ...]] = []
    count = 0
    failed = 0
    assets: dict[str, Any] = {}
    for split in ("train", "test"):
        name = f"diffractgpt_{split}"
        assets[name] = validate_asset(name)
        table = pq.read_table(ASSETS[name]["path"], columns=["input", "id", "output"])
        for split_ordinal, item in enumerate(table.to_pylist()):
            try:
                match = DIFFRACTGPT_FORMULA.search(item["input"])
                if match is None:
                    raise ValueError("formula missing from prompt")
                formula, key, anonymous = canonical_formula(match.group(1).strip())
                structure = structure_from_diffractgpt(item["output"])
                payload = zlib.compress(
                    json.dumps(structure.as_dict(), separators=(",", ":")).encode(), level=6
                )
            except Exception as exc:
                failed += 1
                if failed <= 10:
                    print(f"DiffractGPT failure {item.get('id')}: {exc}", file=sys.stderr)
                continue
            rows.append(
                (
                    source,
                    f"{split}:{split_ordinal}:{item['id']}",
                    split,
                    count,
                    formula,
                    key,
                    anonymous,
                    None,
                    "pymatgen-json-zlib",
                    payload,
                    f"released-jid:{item['id']}",
                )
            )
            count += 1
            if len(rows) >= 1000:
                insert_batch(connection, rows)
    if rows:
        insert_batch(connection, rows)
    # Four training examples reuse a JID. Split ordinal is part of the exposure
    # identity so every released example remains in the conservative boundary.
    if count + failed != expected or failed:
        raise RuntimeError(f"DiffractGPT indexed={count}, failed={failed}, expected={expected}")
    finish_source(
        connection,
        source,
        count=count,
        failed=failed,
        digest=None,
        details={
            "assets": assets,
            "released_example_count": expected,
            "unique_raw_jid_count": 75_993,
            "duplicate_jid_excess_retained_by_split_ordinal_identity": 4,
        },
    )
    print(f"{source}: indexed {count}")


def index_dara(connection: sqlite3.Connection) -> None:
    source = "dara_cod_2024"
    expected = int(ASSETS["dara_cod_index"]["expected_unique_records"])
    if source_done(connection, source, expected):
        print(f"{source}: already complete")
        return
    asset = validate_asset("dara_cod_index")
    clear_source(connection, source)
    with gzip.open(ASSETS["dara_cod_index"]["path"], "rt", encoding="utf-8") as stream:
        data = json.load(stream)
    by_id: dict[str, tuple[str, int | None]] = {}
    for values in data.values():
        for formula, cod_id, spacegroup, _ in values:
            by_id.setdefault(str(cod_id), (str(formula), int(spacegroup) if spacegroup else None))
    rows: list[tuple[Any, ...]] = []
    failed = 0
    for ordinal, (record_id, (raw_formula, spacegroup)) in enumerate(sorted(by_id.items())):
        try:
            formula, key, anonymous = canonical_formula(raw_formula)
        except (TypeError, ValueError):
            failed += 1
            continue
        rows.append(
            (
                source,
                record_id,
                None,
                ordinal,
                formula,
                key,
                anonymous,
                spacegroup,
                "cod-id-only",
                None,
                record_id,
            )
        )
        if len(rows) >= 5000:
            insert_batch(connection, rows)
    if rows:
        insert_batch(connection, rows)
    if len(by_id) != expected or failed:
        raise RuntimeError(f"DARA unique={len(by_id)}, failed={failed}, expected={expected}")
    finish_source(
        connection,
        source,
        count=len(by_id),
        failed=failed,
        digest=asset["sha256"],
        details={"archive": asset, "chemical_system_buckets": len(data)},
    )
    print(f"{source}: indexed {len(by_id)}")


def mp_api_get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    api_key = os.environ.get("MP_API_KEY")
    if not api_key:
        raise RuntimeError("MP_API_KEY is required to freeze the current MP snapshot")
    last_error: Exception | None = None
    for attempt in range(6):
        try:
            response = requests.get(
                f"{MP_API_ROOT}{path}",
                params=params,
                headers={"X-API-KEY": api_key},
                timeout=180,
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            time.sleep(1.0 + attempt)
    raise RuntimeError(f"Materials Project API request failed: {last_error}")


def index_materials_project(connection: sqlite3.Connection) -> None:
    source = "materials_project_2026_04_13"
    if source_done(connection, source, MP_EXPECTED_RECORDS):
        print(f"{source}: already complete")
        return
    heartbeat = mp_api_get("/heartbeat")
    if heartbeat.get("db_version") != MP_EXPECTED_DB_VERSION:
        raise RuntimeError(
            f"Materials Project DB changed: {heartbeat.get('db_version')} != "
            f"{MP_EXPECTED_DB_VERSION}; create a new benchmark version"
        )
    probe = mp_api_get(
        "/materials/summary/",
        {
            "_limit": 1,
            "_fields": "material_id,formula_pretty,structure,symmetry",
        },
    )
    total = int(probe["meta"]["total_doc"])
    if total != MP_EXPECTED_RECORDS:
        raise RuntimeError(f"Materials Project row count {total} != {MP_EXPECTED_RECORDS}")
    clear_source(connection, source)
    snapshot = SOURCES / f"materials-project-{MP_EXPECTED_DB_VERSION}.jsonl.gz"
    temporary = snapshot.with_suffix(snapshot.suffix + ".partial")
    rows: list[tuple[Any, ...]] = []
    count = 0
    failed = 0
    fields = "material_id,formula_pretty,structure,symmetry"
    with gzip.open(temporary, "wt", encoding="utf-8", compresslevel=6) as archive:
        for skip in range(0, total, 1000):
            payload = mp_api_get(
                "/materials/summary/",
                {"_limit": 1000, "_skip": skip, "_fields": fields},
            )
            documents = payload["data"]
            if not documents:
                raise RuntimeError(f"Materials Project returned no rows at skip={skip}")
            for document in documents:
                archive.write(json.dumps(document, separators=(",", ":"), sort_keys=True) + "\n")
                try:
                    structure = Structure.from_dict(document["structure"])
                    formula, key, anonymous = canonical_formula(structure.composition.as_dict())
                    structure_payload = zlib.compress(
                        json.dumps(structure.as_dict(), separators=(",", ":")).encode(), level=6
                    )
                    symmetry = document.get("symmetry") or {}
                    spacegroup = symmetry.get("number")
                except Exception as exc:
                    failed += 1
                    if failed <= 10:
                        print(
                            f"Materials Project failure {document.get('material_id')}: {exc}",
                            file=sys.stderr,
                        )
                    continue
                rows.append(
                    (
                        source,
                        str(document["material_id"]),
                        None,
                        count,
                        formula,
                        key,
                        anonymous,
                        int(spacegroup) if spacegroup else None,
                        "pymatgen-json-zlib",
                        structure_payload,
                        f"api-ordinal:{count}",
                    )
                )
                count += 1
            if len(rows) >= 1000:
                insert_batch(connection, rows)
            print(f"Materials Project {min(skip + len(documents), total):,}/{total:,}")
    temporary.replace(snapshot)
    if rows:
        insert_batch(connection, rows)
    if count + failed != total or failed:
        raise RuntimeError(f"Materials Project indexed={count}, failed={failed}, expected={total}")
    digest = sha256_file(snapshot)
    finish_source(
        connection,
        source,
        count=count,
        failed=failed,
        digest=digest,
        details={
            "snapshot_path": str(snapshot.relative_to(ROOT)),
            "snapshot_sha256": digest,
            "database_version": heartbeat["db_version"],
            "api_version": heartbeat["version"],
            "api_pymatgen_version": heartbeat["pymatgen"],
            "api_key_committed": False,
        },
    )
    print(f"{source}: indexed {count}")


def index_cod(connection: sqlite3.Connection) -> None:
    source = "cod_current"
    expected_parquet = int(ASSETS["cod_current"]["expected_records"])
    if not COD_INVENTORY_REPORT.is_file():
        raise FileNotFoundError(
            f"missing COD live-delta report: {COD_INVENTORY_REPORT}; run freeze_cod_delta.py"
        )
    inventory_report = json.loads(COD_INVENTORY_REPORT.read_text(encoding="utf-8"))
    live_only_ids = [int(value) for value in inventory_report["live_only_ids"]]
    changed_existing_ids = {int(value) for value in inventory_report["changed_existing_ids"]}
    snapshot_missing_cif_ids = {
        int(value) for value in inventory_report.get("snapshot_missing_cif_ids", [])
    }
    overridden_parquet_ids = changed_existing_ids | snapshot_missing_cif_ids
    delta_ids = [int(value) for value in inventory_report["delta_ids"]]
    expected = expected_parquet + len(live_only_ids)
    if source_done(connection, source, expected):
        print(f"{source}: already complete ({expected})")
        return
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise RuntimeError("index_cod requires pyarrow") from exc
    asset = validate_asset("cod_current")
    parquet = pq.ParquetFile(ASSETS["cod_current"]["path"])
    fast_parquet = ParquetFile(str(ASSETS["cod_current"]["path"]))
    if parquet.metadata.num_rows != expected_parquet:
        raise RuntimeError(f"COD parquet rows {parquet.metadata.num_rows} != {expected_parquet}")
    if len(fast_parquet.row_groups) != parquet.metadata.num_row_groups:
        raise RuntimeError("COD Parquet readers disagree on row-group count")
    required_columns = {"file", "formula", "sgNumber", "cif_text"}
    missing_columns = required_columns - set(parquet.schema.names)
    if missing_columns:
        raise RuntimeError(f"COD parquet is missing columns: {sorted(missing_columns)}")
    clear_source(connection, source)
    rows: list[tuple[Any, ...]] = []
    failed = 0
    count = 0
    nonstructural_ids: list[int] = []
    stripped_embedded_bytes = 0
    started = time.monotonic()
    parquet_seen = 0
    columns = ["file", "formula", "sgNumber"]
    with ASSETS["cod_current"]["path"].open("rb") as parquet_stream:
        for row_group_number in range(parquet.metadata.num_row_groups):
            items = parquet.read_row_group(row_group_number, columns=columns).to_pylist()
            cifs = iter_cod_row_group_cifs(parquet_stream, fast_parquet, row_group_number)
            for item, (compact_cif, stripped_bytes) in zip(items, cifs, strict=True):
                parquet_seen += 1
                stripped_embedded_bytes += stripped_bytes
                ordinal = count + failed
                record_id = str(item["file"])
                if int(record_id) in overridden_parquet_ids:
                    continue
                cif = compact_cif
                payload_format = "cif-zlib"
                try:
                    try:
                        if not isinstance(item["formula"], str):
                            raise ValueError("missing metadata formula")
                        raw_formula = item["formula"].strip().strip("-").strip()
                        formula, key, anonymous = canonical_formula(raw_formula)
                    except (TypeError, ValueError):
                        formula, key, anonymous = formula_from_cif(cif)
                except Exception as exc:
                    # A small number of active COD records are bibliographic or otherwise
                    # malformed deposits with neither a usable formula nor a parseable
                    # periodic structure.  Retain every such raw record in the frozen
                    # boundary, but keep it out of formula/structure candidate lookups by
                    # assigning a record-specific sentinel.  This is stricter and more
                    # auditable than silently dropping it or inventing a composition.
                    formula = f"UNRESOLVED-COD-{record_id}"
                    key = f"__unresolved_cod_formula__:{record_id}"
                    anonymous = f"__unresolved_cod_topology__:{record_id}"
                    payload_format = "unparseable-cif-zlib"
                    nonstructural_ids.append(int(record_id))
                    if len(nonstructural_ids) <= 10:
                        print(f"COD nonstructural {record_id}: {exc}", file=sys.stderr)
                rows.append(
                    (
                        source,
                        record_id,
                        None,
                        ordinal,
                        formula,
                        key,
                        anonymous,
                        int(item["sgNumber"]) if item["sgNumber"] else sg_from_cif(cif),
                        payload_format,
                        compress_text(compact_cif),
                        f"parquet-row:{parquet_seen - 1}",
                    )
                )
                count += 1
                if len(rows) >= 5000:
                    insert_batch(connection, rows)
                if parquet_seen % 100_000 == 0:
                    elapsed = time.monotonic() - started
                    print(
                        f"COD {parquet_seen:,}/{expected_parquet:,} "
                        f"({parquet_seen / elapsed:,.0f} rows/s)"
                    )
    for record_number in delta_ids:
        record_id = str(record_number)
        relative = Path(record_id[0]) / record_id[1:3] / record_id[3:5] / f"{record_id}.cif"
        path = COD_DELTA / relative
        ordinal = count + failed
        cif = path.read_text(encoding="utf-8", errors="replace")
        if not cif.strip():
            raise RuntimeError(f"COD live-delta {record_id} has no archived CIF text")
        compact_cif = COD_EMBEDDED_FILE.sub("", cif).rstrip() + "\n"
        stripped_embedded_bytes += len(cif.encode()) - len(compact_cif.encode())
        payload_format = "cif-zlib"
        try:
            formula, key, anonymous = formula_from_cif(cif)
        except Exception as exc:
            formula = f"UNRESOLVED-COD-{record_id}"
            key = f"__unresolved_cod_formula__:{record_id}"
            anonymous = f"__unresolved_cod_topology__:{record_id}"
            payload_format = "unparseable-cif-zlib"
            nonstructural_ids.append(int(record_id))
            if len(nonstructural_ids) <= 10:
                print(f"COD live-delta nonstructural {record_id}: {exc}", file=sys.stderr)
        rows.append(
            (
                source,
                record_id,
                "live-delta-2026-07-19",
                ordinal,
                formula,
                key,
                anonymous,
                sg_from_cif(cif),
                payload_format,
                compress_text(compact_cif),
                f"official-rsync:{relative.as_posix()}",
            )
        )
        count += 1
        if len(rows) >= 5000:
            insert_batch(connection, rows)
    if rows:
        insert_batch(connection, rows)
    if count != expected or failed:
        raise RuntimeError(f"COD indexed={count}, failed={failed}, expected={expected}")
    boundary_components = {
        "parquet_sha256": asset["sha256"],
        "official_inventory_sha256": inventory_report["inventory_sha256"],
        "live_delta_merkle_sha256": inventory_report["delta_merkle_sha256"],
    }
    boundary_digest = hashlib.sha256(
        json.dumps(boundary_components, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    finish_source(
        connection,
        source,
        count=count,
        failed=failed,
        digest=boundary_digest,
        details={
            "archive": asset,
            "boundary_components": boundary_components,
            "compressed_snapshot_date": "2026-07-06",
            "official_delta_freeze_date": "2026-07-19",
            "snapshot_active_record_count": expected_parquet,
            "frozen_union_record_count": expected,
            "source_cif_download_count": 533_862,
            "on_hold_entries_excluded_by_snapshot_publisher": 411,
            "huggingface_repository": "LMucko/crystallography-open-database",
            "huggingface_commit": "7d0b1c92860e8092ac469c6d3780f9666c305692",
            "official_inventory_report": str(COD_INVENTORY_REPORT.relative_to(ROOT)),
            "official_inventory_report_sha256": sha256_file(COD_INVENTORY_REPORT),
            "official_rsync_cif_count": inventory_report["official_cif_count"],
            "live_only_count": len(live_only_ids),
            "changed_existing_count": len(changed_existing_ids),
            "snapshot_missing_cif_count": len(snapshot_missing_cif_ids),
            "official_delta_record_count": len(delta_ids),
            "parquet_only_count": inventory_report["parquet_only_count"],
            "nonstructural_record_count": len(nonstructural_ids),
            "nonstructural_record_ids": sorted(nonstructural_ids),
            "nonstructural_policy": (
                "raw active COD record retained with record-specific sentinel keys; "
                "not treated as a formula-bearing or parseable periodic structure"
            ),
            "embedded_shelx_bytes_removed_from_index_payloads": stripped_embedded_bytes,
            "raw_cif_text_covered_by_archive_hash": True,
        },
    )
    print(f"{source}: indexed {count} records in the complete frozen COD union")


INDEXERS = {
    "mp20": index_mp20,
    "crystalyze": index_crystalyze,
    "noma": index_noma,
    "jarvis": index_jarvis,
    "diffractgpt": index_diffractgpt,
    "dara": index_dara,
    "materials-project": index_materials_project,
    "cod": index_cod,
}


def write_lock(connection: sqlite3.Connection) -> dict[str, Any]:
    connection.commit()
    connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    states = connection.execute(
        "SELECT source, status, record_count, failed_count, source_sha256, details_json "
        "FROM source_state ORDER BY source"
    ).fetchall()
    lock = {
        "schema_version": "1.0.0",
        "freeze_date": FREEZE_DATE,
        "framework_exposure_boundaries": FRAMEWORK_BOUNDARIES,
        "index": {
            "path": str(INDEX.relative_to(ROOT)),
            "sha256": sha256_file(INDEX) if INDEX.is_file() else None,
        },
        "sources": {
            source: {
                "status": status,
                "record_count": count,
                "failed_count": failed,
                "sha256": digest,
                "details": json.loads(details),
            }
            for source, status, count, failed, digest, details in states
        },
        "api_key_committed": False,
    }
    temporary = LOCK.with_suffix(".partial")
    temporary.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(LOCK)
    return lock


def verify_frozen_files(connection: sqlite3.Connection) -> None:
    """Re-hash every frozen source artifact and validate archive metadata."""
    for name in (
        "crystalyze_mp20",
        "noma",
        "jarvis_2022",
        "diffractgpt_train",
        "diffractgpt_test",
        "dara_cod_index",
    ):
        validate_asset(name)

    mp20_root = ROOT / ".runs" / "pxrd100" / "source"
    for split, (filename, expected_hash, _) in MP20_FILES.items():
        digest = sha256_file(mp20_root / filename)
        if digest != expected_hash:
            raise RuntimeError(f"MP20 {split} file hash changed: {digest}")

    mp_state = connection.execute(
        "SELECT source_sha256, details_json FROM source_state "
        "WHERE source = 'materials_project_2026_04_13'"
    ).fetchone()
    if mp_state is None:
        raise RuntimeError("Materials Project source state is missing")
    mp_details = json.loads(mp_state[1])
    mp_snapshot = ROOT / Path(mp_details["snapshot_path"])
    mp_digest = sha256_file(mp_snapshot)
    if mp_digest != mp_state[0] or mp_digest != mp_details["snapshot_sha256"]:
        raise RuntimeError("Materials Project snapshot hash changed")

    cod_state = connection.execute(
        "SELECT record_count, failed_count, source_sha256, details_json "
        "FROM source_state WHERE source = 'cod_current'"
    ).fetchone()
    if cod_state is None:
        raise RuntimeError("COD source state is missing")
    cod_details = json.loads(cod_state[3])
    cod_asset = validate_asset("cod_current")
    if sha256_file(COD_INVENTORY_REPORT) != cod_details["official_inventory_report_sha256"]:
        raise RuntimeError("COD official inventory report hash changed")
    inventory_report = json.loads(COD_INVENTORY_REPORT.read_text(encoding="utf-8"))
    if sha256_file(COD_INVENTORY) != inventory_report["inventory_sha256"]:
        raise RuntimeError("COD official inventory hash changed")
    live_only_ids = [int(value) for value in inventory_report["live_only_ids"]]
    delta_ids = [int(value) for value in inventory_report["delta_ids"]]
    delta_digest = hashlib.sha256()
    for record_number in delta_ids:
        record_id = str(record_number)
        relative = Path(record_id[0]) / record_id[1:3] / record_id[3:5] / f"{record_id}.cif"
        delta_digest.update(
            relative.as_posix().encode()
            + b"\0"
            + sha256_file(COD_DELTA / relative).encode()
            + b"\n"
        )
    if delta_digest.hexdigest() != inventory_report["delta_merkle_sha256"]:
        raise RuntimeError("COD official live-delta digest changed")
    boundary_components = {
        "parquet_sha256": cod_asset["sha256"],
        "official_inventory_sha256": inventory_report["inventory_sha256"],
        "live_delta_merkle_sha256": inventory_report["delta_merkle_sha256"],
    }
    boundary_digest = hashlib.sha256(
        json.dumps(boundary_components, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if cod_state[2] != boundary_digest:
        raise RuntimeError("COD frozen-union digest differs from source state")
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise RuntimeError("COD verification requires pyarrow") from exc
    parquet = pq.ParquetFile(ASSETS["cod_current"]["path"])
    expected_parquet_records = int(ASSETS["cod_current"]["expected_records"])
    expected_cod_records = expected_parquet_records + len(live_only_ids)
    if parquet.metadata.num_rows != expected_parquet_records:
        raise RuntimeError("COD parquet metadata row count changed")
    if cod_state[0] != expected_cod_records or cod_state[1] != 0:
        raise RuntimeError("COD source state does not cover every active snapshot record")
    if cod_details["snapshot_active_record_count"] != expected_parquet_records:
        raise RuntimeError("COD source detail count changed")
    if cod_details["frozen_union_record_count"] != expected_cod_records:
        raise RuntimeError("COD source detail count changed")

    missing_dara = connection.execute(
        "SELECT COUNT(*) FROM records AS d LEFT JOIN records AS c "
        "ON c.source = 'cod_current' AND c.record_id = d.record_id "
        "WHERE d.source = 'dara_cod_2024' AND c.record_id IS NULL"
    ).fetchone()[0]
    if missing_dara:
        raise RuntimeError(
            f"{missing_dara} exact DARA public-COD IDs lack a parseable frozen COD structure"
        )


def audit(connection: sqlite3.Connection) -> None:
    expected = {
        "pxrdgen_mp20": 45_229,
        "crystalyze_mp20": 45_052,
        "decifer_noma": 2_285_914,
        "jarvis_dft_2022": 75_993,
        "diffractgpt_released": 75_997,
        "dara_cod_2024": 62_098,
        "materials_project_2026_04_13": MP_EXPECTED_RECORDS,
    }
    errors: list[str] = []
    for source, count in expected.items():
        state = connection.execute(
            "SELECT status, record_count, failed_count FROM source_state WHERE source = ?",
            (source,),
        ).fetchone()
        if state != ("complete", count, 0):
            errors.append(f"{source}: expected complete/{count}/0, found {state}")
        actual = connection.execute(
            "SELECT COUNT(*) FROM records WHERE source = ?", (source,)
        ).fetchone()[0]
        if actual != count:
            errors.append(f"{source}: table rows {actual} != {count}")
    cod = connection.execute(
        "SELECT status, record_count, failed_count FROM source_state WHERE source = 'cod_current'"
    ).fetchone()
    if cod is None or cod[0] != "complete" or cod[1] < COD_MIN_PARSEABLE_RECORDS:
        errors.append(f"cod_current: incomplete or unexpectedly small: {cod}")
    elif (
        connection.execute("SELECT COUNT(*) FROM records WHERE source = 'cod_current'").fetchone()[
            0
        ]
        != cod[1]
    ):
        errors.append("cod_current: table row count differs from source state")
    duplicates = connection.execute(
        "SELECT source, COUNT(*) - COUNT(DISTINCT record_id) FROM records "
        "GROUP BY source HAVING COUNT(*) != COUNT(DISTINCT record_id)"
    ).fetchall()
    if duplicates:
        errors.append(f"duplicate source IDs: {duplicates}")
    if errors:
        raise RuntimeError("exposure-index audit failed:\n- " + "\n- ".join(errors))
    verify_frozen_files(connection)
    lock = write_lock(connection)
    print(
        "OK: complete exposure index; "
        + ", ".join(f"{name}={entry['record_count']:,}" for name, entry in lock["sources"].items())
    )


def stats(connection: sqlite3.Connection) -> None:
    for row in connection.execute(
        "SELECT source, status, record_count, failed_count FROM source_state ORDER BY source"
    ):
        print("\t".join(str(value) for value in row))
    print(f"database_bytes\t{INDEX.stat().st_size if INDEX.exists() else 0}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "audit", "stats"))
    parser.add_argument(
        "--source",
        action="append",
        choices=tuple(INDEXERS),
        help="source to build; repeat as needed (default: all)",
    )
    parser.add_argument("--replace-source", action="store_true")
    args = parser.parse_args()
    connection = connect()
    try:
        if args.command == "build":
            selected = args.source or list(INDEXERS)
            for name in selected:
                if args.replace_source:
                    source_name = {
                        "mp20": "pxrdgen_mp20",
                        "crystalyze": "crystalyze_mp20",
                        "noma": "decifer_noma",
                        "jarvis": "jarvis_dft_2022",
                        "diffractgpt": "diffractgpt_released",
                        "dara": "dara_cod_2024",
                        "materials-project": "materials_project_2026_04_13",
                        "cod": "cod_current",
                    }[name]
                    clear_source(connection, source_name)
                INDEXERS[name](connection)
            write_lock(connection)
        elif args.command == "audit":
            audit(connection)
        else:
            stats(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
