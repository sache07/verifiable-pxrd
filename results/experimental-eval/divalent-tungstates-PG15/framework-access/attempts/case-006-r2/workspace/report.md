# Powder XRD phase analysis

The crystalline model contains two phases:

| Phase | Space group | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| CuWO4 | P -1 | a = 4.70848 Å, b = 5.84288 Å, c = 4.88180 Å; α = 88.3435°, β = 92.5336°, γ = 97.2502° | 97.46 wt% |
| WO3 | P 21/c | a = 7.69081 Å, b = 7.53947 Å, c = 10.52533 Å; β = 136.0656° | 2.54 wt% |

The dominant pattern is indexed by ambient triclinic CuWO4. Its starting model was obtained by Cu substitution into the closely related (Cu,Zn)WO4 wolframite structure, followed by cell and coordinate refinement. A [001] uniaxial microstrain model (about 1704 ppm equatorial and 1134 ppm axial) accounts for the reflection-dependent broadening. Residual peaks at 23.45°, 23.92°, 24.69°, and 29.25° 2θ identify monoclinic WO3; adding it removes this coherent residual and lowers the one-phase Rwp from about 5.15% to the final 3.89%. A CuO candidate was tested, but its refined scale collapsed to zero, so it was not retained.

The native zero-cycle replay of `final.gpx` gives Rwp = 3.890%, Rp = 3.035%, and goodness of fit = 1.608 for 8301 points with Poisson count weighting. The replay reports no negative-background, negative-width, polarization, or displacement-parameter flags.

The CuWO4 identity and framework are well supported. Exact light-atom coordinates are less certain than the phase identity because the directly matching ambient reference was unavailable. WO3 is only about 2.5 wt%; its cell and abundance are supported by distinct lines, but its atomic coordinates cannot be refined reliably from this pattern and were therefore held to a published physical monoclinic model. The minor-phase displacement parameter and smooth-background choice correlate with its scale; a practical fraction uncertainty is about ±0.5 percentage points. Fractions are normalized only over the modeled crystalline material, so amorphous content, if present, is not quantified.
