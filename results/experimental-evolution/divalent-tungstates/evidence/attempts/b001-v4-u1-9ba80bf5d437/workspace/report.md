# PXRD phase analysis

The pattern is modeled by three crystalline phases: scheelite SrWO4 product, monoclinic WO3, and orthorhombic SrCO3 (strontianite). This is chemically consistent with incomplete reaction of the stated WO3 + SrCO3 precursors after heating at 650 °C.

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| SrWO4 | I 41/a | a = 5.383792, c = 11.879949 | 62.186(16)% |
| WO3 | P 21/n | a = 7.276600, b = 7.541577, c = 7.681067, beta = 90.8822 | 22.873(12)% |
| SrCO3 | Pnma | a = 6.011124, b = 5.089376, c = 8.379709 | 14.942(16)% |

Parentheses are GSAS-II formal standard uncertainties. Fractions sum to 100% over the modeled crystalline phases; amorphous material is not measured by this normalization.

## Identification and physical inventory

The diagnostic peak families are jointly explained by scheelite SrWO4 (including the strong low-angle line near 17.4° and families near 27–33°, 44–48°, and 55.5°), monoclinic WO3 (notably the 22.5–23.8° multiplet), and strontianite SrCO3 (including the 24.6/25.3° pair). Their presence also closes the expected product/residual-precursor balance.

No exact SrWO4 record was present in the supplied index. A stoichiometric-analogue search was therefore run and several parents were screened with the same provisional nuisance schedule. The accepted model is COD 7219229, a 298 K X-ray scheelite CaWO4 structure, with the chemically direct Ca-to-Sr substitution and a refined SrWO4 cell. EuWO4- and SrMoO4-derived scheelites fit less well and gave less satisfactory local geometry; a pressure-type fergusonite CaWO4 parent drove its scale to the lower bound. The final substituted structure is fully occupied and has four W–O bonds of 1.819 Å and eight Sr–O bonds of 2.545–2.560 Å.

For WO3, COD 2311041 (a neutron-diffraction monoclinic structure; the CIF does not state a measurement temperature) outperformed tested triclinic, alternative monoclinic, and tetragonal records. It was transformed exactly to the conventional P21/n setting before the final pass. Its fully occupied, distorted WO6 octahedra have six W–O distances of 1.715–2.159 Å. For SrCO3, the published strontianite record COD 9008198 was retained (its CIF also gives no explicit measurement temperature); the high-temperature/disordered R-3m alternative lost its scale. The final carbonate has C–O = 1.289–1.302 Å and nine-coordinate Sr–O = 2.562–2.728 Å. Added or replacement Sr3W2O9 models also lost their scale and their unique lines were unsupported.

Only cells, scales, and justified profile/intensity terms were refined; atomic coordinates were held to the screened literature/prototype values. In particular, an unrestrained SrWO4 oxygen-coordinate branch lowered the residual but lengthened W–O to about 2.018 Å and shortened Sr–O to 2.411–2.477 Å, so it was rejected as an intensity surrogate. The precise SrWO4 oxygen coordinates are therefore not independently determined by this powder pattern.

## Final profile and evidence

The clean final pass used all 8,301 points from 9.9034–100.0946° 2theta, the supplied Cu Kalpha1/Kalpha2 wavelengths and ratio, a 10-term Chebyshev background, and Poisson working weights because pointwise uncertainties were not supplied. The sole angular correction is zero = -0.63654°. The common nonnegative peak profile retained W and X; U and bounded SH/L trials went to their lower bounds and were rejected. Size-only and strain-only branches were challenged for every phase. Only isotropic WO3 size remained reproducible, 0.14793(41) micrometres; all strain terms and the initially marginal SrCO3 size term were pruned after texture was introduced.

March–Dollase tests against symmetry-distinct axes retained SrWO4 [110] = 0.73501(21), WO3 [001] = 1.26548(47), and SrCO3 [001] = 0.8313(92). The carbonate term improves several separate families (111, 102, 013/202, and 104), rather than one overlap. Extinction, roughness, displacement/transparency, and atomic-coordinate branches were rejected or left neutral.

The final full-range save/reopen replay converged with Rwp = 4.1392%, Rp = 3.0829%, Rexp = 2.8612%, GOF = 1.4492, and no frozen variables. The only correlation above |0.8| is common W versus X (-0.870). Reopening `final.gpx` reproduces the exported fractions and profile. The largest residuals occur on already assigned SrWO4 and WO3 families around 17.4°, 22.9–23.8°, 32.6–32.7°, and 55.5°; no coherent extra-phase family remains.

## Remaining uncertainty

Phase identities are well supported, but the formal fraction uncertainties are optimistic because the data supplied no standard uncertainties, preferred orientation is substantial, peaks overlap, and the SrWO4 coordinates come from a substituted prototype. A practical uncertainty of roughly 1–3 absolute wt% per phase is more realistic than the formal values. The crystalline fractions do not constrain any amorphous fraction, and the fixed atomic coordinates should not be interpreted as a new structure determination.
