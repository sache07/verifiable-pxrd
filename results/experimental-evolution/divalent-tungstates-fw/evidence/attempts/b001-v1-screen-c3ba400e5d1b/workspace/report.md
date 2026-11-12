# Powder XRD phase analysis

The pattern is described by three crystalline phases. Fractions are normalized over those phases only; no amorphous fraction can be obtained from this data set.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| PbWO4, scheelite | I 41/a | 65.76(21)% |
| WO3, monoclinic | P 21/c | 18.23(17)% |
| PbCO3, cerussite | P n m a | 16.01(14)% |

Parent structures were normalized and physically screened before comparison. PbWO4 was built from the COD 7219229 CaWO4 scheelite parent by replacing Ca with Pb; WO3 and PbCO3 use COD 2311041 and COD 1010956, respectively. All final CIFs pass the supplied geometry/occupancy screen.

## Evidence and model selection

The dominant peak family is fitted by scheelite PbWO4. Under the same fixed-coordinate, low-flexibility three-phase model, the Ca-parent scheelite analogue gave Rwp = 3.946%, compared with 4.014% for the physically passing Pb7W8O28.8 P4/nnc source; after identical profile convergence the values were 3.733% and 3.793%. Monoclinic and wolframite PbWO4 alternatives were much poorer (Rwp above 12%). Thus the scheelite model was retained on diffraction evidence, not merely on the expected PbCO3 + WO3 reaction chemistry.

After fitting the main phase, the residual contained the characteristic WO3 multiplet at about 23.64, 24.13 and 24.91 degrees 2theta, with supporting lines near 27.14, 29.1–29.5 and 33.8–34.7 degrees. The remaining residual then identified cerussite through the 25.34/26.04-degree pair and supporting lines near 20.64, 35.2–36.7, 44.06 and 47.56 degrees. These assignments are also chemically plausible as residual starting materials, but chemistry was not used to constrain their fractions. Re-optimizing after deleting WO3 raised Rwp from 3.642% to 5.373%; deleting PbCO3 raised it to 5.601%. PbO controls refined to zero or unstable scale and were rejected.

Cells, scales, six background coefficients, angular zero, polarization, and common U/X profile terms were refined. Only an isotropic coherent-domain size for PbWO4 was retained (0.1367(41) micrometres); size/strain terms for the minor phases, main-phase strain, preferred orientation, and additional asymmetry were unsupported or nonphysical. Refining the one unique scheelite oxygen site lowered chi-square by about 68 for three variables and converged to the same coordinates from six- and eight-coefficient background branches and from a specimen-displacement branch. Minor-phase coordinates and all displacement parameters were not determined reliably and remain at normalized parent values.

The final Poisson-weighted fit has Rwp = 3.6421%, Rp = 2.8719%, and goodness of fit = 1.0843 for 8,301 points and 26 refined variables. An eight-term background improved Rwp by only 0.0009 percentage point and was not retained. A separate specimen-displacement branch gave Rwp = 3.6484% and fractions within 0.03 percentage point of the selected branch. Independent forward replay of `final.gpx`, with cached calculated intensities ignored, reproduced `fit.csv`, the phase fractions, and the exported structures; it reported no negative-width, background, polarization, or displacement-parameter review flags.

## Remaining uncertainty

The quoted uncertainties are formal GSAS-II standard uncertainties conditional on this three-phase model. Background and zero/displacement restarts changed the fractions by less than 0.06 percentage point, but source-model uncertainty is larger: the inferior P4/nnc Pb-W-O alternative shifts individual fractions by roughly 1–2 percentage points. The exact Pb-W-O ordering is therefore less certain than the identification of a scheelite-like PbWO4 majority phase. Likewise, monoclinic WO3 was only modestly better than a closely related triclinic source, so the presence and amount of WO3 are more secure than its fine polymorph assignment. The refined angular zero is relatively large (0.5542 degrees); because no calibrated profile or specimen displacement was supplied, absolute lattice metrics carry additional systematic uncertainty even though phase fractions were stable. No claim is made about amorphous material.
