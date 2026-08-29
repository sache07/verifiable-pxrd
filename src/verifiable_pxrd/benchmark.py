from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .util import load_json, sha256_file


@dataclass(frozen=True, slots=True)
class Problem:
    problem_id: str
    formula: str
    pattern: Path
    reference: Path
    record: Path
    wavelength: float = 1.5406
    radiation: str = "Cu Kalpha1"


def _safe_child(root: Path, relative: str) -> Path:
    value = PurePosixPath(relative)
    if value.is_absolute() or ".." in value.parts:
        raise ValueError(f"unsafe relative path: {relative}")
    return root / value


def load_problem_collection(manifest_path: Path) -> list[Problem]:
    """Load either a self-contained problem collection or a lightweight panel."""

    manifest_path = manifest_path.resolve()
    root = manifest_path.parent
    payload = load_json(manifest_path)
    records = payload.get("problems")
    if records is None:
        records = payload.get("cases")
        if not isinstance(records, list):
            raise ValueError(f"{manifest_path} does not contain a problems or cases list")
        data_root_value = str(payload.get("path_root", "."))
        if Path(data_root_value).is_absolute():
            raise ValueError("panel path_root must be relative")
        data_root = (root / data_root_value).resolve()
        problems = []
        for item in records:
            problem_id = str(item.get("problem_id", item.get("case_id")))
            if not problem_id or problem_id == "None":
                raise ValueError(f"panel entry has no problem_id or case_id: {item}")
            pattern = _safe_child(data_root, str(item["pattern_path"])).resolve()
            reference = _safe_child(data_root, str(item["reference_path"])).resolve()
            for candidate in (pattern, reference):
                if not candidate.is_file():
                    raise FileNotFoundError(candidate)
            problems.append(
                Problem(
                    problem_id=problem_id,
                    formula=str(item["formula"]),
                    pattern=pattern,
                    reference=reference,
                    record=manifest_path,
                    wavelength=float(item.get("wavelength", 1.5406)),
                    radiation=str(item.get("radiation", "Cu Kalpha1")),
                )
            )
        if len({item.problem_id for item in problems}) != len(problems):
            raise ValueError(f"duplicate problem identifiers in {manifest_path}")
        return problems
    if not isinstance(records, list):
        raise ValueError(f"{manifest_path} problems field is not a list")
    problems: list[Problem] = []
    for item in records:
        problem_id = str(item["problem_id"])
        problem_root = root / "problems" / problem_id
        record_path = problem_root / "problem.json"
        record = load_json(record_path) if record_path.is_file() else item
        inputs = record["problem_input"]["files"]
        pattern_item = next(
            entry for entry in inputs if entry["role"] == "powder_diffraction_pattern"
        )
        pattern = _safe_child(problem_root, str(pattern_item["path"]))
        reference = _safe_child(problem_root, str(record["solution"]["path"]))
        formula = str(record["metadata"]["formula"])
        for path, expected in (
            (pattern, pattern_item.get("sha256")),
            (reference, record["solution"].get("sha256")),
        ):
            if not path.is_file():
                raise FileNotFoundError(path)
            if expected and sha256_file(path) != expected:
                raise RuntimeError(f"hash mismatch: {path}")
        problems.append(
            Problem(
                problem_id=problem_id,
                formula=formula,
                pattern=pattern,
                reference=reference,
                record=record_path,
            )
        )
    if len({item.problem_id for item in problems}) != len(problems):
        raise ValueError(f"duplicate problem identifiers in {manifest_path}")
    return problems


def validate_corpus(corpus: Path) -> dict[str, Any]:
    """Validate one pXRD-100/OOD corpus and its fixedparams-v1 patterns."""

    source = load_json(corpus / "manifest.json")
    target_root = corpus / "targets/fixedparams-v1"
    target = load_json(target_root / "manifest.json")
    source_by_id = {str(item["case_id"]): item for item in source["cases"]}
    failures: list[str] = []
    for item in target["cases"]:
        case_id = str(item["case_id"])
        record = source_by_id.get(case_id)
        if record is None:
            failures.append(f"{case_id}: absent from source manifest")
            continue
        structure = _safe_child(corpus, str(record["path"]))
        pattern = _safe_child(target_root, str(item["pattern_path"]))
        checks = (
            (structure, str(record["sha256"])),
            (pattern, str(item["pattern_sha256"])),
        )
        for path, expected in checks:
            if not path.is_file():
                failures.append(f"{case_id}: missing {path}")
            elif sha256_file(path) != expected:
                failures.append(f"{case_id}: hash mismatch {path}")
    return {
        "dataset_id": source.get("dataset_id"),
        "source_cases": len(source_by_id),
        "pattern_cases": len(target["cases"]),
        "valid": not failures and len(source_by_id) == len(target["cases"]),
        "failures": failures,
    }
