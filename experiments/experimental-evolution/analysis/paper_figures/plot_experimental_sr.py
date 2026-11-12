"""Rebuild Figure 9 from frozen Sr project replays; no fitting is performed.

Requires numpy and matplotlib. Input arrays and their source-file hashes are in
data/experimental_transfer/sr_profiles.npz; reported residuals are checked
against the existing experimental-transfer records.
"""
import os
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / "results/experimental-eval/divalent-tungstates-PG15/paper-data/experimental_transfer"
OUTPUT = Path(os.environ.get("PXRD_RELEASE_OUTPUT", ROOT / ".runs/multiphase-reproduction")) / "figures/sr_profiles.pdf"
SPECS = [
    ("P0", 1, "Baseline", "#466682",
     r"SrWO$_4$ + WO$_3$ + Sr$_3$W$_2$O$_9$; no Sr$_2$WO$_5$ recovery"),
    ("F", 2, "Framework access", "#008575",
     r"Eight submitted phases; no Sr$_2$WO$_5$ match"),
    ("E", 2, "Evolved v6", "#CE6C28",
     r"SrWO$_4$ + WO$_3$ + Sr$_2$WO$_5$; Sr$_2$WO$_5$ recovered"),
]


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8,
        "axes.titlesize": 9, "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
        "legend.fontsize": 7.3, "axes.spines.top": False,
        "axes.spines.right": False, "axes.linewidth": .65,
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "savefig.facecolor": "white",
    })
    records = json.loads((DATA / "records.json").read_text())
    case = next(c for c in records["cases"] if c["case"] == "case-014")
    with np.load(DATA / "sr_profiles.npz", allow_pickle=False) as archive:
        arrays = {k: archive[k] for k in archive.files}
    x, observed = arrays["x"], arrays["observed"]
    assert np.all(np.diff(x) > 0)
    evaluation = (x >= 10.1) & (x <= 99.9)
    markers = [29.75, 30.9, 32.6, 44.7, 48.6, 57.0, 61.2]
    fig, axes = plt.subplots(
        3, 2, figsize=(7.35, 5.4), squeeze=False,
        gridspec_kw={"width_ratios": [2.2, 1], "wspace": .23, "hspace": .6},
    )
    for i, (key, replicate, label, color, subtitle) in enumerate(SPECS):
        row = next(r for r in case["attempts"][key] if r["replicate"] == replicate)
        prediction = arrays[key]
        obs_eval, pred_eval = observed[evaluation], prediction[evaluation]
        weights = 1 / np.maximum(obs_eval, 1)
        residual = 100 * np.sqrt(
            np.sum(weights * (obs_eval - pred_eval)**2)
            / np.sum(weights * obs_eval**2)
        )
        assert abs(residual - row["rwp"]) < 1e-4
        norm = max(observed)
        obs, pred = observed / norm, prediction / norm
        difference = obs - pred
        for j, ax in enumerate(axes[i]):
            bounds = (10.1, 70) if j == 0 else (65.5, 68.5)
            mask = (x >= bounds[0]) & (x <= bounds[1])
            maximum = obs[mask].max()
            offset = .22 * maximum
            ax.plot(x[mask][::3], obs[mask][::3], ".", color="#262626",
                    ms=1.1, alpha=.7, label="Observed")
            ax.plot(x[mask], pred[mask], color=color, lw=.8, label="Calculated")
            ax.plot(x[mask], difference[mask] - offset, color="#858585",
                    lw=.55, label="Difference (offset)")
            ax.axhline(-offset, color="#c9c9c9", lw=.5)
            for position in markers:
                if bounds[0] < position < bounds[1]:
                    ax.axvline(position, color="#4b9f8d", lw=.6, alpha=.45,
                               linestyle="--")
            ax.set_xlim(*bounds)
            ax.set_ylim(-.65 * maximum, 1.12 * maximum)
            ax.tick_params(axis="y", labelleft=False, left=False)
            if i == 2:
                ax.set_xlabel(r"$2\theta$ (degrees)")
            else:
                ax.tick_params(axis="x", labelbottom=False)
            if j == 0:
                ax.set_title(
                    f"({chr(97+i)}) {label}, r{replicate}  |  "
                    + r"$R_{\mathrm{wp}}$" + f" = {row['rwp']:.2f}%\n{subtitle}",
                    loc="left", fontsize=8, pad=7,
                )
            else:
                ax.set_title("Diagnostic region", loc="left", fontsize=8, pad=7)
    axes[0, 0].legend(loc="upper right", fontsize=6.5, frameon=False)
    fig.text(.005, .52, "Intensity (common normalization within each measurement)",
             rotation=90, va="center", fontsize=8)
    fig.savefig(OUTPUT, bbox_inches="tight", pad_inches=0.035)
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
