"""Mechanical extraction of declared CIFs from an LLM text response."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def output_text(response: dict[str, Any]) -> str:
    chunks: list[str] = []
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                chunks.append(str(content["text"]))
    return "\n\n".join(chunks).strip()


def cif_blocks(text: str) -> list[tuple[str | None, str]]:
    """Return (requested filename, CIF) pairs from fenced response text."""

    found: list[tuple[str | None, str]] = []
    fence = re.compile(r"```(?:cif)?\s*\n?(data_[\s\S]*?)```", re.IGNORECASE)
    for match in fence.finditer(text):
        context = text[max(0, match.start() - 180) : match.start()]
        names = re.findall(
            r"(?:selected|alternative-\d+)\.cif",
            context,
            flags=re.IGNORECASE,
        )
        name = names[-1].lower() if names else None
        found.append((name, match.group(1).strip() + "\n"))
    if not found:
        start = re.search(r"(?m)^data_\S*", text)
        if start:
            found.append((None, text[start.start() :].strip() + "\n"))
    return found


def materialize_cifs(text: str, workspace: Path) -> list[str]:
    workspace.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    next_alternative = 1
    for index, (requested, body) in enumerate(cif_blocks(text)):
        if (
            requested == "selected.cif" and "selected.cif" not in written
        ) or (requested and re.fullmatch(r"alternative-\d+\.cif", requested)):
            name = str(requested)
        elif index == 0 and "selected.cif" not in written:
            name = "selected.cif"
        else:
            while f"alternative-{next_alternative}.cif" in written:
                next_alternative += 1
            name = f"alternative-{next_alternative}.cif"
            next_alternative += 1
        if name in written:
            while f"alternative-{next_alternative}.cif" in written:
                next_alternative += 1
            name = f"alternative-{next_alternative}.cif"
            next_alternative += 1
        (workspace / name).write_text(body, encoding="utf-8")
        written.append(name)
    return written
