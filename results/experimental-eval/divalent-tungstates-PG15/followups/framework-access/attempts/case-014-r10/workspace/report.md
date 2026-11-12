# Powder XRD phase analysis

## Result

The pattern is best described by four crystalline phases. Fractions below are normalized over those phases; they do not include any amorphous material.

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| SrWO4, scheelite | I 41/a | a = 5.42504, c = 11.97384 | 0.63175 (63.18 wt%) |
| SrWO4, monoclinic polymorph | C 2/c | a = 7.23029, b = 11.11685, c = 5.11209, beta = 134.6617 | 0.10301 (10.30 wt%) |
| WO3, monoclinic | P 21/c | a = 7.31253, b = 7.55022, c = 10.54400, beta = 133.0703 | 0.10971 (10.97 wt%) |
| Sr3WO6, cubic | P a -3 | a = 10.95898 | 0.15552 (15.55 wt%) |

The final whole-pattern fit has Rwp = 11.1189%, Rp = 7.6412%, Rexp = 3.5351%, and goodness of fit = 3.1485 (8,282 observations; counting weights `1/max(counts,1)`). The calculated profile was independently regenerated from the atoms and profile parameters in `final.gpx`; its Rwp is 11.1189%, and all four exported CIFs agree with the corresponding project phases.

## Evidence and model construction

The dominant reflections and systematic absences match scheelite SrWO4 (starting model COD 1546036). A scheelite-only refinement left structured unmatched peaks and gave Rwp about 17.8%. Two chemically plausible residual components were then identified: monoclinic C 2/c SrWO4 (COD 1546037) and monoclinic P 21/c WO3 (COD 1528915). Refining those three phases reduced Rwp to about 13.1%.

The remaining residual peaks formed a reproducible cubic pattern. The best structural match was the P a -3 Cu3WO6 framework (COD 1527404), converted to the chemically appropriate Sr3WO6 composition and refined as a Sr-containing analogue. Adding this phase reduced the intermediate Rwp from about 13.1% to 12.6%; bounded profile, lattice, scale, texture, and coordinate refinement produced the final 11.12% fit. No stable fifth phase was supported by residual searches. The modeled bulk Sr/W atomic ratio is about 1.03, consistent with the nominal 1:1 SrCO3:WO3 feed within phase/fraction uncertainty.

The Cu K-alpha1/K-alpha2 wavelengths and 2:1 intensity ratio from the metadata were modeled explicitly. Phase fractions were calculated from the refined GSAS-II phase scales multiplied by unit-cell masses, then normalized to sum to one.

## Confidence and limitations

The scheelite SrWO4 and WO3 phase identities are high-confidence; the monoclinic SrWO4 and analogue-derived Sr3WO6 assignments are moderate-confidence because their peaks overlap strongly with the dominant phase and require substantial phase-specific broadening/texture. In particular, the cubic phase's cell and diffraction contribution are supported, but its detailed Sr3WO6 atomic arrangement should be independently confirmed before being treated as definitive.

The data contain no supplied point uncertainties or instrument-standard scan. Several profile or microstructure terms reached their allowed bounds, and phase scale, preferred orientation, roughness, polarization, and broadening are correlated. Consequently, the minor-phase fractions should not be interpreted as more accurate than a few absolute weight-percent; formal standard uncertainties from this refinement would understate the systematic uncertainty. Amorphous content cannot be determined from this analysis, and a weak or heavily overlapped trace phase cannot be excluded.

The fitted effective zero offset is 0.3701°. With only one scan it cannot be separated reliably from specimen-height displacement, so the refined lattice constants also retain systematic uncertainty. Heavy-atom scattering dominates this pattern: oxygen coordinates are substantially less secure than the phase identities and cells. The submitted WO3 model has four symmetry-related O-O contacts near 1.58 Å; the same review flag is present in its database parent. Thus its WO3 identity is reliable, but its refined oxygen sublattice/local geometry is not. Atomic coordinates in all minor phases should be regarded as constrained powder models rather than precise local-structure determinations.
