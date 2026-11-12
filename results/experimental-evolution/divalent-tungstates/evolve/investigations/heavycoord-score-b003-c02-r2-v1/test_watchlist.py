#!/usr/bin/env python3
"""Re-challenge plausible weak phases under the clean common profile."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
COD_ROOT = Path(
    "<HOME>/.local/share/characterizagent/backends/dara/cod-filtered-2024/cif"
)
BASE = ROOT / "wo3_record_2311041.gpx"


def cod_path(cod_id: str) -> Path:
    return COD_ROOT / cod_id[0] / cod_id[1:3] / cod_id[3:5] / f"{cod_id}.cif"


CANDIDATES = {
    "CuO_196K_9016057": cod_path("9016057"),
    "CuO_ambient_1011194": cod_path("1011194"),
    "CuWO4_ambient_prototype": ROOT / "candidates" / "cuwo4_ambient_prototype.cif",
    "CuWO4_HP_P-1_4000806": cod_path("4000806"),
    "CuWO4_HP_P2c_4000807": cod_path("4000807"),
}


def main() -> None:
    for name, cif in CANDIDATES.items():
        output = ROOT / f"watch_{name}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        phase = project.add_phase(
            str(cif), phasename=name, histograms=[hist], fmthint="CIF"
        )
        phase.HAPvalue("Scale", 0.02, [hist])
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
        project.set_Controls("cycles", 10)
        try:
            project.refine(makeBack=False)
            project.save()
            scale = phase.HAPvalue("Scale")
            print(
                name,
                "wR", hist.get_wR(),
                "scale", scale,
                "cell", phase.get_cell(),
                "mass", hist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(name, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
