from __future__ import annotations

import argparse
import json
from pathlib import Path

from .benchmark import validate_corpus
from .continual import (
    harness_doctor,
    import_training_run,
    launch_training_baseline,
    launch_training_wave,
    training_status,
)
from .coverage import (
    coverage_status,
    evaluate_coverage_run,
    run_coverage,
    run_coverage_replay,
)
from .iterative_coverage import evaluate_iterative_coverage, run_iterative_coverage
from .llm_verifier import evaluate_llm_verifier, run_llm_verifier
from .run import doctor, evaluate_run, run_panel
from .rwp_verifier import score_case, score_monkey_bundles
from .setup_runtime import setup_runtime


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="vpbench")
    commands = root.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate-benchmark")
    validate.add_argument("--root", type=Path, default=Path("pxrd-bench"))
    health = commands.add_parser("doctor")
    health.add_argument("--condition", type=Path, required=True)
    setup = commands.add_parser(
        "setup-runtime",
        help="install the pinned materials-science and GSAS-II runtime on macOS/Linux",
    )
    setup.add_argument(
        "--prefix",
        type=Path,
        default=Path.home() / ".local/share/verifiable-pxrd",
        help="installation root (default: ~/.local/share/verifiable-pxrd)",
    )
    setup.add_argument(
        "--source-condition",
        type=Path,
        help="condition containing the pinned installer payloads",
    )
    setup.add_argument("--codex", type=Path, help="Codex executable (auto-detected by default)")
    setup.add_argument("--cod-metadata", type=Path, help="optional local COD metadata file")
    setup.add_argument("--cod-cifs", type=Path, help="optional local COD CIF directory")
    setup.add_argument(
        "--environment-file",
        type=Path,
        help="sourceable output file (defaults to PREFIX/runtime.env)",
    )
    setup.add_argument("--dry-run", action="store_true", help="print the plan without writing")
    run = commands.add_parser("run")
    run.add_argument("--condition", type=Path, required=True)
    run.add_argument("--panel", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--parallel", type=int, default=1)
    run.add_argument("--replicates", type=int, default=1)
    run.add_argument("--replicate-start", type=int, default=1)
    run.add_argument("--dry-run", action="store_true")
    evaluate = commands.add_parser("evaluate")
    evaluate.add_argument("run_root", type=Path)
    coverage = commands.add_parser("coverage")
    coverage_commands = coverage.add_subparsers(dest="coverage_command", required=True)
    coverage_run = coverage_commands.add_parser("run")
    coverage_run.add_argument("--condition", type=Path, required=True)
    coverage_run.add_argument("--panel", type=Path, required=True)
    coverage_run.add_argument("--output", type=Path, required=True)
    coverage_run.add_argument("--parallel", type=int, default=1)
    coverage_run.add_argument("--dry-run", action="store_true")
    coverage_replay = coverage_commands.add_parser("replay")
    coverage_replay.add_argument("--condition", type=Path, required=True)
    coverage_replay.add_argument("--panel", type=Path, required=True)
    coverage_replay.add_argument("--source", type=Path, required=True)
    coverage_replay.add_argument("--output", type=Path, required=True)
    coverage_replay.add_argument("--parallel", type=int, default=1)
    coverage_replay.add_argument("--dry-run", action="store_true")
    coverage_evaluate = coverage_commands.add_parser("evaluate")
    coverage_evaluate.add_argument("run_root", type=Path)
    coverage_status_command = coverage_commands.add_parser("status")
    coverage_status_command.add_argument("run_root", type=Path)
    coverage_chain = coverage_commands.add_parser("chain")
    coverage_chain.add_argument("--judge-condition", type=Path, required=True)
    coverage_chain.add_argument("--solver-condition", type=Path, required=True)
    coverage_chain.add_argument("--panel", type=Path, required=True)
    coverage_chain.add_argument("--source", type=Path, required=True)
    coverage_chain.add_argument("--wrapper", type=Path, required=True)
    coverage_chain.add_argument("--policy", type=Path, required=True)
    coverage_chain.add_argument("--continuation-prompt", type=Path, required=True)
    coverage_chain.add_argument("--output", type=Path, required=True)
    coverage_chain.add_argument("--parallel", type=int, default=1)
    coverage_chain.add_argument("--max-continuations", type=int, default=7)
    coverage_chain.add_argument("--judge-timeout", type=int)
    coverage_chain.add_argument("--continuation-timeout", type=int)
    coverage_chain.add_argument("--dry-run", action="store_true")
    coverage_chain_evaluate = coverage_commands.add_parser("chain-evaluate")
    coverage_chain_evaluate.add_argument("run_root", type=Path)
    rwp = commands.add_parser("rwp-verifier")
    rwp_commands = rwp.add_subparsers(dest="rwp_command", required=True)
    rwp_score = rwp_commands.add_parser("score")
    rwp_score.add_argument("--pattern", type=Path, required=True)
    rwp_score.add_argument("--wavelength", type=float, required=True)
    rwp_score.add_argument("--candidate", type=Path, action="append", required=True)
    rwp_score.add_argument("--output", type=Path, required=True)
    rwp_score.add_argument("--gsas-python", type=Path)
    rwp_score.add_argument("--parallel", type=int, default=1)
    rwp_score.add_argument("--fit-timeout", type=int, default=300)
    rwp_monkeys = rwp_commands.add_parser("monkeys")
    rwp_monkeys.add_argument("--panel", type=Path, required=True)
    rwp_monkeys.add_argument("--source", type=Path, action="append", required=True)
    rwp_monkeys.add_argument("--output", type=Path, required=True)
    rwp_monkeys.add_argument("--gsas-python", type=Path)
    rwp_monkeys.add_argument("--parallel", type=int, default=1)
    rwp_monkeys.add_argument("--wavelength", type=float)
    rwp_monkeys.add_argument("--fit-timeout", type=int, default=300)
    llm_verifier = commands.add_parser("llm-verifier")
    llm_verifier_commands = llm_verifier.add_subparsers(
        dest="llm_verifier_command", required=True
    )
    llm_verifier_run = llm_verifier_commands.add_parser("run")
    llm_verifier_run.add_argument("--condition", type=Path, required=True)
    llm_verifier_run.add_argument("--panel", type=Path, required=True)
    llm_verifier_run.add_argument("--source", type=Path, required=True)
    llm_verifier_run.add_argument("--wrapper", type=Path, required=True)
    llm_verifier_run.add_argument("--policy", type=Path, required=True)
    llm_verifier_run.add_argument("--output", type=Path, required=True)
    llm_verifier_run.add_argument("--parallel", type=int, default=1)
    llm_verifier_run.add_argument("--timeout", type=int)
    llm_verifier_run.add_argument("--rwp-root", type=Path)
    llm_verifier_run.add_argument("--dry-run", action="store_true")
    llm_verifier_evaluate = llm_verifier_commands.add_parser("evaluate")
    llm_verifier_evaluate.add_argument("run_root", type=Path)
    train = commands.add_parser("train")
    train_commands = train.add_subparsers(dest="train_command", required=True)
    train_doctor = train_commands.add_parser("doctor")
    train_doctor.add_argument("--config", type=Path, required=True)
    train_status = train_commands.add_parser("status")
    train_status.add_argument("--config", type=Path, required=True)
    train_import = train_commands.add_parser("import-run")
    train_import.add_argument("--config", type=Path, required=True)
    train_import.add_argument("--source", type=Path, required=True)
    train_import.add_argument("--label", required=True)
    train_baseline = train_commands.add_parser("baseline")
    train_baseline.add_argument("--config", type=Path, required=True)
    baseline_selection = train_baseline.add_mutually_exclusive_group()
    baseline_selection.add_argument("--next", type=int)
    baseline_selection.add_argument("--problem", action="append", dest="problems")
    baseline_selection.add_argument("--all-missing", action="store_true")
    train_baseline.add_argument("--parallel", type=int)
    train_baseline.add_argument("--label")
    train_baseline.add_argument("--dry-run", action="store_true")
    train_wave = train_commands.add_parser("wave")
    train_wave.add_argument("--config", type=Path, required=True)
    selection = train_wave.add_mutually_exclusive_group()
    selection.add_argument("--next", type=int)
    selection.add_argument("--problem", action="append", dest="problems")
    train_wave.add_argument("--parallel", type=int)
    train_wave.add_argument("--label")
    train_wave.add_argument("--dry-run", action="store_true")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "validate-benchmark":
            result = {
                name: validate_corpus((args.root / name).resolve())
                for name in ("pXRD-100", "pXRD-ood")
            }
            result["valid"] = all(item["valid"] for item in result.values())
        elif args.command == "doctor":
            result = doctor(args.condition)
        elif args.command == "setup-runtime":
            result = setup_runtime(
                args.prefix,
                source_condition=args.source_condition,
                codex=args.codex,
                cod_metadata=args.cod_metadata,
                cod_cifs=args.cod_cifs,
                environment_file=args.environment_file,
                dry_run=args.dry_run,
            )
        elif args.command == "run":
            if args.parallel < 1 or args.replicates < 1 or args.replicate_start < 1:
                raise ValueError("parallel, replicates, and replicate-start must be positive")
            result = run_panel(
                args.condition,
                args.panel,
                args.output,
                args.parallel,
                args.replicates,
                args.replicate_start,
                args.dry_run,
            )
        elif args.command == "evaluate":
            result = evaluate_run(args.run_root)
        elif args.command == "coverage":
            if args.coverage_command == "run":
                if args.parallel < 1:
                    raise ValueError("parallel must be positive")
                result = run_coverage(
                    args.condition,
                    args.panel,
                    args.output,
                    args.parallel,
                    args.dry_run,
                )
            elif args.coverage_command == "replay":
                if args.parallel < 1:
                    raise ValueError("parallel must be positive")
                result = run_coverage_replay(
                    args.condition,
                    args.panel,
                    args.source,
                    args.output,
                    args.parallel,
                    args.dry_run,
                )
            elif args.coverage_command == "evaluate":
                result = evaluate_coverage_run(args.run_root)
            elif args.coverage_command == "status":
                result = coverage_status(args.run_root)
            elif args.coverage_command == "chain":
                if (
                    args.parallel < 1
                    or args.max_continuations < 0
                    or (args.judge_timeout is not None and args.judge_timeout < 1)
                    or (
                        args.continuation_timeout is not None
                        and args.continuation_timeout < 1
                    )
                ):
                    raise ValueError(
                        "parallel and timeouts must be positive; max-continuations cannot be negative"
                    )
                result = run_iterative_coverage(
                    args.judge_condition,
                    args.solver_condition,
                    args.panel,
                    args.source,
                    args.wrapper,
                    args.policy,
                    args.continuation_prompt,
                    args.output,
                    args.parallel,
                    args.max_continuations,
                    args.judge_timeout,
                    args.continuation_timeout,
                    args.dry_run,
                )
            elif args.coverage_command == "chain-evaluate":
                result = evaluate_iterative_coverage(args.run_root)
            else:
                raise AssertionError(args.coverage_command)
        elif args.command == "rwp-verifier":
            if args.parallel < 1 or args.fit_timeout < 1:
                raise ValueError("parallel and fit-timeout must be positive")
            if args.rwp_command == "score":
                result = score_case(
                    args.pattern,
                    args.wavelength,
                    args.candidate,
                    args.output,
                    gsas_python=args.gsas_python,
                    parallel=args.parallel,
                    timeout_seconds=args.fit_timeout,
                )
            elif args.rwp_command == "monkeys":
                result = score_monkey_bundles(
                    args.panel,
                    args.source,
                    args.output,
                    gsas_python=args.gsas_python,
                    parallel=args.parallel,
                    wavelength=args.wavelength,
                    timeout_seconds=args.fit_timeout,
                )
            else:
                raise AssertionError(args.rwp_command)
        elif args.command == "llm-verifier":
            if args.llm_verifier_command == "run":
                if args.parallel < 1 or (args.timeout is not None and args.timeout < 1):
                    raise ValueError("parallel and timeout must be positive")
                result = run_llm_verifier(
                    args.condition,
                    args.panel,
                    args.source,
                    args.wrapper,
                    args.policy,
                    args.output,
                    args.parallel,
                    args.timeout,
                    args.rwp_root,
                    args.dry_run,
                )
            elif args.llm_verifier_command == "evaluate":
                result = evaluate_llm_verifier(args.run_root)
            else:
                raise AssertionError(args.llm_verifier_command)
        elif args.command == "train":
            if args.train_command == "doctor":
                result = harness_doctor(args.config)
            elif args.train_command == "status":
                result = training_status(args.config)
            elif args.train_command == "import-run":
                result = import_training_run(args.config, args.source, args.label)
            elif args.train_command == "baseline":
                if args.parallel is not None and args.parallel < 1:
                    raise ValueError("parallel must be positive")
                result = launch_training_baseline(
                    args.config,
                    problem_ids=args.problems,
                    next_count=args.next,
                    all_missing=args.all_missing,
                    parallel=args.parallel,
                    label=args.label,
                    dry_run=args.dry_run,
                )
            elif args.train_command == "wave":
                if args.parallel is not None and args.parallel < 1:
                    raise ValueError("parallel must be positive")
                result = launch_training_wave(
                    args.config,
                    problem_ids=args.problems,
                    next_count=args.next,
                    parallel=args.parallel,
                    label=args.label,
                    dry_run=args.dry_run,
                )
            else:
                raise AssertionError(args.train_command)
        else:
            raise AssertionError(args.command)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("valid", True) else 1
    except Exception as error:
        print(json.dumps({"error": f"{type(error).__name__}: {error}"}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
