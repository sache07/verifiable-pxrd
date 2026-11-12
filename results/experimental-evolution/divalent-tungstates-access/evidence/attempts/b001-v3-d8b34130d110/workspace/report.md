# Powder XRD phase analysis

The crystalline model contains four phases. Fractions are normalized over those modeled crystalline phases.

| Phase | Space group | Weight fraction | Reference framework |
|---|---:|---:|---|
| CuWO4 | P -1 | 0.65720 (65.720 wt%) | COD 4000806 |
| Cu3WO6 | P a -3 | 0.13102 (13.102 wt%) | COD 1527404 |
| WO3 | P 21/c | 0.18470 (18.470 wt%) | COD 2311041 |
| CuO (tenorite) | C 2/c | 0.02709 (2.709 wt%) | COD 1011194 |

## Evidence and model selection

CuWO4 accounts for the dominant triclinic pattern. Distinct weaker families require Cu3WO6 (including the low-angle cubic reflections near 15.2 and 19.8 degrees 2theta), monoclinic WO3 (the split family near 22.7–23.9 degrees), and CuO (notably the tenorite contributions near 35.1, 38.3, and 48.4 degrees). Adding CuO reduced the residual at its whole reflection family rather than only at one peak. The resulting phase assemblage gives an overall Cu:W atomic ratio of about 1.03, chemically economical for the CuO/WO3 precursor context. Every coherent residual family is indexed by these four phases; remaining residuals are centered on accepted reflections, so no fifth phase was added.

Several WO3 references and symmetries were tested with comparable cell, coordinate, and profile relaxation. An unrestricted triclinic P -1 model reached a lower numerical Rwp only by collapsing W–O distances to 0.87–1.33 A and producing a 1.66 A O–O contact, so it was rejected. With parent-centered physical coordinate bounds, triclinic WO3 gave Rwp 4.535%, whereas monoclinic P 21/c gave 4.157% before the final texture/strain pass. The retained P 21/c model has no flagged contacts and a shortest W–O distance of 1.63 A.

## Refinement and uncertainty

The submitted GSAS-II project models Cu K-alpha1/K-alpha2 radiation on the full 8301-point grid. Refined terms include phase scales and cells, selected symmetry-allowed coordinates, background, zero/specimen displacement, instrument profile, phase size/strain, and statistically supported texture. Surface roughness was tested but rejected after fresh profile recalculation. A fresh atomic replay of `final.gpx` gives Rwp = 4.1061%, Rp = 3.1284%, and weighted chi-square = 53574.75 with weights 1/max(Iobs,1); it reports no profile-review flags. The four submitted CIFs pass geometry, occupancy, and displacement-tensor screening.

No pointwise experimental uncertainties were supplied, so formal standard uncertainties are not reported and systematic model error likely dominates. The 2.7 wt% CuO fraction is the least secure quantitative value because it is weak, though it is supported by multiple distinct reflections and has a stable positive scale. The detailed oxygen shifts and displacement parameters of WO3 and Cu3WO6 cannot be determined reliably from this powder pattern alone; their source-framework coordinates were therefore mostly retained rather than over-refined. The reported fractions do not measure any amorphous content, which cannot be determined reliably from these data without an internal standard.
