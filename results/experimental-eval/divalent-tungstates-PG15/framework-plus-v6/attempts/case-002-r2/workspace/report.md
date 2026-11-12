# Powder XRD phase analysis

The pattern is best described by five crystalline phases. Fractions below are normalized over the modeled crystalline material; no amorphous fraction was measured.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| Triclinic WO3 | P-1, COD 2106293; refined cell 7.32972, 7.52743, 7.69687 A, 88.9322, 90.6437, 90.6996 deg | 44.811% |
| BaO2 | I4/mmm, COD 1010113; refined cell a = 3.81270, c = 6.84928 A | 31.799% |
| Monoclinic WO3 | P21/c, COD 2311041; refined cell 7.69057, 7.54094, 10.52888 A, beta = 136.0722 deg | 22.862% |
| BaWO4 | I41/a, COD 1527204; source cell a = 5.614, c = 12.719 A | 0.321% (tentative) |
| BaO | Fm-3m, COD 1011362; source cell a = 5.496 A | 0.207% (tentative) |

## Evidence

The dense WO3 peak set, including the 23.4--24.7 deg triplet and independent middle- and high-angle families, requires both triclinic and monoclinic WO3. Adding the monoclinic record gave a stable positive scale, a physically small cell change from its source, and reduced the early common-profile Rwp from 8.38% to 7.30% before the final profile refinement. BaO2 accounts for the strong families near 26.3, 27.1, 33.5, 43.0, 46.6, and 55--56 deg. This inventory is chemically consistent with a largely unreacted BaO2/WO3 charge after only 200 deg C, with trace tungstate formation and BaO.

The trace assignments were re-challenged after rebuilding the common profile. From the final baseline (Rwp 5.76664%), omitting BaWO4 increased Rwp to 5.78172%, omitting BaO to 5.77368%, and omitting both to 5.78889%. BaO is supported by residual intensity around its 28.4, 32.9, 47.0, and 55.7 deg families. BaWO4 is supported mainly by partly overlapped families near 26.8, 43.3, and 69.2 deg; its nominally distinctive 32.2 deg feature is not cleanly resolved.

The final full-range fit has Rwp = 5.76664%, Rp = 4.38436%, and chi-square = 20824.57 using weights 1/max(counts, 1) over 8301 points. The 11-term Chebyshev background is smooth and nonnegative (about 190--2444 counts). Disabling the supported surface-roughness correction raises Rwp to 6.246%. Independent replay from `final.gpx` regenerated the same profile, fractions, and structures with no profile-review flags; `fit.csv` agrees with that replay to better than 5e-9 counts.

## Uncertainty and model limits

The two WO3 fractions are anti-correlated because many reflections overlap; their split is well supported as a two-polymorph model, but its systematic uncertainty is larger than the formal least-squares errors and is plausibly a few weight-percent. The BaWO4 and BaO fractions are below 0.4 wt% and should be treated as semiquantitative; neither their cells nor detailed atomic structures can be determined reliably from this pattern. Their source cells and published coordinates were therefore retained.

Restrained coordinate trials for the major phases hit bounds, became highly correlated, or diverged, so atomic coordinates could not be refined reliably. Submitted coordinates are the physically screened published models, while only the three major cells and tied isotropic displacement parameters were refined. Several width terms remain at the laboratory envelope, adding systematic uncertainty to fractions.

The BaO2 model contains a 1.315 A O--O contact, expected for a peroxide ion rather than an impossible oxide contact. The old BaWO4 record uses mutually exclusive half-occupied split oxygen sites separated by about 1.17 A; these are a disorder model and must not be interpreted as simultaneously occupied atoms. This disorder, together with the very low abundance, makes the detailed BaWO4 structure particularly uncertain.
