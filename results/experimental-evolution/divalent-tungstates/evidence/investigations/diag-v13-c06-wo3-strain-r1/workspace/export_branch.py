#!/usr/bin/env python3
"""Export a self-consistent researcher diagnostic from a saved GPX branch."""

import csv
import json
import shutil
from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source.gpx"
FINAL = ROOT / "final.gpx"

PHASE_OUTPUTS = (
    ("PbWO4 (scheelite)", "PbWO4", "phase_1_PbWO4.cif", "COD 9009811"),
    ("WO3 (monoclinic)", "WO3", "phase_2_WO3.cif", "COD 2311041"),
    ("Pb3O4 (minium)", "Pb3O4", "phase_3_Pb3O4.cif", "COD 9012124"),
    ("PbO (massicot)", "PbO", "phase_4_PbO.cif", "COD 2310433"),
)


shutil.copy2(SOURCE, FINAL)
project = G2sc.G2Project(str(FINAL))
h = project.histogram(0)
rv = project.data["Covariance"]["data"].get("Rvals", {})

mass = h.ComputeMassFracs()
raw = [float(mass[p.name][0]) for p in project.phases()]
esd = [float(mass[p.name][1]) for p in project.phases()]
total = sum(raw)
fractions = [value / total for value in raw]
fractions[-1] = 1.0 - sum(fractions[:-1])

phase_rows = []
for index, (phase, metadata) in enumerate(zip(project.phases(), PHASE_OUTPUTS)):
    display_name, formula, filename, source = metadata
    phase.export_CIF(str(ROOT / filename))
    cell = phase.get_cell()
    phase_rows.append({
        "name": display_name,
        "formula": formula,
        "space_group": phase.data["General"]["SGData"]["SpGrp"].strip(),
        "source_record": source,
        "cif_path": filename,
        "project_path": "final.gpx",
        "weight_fraction": fractions[index],
        "weight_fraction_esd": esd[index],
        "weight_percent": 100.0 * fractions[index],
        "cell": {
            "a_angstrom": float(cell["length_a"]),
            "b_angstrom": float(cell["length_b"]),
            "c_angstrom": float(cell["length_c"]),
            "alpha_deg": float(cell["angle_alpha"]),
            "beta_deg": float(cell["angle_beta"]),
            "gamma_deg": float(cell["angle_gamma"]),
            "volume_angstrom3": float(cell["volume"]),
        },
    })

profile = h.data["data"][0]
arrays = h.data["data"][1]
with open(ROOT / "fit.csv", "w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(("two_theta_deg", "observed_counts", "calculated_counts",
                     "difference_counts", "background_counts"))
    for x, observed, calculated, background in zip(
            arrays[0], arrays[1], arrays[3], arrays[4]):
        observed = float(observed)
        calculated = float(calculated)
        writer.writerow((f"{float(x):.8f}", f"{observed:.10g}",
                         f"{calculated:.10g}", f"{observed-calculated:.10g}",
                         f"{float(background):.10g}"))

result = {
    "project_path": "final.gpx",
    "pattern_path": "inputs/pattern.csv",
    "fit_path": "fit.csv",
    "quantification_basis": "modeled crystalline phases, normalized to 1.0",
    "phases": phase_rows,
    "fit_statistics": {
        "r_wp_percent": float(h.get_wR()),
        "r_p_percent": float(profile.get("R", float("nan"))),
        "r_exp_percent": float(profile.get("wRmin", float("nan"))),
        "goodness_of_fit": float(rv.get("GOF", float("nan"))),
        "chi_squared": float(rv.get("chisq", float("nan"))),
        "n_observations": int(rv.get("Nobs", profile.get("Nobs", 0))),
        "n_variables": int(rv.get("Nvars", 0)),
        "durbin_watson": float(profile.get("Durbin-Watson", float("nan"))),
        "converged": bool(rv.get("converged", False)),
    },
    "measurement_range_two_theta_deg": [
        float(h.data["Limits"][0][0]), float(h.data["Limits"][0][1])],
}
with open(ROOT / "result.json", "w") as stream:
    json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)

models = {}
for phase in project.phases():
    hap = phase.data["Histograms"][h.name]
    models[phase.name] = {
        "size_model": hap["Size"][0],
        "size_um": list(hap["Size"][1][:2]),
        "size_flags": list(hap["Size"][2][:2]),
        "strain": hap["Mustrain"][1][0],
        "strain_flags": list(hap["Mustrain"][2]),
        "march_ratio": hap["Pref.Ori."][1],
        "march_refine": hap["Pref.Ori."][2],
        "march_axis": list(hap["Pref.Ori."][3]),
    }
diagnostic = {
    "source": "v13 c06 four-phase p1_strain_low checkpoint",
    "operation": "export only; no refinement or parameter changes",
    "profile": {key: h.InstrumentParameters[key][1] for key in
                ("Zero", "Polariz.", "U", "V", "W", "X", "Y", "Z", "SH/L")},
    "phase_models": models,
    "result": result,
}
with open(ROOT / "diagnostic.json", "w") as stream:
    json.dump(diagnostic, stream, indent=2, sort_keys=True)

(ROOT / "report.md").write_text(
    "# v13 c06 WO3-strain checkpoint diagnostic\n\n"
    "This researcher diagnostic exports the saved `p1_strain_low.gpx` branch "
    "without further refinement or parameter changes. It tests whether v13 "
    "discarded a valid interior WO3-strain model.\n")

print(json.dumps(diagnostic, indent=2, sort_keys=True))
