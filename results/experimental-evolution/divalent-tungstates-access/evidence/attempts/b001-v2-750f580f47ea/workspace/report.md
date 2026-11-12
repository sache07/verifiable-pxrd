# Powder XRD phase analysis

The 700 °C CuO–WO3 sample is a four-phase crystalline mixture. Weight fractions below are normalized over the modeled crystalline material; they do not quantify any amorphous content.

| Phase | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| CuWO4 | P -1 | 65.7987 wt% | a=4.62224, b=4.85992, c=5.74819; α=88.6758, β=84.7010, γ=88.5195 |
| Cu3WO6 | Pa-3 | 12.9318 wt% | a=9.79238 |
| WO3 | P -1 | 18.8437 wt% | a=7.30013, b=7.55945, c=7.68525; α=90.0037, β=89.0200, γ=89.9969 |
| CuO | C 2/c | 2.4259 wt% | a=4.66994, b=3.43084, c=5.12011; β=99.5393 |

The formal one-sigma scale/covariance errors are 0.033, 0.024, 0.026, and 0.016 wt percentage point, respectively. These are counting-statistical refinement errors only; model, overlap, calibration, and preferred-profile systematics are larger, particularly for the minor CuO phase.

## Evidence and model choice

All phases were refined simultaneously against the original 10–100° Cu Kα1/Kα2 grid. CuWO4 accounts for the triclinic splitting and lines at 15.00°, 18.81°, 29.08°, and 30.07° 2θ. Cu3WO6 is required by its Pa-3 sequence at 15.19°, 19.79°, 32.50°, 33.78°, and 57.60°. Triclinic WO3 gives the diagnostic 22.67°/23.05°/23.91° triplet. Minor CuO is supported by the 35.08–35.10°, 38.31°, 38.64°, and 48.44° lines; its scale remained positive and stable in the shared fit.

Published COD structures 4000806, 1527404, 2106293, and 1011194 supplied the respective starting models. Same-state comparisons favored triclinic WO3 over tested P21/c and orthorhombic references and triclinic CuWO4 over the P2/c alternative. The C2/c and Cc descriptions of CuO are effectively indistinguishable at this abundance, so the conventional C2/c model is reported. No coherent set of unassigned residual peaks remained; the largest residual structure is oscillatory around already modeled WO3 and CuWO4 peaks, so residual-directed prototype transfer was not warranted. Numerically failed trials were treated as unknown, not as evidence against a phase.

A Cu2WO4 precursor addition was tested in the complete four-phase state from 0.5, 2, and 5 wt% starts. Its scale reproducibly converged to only 0.050–0.054 wt%, including when its cell was allowed to vary. This is below reliable identification/quantification here: Cu2WO4 is therefore not included, but is not claimed absent. No amorphous fraction can be inferred from this measurement alone.

## Refinement and uncertainty

The final full-grid, zero-parameter replay gives Rwp=2.17674%, Rp=1.64364%, χ²=15056.33, and GOF=1.348 for 8301 points. The model uses the reported Cu Kα doublet, a +785 µm specimen displacement, −0.025° zero offset, a smooth 12-term background, and phase-specific size/microstrain broadening. Preferred orientation was not supported. WO3 anisotropic broadening is clear; the exact anisotropy axes for CuO and CuWO4 are less secure and do not alter the submitted atomic structures appreciably.

WO3 oxygen positions are less well determined than the W sublattice, and the CuO coordinates/displacement parameter are largely reference-controlled because CuO is only 2.4 wt%. All submitted CIFs pass the supplied geometry/occupancy screen: minimum contacts are 1.775 Å (CuWO4), 1.819 Å (Cu3WO6), 1.708 Å (WO3), and 1.946 Å (CuO), with no flagged contacts. The replay also reports no negative-width, background, displacement, or polarization flags. In `fit.csv`, difference is observed minus calculated intensity.
