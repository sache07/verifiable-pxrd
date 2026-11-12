# PXRD phase analysis and refinement report

## Result

The pattern is modeled as three crystalline phases. Weight fractions are normalized over those modeled crystalline phases only.

| Phase | Structure | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO4 (scheelite) | I 41/a, no. 88 | a = 5.39314, c = 11.89994 | 58.96(14) wt% |
| WO3 (monoclinic) | P 21/c, no. 14, alternate setting | a = 7.69338, b = 7.55509, c = 10.51392, beta = 136.1156 | 25.01(11) wt% |
| SrCO3 (strontianite) | Pnma, no. 62 | a = 6.02377, b = 5.09736, c = 8.39402 | 16.03(15) wt% |

The final full-range fit (9.903–100.095° 2theta, 8301 points) has Rwp = 3.551%, Rp = 2.728%, Rexp = 2.861%, and GOF = 1.243. The values in parentheses above are GSAS-II least-squares standard uncertainties in the last two digits; they do not include model or specimen-systematic uncertainty.

## Evidence and model selection

The chemistry is consistent with partial reaction of the reported WO3 and SrCO3 precursors at 650 °C to form scheelite SrWO4, leaving both precursors. SrWO4 is supported by its 112/004/200 families at 27.176/29.428/32.616° and many independent mid- and high-angle families. Monoclinic WO3 contributes the resolved 22.513/22.939/23.815° triplet and independent families near 33.0–33.6°, 46.7–49.5°, and 54.9–55.6°. Pnma SrCO3 is supported by the 111/102 pair at 24.616/25.262° and repeated families at 34.607/36.032°, 43.613/46.091°, and 49.425/49.788°. Thus, each retained phase has multiple coherent families, not merely one overlapped line.

No exact SrWO4 entry was available in the supplied index. A stoichiometric-analogue search was therefore used. The SrMoO4 scheelite record COD 2300460 was selected because it preserves the exact Sr sublattice and permits the isovalent Mo6+ to W6+ substitution; its oxygen geometry was physically sound. A BaWO4 alternative contained split half-occupied oxygen sites and an implausibly short contact in the supplied record. Only the SrWO4 cell was refined; its atom coordinates remain those of the physically screened analogue. The exported model has a shortest W–O distance of 1.727 Å and density 6.44 g cm-3.

For WO3, COD 2311041 (P 21/c, alternate cell setting) was selected. Under the same neutral profile, broadening, and texture-axis screen, its Rwp was 3.551%, compared with 3.607% for triclinic COD 2106293 and 3.665% for conventional-setting monoclinic COD 1528915. The selected model also avoids the two extra cell-angle freedoms of the triclinic description. The alternate monoclinic setting has beta about 136° but is equivalent to the familiar near-orthogonal gamma-WO3 cell. Orthorhombic and high-pressure records fitted substantially worse in the preliminary physical/source screen. The final WO3 geometry is sound (shortest W–O 1.718 Å; density 7.27 g cm-3).

Pnma SrCO3 uses COD 9008198. A high-temperature rhombohedral SrCO3 watch phase refined to 0.02(13) wt% and was rejected. High-pressure Sr3W2O9 refined to the scale lower bound (about 10^-12) and lacked its expected unique low-angle families. Adding a second, symmetry-equivalent WO3 record produced scale splitting, but single-record replays showed that this was duplicate structure-factor mixing rather than reliable evidence for another phase; no separate WO3-polymorph fraction is reported.

## Refinement controls

The Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio were fixed to the metadata. The common profile used a smooth five-term Chebyshev background, one specimen-shift correction (+1056.6 micrometres in GSAS-II convention), refined polarization (0.7525), and a nonnegative low-dimensional profile with U = 0, W = 39.909, and X = 4.043. Zero, transparency, roughness, V, Y, and Z were fixed at neutral values. Phase size was fixed at the effectively neutral GSAS-II upper value (10 micrometres), and SrWO4/SrCO3 strain refined back to zero. WO3 alone required replay-stable isotropic microstrain, 4416 ± 103 microstrain; adding WO3 size returned to the neutral bound.

March–Dollase texture was supported by multiple families and retained for SrWO4 [111] (0.6863), WO3 [10-1] (1.2537), and SrCO3 [001] (0.8285). Removing those terms separately raised Rwp to 5.271%, 5.002%, and 3.639%, respectively; competing axial and diagonal directions fitted worse. An SH/L trial refined to about 0.0144 but improved Rwp by only 0.004 percentage point and was 95.7% correlated with specimen shift, so it was pruned and fixed at 0.002. The final project was saved, reopened, replayed over the full range, and then used directly for all CIF and profile exports.

## Remaining uncertainty

The phase identities and three-phase inventory are well supported, but the quoted fraction uncertainties are statistical only. Preferred orientation is strong, the instrument profile was not independently calibrated, and the specimen displacement is large; a realistic systematic uncertainty in individual fractions is likely on the order of 1–3 absolute wt%, not the smaller formal values. The fractions do not quantify amorphous material or any phase below the pattern/model detection limit.

Atomic coordinates and displacement parameters were not independently refined: laboratory powder intensities, texture, and the close WO3 polymorph alternatives make such refinement underdetermined without restraints or higher-resolution data. Residual intensity mismatch remains in parts of the WO3 22.5–23.8° cluster and some mid-angle peaks. Consequently, the selected monoclinic WO3 record is preferred but subtle local distortion, defects, or a trace unresolved WO3 variant cannot be quantified reliably from this scan.
