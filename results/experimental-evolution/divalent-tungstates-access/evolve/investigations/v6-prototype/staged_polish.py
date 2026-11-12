#!/usr/bin/env python3
"""Branch a complete GSAS-II model through bounded coordinate sequences.

Usage (including the controller procedure-test interface):
    staged_polish.py INPUT.gpx OUTPUT.gpx INPUTS_DIR

The script is deliberately chemistry-agnostic. It never adds, removes, or
renames phases and does not select reference structures. It compares three
refinement paths from the supplied complete physical checkpoint, limits every
atomic coordinate component to a small Cartesian-equivalent neighborhood of
that checkpoint, and returns a materially better replayable branch only when
relative geometry and phase fractions remain stable. The caller remains
responsible for a final geometry review and for re-exporting CIFs, fractions,
and fit.csv.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import sys
import traceback

from GSASII import GSASIIscriptable as G2
from GSASII import GSASIIlattice as G2lat
from GSASII import GSASIIstrMain as G2st


COORDINATE_WINDOW_ANGSTROM = 0.10
CELL_METRIC_FRACTION = 0.01
CELL_SHEAR_MINIMUM_SPAN = 0.0003
MAX_PAIR_CONTRACTION_ANGSTROM = 0.18
MINIMUM_FRACTION_RATIO = 0.25
MINIMUM_RWP_GAIN_PERCENT = 0.02
MAXIMUM_SHIFT_ESD = 1.0
MAXIMUM_COORDINATE_STABILIZATION_PASSES = 3
MAXIMUM_SETTLE_PASSES = 3
COORDINATE_VARIABLE = re.compile(r"^(\d+)::dA[xyz]:(\d+)$")


def histogram(project):
    """Choose the populated powder histogram in a normal solver project."""
    histograms = project.histograms()
    if not histograms:
        raise RuntimeError("project contains no powder histogram")
    return max(histograms, key=lambda item: len(item.data.get("data", [[], []])[1]))


def clear_flags(project) -> None:
    """Freeze nuisance and structural flags while retaining their values."""
    hist = histogram(project)
    hist.Background[0][1] = False
    for value in hist.InstrumentParameters.values():
        if isinstance(value, list) and len(value) > 2:
            value[2] = False
    for value in hist.SampleParameters.values():
        if isinstance(value, list) and len(value) > 1 and isinstance(value[1], bool):
            value[1] = False

    for phase in project.phases():
        try:
            phase.clear_refinements({"Cell": True})
        except Exception:
            pass
        phase.set_refinements({"LeBail": False})
        for atom in phase.atoms():
            atom.refinement_flags = " "
        hap = phase.data["Histograms"].get(hist.name)
        if not hap:
            continue
        if isinstance(hap.get("Scale"), list) and len(hap["Scale"]) > 1:
            hap["Scale"][1] = False
        for key in ("Size", "Mustrain"):
            value = hap.get(key)
            if isinstance(value, list) and len(value) > 2 and isinstance(value[2], list):
                value[2] = [False] * len(value[2])
            if isinstance(value, list) and len(value) > 5 and isinstance(value[5], list):
                value[5] = [False] * len(value[5])
        value = hap.get("Pref.Ori.")
        if isinstance(value, list) and len(value) > 2:
            value[2] = False
        value = hap.get("HStrain")
        if isinstance(value, list) and len(value) > 1 and isinstance(value[1], list):
            value[1] = [False] * len(value[1])
        value = hap.get("Extinction")
        if isinstance(value, list) and len(value) > 1:
            value[1] = False
        value = hap.get("Babinet")
        if isinstance(value, dict):
            for parameter in value.values():
                if isinstance(parameter, list) and len(parameter) > 1:
                    parameter[1] = False

    controls = project.data.get("Controls", {}).get("data", {})
    controls["parmFrozen"] = {"FrozenList": []}


def reset_limits(project) -> None:
    """Remove stale bounds inherited from the solver's earlier branches."""
    controls = project.data["Controls"]["data"]
    controls["parmMinDict"] = {}
    controls["parmMaxDict"] = {}
    controls["parmFrozen"] = {"FrozenList": []}


def clear_frozen(project) -> None:
    project.data["Controls"]["data"]["parmFrozen"] = {"FrozenList": []}


def install_bounds(project) -> None:
    """Install only the scale, cell and coordinate limits used here."""
    project.index_ids()
    for phase in project.phases():
        cell = phase.get_cell()
        lengths = [float(cell["length_a"]), float(cell["length_b"]), float(cell["length_c"])]
        pid = phase.data["pId"]
        hist = histogram(project)
        hap = phase.data["Histograms"].get(hist.name)
        if hap and isinstance(hap.get("Scale"), list):
            scale = max(float(hap["Scale"][0]), 0.0)
            project.set_Controls(
                "parmMin", max(scale * MINIMUM_FRACTION_RATIO, 0.0),
                variable=f"{pid}:0:Scale",
            )
            project.set_Controls(
                "parmMax", max(scale * 5.0, 1.0), variable=f"{pid}:0:Scale"
            )

        reciprocal = G2lat.cell2A([
            cell["length_a"], cell["length_b"], cell["length_c"],
            cell["angle_alpha"], cell["angle_beta"], cell["angle_gamma"],
        ])
        for index, value in enumerate(reciprocal):
            value = float(value)
            span = max(
                CELL_METRIC_FRACTION * abs(value), CELL_SHEAR_MINIMUM_SPAN
            )
            project.set_Controls(
                "parmMin", value - span, variable=f"{pid}::A{index}"
            )
            project.set_Controls(
                "parmMax", value + span, variable=f"{pid}::A{index}"
            )

        for index, atom in enumerate(phase.atoms()):
            for axis, value, length in zip("xyz", atom.coordinates, lengths):
                half_width = COORDINATE_WINDOW_ANGSTROM / max(length, 1.0e-6)
                variable = f"{pid}::dA{axis}:{index}"
                project.set_Controls("parmMin", float(value) - half_width, variable=variable)
                project.set_Controls("parmMax", float(value) + half_width, variable=variable)


def mass_fractions(project) -> dict[str, float]:
    """Return crystalline mass fractions, including before covariance exists."""
    hist = histogram(project)
    try:
        values = hist.ComputeMassFracs()
    except (KeyError, TypeError, ValueError):
        values = {}
    if values:
        return {
            str(name): float(value[0])
            for name, value in values.items()
        }

    # ComputeMassFracs requires a saved covariance matrix only to propagate
    # uncertainties.  The fractions themselves are normalized phase
    # scale*formula-mass products (GSASIIstrMath.calcMassFracs).  Some valid
    # solver checkpoints intentionally omit covariance, so use that same
    # value calculation as a covariance-free fallback.
    weighted = {}
    for phase in project.phases():
        general = phase.data.get("General", {})
        hap = phase.data.get("Histograms", {}).get(hist.name)
        if not hap or not hap.get("Use", True):
            continue
        if general.get("Type") == "magnetic" or general.get("doPawley"):
            continue
        scale = hap.get("Scale", [0.0])[0]
        weighted[str(phase.name)] = max(
            0.0, float(general.get("Mass", 0.0)) * float(scale)
        )
    total = sum(weighted.values())
    if total <= 0.0:
        raise RuntimeError("cannot compute positive crystalline mass fractions")
    return {name: value / total for name, value in weighted.items()}


def convergence_state(project) -> dict:
    rvals = (
        project.data.get("Covariance", {}).get("data", {}).get("Rvals", {})
    )
    maximum = rvals.get("Max shft/sig")
    return {
        "converged": bool(rvals.get("converged", False)),
        "max_shift_esd": None if maximum is None else float(maximum),
        "frozen": list(project.get_Frozen()),
    }


def checkpoint_coordinates(project) -> dict[tuple[int, int], tuple[float, float, float]]:
    coordinates = {}
    for phase in project.phases():
        pid = int(phase.data["pId"])
        for index, atom in enumerate(phase.atoms()):
            coordinates[(pid, index)] = tuple(float(item) for item in atom.coordinates)
    return coordinates


def frozen_coordinate_atoms(record: dict) -> set[tuple[int, int]]:
    atoms = set()
    for variable in record.get("frozen", []):
        match = COORDINATE_VARIABLE.match(str(variable))
        if match:
            atoms.add((int(match.group(1)), int(match.group(2))))
    return atoms


def record_is_converged(record: dict) -> bool:
    maximum = record.get("max_shift_esd")
    return bool(record.get("converged")) and maximum is not None and maximum <= MAXIMUM_SHIFT_ESD


def geometry_profile(project) -> dict[str, dict]:
    """Record broad-neighbor minimum distances for relative branch checks."""
    profile = {}
    for index, phase in enumerate(project.phases()):
        controls, data = phase.InitDisAgl(False)
        controls["Factors"] = [1.25, 0.0]
        _, distances, _ = G2st.RetDistAngle(controls, data, dmin=0.01)
        atoms = phase.atoms()
        pair_minima: dict[str, float] = {}
        for center, rows in distances.items():
            for row in rows:
                other = int(row[0])
                pair = "-".join(sorted((atoms[center].element, atoms[other].element)))
                distance = float(row[-2])
                pair_minima[pair] = min(pair_minima.get(pair, distance), distance)
        key = f"{index}:{phase.name}"
        profile[key] = {
            "pair_min_A": pair_minima,
            "catastrophic_contacts": [
                [str(left), str(right), float(distance)]
                for left, right, distance in phase.ShortDistances(useAll=False)
            ],
        }
    return profile


def branch_audit(project, baseline_geometry, baseline_fractions, records) -> dict:
    geometry = geometry_profile(project)
    fractions = mass_fractions(project)
    violations = []
    for phase_key, phase_geometry in geometry.items():
        if phase_geometry["catastrophic_contacts"]:
            violations.append({
                "type": "catastrophic_contact",
                "phase": phase_key,
                "contacts": phase_geometry["catastrophic_contacts"],
            })
        source_pairs = baseline_geometry.get(phase_key, {}).get("pair_min_A", {})
        for pair, distance in phase_geometry["pair_min_A"].items():
            if pair not in source_pairs:
                continue
            contraction = float(source_pairs[pair]) - float(distance)
            if contraction > MAX_PAIR_CONTRACTION_ANGSTROM:
                violations.append({
                    "type": "pair_contraction",
                    "phase": phase_key,
                    "pair": pair,
                    "source_A": float(source_pairs[pair]),
                    "branch_A": float(distance),
                    "contraction_A": contraction,
                })
    for phase, source_fraction in baseline_fractions.items():
        branch_fraction = fractions.get(phase, 0.0)
        if source_fraction >= 0.01 and branch_fraction < source_fraction * MINIMUM_FRACTION_RATIO:
            violations.append({
                "type": "fraction_collapse",
                "phase": phase,
                "source_fraction": source_fraction,
                "branch_fraction": branch_fraction,
            })
    coordinate_records = [item for item in records if item.get("kind") == "coordinates"]
    if not coordinate_records or not record_is_converged(coordinate_records[-1]):
        violations.append({
            "type": "coordinate_nonconvergence",
            "record": coordinate_records[-1] if coordinate_records else None,
        })
    elif frozen_coordinate_atoms(coordinate_records[-1]):
        violations.append({
            "type": "coordinate_bounds",
            "record": coordinate_records[-1],
        })
    settle_records = [item for item in records if item.get("kind") == "settle"]
    if not settle_records or not record_is_converged(settle_records[-1]):
        violations.append({
            "type": "settle_nonconvergence",
            "record": settle_records[-1] if settle_records else None,
        })
    elif settle_records[-1].get("frozen"):
        violations.append({
            "type": "settle_bounds",
            "record": settle_records[-1],
        })
    return {
        "eligible": not violations,
        "fractions": fractions,
        "geometry": geometry,
        "violations": violations,
    }


def enable_scales_and_background(project) -> None:
    hist = histogram(project)
    hist.Background[0][1] = True
    for phase in project.phases():
        hap = phase.data["Histograms"].get(hist.name)
        if hap and isinstance(hap.get("Scale"), list) and len(hap["Scale"]) > 1:
            hap["Scale"][1] = True


def set_atoms(phase, predicate) -> None:
    for atom in phase.atoms():
        atom.refinement_flags = "X" if predicate(atom) else " "


def set_all_atoms(project, predicate) -> None:
    for phase in project.phases():
        set_atoms(phase, predicate)


def is_oxygen(atom) -> bool:
    return atom.element.strip().upper() in {"O", "O-2"}


def run(
    project, stage: str, records: list[dict], cycles: int,
    kind: str = "other",
) -> float:
    clear_frozen(project)
    project.set_Controls("cycles", cycles)
    project.save()
    project.refine(makeBack=False)
    project.save()
    hist = histogram(project)
    wr = float(hist.get_wR())
    state = convergence_state(project)
    records.append({
        "stage": stage,
        "kind": kind,
        "Rwp_percent": wr,
        "fractions": mass_fractions(project),
        **state,
    })
    print(json.dumps(records[-1]), flush=True)
    return wr


def settle(project, records: list[dict]) -> float:
    wr = float(histogram(project).get_wR())
    for pass_index in range(MAXIMUM_SETTLE_PASSES):
        clear_flags(project)
        enable_scales_and_background(project)
        for phase in project.phases():
            phase.set_refinements({"Cell": True})
        wr = run(
            project, f"cell_scale_background_settle_{pass_index + 1}",
            records, 6, kind="settle",
        )
        if record_is_converged(records[-1]) and not records[-1]["frozen"]:
            break
    clear_flags(project)
    project.save()
    return wr


def stabilize_coordinates(project, records, source_coordinates) -> set[tuple[int, int]]:
    """Roll bound-hit atoms back, then converge the remaining interior sites."""
    excluded: set[tuple[int, int]] = set()
    for pass_index in range(MAXIMUM_COORDINATE_STABILIZATION_PASSES):
        previous = records[-1]
        excluded.update(frozen_coordinate_atoms(previous))
        for phase in project.phases():
            pid = int(phase.data["pId"])
            for index, atom in enumerate(phase.atoms()):
                key = (pid, index)
                if key in excluded:
                    atom.coordinates = source_coordinates[key]

        if record_is_converged(previous) and not frozen_coordinate_atoms(previous):
            break

        clear_flags(project)
        enable_scales_and_background(project)
        active = 0
        for phase in project.phases():
            pid = int(phase.data["pId"])
            for index, atom in enumerate(phase.atoms()):
                atom.refinement_flags = " " if (pid, index) in excluded else "X"
                active += int(bool(atom.refinement_flags.strip()))
        if not active:
            break
        run(
            project, f"interior_coordinate_settle_{pass_index + 1}",
            records, 8, kind="coordinates",
        )
    return excluded


def branch_all(project, records: list[dict], source_coordinates) -> float:
    set_all_atoms(project, lambda atom: True)
    run(project, "all_coordinates", records, 10, kind="coordinates")
    stabilize_coordinates(project, records, source_coordinates)
    return settle(project, records)


def branch_heavy_light(project, records: list[dict], source_coordinates) -> float:
    set_all_atoms(project, lambda atom: not is_oxygen(atom))
    run(project, "all_heavy_coordinates", records, 8, kind="coordinates")
    set_all_atoms(project, is_oxygen)
    run(project, "all_oxygen_coordinates", records, 8, kind="coordinates")
    set_all_atoms(project, lambda atom: True)
    run(project, "joint_coordinate_settle", records, 6, kind="coordinates")
    stabilize_coordinates(project, records, source_coordinates)
    return settle(project, records)


def branch_phasewise(project, records: list[dict], source_coordinates) -> float:
    for index, phase in enumerate(project.phases()):
        set_all_atoms(project, lambda atom: False)
        set_atoms(phase, lambda atom: not is_oxygen(atom))
        run(
            project, f"phase_{index}_heavy_coordinates", records, 6,
            kind="coordinates",
        )
        set_all_atoms(project, lambda atom: False)
        set_atoms(phase, is_oxygen)
        run(
            project, f"phase_{index}_oxygen_coordinates", records, 6,
            kind="coordinates",
        )
    set_all_atoms(project, lambda atom: True)
    run(project, "joint_coordinate_settle", records, 6, kind="coordinates")
    stabilize_coordinates(project, records, source_coordinates)
    return settle(project, records)


def load_branch(source: Path, destination: Path):
    project = G2.G2Project(gpxfile=str(source), newgpx=str(destination))
    clear_flags(project)
    reset_limits(project)
    install_bounds(project)
    enable_scales_and_background(project)
    project.save()
    return project


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: staged_polish.py INPUT.gpx OUTPUT.gpx INPUTS_DIR")
    source = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    # INPUTS_DIR is accepted for the package/procedure interface. This helper
    # intentionally needs no case metadata or lookup table.
    Path(sys.argv[3]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    work = output.parent / f".{output.stem}_staged_polish"
    work.mkdir(parents=True, exist_ok=True)

    G2.SetPrintLevel("error")
    summary = {
        "source": str(source),
        "settings": {
            "coordinate_window_A_per_axis": COORDINATE_WINDOW_ANGSTROM,
            "cell_metric_fraction": CELL_METRIC_FRACTION,
            "maximum_pair_contraction_A": MAX_PAIR_CONTRACTION_ANGSTROM,
            "minimum_fraction_ratio": MINIMUM_FRACTION_RATIO,
            "minimum_Rwp_gain_percent": MINIMUM_RWP_GAIN_PERCENT,
            "maximum_shift_esd": MAXIMUM_SHIFT_ESD,
        },
        "branches": [],
    }
    baseline_path = work / "baseline.gpx"
    baseline_project = load_branch(source, baseline_path)
    baseline_rwp = float(histogram(baseline_project).get_wR())
    baseline_geometry = geometry_profile(baseline_project)
    baseline_fractions = mass_fractions(baseline_project)
    clear_flags(baseline_project)
    baseline_project.save()
    candidates = [(baseline_rwp, baseline_path, "baseline")]
    summary["branches"].append({
        "name": "baseline",
        "Rwp_percent": baseline_rwp,
        "status": "complete",
        "eligible": True,
        "fractions": baseline_fractions,
        "geometry": baseline_geometry,
    })

    for name, operation in (
        ("all", branch_all),
        ("heavy_light", branch_heavy_light),
        ("phasewise", branch_phasewise),
    ):
        branch_path = work / f"{name}.gpx"
        records: list[dict] = []
        try:
            project = load_branch(source, branch_path)
            source_coordinates = checkpoint_coordinates(project)
            wr = operation(project, records, source_coordinates)
            project.save()
            audit = branch_audit(
                project, baseline_geometry=baseline_geometry,
                baseline_fractions=baseline_fractions,
                records=records,
            )
            if audit["eligible"]:
                candidates.append((wr, branch_path, name))
            summary["branches"].append({
                "name": name,
                "Rwp_percent": wr,
                "status": "complete",
                "stages": records,
                **audit,
            })
        except Exception as exc:
            summary["branches"].append({
                "name": name,
                "status": "failed",
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "stages": records,
            })
            print(json.dumps({"branch": name, "error": str(exc)}), flush=True)

    best_rwp, best_path, best_name = min(candidates, key=lambda item: item[0])
    if baseline_rwp - best_rwp < MINIMUM_RWP_GAIN_PERCENT:
        best_rwp, best_path, best_name = baseline_rwp, baseline_path, "baseline"
    shutil.copy2(best_path, output)
    summary["selected"] = {
        "name": best_name,
        "Rwp_percent": best_rwp,
        "output": str(output),
    }
    output.with_suffix(".staged_polish.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary["selected"]), flush=True)


if __name__ == "__main__":
    main()
