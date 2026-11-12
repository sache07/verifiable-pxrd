#!/usr/bin/env python3
"""Plot isolated CuO families with and without CuO microstrain."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
MODELS = {
    "no CuO strain": ROOT / "three_phase_broadening_Cu3WO6_size.gpx",
    "CuO strain": ROOT / "combined_CuO_strain.gpx",
}
WINDOWS = [
    (32.59, 0.50, "CuO 110 (low angle)"),
    (35.64, 0.48, "CuO 002 / 11-1"),
    (58.55, 0.55, "CuO 202 (middle angle)"),
    (65.86, 0.55, "CuO 022 (middle-high angle)"),
    (82.72, 0.65, "CuO 31-3 (high angle)"),
]


def arrays(path: Path) -> np.ndarray:
    project = G2sc.G2Project(str(path))
    return np.asarray(project.histogram(0).data["data"][1], dtype=float)


def main() -> None:
    data = {name: arrays(path) for name, path in MODELS.items()}
    source = next(iter(data.values()))
    fig, axes = plt.subplots(len(WINDOWS), 1, figsize=(9, 12), constrained_layout=True)
    colors = {"no CuO strain": "#d55e00", "CuO strain": "#0072b2"}
    for ax, (center, half_width, title) in zip(axes, WINDOWS):
        use = np.abs(source[0] - center) <= half_width
        x = source[0, use]
        y = source[1, use]
        ax.plot(x, y, "k.", ms=2.5, label="observed")
        for name, arr in data.items():
            ax.plot(x, arr[3, use], lw=1.2, color=colors[name], label=name)
        ax.set_title(title)
        ax.set_ylabel("counts")
        ax.grid(alpha=0.15)
    axes[-1].set_xlabel(r"$2\theta$ (degrees)")
    axes[0].legend(ncol=3, fontsize=8)
    fig.savefig(ROOT / "width_diagnostics.png", dpi=180)

    # Report local weighted residual sums for the same windows.
    for center, half_width, title in WINDOWS:
        use = np.abs(source[0] - center) <= half_width
        print(title)
        for name, arr in data.items():
            chi = np.sum(arr[2, use] * (arr[1, use] - arr[3, use]) ** 2)
            print(name, float(chi), "n", int(use.sum()))


if __name__ == "__main__":
    main()
