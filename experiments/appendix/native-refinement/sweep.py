"""Run disjoint account shards with bounded concurrency and a shared budget.

Launch one process per authenticated Modal profile. Keep this local coordinator
running; --detach protects already submitted calls if it is interrupted. Resume
with the identical command to reconnect to durable call IDs, without re-running
collected tasks. A reservation with no call ID requires manual reconciliation.
"""
from __future__ import annotations
import argparse
from collections import Counter, deque
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import os
from pathlib import Path
import shutil
import time

from common import HERE, code_hash, fingerprint, read_json, verify_task, write_json
from sweep_budget import Budget


def shard_tasks(tasks, shard, shards):
    if not 0 <= shard < shards:
        raise ValueError("Invalid shard")
    return [task for i, task in enumerate(tasks) if i % shards == shard]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--shard", type=int, required=True)
    parser.add_argument("--shards", type=int, default=2)
    parser.add_argument("--gpus", type=int, default=10)
    parser.add_argument("--cpus", type=int, default=4, help="Concurrent CPU workers, each with 2 cores")
    parser.add_argument("--budget", type=float, required=True)
    parser.add_argument("--allow-full", action="store_true")
    args = parser.parse_args()
    if not args.allow_full:
        parser.error("Requires --allow-full and prior spending approval")
    if min(args.gpus, args.cpus) < 1:
        parser.error("Concurrency must be positive")
    if not args.campaign.replace("-", "").replace("_", "").isalnum():
        parser.error("Unsafe campaign name")
    # Must be set before importing Modal or constructing its client/functions.
    os.environ["MODAL_PROFILE"] = args.profile
    os.environ["NATIVE_GPU_CONCURRENCY"] = str(args.gpus)
    os.environ["NATIVE_CPU_CONCURRENCY"] = str(args.cpus)
    import modal
    from remote import app, collect, cpu_worker, gpu_worker, SOURCE_HASH_AT_IMPORT

    source_hash = SOURCE_HASH_AT_IMPORT
    all_tasks = read_json(args.tasks)
    manifest = read_json(args.tasks.parent / "manifest.json")
    if fingerprint(all_tasks) != manifest["tasks_sha256"]:
        raise ValueError("Frozen task manifest does not match task file")
    tasks = shard_tasks(all_tasks, args.shard, args.shards)
    del all_tasks
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    identity = dict(profile=args.profile, campaign=args.campaign, shard=args.shard, shards=args.shards,
                    tasks_sha256=manifest["tasks_sha256"], source_hash=source_hash,
                    ids=[t["id"] for t in tasks], budget_usd=args.budget,
                    ledger=str(args.ledger.resolve()), gpu_workers=args.gpus, cpu_workers=args.cpus)
    plan = root / "plan.json"
    if plan.exists() and read_json(plan) != identity:
        raise ValueError("Existing plan differs; do not overwrite a running campaign")
    write_json(plan, identity)
    snapshot = root / "runner"
    snapshot.mkdir(exist_ok=True)
    for path in HERE.iterdir():
        if path.is_file() and path.suffix in {".py", ".json"}:
            shutil.copy2(path, snapshot / path.name)
    budget = Budget(args.ledger, args.budget)
    records = budget.records()
    queues = {"gpu": deque(), "cpu": deque()}
    reconnect = []
    statuses = Counter()
    for task in tasks:
        verify_task(task)
        key = fingerprint({"task": task, "source": source_hash})
        result_path = root / "candidates" / task["id"] / "result.json"
        prior = records.get(key)
        if prior and (prior["profile"] != args.profile or prior["output"] != str(root)):
            raise ValueError("Candidate is assigned to another profile/output")
        if result_path.exists():
            result = read_json(result_path)
            if result.get("task_fingerprint") != key:
                raise ValueError(f"Mismatched prior result: {result_path}")
            if not prior:
                raise ValueError("Existing result has no budget record")
            budget.settle(key, task, result)
            statuses[result["status"]] += 1
        elif prior:
            if not prior.get("call_id"):
                raise ValueError(f"Unresolved reservation for {task['id']}; inspect before retrying")
            reconnect.append((task, key, prior["call_id"]))
        else:
            queues["gpu" if task["method"] == "crystalyze" else "cpu"].append((task, key))
    print(f"Profile {args.profile}; shard {args.shard}/{args.shards}; {len(tasks)} tasks; "
          f"{sum(map(len, queues.values()))} unsubmitted; {len(reconnect)} reconnects; "
          f"{dict(statuses)} collected; code {source_hash}", flush=True)
    limits = {"gpu": 2 * args.gpus, "cpu": 2 * args.cpus}
    active = Counter()
    pending = {}
    abort = False
    def progress(state):
        write_json(root / "progress.json", dict(state=state, updated_unix=time.time(),
            profile=args.profile, shard=args.shard, total=len(tasks), collected=dict(statuses),
            submitted_pending=dict(active), unsubmitted={k: len(v) for k, v in queues.items()}))
    progress("building")
    with modal.enable_output(), app.run(name=f"{args.campaign}-{args.profile}", detach=True):
        if code_hash() != source_hash:
            raise ValueError("Runner files changed during image build; refusing source drift")
        with ThreadPoolExecutor(max_workers=sum(limits.values()) + len(reconnect)) as pool:
            def track(task, key, call, call_id=None):
                kind = "gpu" if task["method"] == "crystalyze" else "cpu"
                active[kind] += 1
                pending[pool.submit(call.get)] = (task, key, kind, call_id or call.object_id)
            for task, key, call_id in reconnect:
                track(task, key, modal.FunctionCall.from_id(call_id), call_id)
            while pending or any(queues.values()):
                if not abort:
                    for kind, queue in queues.items():
                        while queue and active[kind] < limits[kind]:
                            task, key = queue[0]
                            if not budget.reserve(key, task, profile=args.profile, output=str(root),
                                                  campaign=args.campaign, source_hash=source_hash):
                                break
                            queue.popleft()
                            try:
                                function = gpu_worker if kind == "gpu" else cpu_worker
                                call = function.spawn(task, args.campaign, source_hash)
                                budget.update(key, call_id=call.object_id, state="submitted")
                                track(task, key, call)
                            except Exception as error:
                                # Submission may have succeeded remotely: retain the hold.
                                budget.update(key, state="submission_unknown", error=repr(error))
                                print(f"SUBMISSION ERROR; stopping new calls: {error}", flush=True)
                                abort = True
                                break
                progress("draining_after_error" if abort else "running")
                if not pending:
                    break  # All finished, or budget exhausted: never silently exceed cap.
                done, _ = wait(pending, timeout=30, return_when=FIRST_COMPLETED)
                for future in done:
                    task, key, kind, call_id = pending.pop(future)
                    active[kind] -= 1
                    try:
                        payload = future.result()
                        collect(payload, root)
                        budget.settle(key, task, payload["result"])
                        statuses[payload["result"]["status"]] += 1
                        result = payload["result"]
                        if result.get("code_sha256") not in (None, source_hash):
                            raise ValueError("Remote source hash differs")
                    except Exception as error:
                        budget.update(key, state="collection_error", error=repr(error))
                        print(f"COLLECTION ERROR {call_id}; reconnect on resume: {error}", flush=True)
                        abort = True
    state = "needs_recovery" if abort else "budget_paused" if any(queues.values()) else "complete"
    progress(state)
    print(f"{state}: {dict(statuses)}; {sum(map(len, queues.values()))} unsubmitted", flush=True)
    if state != "complete":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
