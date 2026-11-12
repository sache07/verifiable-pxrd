#!/usr/bin/env python3
"""Visual and residual-led checks for the provisional final profile."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "polar_texture_CuO_010.gpx"
WINDOWS = [
    (15.3, 20.8, "Cu3WO6 low angle"),
    (22.8, 24.9, "WO3 low-angle family"),
    (35.1, 39.5, "CuO strongest families"),
    (47.5, 51.7, "middle-angle mixed families"),
    (57.5, 64.2, "middle/high-angle families"),
    (81.8, 90.3, "high-angle families"),
]


def main() -> None:
    project = G2sc.G2Project(str(PROJECT))
    hist = project.histogram(0)
    data = np.asarray(hist.data["data"][1], dtype=float)
    x, yobs, weight, ycalc, background, diff = data
    use = (x >= 10.0) & (x <= 100.0)

    fig, axes = plt.subplots(4, 2, figsize=(13, 12), constrained_layout=True)
    ax = axes.flat[0]
    ax.plot(x[use], yobs[use], "k-", lw=0.45, label="observed")
    ax.plot(x[use], ycalc[use], color="#d55e00", lw=0.65, label="calculated")
    offset = np.percentile(yobs[use], 2) - 3.0 * np.std(diff[use])
    ax.plot(x[use], diff[use] + offset, color="#0072b2", lw=0.5, label="difference (offset)")
    ax.set_title("Full-range fit")
    ax.legend(fontsize=8)
    ax.set_ylabel("counts")

    ax = axes.flat[1]
    norm = diff[use] * np.sqrt(weight[use])
    ax.plot(x[use], norm, color="#0072b2", lw=0.5)
    ax.axhline(0.0, color="k", lw=0.5)
    ax.set_title("Weighted difference")
    ax.set_ylabel(r"$(y_o-y_c)/\sqrt{y_o}$")

    for ax, (lower, upper, title) in zip(axes.flat[2:], WINDOWS):
        sel = (x >= lower) & (x <= upper)
        ax.plot(x[sel], yobs[sel], "k.", ms=2.2, label="observed")
        ax.plot(x[sel], ycalc[sel], color="#d55e00", lw=1.0, label="calculated")
        ax.plot(x[sel], background[sel], color="#009e73", lw=0.65, label="background")
        ax.set_title(title)
        ax.set_ylabel("counts")
    for ax in axes[-1]:
        ax.set_xlabel(r"$2\theta$ (degrees)")
    fig.savefig(ROOT / "final_diagnostic.png", dpi=180)

    smooth = gaussian_filter1d(diff[use] * np.sqrt(weight[use]), 2.0)
    xx = x[use]
    peaks, _ = find_peaks(np.abs(smooth), distance=12, prominence=0.45)
    ranked = sorted(peaks, key=lambda i: abs(smooth[i]), reverse=True)
    print("Largest smoothed weighted residual extrema:")
    for i in ranked[:30]:
        print(f"{xx[i]:9.4f} {smooth[i]:9.4f}")


if __name__ == "__main__":
    main()
