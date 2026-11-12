#!/usr/bin/env python3
"""Fail fast on machine-readable PXRD submission omissions and schema drift."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


REQUIRED_OUTPUTS = ("result.json", "report.md", "fit.csv", "final.gpx")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", nargs="?", default=".", type=Path)
    parser.add_argument("--fraction-tolerance", type=float, default=0.005)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    errors: list[dict] = []
    warnings: list[dict] = []
    for name in REQUIRED_OUTPUTS:
        path = workspace / name
        if not path.is_file() or path.stat().st_size == 0:
            errors.append({"reason": "missing_or_empty_required_output", "path": name})

    data = None
    try:
        data = json.loads((workspace / "result.json").read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append({"reason": "unreadable_result_json", "error": str(exc)})

    fractions: list[float] = []
    paths: list[str] = []
    if data is not None:
        if not isinstance(data, dict):
            errors.append({"reason": "result_json_not_object"})
        else:
            rows_key = next((key for key in ("phases", "crystalline_phases") if key in data), None)
            rows = data.get(rows_key) if rows_key else None
            if not isinstance(rows, list) or not rows:
                phase_like = sorted(
                    key for key, value in data.items() if "phase" in key.lower() and isinstance(value, list)
                )
                errors.append(
                    {
                        "reason": "missing_nonempty_top_level_phases_array",
                        "phase_like_unrecognized_keys": phase_like,
                    }
                )
                rows = []
            elif rows_key != "phases":
                warnings.append({"reason": "recognized_noncanonical_phase_array", "key": rows_key})
            if len(rows) > 16:
                errors.append({"reason": "too_many_phase_records", "count": len(rows)})
            for index, row in enumerate(rows):
                if not isinstance(row, dict):
                    errors.append({"reason": "phase_record_not_object", "index": index})
                    continue
                cif_key = next(
                    (key for key in ("cif_path", "cif", "structure_file") if key in row), None
                )
                cif = row.get(cif_key) if cif_key else None
                if not isinstance(cif, str) or not cif.strip():
                    errors.append({"reason": "phase_missing_recognized_cif_path", "index": index})
                else:
                    path = (workspace / cif).resolve()
                    if not path.is_relative_to(workspace) or not path.is_file():
                        errors.append(
                            {"reason": "phase_cif_missing_or_external", "index": index, "cif_path": cif}
                        )
                    paths.append(str(path))
                    if cif_key != "cif_path":
                        warnings.append(
                            {"reason": "recognized_noncanonical_cif_path", "index": index, "key": cif_key}
                        )
                fraction_key = next(
                    (key for key in ("weight_fraction", "weight_percent", "wt_percent") if key in row),
                    None,
                )
                fraction = row.get(fraction_key) if fraction_key else None
                try:
                    if isinstance(fraction, bool):
                        raise ValueError("boolean")
                    value = float(fraction)
                    if fraction_key in ("weight_percent", "wt_percent"):
                        value /= 100.0
                    if not math.isfinite(value) or value <= 0 or value > 1:
                        raise ValueError("must be finite in (0,1]")
                    fractions.append(value)
                    if fraction_key != "weight_fraction":
                        warnings.append(
                            {
                                "reason": "recognized_noncanonical_fraction",
                                "index": index,
                                "key": fraction_key,
                            }
                        )
                except (TypeError, ValueError, OverflowError) as exc:
                    errors.append(
                        {
                            "reason": "invalid_weight_fraction",
                            "index": index,
                            "value": fraction,
                            "error": str(exc),
                        }
                    )
            if len(paths) != len(set(paths)):
                errors.append({"reason": "duplicate_cif_path"})
            if fractions and len(fractions) == len(rows):
                total = sum(fractions)
                if abs(total - 1.0) > args.fraction_tolerance:
                    errors.append(
                        {
                            "reason": "weight_fractions_not_normalized",
                            "sum": total,
                            "tolerance": args.fraction_tolerance,
                        }
                    )
            unresolved = data.get("unresolved_components", [])
            if unresolved and not isinstance(unresolved, list):
                errors.append({"reason": "unresolved_components_not_array"})
            elif isinstance(unresolved, list) and unresolved:
                warnings.append(
                    {
                        "reason": "unresolved_components_require_conditional_fraction_review",
                        "count": len(unresolved),
                    }
                )

    report = {
        "workspace": str(workspace),
        "status": "fail" if errors else "pass",
        "phase_count": len(fractions),
        "fraction_sum": sum(fractions) if fractions else None,
        "errors": errors,
        "warnings": warnings,
        "scope": "Schema/path/fraction readback only; run CIF and GPX audits separately.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
