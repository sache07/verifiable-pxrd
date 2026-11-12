# Powder XRD phase analysis

The best physical four-phase model contains wolframite MnWO4, monoclinic WO3, and two minor manganese tungstate phases. Weight fractions are normalized over these modeled crystalline phases; no amorphous fraction was determined.

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| MnWO4 | P 2/c | a=4.79675, b=5.71084, c=4.97710, beta=91.1235 | 72.18% |
| WO3 | P 21/c | a=7.69034, b=7.54385, c=10.53306, beta=136.1241 | 15.31% |
| Mn2WO6 | R -3 c | a=8.64650, c=22.11700 | 6.96% |
| Mn3WO6 | R -3 | a=8.87546, c=10.78086 | 5.56% |

## Evidence

The calculation used the reported Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio. The strongest peak-position and intensity families are accounted for by P 2/c MnWO4; a second extensive family is matched by P 21/c WO3 in a transformed monoclinic setting. Both phases retain positive, stable scales and physically ordinary cells through staged background, displacement, cell, scale, and profile refinement. The selected WO3 reference has a 2.54 angstrom minimum O-O distance; an otherwise close checkpoint with an unphysical 1.58 angstrom O-O contact was rejected.

After those phases were fitted, coherent residual families remained. The R -3 c Mn2WO6 model accounts particularly for the approximately 20.90, 29.15, 47.03, and 57.01 degree families, while the R -3 Mn3WO6 model accounts for the approximately 35.3--35.6 and 54.9 degree families. Simple manganese oxides and alternative Mn-W-O polymorphs did not account for these families as broadly while retaining positive scales and physical geometry. The accepted minor-phase models have positive scales, densities of about 5.42 and 6.02 g/cm3, respectively, and physically plausible Mn-O, W-O, and O-O distances. The resulting bulk crystalline Mn:W molar ratio is about 0.93, consistent with a predominantly MnWO4 product containing residual WO3.

The final full-grid fit has Rwp=12.039%, Rp=6.834%, Rexp=1.773%, and goodness-of-fit=6.790 for 10--100 degrees two-theta. The saved project reproduces this result on a fresh GSAS-II refinement pass.

## Remaining uncertainty

MnWO4 and WO3 are secure assignments. The two minor-phase structures are analogue-derived models: the R -3 c topology was adapted from a NASICON-related framework and the R -3 topology from a Mn-tellurate-related framework, then constrained to physical Mn-O/W-O geometry. Their reflection families and combined presence are supported, but extensive overlap means their exact topology, oxygen coordinates, and individual 6.96%/5.56% split cannot be determined reliably from this pattern alone. The formal scale-derived fraction uncertainties in `result.json` are conditional and are smaller than this structural-model uncertainty.

Several broadening parameters reached the allowed physical search limits, and localized relative-intensity residuals remain even though no additional coherent unindexed family was found. Consequently, the minor-phase fractions should be treated as approximate. The reported values exclude any amorphous or unidentified noncrystalline material.
