# PXRD phase analysis

## Result

The pattern is modeled by three crystalline phases. Fractions are normalized over these phases only.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| CaWO4 | scheelite, I 41/a | 0.78269(59) |
| WO3 | monoclinic, P 21/c | 0.11556(34) |
| Ca3WO6 | P 21/n analogue model | 0.10175(53) |

The full-range replay over 9.9034–100.0946 degrees 2theta converged with Rwp = 2.8590%, Rp = 2.2236%, Rexp = 2.2469%, and goodness of fit = 1.2746 (8,301 points, 29 refined variables). The supplied intensities are raw counts without pointwise uncertainties, so Poisson uncertainties, sigma = sqrt(counts), were used. The parenthetical fraction uncertainties are conditional least-squares estimates and do not include phase-model or other systematic uncertainty.

## Phase evidence and source choice

Scheelite CaWO4 accounts for its characteristic independent families near 18.4, 28.5, 31.2, 34.0, 39.0, and 46.9 degrees. Its refined cell is a = 5.24219 A and c = 11.37595 A. Monoclinic WO3 accounts for the diagnostic 22.9/23.4/24.2 degree group and further families near 26.4 and 33.1–33.4 degrees. Its refined source-setting cell is a = 7.68253 A, b = 7.53164 A, c = 10.50426 A, beta = 136.0695 degrees.

Those two phases left coherent families near 18.7, 19.3, 22.0, 30.7, 31.4, 37.5, 45.1, and 57.0 degrees. Charge-balanced non-1:1 Ca-W-O formulas were therefore enumerated and searched with `learned/stoichiometric_analogues.py`. A Ca3OsO6 parent (COD 1562666, P 21/n) gave a chemically direct, isovalent Os(VI)-to-W(VI) substitution with the same ordered Ca/O framework. The resulting Ca3WO6 model explains these independent families with a positive replay-stable scale; its refined cell is a = 5.53280 A, b = 5.78131 A, c = 8.01203 A, beta = 90.0662 degrees.

Structurally distinct WO3 records were given matched opportunities. In the neutral three-phase comparison, COD 2311041 gave Rwp = 12.5708%, versus 12.6000% for a triclinic record and 12.6414% for another monoclinic record. After cross-seeding shared nuisance terms and applying each source's compact texture leader, all branches were bound-free. In the final polarized comparison, retained COD 2311041 gave Rwp = 2.8590%, while the lower-symmetry triclinic source gave 2.9988%. Thus lower symmetry did not win either required comparison.

## Refinement and challenge results

The retained model uses an eight-coefficient Chebyshev background, phase scales and cells, one common zero correction, nonnegative common U/W terms, isotropic phase sizes, a CaWO4 [110] March-Dollase term, and refined polarization (0.87336). Fixing polarization at 0.5 worsened Rwp to 6.7929%; reducing the background to six coefficients worsened it to 3.3496%. A combined roughness branch froze a parameter and had a >99% roughness-parameter correlation, so roughness was restored to zero. Strain, X, V/Y/Z, asymmetry, and minor-phase texture were unsupported and are literal neutral values. Deleting the CaWO4 texture, WO3 size, or Ca3WO6 size increased Rwp to 6.2163%, 2.9368%, and 3.0252%, respectively; the CaWO4 size deletion was unstable and much worse.

CaO was retested only after the three-phase inventory had converged. It refined to a conditional 0.00126(38) fraction and changed Rwp by only 0.0019 percentage point. Its strongest 200 line near 37.10 degrees did not improve the local fit, while the small gains came mainly from coincident or very weak lines. It therefore lacks two independent non-coincident families and is not retained; a CaO fraction cannot be reported reliably. No same-formula phase coexistence was supported.

## Remaining uncertainty

All three submitted CIFs pass `learned/cif_health.py`. The CaWO4 and WO3 assignments and the three phase fractions are robust within this crystalline model. Ca3WO6 is supported as a diffraction phase and charge-balanced topology, but its atomic coordinates and displacement parameters are inherited from the Ca3OsO6 analogue; only its cell, scale, and profile terms were refined. Its detailed atomic structure is therefore not independently determined by this powder pattern. No amorphous fraction was measured, so the reported fractions must not be interpreted as absolute bulk fractions if amorphous material is present.
