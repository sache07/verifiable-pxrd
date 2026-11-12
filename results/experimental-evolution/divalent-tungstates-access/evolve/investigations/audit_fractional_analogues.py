"""Audit fractional-composition and loose prototype routes missed by library_neighbours.py.

This is a curation diagnostic, not solver guidance. It retains entries with the
same normalized anion/cation stoichiometry as an ordered target, then performs a
chemistry-blind framework match. Fractional solid solutions are intentionally
included because they can be purified into an ordered target model.
"""

from __future__ import annotations

import argparse
import gzip
import json
import warnings
from pathlib import Path

from pymatgen.analysis.structure_matcher import FrameworkComparator, StructureMatcher
from pymatgen.core import Composition, Structure


INDEX = Path(
    "<HOME>/.local/share/characterizagent/backends/dara/venv/"
    "lib/python3.11/site-packages/dara/data/cod_filtered_info_2024.json.gz"
)
CIFS = Path("<HOME>/.local/share/characterizagent/backends/dara/cod-filtered-2024/cif")


def cif_path(record_id: str) -> Path:
    return CIFS / record_id[0] / record_id[1:3] / record_id[3:5] / f"{record_id}.cif"


def load(path: Path) -> Structure:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        structure = Structure.from_file(path, primitive=False)
    structure.remove_oxidation_states()
    return structure


def normalized_counts(composition: Composition, oxygen_target: float) -> dict[str, float] | None:
    counts = composition.get_el_amt_dict()
    oxygen = counts.get("O", 0.0)
    if oxygen <= 0:
        return None
    scale = oxygen_target / oxygen
    return {element: amount * scale for element, amount in counts.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--stol", type=float, default=0.5)
    parser.add_argument("--ltol", type=float, default=0.3)
    parser.add_argument("--angle-tol", type=float, default=10.0)
    parser.add_argument("--max-sites", type=int, default=80)
    parser.add_argument(
        "--direct-only",
        action="store_true",
        help=(
            "pre-filter to candidates retaining both target cations or replacing "
            "only one target cation by one candidate cation"
        ),
    )
    args = parser.parse_args()

    target = load(args.model)
    target_reduced = target.composition.reduced_composition
    target_counts = target_reduced.get_el_amt_dict()
    oxygen_target = target_counts.get("O", 0.0)
    target_total = sum(target_counts.values())
    target_cations = set(target_counts) - {"O"}
    matcher = StructureMatcher(
        ltol=args.ltol,
        stol=args.stol,
        angle_tol=args.angle_tol,
        primitive_cell=True,
        scale=True,
        attempt_supercell=True,
        allow_subset=False,
        comparator=FrameworkComparator(),
    )

    with gzip.open(INDEX, "rt") as handle:
        index = json.load(handle)

    rows: list[dict[str, object]] = []
    considered = 0
    for system, entries in index.items():
        for formula, raw_id, space_group_number, *_ in entries:
            record_id = str(raw_id)
            try:
                index_composition = Composition(formula)
            except Exception:
                continue
            normalized = normalized_counts(index_composition, oxygen_target)
            if normalized is None:
                continue
            if abs(sum(normalized.values()) - target_total) > 0.03:
                continue
            index_cations = set(normalized) - {"O"}
            if index_cations - target_cations and len(index_cations) > 3:
                continue
            if args.direct_only:
                missing_index = target_cations - index_cations
                extra_index = index_cations - target_cations
                if len(missing_index) > 1 or len(extra_index) > 1:
                    continue
            path = cif_path(record_id)
            if not path.is_file():
                continue
            try:
                candidate = load(path)
            except Exception:
                continue
            if len(candidate) > args.max_sites:
                continue
            structure_counts = normalized_counts(candidate.composition, oxygen_target)
            if structure_counts is None or abs(sum(structure_counts.values()) - target_total) > 0.03:
                continue
            considered += 1
            try:
                rms = matcher.get_rms_dist(target, candidate)
            except Exception:
                rms = None
            candidate_cations = set(structure_counts) - {"O"}
            missing = sorted(target_cations - candidate_cations)
            retained = sorted(target_cations & candidate_cations)
            extras = sorted(candidate_cations - target_cations)
            same_sg = int(space_group_number) == target.get_space_group_info(symprec=1e-3)[1]
            volume_ratio = (candidate.volume / len(candidate)) / (target.volume / len(target))
            linear_mismatch = 100.0 * abs(volume_ratio ** (1.0 / 3.0) - 1.0)
            # Keep chemistry-blind matches plus same-space-group, similar-metric
            # candidates that can expose a matcher false negative such as a
            # poorly reported prototype.
            if rms is None and not (same_sg and linear_mismatch <= 12.0):
                continue
            rows.append(
                {
                    "cod_id": record_id,
                    "formula": candidate.composition.reduced_formula,
                    "index_formula": formula,
                    "chemical_system": system,
                    "space_group_number": int(space_group_number),
                    "framework_rms": None if rms is None else round(float(rms[0]), 5),
                    "match_mode": "framework" if rms is not None else "metric_prototype_fallback",
                    "linear_volume_mismatch_percent": round(linear_mismatch, 3),
                    "retained_target_cations": retained,
                    "missing_target_cations": missing,
                    "extra_cations": extras,
                    "normalized_composition": {
                        key: round(value, 6) for key, value in sorted(structure_counts.items())
                    },
                }
            )

    rows.sort(
        key=lambda row: (
            len(row["missing_target_cations"]),
            row["framework_rms"] is None,
            row["framework_rms"] if row["framework_rms"] is not None else 99.0,
            row["linear_volume_mismatch_percent"],
            row["cod_id"],
        )
    )
    result = {
        "target": str(args.model.resolve()),
        "target_formula": target.composition.reduced_formula,
        "matcher": {"ltol": args.ltol, "stol": args.stol, "angle_tol": args.angle_tol},
        "direct_only": args.direct_only,
        "stoichiometric_candidates_considered": considered,
        "routes": rows,
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
