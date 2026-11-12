# Powder XRD phase analysis

The final seven-phase atomic model gives **Rwp = 10.340%** (Rp = 7.404%, goodness of fit = 2.961) in a no-refinement replay of `final.gpx` over all 8282 measured points. The replay regenerated structure factors and reflection lists, left the project unchanged, produced a nonnegative background, and raised no profile-review flags.

| Crystalline phase | Weight fraction (%) | Submitted structure |
|---|---:|---|
| scheelite PbWO4 | 55.47 | `phase_1_pbwo4_9009811.cif` |
| monoclinic WO3 | 9.74 | `phase_2_wo3_1528915.cif` |
| litharge PbO | 3.09 | `phase_3_litharge_9012700.cif` |
| massicot PbO | 7.65 | `phase_4_massicot_2310433.cif` |
| Pb2WO5 (Pb2MoO5-type) | 13.35 | `phase_5_pb2wo5_from_mo_7220560.cif` |
| Pb3WO6 (Pb3UO6-type) | 9.48 | `phase_6_pb3wo6_from_u_2310493.cif` |
| tetragonal Pb3O4 | 1.23 | `phase_7_pb3o4_1537983.cif` |

Fractions are normalized over the modeled crystalline material; this experiment does not determine an amorphous fraction.

## Evidence

Scheelite PbWO4 accounts for the dominant families at about 27.70, 33.06, 45.03, 51.49 and 55.54° 2theta. Monoclinic WO3 is required by the 23.35/23.84/24.65° cluster and its higher-angle families. Litharge and massicot PbO are independently supported by their distinct 32.05/48.80° and 29.33/30.55/38.05° families. Weak tetragonal Pb3O4 is supported by coherent lines near 26.85, 31.03 and 32.79°.

The off-stoichiometric phases are supported by families not explained by those four records. Pb2WO5 matches lines near 25.90, 29.24, 31.05 and 43.39°; an isovalent W-for-Mo model based on COD 7220560 was substantially better than the Pb2CrO5-type alternate. Pb3WO6 matches the 26.59/28.74/29.40/30.19° group and associated mid-angle lines. A composition-, cell- and space-group-filtered analogue search found Pb3UO6 (COD 2310493, Pnma) as the only close same-symmetry parent, so U6+ was replaced by W6+ and the model was cell-refined.

Alternative scheelite, Pb-deficient scheelite, triclinic/other WO3, massicot and Pb3O4 records were challenged under the same nuisance model. They either fitted worse or produced unstable/nonphysical metrics. The final profile uses one specimen-displacement correction, a smooth eight-term Chebyshev background, a common nonnegative width profile, selected phase size/strain terms, and only texture axes supported by multiple families.

## Remaining uncertainty

The Pb2WO5 and especially Pb3WO6 structures are analogue-derived rather than direct database identifications. Pb3WO6 preferred orientation was strongly supported along [010], but its unconstrained ratio reached the allowed range edge; the submitted project therefore uses a fixed interior ratio of 1.35. Its exact coordinates and 9.48 wt% fraction should not be treated as high precision. The 1.23 wt% Pb3O4 fraction is also near the practical detection limit.

Published WO3 and Pb3O4 coordinates trigger a geometry-review warning for short O--O contacts (about 1.58 and 1.80 Å, respectively), though there are no hard contacts, invalid occupancies or density failures. Oxygen-coordinate refinements were not identifiable without exceeding the stated reference-mismatch scale, so the published coordinates were retained. Massicot broadening is resolution-limited (fixed 0.045 micrometre size), adding correlation to its fraction. Residual intensity/profile mismatch remains in heavily overlapped 25--60° regions; major-phase fractions are more reliable than the weak/analogue-derived fractions.
