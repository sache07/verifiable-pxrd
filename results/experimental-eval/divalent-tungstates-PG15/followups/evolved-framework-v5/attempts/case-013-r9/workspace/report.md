# PXRD phase analysis

## Result

The pattern is described by four crystalline phases. Weight fractions are normalized over these modeled crystalline phases; they do not measure amorphous material or absolute sample composition. Parenthetical uncertainties are the formal one-standard-deviation GSAS-II covariance estimates and are smaller than the likely total systematic uncertainty.

| Phase | Space group | Reference | Crystalline weight fraction |
|---|---:|---:|---:|
| PbWO4, scheelite | I 41/a | COD 9009811 | 73.88(28)% |
| PbO, massicot | P b c m | COD 2310433 | 10.01(16)% |
| WO3, monoclinic | P 21/c | COD 2311041 | 10.41(25)% |
| PbO, litharge | P 4/n m m | COD 9012700 | 5.70(13)% |

This inventory is chemically consistent with partial reaction of the stated PbO and WO3 precursors at 500 degrees C to form scheelite PbWO4, while retaining both PbO polymorphs and monoclinic WO3.

## Evidence and structural model

The model was refined against the full 10--100 degree 2theta Cu Kalpha1/Kalpha2 profile using the wavelengths and 0.5 Kalpha2/Kalpha1 ratio in `inputs/metadata.json`. Strong PbWO4 families occur near 27.71, 29.91, 33.07, 45.03, 47.29, 51.49, 55.54, and 56.82 degrees. Distinct massicot reflections occur near 29.35, 30.62, 38.09, 53.38, 56.29, 60.53, and 63.28 degrees; monoclinic WO3 near 23.39, 23.89, 24.64, 26.77, 34.44, 41.91, 48.44, and 50.22 degrees; and litharge near 29.00, 32.11, 35.95, 45.92, 48.86, 54.91, 60.03, and 66.86 degrees. Thus each reported minor phase is supported by a family of reflections rather than by one isolated peak.

The final refinement used phase scales and cells, a Chebyshev background, a common physical peak profile, zero offset, axial-divergence asymmetry, and one supported March-Dollase correction for massicot [100]. Coordinate trials were retained only when geometry stayed physical. Exported structures have the expected formulas and coordination: PbWO4 has W--O = 1.775 A and Pb--O = 2.613--2.656 A; massicot has shortest Pb--O = 2.144 A; monoclinic WO3 has six W--O distances from 1.717 to 2.163 A; and litharge has four Pb--O distances of 2.315 A. The WO3 model is the physical COD 2311041 structure in its nonstandard P 21/c setting. The litharge reference was rewritten in the equivalent origin choice required for correct GSAS-II site multiplicities; its topology and composition remain those of COD 9012700.

## Fit and uncertainty

The final full-grid fit has Rwp = 14.160%, Rp = 9.832%, Rexp = 3.502%, goodness of fit = 4.051, and chi-squared = 135394.45 for 8281 fitted observations and 30 variables. The refinement converged with maximum shift/esd = 0.054. `fit.csv` contains observed, calculated, and observed-minus-calculated intensities on the complete input grid, and `final.gpx` is the replayable GSAS-II project from which the submitted CIFs, fractions, and profile were exported.

Residual maxima remain around 25.92, 30.15, and 31.04 degrees, along with imperfect intensities at several accepted-phase peak positions. Candidate Pb3O4, Pb2O3, PbO2, WO2, W3O8, and raspite PbWO4 models were examined. None supplied a chemically plausible, stable positive contribution with broad independent-family support. In particular, Pb3O4/Pb2O3 gains required cell distortion or borrowed intensity from accepted WO3/PbO peaks, while a superficially matching fluorite PbO2 reference was a 160 kbar high-pressure phase and is not plausible for this synthesis. Some alternative refinements failed numerically; that is treated as unknown rather than proof of absence.

Accordingly, no fifth crystalline phase identity or fraction can be determined reliably from this pattern. The reported formal fraction errors omit model choice, preferred orientation, peak overlap, absorption/microabsorption, and background/profile systematics, so the last quoted digits should not be interpreted as absolute accuracy.
