"""Rebuild the original evolution figure from the released 135-attempt ledger."""
from pathlib import Path
from collections import defaultdict
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
ROOT = Path(__file__).resolve().parents[4]
SYN = ROOT / "results/experimental-evolution/divalent-tungstates"
OUT = Path(os.environ.get("PXRD_RELEASE_OUTPUT", ROOT / ".runs/multiphase-reproduction"))
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)
COLORS = ["#466682", "#CE6C28"]
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8,"axes.titlesize":9,
"axes.labelsize":8.5,"xtick.labelsize":7.5,"ytick.labelsize":7.5,
"legend.fontsize":7.3,"axes.spines.top":False,"axes.spines.right":False,
"axes.linewidth":.65,"pdf.fonttype":42,"ps.fonttype":42,"savefig.facecolor":"white"})
def read_json(path):
    return json.loads(path.read_text())
def write_csv(*args):
    pass  # The complete table is produced by analysis/reproduce.py.
def save(fig, name):
    fig.savefig(FIG / (name + ".pdf"), bbox_inches="tight", pad_inches=.035)
    plt.close(fig)
state = read_json(SYN / "evidence/status.json")
JOBS = [j for j in state["jobs"] if not j.get("superseded_by")]
assert len(JOBS) == 135 and all(j["status"] == "complete" for j in JOBS)
syn_records = [dict(id=j["id"], case=j["case_id"], policy=j["policy"],
                    group=j["group"], purpose=j["purpose"], replicate=j["replicate"],
                    score=j["score_100"], D=j.get("D_poisson"),
                    physical_validity=j.get("physical_validity")) for j in JOBS]
write_csv("synthetic_attempts.csv", syn_records)
SCORES = defaultdict(list)
for j in JOBS:
    SCORES[j["policy"], j["case_id"]].append(j["score_100"])
first_cases = [f"b001-c{i:02d}" for i in range(1, 7)]
initial_labels = [
    r"c01  CaWO$_4$ control", r"c02  Zn: three phases",
    r"c03  hidden SrWO$_4$", r"c04  hidden MnWO$_4$",
    r"c05  hidden Ca$_3$WO$_6$", r"c06  Pb: four phases",
]
COLS = ["P0", "v1", "v2", "v3", "v4", "v5", "v6-screen", "v6"]
matrix = np.full((6, len(COLS)), np.nan)
for i, case in enumerate(first_cases):
    for t, p in enumerate(COLS):
        values = ([j["score_100"] for j in JOBS if j["case_id"] == case
                   and j["policy"] == "v6" and j["purpose"] == "development"]
                  if p == "v6-screen" else SCORES[p, case])
        if values:
            matrix[i, t] = np.mean(values)
assert abs(np.mean(matrix[:, 0]) - 50.04) < .01
assert abs(np.mean(matrix[:, -1]) - 74.07) < .01
fig = plt.figure(figsize=(7.35, 6.2))
gs = fig.add_gridspec(2, 2, height_ratios=[1.18, 1], width_ratios=[1.25, 1],
                      hspace=.68, wspace=.5)
ax = fig.add_subplot(gs[0, :])
cmap = plt.colormaps["YlGnBu"].copy()
cmap.set_bad("#f0f0f0")
im = ax.imshow(matrix, vmin=0, vmax=100, cmap=cmap, aspect="auto")
ax.set_xticks(range(8), ["Baseline\nmean, n=3", "v1", "v2", "v3", "v4", "v5",
                         "v6\nscreen", "v6\nmean, n=3"])
ax.set_yticks(range(6), initial_labels)
ax.tick_params(length=0)
for i in range(6):
    for t in range(8):
        v = matrix[i, t]
        ax.text(t, i, "—" if np.isnan(v) else f"{v:.1f}", ha="center", va="center",
                color="white" if v > 67 else "#222222", fontsize=8)
ax.axvline(5.5, color="white", lw=2)
ax.axvline(6.5, color="white", lw=2)
ax.set_title("(a) Development screens and repeated evaluation", loc="left", pad=10, weight="bold")
fig.colorbar(im, ax=ax, fraction=.024, pad=.018, label="Synthetic score")
ax2 = fig.add_subplot(gs[1, 0])
for i, case in enumerate(first_cases):
    a, b = np.mean(SCORES["P0", case]), np.mean(SCORES["v6", case])
    ax2.plot([a, b], [i, i], c="#c7cbd0", lw=1.7, zorder=1)
    for p, col, shift in [("P0", COLORS[0], -.10), ("v6", COLORS[1], .10)]:
        values = SCORES[p, case]
        ax2.scatter(values, np.full(len(values), i + shift), s=14, color=col, alpha=.45)
        ax2.scatter(np.mean(values), i, s=34, color=col,
                    label={"P0": "Baseline", "v6": "Evolved v6"}[p] if i == 0 else None, zorder=3)
ax2.set_yticks(range(6), [f"c{i:02d}" for i in range(1, 7)])
ax2.invert_yaxis()
ax2.set_xlim(0, 103)
ax2.set_xlabel("Synthetic score (dots: attempts; large dots: means)")
ax2.grid(axis="x", color="#e7e7e7")
ax2.set_axisbelow(True)
ax2.legend(frameon=False, loc="upper left")
ax2.set_title("(b) Initial-panel repeat variability", loc="left", weight="bold", pad=10)
ax3 = fig.add_subplot(gs[1, 1])
transfer_rows = []
for i, batch in enumerate(["b001", "b002", "b003"]):
    cids = sorted({j["case_id"] for j in JOBS if j["case_id"].startswith(batch)})
    for p, offset, color in [("P0", -.18, COLORS[0]), ("v6", .18, COLORS[1])]:
        means = [np.mean(SCORES[p, c]) for c in cids]
        val = float(np.mean(means))
        ax3.bar(i + offset, val, width=.32, color=color, label=p if i == 0 else None)
        ax3.text(i + offset, val + 2, f"{val:.1f}", ha="center", fontsize=8)
        transfer_rows.append(dict(batch=batch, policy=p, n_cases=len(cids),
                                  n_attempts=sum(len(SCORES[p, c]) for c in cids), mean_score=val))
ax3.set_xticks(range(3), ["Initial panel\n6 cases", "New batch 2\n2 cases", "New batch 3\n2 cases"])
ax3.set_ylim(0, 102)
ax3.set_ylabel("Mean synthetic score")
ax3.set_title("(c) Transfer to new cases", loc="left", weight="bold", pad=10)
ax3.grid(axis="y", color="#e7e7e7")
ax3.set_axisbelow(True)
save(fig, "evolution")
write_csv("synthetic_transfer.csv", transfer_rows)
