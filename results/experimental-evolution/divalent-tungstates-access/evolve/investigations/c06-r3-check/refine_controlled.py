#!/usr/bin/env python3
"""Controlled staged GSAS-II refinement for the Mn-W-O three-phase model."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from GSASII import GSASIIscriptable as G2
from GSASII import GSASIIlattice as G2lat


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "inputs" / "pattern.csv"
COD_ROOT = Path(
    "<EVOLUTION_SOURCE>/runs/"
    "divalent-tungstates-access/resources/b001-c06/cif"
)


def cod_path(cod_id: str) -> Path:
    return COD_ROOT / cod_id[0] / cod_id[1:3] / cod_id[3:5] / f"{cod_id}.cif"


def set_bound(project: G2.G2Project, variable: str, low: float, high: float) -> None:
    project.set_Controls("parmMin", low, variable=variable)
    project.set_Controls("parmMax", high, variable=variable)


def write_instrument(path: Path) -> None:
    path.write_text(
        "# Cu Kalpha laboratory instrument; GSAS-II starting values\n"
        "Type:PXC;Bank:1\n"
        "Lam1:1.540598;Lam2:1.544426;I(L2)/I(L1):0.5\n"
        "Zero:-0.08128;Polariz.:0.70;Azimuth:0.0\n"
        "U:20.0;V:0.0;W:20.0;X:1.0;Y:0.0;Z:0.0;SH/L:0.03\n"
    )


def state(project: G2.G2Project, label: str) -> None:
    hist = project.histograms()[0]
    weighted = []
    rows = []
    for phase in project.phases():
        hap = phase.data["Histograms"][hist.name]
        value = phase.data["General"]["Mass"] * hap["Scale"][0]
        weighted.append(value)
        rows.append(
            {
                "name": phase.name,
                "cell": [round(v, 7) for v in phase.data["General"]["Cell"][1:7]],
                "scale": round(hap["Scale"][0], 7),
                "size": round(hap["Size"][1][0], 5),
                "strain": round(hap["Mustrain"][1][0], 3),
            }
        )
    total = sum(weighted)
    for row, value in zip(rows, weighted):
        row["fraction"] = round(value / total, 7)
    summary = {
        "label": label,
        "Rwp": hist.get_wR(),
        "instrument": {
            key: round(hist.InstrumentParameters[key][1], 7)
            for key in ("Zero", "U", "W", "X", "SH/L", "Polariz.")
        },
        "shift_um": hist.SampleParameters["Shift"][0],
        "phases": rows,
    }
    print(json.dumps(summary), flush=True)
    history = Path(project.filename).parent / "history.jsonl"
    with history.open("a") as stream:
        stream.write(json.dumps(summary) + "\n")


def run(project: G2.G2Project, label: str, cycles: int = 12) -> None:
    project.set_Controls("cycles", cycles)
    project.refine()
    project.save()
    state(project, label)


def export_profile(project: G2.G2Project) -> None:
    data = project.histograms()[0].data["data"][1]
    np.savetxt(
        Path(project.filename).parent / "profile.csv",
        np.column_stack((data[0], data[1], data[3], data[4], data[5])),
        delimiter=",",
        header="two_theta_deg,observed,calculated,background,difference",
        comments="",
    )


def main() -> None:
    output = ROOT / ".tmp" / "controlled" / "model.gpx"
    output.parent.mkdir(parents=True, exist_ok=True)
    for old in (output, output.parent / "history.jsonl"):
        if old.exists():
            old.unlink()
    instrument = output.parent / "working.instprm"
    write_instrument(instrument)

    G2.SetPrintLevel("warn")
    project = G2.G2Project(newgpx=str(output))
    sources = [
        (cod_path("1520200"), "MnWO4", 150.0),
        (cod_path("1528915"), "WO3", 10.0),
        (ROOT / ".tmp" / "candidates" / "Mn2WO5_from_Mn2AsO5.cif", "Mn2WO5", 6.0),
    ]
    phases = []
    for source, name, scale in sources:
        phase = project.add_phase(str(source), phasename=name, fmthint="CIF")
        for atom in phase.atoms():
            atom.data[atom.cia] = "I"
            atom.uiso = 0.005
            atom.refinement_flags = " "
        phases.append((phase, scale))

    hist = project.add_powder_histogram(
        str(INPUT), str(instrument), phases=[p for p, _ in phases], fmthint="comma"
    )
    hist.set_refinements(
        {
            "Limits": [9.90343322, 100.09455322],
            "Background": {
                "type": "chebyschev-1",
                "no. coeffs": 12,
                "coeffs": [1500.0] + [0.0] * 11,
                "refine": True,
            },
        }
    )
    hist.SampleParameters["Scale"] = [1.0, False]
    hist.SampleParameters["Type"] = "Bragg-Brentano"
    hist.SampleParameters["Gonio. radius"] = 200.0
    hist.SampleParameters["Shift"] = [-800.0, False]
    hist.SampleParameters["Transparency"] = [0.0, False]
    hist.SampleParameters["SurfRoughA"] = [0.0, False]
    hist.SampleParameters["SurfRoughB"] = [0.0, False]

    for phase, scale in phases:
        hap = phase.data["Histograms"][hist.name]
        hap["Scale"] = [scale, True]
        hap["Size"][0] = "isotropic"
        hap["Size"][1][0] = 0.30
        hap["Size"][2] = [False, False, False]
        hap["Mustrain"][0] = "isotropic"
        hap["Mustrain"][1][0] = 2000.0
        hap["Mustrain"][2] = [False, False, False]
        set_bound(project, f"{phase.id}:0:Scale", 0.0, 2000.0)
        reciprocal = G2lat.cell2A(phase.data["General"]["Cell"][1:7])
        for index, value in enumerate(reciprocal):
            # Maximum generated reference mismatch is 0.5% strain. A 1.2%
            # reciprocal-metric box covers this while breaking the otherwise
            # near-degeneracy between common angular offset and all cells.
            if abs(value) >= 0.005:
                low, high = sorted((0.988 * value, 1.012 * value))
            else:
                low, high = value - 0.0004, value + 0.0004
            set_bound(project, f"{phase.id}::A{index}", low, high)
        set_bound(project, f"{phase.id}:0:Size;i", 0.04, 1.5)
        set_bound(project, f"{phase.id}:0:Mustrain;i", 0.0, 8000.0)

    set_bound(project, ":0:Zero", -0.25, 0.25)
    set_bound(project, ":0:Shift", -800.0, 800.0)
    for key, low, high in (
        ("U", 0.0, 40.0),
        ("W", 2.0, 40.0),
        ("X", 0.1, 6.0),
        ("SH/L", 0.005, 0.10),
        ("Polariz.", 0.5, 1.0),
    ):
        set_bound(project, f":0:{key}", low, high)
    project.save()

    run(project, "scales and background", 15)

    for phase, _ in phases:
        phase.set_refinements({"Cell": True})
    run(project, "cells at fixed calibration", 20)
    for phase, _ in phases:
        phase.clear_refinements({"Cell": True})

    hist.set_refinements({"Instrument Parameters": ["Zero"]})
    run(project, "zero only", 12)
    hist.clear_refinements({"Instrument Parameters": ["Zero"]})
    hist.set_refinements({"Sample Parameters": ["Shift"]})
    run(project, "displacement only", 12)
    hist.clear_refinements({"Sample Parameters": ["Shift"]})

    for phase, _ in phases:
        phase.set_refinements({"Cell": True})
    run(project, "cells after calibration", 15)
    for phase, _ in phases:
        phase.clear_refinements({"Cell": True})

    hist.set_refinements({"Instrument Parameters": ["U", "W", "X", "SH/L"]})
    run(project, "shared profile", 20)
    hist.clear_refinements({"Instrument Parameters": ["U", "W", "X", "SH/L"]})

    for phase, _ in phases:
        phase.set_HAP_refinements(
            {"Mustrain": {"type": "isotropic", "refine": True}}
        )
    run(project, "phase microstrain", 18)
    for phase, _ in phases:
        phase.clear_HAP_refinements({"Mustrain": True})

    for phase, _ in phases:
        phase.set_HAP_refinements(
            {"Size": {"type": "isotropic", "value": 0.30, "refine": True}}
        )
    run(project, "phase size", 18)
    for phase, _ in phases:
        phase.clear_HAP_refinements({"Size": True})

    # One final position/profile alternation after widths are close.
    for phase, _ in phases:
        phase.set_refinements({"Cell": True})
    hist.set_refinements({"Instrument Parameters": ["Zero"]})
    run(project, "cells and zero final", 15)
    for phase, _ in phases:
        phase.clear_refinements({"Cell": True})
    hist.clear_refinements({"Instrument Parameters": ["Zero"]})
    export_profile(project)


if __name__ == "__main__":
    main()
