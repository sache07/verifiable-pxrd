# Crystalline phase analysis

Rietveld refinement identifies a dominant triclinic copper tungstate phase and a small amount of unreacted monoclinic tungsten trioxide. Weight fractions are normalized over the modeled crystalline material.

| Phase | Space group | Refined unit cell | Weight fraction |
|---|---|---|---:|
| CuWO4 | P -1 | a = 4.71235 Å, b = 5.84763 Å, c = 4.88558 Å; alpha = 91.6554°, beta = 92.5340°, gamma = 82.7493° | 97.80 wt% |
| WO3 | P 21/c | a = 7.69290 Å, b = 7.54771 Å, c = 10.5287 Å; beta = 136.060° | 2.20 wt% |

The WO3 cell is an alternate but crystallographically equivalent P 21/c setting. Its atomic coordinates and displacement parameters were held at the reference-model values because a phase at approximately 2 wt% does not contain enough information for reliable independent coordinate refinement. Its lattice and scale were refined. CuWO4 lattice parameters and atomic coordinates were refined.

## Evidence and refinement

The CuWO4 model accounts for the low-angle reflections near 15.6° and 19.3° 2theta and the characteristic dense multiplet from approximately 23–39°. A CuWO4-only refinement left a reproducible set of unmatched intensities and gave Rwp approximately 7.43%. Adding P 21/c WO3 accounts for peaks near 23.43°, 23.89°, 24.69° and the 33.6–34.5° region, lowering Rwp to 6.525% (Rp = 4.734%, Rexp = 2.434%, goodness of fit = 2.689). The final least-squares calculation converged with a maximum shift/esd of 0.009.

CuO, Cu2O and Cu3WO6 were tested as additional chemically plausible phases. CuO refined to effectively zero; Cu2O refined to 0.02(6) wt% and Cu3WO6 to 0.08(5) wt%. These are not significant and were excluded from the submitted model. A Cu2WO4 candidate also predicts low-angle reflections absent from the data.

The refinement used the supplied Cu Kalpha1/Kalpha2 wavelengths and intensity ratio, a 12-term Chebyshev background, and Poisson counting weights because the input supplied no pointwise uncertainties. The fitted interval was nominally 10–100° 2theta; `fit.csv` contains the 8,284 points used by GSAS-II (10.00123–100.00795°, reflecting its endpoint indexing).

## Uncertainty and limitations

The least-squares standard uncertainty for each normalized phase fraction is 0.056 wt%, but this is only a counting-statistical estimate. Uncertainty in the empirical instrument profile, reference structures, background, preferred orientation and microstructure is not fully represented; the realistic uncertainty of the minor WO3 amount is therefore likely a few tenths of a weight percent. Its presence is supported, but detailed WO3 atomic parameters cannot be determined reliably from this pattern.

No internal standard or amorphous model was supplied, so an absolute amorphous fraction cannot be determined. The reported 97.80/2.20 wt% values sum to 100% over the modeled crystalline phases only.
