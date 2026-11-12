"""Shared command-line driver for framework-specific baseline adapters."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType
from typing import Any

from .candidates import materialize_case_candidates

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RUN_ROOT = REPOSITORY_ROOT / ".runs" / "baselines"

REALPXRD_INPUT_MODES = (
    "lattice-free-primitive-formula-oracle",
    "lattice-conditioned-primitive-cell-oracle",
    "lattice-free-reduced-formula",
)

DATASET_ENV = {
    "corpus_root": "VERIFIABLE_PXRD_CORPUS_ROOT",
    "dataset_id": "VERIFIABLE_PXRD_DATASET_ID",
    "case_prefix": "VERIFIABLE_PXRD_CASE_PREFIX",
    "support_policy": "VERIFIABLE_PXRD_SUPPORT_POLICY",
    "source_manifest_sha256": "VERIFIABLE_PXRD_SOURCE_MANIFEST_SHA256",
}


def load_runner_options(adapter_path: Path) -> dict[str, Any]:
    """Load the paper-condition defaults stored beside an adapter."""

    metadata_path = adapter_path.with_name("baseline.json")
    if not metadata_path.is_file():
        raise RuntimeError(f"missing baseline metadata: {metadata_path}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    options = metadata.get("runner_options", {})
    if not isinstance(options, dict):
        raise RuntimeError(f"runner_options must be an object: {metadata_path}")
    return options


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def configure_dataset(args: argparse.Namespace) -> dict[str, str]:
    corpus = args.corpus_root.expanduser().resolve()
    manifest_path = corpus / "manifest.json"
    if not manifest_path.is_file():
        raise RuntimeError(f"missing corpus manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = list(manifest.get("cases", []))
    if len(cases) != 100:
        raise RuntimeError(f"expected 100 corpus cases, found {len(cases)}")
    dataset_id = args.dataset_id or str(manifest.get("dataset_id") or "")
    if not dataset_id or str(manifest.get("dataset_id")) != dataset_id:
        raise RuntimeError("requested dataset ID does not match the corpus manifest")
    case_prefix = args.case_prefix or str(cases[0]["case_id"]).split("-", 1)[0]
    if any(not str(case["case_id"]).startswith(case_prefix + "-") for case in cases):
        raise RuntimeError("requested case prefix does not cover the corpus")
    identity = {
        "corpus_root": str(corpus),
        "dataset_id": dataset_id,
        "case_prefix": case_prefix,
        "support_policy": args.support_policy,
        "source_manifest_sha256": sha256_file(manifest_path),
    }
    for key, environment_name in DATASET_ENV.items():
        os.environ[environment_name] = identity[key]
    return identity


def load_adapter(framework: str, adapter_path: Path) -> ModuleType:
    """Load an adapter only after the selected corpus has been configured."""

    path = adapter_path.resolve()
    module_name = "verifiable_pxrd_baseline_" + framework.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load baseline adapter: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def output_root(corpus_root: Path, framework: str) -> Path:
    return RUN_ROOT / "outputs" / corpus_root.name.lower() / framework


def handle_path(corpus_root: Path, framework: str, run_id: str) -> Path:
    return RUN_ROOT / "handles" / corpus_root.name.lower() / framework / f"{run_id}.json"


def production_requests(
    adapter: ModuleType,
    *,
    framework: str,
    run_id: str,
    shard_size: int,
    seed_base: int,
    composition_mode: str,
    input_mode: str | None,
) -> list[dict[str, Any]]:
    kwargs: dict[str, Any] = {
        "run_id": run_id,
        "shard_size": shard_size,
        "seed_base": seed_base,
    }
    if framework == "decifer":
        kwargs["composition_mode"] = composition_mode
    elif composition_mode != "reduced":
        raise ValueError("--composition-mode is only supported for deCIFer")
    if framework == "realpxrd-solver":
        kwargs["input_mode"] = input_mode or adapter.DEFAULT_INPUT_MODE
    elif input_mode is not None:
        raise ValueError("--input-mode is only supported for RealPXRD-Solver")
    return adapter.make_requests(**kwargs)


def main(
    framework: str,
    adapter_path: Path,
    argv: Sequence[str] | None = None,
) -> int:
    """Run one framework through the common preflight/submit/collect lifecycle."""

    runner_options = load_runner_options(adapter_path)
    parser = argparse.ArgumentParser(prog=f"{framework}/run.py")
    parser.add_argument("command", choices=("doctor", "preflight", "submit", "collect", "status"))
    parser.add_argument("--run-id")
    parser.add_argument(
        "--corpus-root",
        type=Path,
        default=REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100",
    )
    parser.add_argument("--dataset-id")
    parser.add_argument("--case-prefix")
    parser.add_argument(
        "--support-policy",
        choices=("manifest", "common-envelope", "require-all"),
        default=runner_options.get("support_policy"),
    )
    parser.add_argument("--gpu")
    parser.add_argument("--cpu", type=int, default=8)
    parser.add_argument("--shard-size", type=int)
    parser.add_argument("--seed-base", type=int, default=runner_options.get("seed_base"))
    parser.add_argument("--max-containers", type=int, default=10)
    parser.add_argument("--timeout", type=float, default=0)
    parser.add_argument(
        "--composition-mode",
        choices=("reduced", "full-cell-oracle"),
        default=runner_options.get("composition_mode", "reduced"),
    )
    parser.add_argument(
        "--input-mode",
        choices=REALPXRD_INPUT_MODES,
        default=runner_options.get("input_mode"),
    )
    args = parser.parse_args(argv)
    if args.support_policy is None:
        args.support_policy = "manifest"
    identity = configure_dataset(args)
    adapter = load_adapter(framework, adapter_path)

    shard_size = args.shard_size or int(getattr(adapter, "DEFAULT_SHARD_SIZE", 10))
    gpu = args.gpu or str(getattr(adapter, "DEFAULT_GPU", ""))
    seed_base = args.seed_base if args.seed_base is not None else 20260719

    if args.command == "doctor":
        print(json.dumps(adapter.modal_doctor(gpu_type=gpu), indent=2, sort_keys=True))
        return 0
    if not args.run_id:
        parser.error("--run-id is required for this command")
    requests = production_requests(
        adapter,
        framework=framework,
        run_id=args.run_id,
        shard_size=shard_size,
        seed_base=seed_base,
        composition_mode=args.composition_mode,
        input_mode=args.input_mode,
    )
    corpus_root = Path(identity["corpus_root"])
    handle = handle_path(corpus_root, framework, args.run_id)
    output = output_root(corpus_root, framework)

    if args.command == "preflight":
        if hasattr(adapter, "make_preflight_request"):
            request = adapter.make_preflight_request(
                run_id=f"{args.run_id}-preflight", cpu_count=args.cpu
            )
        else:
            request = dict(requests[0])
            request["run_id"] = f"{args.run_id}-preflight"
            request["case_ids"] = request["case_ids"][:1]
            request["shard_index"] = 0
        shard = adapter.modal_run(request, output, gpu_type=gpu)
        materialize_case_candidates(shard.parent)
        print(shard)
        return 0
    if args.command == "submit":
        if handle.exists():
            raise RuntimeError(f"durable handle already exists: {handle}")
        print(
            adapter.modal_submit(
                requests,
                handle,
                max_containers=args.max_containers,
                gpu_type=gpu,
            )
        )
        return 0
    if not handle.is_file():
        raise RuntimeError(f"missing durable handle: {handle}")
    handle_payload = json.loads(handle.read_text(encoding="utf-8"))
    for key in ("source_dataset_id", "case_prefix", "support_policy", "source_manifest_sha256"):
        expected_key = "dataset_id" if key == "source_dataset_id" else key
        if str(handle_payload.get(key, "")) != identity[expected_key]:
            raise RuntimeError(f"durable handle identity mismatch for {key}")
    if args.command == "collect":
        state = adapter.modal_collect(handle, output, timeout=args.timeout)
        run_root = output / args.run_id
        if run_root.is_dir():
            candidates = materialize_case_candidates(run_root)
            state["case_first_candidates"] = {
                key: value for key, value in candidates.items() if key != "candidates"
            }
        print(json.dumps(state, indent=2, sort_keys=True))
        return 0
    print(handle.read_text(encoding="utf-8"), end="")
    return 0
