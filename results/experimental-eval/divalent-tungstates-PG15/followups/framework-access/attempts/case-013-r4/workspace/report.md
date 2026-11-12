# Powder XRD phase analysis

## Result

The pattern is best described by a five-phase, partially reacted PbO–WO3 mixture. Weight fractions are normalized over the modeled crystalline material; no amorphous fraction was measured.

| Phase | Structural model | Weight % |
|---|---|---:|
| PbWO4, scheelite | I 41/a; a = 5.45769 Å, c = 12.0446 Å | 57.33 |
| WO3, monoclinic | P 21/c; a = 7.29214 Å, b = 7.53409 Å, c = 10.5576 Å, beta = 133.235° | 10.28 |
| PbO, massicot | Pbcm; a = 5.89040 Å, b = 5.48382 Å, c = 4.76922 Å | 13.35 |
| Pb2WO5 intermediate | C 2/m; a = 14.2127 Å, b = 5.80122 Å, c = 7.34498 Å, beta = 113.919° | 10.94 |
| Pb3WO6 intermediate | provisional P 21/m model; a = 7.14804 Å, b = 5.73844 Å, c = 8.04422 Å, beta = 102.189° | 8.09 |

The fresh atomic replay of `final.gpx` gives Rwp = 10.982% and Rp = 7.919% over all 8,282 points (Poisson weights, 1/max(counts,1)). The calculated profile in `fit.csv` is from that replay, not from cached GSAS-II arrays.

## Evidence and model selection

PbWO4 accounts for the dominant scheelite series, while monoclinic WO3 and orthorhombic massicot PbO account for substantial residual precursor peaks, consistent with incomplete reaction after 500 °C firing. A PbWO4/WO3/PbO-only model left reproducible peaks near 25.91°, 30.15–30.24°, and 31.05° 2theta. A C 2/m Pb2WO5 framework adapted from published Pb2MoO5 accounts for the 25.91° family and related reflections. A P 21/m Pb3WO6 framework adapted from Pb3SO6 uniquely accounts for the 30.15–31.05° group; alternative Pb3WO6 settings either fitted materially worse or refined to negligible abundance.

Pb2O3 and lead-deficient Pb7W8O28.8 tests refined to negligible abundance. Orthorhombic PbO2 reduced the residual around one congested 28.5–29° region only by driving its broadening parameters to limits; its independent low-angle line was unsupported and PbO2 is not credible after a 500 °C treatment. It was therefore excluded.

Published PbWO4, WO3, and PbO structures were used as starting models. The WO3 oxygen sublattice was replaced with the physically consistent P 21/c literature model, eliminating a short O–O contact and also improving the fit. Unit cells were refined. Heavy-atom reference adjustments were limited to 0.04 Å per site, matching the stated reference-mismatch scale; oxygen coordinates were otherwise held to the reference frameworks. The Cu Kalpha1/Kalpha2 doublet, background, zero offset, specimen displacement, peak widths, phase size/strain, polarization, surface roughness, and supported March–Dollase texture terms are stored in the project.

## Remaining uncertainty

The Pb2WO5 identification and framework are supported by multiple peaks, but its oxygen coordinates are weakly constrained by this X-ray pattern; its exact local structure and fraction have greater systematic uncertainty than the three published phases.

The Pb3WO6 assignment is the least secure. Its cell and Pb/W scattering framework are supported by otherwise-unmodeled peaks, but the submitted P 21/m model is an analogue-derived profile model, not a reliable determination of the complete atomic structure. In particular, its inherited oxygen sublattice gives W–O distances as short as about 1.46 Å. The exact Pb3WO6 oxygen arrangement cannot be determined reliably from these data, and its approximately 8 wt% fraction can trade with overlapping minor-phase intensity. Fractions should therefore be treated as conditional estimates with systematic uncertainty of several weight-percentage points, rather than as covariance-limited values.

Residual structured misfit remains (Rwp is about 3.14 times the no-parameter-correction counting-statistical Rexp), chiefly in heavily overlapped low-angle peaks and minor-phase intensities. The analysis does not quantify amorphous material or phases below the practical detection limit.
