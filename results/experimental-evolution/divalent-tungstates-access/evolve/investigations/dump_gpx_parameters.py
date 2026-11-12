"""Read-only compact dump of refined GSAS-II profile parameters for diagnosis."""

import json
import sys

import GSASIIscriptable as G2sc


def compact_phase_parameters(parameters: dict) -> dict:
    preferred = parameters.get("Pref.Ori.", [])
    size = parameters.get("Size", [])
    strain = parameters.get("Mustrain", [])
    return {
        "Scale": parameters.get("Scale"),
        "Pref.Ori.": preferred[:4],
        "Size": size[:4],
        "Mustrain": strain[:4],
        "HStrain": parameters.get("HStrain", [])[:2],
    }


def main(path: str) -> None:
    project = G2sc.G2Project(path)
    out = {"project": path, "histograms": [], "phases": []}
    for histogram in project.histograms():
        data = histogram.data
        instrument = data.get("Instrument Parameters", [{}])[0]
        sample = data.get("Sample Parameters", {})
        background = data.get("Background", [])
        out["histograms"].append(
            {
                "name": histogram.name,
                "instrument": {
                    key: instrument.get(key)
                    for key in ["Zero", "Polariz.", "U", "V", "W", "X", "Y", "Z", "SH/L"]
                },
                "sample": {
                    key: sample.get(key)
                    for key in ["Shift", "Transparency", "SurfRoughA", "SurfRoughB"]
                },
                "background": background[0][:3] if background else None,
                "residuals": data.get("Residuals", {}),
            }
        )
    for phase in project.phases():
        data = phase.data
        out["phases"].append(
            {
                "name": phase.name,
                "cell": data.get("General", {}).get("Cell"),
                "histograms": {
                    histogram: compact_phase_parameters(parameters)
                    for histogram, parameters in data.get("Histograms", {}).items()
                },
            }
        )
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main(sys.argv[1])
