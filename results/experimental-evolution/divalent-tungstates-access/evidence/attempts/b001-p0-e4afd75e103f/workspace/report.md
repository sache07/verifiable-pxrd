# Powder XRD phase analysis

The pattern is modeled by three crystalline phases. Weight fractions are normalized over those phases only.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CaWO₄, scheelite | *I*4₁/*a* (No. 88) | *a* = 5.23828, *c* = 11.33570 | 78.64(17) wt% |
| WO₃, monoclinic | *P*2₁/*n* (No. 14) | *a* = 7.31317, *b* = 7.55595, *c* = 7.69179, β = 91.0473 | 15.57(7) wt% |
| CaCO₃, calcite | *R*-3*c* (No. 167) | *a* = 4.98424, *c* = 17.06858 | 5.80(19) wt% |

The numbers in parentheses are internal GSAS-II least-squares standard uncertainties in the last quoted digits. They do not include phase-model, background, absorption, or microabsorption systematics.

## Evidence and refinement

Candidate structures consistent with the CaCO₃ + WO₃, 650 °C context were screened against the complete pattern, then refined by whole-pattern Rietveld fitting in GSAS-II. Published COD models 7219229 (scheelite CaWO₄), 1528915 (monoclinic WO₃), and 1547347 (calcite) supplied the starting atomic models. The final calculation uses the stated Cu Kα₁/Kα₂ doublet, a specimen-displacement/zero correction, a smooth log-interpolated background, and bounded phase/instrument broadening terms.

CaWO₄ accounts for the dominant lines near 18.3, 28.4, 31.2, 33.9, and 46.9° 2θ. Monoclinic WO₃ is required by the distinctive 22.77/23.19/23.98° triplet and the split features around 33 and 41°; alternative orthorhombic, small-cell monoclinic, and triclinic candidate models did not reproduce this splitting comparably without implausible lattice changes. Calcite is supported most clearly by its 104 line at 29.07° and weaker correlated lines at 35.67, 39.11, 42.87, 47.17, and 48.20°. Trial CaO and Ca₃WO₆ additions refined to zero scale and were excluded. The residual WO₃ and CaCO₃ quantities are also chemically consistent with incomplete CaCO₃ + WO₃ → CaWO₄ + CO₂ reaction.

An independent, no-refinement replay of `final.gpx` on all 8,301 measured points gives *R*wp = 3.8659%, *R*p = 2.9099%, *R*exp = 3.1382%, and reduced χ² = 1.5175. `fit.csv` was regenerated from that replay, rather than from cached profile arrays.

## Remaining uncertainty

The phase identities and CaWO₄/WO₃ framework models are well constrained by multiple resolved peaks. Calcite is a minor, strongly overlapping component, so its realistic abundance uncertainty is larger than its formal 0.19 wt% standard uncertainty; its presence is reliable, but the last fraction digit is not. Exact WO₃ oxygen positions are not reliably determined by this Cu X-ray pattern because W dominates the scattering. They were therefore kept close to the published model; that model contains symmetry-related O···O contacts near 1.58 Å, so the submitted WO₃ CIF should be treated as a phase/framework model rather than a precise oxygen-sublattice determination. No absolute amorphous content can be obtained without an internal standard, and all reported fractions exclude any amorphous material.
