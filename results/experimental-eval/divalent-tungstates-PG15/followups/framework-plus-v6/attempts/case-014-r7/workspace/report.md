# Powder XRD phase analysis

The pattern is described by three crystalline phases: **62.63 wt% scheelite SrWO4**, **10.21 wt% monoclinic WO3**, and **27.16 wt% orthorhombic Sr2WO5**. Fractions are normalized over these modeled crystalline phases; an amorphous fraction cannot be obtained from this analysis. The final full-range atomic-model refinement gives Rwp = 6.948%, Rp = 5.323%, and goodness of fit = 1.965.

## Evidence

The dominant I 41/a SrWO4 assignment is supported across the scan by the 112, 004, 020, 024, and 220 families at approximately 27.95, 30.18, 33.36, 45.43, and 47.72 degrees 2theta, with consistent higher-angle families. Monoclinic P 21/n WO3 accounts for the characteristic groups near 23.43–24.69, 33.57–34.48, and 47.52–50.22 degrees.

Those two phases leave a coherent residual family at about 14.99, 16.59, 29.70, 32.57, and 44.62 degrees. No exact Sr2WO5 entry was available in the screened COD subset. A required cross-chemistry prototype search identified Pnma Ba2ReO5 (COD 1529756); the charge-preserving substitutions Ba2+ -> Sr2+ and Re6+ -> W6+, followed by lattice contraction and cell refinement, account for that entire family and lower Rwp from about 18% to about 11% at the inventory stage. Its final cell is a = 7.25359, b = 5.54850, c = 10.89457 A. SrCO3, SrO, Sr3W2O9, monoclinic SrWO4, and Sr3WO6 analogue records were re-challenged under the final common profile. Their fitted amounts were only 0–0.29 wt% with negligible, non-unique improvements, so they were not retained.

The final model uses one specimen-displacement correction, a smooth eight-term Chebyshev background, a Cu Kalpha doublet, Suortti surface roughness, and common polarization/asymmetry terms. Phase-specific size terms are supported for WO3 and Sr2WO5. Isotropic microstrain trials became negative, and all preferred-orientation axes refined close to unity, so both effects were pruned. The saved project was reopened and reconverged over all 8,282 points before the CIFs and `fit.csv` were exported; an independent no-refinement replay regenerated the same fractions with no project review flags.

## Remaining uncertainty

The SrWO4 identity and its scheelite framework are secure. The WO3 phase identity and cell are also secure, but its old, low-precision source coordinates generate a 1.58 A O-O close-site review flag; unconstrained coordinate refinement was unstable, so detailed WO3 bond geometry should not be interpreted from the submitted model.

The Pnma symmetry, cell, composition, and phase fraction of Sr2WO5 are strongly supported by its many unique or partly overlapped reflections, but its internal structure is less certain because it is analogue-derived. Only a physically limited heavy-atom adjustment (about 0.04 A RMS) was retained; oxygen coordinates remain prototype-derived. The common instrumental width and SrWO4 crystallite-size contributions could not be separated reliably: bounded trials collapsed at limits, so the replay-stable common profile was retained and no SrWO4 domain size is claimed. Formal fraction standard uncertainties are about 0.12–0.16 wt%, but roughness, displacement-parameter, and analogue-model correlations make a more realistic absolute systematic uncertainty roughly 1–2 wt% per phase.
