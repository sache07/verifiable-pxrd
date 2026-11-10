"""Rebuild native and shared fixed-profile distributions from the frozen CSVs."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42})
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
from scipy.stats import gaussian_kde

ROOT = Path(__file__).resolve().parents[3]
CONDITIONS = [("Crystalyze", "crystalyze"), ("DiffractGPT", "diffractgpt"),
    ("Ab-PXRD-Solver", "ab-pxrd-solver"), ("deCIFer (known Z)", "decifer-known-z"),
    ("PXRDGen (known Z)", "pxrdgen-known-z"), ("RealPXRD-Solver (known Z)", "realpxrd-solver-known-z"),
    ("GPT-5.6 Sol (high)", "gpt-5-6-sol-high"), ("matsci-codex", "matsci-codex"),
    ("pxrd-codex", "pxrd-codex"), ("adapted-codex", "adapted-codex")]
TRUNCATED = {"matsci-codex", "pxrd-codex", "adapted-codex"}
COLORS = {True: "#3569A8", False: "#C44E52"}


def load(root, metric):
    filename = "native-rwp-candidates.csv" if metric == "native" else "fixedparams-v1-rwp-candidates.csv"
    manifest = json.loads((root / "manifest.json").read_text())
    if hashlib.sha256((root / filename).read_bytes()).hexdigest() != manifest["files"][filename]["sha256"]:
        raise ValueError(f"Frozen data changed: {filename}")
    rows, references = [], []
    for row in csv.DictReader((root / filename).open()):
        if not row["rwp_percent"] or not math.isfinite(float(row["rwp_percent"])):
            continue
        value = float(row["rwp_percent"])
        if row.get("condition_type") == "reference":
            references.append(value)
            continue
        rows.append({"condition": row.get("condition", row.get("framework")),
                     "exact": row["exact_match"].lower() == "true", "rwp": value})
    if metric == "fixed" and (len(references) != 200 or any(abs(v) > 1e-12 for v in references)):
        raise ValueError("Expected 200 zero-residual reference self-comparisons")
    return rows


def edges(values, metric, global_upper):
    if metric == "fixed":
        return np.linspace(0, global_upper, 41)
    count = min(42, max(14, len(np.histogram_bin_edges(values, bins="fd")) - 1))
    width = np.ptp(values)
    lower, upper = max(0, min(values) - .04 * width), max(values) + .04 * width
    return np.linspace(lower, max(upper, lower + 1e-8), count + 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "results/appendix/profile-residuals/as-submitted")
    parser.add_argument("--output", type=Path, default=ROOT / ".runs/profile-residuals")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    summary = []
    for metric in ("native", "fixed"):
        rows = load(args.data, metric)
        upper = max(10, math.ceil(max(r["rwp"] for r in rows) / 10) * 10)
        fig, axes = plt.subplots(5, 2, figsize=(10.8, 14.2))
        for ax, (name, slug) in zip(axes.flat, CONDITIONS):
            members = [r for r in rows if r["condition"] == name]
            ax.set_title(name, loc="left", fontweight="semibold", fontsize=10)
            if not members:
                ax.text(.5, .5, "Native dense-profile residual unavailable\n(sparse peak-list representation)",
                        ha="center", va="center", transform=ax.transAxes, fontsize=9)
                ax.set_axis_off()
                continue
            pooled = np.array([r["rwp"] for r in members])
            bins = edges(pooled, metric, upper)
            domain = np.linspace(bins[0], bins[-1], 700)
            counts = {}
            for exact in (False, True):
                values = np.array([r["rwp"] for r in members if r["exact"] == exact])
                counts[exact] = len(values)
                if not len(values):
                    continue
                color = COLORS[exact]
                ax.hist(values, bins=bins, density=True, color=color, alpha=.18, edgecolor=color, linewidth=.5)
                if len(values) >= 3 and np.std(values) > 0:
                    ax.plot(domain, gaussian_kde(values)(domain), color=color, linewidth=1.6)
                ax.axvline(np.mean(values), color=color, linewidth=1.6)
                ax.axvline(np.median(values), color=color, linewidth=1.6, linestyle="--")
                summary.append(dict(metric=metric, condition=name, exact=exact, n=len(values),
                                    mean=float(np.mean(values)), median=float(np.median(values))))
            xmax = np.quantile(pooled, .95) if metric == "native" and slug in TRUNCATED else bins[-1]
            ax.set_xlim(bins[0], xmax)
            ax.text(.985, .95, f"exact n={counts[True]:,}\nmiss n={counts[False]:,}",
                    transform=ax.transAxes, ha="right", va="top", fontsize=8)
            ax.grid(axis="y", color="#D7D7D7", linewidth=.5, alpha=.7)
            ax.spines[["top", "right"]].set_visible(False)
            ax.tick_params(labelsize=8)
            ax.set_xlabel(("Framework-native" if metric == "native" else "Shared fixed-parameter") + r" $R_{\mathrm{wp}}$ (%)", fontsize=8.5)
        for ax in axes[:, 0]:
            ax.set_ylabel("Density", fontsize=8.5)
        fig.legend(handles=[Patch(color=COLORS[True], alpha=.3, label="Exact match"),
            Patch(color=COLORS[False], alpha=.3, label="Miss"),
            Line2D([], [], color="#333333", label="Mean"),
            Line2D([], [], color="#333333", linestyle="--", label="Median")],
            loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(.5, .967))
        fig.suptitle(("Framework-native" if metric == "native" else "Shared fixed-parameter") +
                     " profile residuals by structural recovery", y=.99, fontsize=15)
        note = ("Agent panels reuse clean fixedparams-v1 scores. Native scales differ across specialists.\n"
                "Coding-agent axes end at the pooled 95th percentile; all points remain in density estimates and summary statistics."
                if metric == "native" else
                "Clean reference and candidate profiles are independently max-normalized. No noise, fitting, alignment, or refinement.")
        fig.text(.06, .012, note, fontsize=8, va="bottom")
        fig.subplots_adjust(left=.075, right=.985, bottom=.065, top=.935, hspace=.43, wspace=.22)
        for extension in ("pdf", "png"):
            fig.savefig(args.output / f"{metric}-rwp-distributions.{extension}", dpi=200, bbox_inches="tight")
        plt.close(fig)
    with (args.output / "summary.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)


if __name__ == "__main__":
    main()
