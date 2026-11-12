# PXRD phase analysis

## Result

The modeled crystalline material is **33.94 wt% tetragonal BaO2** (I4/mmm) and **66.06 wt% triclinic WO3** (P-1), normalized over these two crystalline phases. The formal GSAS-II scale-derived standard uncertainty is 0.15 wt% for each fraction. A more realistic uncertainty is about ±1 wt% because there is no internal standard or calibrated instrument profile and the fractions shift by several tenths of a percent among acceptable envelope/profile choices.

The final fit has Rwp = 7.051%, Rp = 5.251%, Rexp = 3.634%, and GOF = 1.940 (8301 points, 31 refined variables, no dropped variables). `fit.csv` is regenerated from the same `final.gpx` used to export both CIFs and fractions.

## Evidence for the phase model

The low-angle WO3 triplet near 23.39, 23.88, and 24.60 degrees and its many higher-angle split families require the triclinic model. BaO2 independently accounts for strong reflections near 26.28, 27.02, 33.48, 42.92, and 47.93 degrees. Leave-one-phase-out fits are poor: Rwp is 31.90% for BaO2 alone and 20.55% for triclinic WO3 alone.

Atomistic alternatives were screened with matched nuisance refinements and audited CIFs. In the initial matched comparison, triclinic, monoclinic, and orthorhombic WO3 gave Rwp values of 8.072%, 9.209%, and 11.433%, respectively. Retesting replacements against the mature model still favored triclinic WO3 (7.051%): monoclinic WO3 was 7.51–7.57% and developed a 95% size/strain correlation, while orthorhombic WO3 stalled at 9.15% with a dropped profile variable. Malformed database candidates with duplicate/implausibly close oxygen sites were rejected before refinement.

An ordered, charge-balanced scheelite BaWO4 model was also challenged against the mature fit. Its scale-only result was nominally 0.15(4) wt%, but it failed the required multi-peak test: most benefit came from overlap near existing peaks, the isolated 28.32-degree line helped only slightly, and the stronger isolated 32.13-degree prediction plus several other strong lines worsened the residual. BaWO4 is therefore not reported as a determined phase; this dataset does not support a reliable BaWO4 fraction.

## Structural refinement and uncertainty

The BaO2 model began from COD 1010113. Its refined cell is a = 3.81286 A and c = 6.84877 A. The peroxide oxygen coordinate refined to z = 0.3945(9), giving an O-O distance of 1.445 A. The CIF audit flags this short O-O contact for review, but it is chemically expected for peroxide and all sites are fully occupied.

The WO3 model began from COD 2106293. Its refined cell is a = 7.31677 A, b = 7.53440 A, c = 7.69207 A, alpha = 89.4575 degrees, beta = 90.7293 degrees, and gamma = 90.2935 degrees. The database atomic coordinates were retained: the broad, heavily overlapped pattern cannot reliably refine the 16 independent WO3 sites or their displacement parameters. Thus the triclinic topology and phase fraction are supported, but fine WO3 coordinates/ADPs should not be interpreted as measured by this dataset.

The final nuisance model uses a 12-term Chebyshev background, one global Gaussian-width term, simple surface roughness, one sample-displacement term, and isotropic size plus microstrain for each phase. Removing any phase size/strain contribution materially degraded the complete-pattern fit. No March-Dollase term was retained; tested ratios stayed within 0.987–1.030 for BaO2 and 0.992–1.012 for WO3. Size and microstrain are strongly covariant (about 0.87–0.90), so their numerical values are descriptive only. The displacement correction also assumes the GSAS-II default 200 mm goniometer radius because no radius/calibrant was supplied; refined lattice constants consequently carry additional systematic uncertainty.

Fractions are conditional on the modeled crystalline phases and do not quantify amorphous material.
