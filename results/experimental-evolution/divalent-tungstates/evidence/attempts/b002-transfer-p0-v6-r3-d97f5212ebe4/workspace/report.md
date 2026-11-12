# PXRD phase analysis

The pattern is described by four crystalline phases. Fractions are normalized over those modeled crystalline phases; they do not quantify amorphous material or absolute product yield.

| Phase | Space group | Weight fraction | Structural model |
|---|---:|---:|---|
| BaWO4 | I 41/a (88) | 62.74(16) wt% | `phase_BaWO4.cif` |
| Ba3W2O9 | R -3 c (167) | 16.53(11) wt% | `phase_Ba3W2O9.cif` |
| WO3 | P 21/c (14), alternate setting | 12.79(14) wt% | `phase_WO3.cif` |
| BaCO3 (witherite) | Pmcn/Pnma (62) | 7.93(19) wt% | `phase_BaCO3.cif` |

The full-range fit (9.9034–100.0946 degrees 2theta, Cu Kalpha1/Kalpha2) has Rwp = 3.2751%, Rp = 2.5371%, Rexp = 3.0170%, goodness of fit = 1.0873, and Durbin-Watson = 1.704. The formal fraction e.s.d.s assume Poisson counting weights because uncertainties were not supplied.

## Evidence and model selection

BaWO4 accounts for the dominant scheelite families near 26.70, 32.05, 43.19, 48.98, 53.68, 54.64, and 69.15 degrees. Ba3W2O9 is required by coherent families including 17.79, 26.26, 27.77, 30.81, 40.79, 63.07, and 63.83 degrees. Monoclinic WO3 is identified especially by the resolved 23.40/23.86/24.66 degree triplet and the 33.54–34.46 degree group. The weaker BaCO3 scale is supported by several partly separated families, including those near 27.97, 34.84, 42.27, 44.46, 47.24, 71.22, 73.18, and 92.06 degrees, and remains stable when its physical alternate record is used.

The only exact BaWO4 COD record available (1527204) has split half-occupied oxygen sites and impossible local geometry, so rejection of that record was not treated as rejection of the phase. Ordered I 41/a analogues from BaMoO4, SrWO4, and CaWO4 were compared under the same nuisance model. The statistically preferred unconstrained oxygen minimum gave implausible W-O/Ba-O geometry. The submitted model therefore uses the ordered BaMoO4 prototype (COD 2300459, Mo replaced by W) and a restrained oxygen refinement with four equivalent W-O targets of 1.82(2) A. It gives W-O = 1.839 A and Ba-O = 2.687/2.775 A. The Ba3W2O9 and WO3 models use COD 1533878 and 2311041. For BaCO3, the modern COD 9010928 coordinates contain a 1.406 A C-O bond; the more plausible Pnma coordinates from COD 1011149 were origin-transformed into the fitted Pmcn setting and replayed while retaining the room-temperature isotropic U values from 9010928. This gives C-O = 1.239–1.241 A and a slightly better fit.

A smooth six-coefficient monotonic background, one zero correction, polarization, and common nonnegative W/X profile terms were refined. Only replay-stable phase broadening was retained: isotropic size for Ba3W2O9 and WO3, and isotropic microstrain for BaCO3. Roughness, texture, U/V/Y, additional asymmetry, extinction, and unsupported size/strain terms were neutralized. For representative BaWO4 families at 32.05, 48.98, and 79.40 degrees, observed/calculated peak maxima agree within one 0.01087-degree data step and observed/calculated FWHM values are 0.159/0.161, 0.210/0.209, and 0.138/0.135 degrees; their left/right half-widths also agree, so no extra asymmetry or texture term was retained.

## Remaining uncertainty

BaWO4's phase identity, cell, heavy-atom framework, and fraction are robust, but its oxygen coordinate is restraint- and prototype-dependent and is not independently determined reliably by this multiphase laboratory XRD pattern. Atomic coordinates of the weaker phases were held to screened source structures while their cells, scales, and supported broadening were refined.

Ba3WO6 was rejected after its scale collapsed to zero. A reduced Ba0.15WO3 bronze candidate refined to about 0.53(14) wt% in a watch-list trial, but its strongest predicted lines lacked coherent residual support and improved Rwp by only 0.004 percentage points; its presence and fraction therefore cannot be determined reliably, and it is not included. Sub-percent additional crystalline material remains possible. The quoted fraction e.s.d.s are covariance estimates and do not include structural-record, background, absorption, or microabsorption systematics; small differences below roughly one absolute wt% should be treated cautiously.
