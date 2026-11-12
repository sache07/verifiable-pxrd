# Powder XRD phase analysis

The pattern is modeled by three crystalline phases: wolframite ZnWO4, monoclinic WO3, and wurtzite ZnO. The refined fractions are normalized over these modeled crystalline phases.

| Phase | Space group | Weight fraction | Refined cell |
|---|---:|---:|---|
| ZnWO4 | P 2/c | 0.7398 (73.98 wt%) | a = 4.69392 Å, b = 5.72246 Å, c = 4.92935 Å, beta = 90.6310° |
| WO3 | P 21/c | 0.1892 (18.92 wt%) | a = 7.69624 Å, b = 7.53919 Å, c = 10.5367 Å, beta = 136.104° |
| ZnO | P 63mc | 0.0711 (7.11 wt%) | a = 3.25243 Å, c = 5.20947 Å |

The full-grid fit has Rwp = 5.152%, Rp = 3.994%, and reduced chi-square = 1.862 using count-statistical weights. The corresponding Poisson-only expected Rwp is 3.792%. The independently regenerated GSAS-II profile reproduces Rwp = 5.152% and has no negative-background, negative-width, or negative-ADP review flags.

## Evidence

ZnWO4 (COD 1520641) accounts for the dominant peak set but cannot explain the complete pattern. Its residual contains the wurtzite ZnO family near 31.9, 34.3, 47.8, 56.7, and 62.9° 2theta, as well as the monoclinic WO3 cluster between about 23–29° and near 33–34°. Adding ZnO (COD 9004178) and WO3 (COD 2311041) removes these coherent residual families. No additional repeatable peak family supports a fourth crystalline phase. The remaining WO3:ZnO mass ratio is also close to that expected for residual, incompletely reacted 1:1-molar precursors in the reaction ZnO + WO3 -> ZnWO4.

The alternative monoclinic WO3 parent COD 1528915 was tested; COD 2311041 gave the better whole-pattern fit and is retained in a nonstandard P21/c setting. Preferred-orientation searches on all documented axes converged close to random powder and were omitted. WO3 requires both finite-size and microstrain broadening; the final effective values are about 0.122 micrometers and 3540 ppm.

## Remaining uncertainty

The phase identities are reliable, but detailed WO3 oxygen coordinates are not determined reliably by this overlapping, W-dominated powder pattern. Unconstrained oxygen refinement produced unsupported displacements, so the parent oxygen framework was retained and only the W coordinates were adjusted. The ZnO internal coordinate is likewise weakly constrained. All submitted CIFs pass the contact/occupancy screen.

Surface roughness, polarization, and the dominant-phase scale are correlated. Across physically allowed refinement branches the fraction spread was approximately 2 wt% absolute for ZnWO4/WO3 and about 1 wt% for ZnO; these are practical sensitivity estimates, not formal standard uncertainties. The fractions exclude any amorphous material because no internal standard was supplied, so an amorphous fraction cannot be determined reliably.
