# Powder XRD phase analysis

## Result

The 900 °C product from SrCO3 and WO3 is best described by four crystalline components. Weight fractions are normalized over these modeled crystalline phases; they do not measure any amorphous content.

| Phase model | Refined cell (Å, °) | Weight fraction | Assessment |
|---|---|---:|---|
| Scheelite SrWO4, *I*41/*a* | *a* = 5.417887, *c* = 11.960512 | 75.50 wt% (formal esd 0.36 wt%) | High-confidence phase assignment and structure |
| Monoclinic WO3, *P*21/*c* | *a* = 7.697250, *b* = 7.539071, *c* = 10.545776, beta = 136.171612 | 14.03 wt% (formal esd 0.24 wt%) | High-confidence phase assignment; physical neutron model COD 2311041 |
| Cubic ordered-double-perovskite Sr3WO6, *Fm*-3*m* | *a* = 8.616823 | 3.95 wt% (formal esd 0.18 wt%) | Moderate-confidence prototype assignment |
| Sr tungsten-bronze model, *P*4/*mbm* | *a* = 12.505686, *c* = 3.908974 | 6.51 wt% (formal esd 0.28 wt%) | TTB topology and metric are supported, but exact composition, structure, and fraction are not reliably determined |

The final fit has Rwp = 15.2140%, Rp = 10.3324%, Rexp = 3.5351%, goodness of fit = 4.3079, and Durbin–Watson = 0.1285 over all 8,282 points from 10.0094–99.9938° 2theta. The reflection-geometry model used the reported Cu K-alpha1/K-alpha2 wavelengths (1.540598/1.544426 Å) and 0.5 intensity ratio. Because pointwise uncertainties were not supplied, the refinement used counting-statistics weights, `w = 1/max(I,1)`.

## Evidence

Scheelite SrWO4 accounts for the dominant 18.30, 27.97, 45.44, 47.73, 51.95, and 56.06° families. Monoclinic WO3 accounts for the characteristic 23.43/23.92/24.69° group and the 33.57/34.49° group. The weak cubic family is consistently indexed by an F-centered cell at 29.63 (220), 42.22 (400), 52.25 (422), 61.04 (440), and 69.13° (620). The remaining repeated family is indexed by the tetragonal-tungsten-bronze metric, including calculated lines near 29.76, 32.50, 46.73, 52.07, and 56.22–57.41°. With all other parameters fixed, omitting SrWO4, WO3, Sr3WO6, or the bronze raises Rwp from 15.21% to 43.29%, 18.44%, 15.70%, or 15.95%, respectively.

SrCO3, SrO, SrO2, Sr3W2O9, and a high-pressure SrWO4 polymorph were tested but lacked their required reflection families or refined to zero scale. No additional chemically plausible tested phase gave a stable positive contribution after the four accepted families were modeled.

The legacy monoclinic WO3 entry that gave a slightly competitive profile had an approximately 1.58 Å O–O contact and was rejected. The submitted physical WO3 model has six W–O distances of 1.715–2.159 Å and a 2.539 Å minimum O–O separation. Geometry checks also give W–O = 1.891 Å in SrWO4, 1.810 Å in cubic Sr3WO6, and approximately 1.90–1.99 Å in the bronze framework. Unstable coordinate refinements were rolled back to these physical structures.

## Remaining uncertainty

The low Durbin–Watson value and goodness of fit well above one show substantial correlated model/profile error, so the tabulated least-squares esds substantially understate practical uncertainty. The SrWO4 and WO3 identities are robust, but their fractions remain conditional on the four-phase crystalline model and its texture/profile treatment.

The Sr3WO6 reflection metric is convincing, but the ideal *Fm*-3*m* ordering and oxygen coordinate are only moderately constrained by this minor contribution. For the bronze, the *P*4/*mbm* framework and cell are supported across a family of reflections, but Sr occupancy and exact stoichiometry are not identifiable from this pattern. Its CIF uses a Sr6W10O30 model, and the reported 6.51 wt% is model-dependent; neither that exact structure nor that fraction should be treated as reliable. Unmodeled amorphous material, if present, cannot be quantified without an internal standard.

The submitted `final.gpx` reproduces `fit.csv` exactly in a zero-cycle GSAS-II replay and is the project used to export all four CIFs and the normalized phase fractions.
