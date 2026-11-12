# Powder XRD phase analysis

The pattern is described by three crystalline phases. Fractions are normalized over these modeled crystalline phases; this analysis does not quantify amorphous material.

| Phase | Structure | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| ZnWO4 | wolframite, P2/c (No. 13) | a = 4.69201, b = 5.72007, c = 4.92747, β = 90.6311 | 0.72693 (72.69 wt%) |
| WO3 | monoclinic, P21/c (No. 14) | a = 7.30590, b = 7.53809, c = 10.53411, β = 133.0908 | 0.20934 (20.93 wt%) |
| ZnO | wurtzite, P63mc (No. 186) | a = 3.25078, c = 5.21003 | 0.06373 (6.37 wt%) |

## Evidence

The chemistry is consistent with partial reaction of the stated WO3 and ZnO precursors at 900 °C to wolframite ZnWO4, with both precursors remaining. ZnWO4 accounts for the families at approximately 15.61°, 19.03°, 30.58/30.83°, 36.56°, and 38.46° 2θ. Monoclinic WO3 is required by the 23.23/23.71/24.48° and 33.38–34.28° families. Wurtzite ZnO is independently supported by its 31.88°, 56.69°, 62.93°, and 68.03/69.17° reflections.

Starting structures were COD 1520641 (ZnWO4), 2311041 (WO3), and 9004178 (ZnO). Alternative WO3 records were screened with the same nuisance model. COD 1528915 gave a slightly poorer fit and contains a 1.575 Å O–O contact; triclinic COD 2106293 gained only marginal profile agreement while requiring excessive cell-angle changes and extra structural freedom. High-pressure monoclinic and orthorhombic alternatives were clearly poorer. After profile refinement, the remaining residual extrema alternate across already modeled ZnWO4 multiplets rather than forming coherent unique families, so there is no reliable evidence for a fourth crystalline phase.

## Refinement and uncertainty

The final Bragg–Brentano model uses one specimen-height correction (−227.3 µm), a smooth positive eight-coefficient background, Suortti surface roughness, and phase-specific isotropic crystallite sizes. Microstrain, texture, free polarization, and free axial-divergence terms were rejected because they were unchanged, strongly surrogate-correlated, or required bound/frozen values. Small ZnWO4 oxygen shifts and one constrained WO3 tungsten-coordinate mode were retained; all exported structures pass the contact and occupancy screen.

Independent replay of `final.gpx` over all 8,301 points gives Rwp = 6.2621%, Rp = 4.7944%, χ² = 22,642.27, reduced χ² = 2.7389, and goodness of fit = 1.655. Replay produced no negative-background, negative-width, or other profile-review flags.

The least-squares fraction standard errors are about 0.12–0.15 wt%, but they do not include source-structure, displacement-parameter, surface-roughness, or profile-model uncertainty. The latter is dominant: a more realistic uncertainty is roughly 1–2 wt% absolute for ZnWO4 and WO3 and about 0.5–1 wt% for ZnO. The phase identities are reliable; detailed oxygen coordinates in WO3 and fractions beyond that systematic precision are not reliably determined by this powder pattern alone.
