# Powder XRD phase analysis

## Result

The pattern is described by three crystalline phases. Fractions are normalized only over those modeled crystalline phases; this measurement does not determine an amorphous fraction.

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| CaWO4, scheelite | I 41/a | a = 5.24705, c = 11.37802 | 70.17(9)% |
| monoclinic WO3 | P 21/c | a = 7.68414, b = 7.54090, c = 10.50928, beta = 136.0693 | 16.23(6)% |
| Ca3WO6-type ordered perovskite-related phase | P 21 | a = 5.54921, b = 5.80694, c = 8.00467, beta = 90.2133 | 13.60(8)% |

The parenthetical errors are formal GSAS-II covariance e.s.d.'s in weight percent. More realistic approximate systematic uncertainties are +/-1.1, +/-0.9, and +/-0.5 wt% respectively; these are correlated and mainly reflect missing parent ADPs, nuisance-profile choices, and analogue choice.

The final fit has Rwp = 4.7999%, Rp = 3.4972%, Rexp = 2.6169%, goodness of fit = 1.834, and reduced chi-square = 3.364. Poisson uncertainties, sigma = sqrt(counts), were used because the metadata supplies no pointwise uncertainties.

## Evidence and model selection

- CaWO4 is the dominant phase and accounts for the strong scheelite line family throughout the pattern. The starting structure was COD 7219229.
- Monoclinic WO3 is required by the characteristic group near 23.02, 23.45, and 24.27 degrees 2-theta and its higher-angle companions. Removing it and re-equilibrating the model raises Rwp to 15.22%. COD 2311041 beat the near-equivalent COD 1528915 setting by about 0.13 Rwp percentage point in matched cumulative restarts.
- A coherent residual family at approximately 19.35, 22.04, 31-32, 36-37, 45.14, 56-57, and 65.82 degrees requires a Ca3WO6-type phase. Removing it raises Rwp to 11.16%. The exact-composition Ca3UO6 parent COD 2310470, with U mapped to W, beat the Sr2MnWO6-derived ordered-perovskite finalist COD 1532958 by about 0.44 Rwp percentage point in matched restarts.
- Reintroducing CaO (COD 1563196) after the final model was stabilized gives only 0.087(43) wt% and changes Rwp by 0.0009 percentage point. It has no convincing independent multiline residual family and was therefore omitted.

## Refinement and physical checks

The mechanism pass compared background families and orders, zero/displacement branches, common width and axial-divergence terms, roughness/polarization, phase size and strain, and texture. The retained model uses an eight-term Chebyshev-1 background, a refined zero offset, phase scales and cells, positive size/strain terms, WO3 [001] March-Dollase texture, and a reproducible positive surface-roughness branch. Free polarization branches were nonphysical or unstable, so polarization was not retained as a refined term and remains at 0.70.

Coordinates were tested only after the inventory and profile stabilized. A CaWO4 oxygen block and one WO3 tungsten site gave repeatable improvements from independent nuisance starts while retaining sensible geometry. Other oxygen or displacement-parameter refinements were unstable or produced implausible contacts and were rejected. Historical WO3 and Ca3UO6 CIF sites without reported ADPs were normalized to fixed Uiso = 0.01 square angstrom; those ADPs are not determined by this dataset.

The Ca3WO6 oxygen cage was chemically adapted from the Ca3UO6 parent to six W-O distances of about 1.930 angstrom before the final fixed-coordinate comparison. Direct refinement of that cage was not stable, so its exact P 21 distortion is not reliable. The submitted structures have no negative occupancies or ADPs and no short contacts: CaWO4 W-O is about 1.755 angstrom, monoclinic WO3 W-O spans about 1.678-2.200 angstrom, and the shortest Ca-O distance in the Ca3WO6 model is about 2.162 angstrom.

An independent replay of `final.gpx` returned Rwp = 4.8003% and changed every phase fraction by less than 0.0003 wt%; no GSAS-II variables were frozen. The fit remains above the counting-noise expectation, with the largest residuals attached to major-peak intensity/profile shapes rather than a new coherent phase family.

## Remaining uncertainty

The CaWO4 and monoclinic WO3 identifications are reliable. The third phase is reliably required and is best represented as Ca3WO6 in an ordered-perovskite-related topology, but its exact low-symmetry oxygen coordinates cannot be claimed from this pattern alone. Fractions are likewise reliable only to the systematic ranges stated above: using the historical zero-ADP placeholders instead of physically positive fixed ADPs shifts CaWO4 and WO3 by roughly 1 wt%, much more than their formal covariance errors.
