# Crystalline phase analysis

## Result

Four crystalline phases are required. The refined fractions are normalized over those modeled crystalline phases; they do not measure amorphous material.

| Phase | Space group | Weight fraction | Refined cell (Å, °) | CIF |
|---|---:|---:|---|---|
| BaWO₄, scheelite | I4₁/a | 64.21(15)% | a = 5.63041, c = 12.69407 | `phase_BaWO4.cif` |
| Ba₃W₂O₉ | R-3c | 15.68(10)% | a = 10.13464, c = 13.95793 | `phase_Ba3W2O9.cif` |
| WO₃ | P2₁/c | 12.26(13)% | a = 7.68883, b = 7.54072, c = 10.51547, β = 136.07275 | `phase_WO3.cif` |
| BaCO₃, witherite | Pmcn (Pnma-equivalent setting) | 7.85(17)% | a = 5.31007, b = 8.91791, c = 6.43628 | `phase_BaCO3.cif` |

The full-range replay gives Rwp = 3.0834%, Rp = 2.3633%, Rexp = 3.0170%, and goodness of fit = 1.0239 for 8,301 points and 31 refined variables.

## Evidence and model selection

The WO₃ + BaCO₃ precursor context at 750 °C anchors BaWO₄ as the principal product and makes residual WO₃/BaCO₃ chemically credible. Ba₃W₂O₉ is charge-balanced and accounts for independent families at approximately 26.26°, 30.81°, 40.79°, 54.54°, 63.07°, and 63.83° 2θ. Monoclinic WO₃ is supported by the 23.40°/23.86°/24.66° triplet and families near 33.54°, 34.46°, 50.25°, and 56.24°. BaCO₃ remains replay-stable and has distinguishable families near 24.17°/24.54°, 27.98°, 34.83°, 44.47°, and 45.12°; it is therefore retained despite being the weakest phase.

Source records were treated as competitors. After cross-seeding the common nuisance terms, the selected WO₃ record gave Rwp = 3.0834%, versus 3.1571% for another monoclinic record and 3.0872% for a triclinic record. Low-dimensional anisotropic broadening did not let the triclinic model overtake the simpler P2₁/c model. The selected witherite record gave 3.0834%, versus 3.6752% and 3.3115% for orthorhombic and hexagonal alternatives. The exact BaWO₄ database record contains split half-occupied oxygen sites and gave 4.6742%; an ordered scheelite model adapted from the health-passing SrWO₄ parent COD 1546036 gave 3.0834%. All final exported CIFs pass `learned/cif_health.py`.

Approximate observed low/middle/high-angle width checks were 26.692°: FWHM 0.146° (left/right half-width 0.060°/0.086°), 43.187°: 0.204° (0.065°/0.139°), and 69.158°: 0.130° (0.076°/0.054°). Independent minor-phase examples are broader: Ba₃W₂O₉ families at 30.821°, 40.797°, and 63.823° have approximate FWHM 0.178°, 0.294°, and 0.182°; WO₃ lines at 23.400°, 34.451°, and 56.314° have approximate FWHM 0.156°, 0.251°, and 0.323°. This behavior supports isotropic phase strain for Ba₃W₂O₉, WO₃, and BaCO₃. Size trials reached their neutral boundary, while uniaxial strain, March–Dollase texture, roughness, and SH/L release produced only marginal, unstable, or unphysical gains and were pruned.

The retained common polarization term reproduces an angular intensity trend across independent families of all four phases, improves both middle- and high-angle residuals, and remains stable at 0.974–0.977 across background and texture challenges. A nine-coefficient smooth background is retained; a tenth coefficient refined effectively to zero. The final project was cold-reopened and replayed over 9.9034–100.0946° 2θ before the profile, fractions, and CIFs were exported.

## Remaining uncertainty

No precursor amounts or ratio were supplied, so no mass-balance constraint was invented. The fractions are crystalline-only values; without an internal standard, amorphous content cannot be quantified. Their parenthetical uncertainties are formal GSAS-II standard uncertainties and do not include microabsorption, source-model, or residual line-shape systematics. The WO₃ source ranking is close, so the P2₁/c assignment is preferred but not uniquely proven by this pattern. The ordered scheelite assignment is robust, but its oxygen coordinates remain analogue-derived because refining them did not provide enough independent improvement to retain. A Ba₃WO₆ trial collapsed; the available bronze CIF was unreadable, and no unmatched coherent families justified constructing or quantifying that phase.
