# PXRD phase analysis

## Result

The crystalline sample is modeled as scheelite SrWO4 plus unreacted WO3 and SrCO3. Fractions are normalized only over these modeled crystalline phases.

| Phase | Structural model | Refined cell | Weight fraction |
|---|---|---|---:|
| SrWO4 | tetragonal, *I*41/*a* | *a* = 5.393095(9), *c* = 11.900037(20) Å | 0.61889 (61.89 wt%) |
| WO3 | triclinic, *P*-1 | *a* = 7.289106(21), *b* = 7.555189(30), *c* = 7.694648(50) Å; α = 89.9483(11)°, β = 90.8913(7)°, γ = 90.1213(23)° | 0.23556 (23.56 wt%) |
| SrCO3 | orthorhombic, *Pnma* | *a* = 6.024963(70), *b* = 5.097069(50), *c* = 8.393286(57) Å | 0.14554 (14.55 wt%) |

The full-range replay (9.9034–100.0946° 2θ; 8,301 points) gives Rwp = 3.271%, Rp = 2.563%, Rexp = 2.861%, and goodness-of-fit = 1.146. The reopened project converged with no SVD zeros, maximum shift/esd 0.004, and no parameter correlations above 0.90.

## Evidence and model selection

The chemistry is consistent with reaction of the reported WO3 and SrCO3 precursors to SrWO4, with both precursors remaining crystalline. No precursor amounts or ratio were supplied, so no mass-balance or conversion constraint was imposed or varied.

- Removing SrWO4 produces Rwp 22.42% and an invalid negative-X profile surrogate; removing WO3 gives Rwp 10.30%; removing SrCO3 gives Rwp 4.76%, versus 3.27% for the retained inventory.
- SrCO3 has multiple independent, non-coincident families. Removing it increases local weighted residuals by factors of about 70 at 24.35–24.85° (111), 62 at 25.05–25.48° (102), 39 at 35.82–36.25°, and 27 at 43.40–43.85°. Its positive scale and approximately 14.5 wt% fraction survived every profile and inventory replay.
- The SrWO4 coordinates came from a health-passing scheelite CaWO4 record (COD 7219229), with the chemically justified Ca2+→Sr2+ substitution. A health-passing SrMoO4 analogue was also tested but fit less well under matched terms.
- The selected WO3 source is the health-passing triclinic record COD 2106293. Its matched, converged model gives Rwp 3.27%, compared with 4.05% for the best health-passing monoclinic *P*21/*c* competitor (COD 2311041). The triclinic model halves the weighted residual over the 32.35–33.90° split family, reduces it by 40% over 49.00–50.45°, and reproduces the observed 86.707/86.979° high-angle doublet at 86.707/86.968°. Its three refined angles differ from 90° by approximately 4.7, 133, and 5.3 standard uncertainties. The advantage remains after independent texture, broadening, background, polarization, and profile replays.
- One WO3 family at 54.7–55.9° is slightly better with the monoclinic model. Thus triclinic WO3 is the preferred assignment, but the exact WO3 polymorph is not completely unique from this laboratory pattern. Importantly, replacing it with the monoclinic competitor changes each phase fraction by less than 0.1 percentage point.
- Tetragonal, orthorhombic, hexagonal, and alternate monoclinic WO3 records were tested. Structurally defective/review records were rejected against passing alternates; Sr3W2O9 was rejected because its scale collapsed to zero.

All retained source models and all final CIFs were screened with `learned/cif_health.py`. The final CIFs pass: they are ordered, have full valid occupancies, and contain no hard contacts or parser warnings.

## Profile and peak-shape audit

The retained common profile has nonnegative W = 39.436 and X = 3.463, with U fixed at 1; a single effective sample-shift correction refined to 1.057 mm. The 14-term background is smooth and positive (1008–1037 counts). Surface roughness was rejected because it correlated 96% with the dominant scale. Adding U gave only a 0.002-point Rwp gain, and every crystallite-size trial reached a bound. Supported terms are uniaxial strain for SrWO4 along [001], uniaxial strain for WO3 along [010], and one low-index March–Dollase term per phase. SrCO3 broadening was kept neutral.

Empirical positions and widths below are from smoothed local observed/calculated envelopes. Each width is FWHM with left/right half-widths in parentheses, in degrees 2θ.

| Phase/family | Observed position; FWHM (L/R) | Calculated position; FWHM (L/R) |
|---|---|---|
| SrWO4 011, low | 17.466; 0.174 (0.093/0.080) | 17.456; 0.175 (0.083/0.092) |
| SrWO4 024, middle | 44.817; 0.214 (0.095/0.119) | 44.817; 0.210 (0.095/0.116) |
| SrWO4 136/316, high | 72.646; 0.168 (0.093/0.076) | 72.635; 0.152 (0.075/0.077) |
| WO3 020, low | 22.943; 0.196 (0.091/0.105) | 22.954; 0.204 (0.103/0.101) |
| WO3 2-20/202/220, middle | 33.614; 0.229 (0.126/0.102) | 33.592; 0.236 (0.111/0.125) |
| WO3/SrWO4 high-angle doublet | 86.707 and 86.979; primary 0.199 (0.099/0.100) | 86.707 and 86.968; primary 0.187 (0.094/0.093) |
| SrCO3 111, low | 24.649; 0.183 (0.109/0.074) | 24.627; 0.179 (0.083/0.096) |
| SrCO3 203/122, middle | 43.676; 0.195 (0.102/0.093) | 43.654; 0.199 (0.078/0.121) |
| SrCO3 413/331, high | 73.298; 0.158 (0.081/0.077) | 73.287; 0.274 (0.090/0.184) |

The weak high-angle SrCO3 family is noisy and its width is not reproduced reliably; it was not used to justify extra broadening. The high-angle WO3 family overlaps strong SrWO4 scattering, so its individual WO3 FWHM is likewise not independently determined. Low- and middle-angle families provide the reliable phase evidence.

## Remaining uncertainty

The quoted fraction standard uncertainties in `result.json` are covariance-only and are smaller than likely systematic uncertainty from preferred orientation, absorption/intensity corrections, source choice, and the effective displacement correction. The fractions are reliable as a normalized three-crystalline-phase result, but an absolute bulk fraction cannot be determined because no amorphous standard was measured. Atomic coordinates were retained from health-passing source/analogue structures; only cells, scales, and supported profile terms were refined, so this analysis identifies structural models rather than independently redetermining atomic positions.
