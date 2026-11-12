# Powder XRD phase analysis

The final four-phase GSAS-II model gives **Rwp = 13.4325%** and **Rp = 9.5618%** on all 8,282 measured points. The fractions below are normalized over the modeled crystalline material; an amorphous fraction was not determined.

| Phase model | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| SrWO4 (scheelite) | I41/a (88) | 0.71619 | a = 5.41989, c = 11.96347 |
| WO3 | P21/c (14) | 0.10933 | a = 7.69396, b = 7.54110, c = 10.53406, beta = 136.08295 |
| Sr3WO6, tentative prototype model | P21/c (14) | 0.06159 | a = 6.07077, b = 6.18558, c = 8.47647, beta = 90.87659 |
| Sr3W2O9 | C2/c (15) | 0.11288 | a = 9.63841, b = 5.53355, c = 13.42936, beta = 103.61096 |

## Evidence and model selection

Scheelite SrWO4 (COD 1546036) accounts for the dominant 27.97°, 30.20°, and 33.37° families. Monoclinic WO3 is required by its 23.46–24.70° cluster and families near 33.59° and 34.49°. The submitted WO3 coordinates are from the physically valid neutron model COD 2311041. An older room-temperature record (COD 1528915) fit slightly better but was rejected because its deposited coordinates contain 1.57 Å fully occupied O–O contacts. A physical triclinic WO3 record changed Rwp by only 0.013 percentage points and the WO3 fraction by less than 0.4 percentage point, so the higher-symmetry monoclinic model was retained; this data does not uniquely resolve those two closely related WO3 distortions.

The minor Sr3WO6 model is supported by coherent partly separated families at approximately 29.64/29.97°, 41.99°, 52.21/52.82°, and 61.07°. No exact Sr3WO6 entry was available. Its CIF was therefore built by isovalent U6+ -> W6+ substitution in the Sr3UO6 P21/c prototype (COD 2001752), followed by cell/scale refinement and a small geometry-screened coordinate adjustment. Ca3WO6-, alternate Sr3UO6-, and Ca3OsO6-derived models fit worse or produced inferior geometry.

Sr3W2O9 (COD 2311977) was recovered by re-challenging the residual inventory. It explains a particularly diagnostic family near 32.54° plus partly separated intensity near 44.34–44.61° and 67.65°. SrO and W3O8 watch-list trials remained below about 0.9 wt% in the earlier common-profile model and lacked a coherent independent family set, so they were not retained. The bulk Sr/W molar ratio implied by the final crystalline fractions is 0.967, close to the nominal 1:1 precursor ratio.

All submitted structures pass the contact/occupancy screen: minimum O–O distances are 2.54 Å or longer, and minimum W–O distances are 1.72–2.04 Å depending on phase. The accepted profile uses one specimen-displacement correction (-626.6 micrometres), a smooth eight-coefficient Chebyshev background, isotropic size broadening for SrWO4 and WO3, and isotropic microstrain for the two ternary minor phases. Texture, surface roughness, and an additional refined asymmetry term were rejected as bound, correlated, or axis-ambiguous. A fixed polarization scan strongly favored the physical endpoint 1.00. Fresh atomic replay of `final.gpx` required no optimization and raised no profile review flags.

## Remaining uncertainty

The SrWO4 identification and its dominant fraction are robust. The exact WO3 monoclinic-versus-triclinic distortion is not reliably determined, although an approximately 11 wt% WO3 contribution is stable across those records.

The Sr3WO6 atomic structure **cannot be determined reliably from this powder pattern alone**: it is a chemically justified analogue rather than an exact reference, its peaks overlap the other ternary phases, and its approximately 6.2 wt% fraction is model dependent. Sr3W2O9 is better supported as a phase, but its refined cell volume is about 3% below the source record and its coordinates were not independently refinable; its exact structure and approximately 11.3 wt% fraction should therefore also be treated as provisional. Competing acceptable profile/polymorph choices suggest uncertainties of roughly 1–3 absolute wt% for the minor phases, but these are sensitivity estimates rather than formal standard uncertainties. The common W and X width coefficients also finish at the upper edge of the physically screened range, so the derived size/strain values should not be interpreted as precise microstructural measurements.
