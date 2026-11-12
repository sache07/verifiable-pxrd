#!/usr/bin/env python3
"""Build and stage an initial GSAS-II refinement for the Cu-W-O pattern."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
PATTERN = ROOT / "inputs" / "pattern.csv"
XYE = ROOT / "pattern.xye"
INST = ROOT / "instrument.instprm"
GPX = ROOT / "initial.gpx"
COD_ROOT = Path(
    "<HOME>/.local/share/characterizagent/backends/dara/cod-filtered-2024/cif"
)


def cod_path(cod_id: str) -> Path:
    return COD_ROOT / cod_id[0] / cod_id[1:3] / cod_id[3:5] / f"{cod_id}.cif"


def make_xye() -> None:
    with PATTERN.open(newline="") as source, XYE.open("w") as target:
        rows = csv.DictReader(source)
        for row in rows:
            x = float(row["two_theta_deg"])
            y = float(row["intensity"])
            # No pointwise s.u.'s were supplied. Counting-statistical weights
            # are the least-assumptive approximation for raw count data.
            target.write(f"{x:.8f} {y:.8f} {math.sqrt(max(y, 1.0)):.8f}\n")


def snapshot(project: G2sc.G2Project, label: str) -> dict:
    hist = project.histogram(0)
    phases = {}
    for phase in project.phases():
        hap = phase.getHAPvalues(hist)
        phases[phase.name] = {
            "cell": phase.get_cell(),
            "scale": hap["Scale"][0],
            "scale_refine": hap["Scale"][1],
            "size": hap["Size"],
            "mustrain": hap["Mustrain"],
        }
    return {
        "label": label,
        "residuals": hist.residuals,
        "instrument": hist.InstrumentParameters,
        "sample": hist.SampleParameters,
        "background": hist.Background,
        "phases": phases,
    }


def refine(project: G2sc.G2Project, label: str, log: list[dict]) -> None:
    project.refine(makeBack=False)
    log.append(snapshot(project, label))
    print(label, json.dumps(log[-1]["residuals"], sort_keys=True))


def main() -> None:
    make_xye()
    project = G2sc.G2Project(newgpx=str(GPX))
    hist = project.add_powder_histogram(
        str(XYE), str(INST), fmthint="xye"
    )
    hist.Limits("lower", 10.0)
    hist.Limits("upper", 100.0)
    hist.set_refinements(
        {
            "Background": {
                "type": "chebyschev-1",
                "refine": True,
                "no. coeffs": 6,
                "coeffs": [1500.0, -400.0, 150.0, -50.0, 10.0, 0.0],
            }
        }
    )
    wo3 = project.add_phase(
        str(cod_path("1528915")),
        phasename="WO3_monoclinic",
        histograms=[hist],
        fmthint="CIF",
    )
    cu3wo6 = project.add_phase(
        str(cod_path("1527404")),
        phasename="Cu3WO6_cubic",
        histograms=[hist],
        fmthint="CIF",
    )

    # Keep all unused phase nuisance terms physically neutral.
    for phase in project.phases():
        phase.HAPvalue("Scale", 0.5, [hist])
        phase.setSampleProfile(hist, "size", "isotropic", 10.0, LGmix=1.0)
        phase.setSampleProfile(hist, "microstrain", "isotropic", 1.0, LGmix=1.0)
        phase.clear_HAP_refinements(
            {
                "Size": True,
                "Mustrain": True,
                "HStrain": True,
                "Pref.Ori.": True,
                "Babinet": ["BabA", "BabU"],
                "Extinction": True,
            },
            [hist],
        )
        phase.set_HAP_refinements({"Scale": True}, [hist])

    project.set_Controls("cycles", 8)
    log: list[dict] = []

    refine(project, "background_scales", log)

    # Use one angular correction only. Zero is tested first; specimen
    # displacement will be compared later under an otherwise common model.
    hist.set_refinements({"Instrument Parameters": ["Zero"]})
    refine(project, "plus_zero", log)

    wo3.set_refinements({"Cell": True})
    cu3wo6.set_refinements({"Cell": True})
    refine(project, "plus_cells", log)

    # Common nonnegative low-dimensional profile. V, Y and Z remain zero.
    hist.set_refinements({"Instrument Parameters": ["W", "X"]})
    refine(project, "plus_common_W_X", log)

    project.save(str(GPX))
    (ROOT / "initial_log.json").write_text(json.dumps(log, indent=2, default=str) + "\n")


if __name__ == "__main__":
    main()
