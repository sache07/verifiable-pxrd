# Quantitative phase analysis

The pattern is modeled as three crystalline phases. Fractions are normalized over those modeled crystalline phases only.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MgWO₄ (wolframite) | P2/c, COD 9013902 | a = 4.69031, b = 5.67490, c = 4.92928, β = 90.77510 | 77.09 wt% |
| MgO (periclase) | Fm-3m, COD 9000499 | a = 4.21301 | 7.06 wt% |
| WO₃ | P-1, COD 2106293 | a = 7.30452, b = 7.53726, c = 7.69013; α = 89.87056, β = 90.82853, γ = 90.06127 | 15.85 wt% |

The covariance-derived standard uncertainties are 0.123, 0.105, and 0.093 wt% for MgWO₄, MgO, and WO₃, respectively. These are formal errors and do not include structural-model uncertainty.

## Evidence and phase selection

The MgO + WO₃ precursor context, peak positions, and complete reflection families support wolframite MgWO₄ as the reaction product with residual MgO and WO₃. The remaining exact Mg–W–O database entries were a malformed duplicate MgWO₄ record and MgWO₄·2H₂O, the latter being incompatible with the reported 900 °C treatment; neither supplies an unexplained peak family. Nested deletions from the final common model increased Rwp from 6.042% to 7.348% without MgO, 17.652% without WO₃, and 18.144% for MgWO₄ alone. Both residual precursors are therefore required and are not background/scale surrogates.

Multiple physical WO₃ records were challenged. Initial restrained fits rejected orthorhombic Pnma (Rwp 10.83%) and tetragonal P4/ncc (15.12%). The serious alternatives were monoclinic P2₁/c (COD 2311041, equivalently transformed to P2₁/n) and triclinic P-1 (COD 2106293). Both source records contained zero displacement-parameter placeholders. After replacing those with the same one-parameter positive common WO₃ Uiso model and applying identical isotropic-strain and texture tests, P-1 gave Rwp = 6.0415% versus 6.1070% for P2₁/n. The associated χ² reduction was about 737 for two additional metric parameters, so P-1 is selected. WO₃ chemistry is secure, but its exact low-symmetry polymorph remains less certain than the phase identity because measurement temperature was not supplied and the monoclinic model is still close.

All sites are fully occupied and the geometries are physical. MgWO₄ has six Mg–O contacts at 2.049–2.170 Å and six W–O contacts at 1.779–2.130 Å. The four independent W sites in triclinic WO₃ each remain six-coordinate, with W–O distances spanning 1.714–2.218 Å. MgO gives six Mg–O contacts at 2.107 Å. Positional coordinates were held at their literature values; this overlapping laboratory pattern does not support an independent coordinate refinement. A single common WO₃ Uiso = 0.01584(74) Å² was refined because separate O/W terms were not identifiable (the oxygen term collapsed to its bound).

## Refinement and uncertainty

The final GSAS-II model uses the reported Cu Kα1/Kα2 wavelengths and fixed 0.5 intensity ratio, an eight-term smooth Chebyshev background, one specimen-displacement correction, nonnegative common U/X width terms, one SH/L asymmetry term, and one low-angle roughness term. Unused size, H-strain, extinction, Babinet, and phase-specific broadening terms were neutralized. Only isotropic WO₃ microstrain, 691(86) µstrain, was retained. Mild March–Dollase terms for MgWO₄ [001], 0.9877 ± 0.0012, and WO₃ [010], 1.0284 ± 0.0028, were independently supported: deleting strain, MgWO₄ texture, or WO₃ texture raised Rwp to 6.0650%, 6.0828%, and 6.0803%, respectively. No coherent unassigned reflection family remains.

The final fit over the requested 10–100° 2θ range has Rwp = 6.0415%, Rp = 4.4170%, Rexp = 2.8639%, and goodness-of-fit = 2.1096. Pointwise uncertainties were not supplied, so count-derived statistical weights were used. The competitive WO₃ models shift its fraction by about 0.9 wt% (and MgWO₄ by about 0.8 wt%), which is a more realistic model-related uncertainty than the formal covariance values. With no external standard, amorphous material and undetected trace phases cannot be quantified; these fractions are not absolute bulk fractions if such material is present.

The submitted CIFs, profile, fractions, and statistics were exported directly from `final.gpx` after two reopen/replay cycles (maximum shift/esd 0.009 then 0.001; no frozen variables).
