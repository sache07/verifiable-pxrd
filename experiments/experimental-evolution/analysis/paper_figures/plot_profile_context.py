"""Rebuild Zn profiles, measured-pattern overview and v5 regression diagnostics.

Reads only public benchmark inputs and saved evaluation outputs. No refinement.
The Zn comparison uses the same fixed r3 attempts as the manuscript illustration.
"""

from collections import defaultdict
import json
import os
from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
RESULTS = ROOT / "results/experimental-eval/divalent-tungstates-PG15"
BENCH = ROOT / "pxrd-bench/divalent-tungstates-PG15"
OUTPUT = (
    Path(os.environ.get("PXRD_RELEASE_OUTPUT", ROOT / ".runs/multiphase-reproduction")) / "figures"
)
OUTPUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def load(path):
    return json.loads(path.read_text())


def save(fig, name):
    path = OUTPUT / f"{name}.pdf"
    fig.savefig(path, bbox_inches="tight", pad_inches=0.035)
    plt.close(fig)
    print(path)


fig, axes = plt.subplots(
    2,
    2,
    figsize=(7.35, 3.6),
    squeeze=False,
    gridspec_kw={"width_ratios": [2.2, 1], "wspace": 0.23, "hspace": 0.6},
)
for i, (condition, label, color) in enumerate(
    [("baseline", "Baseline", "#466682"), ("evolved", "Evolved v6", "#CE6C28")]
):
    row = next(
        r
        for r in load(RESULTS / condition / "per_attempt.json")
        if r["case"] == "case-015" and r["replicate"] == 3
    )
    path = RESULTS / condition / "attempts/case-015-r3/evaluation/project_replay/prediction.npz"
    with np.load(path, allow_pickle=False) as data:
        x, obs, pred = (data[k] for k in ("x", "observed", "predicted"))
        mask = (x >= 10.1) & (x <= 99.9)
        weights = 1 / np.maximum(obs[mask], 1)
        rwp = 100 * np.sqrt(
            np.sum(weights * (obs[mask] - pred[mask]) ** 2) / np.sum(weights * obs[mask] ** 2)
        )
        assert abs(rwp - row["replay_interior_rwp"]) < 1e-4
        norm = max(obs)
        obs, pred = obs / norm, pred / norm
        for j, ax in enumerate(axes[i]):
            bounds = (10.1, 70) if j == 0 else (22.5, 25)
            m = (x >= bounds[0]) & (x <= bounds[1])
            scale = obs[m].max()
            offset = 0.22 * scale
            ax.plot(
                x[m][::3], obs[m][::3], ".", color="#262626", ms=1.1, alpha=0.7, label="Observed"
            )
            ax.plot(x[m], pred[m], color=color, lw=0.8, label="Calculated")
            ax.plot(
                x[m],
                obs[m] - pred[m] - offset,
                color="#858585",
                lw=0.55,
                label="Difference (offset)",
            )
            ax.axhline(-offset, color="#c9c9c9", lw=0.5)
            ax.set_xlim(*bounds)
            ax.set_ylim(-0.65 * scale, 1.12 * max(scale, pred[m].max()))
            ax.tick_params(axis="y", labelleft=False, left=False)
            if i == 1:
                ax.set_xlabel(r"$2\theta$ (degrees)")
            else:
                ax.tick_params(axis="x", labelbottom=False)
            title = (
                (
                    f"({chr(97 + i)}) {label}, r3  |  "
                    + r"$R_{\mathrm{wp}}$"
                    + f" = {rwp:.2f}%\n"
                    + r"ZnWO$_4$ + WO$_3$ + ZnO"
                )
                if j == 0
                else "Diagnostic region"
            )
            ax.set_title(title, loc="left", fontsize=8, pad=7)
axes[0, 0].legend(loc="upper right", fontsize=6.5, frameon=False)
fig.text(
    0.005,
    0.52,
    "Intensity (common normalization within measurement)",
    rotation=90,
    va="center",
    fontsize=8,
)
save(fig, "zn_profiles")

fig, axes = plt.subplots(5, 3, figsize=(7.35, 7), sharex=True)
for meta, ax in zip(load(BENCH / "case-metadata.json"), axes.flat):
    data = np.genfromtxt(BENCH / "cases" / meta["case"] / "pattern.csv", delimiter=",", names=True)
    ax.plot(
        data["two_theta_deg"], data["intensity"] / max(data["intensity"]), color="#526e87", lw=0.5
    )
    precursor = next(p for p in meta["precursors"] if p != "WO3")
    precursor = re.sub(r"(\d+)", r"$_{\1}$", precursor)
    ax.set_title(
        f"{meta['case'][-3:]}  {precursor} + WO$_3$, {meta['temperature_C']:.0f}°C",
        fontsize=7.5,
        loc="left",
    )
    ax.set_yticks([])
    ax.set_xlim(10, 100)
    ax.set_xticks([20, 40, 60, 80, 100])
    ax.spines["left"].set_visible(False)
for ax in axes[-1]:
    ax.set_xlabel(r"$2\theta$ (degrees)")
fig.subplots_adjust(hspace=0.6, wspace=0.17)
save(fig, "measured_patterns")

status = load(
    ROOT / "results/experimental-evolution/divalent-tungstates-access/evidence/status.json"
)
scores = defaultdict(list)
for job in status["jobs"]:
    if job["status"] == "complete" and job["policy"] in ("P0", "v5"):
        scores[job["policy"], job["case_id"]].append(job["score_100"])
cases = sorted({c for policy, c in scores if policy == "v5"})
deltas = [np.mean(scores["v5", c]) - np.mean(scores["P0", c]) for c in cases]
assert len(cases) == 6
fig, ax = plt.subplots(figsize=(7.2, 2.3))
names = [
    "Ca: weak calcite",
    "Cu: four phases",
    r"Mn$_3$WO$_6$",
    "Harder Zn",
    r"Harder Mn$_3$WO$_6$",
    r"Easier Mn$_3$WO$_6$",
]
ax.bar(np.arange(6), deltas, width=0.6, color=["#008575" if v >= 0 else "#925b60" for v in deltas])
ax.axhline(0, color="#454545", lw=0.7)
ax.axhline(-15, color="#925b60", ls="--", lw=0.8, label="Maximum permitted case regression")
ax.set_xticks(np.arange(6), names, fontsize=7.3)
ax.set_ylabel("v5 − framework baseline\n(synthetic score points)")
ax.set_ylim(-46, 49)
for i, val in enumerate(deltas):
    ax.text(
        i,
        val + (2 if val >= 0 else -2),
        f"{val:+.1f}",
        ha="center",
        va="bottom" if val >= 0 else "top",
        fontsize=8,
    )
ax.legend(loc="upper left", frameon=False)
save(fig, "framework_v5_regressions")
