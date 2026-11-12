# PXRD phase analysis

The pattern is best described by two crystalline precursor phases rather than a resolved reaction product:

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| BaCO3 (witherite) | orthorhombic Pmcn setting of Pnma, No. 62 | 52.36 wt% |
| WO3 | monoclinic P21/c, No. 14 | 47.64 wt% |

The listed fractions are normalized over the modeled crystalline phases. Their covariance-only standard uncertainty is 0.16 wt% for each phase. A more realistic model-dependent uncertainty is about ±0.6 wt%, estimated from the near-tied WO3 symmetry alternative and accepted nuisance branches. No amorphous fraction can be measured without an internal standard.

## Evidence

The monoclinic WO3 model accounts for the resolved low-angle family at calculated 2θ = 23.404, 23.888, and 24.643°, as well as independent higher-angle families near 34.33–34.45, 47.51–50.16, and 53.78–56.24°. Witherite accounts for independent reflections near 24.197, 34.039, 34.859, 42.291, 43.200, and 44.495°. Removing BaCO3 or WO3 from the mature refinement raises Rwp from 6.98% to approximately 24.7% or 26.9%, respectively, so both phases have broad, multi-peak support rather than overlap-only scale credit.

Several WO3 structures were tested with identical staged nuisance refinements. Orthorhombic Pnma was clearly inferior (Rwp about 13.39%). Triclinic P-1 remained close (Rwp 6.9891%) to monoclinic P21/c (6.9804%). P21/c was selected because it gives the slightly lower complete-pattern residual with fewer cell variables and is the chemically expected room-temperature WO3 symmetry. This distinction is not strong enough to claim that a very small triclinic distortion is excluded.

A clean scheelite BaWO4 I41/a model was constructed by the charge-balanced Mo6+→W6+ substitution in an audited BaMoO4 topology and tested from the mature baseline. A forced three-phase refinement returned an apparent 0.29 wt% BaWO4 and lowered Rwp by only 0.018 percentage point. It failed the structural acceptance test: its strong, relatively unique predictions at 28.33 and 32.15° worsened the local residual, while most gains occurred at overlaps. BaWO4 is therefore not included, and a trace BaWO4 fraction cannot be determined reliably from this pattern.

## Refinement and fit

The refinement used the reported Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio, a 10-term Chebyshev background, phase scales and cells, sample displacement, minimal W/X/Y profile terms, polarization, weak one-axis March-Dollase corrections, and a refined WO3 isotropic size profile term. Removing each retained optional term caused matched full-pattern degradation. Extra U or V terms became nonphysical or unstable; surface roughness was negative and 99.6% correlated; BaCO3 size was singular; and microstrain showed an exact phase-swapping degeneracy, so these terms were rejected. Atomic coordinates and displacement parameters were kept at the audited source values because the overlapped laboratory pattern does not support their independent refinement. The nominal WO3 size term, 0.233(11) µm, should not be interpreted as a calibrated crystallite size because no instrumental profile standard was supplied.

Final statistics are Rwp = 6.980%, Rp = 5.293%, GOF = 2.007, and reduced χ² = 4.028 over 10–100° 2θ. The low Durbin–Watson value (0.546) confirms correlated profile residuals, especially in crowded regions, so formal parameter errors understate systematic uncertainty. Both submitted CIFs pass composition, occupancy, symmetry, duplicate-site, and contact audits; `final.gpx` passes convergence, profile-regeneration, and positive-width checks with no audit flags.
