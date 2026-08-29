from __future__ import annotations

import gzip
import json
from pathlib import Path


def readable_trace(path: Path, max_chars: int = 80_000) -> str:
    blocks: list[str] = []
    size = 0
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            item = event.get("item") or {}
            if event.get("type") != "item.completed":
                continue
            kind = item.get("type")
            block = ""
            if kind == "agent_message":
                block = "Agent message:\n" + str(item.get("text", ""))
            elif kind == "command_execution":
                output = str(item.get("aggregated_output", ""))
                if len(output) > 4_000:
                    output = output[:2_000] + "\n...[elided]...\n" + output[-2_000:]
                block = f"Command:\n{item.get('command', '')}\nOutput:\n{output}"
            if block:
                blocks.append(block)
                size += len(block)
            if size >= max_chars:
                blocks.append("[Trace truncated at the fixed reflection bound.]")
                break
    return "\n\n".join(blocks)
