# PXRD phase analysis

The crystalline pattern is explained by two phases: **64.00(15) wt% monoclinic gamma-WO3** and **36.00(15) wt% tetragonal BaO2**. Parentheses are covariance-derived one-sigma uncertainties in the last digits; the fractions are normalized only over the modeled crystalline phases.

| Phase | Structural model | Refined cell | Crystalline wt% |
|---|---|---|---:|
| gamma-WO3 | P 21/n, No. 14 (equivalent P 21/c setting) | a = 7.31561, b = 7.53306, c = 7.69129 A, beta = 90.7129 deg | 64.00(15) |
| BaO2 | I 4/mmm, No. 139 | a = 3.81345, c = 6.84696 A | 36.00(15) |

The final fit has Rwp = 7.398%, Rp = 5.499%, Rexp = 3.641%, and GOF = 2.036. The saved `fit.csv` difference is observed minus calculated intensity.

## Evidence and model selection

The monoclinic WO3 model accounts for the characteristic 23.4/23.9/24.7 degree cluster and many independent reflections through 100 degrees. BaO2 accounts for distinct families near 26.3, 27.1, 33.5, 43.0, 46.6, and 55.8 degrees. Both atomistic models therefore have broad, multi-peak support rather than support from overlap alone.

The starting structures were COD 2311041 for WO3, transformed exactly to a conventional P 21/n cell, and COD 1010113 for BaO2. Both were audited before use. Refined W coordinates retained plausible WO3 contacts (shortest W-O 1.716 A). Refining the peroxide O coordinate gives O-O = 1.457 A; the CIF audit flags this as a short O-O contact, but it is the chemically expected peroxide bond rather than a model defect.

Matched tests rejected alternative WO3 P 21/m, triclinic, and orthorhombic structures, as well as BaWO4, Ba3WO6, Ba3W2O9, BaO, and W3O8 additions. The largest trace trial, Ba3W2O9 at about 0.45 wt%, mainly fitted a single noise excursion near 30.84 degrees and predicted unsupported unique peaks, so it did not meet the multi-peak criterion. No third crystalline phase has a reliable structure or fraction in this pattern.

Refinement used Cu K-alpha1 (1.540598 A), Poisson count weights because point uncertainties were not supplied, a 12-term Chebyshev background, refined scales/cells/zero/polarization, one global Lorentzian width term, phase-specific isotropic broadening, and a mild WO3 [101] March-Dollase term. A K-alpha doublet model, surface roughness, sample displacement, added global width terms, and phase strain were rejected by poorer, correlated, nonphysical, or region-limited behavior. The final angular-branch test selected the zero-only baseline; the joint zero/displacement branch was 0.9997 correlated. Removing each retained optional term caused a matched complete-pattern degradation. Final profile regeneration and the GSAS-II numerical audit passed with no flags.

## Remaining uncertainty

The formal fraction uncertainties (about 0.15 wt percentage points) understate model systematic uncertainty. There was no calibrated instrument profile, external standard, or effective-polarization calibration; profile/texture/ADP alternatives indicate that uncertainty at roughly the 1-2 wt percentage-point level is more realistic. The values do not quantify amorphous material, and strongly overlapping or sub-percent crystalline impurities cannot be excluded.

WO3 oxygen coordinates and displacement parameters could not be refined reliably: unconstrained oxygen refinement produced implausibly short approximately 1.60 A W-O contacts, while ADP refinement destabilized polarization and phase scales. Those quantities were therefore retained at source/default values; zero Uiso values in the WO3 CIF denote unrefined displacement parameters, not a physical determination of zero thermal motion.
