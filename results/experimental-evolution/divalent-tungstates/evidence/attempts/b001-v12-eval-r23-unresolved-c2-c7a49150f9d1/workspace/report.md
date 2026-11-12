# PXRD phase analysis

The pattern is described by three crystalline phases. Weight fractions are normalized over those modeled crystalline phases; no amorphous fraction was measured.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| CaWO4, scheelite | I41/a, COD 7219229 | 78.150 wt% |
| gamma-WO3 | P21/c, COD 2311041 (nonconventional cell setting) | 11.476 wt% |
| Ca3WO6 | P21/n analogue derived by Os6+ -> W6+ substitution in Ca3OsO6, COD 1562666 | 10.374 wt% |

The full-range final fit (9.9034–100.0946 degrees 2theta, 8,301 points) has Rwp = 2.641%, Rp = 2.025%, Rexp = 2.247%, and GOF = 1.178. The final save/reopen replay converged with no frozen variables and maximum shift/esd of 0.000067.

## Evidence

Scheelite CaWO4 accounts for the dominant families near 18.434, 28.54, 31.27, 39.03, 46.94, 54.11, 57.71, and 59.29 degrees. Monoclinic WO3 is required by its resolved 22.954/23.421/24.225 degree triplet and independent families in the 33–34, 41–42, 49–51, and 55–56 degree regions. Ca3WO6 is required by coherent families near 19.292, 22.019, 30.723, 32.169, 36.602, 37.537, 45.13, 50.8, and 55–57 degrees. Removing WO3 raises Rwp to 12.71%; removing Ca3WO6 raises it to 8.21%.

The retained WO3 record outperformed close exact-formula competitors under the same complete profile model: Rwp 2.643% for COD 2311041, versus 3.432% for monoclinic COD 1528915, 2.787% for triclinic COD 2106293, and 8.071% for orthorhombic COD 2107312. Width elaboration of the alternatives did not reverse the ranking without forcing a shared profile term to a boundary. For Ca3WO6, the simpler P21/n model also beat the lower-symmetry P21 analogue after cross-seeding and elaboration (best Rwp 2.641% versus 2.667%); the P21-only low-angle reflection had no supporting observed family.

Peak-shape checks were consistent across angle. Representative observed position/FWHM/left/right half-width values (degrees 2theta) are: CaWO4 18.434/0.217/0.105/0.112 and 46.936/0.304/0.134/0.171; WO3 22.954/0.166/0.083/0.083, 23.421/0.167/0.083/0.085, and 41.753/0.217/0.089/0.128; Ca3WO6 19.292/0.195/0.096/0.099 and 37.537/0.239/0.117/0.122. High-angle right shoulders track the modeled Cu Kalpha2 component; there was no repeated low-angle axial asymmetry, so SH/L was not released. The retained broadening terms are CaWO4 uniaxial size and Ca3WO6 isotropic size plus strain; WO3 phase-width trials were neutral or forced shared X to zero. A low-index CaWO4 [110] March-Dollase term was replay-stable, while texture trials for the minor phases remained neutral.

All retained source/adapted models and all final CIFs passed `learned/cif_health.py`. The metadata gives precursor identities (WO3 and CaO) but no precursor amounts or ratio, so no composition ratio was adjusted or imposed.

## Remaining uncertainty

The Ca3WO6 formula and reflection set are well supported, but its detailed atomic coordinates are not independently determined by this pattern: they remain an isovalent Ca3OsO6-derived analogue, with the cell, scale, and profile terms refined. Thus its exact atomic structure is less certain than its presence and approximate fraction.

A CaO control refined to about 0.12 wt%, but only its 31.97 degree line was noncoincident; all other calculated CaO families overlap retained-phase reflections, and its size challenge hit a boundary. It therefore fails the two-independent-family criterion and is not reported as a phase; a trace amount cannot be excluded or quantified reliably. Alternate same-formula phases either collapsed to zero scale or split fractions unstably under broadening challenges, so polymorph coexistence is not supported.

The quoted covariance esds in `result.json` are conditional, not full accuracy estimates: pointwise uncertainties and a calibrated instrumental profile were unavailable, and scale is correlated with polarization/roughness. Systematic fraction uncertainty is consequently larger than the formal esds. The analysis also does not quantify amorphous material.
