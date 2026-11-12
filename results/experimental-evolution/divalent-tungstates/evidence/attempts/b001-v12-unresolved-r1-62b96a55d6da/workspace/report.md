# Quantitative crystalline-phase analysis

Three crystalline phases are retained: scheelite SrWO4 (reaction product), monoclinic WO3, and orthorhombic SrCO3 (unreacted precursors). Fractions are normalized over these modeled crystalline phases.

| Phase | Space group and refined cell | Weight fraction |
|---|---|---:|
| SrWO4 | I 41/a; a = 5.39306 Å, c = 11.90006 Å | 0.60686 ± 0.00140 |
| WO3 | P 21/c; a = 7.28917 Å, b = 7.55491 Å, c = 10.51674 Å, beta = 132.9841° | 0.24102 ± 0.00111 |
| SrCO3 | Pnma; a = 6.02452 Å, b = 5.09735 Å, c = 8.39309 Å | 0.15212 ± 0.00141 |

The full-range refinement (9.9034–100.0946° 2theta, 8,301 points) gives Rwp = 3.4916%, Rp = 2.6517%, Rexp = 2.8612%, and GOF = 1.2226. The final replay converged with maximum shift/ESD = 0.005. The quoted fraction uncertainties are formal least-squares ESDs.

## Evidence and model selection

SrWO4 is established by the scheelite families near 17.45, 27.18/27.31, 29.44, 32.62, 47.10, 55.52, and 56.82° 2theta. No exact SrWO4 record was available in the supplied index, so the ordered I 41/a SrMoO4 model (COD 2300460) was adapted by the isovalent Mo6+ to W6+ substitution and its cell was refined. BaWO4-derived scheelite, monoclinic CaWO4-derived, and wolframite-derived competitors either collapsed in scale or failed their physical/convergence checks.

WO3 is identified independently by the 22.51/22.94/23.81° triplet and further families near 33.58, 41.31, 49.29, and 54.15°. The selected ordered P 21/c record is COD 2311041. A second monoclinic record refined to Rwp = 3.7050%. A lower-symmetry triclinic record approached Rwp = 3.4960% only after its own texture/strain loop, but remained worse than P 21/c and used two additional variables (AIC 3391.0 versus 3366.1). Thus P 21/c is preferred, though the near triclinic competitor leaves some uncertainty in the detailed WO3 symmetry/atomic model. Its effect on the WO3 fraction is small (about 0.0009 absolute).

SrCO3 is supported by non-coincident families near 24.65, 25.26, 36.04/36.12, 43.6, and 47.23°. The Pnma record (COD 9008198) decisively outperformed the rhombohedral alternative. Removing SrWO4, WO3, or SrCO3 raises Rwp to 22.56%, 10.68%, or 4.98%, respectively. A scale-first Sr3W2O9 watch-list test collapsed to 1e-12 from three starting scales, so no reliable fourth phase is retained.

The mature model uses the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, an eight-term smooth background, one specimen-shift correction, nonnegative common U/W/X, refined polarization, simple March-Dollase terms, and a two-parameter [010] WO3 strain model. Failed roughness, extra phase-size, generalized-strain, and SH/L terms were pruned. Representative low/middle/high-angle peak audits showed no repeated left/right asymmetry requiring an additional axial term. All three final CIFs pass `learned/cif_health.py` without invalid occupancy or hard-contact flags.

## Chemical closure and uncertainty

The assemblage is chemically consistent with incomplete SrCO3 + WO3 -> SrWO4 + CO2 reaction at 650 °C. Converting the refined phase masses to moles gives total Sr/W = 0.9968; this near-unity closure is supporting evidence, not a fitted constraint, because precursor amounts were not reported.

Fractions are crystalline-phase-normalized only. Without an internal standard, amorphous content and therefore absolute bulk fractions cannot be determined. Systematic uncertainty from preferred orientation, source choice, specimen geometry, and the absence of supplied pointwise intensity uncertainties is larger than the formal ESDs. The SrWO4 atom coordinates are an isostructural analogue rather than an independently refined coordinate model, and the detailed WO3 symmetry remains the principal structural ambiguity.
