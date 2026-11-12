# Powder XRD phase analysis

The pattern is modeled by six crystalline phases. Weight fractions are normalized over those modeled crystalline phases; no amorphous fraction can be obtained without an external standard.

| Phase | Weight fraction | wt% |
|---|---:|---:|
| PbWO4, scheelite | 0.5569(22) | 55.69(22) |
| PbO, massicot | 0.0734(14) | 7.34(14) |
| PbO, litharge | 0.0833(12) | 8.33(12) |
| Pb2WO5, monoclinic model | 0.1525(20) | 15.25(20) |
| Pb3WO6, ordered model | 0.0405(8) | 4.05(8) |
| WO3, monoclinic | 0.0934(16) | 9.34(16) |

Parentheses are one-standard-deviation statistical errors propagated from the GSAS-II scale covariance. They do not include structural-model, preferred-orientation, absorption, or phase-overlap uncertainty.

## Evidence and refinement

The PbO + WO3 precursor context and 500 °C treatment support lead tungstates together with unreacted oxides. Scheelite PbWO4 (COD 9009811) accounts for the dominant family. Physical exact-composition references account for monoclinic WO3 (COD 2311041), orthorhombic massicot PbO (COD 2310433), and tetragonal litharge PbO (COD 9012700). The litharge CIF required correction of an erroneous origin-choice transform in the stock import; the submitted P4/nmm model has the proper PbO multiplicities.

Two coherent residual families remained after those ordinary phases. A monoclinic Pb2MoO5 reference (COD 7220560) with isovalent Mo6+ -> W6+ substitution matches the Pb2WO5 family; adding it lowered Rwp from about 14.89% to 12.28% and retained a positive ~15 wt% scale. A smaller family, including the distinct reflection near 30.15° 2theta, is matched by an ordered Pb analogue of Ba3WO6 (COD 1534803); adding it lowered Rwp from about 12.28% to 11.55% and retained a positive ~4 wt% scale. Raspite PbWO4 refined to zero, while Pb3O4 gave only a negligible overlapping-profile improvement, so neither was retained. Once the six accepted phases indexed the coherent families, further library searching was stopped.

Cells, scales, background, supported size/strain terms, and three screened March-Dollase terms were refined. Heavy-atom coordinates were accepted only where bond geometry remained physical. Oxygen-coordinate branches worsened the fit and were rolled back. An older WO3 reference with a 1.58 Å O-O contact and a later WO3 coordinate branch with a 1.60 Å W-O contact were rejected even though they gave slightly lower intermediate Rwp values. The final full-grid refinement covers all 8,282 observations and gives Rwp = 9.0732%, Rp = 6.5946%, and GOF = 2.5980. Independent atomic forward replay of `final.gpx`, with fresh reflection lists and no optimization, reproduces Rwp = 9.0732% and raises no profile-geometry review flags.

## Remaining uncertainty

The Pb2WO5 topology is well supported by a broad reflection family, but its submitted atomic model is analogue-derived; oxygen positions were not independently determined by this powder pattern. The Pb3WO6 assignment is more tentative because it is only ~4 wt% and uses an ordered low-symmetry analogue model: the family and approximate fraction are supported, but detailed Pb/W/O ordering cannot be determined reliably. The separate massicot/litharge fractions also carry systematic overlap and texture uncertainty larger than their covariance-only errors. The largest residual excursions occur around strong accepted reflections (especially 27.5–27.7°) and alternate in sign, consistent with peak-shape/intensity mismatch rather than an additional coherent phase family.

`final.gpx`, the six submitted CIFs, `fit.csv`, and `result.json` all come from the same converged full-grid checkpoint.
