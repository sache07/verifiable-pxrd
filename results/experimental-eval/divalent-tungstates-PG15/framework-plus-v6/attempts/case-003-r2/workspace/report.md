# Powder XRD phase analysis

The pattern is modeled as three crystalline phases. This is chemically consistent with partial reaction of CaCO3 and WO3 at 500 °C to form CaWO4, with both precursors remaining crystalline.

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| Monoclinic WO3 | P 21/c, COD 2311041-derived | 0.5612 (56.12 wt%) |
| CaWO4, scheelite | I 41/a, COD 7219229-derived | 0.1213 (12.13 wt%) |
| CaCO3, calcite | R -3 c, COD 1547347-derived | 0.3175 (31.75 wt%) |

The strongest identification evidence is the monoclinic WO3 cluster near 23.42, 23.90, and 24.67° 2theta; CaWO4 families near 18.91, 29.03, 31.72, and 34.46°; and calcite families near 29.71, 39.71, 43.46, and 48.55°. The three-phase model accounts for the coherent peak families over the full 10–100° range, and no residual family consistently supports an additional crystalline phase. A physically valid triclinic WO3 alternative (COD 2106293) was replayed with the same nuisance model and fit worse (Rwp 9.14% versus 8.78% at that comparison stage), with larger cell-angle drift. Other plausible records were also screened for occupied composition, symmetry, contacts, and geometry rather than rejected solely on scale.

The final refinement used one Bragg–Brentano specimen-displacement correction (-561 micrometres), a smooth six-term Chebyshev-1 background, and a nonnegative common profile (U = 0, W = 12.889, X = 0.1). Isolated low-, middle-, and high-angle families show no remaining monotonic position or width trend. WO3 required [010] uniaxial microstrain; CaWO4 and calcite retained isotropic strain. Replayed March–Dollase terms were retained for CaWO4 [111] and calcite [001]. Extra SH/L, polarization, surface-roughness, and other texture/strain trials were pruned because their gains were negligible, highly correlated, or not replay-stable. All scales are positive, the background remains positive, and the final save/reopen refinement converged without frozen parameters (maximum shift/esd 0.011).

The independently regenerated final profile gives Rwp = 7.7864%, Rp = 5.9728%, chi-square = 87708.29, and goodness of fit = 3.2572 for 8293 points and 26 refined parameters. The submitted `fit.csv` is from native GSAS-II forward replay of `final.gpx`, not from cached calculated intensities. The replay also reproduced the submitted CIFs byte-for-byte and raised no profile-review flags. All three structures pass the contact and occupancy screen.

The phase identities, cells, and crystalline fractions are reliable, but the covariance-only fraction uncertainties (about 0.1–0.2 wt%) understate model uncertainty. Across physically accepted model variants, fractions moved by roughly 1–2 percentage points; about ±2 wt% absolute is therefore a more realistic uncertainty for each reported fraction. Fractions are normalized only over the modeled crystalline phases; amorphous content cannot be determined without an internal standard.

Light-atom detail is less certain than phase identity. Only the two WO3 W sites, one WO3 O site, and the calcite O coordinate gave physically bounded, replay-stable improvements. The W-site displacement amplitude was explicitly profiled and fixed at the 0.040 Å physical-envelope boundary, so its exact value remains uncertain. Releasing all WO3 O coordinates or the CaWO4 O coordinate required implausible 0.14–0.40 Å shifts, so those coordinates remain at their screened parent-model values in the submitted CIFs. The calcite Uiso profile reached the tested upper limit (0.020 Å2), CaWO4 crystallite size reached the 0.04 micrometre lower bound, and calcite size was not identifiable; these displacement/microstructure values should not be interpreted quantitatively.
