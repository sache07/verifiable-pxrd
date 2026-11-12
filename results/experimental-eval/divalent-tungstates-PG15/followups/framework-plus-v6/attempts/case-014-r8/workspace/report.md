# Powder XRD phase analysis

The pattern is best described by five crystalline components. Fractions are normalized over these modeled crystalline phases; the scan does not determine amorphous content.

| Phase and structural model | Space group | Weight fraction (wt%) | Formal 1σ (wt%) | Assessment |
|---|---:|---:|---:|---|
| Scheelite SrWO4, COD 1546036 | I 41/a | 65.09 | 0.34 | Well supported, dominant phase |
| Monoclinic WO3, COD 2311041 | P 21/c | 10.41 | 0.18 | Well supported phase; ambient neutron model selected |
| Sr2WO5, derived from Ba2ReO5 COD 1529756 | P n m a | 11.90 | 0.26 | Phase/lattice supported; atomic model and fraction approximate |
| Sr3WO6, derived from Ca3WO6 COD 1563081 | P 21/c | 7.51 | 0.21 | Phase/lattice supported; atomic model and fraction approximate |
| High-temperature/disordered SrCO3, COD 1539128 | R -3 m | 5.08 | 0.27 | Tentative; exact polymorph and fraction are not reliable |

The quoted 1σ values are scale-covariance errors only. They do not include source choice, peak overlap, fixed size/texture terms, or analogue-model error, so the systematic uncertainty—especially for the last three phases—is larger.

## Evidence for the inventory

The Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio from `metadata.json` were modeled explicitly. SrWO4 accounts for the dominant scheelite pattern throughout the scan. Monoclinic WO3 is supported by the resolved family near 23.47, 23.96, and 24.73° 2θ. Families near 16.62, 30.89, and 32.60° support the Sr2WO5 lattice; those near 29.75, 42.17, 53.44, and 61.27° support Sr3WO6. Broad intensity near 22.09°, with related features around 44.67° and 67.0°, supports the minor carbonate candidate.

Under the same provisional nuisance model, removing Sr2WO5 increased Rwp from 15.92% to 16.77%, removing Sr3WO6 increased it to 16.43%, and removing carbonate increased it to 16.39%. A model containing only SrWO4, WO3, and carbonate gave 17.96%. Exact Sr3W2O9 and SrO controls did not explain the unique residual families. A five-lattice Le Bail diagnostic reached Rwp 7.85%, showing that the selected lattices account for most peak positions even though the atomic intensity model remains imperfect.

No exact Sr2WO5 or Sr3WO6 entry was available. The submitted models use isovalent Ba→Sr and Re→W substitution in Ba2ReO5, and Ca→Sr substitution in Ca3WO6, followed by unit-cell refinement. Their geometries pass the contact/occupancy screen, but unrestrained coordinate refinements produced implausible oxygen shifts and were rejected. These CIFs therefore retain parent-framework coordinates and should not be treated as unique structure determinations.

For WO3, the older room-temperature P21/n X-ray entry COD 1528915 gave Rwp 13.37% but contains an implausible 1.58 Å fully occupied O···O contact. The physically clean ambient neutron record COD 2311041 gives essentially the same agreement (final Rwp 13.39%) and was selected. A triclinic WO3 alternate was worse (Rwp 13.50%).

The ordinary Pnma SrCO3 control refined to zero scale and became unstable. The R-3m high-temperature record is consistent with the 900 °C firing history and the observed broad families, but its oxygen sublattice is orientationally disordered (half-occupied alternatives). Those alternatives create short apparent O···O contacts if treated as simultaneous sites. Retention of this polymorph after firing is not established by the metadata, so its identification and 5.08 wt% estimate remain tentative.

## Final refinement and limitations

The final full-range atomic Rietveld model has Rwp = 13.3866%, Rp = 9.4148%, goodness of fit = 3.7905, and reduced χ² = 14.3676 for 8,282 points. It uses one Bragg–Brentano specimen shift (-620 µm), a nonnegative common U/W/X profile, a smooth 10-coefficient Chebyshev background, low-angle roughness, fixed phase-size terms, and one supported Sr2WO5 [001] March–Dollase term (ratio 0.709). Unsupported strain, coordinate, extra texture, polarization, and asymmetry refinements were pruned.

The largest residuals are intensity/shape errors at strong scheelite peaks and at partly overlapped analogue-phase families. Small unmatched features remain, but they do not define a coherent sixth lattice at a reliable abundance. Thus the major SrWO4 and WO3 amounts are the most robust; the two analogue-derived fractions are semiquantitative, and the minor carbonate structure/fraction cannot be determined reliably from this pattern alone.

The saved `final.gpx` was reopened and independently forward-replayed over all 8,282 points without optimization. The regenerated profile has Rwp 13.3866%, no profile-review flags, and exact agreement with the submitted phase fractions and CIF models.
