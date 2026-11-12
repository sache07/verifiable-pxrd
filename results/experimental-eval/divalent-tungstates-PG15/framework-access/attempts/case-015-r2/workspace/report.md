# Powder XRD phase analysis

The crystalline product is a three-phase mixture dominated by wolframite ZnWO4, with unreacted monoclinic WO3 and wurtzite ZnO. Fractions are normalized over these modeled crystalline phases; no amorphous fraction can be obtained without an internal standard.

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| ZnWO4 (wolframite) | P 2/c | a = 4.69659, b = 5.72566, c = 4.93229, beta = 90.6350 | 0.74719 (74.72 wt%) |
| WO3 (monoclinic) | P 21/c | a = 7.70185, b = 7.54460, c = 10.5444, beta = 136.104 | 0.18907 (18.91 wt%) |
| ZnO (wurtzite) | P 63 m c | a = b = 3.25433, c = 5.21578 | 0.06374 (6.37 wt%) |

## Evidence and refinement

The dominant peak positions and intensity sequence index as wolframite ZnWO4. A ZnWO4-only model leaves a structured set of peaks matched by room-temperature monoclinic WO3; the remaining characteristic wurtzite ZnO reflections, including its low-angle triplet, require the third phase. Adding ZnO gives a substantial profile improvement and a stable approximately 6 wt% scale fraction. No reproducible residual-peak family supports a fourth crystalline phase.

The starting structural models were COD 1520641 (ZnWO4), COD 2311041 (WO3), and COD 9004178 (ZnO). The GSAS-II model uses the Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio supplied in the metadata. Cell parameters, phase scales, background, zero/displacement and line-shape terms were refined in stages. Atomic positions were varied only where supported: the ZnWO4 coordinates, WO3 tungsten positions, and ZnO oxygen z coordinate. The submitted profile is a fresh native GSAS-II forward calculation from `final.gpx`, not a cached fitted curve.

The full-grid fit has Rwp = 4.8868%, chi-square = 13789.05, and goodness of fit = 1.2903 for 8301 points and 19 active parameters. In `fit.csv`, `difference` is observed minus calculated intensity.

## Remaining uncertainty

The phase inventory and the presence of all three phases are reliable. Across defensible profile/structure branches the fractions moved by about one percentage point; because pointwise uncertainties and a calibrated instrumental profile were not supplied, precision finer than roughly 1–2 wt% should not be inferred. Crystallite-size and microstrain terms are strongly covariant with the instrumental width and are therefore nuisance terms rather than reliable microstructural measurements.

Monoclinic WO3 and closely related lower-symmetry/alternative-cell descriptions give very similar broadened profiles. P 21/c is selected from the room-temperature chemical context and the simplest adequate fit, but this powder pattern does not reliably determine the detailed WO3 oxygen sublattice; literature oxygen coordinates were retained. The minor-phase ZnO internal coordinate is likewise less secure than its identity and fraction. Weak additional crystalline material below approximately 1–2 wt% cannot be excluded.
