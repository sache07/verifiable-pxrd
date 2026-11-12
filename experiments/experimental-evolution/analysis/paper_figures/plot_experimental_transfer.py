"""Build experimental-transfer figures and tables from frozen evaluation records.

Default: python scripts/plot_experimental_transfer.py
Refresh the compact inputs from the adjacent research repositories:
  python scripts/plot_experimental_transfer.py --refresh-inputs --workspace /path/to/workspace --replay-results /path/to/replay-results

No solver or refinement is run. Requires numpy and matplotlib. PG profiles are
rescored exported curves, not independently regenerated atomic refinements.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / "results/experimental-eval/divalent-tungstates-PG15/paper-data/experimental_transfer"
TABLES = Path(os.environ.get("PXRD_RELEASE_OUTPUT", ROOT / ".runs/multiphase-reproduction")) / "tables"
FIGURES = Path(os.environ.get("PXRD_RELEASE_OUTPUT", ROOT / ".runs/multiphase-reproduction")) / "figures"
RUNS = {
    "P0": "pxrd-sol-max-p0-eval15-repeat2-20261019",
    "E": "pxrd-eval15-v6nov-20261104",
    "F": "pxrd-pg15-framework-access-20261105",
    "FE": "pxrd-pg15-fwaccess-evolved-20261109",
    "Fv5": "pxrd-pg15-fwaccess-v5-20261109",
}
COLORS = {"PG": "#008575", "P0": "#466682", "E": "#CE6C28"}
LABELS = {"PG": "Deposited PG", "P0": "Baseline", "E": "Evolved v6"}
CONDITION_LABELS = {**LABELS, "F": "Framework access", "FE": "Framework + v6", "Fv5": "Evolved framework v5"}


def rwp(y, prediction):
    weights = 1 / np.maximum(y, 1)
    return float(100 * np.sqrt(np.sum(weights * (y-prediction)**2) / np.sum(weights * y**2)))


def refresh_inputs(workspace, replay_results):
    raw = workspace / "verifiable-pxrd-raw/results/experimental-eval/divalent-tungstates-PG15"
    bench = workspace / "verifiable-pxrd/pxrd-bench/divalent-tungstates-PG15"
    provenance = {}

    def remember(path):
        provenance[str(path.relative_to(workspace))] = hashlib.sha256(path.read_bytes()).hexdigest()
        return path

    def read(path):
        return json.loads(remember(path).read_text())

    metadata = read(bench / "case-metadata.json")
    references = read(raw / RUNS["E"] / "references/ceder_summary.json")["cases"]
    cases = {m["case"]: {"case": m["case"], "precursors": m["precursors"],
                          "temperature_C": m["temperature_C"]} for m in metadata}
    for row in references:
        cases[row["case"]]["pg_phases"] = row["ceder_phases"]
    panels = {}
    for key, run in RUNS.items():
        rows = read(replay_results / key / "per_attempt.json")
        panels[key] = rows
        for row in rows:
            case = cases[row["case"]]
            reference_rwp = row["ceder_interior_rwp"]
            if "pg_rwp" in case:
                assert abs(case["pg_rwp"] - reference_rwp) < 1e-9
            case["pg_rwp"] = reference_rwp
            verified = (row.get("replay") or {}).get("status") == "verified"
            case.setdefault("attempts", {}).setdefault(key, []).append({
                "id": row["id"], "replicate": row["replicate"], "verified": verified,
                "rwp": row.get("replay_interior_rwp") if verified else None,
                "minutes": row.get("minutes"),
                "background_terms": len(row["replay"]["background_coefficients"]),
                "shl": row["replay"]["instrument"]["SH/L"][1],
                "phases": [{k: p.get(k) for k in ("formula", "weight_fraction", "space_group", "target_matches")}
                           for p in row.get("phases", [])],
            })
    opus = raw / "pxrd-opus-p0-eval15-20261019/report/OPUS5_R1_COMPARISON.csv"
    with remember(opus).open() as handle:
        for row in csv.DictReader(handle):
            cases[row["case"]]["opus_rwp"] = float(row["opus5_rwp_secondary"])

    # Median-residual attempts are chosen for the Cu illustration, not the best fits.
    selected = {}
    curves = {}
    for key in ("P0", "E"):
        valid = sorted((r for r in panels[key] if r["case"] == "case-006"
                        and (r.get("replay") or {}).get("status") == "verified"),
                       key=lambda r: r["replay_interior_rwp"])
        assert len(valid) == 3
        row = valid[1]
        path = replay_results / key / "attempts" / row["id"] / "project_replay/prediction.npz"
        array = np.load(remember(path))
        mask = (array["x"] >= 10.1) & (array["x"] <= 99.9)
        x, observed, predicted = (array[k][mask] for k in ("x", "observed", "predicted"))
        assert abs(rwp(observed, predicted) - row["replay_interior_rwp"]) < 1e-4
        if curves:
            assert np.allclose(x, curves["x"], atol=1e-7, rtol=0)
            assert np.allclose(observed, curves["observed"], atol=1e-7, rtol=0)
        curves.update(x=x, observed=observed)
        curves[key] = predicted
        selected[key] = row["replicate"]
    ref = read(bench / "references/case-006-reference-data.json")["plot_data"]
    assert min(ref["x"]) <= curves["x"][0] < curves["x"][-1] <= max(ref["x"])
    curves["PG"] = np.interp(curves["x"], ref["x"], ref["y_calc"])
    assert abs(rwp(curves["observed"], curves["PG"]) - cases["case-006"]["pg_rwp"]) < 1e-8
    DATA.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(DATA / "cu_profiles.npz", **curves)
    payload = {"cases": [cases[k] for k in sorted(cases)], "cu_selected_replicates": selected,
               "residual_definition": "100 sqrt(sum((observed-predicted)^2/max(observed,1))/sum(observed^2/max(observed,1))); 10.1--99.9 degrees",
               "opus_note": "One Claude Opus 5 high-effort attempt per scan; Claude Code; secondary 1e-6 degree grid tolerance.",
               "provenance_sha256": provenance}
    (DATA / "records.json").write_text(json.dumps(payload, indent=2) + "\n")


def values(case, key):
    return [r["rwp"] for r in case["attempts"][key] if r["rwp"] is not None]


def refresh_model_comparison(workspace):
    """Freeze the older high-effort comparison, checked against saved replays."""
    raw = workspace / "verifiable-pxrd-raw/results/experimental-eval/divalent-tungstates-PG15"
    opus = raw / "pxrd-opus-p0-eval15-20261019"
    csv_path = opus / "report/OPUS5_R1_COMPARISON.csv"
    master_path = opus / "checks/eval15_all/master.json"
    status_path = raw / "pxrd-matched-p0-eval15-20261007/analysis/status.json"
    replacement_path = opus / "analysis/attempts/P0-exp-case-015-r3-replacement/result.json"
    cancelled_path = opus / "secondary_gridtol/analysis/attempts/P0-exp-case-015-r3/result.json"
    master = json.loads(master_path.read_text())
    jobs = json.loads(status_path.read_text())["jobs"]
    assert len(jobs) == 45 and all(j["model"] == "gpt-5.6-sol" and j["effort"] == "high" for j in jobs)
    high = [r for r in master if r["experiment"] == "pxrd-matched-p0-eval15-20261007"]
    other = [r for r in master if r["condition"] == "Opus 5"]
    assert len(high) == 45 and len(other) == 15
    cases = []
    with csv_path.open() as handle:
        for row in csv.DictReader(handle):
            scores = [float(row[f"sol_r{r}"]) for r in (1, 2, 3)]
            attempts = []
            for rep, score in enumerate(scores, 1):
                saved = next(r for r in high if r["case"] == row["case"] and r["id"].endswith(f"-r{rep}"))
                replacement = row["case"] == "case-015" and rep == 3
                if replacement:
                    cancelled = json.loads(cancelled_path.read_text())
                    assert cancelled["execution_status"] == "cancelled_by_user"
                    result = json.loads(replacement_path.read_text())
                    assert result["replay"]["status"] == "verified"
                    saved = {"id": result["id"], "primary_status": "verified", "basis": "replay",
                             "rwp": result["replay_interior_rwp"], "minutes": result["minutes"]}
                assert saved["primary_status"] == "verified" and saved["basis"] == "replay"
                assert abs(saved["rwp"] - score) < 1e-10
                attempts.append({"id": saved["id"], "replicate": rep, "rwp": score,
                                 "minutes": saved["minutes"], "verified": True,
                                 "replacement_for_cancelled": replacement})
            saved_opus = next(r for r in other if r["case"] == row["case"])
            assert abs(saved_opus["rwp"] - float(row["opus5_rwp_secondary"])) < 1e-10
            cases.append({"case": row["case"], "sol_high": attempts,
                          "opus_rwp": saved_opus["rwp"], "opus_minutes": float(row["opus5_minutes"]),
                          "opus_segments": int(row["opus5_segments"])})
    payload = {"cases": cases,
               "sol_high_note": "gpt-5.6-sol/high, Codex 0.154, 45 attempts; no solver time limit; original-data project replay.",
               "opus_note": "claude-opus-5/high, Claude Code 2.1.299, 15 attempts; 1e-6 degree grid tolerance; resumed sessions retained.",
               "replacement_note": "The previously reported comparison replaces user-cancelled case-015 r3 with the saved P0-exp-case-015-r3-replacement from the October 8 run.",
               "provenance_sha256": {str(p.relative_to(workspace)): hashlib.sha256(p.read_bytes()).hexdigest()
                                     for p in (csv_path, master_path, status_path, replacement_path, cancelled_path)}}
    (DATA / "model_comparison.json").write_text(json.dumps(payload, indent=2) + "\n")


def validate(data):
    """Check denominators, frozen profile metrics, and the comparisons in the text."""
    cases = data["cases"]
    assert len(cases) == 15
    assert {c["case"] for c in cases} == {f"case-{i:03d}" for i in range(1, 16)}
    for key in RUNS:
        for c in cases:
            rows = c["attempts"][key]
            assert len(rows) == 3 and {r["replicate"] for r in rows} == {1, 2, 3}
            for row in rows:
                assert row["verified"] == (row["rwp"] is not None)
                assert row["rwp"] is None or (np.isfinite(row["rwp"]) and row["rwp"] >= 0)
        assert sum(len(values(c, key)) for c in cases) == 45
    assert sum(np.mean(values(c, "E")) < np.mean(values(c, "P0")) for c in cases) == 10
    assert sum(np.mean(values(c, "E")) < c["pg_rwp"] for c in cases) == 13
    expected = {"P0": 7.89888288683027, "E": 6.708885087581412,
                "F": 5.9788635963485985, "FE": 6.487135387702234,
                "Fv5": 6.441630701124566}
    for key, mean in expected.items():
        assert np.isclose(np.mean([np.mean(values(c, key)) for c in cases]), mean, rtol=0, atol=1e-10)
    assert np.isclose(np.mean([c["pg_rwp"] for c in cases]), 12.592498682254469)
    assert np.isclose(np.mean([c["opus_rwp"] for c in cases]), 6.32201800356158)
    cu = next(c for c in cases if c["case"] == "case-006")
    arr = np.load(DATA / "cu_profiles.npz")
    assert np.all(np.diff(arr["x"]) > 0)
    assert arr["x"][0] >= 10.1 and arr["x"][-1] <= 99.9
    for key in COLORS:
        expected_rwp = cu["pg_rwp"] if key == "PG" else next(
            r["rwp"] for r in cu["attempts"][key]
            if r["replicate"] == data["cu_selected_replicates"][key])
        assert np.isclose(rwp(arr["observed"], arr[key]), expected_rwp, rtol=0, atol=1e-4)


def phase_weights(case, key, formula, structural=False):
    return [100 * sum((p.get("weight_fraction") or 0) for p in r["phases"]
                     if ((p.get("target_matches") or {}).get(formula, False) if structural else p["formula"] == formula))
            for r in case["attempts"][key]]


def chem(text):
    import re
    return re.sub(r"(\d+)", r"$_{\1}$", text)


def table_macro(filename, name, rows):
    (TABLES / filename).write_text(
        "% Generated by scripts/plot_experimental_transfer.py.\n"
        + "\\newcommand{\\" + name + "}{%\n" + "\n".join(rows) + "\n}\n")


def tables(data):
    TABLES.mkdir(parents=True, exist_ok=True)
    cases = data["cases"]
    model_cases = {r["case"]: r for r in json.loads((DATA / "model_comparison.json").read_text())["cases"]}
    assert len(model_cases) == 15
    for case in cases:
        model = model_cases[case["case"]]
        assert len(model["sol_high"]) == 3 and all(a["verified"] for a in model["sol_high"])
        assert abs(model["opus_rwp"] - case["opus_rwp"]) < 1e-10
    assert np.isclose(np.mean([a["rwp"] for m in model_cases.values() for a in m["sol_high"]]), 8.976938725561068)
    pg = [c["pg_rwp"] for c in cases]
    primary = [f"Deposited PG & {np.mean(pg):.2f} & {np.median(pg):.2f} & \\textemdash & \\textemdash & \\textemdash \\\\"]
    for key in ("P0", "E"):
        repeats = np.asarray([values(c, key) for c in cases])
        assert repeats.shape == (15, 3)
        means = repeats.mean(axis=1)
        best_of_three = repeats.min(axis=1).mean()
        within_scan_sd = repeats.std(axis=1, ddof=1).mean()
        attempts = [r for c in cases for r in c["attempts"][key]]
        minutes = np.mean([r["minutes"] for r in attempts])
        primary.append(f"{LABELS[key]} & {np.mean(means):.2f} & {np.median(means):.2f} & {best_of_three:.2f} & {within_scan_sd:.2f} & {minutes:.1f} \\\\")
    table_macro("primary_rows.tex", "experimentalTransferPrimaryRows", primary)

    lines = []
    for i, c in enumerate(cases):
        if i:
            lines.append(r"\addlinespace[3pt]")
        minima = {key: min(values(c, key)) for key in RUNS}
        precursor = next(p for p in c["precursors"] if p != "WO3")
        for rep in (1, 2, 3):
            label = c["case"][-3:] + " (" + chem(precursor) + ")" if rep == 1 else ""
            row = [label, str(rep), f'{c["pg_rwp"]:.2f}' if rep == 1 else ""]
            high = model_cases[c["case"]]["sol_high"]
            high_attempt = next(a for a in high if a["replicate"] == rep)
            score = high_attempt["rwp"]
            cell = f"{score:.2f}"
            if score == min(a["rwp"] for a in high):
                cell = r"\textbf{" + cell + "}"
            if high_attempt.get("replacement_for_cancelled"):
                cell += r"$^{\dagger}$"
            row.append(cell)
            for key in RUNS:
                attempt = next(r for r in c["attempts"][key] if r["replicate"] == rep)
                v = attempt["rwp"]
                cell = r"\textemdash" if v is None else f"{v:.2f}"
                if v is not None and abs(v-minima[key]) < 1e-12:
                    cell = r"\textbf{" + cell + "}"
                row.append(cell)
            row.append(f'{c["opus_rwp"]:.2f}' if rep == 1 else "")
            lines.append(" & ".join(row) + r" \\" + ("*" if rep < 3 else ""))
    lines += [r"\midrule"]
    for title, fn in [("Mean", np.mean), ("Median", np.median)]:
        row = [r"\multicolumn{2}{l}{" + title + "}", f"{fn(pg):.2f}"]
        row += [f'{fn([np.mean([a["rwp"] for a in model_cases[c["case"]]["sol_high"]]) for c in cases]):.2f}']
        row += [f"{fn([np.mean(values(c,k)) for c in cases]):.2f}" for k in RUNS]
        row += [f'{fn([c["opus_rwp"] for c in cases]):.2f}']
        lines.append(" & ".join(row) + r" \\")
    table_macro("all_attempts_rows.tex", "experimentalTransferAllAttemptRows", lines)

    # Inventory differences are assessed across all three initial attempts, not a selected best run.
    specs = [("003", "Ca", "CaCO3", False), ("006", "Cu", "CuWO4", False),
             ("007", "Mg", "MgO", False), ("008", "Mn", "WO3", False),
             ("013", "Pb", "Pb3WO6", True), ("014", "Sr", "Sr2WO5", True),
             ("015", "Zn", "ZnO", False)]
    lines = []
    for suffix, element, formula, structural in specs:
        c = next(c for c in cases if c["case"] == "case-" + suffix)
        texformula = chem(formula)
        pgwt = 100 * sum(p["weight_fraction"] for p in c["pg_phases"] if p["formula"] == formula)
        cells = []
        pgtext = texformula + (f": {pgwt:.1f} wt\\%" if pgwt else ": absent")
        if suffix == "006":
            pgtext = "7 phase models; " + pgtext
        cells.append(pgtext + r"\newline $R_{\mathrm{wp}}=" + f'{c["pg_rwp"]:.2f}' + r"\%$")
        for key in ("P0", "E"):
            weights = phase_weights(c, key, formula, structural)
            positive = [w for w in weights if w > 0]
            n = len(positive)
            text = texformula + f": {n}/3"
            if positive:
                text += r"\newline " + f"{min(positive):.1f}--{max(positive):.1f} wt\\%"
            if suffix == "006":
                text = "2 phase models in 3/3" + r"\newline " + texformula + f": {min(weights):.1f}--{max(weights):.1f} wt\\%"
            text += r"\newline $\overline{R}_{\mathrm{wp}}=" + f'{np.mean(values(c,key)):.2f}' + r"\%$"
            cells.append(text)
        lines.append(" & ".join([suffix + " (" + element + ")"] + cells) + r" \\")
        lines.append(r"\addlinespace[4pt]")
    table_macro("inventory_rows.tex", "experimentalTransferInventoryRows", lines)


def save(fig, name, preview):
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / (name + ".pdf"), bbox_inches="tight", pad_inches=.04)
    if preview:
        preview.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview / (name + ".png"), dpi=180, bbox_inches="tight", pad_inches=.04)
    plt.close(fig)


def comparison(data, preview):
    cases = data["cases"]
    fig, (ax, delta) = plt.subplots(1, 2, figsize=(7.35, 5.0), gridspec_kw={"width_ratios": [1.5, 1], "wspace": .38})
    for key, offset, marker in [("PG", -.22, "D"), ("P0", 0, "o"), ("E", .22, "s")]:
        for i, c in enumerate(cases):
            v = [c["pg_rwp"]] if key == "PG" else values(c, key)
            ax.plot([min(v), max(v)], [i+offset]*2, c=COLORS[key], lw=1, alpha=.7)
            ax.scatter(np.mean(v), i+offset, s=18, marker=marker, color=COLORS[key], label=LABELS[key] if i == 0 else None)
    ax.set_yticks(range(15), [c["case"][-3:] + "  " + chem(next(p for p in c["precursors"] if p != "WO3")) for c in cases])
    ax.set_xscale("log")
    ax.set_xlim(2.8, 52)
    ax.set_xticks([3, 5, 10, 20, 50], ["3", "5", "10", "20", "50"])
    ax.minorticks_off()
    ax.set_xlabel(r"$R_{\mathrm{wp}}$ (%, logarithmic scale)")
    ax.set_title("(a) Experimental profile agreement", loc="left", weight="bold")
    differences = [np.mean(values(c,"E"))-np.mean(values(c,"P0")) for c in cases]
    delta.scatter(differences, range(15), color=COLORS["E"], s=22)
    delta.axvline(0, color="#555555", lw=.7)
    delta.set_yticks(range(15), [])
    delta.set_xlim(-6.2, 1.2)
    delta.set_xlabel(r"Evolved minus baseline $R_{\mathrm{wp}}$" + "\n(percentage points)")
    delta.set_title("(b) Effect of evolution", loc="left", weight="bold")
    for a in (ax, delta):
        a.set_ylim(14.7,-.7)
        a.grid(axis="x", color="#e7e7e7")
        a.set_axisbelow(True)
    ax.legend(loc="lower center", bbox_to_anchor=(.5,-.24), ncol=3, frameon=False, columnspacing=1.1, handletextpad=.4)
    save(fig, "transfer_comparison", preview)


def ablation_comparison(data, preview):
    """The existing five-condition figure, using the same replay records as Table 4."""
    cases = data["cases"]
    colors = ["#466682", "#CE6C28", "#008575", "#8154A2", "#AE4A68"]
    fig, (ax, ar) = plt.subplots(1, 2, figsize=(7.35, 5.15),
                                gridspec_kw={"width_ratios": [1.5, 1], "wspace": .42})
    offsets = np.linspace(-.27, .27, 5)
    for j, key in enumerate(RUNS):
        for i, case in enumerate(cases):
            v = values(case, key)
            y = i + offsets[j]
            ax.plot([min(v), max(v)], [y, y], color=colors[j], lw=.7, alpha=.55)
            ax.scatter(np.mean(v), y, s=15, color=colors[j], label=CONDITION_LABELS[key] if i == 0 else None)
        if key != "P0":
            ar.scatter([np.mean(values(c, key))-np.mean(values(c, "P0")) for c in cases],
                       np.arange(15)+offsets[j], color=colors[j], s=15)
    ax.set_yticks(range(15), [c["case"][-3:]+"  "+chem(next(p for p in c["precursors"] if p != "WO3"))
                            +f', {c["temperature_C"]:.0f}°C' for c in cases])
    ax.set_xlim(2, 18)
    ax.set_xticks([3, 6, 9, 12, 15, 18])
    ax.set_xlabel(r"Verified $R_{\mathrm{wp}}$ (%)")
    ar.set_xlabel("Change from baseline (percentage points)")
    ar.axvline(0, color="#505050", lw=.8)
    ar.set_xlim(-7.2, 1.2)
    ar.set_xticks([-6, -4, -2, 0])
    ar.set_yticks(range(15), [])
    for a in (ax, ar):
        a.set_ylim(14.65, -.65)
        a.grid(axis="y", color="#ededed", lw=.7)
        a.grid(axis="x", color="#f0f0f0", lw=.6)
        a.set_axisbelow(True)
    ax.set_title("(a) Mean and range of attempts", loc="left", weight="bold", pad=10)
    ar.set_title("(b) Paired mean differences", loc="left", weight="bold", pad=10)
    fig.legend(*ax.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(.53, 1.075),
               ncol=3, frameon=False)
    save(fig, "experimental_comparison", preview)


def cu_profiles(data, preview):
    arr = np.load(DATA / "cu_profiles.npz")
    c = next(c for c in data["cases"] if c["case"] == "case-006")
    x, y = arr["x"], arr["observed"]
    norm = y.max()
    fig, axes = plt.subplots(3,2, figsize=(7.35,5.7), gridspec_kw={"width_ratios":[2.1,1],"wspace":.2,"hspace":.66})
    descriptions = {"PG": "Seven phase models; CuWO$_4$ 68.1 wt%", "P0": "CuWO$_4$ + WO$_3$; CuWO$_4$ 97.8 wt%", "E": "CuWO$_4$ + WO$_3$; CuWO$_4$ 97.5 wt%"}
    for j, bounds in enumerate([(10.1,99.9),(22,40)]):
        m = (x>=bounds[0]) & (x<=bounds[1])
        offset = .3 * max(y[m]/norm)
        ymin = min(-.55, min(np.min((y[m]-arr[k][m])/norm-offset) for k in COLORS)) - .04
        ymax = 1.12 * max(max(y[m]/norm), max(np.max(arr[k][m]/norm) for k in COLORS))
        for i,key in enumerate(("PG","P0","E")):
            ax = axes[i,j]
            ax.plot(x[m][::3], y[m][::3]/norm, ".", color="#262626", ms=1, alpha=.65, label="Observed")
            ax.plot(x[m], arr[key][m]/norm, color=COLORS[key], lw=.8, label="Calculated")
            ax.plot(x[m], (y[m]-arr[key][m])/norm-offset, color="#888888", lw=.55, label="Difference (offset)")
            ax.axhline(-offset, color="#cccccc", lw=.5)
            ax.set_xlim(*bounds)
            ax.set_ylim(ymin,ymax)
            ax.tick_params(axis="y", left=False,labelleft=False)
            if i==2: ax.set_xlabel(r"$2\theta$ (degrees)")
            else: ax.tick_params(axis="x",labelbottom=False)
            if j==0:
                rep = "" if key=="PG" else f', r{data["cu_selected_replicates"][key]}'
                score = rwp(y,arr[key])
                ax.set_title(f'({chr(97+i)}) {LABELS[key]}{rep} | '+r'$R_{\mathrm{wp}}$'+f' = {score:.2f}%\n'+descriptions[key], loc="left", fontsize=8, pad=8)
            else: ax.set_title("Expanded region",loc="left",fontsize=8,pad=8)
    axes[0,0].legend(loc="upper right", frameon=False,fontsize=6.1)
    fig.text(.005,.5,"Intensity (common observed-maximum normalization)",rotation=90,va="center",fontsize=8)
    save(fig,"cu_deposited_profiles",preview)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-inputs",action="store_true")
    parser.add_argument("--refresh-model-comparison", action="store_true")
    parser.add_argument("--tables-only", action="store_true")
    parser.add_argument("--workspace",type=Path,default=ROOT.parent)
    parser.add_argument("--replay-results",type=Path, help="Output of the research repository's replay_panels.py")
    parser.add_argument("--preview-dir",type=Path)
    args=parser.parse_args()
    if args.refresh_inputs:
        if args.replay_results is None:
            parser.error("--refresh-inputs requires --replay-results")
        refresh_inputs(args.workspace.resolve(), args.replay_results.resolve())
    if args.refresh_model_comparison:
        refresh_model_comparison(args.workspace.resolve())
    data=json.loads((DATA/"records.json").read_text())
    validate(data)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8,"axes.titlesize":9,
                         "axes.labelsize":8.5,"xtick.labelsize":7.5,"ytick.labelsize":7.5,
                         "legend.fontsize":7.3,"axes.spines.top":False,"axes.spines.right":False,
                         "axes.linewidth":.65,"pdf.fonttype":42,"ps.fonttype":42,"savefig.facecolor":"white"})
    tables(data)
    if args.tables_only:
        print("Built tables; figures unchanged.")
        return
    comparison(data,args.preview_dir)
    ablation_comparison(data,args.preview_dir)
    cu_profiles(data,args.preview_dir)
    print("Built primary table, inventory comparison, all-attempt score table, and three figures.")


if __name__ == "__main__":
    main()
