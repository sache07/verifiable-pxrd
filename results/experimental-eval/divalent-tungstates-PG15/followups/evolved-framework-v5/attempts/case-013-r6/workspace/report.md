# Powder XRD phase analysis

The pattern is described by five crystalline phases. Weight fractions are normalized over those phases:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| PbWO4, stolzite (scheelite type) | I 41/a | 59.71 wt% |
| PbO, massicot | Pbcm | 9.84 wt% |
| PbO, litharge | P 4/nmm | 6.48 wt% |
| WO3, monoclinic | P 21/c | 9.82 wt% |
| Pb2WO5 | C 2/m | 14.15 wt% |

This inventory is chemically consistent with partial reaction of the PbO and WO3 precursors at 500 °C. Dominant PbWO4 reflections account for the strong families near 27.7°, 33.1°, 45.0°, 47.3°, 51.5°, 55.5°, 56.8°, and 72.3° 2θ. The monoclinic WO3 low-angle multiplet, distinct massicot and litharge PbO families, and the Pb2WO5 family spanning approximately 25.9°, 29–31°, 39–43°, 50–55°, and 60–64° are all required. Removing massicot or Pb2WO5 produced large, coherent residual families; after inclusion, no additional coherent family justified another phase.

The final full-grid fit has Rwp = 10.112%, Rp = 6.874%, Rexp = 3.502%, and goodness of fit = 2.888. The project replays without optimizing any parameter, with no frozen variables, negative widths, negative displacement tensors, or impossible contacts. A defective older WO3 coordinate set was rejected because of a 1.58 Å O–O contact; the submitted neutron-derived WO3 model has W–O distances of about 1.71–2.16 Å. Coordinate-refinement branches that created short contacts were likewise rolled back.

The main uncertainty is Pb2WO5: no exact-composition entry was available in the frozen reference index, so its C2/m model was transferred from isostructural Pb2MoO5 by Mo(VI)→W(VI) substitution. The Mo-parent start fit better than bounded midpoint and Pb2CrO5-derived starts, and its geometry is physical, but the oxygen coordinates are not independently established by this powder pattern. Its 14.15 wt% fraction is therefore model-dependent. Peak overlap also makes the massicot/litharge split less secure than their combined PbO amount (16.32 wt%). The tabulated least-squares ESDs in `result.json` are internal precision estimates and likely understate those structural/profile systematic uncertainties.
