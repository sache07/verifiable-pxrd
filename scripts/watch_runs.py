#!/usr/bin/env python3
"""Render compact progress for one or more vpbench run directories."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from pathlib import Path

SYMBOLS = {
    "pending": "·",
    "running": "R",
    "failed": "!",
    "stopped": "S",
}


def load_progress(root: Path) -> dict[str, object] | None:
    progress = root / "progress.json"
    if not progress.is_file():
        return None
    return json.loads(progress.read_text(encoding="utf-8"))


def load_attempts(root: Path) -> list[dict[str, object]] | None:
    progress = load_progress(root)
    return progress["attempts"] if progress is not None else None


def symbol(row: dict[str, object]) -> str:
    status = str(row.get("status", "pending"))
    if status == "archived":
        return "✓" if row.get("exact_success") is True else "×"  # noqa: RUF001
    return SYMBOLS.get(status, "?")


def summary(attempts: list[dict[str, object]]) -> str:
    names = ("pending", "running", "archived", "failed", "stopped")
    statuses = {name: sum(row.get("status") == name for row in attempts) for name in names}
    exact = sum(row.get("exact_success") is True for row in attempts)
    timed_out = sum(row.get("timed_out") is True for row in attempts)
    return (
        f"exact={exact}/{statuses['archived']} completed | running={statuses['running']} "
        f"pending={statuses['pending']} failed={statuses['failed']} "
        f"stopped={statuses['stopped']} timed_out={timed_out}"
    )


def render(root: Path) -> list[str]:
    progress = load_progress(root)
    if progress is None:
        return [f"{root.name}: not started"]
    attempts = progress["attempts"]
    if attempts and "replicate" not in attempts[0]:
        statuses = {
            name: sum(row.get("status") == name for row in attempts)
            for name in ("pending", "running", "archived", "failed", "staged")
        }
        metrics = progress.get("metrics", {})
        scored = int(metrics.get("count", 0))
        return [
            root.name,
            (
                f"scored={scored}/{len(attempts)} running={statuses['running']} "
                f"pending={statuses['pending']} failed={statuses['failed']}"
            ),
            (
                f"accuracy={float(metrics.get('accuracy', 0)):.3f} "
                f"miss_recall={float(metrics.get('continue_recall', 0)):.3f} "
                f"stop_recall={float(metrics.get('stop_recall', 0)):.3f} "
                f"false_stops={int(metrics.get('false_stop', 0))} "
                f"continuation_rate={float(metrics.get('continuation_rate', 0)):.3f}"
            ),
        ]
    replicates: dict[int, list[dict[str, object]]] = defaultdict(list)
    problem_order: list[str] = []
    seen: set[str] = set()
    for row in attempts:
        problem_id = str(row["problem_id"])
        if problem_id not in seen:
            seen.add(problem_id)
            problem_order.append(problem_id)
        replicates[int(row["replicate"])].append(row)
    if len(replicates) == 1 or len(problem_order) > 40:
        return [f"{root.name}: {summary(attempts)}"]

    lookup = {
        (int(row["replicate"]), str(row["problem_id"])): row
        for row in attempts
    }
    lines = [root.name, "       " + " ".join("──" for _ in problem_order)]
    for replicate in sorted(replicates):
        rows = [lookup[(replicate, problem_id)] for problem_id in problem_order]
        exact = sum(row.get("exact_success") is True for row in rows)
        completed = sum(row.get("status") == "archived" for row in rows)
        matrix = "  ".join(symbol(row) for row in rows)
        lines.append(
            f"rep {replicate:<2} {matrix}   {exact:>2}/{len(rows)}   {completed:>2}/{len(rows)}"
        )
    exact_cases = {
        str(row["problem_id"])
        for row in attempts
        if row.get("exact_success") is True
    }
    lines.extend(
        [
            "",
            "Legend: ✓ exact   × completed miss   R running   · pending   ! failed   S stopped",  # noqa: RUF001
            f"All replicates: {summary(attempts)}",
            f"Pass@{len(replicates)} union so far: {len(exact_cases)}/{len(problem_order)} cases",
        ]
    )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--interval", type=int, default=10)
    args = parser.parse_args()
    while True:
        print("\033[2J\033[H", end="")
        print(time.strftime("%Y-%m-%d %H:%M:%S %Z"))
        for root in args.roots:
            print("\n".join(render(root)))
            print()
        print("\nCtrl-C stops only this dashboard; the runner is in a separate tmux window.")
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
