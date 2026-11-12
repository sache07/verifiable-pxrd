# PXRD phase analysis

The pattern is best modeled as two crystalline phases: **75.12 wt% monoclinic WO3** and **24.88 wt% spinel Co3O4**, normalized over the modeled crystalline material. The formal covariance uncertainty is ±0.28 percentage point for each complementary fraction. A more realistic model-dependent uncertainty is about ±2 percentage points because the data lack supplied pointwise uncertainties and a calibrated instrument profile, and the phase scales retain sensitivity to displacement/polarization choices.

## Evidence and phase inventory

The low-angle WO3 triplet near 23.46, 23.95, and 24.71° 2theta and its many middle/high-angle families are reproduced by COD 2311041 after an exactly equivalent cell transformation to a near-orthogonal P 21/n setting (space-group No. 14). Co3O4 is independently required by coherent families near 19.37, 31.63, 37.20, 45.15, 59.67, and 65.55° and is modeled from the 296 K structure COD 9005896 (F d -3 m, No. 227). The refined structures have plausible geometry: W–O = 1.71–2.16 Å and Co–O approximately 1.91–1.93 Å.

Alternative records were challenged under the same final nuisance model. The selected WO3 model gives Rwp = 3.218%, compared with 3.282% for triclinic COD 2106293 despite its additional cell variables and 4.079% for monoclinic COD 1528915. Orthorhombic and high-pressure small-cell records were substantially poorer in the earlier inventory screen.

No usable exact CoWO4 database model was available: COD 5910316 has malformed duplicate/overoccupied sites. The required stoichiometric-analogue search supplied physically plausible CoMoO4 (COD 7205001, Mo→W) and FeWO4 (COD 9008124, Fe→Co) parents. Both substituted models passed bond/density screening but refined to the imposed scale floor (1e-12) when re-challenged under the final profile. CoWO4 is therefore not included; its fraction cannot be determined reliably and should not be interpreted as exactly zero. No coherent unassigned peak family requires another crystalline phase, but a trace phase below the data's detection capability remains possible.

## Refinement model and checks

The GSAS-II model used the supplied Cu Kalpha1/Kalpha2 wavelengths (1.540598/1.544426 Å) and 0.5 intensity ratio. With no experimental uncertainties supplied, Poisson weights (1/count) were used. Refined terms were both phase scales and cells, a smooth nine-term Chebyshev-1 background, one specimen-shift correction, polarization, and nonnegative common U/W/X profile terms. The final GSAS-II specimen shift is -585.19(1.18) micrometres; its large magnitude follows the observed angle-dependent peak displacement but means the absolute lattice constants are less certain than their formal e.s.d.'s suggest.

WO3 required replay-stable [010] uniaxial microstrain, 4262(124) and 2974(119) microstrain in the equatorial/axial components. Removing it or replacing it with isotropic strain worsened Rwp to 3.391% and 3.309%. Once the common W profile term was admitted, phase-size terms became singular or collapsed and were removed. SH/L asymmetry was 98.8% correlated with specimen shift; low-angle roughness hit a bound and correlated 98% with scale; both were rejected. Symmetry-distinct texture trials were also rejected: the strongest b-axis result improved 020 but worsened 040 and 060, so it failed the required multi-family coherence test.

For Co3O4, the one independent oxygen coordinate refined to x = 0.26154(72), and one common isotropic displacement parameter refined to Uiso = 0.02016(129) Å². Splitting Co and O displacement factors gave no meaningful additional improvement. WO3 coordinates were retained from the source model and Uiso was fixed at 0.01 Å²; attempts to refine WO3 displacement factors drove polarization to its bound and did not replay-converge, so those parameters cannot be determined reliably from this pattern.

## Fit and remaining uncertainty

The final full-range replay converged without covariance or bound warnings: Rwp = 3.218%, Rp = 2.312%, Rexp = 1.722%, and goodness-of-fit = 1.871 (8301 points, 25 variables). The background is smooth and positive, and isolated low-, middle-, and high-angle families show no systematic position drift; remaining residual structure is concentrated around the strongest overlapping WO3 peaks and modest intensity/profile imperfections.

Fractions quantify only the modeled crystalline phases. No internal standard was supplied, so amorphous content cannot be measured. The submitted CIFs, fractions, and every row of `fit.csv` were exported from the saved and reopened `final.gpx`; `fit.csv` defines difference as observed minus calculated.
