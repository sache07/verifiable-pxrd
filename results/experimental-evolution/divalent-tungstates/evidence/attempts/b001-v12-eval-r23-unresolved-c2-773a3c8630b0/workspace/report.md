# PXRD phase analysis

Three crystalline phases are required by the full 9.9034–100.0946° 2θ pattern.

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| SrWO₄ | scheelite, *I*4₁/*a*; a = 5.39313 Å, c = 11.89984 Å | 0.58980 (14) |
| WO₃ | monoclinic, *P*2₁/*c*; a = 7.69326 Å, b = 7.55514 Å, c = 10.51402 Å, β = 136.1168° (source setting) | 0.25215 (11) |
| SrCO₃ | strontianite, *Pnma*; a = 6.02303 Å, b = 5.09740 Å, c = 8.39414 Å | 0.15805 (14) |

Fractions are normalized over the modeled crystalline phases and sum to 1. The final full-range fit has Rwp = 3.4005%, Rp = 2.6024%, and GOF = 1.1905 for 8301 observations and 28 refined variables.

## Evidence

The dominant peak families index as scheelite SrWO₄, including 101, 112, 004, 200, 211, 204, 220, 116, 312, 224, 316, 332, 424, and 512. Because the supplied structure library had no exact SrWO₄ entry, the submitted model was constructed from isostructural SrMoO₄ (COD 2300460) by the isovalent Mo→W substitution. Scheelite CaWO₄/BaWO₄ parents and a fergusonite CaWO₄ model were also inspected; the scheelite topology and tetragonal metric were clearly preferred.

Residual families are explained by unreacted monoclinic WO₃ and orthorhombic SrCO₃. SrCO₃ is supported by independent Pnma families near 24.62°, 25.26°, 36.03°, 43.61°, 47.23°, and higher angles, not by a single coincident line. Removing WO₃ raises Rwp to 10.63%; removing SrCO₃ raises it to 4.93%. A rhombohedral SrCO₃ competitor refined to a scale smaller than its uncertainty and collapsed on replay. The exact-formula Sr₃W₂O₉ watch model collapsed to a 10⁻¹² scale and was rejected.

Several physical WO₃ records and polymorphs were compared from common checkpoints. The submitted health-passing P2₁/c record (COD 2311041) remained better after profile and signed-axis texture challenges than the triclinic P−1 and alternate P2₁/n records. The final broadening is isotropic WO₃ microstrain, 4668(100) µstrain; size, strain, and combined trials for every retained phase were replayed, with unsupported or bounded terms removed. Low-index March–Dollase terms were retained only where removal caused a reproducible loss: SrWO₄ [111], WO₃ [10−1] in the submitted setting, and SrCO₃ [001].

The reported Cu Kα₂/Kα₁ ratio of 0.500 was retained; a free challenge gave approximately 0.505, whereas a Kα₁-only profile was substantially worse. The refined phase amounts give an overall Sr:W molar ratio of 0.994 and residual SrCO₃:WO₃ molar ratio of 0.984, consistent with incomplete reaction of an approximately 1:1 precursor mixture. All three exported CIFs pass `learned/cif_health.py` with ordered, fully occupied sites and no hard contacts.

## Remaining uncertainty

The parent structures' atomic coordinates were retained while cells were refined. Thus the SrWO₄ scheelite topology and the phase identities are reliable, but subtle oxygen displacements—especially the exact local WO₃ distortion—are not uniquely determined by this multiphase pattern. Preferred orientation is substantial, and the one-parameter surface-roughness correction remains about 96% correlated with the dominant-phase scale. There is also no calibrated instrumental profile, supplied pointwise uncertainty, or internal standard. Consequently, the parenthetical fraction uncertainties are formal GSAS-II e.s.d.s and understate model-dependent systematic error; a few weight percent is a more realistic caution. The fractions do not include amorphous material, whose amount cannot be determined from these data.
