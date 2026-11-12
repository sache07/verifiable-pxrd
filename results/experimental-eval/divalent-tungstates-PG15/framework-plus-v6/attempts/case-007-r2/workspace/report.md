# Powder XRD phase analysis

The pattern is explained by three crystalline phases, all consistent with the MgO–WO3 precursor chemistry and 900 °C treatment. Weight fractions below are normalized over the modeled crystalline material.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MgWO4, wolframite | P 2/c | 4.69011, 5.67469, 4.92876; beta 90.7755 | 0.78033 (78.03 wt%) |
| WO3, monoclinic | P 21/c | 7.69013, 7.53710, 10.52938; beta 136.0832 | 0.14955 (14.96 wt%) |
| MgO, periclase | F m -3 m | a = 4.21287 | 0.07012 (7.01 wt%) |

## Evidence

MgWO4 accounts for the dominant families at approximately 15.93, 19.24, 24.21/24.92, 30.81/31.11, 36.79, and 41.86° 2theta. Monoclinic WO3 is required by its characteristic 23.43/23.93/24.67° group and supporting peaks near 33.57–34.47°. MgO is supported by its relatively isolated 200 reflection near 43.2° and coherent 111, 220, and 311 contributions near 37.3, 62.54, and 75.1°. These features persist across the full angular range and are not isolated residual spikes.

The starting structural records were COD 9013902 (MgWO4), 2311041 (WO3), and 9000499 (MgO). A physical alternate WO3 record was tested under the same nuisance model and gave a poorer, bounded replay. No fourth candidate produced a coherent set of unique residual families with a stable positive scale.

## Refinement and validation

The final GSAS-II refinement used the complete 9.9034–100.0949° scan and the supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio. It used an eight-coefficient smooth Chebyshev-1 background, one specimen-displacement correction (zero fixed at 0), a common nonnegative U/W/X profile with axial asymmetry, low-angle surface roughness, isotropic phase microstrain, and a weak MgWO4 [001] March–Dollase term (0.9873). Crystallite sizes were left neutral because size/strain separation was not stable. Anisotropic strain trials were rejected after they failed repeated save/reopen replay.

An independent atomic forward replay of `final.gpx`, regenerating reflection lists and ignoring cached calculated arrays, gives Rwp = 5.81846%, Rp = 4.25112%, chi-square = 34294.58, and GOF = 2.0381 for 8,301 points. It reported no negative profile widths, negative background, nonfinite intensity, or other profile review flags. The submitted CIFs are the replay exports and all pass the geometry/occupancy contact screen.

## Remaining uncertainty

The phase identities and unit cells are well supported. The quoted fractions are exact project outputs, but their physical precision is lower: about 1–2 wt% absolute is a conservative systematic uncertainty, with MgO most sensitive to displacement/roughness and fixed-ADP choices. The MgWO4 scale and surface-roughness parameter retain a 96% correlation, so additional significant figures should not be interpreted.

The WO3 oxygen coordinates cannot be determined reliably from this laboratory X-ray pattern; unconstrained oxygen refinement produced chemically excessive shifts. They were therefore retained from the physically screened reference structure, while the cell and W positions were refined. MgO atomic displacement parameters were also retained from the source because the minor phase provides insufficient independent leverage. The common Gaussian U term profiles to the allowed upper edge, so the decomposition of instrumental and sample broadening—and hence crystallite size or detailed strain anisotropy—is not uniquely determined. Fractions refer only to modeled crystalline phases; an amorphous fraction cannot be established without an internal standard.

In `fit.csv`, `difference = observed - calculated` on every original measurement point.
