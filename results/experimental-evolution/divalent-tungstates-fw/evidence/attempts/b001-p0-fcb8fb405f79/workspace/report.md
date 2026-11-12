# Powder XRD phase analysis

The pattern is modeled with three crystalline phases. Fractions are normalized over those modeled crystalline phases; no amorphous fraction can be obtained without an external standard.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| CaWO4 | Scheelite, I41/a | 0.6967 (69.67 wt%) |
| WO3 | Monoclinic, P21/c | 0.1596 (15.96 wt%) |
| Ca3WO6 | Ordered double perovskite, P21/c setting | 0.1436 (14.36 wt%) |

The dominant scheelite CaWO4 reflections account for the principal peaks and are chemically expected from CaO + WO3 at 800 °C. Monoclinic WO3 accounts for the remaining precursor-like multiplets. Peaks near 19.35, 22.04, 31.46, 36.5–37, 45.07, 50.7 and 56.85° 2theta require the ordered Ca3WO6 model. A CaWO4 + WO3 + CaO trial left these peaks unmodeled (Rwp about 11.7%); the CaO scale collapses when Ca3WO6 is included, so CaO is not reported as a resolved crystalline phase.

CaWO4 was initialized from COD 7219229 and WO3 from COD 2311041. The available reference set did not contain Ca3WO6. Its model was constructed by replacing Mg with Ca in the isostructural double-perovskite Ca2MgWO6 model (COD 2013468), followed by refinement of the lattice and atomic coordinates. Independent Ca/Co and Sr/Ca tungstate analogue starts converged to the same Ca3WO6 framework, supporting the assignment. All three final CIFs pass the contact/occupancy screen; representative shortest bonds are W–O = 1.759 Å in CaWO4, 1.709 Å in WO3, and 1.884 Å in Ca3WO6.

An independent, no-optimization GSAS-II replay of `final.gpx` over all 8301 measured points gives Rwp = 3.6009%, Rp = 2.8162%, and goodness of fit = 1.3828. The replay generated no negative-background, negative-width, or displacement-parameter review flags. The refined profile includes preferred orientation for WO3 ([001], March ratio 0.824) and weak Ca3WO6 texture ([111], ratio 0.963), plus specimen surface roughness and displacement.

The phase identities and approximate fractions are reliable. The formal GSAS-II fraction e.s.d. values are about 0.14, 0.08 and 0.12 wt% for CaWO4, WO3 and Ca3WO6, respectively, but they omit model systematics; a more realistic uncertainty is roughly 1–2 wt percentage points because surface roughness, texture, scale and profile terms are correlated. The Ca3WO6 topology, cell and cation ordering are well supported, while its oxygen coordinates are less certain because it is a 14 wt% analogue-derived phase and laboratory X-ray data are dominated by W scattering. Crystallite size and instrument Lorentzian broadening are also strongly correlated and should not be interpreted quantitatively from this refinement.
