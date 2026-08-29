#!/usr/bin/env python3
"""Run the same pXRD task with model-only and Code Interpreter Responses.

The script intentionally exposes no developer prompt and no tools beyond the
optional stock Code Interpreter. It saves the complete API objects and any
container files so the two behaviors can be inspected after the run.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import requests

TERMINAL_STATUSES = {"completed", "failed", "cancelled", "incomplete"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class OpenAIHTTP:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def json_request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        response = self.session.request(
            method,
            f"{self.base_url}{path}",
            timeout=120,
            **kwargs,
        )
        response.raise_for_status()
        return response.json()

    def upload(self, path: Path) -> dict[str, Any]:
        with path.open("rb") as handle:
            return self.json_request(
                "POST",
                "/files",
                data={"purpose": "user_data"},
                files={"file": (path.name, handle, "text/csv")},
            )

    def download(self, path: str) -> bytes:
        response = self.session.get(f"{self.base_url}{path}", timeout=120)
        response.raise_for_status()
        return response.content


def output_text(response: dict[str, Any]) -> str:
    chunks: list[str] = []
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                chunks.append(content["text"])
    return "\n\n".join(chunks).strip()


def container_ids(response: dict[str, Any]) -> list[str]:
    found: set[str] = set()
    for item in response.get("output", []):
        if item.get("container_id"):
            found.add(item["container_id"])
        for content in item.get("content", []):
            for annotation in content.get("annotations", []):
                if annotation.get("container_id"):
                    found.add(annotation["container_id"])
    return sorted(found)


def safe_filename(name: str, fallback: str) -> str:
    clean = Path(name).name
    return clean if clean not in {"", ".", ".."} else fallback


def download_container_files(
    client: OpenAIHTTP,
    response: dict[str, Any],
    output_dir: Path,
) -> list[Path]:
    downloaded: list[Path] = []
    for container_id in container_ids(response):
        listing = client.json_request(
            "GET", f"/containers/{container_id}/files", params={"limit": 100}
        )
        target = output_dir / "container-files" / container_id
        target.mkdir(parents=True, exist_ok=True)
        for item in listing.get("data", []):
            file_id = item["id"]
            name = safe_filename(
                item.get("path") or item.get("filename") or "",
                file_id,
            )
            destination = target / name
            if destination.exists():
                destination = target / f"{file_id}-{name}"
            destination.write_bytes(
                client.download(f"/containers/{container_id}/files/{file_id}/content")
            )
            downloaded.append(destination)
            if name in {"selected.cif"} or re.fullmatch(r"alternative-\d+\.cif", name):
                shutil.copy2(destination, output_dir / name)
    return downloaded


def extract_cif_from_text(text: str, destination: Path) -> bool:
    fenced = re.search(r"```(?:cif)?\s*\n?(data_[\s\S]*?)```", text, re.IGNORECASE)
    if fenced:
        destination.write_text(fenced.group(1).strip() + "\n", encoding="utf-8")
        return True
    start = re.search(r"(?m)^data_\S*", text)
    if start:
        destination.write_text(text[start.start() :].strip() + "\n", encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--poll-seconds", type=float, default=10.0)
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

    problem = args.problem.resolve()
    prompt_path = problem / "problem_input" / "prompt.md"
    pattern_path = problem / "problem_input" / "pattern.csv"
    if not prompt_path.is_file() or not pattern_path.is_file():
        raise SystemExit(f"problem lacks prompt.md or pattern.csv: {problem}")

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(prompt_path, output / "prompt.md")
    shutil.copy2(pattern_path, output / "pattern.csv")
    prompt = prompt_path.read_text(encoding="utf-8").strip()

    client = OpenAIHTTP(api_key, base_url)
    uploaded = client.upload(pattern_path)
    file_id = uploaded["id"]
    manifest = {
        "problem": problem.name,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "prompt_sha256": sha256(prompt_path),
        "pattern_sha256": sha256(pattern_path),
        "conditions": {
            "model-only": {"tools": []},
            "code-interpreter": {"tools": ["code_interpreter"]},
        },
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    common: dict[str, Any] = {
        "model": args.model,
        "reasoning": {"effort": args.reasoning_effort},
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_file", "file_id": file_id},
                ],
            }
        ],
        "background": True,
        "store": True,
        "max_output_tokens": 65536,
    }
    payloads = {
        "model-only": dict(common),
        "code-interpreter": {
            **common,
            "tools": [
                {
                    "type": "code_interpreter",
                    "container": {"type": "auto", "memory_limit": "4g"},
                }
            ],
        },
    }

    responses: dict[str, dict[str, Any]] = {}
    for condition, payload in payloads.items():
        condition_dir = output / condition
        condition_dir.mkdir()
        request_manifest = {**payload, "input": "prompt.md + pattern.csv"}
        (condition_dir / "request.json").write_text(
            json.dumps(request_manifest, indent=2) + "\n", encoding="utf-8"
        )
        response = client.json_request("POST", "/responses", json=payload)
        responses[condition] = response
        print(f"submitted {condition}: {response['id']}", flush=True)

    pending = set(responses)
    while pending:
        for condition in sorted(tuple(pending)):
            response = client.json_request(
                "GET", f"/responses/{responses[condition]['id']}"
            )
            responses[condition] = response
            with (output / condition / "poll.jsonl").open("a", encoding="utf-8") as log:
                log.write(
                    json.dumps(
                        {
                            "time": time.time(),
                            "status": response.get("status"),
                            "error": response.get("error"),
                        }
                    )
                    + "\n"
                )
            print(f"{condition}: {response.get('status')}", flush=True)
            if response.get("status") in TERMINAL_STATUSES:
                pending.remove(condition)
        if pending:
            time.sleep(args.poll_seconds)

    for condition, response in responses.items():
        condition_dir = output / condition
        (condition_dir / "response.json").write_text(
            json.dumps(response, indent=2) + "\n", encoding="utf-8"
        )
        text = output_text(response)
        (condition_dir / "output.md").write_text(text + "\n", encoding="utf-8")
        if condition == "code-interpreter":
            try:
                download_container_files(client, response, condition_dir)
            except requests.HTTPError as error:
                (condition_dir / "container-download-error.txt").write_text(
                    str(error) + "\n", encoding="utf-8"
                )
        if not (condition_dir / "selected.cif").exists():
            extract_cif_from_text(text, condition_dir / "selected.cif")

    with contextlib.suppress(requests.HTTPError):
        client.json_request("DELETE", f"/files/{file_id}")

    failed = [
        name for name, response in responses.items() if response.get("status") != "completed"
    ]
    print(f"artifacts: {output}", flush=True)
    if failed:
        print(f"non-completed conditions: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
