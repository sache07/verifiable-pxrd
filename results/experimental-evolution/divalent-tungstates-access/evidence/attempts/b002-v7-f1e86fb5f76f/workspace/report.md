# Powder XRD phase analysis

The accepted model contains three crystalline phases. Fractions are normalized over those modeled crystalline phases; no amorphous fraction was measured.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| MnWO4 | wolframite, P 2/c | 0.62557(89) |
| WO3 | monoclinic, P 21/n | 0.20377(74) |
| Mn2WO5 | monoclinic olivenite/sarkinite-type, P 21/n 1 1 | 0.17067(81) |

The parenthetical values are conditional GSAS-II standard uncertainties, not full systematic errors. The read-only forward replay of `final.gpx` over all 8301 points gives Rwp = 7.5941%, Rp = 4.9913%, and GOF = 3.8152. The larger GOF should be treated diagnostically because the input supplied counts but no pointwise standard uncertainties.

## Evidence

The WO3 + Mn3O4 precursor chemistry at 800 °C is consistent with a Mn-W-O product assemblage. Wolframite MnWO4 (COD 1520200) accounts for the dominant reflection families and refines to a = 4.79528, b = 5.70140, c = 4.97078 Å, beta = 91.1064°. Monoclinic WO3 (COD 1528915) accounts for the characteristic 23.1–24.3° family and refines to a = 7.29320, b = 7.53689, c = 7.68317 Å, beta = 90.9518°.

The remaining coherent families, including those near 31.78°, 35.15°, 46.48°, and 54.36°, are indexed by monoclinic Mn2WO5. No exact-composition reference was available in the frozen index, so this phase was built by composition substitution from the monoclinic Cu2AsO5 olivenite parent (COD 9011171). Symmetry-diverse Pnnm olivenite controls and a tetragonal natisite-type model were compared at equal development; the monoclinic basin was both better fitting and physically interior. Scheelite MnWO4 and h-MnO alternatives either predicted absent reflections or drove calibration/cell parameters to tested bounds. After accepting the three phases, the strong residual maxima all coincide with accepted-phase reflections; the weak feature near 25.43° is isolated and does not establish another phase.

The terminal model retained independently supported crystallite-size and preferred-orientation terms. Optional WO3 strain was removed after a simultaneous replay showed a 0.94 correlation with size and bound-seeking behavior. Surface roughness and extra calibration/profile terms were likewise rejected when pinned or inseparable. The required one-time bounded polish selected a converged heavy/light-coordinate branch with stable fractions and no fraction-collapse violation. A subsequent native GSAS-II replay changed no project parameters and raised no analytic profile flags.

## Remaining uncertainty

The Mn2WO5 composition and monoclinic metric are supported, but its detailed topology and coordinates are less secure than those of MnWO4 because they derive from a substituted analogue; the reported fraction therefore has systematic uncertainty larger than its conditional standard uncertainty.

Detailed WO3 oxygen positions are also not reliable. The 1960 reference reports oxygen coordinates at low precision, and the exported model retains an O–O contact of about 1.576 Å that is flagged for adjudication by an independent geometry screen. This does not undermine the monoclinic WO3 phase assignment, lattice, or its principal quantitative contribution, but the WO3 CIF should not be used as a precise local-geometry determination. Atomic displacement parameters were fixed at Uiso = 0.005 Å² because the powder data did not support their independent refinement.
