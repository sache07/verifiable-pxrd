# Phase analysis and Rietveld refinement

The crystalline product is predominantly wolframite-type **NiWO4**, with substantial residual monoclinic **WO3** and trace rocksalt **NiO**. Fractions are normalized only over these modeled crystalline phases; without an internal standard they do not quantify amorphous material.

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---:|---|---:|
| NiWO4 | P 2/c (13) | a=4.60162, b=5.66480, c=4.91176, beta=89.9723 | 0.74338 (74.338 wt%) |
| WO3 | P 21/c (14), nonstandard cell setting | a=7.69124, b=7.53598, c=10.5318, beta=136.090 | 0.25347 (25.347 wt%) |
| NiO | F m -3 m (225) | a=4.18155 | 0.00316 (0.316 wt%) |

## Evidence

NiWO4 accounts for the dominant families near 19.2, 23.9-24.9, 30.9, 36.5, 54.6 and 62.3 degrees 2theta. The WO3 model is required by its characteristic split groups at approximately 23.1-24.3 and 33.2-34.1 degrees, together with higher-angle families. Several physical WO3 records were challenged with the same restrained nuisance model; COD 2311041 gave the coherent multiplet positions and the best residuals. Other monoclinic WO3 records, as well as tetragonal/hexagonal and reduced tungsten-oxide candidates, left systematic peak groups.

After rebuilding the common profile, a small positive NiO scale was supported by coherent, mostly overlapped contributions around 37.2, 62.8, 75-79 and 95 degrees. Stoichiometric precursor NiO (COD 1010093) was preferred over a Ni-deficient rocksalt record. This is chemically consistent with the NiO + WO3 synthesis at 900 degrees C, but it is a trace assignment rather than a strong standalone identification.

The exact-composition NiWO4 database record (COD 5910277) had an incomplete atom loop, so its physically complete wolframite model was reconstructed and cross-checked against ZnWO4 and other divalent-tungstate prototypes. The cell and Ni/W y coordinates were refined; oxygen coordinates were retained from the parent model after free oxygen trials became unstable. The resulting geometry is physical (shortest W-O about 1.79 angstrom). WO3 coordinates were likewise retained from the source model because coordinate release was highly correlated and unsupported.

## Refinement and checks

The full 10.0094-99.9944 degree range was refined in GSAS-II with the supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio. The accepted baseline uses a smooth 12-coefficient Chebyshev background, one specimen-displacement correction (104.79 micrometres; zero fixed), a common nonnegative U/W/X profile, polarization, phase-isotropic size broadening, and a low-angle roughness correction whose poorly identified A term was fixed at the lowest tested physical value. Orders 8 and 10 retained a broad background trend; orders 14 and 16 increasingly absorbed an unmatched scan-edge rise, so 12 was retained. A modest NiWO4 [111] March-Dollase term was supported. Isolated low-, middle- and high-angle families showed no residual position drift, repeated one-sided asymmetry or width-bound collapse. Strain, WO3 texture, extra asymmetry, anisotropic broadening and unconstrained oxygen-coordinate terms were tested and rejected as unsupported or unstable.

An independent no-refinement replay regenerated fresh GSAS-II reflection lists and the entire calculated profile from `final.gpx`; it reproduced the exported CIFs and fractions exactly and raised no negative-background, negative-width or displacement-parameter flags. With Poisson counting weights (no pointwise uncertainties were supplied), Rwp = 4.2529%, Rp = 3.2813%, chi-squared = 12377.90 and goodness of fit = 1.2250 for 8282 points and 34 refined parameters.

## Remaining uncertainty

The major-phase identities and their approximate split are reliable, but the formal least-squares fraction uncertainties in `result.json` do not include model, background, texture or microabsorption systematics. The major fractions should not be interpreted more precisely than roughly 1-2 wt% absolute. The NiO fraction is particularly background/profile sensitive: **about 0.3 wt% is supported, but precision better than approximately +/-0.2 wt% is not reliable**, and its trace identity should be regarded as tentative. X-ray data dominated by W also do not determine the oxygen coordinates independently with high reliability; those coordinates are prototype-constrained.
