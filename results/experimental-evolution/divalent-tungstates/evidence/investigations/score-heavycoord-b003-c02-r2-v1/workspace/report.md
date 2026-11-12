# Quantitative crystalline-phase analysis

## Result

The pattern is described by three crystalline phases. Fractions are normalized over these modeled crystalline phases; without an internal standard, the data do not determine an amorphous fraction.

| Phase | Structural model | Weight fraction | Formal e.s.d. |
|---|---|---:|---:|
| WO3 | monoclinic P21/c (No. 14), COD 2311041 | 55.326 wt% | 0.085 wt% |
| Cu3WO6 | cubic Pa-3 (No. 205), COD 1527404 | 35.879 wt% | 0.076 wt% |
| CuO | monoclinic C2/c (No. 15), COD 1011194 | 8.795 wt% | 0.107 wt% |

The final full-pattern fit has Rwp = 2.8749%, Rp = 2.2220%, Rexp = 2.4096%, goodness of fit = 1.1952, and Durbin-Watson = 1.3795 for 8,284 observations and 29 refined variables. The project was saved, reopened, and replayed over the full range before the final CIF and profile exports; its final maximum shift/e.s.d. was 0.006.

## Phase evidence and inventory tests

The precursor chemistry and 550 °C treatment support a partially reacted CuO-WO3 mixture. Monoclinic WO3 is required by its split low-angle family at approximately 23.21, 23.66, and 24.45 degrees 2theta and by many matching middle- and high-angle families. The selected monoclinic neutron model fit better than a physically plausible triclinic WO3 alternative under the same common nuisance model.

Cu3WO6 has coherent support from families near 15.74, 20.35, 33.06/34.35, 36.80, 43.43, 50.27/51.19, 58.17, 63.87, 70.81, and 87.53 degrees. Residual families near 35.6, 38.8-39.2, 48.97, 53.46, 58.55, 61.7, and 65.9/68.2 degrees establish residual CuO. The ambient C2/c CuO record fit slightly better than a 196 K Cc record and is better matched to the source conditions.

Full site occupancies and the reported stoichiometries were retained; no unsupported vacancies or site mixing were introduced. Geometry checks on the exported models found no implausible short contacts: minimum metal-oxygen distances were 1.714 A for W-O in WO3, 1.789 A for W-O and 1.918 A for Cu-O in Cu3WO6, and 1.946 A for Cu-O in CuO. Atomic coordinates and displacement parameters were not independently determined by this powder pattern: free-coordinate trials distorted coordination, and grouped displacement refinements drove Cu and W values negative. The CIFs therefore combine refined cells with the physically screened source atomic models.

CuWO4 was retained on the watch list. Exact database entries were high-pressure structures, so an ambient-cell cross-chemistry analogue was also tested. In the final common profile it refined to only 0.109(51) wt% and reduced chi-square by about 6.6, chiefly through an overlapped feature rather than coherent unique reflections. It is excluded: a trace below roughly 0.2 wt% is possible, but its presence and fraction cannot be determined reliably from this pattern.

## Refinement model and physical checks

The GSAS-II fit used the metadata Cu K-alpha doublet and 10-100 degree range, with counting weights sigma = sqrt(max(count,1)) because no pointwise uncertainties were supplied. The final baseline contains a smooth six-term Chebyshev background, all phase scales and cells, one zero correction, refined polarization, and a common nonnegative U/W/X profile. Isolated low-, middle-, and high-angle families showed no remaining systematic position or width trend. Refining asymmetry was rejected because it was 98% correlated with zero; a two-parameter roughness trial was internally 99.97% correlated and acted as a polarization surrogate. Specimen displacement was tested as the alternative angular correction, but zero gave the better fit.

Replay-stable phase terms were a [1 0 -1] March-Dollase correction for WO3, [1 1 0] texture and uniaxial crystallite size for Cu3WO6, and [0 1 0] texture plus isotropic microstrain for CuO. Competing texture axes and size/strain combinations were challenged one phase at a time. Unsupported, singular, negative, or bound terms were pruned; unused size, strain, anisotropic strain, roughness, extinction, and Babinet terms remain neutral.

The tabulated formal fraction e.s.d.s are conditional least-squares values and do not include structural-source, texture, broadening, background, or counting-model uncertainty. For example, replacing ambient CuO by the low-temperature model changed its fraction by 0.62 wt%. A practical uncertainty of roughly 1-2 wt% absolute is therefore more defensible, especially for the minor CuO phase, than the formal e.s.d.s alone. The phase identities and the three-phase inventory are well supported; fine atomic parameters, any amorphous content, and the watch-list CuWO4 trace are not reliably determined.
