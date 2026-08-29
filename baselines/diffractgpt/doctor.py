"""Base-model-free readiness check for the DiffractGPT benchmark package.

This verifies the immutable paper adapter, tokenizer, source checkout, and all
100 prepared prompts/targets. It deliberately does not download or load the
4.13 GB base model; that smoke test belongs in the pinned Modal image.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
import subprocess
import sys
from collections import Counter
from itertools import pairwise
from pathlib import Path
from typing import Any

try:
    import sentencepiece as spm
except ImportError as exc:  # pragma: no cover - actionable CLI failure
    raise SystemExit("sentencepiece is required; see baselines/diffractgpt/README.md") from exc

from verifiable_pxrd.baselines.targets import framework_target_root

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
LOCK_PATH = Path(__file__).with_name("artifacts.lock.json")
INFERENCE_PATH = Path(__file__).with_name("baseline.json")
SOURCE_MANIFEST = REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100" / "manifest.json"
TARGET_ROOT = framework_target_root(REPOSITORY_ROOT, "diffractgpt", SOURCE_MANIFEST.parent)
TARGET_MANIFEST = TARGET_ROOT / "manifest.json"
PARAMETERS_PATH = TARGET_ROOT / "parameters.json"
INPUTS_PATH = TARGET_ROOT / "inputs.csv"

EXPECTED_CASES = 100
EXPECTED_PANELS = {"challenge": 30, "polymorph": 40, "representative": 30}
VECTOR_LINE = re.compile(r"\d+\.\d{3}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_source(lock: dict[str, Any]) -> None:
    pin = lock["source_checkout"]
    checkout = ROOT / pin["directory"]
    require((checkout / ".git").is_dir(), f"missing source checkout: {checkout}")
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=checkout,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=checkout,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(revision == pin["commit"], f"source revision {revision} != {pin['commit']}")
    require(not dirty, "pinned AtomGPT source checkout has local changes")
    require(pin["license_status"] == "licensed", "source license status is not cleared")
    require((checkout / pin["license_file"]).is_file(), "source license file is missing")
    reference = pin["later_binning_reference"]
    require(
        reference["exact_paper_preprocessing_match"] is False,
        "later helper must not be represented as an exact paper transform",
    )


def verify_checkpoint(lock: dict[str, Any]) -> Path:
    checkpoint = lock["checkpoint"]
    destination = ROOT / checkpoint["destination"]
    for artifact in checkpoint["artifacts"]:
        path = destination / artifact["path"]
        require(path.is_file(), f"missing checkpoint artifact: {path}")
        require(
            path.stat().st_size == artifact["size_bytes"],
            f"checkpoint size mismatch: {artifact['path']}",
        )
        require(
            sha256_file(path) == artifact["sha256"],
            f"checkpoint digest mismatch: {artifact['path']}",
        )
    adapter_config = read_json(destination / "adapter_config.json")
    require(adapter_config["peft_type"] == "LORA", "checkpoint is not a LoRA adapter")
    require(adapter_config["task_type"] == "CAUSAL_LM", "unexpected adapter task")
    require(
        adapter_config["base_model_name_or_path"] == lock["base_model"]["repository"],
        "adapter/base repository mismatch",
    )
    return destination


def verify_safetensors(path: Path) -> int:
    with path.open("rb") as stream:
        raw_length = stream.read(8)
        require(len(raw_length) == 8, "truncated safetensors length")
        header_length = struct.unpack("<Q", raw_length)[0]
        require(0 < header_length < 16 * 1024 * 1024, "invalid safetensors header length")
        raw_header = stream.read(header_length)
    header = json.loads(raw_header.decode("utf-8"))
    tensors = {name: value for name, value in header.items() if name != "__metadata__"}
    require(tensors, "adapter has no tensors")
    data_bytes = path.stat().st_size - 8 - header_length
    intervals: list[tuple[int, int, str]] = []
    for name, tensor in tensors.items():
        require(set(tensor) >= {"dtype", "shape", "data_offsets"}, f"bad tensor: {name}")
        start, stop = tensor["data_offsets"]
        require(0 <= start <= stop <= data_bytes, f"bad offsets: {name}")
        require(all(int(size) >= 0 for size in tensor["shape"]), f"bad shape: {name}")
        intervals.append((start, stop, name))
    intervals.sort()
    require(intervals[0][0] == 0, "safetensors data does not start at offset zero")
    require(intervals[-1][1] == data_bytes, "safetensors data does not reach EOF")
    for previous, current in pairwise(intervals):
        require(previous[1] == current[0], "safetensors tensors overlap or have a gap")
    return len(tensors)


def expected_prompt(parameters: dict[str, Any], formula: str, vector: str) -> str:
    prompt = parameters["prompt"]
    model_input = prompt["formula_template"].format(
        formula=formula,
        vector=vector.rstrip("\n"),
    )
    return prompt["alpaca_template"].format(prompt["instruction"], model_input, "")


def verify_targets(tokenizer: spm.SentencePieceProcessor) -> tuple[int, str]:
    source_manifest = read_json(SOURCE_MANIFEST)
    source_cases = {case["case_id"]: case for case in source_manifest["cases"]}
    manifest = read_json(TARGET_MANIFEST)
    parameters = read_json(PARAMETERS_PATH)
    inference = read_json(INFERENCE_PATH)
    cases = manifest["cases"]

    require(len(source_cases) == EXPECTED_CASES, "source corpus is not 100 cases")
    require(len(cases) == EXPECTED_CASES, "target manifest is not 100 cases")
    require(len({case["case_id"] for case in cases}) == EXPECTED_CASES, "duplicate cases")
    require(
        Counter(case["panel"] for case in cases) == EXPECTED_PANELS,
        "target panel counts differ from 30/30/40",
    )
    require(
        manifest["source_manifest_sha256"] == sha256_file(SOURCE_MANIFEST),
        "source manifest changed after target generation",
    )
    require(
        "reduced composition" in manifest["benchmark_input"]["composition"],
        "target manifest does not declare reduced-composition input",
    )
    require(
        manifest["atomgpt_binning_reference"]["exact_paper_preprocessing_match"] is False,
        "later code reference is incorrectly represented as an exact paper match",
    )

    tokenizer_config = read_json(
        ROOT / read_json(LOCK_PATH)["checkpoint"]["destination"] / "tokenizer_config.json"
    )
    require(tokenizer_config["add_bos_token"] is True, "tokenizer must add BOS")
    model_limit = int(tokenizer_config["model_max_length"])
    generation_budget = int(inference["generation"]["max_new_tokens"])
    token_counts: dict[str, int] = {}

    for case in cases:
        case_id = case["case_id"]
        source = source_cases.get(case_id)
        require(source is not None, f"target case missing from source: {case_id}")
        require(case["composition_kind"] == "reduced_formula", f"composition kind: {case_id}")
        require(
            case["reduced_composition"] == source["formula"],
            f"reduced composition mismatch: {case_id}",
        )
        require(
            case["reduced_formula_key"] == source["reduced_formula_key"],
            f"reduced formula key mismatch: {case_id}",
        )

        paths = {
            kind: TARGET_ROOT / case[f"{kind}_path"] for kind in ("pattern", "vector", "prompt")
        }
        for kind, path in paths.items():
            require(path.is_file(), f"missing {kind}: {case_id}")
            require(
                sha256_file(path) == case[f"{kind}_sha256"],
                f"{kind} digest mismatch: {case_id}",
            )
        source_cif = REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100" / source["path"]
        require(sha256_file(source_cif) == case["source_cif_sha256"], f"CIF changed: {case_id}")

        vector = paths["vector"].read_text(encoding="utf-8")
        lines = vector.splitlines()
        require(len(lines) == 180, f"vector length is not 180: {case_id}")
        require(all(VECTOR_LINE.fullmatch(line) for line in lines), f"vector format: {case_id}")
        values = [float(line) for line in lines]
        require(min(values) >= 0 and max(values) == 1, f"vector normalization: {case_id}")

        pattern_lines = paths["pattern"].read_text(encoding="utf-8").splitlines()
        require(
            pattern_lines[0] == "two_theta_deg,intensity_model_input",
            f"pattern header: {case_id}",
        )
        require(len(pattern_lines) == 181, f"pattern row count: {case_id}")
        for index, (row, value) in enumerate(zip(pattern_lines[1:], lines, strict=True)):
            require(row == f"{index * 0.5:.1f},{value}", f"pattern/vector mismatch: {case_id}")

        prompt = paths["prompt"].read_text(encoding="utf-8")
        require(
            prompt == expected_prompt(parameters, case["model_formula"], vector),
            f"prompt mismatch: {case_id}",
        )
        # LlamaTokenizer adds one BOS token; raw SentencePiece covers the rest.
        token_counts[case_id] = len(tokenizer.encode(prompt, out_type=int)) + 1

    with INPUTS_PATH.open(encoding="utf-8", newline="") as stream:
        input_rows = list(csv.DictReader(stream))
    require(len(input_rows) == EXPECTED_CASES, "inputs.csv is not 100 rows")
    require(
        all(row["composition_kind"] == "reduced_formula" for row in input_rows),
        "inputs.csv does not explicitly declare reduced compositions",
    )
    max_case = max(token_counts, key=token_counts.get)
    max_tokens = token_counts[max_case]
    require(
        max_tokens + generation_budget <= model_limit,
        f"prompt plus generation budget exceeds tokenizer limit: {max_case}",
    )
    return max_tokens, max_case


def main() -> None:
    lock = read_json(LOCK_PATH)
    verify_source(lock)
    checkpoint = verify_checkpoint(lock)
    tensor_count = verify_safetensors(checkpoint / "adapter_model.safetensors")

    tokenizer = spm.SentencePieceProcessor()
    require(tokenizer.load(str(checkpoint / "tokenizer.model")), "cannot load tokenizer")
    require(tokenizer.vocab_size() > 0, "tokenizer vocabulary is empty")
    max_tokens, max_case = verify_targets(tokenizer)

    base = lock["base_model"]
    print(
        f"OK: paper adapter verified ({tensor_count} tensors), tokenizer verified "
        f"({tokenizer.vocab_size()} pieces), and 100 reduced-composition+pXRD prompts "
        f"verified; longest prompt={max_tokens} tokens ({max_case})."
    )
    print(
        "NOTICE: the immutable adapter declares no license; redistribution and "
        "benchmark use require review."
    )
    print(
        "DEFERRED: full generation requires the locked Modal base "
        f"{base['repository']}@{base['revision']}."
    )


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"BAD: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
