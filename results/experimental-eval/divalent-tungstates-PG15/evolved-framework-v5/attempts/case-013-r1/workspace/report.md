# Powder XRD phase analysis

## Result

The specimen is a six-component crystalline mixture on the adopted model. Weight fractions are normalized over the modeled crystalline phases only.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| PbWO4 (scheelite) | I41/a | 55.18% |
| Pb2WO5-like, expanded-cell variant | C2/m | 13.16% |
| WO3 (monoclinic) | P21/c | 10.23% |
| PbO (massicot) | Pbcm | 7.65% |
| PbO (litharge) | P4/nmm | 7.82% |
| Pb2WO5-like, compact-cell variant | C2/m | 5.96% |

The full 10–100 degrees 2-theta Cu K-alpha Rietveld fit gives **Rwp = 9.705%, Rp = 6.713%, and GOF = 2.775** for 8,282 observations. The refined profile is in `fit.csv`, and `final.gpx` is the exact GSAS-II checkpoint from which the CIFs, fractions, and profile were exported.

## Evidence and model construction

The chemistry is consistent with partial reaction of PbO and WO3 at 500 degrees C: scheelite PbWO4 is the major product, while both PbO polymorphs and monoclinic WO3 remain. The phase assignments are supported across the full pattern rather than by isolated peaks. Representative calculated families are PbWO4 at 27.67, 29.88, 33.03, 45.00, and 47.27 degrees; WO3 at 23.36, 23.84, and 24.63 degrees; massicot at 29.34, 30.57, 32.87, and 38.07 degrees; and litharge at 28.84, 32.10, 35.81, 45.90, and 48.71 degrees.

An expanded C2/m Pb2WO5-like model accounts for families including 25.88, 29.25, 31.03, and 41.88 degrees. A second, more compact C2/m metric is needed for the coherent residual family represented by 26.71, 30.16, 31.43, 43.73/44.14, and higher-angle reflections. Exact-composition and plausible precursor/product alternatives tested at that residual checkpoint either collapsed to negligible scale or did not support the family across the pattern. Once the accepted phases indexed every coherent family, no further phase search was performed.

Reference starting models were COD 9009811 (scheelite), 2311041 (the physical neutron structure of WO3), 2310433 (massicot), and 9012700 (litharge). An earlier WO3 reference gave an unphysical short O–O contact and was rejected even though its Rwp was lower by about 0.02 percentage point. The Pb2WO5-like structures were obtained by chemically substituting W into isostructural Pb2MoO5 (COD 7220560) and Pb2CrO5 (COD 8103050) models, followed by cell and bounded coordinate refinement. The final compact model retains physical tetrahedral W–O distances of about 1.72–1.80 angstrom. Larger unconstrained coordinate moves and profile branches that reached physical bounds were rejected.

## Remaining uncertainty

The two C2/m Pb2WO5-like assignments are the least certain part of the result. They may be two metric/defect or composition domains of one Pb-rich tungstate rather than distinct equilibrium polymorphs, and the compact model is analogue-derived rather than an exact-composition database match. Its 5.96% fraction and the split between the two C2/m components should therefore be treated cautiously; their combined modeled fraction, 19.12%, is more robust than the individual split.

The formal covariance errors recorded in `result.json` (roughly 0.11–0.20 percentage point per phase) do not include model-selection, peak-overlap, preferred-orientation, or analogue-structure uncertainty. The PbO polymorph fractions are also correlated by overlap, and the very broad litharge contribution required a crystallite-size lower bound. No internal standard or amorphous model was available, so an absolute amorphous fraction cannot be determined reliably.
