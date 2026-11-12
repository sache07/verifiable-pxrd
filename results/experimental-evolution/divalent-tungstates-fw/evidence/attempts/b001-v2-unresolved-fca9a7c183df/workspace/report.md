# Powder X-ray diffraction result

The crystalline sample is modeled as wolframite ZnWO4, residual wurtzite ZnO, and residual monoclinic WO3. Fractions are normalized only over these modeled crystalline phases.

| Phase | Space group | Refined cell | Weight fraction |
|---|---|---|---:|
| ZnWO4 | P 2/c | a = 4.70236, b = 5.73152, c = 4.93905 A; beta = 90.6540 deg | 73.56% |
| ZnO | P 63 m c | a = 3.25241, c = 5.20746 A | 7.67% |
| WO3 | P 21/c | a = 7.68868, b = 7.54333, c = 10.51737 A; beta = 136.0442 deg | 18.78% |

## Evidence and model selection

The ZnO and WO3 assignments are consistent with the stated ZnO/WO3 precursor chemistry, while the dominant new line family is indexed by wolframite ZnWO4. Distinct ZnO lines near 34.5, 47.8, 56.9, 63.2, and 68.2 deg and WO3 lines near 23.5, 26.9, 29.0, 29.3, 33.6, and 33.9 deg remain as coherent families rather than isolated residuals. In final cumulative deletion tests, removing ZnWO4, ZnO, or WO3 increased Rwp from 6.05% to 35.47%, 8.26%, or 19.05%, respectively. All three phases are therefore supported.

The ZnWO4 starting model came from public filtered-COD entry 9005254: its mixed Cu/Zn wolframite site was chemically collapsed to Zn. Cd-, Mg-, and Mn-wolframite analogues were compared under the same low-flexibility and cumulative refinement sequence. Wurtzite ZnO (COD 9004178) was preferred over zincblende and rocksalt alternatives. For WO3, the selected physically screened P21/c parent (COD 2311041) was compared with P-1, Pnma, and other P21/c models. Reduced tungsten oxides and ordered multication Zn3WO6-derived frameworks did not acquire a supported positive contribution.

## Refinement and checks

The mechanism-complete profile pass tested background families/orders, zero and specimen-displacement branches, common width and axial-divergence terms, polarization, roughness, crystallite size, microstrain, and texture for each phase. The retained model uses a six-term Chebyshev background, a stable zero-only calibration branch, common Gaussian width and axial divergence, phase-specific broadening, and a supported [010] March-Dollase term for WO3. Roughness and extra anisotropic broadening terms were rejected when improvements were negligible, branch-dependent, or drove parameters to nonphysical limits.

Atomic refinement was performed last and selectively. ZnWO4 W/O coordinates and W isotropic displacement, plus the two WO3 W positions, gave repeatable intensity improvements across nuisance restarts. ZnO coordinates and WO3 oxygen-coordinate refinement were not retained. The exported structures have minimum metal-O distances of 1.888 A (ZnWO4), 1.976 A (ZnO), and 1.641 A (WO3); minimum O-O distances are 2.306 A in ZnWO4 and 2.540 A in WO3.

An independent read-only replay of `final.gpx`, regenerating reflections and ignoring cached calculated arrays, reproduced the full 8,301-point profile with Rwp = 6.05048%, Rp = 4.01170%, Rexp = 2.68518%, and goodness of fit = 2.25328. It reported no negative-background, negative-width, out-of-range polarization, or negative-ADP flags. The replayed fractions and CIF models agree with the submitted files.

## Remaining uncertainty

The P-1 WO3 finalist gave a slightly lower matched pre-atomic profile Rwp (about 6.80% versus 6.87%) but used lower symmetry and additional lattice freedom; this small advantage was not sufficient to displace the physically credible P21/c model. Consequently, the exact WO3 distortion/polymorph is less secure than its presence and approximate abundance. WO3 oxygen-coordinate trials, including restrained trials, generated implausibly short O-O contacts, so those coordinates are not determined reliably by this pattern and remain at the parent values.

The largest remaining structured mismatch is around the strongest overlapping low-angle peak near 24.7 deg, and the counting-statistical floor is not reached. Zero and axial divergence are strongly correlated, although independent valid starts reproduced the curve, structures, and fractions. The numerical fractions are data-refined and stable across those starts, but sub-percent absolute accuracy is not justified because profile/texture/model systematics dominate. No amorphous fraction can be determined from this analysis; the reported fractions apply only to the modeled crystalline inventory.
