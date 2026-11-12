# Powder XRD phase analysis

The modeled crystalline material is single-phase scheelite CaWO₄ (space group *I*4₁/*a*, No. 88), at 1.0000 weight fraction after normalization over the modeled crystalline phases. This is not an absolute bulk fraction: amorphous material and crystalline phases below the pattern's detection sensitivity are not quantified.

## Evidence and model selection

The main observed lines at 18.63, 28.72, 29.04, 31.43, 34.18, 39.20, 47.10, 54.29, and 57.89° 2θ, together with their higher-angle Cu Kα doublets, form the scheelite CaWO₄ reflection family. A normalized modern scheelite source (COD 7219229) gave 3.77% Rwp in the matched fixed-coordinate comparison, versus 5.01% for a repaired 1931 scheelite source and about 29% for monoclinic CaWO₄. Every serious candidate was normalized and passed the supplied occupancy/contact screen before comparison.

The final model refines to *a* = 5.243394 Å and *c* = 11.377795 Å. The Ca and W coordinates and their published isotropic displacement parameters were retained. Only the O x/z coordinates and O Uiso were refined; O y was held at the published value because freeing it gave no reproducible improvement. The O refinements reproduced across 8- and 12-term smooth-background restarts and the exported structure passes the physical screen. Polarization refined to 0.7681. Size and strain were exactly confounded with the common profile, texture refined to unity, and roughness became strongly correlated with scale/polarization, so those terms were omitted.

No additional phase is supported by a multi-line residual family. Fixed-coordinate addition tests for CaO, three WO₃ polymorphs, Ca₃WO₆, Ca₄.₂₆W₁₀O₃₀, and monoclinic CaWO₄ gave <0.6σ support except monoclinic CaWO₄ at only 1.81σ (0.094 wt%); all were deleted. This indicates phase-dependent trace sensitivity of roughly a few tenths of a weight percent, not proof that every possible trace phase is absent.

## Fit and verification

Independent replay of `final.gpx`, with no parameter optimization, gives Rwp = 3.5615%, Rp = 2.7482%, χ² = 8347.78, and goodness of fit = 1.0043 using Poisson counting weights. The Poisson Rwp limit is 3.5515%. Replay found one positive phase at fraction 1.0, a positive background, positive peak widths, no project/profile review flags, and an exported CIF numerically consistent with `CaWO4_scheelite.cif`.
