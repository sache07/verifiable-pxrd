# Powder XRD phase analysis

The pattern is adequately described by two crystalline phases: wolframite-type NiWO4 and monoclinic WO3. The refined phase amounts, normalized over these modeled crystalline phases, are:

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| NiWO4 | P 2/c | a = 4.59964, b = 5.66200, c = 4.90944, beta = 89.9812 | 0.76122 (76.12 wt%) |
| WO3 | P 21/c | a = 7.68792, b = 7.53195, c = 10.52676, beta = 136.0880 | 0.23878 (23.88 wt%) |

## Evidence

The NiWO4 assignment accounts for the characteristic wolframite reflections at approximately 19.19, 23.91, 24.85, 30.87, 36.52, and 54.58 degrees 2theta. The second phase is required by the monoclinic-WO3 triplet near 23.06, 23.53, and 24.28 degrees and its reflections near 26.53, 28.55/28.82, and 33.20-34.09 degrees. These two reflection families account for the visible peaks across the full 10-100 degree range.

Unreacted rocksalt NiO was considered but not retained: its strong 200 reflection expected near 43.3 degrees is absent, and its other required reflections are not supported as a coherent set. Alternative WO3 cell/symmetry models were tested; the P 21/c model gave the most stable chemically plausible whole-pattern fit. The WO3 CIF uses a nonconventional but symmetry-equivalent monoclinic cell setting.

The final GSAS-II model used the supplied Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio. Background, phase scales, zero offset, profile terms, lattice parameters, and atomic coordinates were refined. On all 8,282 measured points, the fit gives Rwp = 4.184%, Rp = 3.222%, Rexp = 3.466%, and goodness of fit = 1.207 (reduced chi-square = 1.458). The calculated profile in `fit.csv` is generated directly from the saved `final.gpx` model.

## Remaining uncertainty

The scale-factor covariance gives a formal uncertainty of about 0.11 weight-percentage point per phase, but this understates uncertainty from background, peak-shape, and structural-model choices. A more realistic interpretation is approximately 76 +/- 1 wt% NiWO4 and 24 +/- 1 wt% WO3. Fractions are relative only to the modeled crystalline material; an amorphous component or trace phase below the pattern's detection sensitivity cannot be quantified without an internal standard. The phase identities and major/minor proportions are well constrained, while individual oxygen coordinates are less precise than the unit cells and phase scales.
