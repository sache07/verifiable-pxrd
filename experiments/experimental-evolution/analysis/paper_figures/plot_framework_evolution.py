"""Rebuild the two framework-access evolution histories from frozen records.

Default uses data/framework_evolution/records.json; no solver jobs are launched.
Refresh with --refresh-inputs --runs-root /path/to/pxrd-evolution/runs.
Requires numpy and matplotlib. The two runs have distinct panels and gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / "results/experimental-eval/divalent-tungstates-PG15/paper-data/framework_evolution/records.json"
FIGURE = Path(os.environ.get("PXRD_RELEASE_OUTPUT", ROOT / ".runs/multiphase-reproduction")) / "figures/framework_evolution.pdf"
TABLE = Path(os.environ.get("PXRD_RELEASE_OUTPUT", ROOT / ".runs/multiphase-reproduction")) / "tables/framework_versions.tex"


def refresh(runs_root):
    payload = {"campaigns": {}, "provenance_sha256": {}}
    fields = ("id", "case_id", "policy", "status", "score_100", "score_status", "score_interval")
    for key, name in (("early", "divalent-tungstates-fw"),
                      ("later", "divalent-tungstates-access")):
        root = runs_root / name
        source = root / "evidence/status.json"
        status = json.loads(source.read_text())
        assert status["current_package"] == "P0"
        payload["campaigns"][key] = {
            "run": name, "snapshot": status["at"], "incumbent": "P0",
            "jobs": [{f: j.get(f) for f in fields} for j in status["jobs"]],
        }
        files = [source, root / "evolve/PROMPT.md", root / "scorer/config_freeze.json"]
        if key == "later":
            files += [root / "control/comparison.py", root / "policies/v5/guidance.md"]
        for path in files:
            payload["provenance_sha256"][str(path.relative_to(runs_root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(payload, indent=2) + "\n")


def interval(job):
    if job["score_100"] is not None:
        return [float(job["score_100"])] * 2
    bounds = job["score_interval"]
    assert bounds is not None and len(bounds) == 2
    return bounds


def summarize(data):
    early = data["campaigns"]["early"]["jobs"]
    assert sum(j["score_100"] is not None for j in early) == 35
    assert len([j for j in early if j["policy"] == "P0"]) == 18
    assert [j["policy"] for j in early if j["score_100"] is None] == ["v9"]
    jobs = data["campaigns"]["later"]["jobs"]
    assert len(jobs) == 156 and all(j["status"] == "complete" for j in jobs)
    assert sum(j["policy"] == "P0" for j in jobs) == 30
    out = []
    for version in range(1, 8):
        policy = f"v{version}"
        candidates = [j for j in jobs if j["policy"] == policy]
        cases = sorted({j["case_id"] for j in candidates})
        assert len(candidates) == 18 and len(cases) == 6
        deltas, variances, bounded = [], [], []
        for case in cases:
            a = [interval(j) for j in candidates if j["case_id"] == case]
            b = [j["score_100"] for j in jobs if j["case_id"] == case and j["policy"] == "P0"]
            assert len(a) == len(b) == 3 and all(v is not None for v in b)
            arr = np.asarray(a)
            deltas.append(arr.mean(axis=0) - np.mean(b))
            # Only one attempt has an interval. Include its variance extrema.
            uncertain = np.flatnonzero(arr[:, 0] != arr[:, 1])
            var_options = [np.var(arr[:, i], ddof=1) for i in (0, 1)]
            if len(uncertain):
                assert len(uncertain) == 1
                i = uncertain[0]
                trial = arr[:, 0].copy()
                trial[i] = np.clip(np.mean(np.delete(trial, i)), *arr[i])
                var_options.append(np.var(trial, ddof=1))
                bounded.append(case)
            variances.append([min(var_options) + np.var(b, ddof=1),
                              max(var_options) + np.var(b, ddof=1)])
        delta = np.asarray(deltas).mean(axis=0)
        # This equals the controller's pooled within-case SE for 3+3 repeats.
        se = np.sqrt(np.asarray(variances).sum(axis=0) / (3 * len(cases)**2))
        threshold = np.maximum(4, 2 * se)
        worst = np.min(deltas, axis=0)
        assert worst[1] < -15
        out.append({"version": policy, "cases": cases, "mean": delta.tolist(),
                    "threshold": threshold.tolist(), "worst": worst.tolist(),
                    "bounded_cases": bounded, "case_deltas": np.asarray(deltas).tolist()})
    assert abs(out[4]["mean"][0] - 2.9604628496773735) < 1e-10
    return out


def number(bounds, signed=False):
    fmt = "+.2f" if signed else ".2f"
    if format(bounds[0], fmt) == format(bounds[1], fmt):
        return format(bounds[0], fmt)
    return "[" + ", ".join(format(x, fmt) for x in bounds) + "]"


def build(data, preview):
    summary = summarize(data)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                         "axes.labelsize": 8, "xtick.labelsize": 7,
                         "ytick.labelsize": 7, "pdf.fonttype": 42})
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.4, 2.8),
                                    gridspec_kw={"width_ratios": [1.13, 1]})
    fig.subplots_adjust(left=.055, right=.995, top=.80, bottom=.22, wspace=.29)
    early = data["campaigns"]["early"]["jobs"]
    policies = ["P0"] + [f"v{i}" for i in range(1, 10)]
    cases = [f"b001-c{i:02d}" for i in range(1, 7)]
    matrix = np.full((6, 10), np.nan)
    for i, case in enumerate(cases):
        for k, policy in enumerate(policies):
            values = [j["score_100"] for j in early if j["policy"] == policy
                      and j["case_id"] == case and j["score_100"] is not None]
            if values:
                assert len(values) == (3 if policy == "P0" else 1)
                matrix[i, k] = np.mean(values)
    cmap = ListedColormap(["#f4d1ba", "#a7d8ce"])
    cmap.set_bad("#eeeeee")
    left.imshow(matrix, cmap=cmap, norm=BoundaryNorm([0, 80, 101], 2), aspect="auto")
    for i in range(6):
        for k in range(10):
            if np.isfinite(matrix[i, k]):
                left.text(k, i, f"{matrix[i, k]:.0f}", ha="center", va="center", fontsize=8.5)
    left.text(9, 4, "…", ha="center", va="center", fontsize=11)
    left.set_xticks(range(10), ["Base"] + [f"v{i}" for i in range(1, 9)] + ["v9*"])
    left.set_yticks(range(6), [f"c{i:02d}" for i in range(1, 7)])
    left.set_xticks(np.arange(-.5, 10), minor=True)
    left.set_yticks(np.arange(-.5, 6), minor=True)
    left.grid(which="minor", color="white", linewidth=1.8)
    left.tick_params(which="both", length=0)
    left.axvline(.5, color="#555555", lw=.9)
    left.set_title("(a) Early: selective screening", loc="left", fontweight="bold", fontsize=9, pad=30)
    left.text(.5, 1.09, "3 baseline solves; 1 per revision / case", transform=left.transAxes,
              ha="center", fontsize=7.4)
    left.legend(handles=[Rectangle((0, 0), 1, 1, fc="#a7d8ce", label=r"$Q\geq80$"),
                         Rectangle((0, 0), 1, 1, fc="#f4d1ba", label=r"$Q<80$"),
                         Rectangle((0, 0), 1, 1, fc="#eeeeee", label="Unscored")],
                loc="upper center", bbox_to_anchor=(.5, -.12), ncol=3, frameon=False,
                fontsize=7, handlelength=1, columnspacing=1.1)
    left.text(.5, -.40, "* v9 unscored; no full-panel validation", transform=left.transAxes,
              ha="center", fontsize=7)
    x = np.arange(1, 8)
    right.axhline(0, color="#999999", lw=.7)
    right.axhline(-15, color="#bb4e40", ls="--", lw=1)
    right.text(7.45, -14, "−15 limit", ha="right", va="bottom", color="#a13f34", fontsize=7)
    for cut in (3.5, 6.5):
        right.axvline(cut, color="#b9b9b9", ls=":", lw=.8)
    right.scatter(x, [np.mean(r["mean"]) for r in summary], color="#303e50", s=28, label="Mean gain", zorder=3)
    right.scatter(x, [np.mean(r["worst"]) for r in summary], color="#c66246", marker="v", s=32,
                  label="Worst case", zorder=3)
    right.scatter(x, [np.mean(r["threshold"]) for r in summary], facecolors="white", edgecolors="#008878",
                  marker="D", s=28, label="Required mean", zorder=3)
    right.add_patch(Rectangle((4.65, -44), .70, 66, fc="none", ec="#8f8f8f", lw=.7))
    right.set(xlim=(.5, 7.5), ylim=(-45, 23), ylabel=r"Change in score $Q$", xlabel="Package revision")
    right.set_xticks(x, [f"v{i}" for i in x])
    right.set_title("(b) Later: 3-repeat evaluation", loc="left", fontweight="bold", fontsize=9, pad=30)
    right.text(.5, 1.09, "6 active cases × 3 solves per condition", transform=right.transAxes,
               ha="center", fontsize=7.4)
    right.legend(loc="upper center", bbox_to_anchor=(.5, -.24), ncol=3, frameon=False,
                 fontsize=7, handletextpad=.2, columnspacing=.6)
    for ax in (left, right):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    left.spines["left"].set_visible(False)
    left.spines["bottom"].set_visible(False)
    FIGURE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE, bbox_inches="tight", pad_inches=.04)
    if preview:
        fig.savefig(preview, dpi=180, bbox_inches="tight", pad_inches=.04)
    plt.close(fig)
    rows = ["% Generated by scripts/plot_framework_evolution.py.", r"\newcommand{\frameworkEvolutionRows}{%"]
    for r in summary:
        rows.append(" & ".join([r["version"], number(r["mean"], True), number(r["threshold"]),
                                 number(r["worst"], True)]) + r" \\")
    TABLE.write_text("\n".join(rows) + "\n}\n")
    print("Verified 35 scored early attempts and 156 later attempts; rebuilt figure and version table.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-inputs", action="store_true")
    parser.add_argument("--runs-root", type=Path)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()
    if args.refresh_inputs:
        if args.runs_root is None:
            parser.error("--refresh-inputs requires --runs-root")
        refresh(args.runs_root)
    build(json.loads(DATA.read_text()), args.preview)
