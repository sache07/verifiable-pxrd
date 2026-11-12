# Powder XRD phase analysis

The crystalline model contains three phases. Fractions are normalized only over these modeled crystalline phases.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| SrWO4, scheelite | I 41/a | 0.6410 (64.1 wt%) |
| WO3, monoclinic | P 21/c | 0.0875 (8.7 wt%) |
| Sr2WO5, analogue-derived | Pnma | 0.2715 (27.2 wt%) |

The full-grid atomic-model replay gives Rwp = 6.6329%, Rp = 4.8872%, and GOF = 1.8792 over 10.0094–99.9944 degrees 2-theta. Because pointwise uncertainties were not supplied, the refinement used counting-statistical weights with sigma = sqrt(intensity). The replay optimized no parameters, reproduced the submitted profile, and raised no negative-background or negative-width flags.

## Evidence

Scheelite SrWO4 accounts for the dominant reflection family throughout the scan. Exact-composition monoclinic WO3 accounts for the coherent triplet near 23.5, 24.0, and 24.7 degrees and its higher-angle family. After fitting those phases, the remaining coherent reflections near 29.8, 30.9, 32.6, 44.7, and 48.6 degrees index together with a Pnma Sr2WO5 model. This inventory is chemically consistent with the precursor context through the incomplete-reaction relation Sr2WO5 + WO3 -> 2 SrWO4. SrCO3, SrO/SrO2, Sr3W2O9, reduced tungsten oxides, and alternate Sr-W-O models did not retain a stable positive scale while indexing the residual family broadly. No coherent unindexed reflection family remains; the largest residual is the heavily overlapped 27.8–28.1 degree group.

The SrWO4 model starts from COD 1546036. Its oxygen position was moved by 0.052 A in a bounded refinement; the resulting tetrahedral W-O distance is 1.907 A. WO3 starts from the physically six-coordinate P21/c model COD 2311041; its W-O distances are 1.70–2.18 A. This was preferred over a marginally closer but strongly rounded 1960 WO3 checkpoint with an implausibly long W-O contact. The refined isotropic crystallite sizes are 0.354 micrometre for SrWO4, 0.185 micrometre for WO3, and 0.187 micrometre for Sr2WO5.

## Remaining uncertainty

No exact Sr2WO5 entry was available in the frozen reference index. Its model was transferred from the Pnma Ba2ReO5 topology (COD 1529756) by Ba->Sr and Re->W substitution, followed by cell and bounded cation-coordinate refinement. Its geometry is ordinary (W-O 1.76–2.07 A; shortest Sr-O about 2.59 A), and it indexes a broad reflection family, but its detailed atomic structure is not determined reliably. Oxygen-coordinate trials ran to their bounds for negligible improvement and were therefore rejected. The Sr2WO5 topology and its approximately 27 wt% amount should be treated as the best-supported, chemically plausible model rather than a definitive structure determination.

Formal scale-covariance uncertainties are only about 0.08–0.11 weight-percentage point and do not represent model uncertainty. The polarization refined to its allowed upper boundary, the instrumental W and X widths remain at physical bounds, and the two surface-roughness parameters are highly correlated. Consequently, systematic uncertainty in the phase fractions is larger than the formal values; the rounded 64:9:27 wt% result is more defensible than the extra digits in `result.json`. Amorphous content, if present, cannot be quantified without an internal standard.

`final.gpx` is the saved GSAS-II project used for the submitted CIFs and fractions. `fit.csv` is a fresh full-grid replay of that project, with difference defined as observed minus calculated.
