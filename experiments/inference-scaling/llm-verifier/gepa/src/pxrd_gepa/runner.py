from __future__ import annotations

import dataclasses
import hashlib
import json
import shutil
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .benchmark import evaluate_example, import_vpbench, rwp_summary, structural_diagnostics
from .decision import score_decision, validate_decision
from .models import Example, ExperimentConfig
from .prompting import render_feedback, render_reflection, render_reviewer


class CodexRuntime:
    def __init__(self, config: ExperimentConfig, run_root: Path):
        self.config = config
        self.run_root = run_root
        self.run_root.mkdir(parents=True, exist_ok=True)
        self.modules = import_vpbench(config)
        base = self.modules["condition"].load_condition(config.condition)
        reviewer = config.reviewer
        self.review_condition = dataclasses.replace(
            base,
            model=str(reviewer["model"]),
            reasoning_effort=str(reviewer["reasoning_effort"]),
            # The benchmark condition's solve prompt is not used for reviewer calls.
            # Pin the active prompt path to this experiment's visible wrapper so the
            # runtime contract does not depend on an unrelated solver prompt.
            prompt=config.prompts.wrapper,
            cpu_quota=str(reviewer["cpu_quota"]),
            memory_max=str(reviewer["memory_max"]),
            tasks_max=int(reviewer["tasks_max"]),
            timeout_seconds=int(reviewer["timeout_seconds"]),
            network=bool(reviewer["network"]),
        )
        reflection = config.reflection
        self.reflection_condition = dataclasses.replace(
            base,
            model=str(reflection["model"]),
            reasoning_effort=str(reflection["reasoning_effort"]),
            timeout_seconds=int(reflection["timeout_seconds"]),
            capability=None,
            network=False,
        )
        self._lock = threading.Lock()
        self._count = 0

    def _new_root(self, lane: str, label: str) -> Path:
        with self._lock:
            self._count += 1
            count = self._count
        token = uuid.uuid4().hex[:8]
        root = self.run_root / lane / f"{count:05d}-{label}-{token}"
        root.mkdir(parents=True)
        return root

    @staticmethod
    def _stage_example(example: Example, root: Path) -> dict[str, Any]:
        evidence = root / "evidence"
        control = root / "control"
        evidence.mkdir()
        control.mkdir()
        staged: dict[str, Any] = {}
        trace_name = (
            "first-pass-trace.jsonl.gz"
            if example.trace.suffix == ".gz"
            else "first-pass-trace.jsonl"
        )
        for key, source, name in (
            ("pattern", example.pattern, "pattern.csv"),
            ("trace", example.trace, trace_name),
            ("final_response", example.final_response, "first-pass-final.md"),
        ):
            destination = evidence / name
            shutil.copy2(source, destination)
            staged[key] = destination
        candidates = []
        for index, source in enumerate(example.candidates):
            name = source.name
            destination = evidence / name
            if destination.exists():
                destination = evidence / f"candidate-{index + 1:03d}.cif"
            shutil.copy2(source, destination)
            candidates.append(destination)
        staged["candidates"] = candidates
        report = evidence / "comparable-rwp-report.json"
        if example.rwp_report is not None:
            shutil.copy2(example.rwp_report, report)
        else:
            report.write_text(
                json.dumps({"available": False, "reason": "not supplied"}, indent=2) + "\n",
                encoding="utf-8",
            )
        staged["rwp_report"] = report
        shutil.copy2(example.reference, control / "reference.cif")
        return {"evidence": evidence, "control": control, **staged}

    def review(self, example: Example, policy: str) -> dict[str, Any]:
        policy_hash = hashlib.sha256(policy.encode()).hexdigest()[:10]
        root = self._new_root("evaluations", f"{example.example_id}-{policy_hash}")
        staged = self._stage_example(example, root)
        workspace = root / "workspace"
        codex_home = root / "codex-home"
        run_dir = root / "run"
        judge_record = root / "judge-record"
        oracle_record = root / "oracle-record"
        judge_record.mkdir()
        oracle_record.mkdir()
        prompt = render_reviewer(self.config.prompts.wrapper, policy, example, staged)
        (root / "prompt.md").write_text(prompt, encoding="utf-8")
        (root / "judge-policy.md").write_text(policy.rstrip() + "\n", encoding="utf-8")
        (judge_record / "prompt.md").write_text(prompt, encoding="utf-8")
        (judge_record / "judge-policy.md").write_text(policy.rstrip() + "\n", encoding="utf-8")
        coverage = self.modules["coverage"]
        coverage._prepare_agent_home(
            self.review_condition,
            workspace,
            codex_home,
            (staged["evidence"],),
        )
        launch = coverage._run_agent(
            self.review_condition,
            workspace,
            codex_home,
            run_dir,
            prompt,
            "gepa-review-" + uuid.uuid4().hex[:10],
            float(self.review_condition.timeout_seconds),
        )
        decision = None
        error = None
        try:
            decision = validate_decision(workspace / "decision.json")
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        for source, name in (
            (run_dir / "codex-events.jsonl", "codex-events.jsonl"),
            (run_dir / "final-answer.md", "final-answer.md"),
            (run_dir / "launch.json", "launch.json"),
            (workspace / "decision.json", "decision.json"),
        ):
            if source.is_file():
                shutil.copy2(source, judge_record / name)
        if error:
            (judge_record / "decision-error.txt").write_text(error + "\n", encoding="utf-8")
        verifier = evaluate_example(self.config, example)
        candidates_exact = bool(verifier["candidates_exact"])
        predicted = decision["decision"] if decision else None
        oracle, score = score_decision(
            predicted,
            candidates_exact,
            false_continue_credit=float(self.config.objective["false_continue_credit"]),
        )
        decision_correct = predicted == oracle
        diagnostics = structural_diagnostics(example, verifier)
        rwp = rwp_summary(example.rwp_report)
        feedback = render_feedback(
            self.config.prompts.feedback,
            {
                "predicted_decision": predicted or "invalid",
                "oracle_decision": oracle,
                "decision_correct": decision_correct,
                "verifier_result": verifier,
                "rwp_summary": rwp,
            },
        )
        (oracle_record / "verifier-result.json").write_text(
            json.dumps(verifier, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        (oracle_record / "structural-diagnostics.json").write_text(
            json.dumps(diagnostics, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        (oracle_record / "evaluator-feedback.md").write_text(feedback, encoding="utf-8")
        shutil.copy2(staged["control"] / "reference.cif", oracle_record / "reference.cif")
        result = {
            "example_id": example.example_id,
            "problem_id": example.problem_id,
            "decision": decision,
            "decision_error": error,
            "oracle_decision": oracle,
            "score": score,
            "decision_correct": decision_correct,
            "candidates_exact": candidates_exact,
            "verifier": verifier,
            "structural_diagnostics": diagnostics,
            "rwp_summary": rwp,
            "feedback": feedback,
            "reflection_artifacts": {
                "blind_evidence": str(staged["evidence"]),
                "judge_record": str(judge_record),
                "oracle_record": str(oracle_record),
                "reference": str(oracle_record / "reference.cif"),
            },
            "launch": launch,
            "run_root": str(root),
        }
        (root / "evaluation.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return result

    def review_batch(self, examples: list[Example], policy: str) -> list[dict[str, Any]]:
        parallel = max(1, int(self.config.reviewer["parallel"]))
        with ThreadPoolExecutor(max_workers=min(parallel, len(examples))) as executor:
            return list(executor.map(lambda example: self.review(example, policy), examples))

    def reflect(self, current_policy: str, reflective_examples: Any) -> str:
        root = self._new_root("reflections", "mutation")
        workspace = root / "workspace"
        codex_home = root / "codex-home"
        run_dir = root / "run"
        prompt = render_reflection(
            self.config.prompts.reflection,
            current_policy,
            reflective_examples,
            int(self.config.reflection["max_policy_words"]),
        )
        (root / "prompt.md").write_text(prompt, encoding="utf-8")
        coverage = self.modules["coverage"]
        artifact_directories: list[Path] = []
        for record in reflective_examples:
            directories = record.get("Inputs", {}).get("artifact_directories", {})
            for value in directories.values():
                path = Path(value)
                readable = path if path.is_dir() else path.parent
                if readable not in artifact_directories:
                    artifact_directories.append(readable)
        coverage._prepare_agent_home(
            self.reflection_condition,
            workspace,
            codex_home,
            tuple(artifact_directories),
        )
        coverage._run_agent(
            self.reflection_condition,
            workspace,
            codex_home,
            run_dir,
            prompt,
            "gepa-reflect-" + uuid.uuid4().hex[:10],
            float(self.reflection_condition.timeout_seconds),
        )
        policy_path = workspace / "judge-policy.md"
        if not policy_path.is_file():
            raise RuntimeError(f"reflection did not write judge-policy.md: {root}")
        policy = policy_path.read_text(encoding="utf-8").strip()
        words = len(policy.split())
        maximum = int(self.config.reflection["max_policy_words"])
        if not policy or words > maximum:
            raise ValueError(f"reflected policy has {words} words; expected 1..{maximum}")
        (root / "accepted-policy.md").write_text(policy + "\n", encoding="utf-8")
        return policy

    def text_lm(self, prompt: str | list[dict[str, Any]]) -> str:
        root = self._new_root("reflections", "gepa-language-model")
        workspace = root / "workspace"
        codex_home = root / "codex-home"
        run_dir = root / "run"
        text = prompt if isinstance(prompt, str) else json.dumps(prompt, indent=2)
        coverage = self.modules["coverage"]
        coverage._prepare_agent_home(self.reflection_condition, workspace, codex_home)
        coverage._run_agent(
            self.reflection_condition,
            workspace,
            codex_home,
            run_dir,
            text,
            "gepa-lm-" + uuid.uuid4().hex[:10],
            float(self.reflection_condition.timeout_seconds),
        )
        answer = run_dir / "final-answer.md"
        if not answer.is_file():
            raise RuntimeError("reflection language model produced no final answer")
        return answer.read_text(encoding="utf-8")
