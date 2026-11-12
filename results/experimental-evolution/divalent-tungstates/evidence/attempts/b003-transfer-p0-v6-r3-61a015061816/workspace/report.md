# PXRD phase analysis

## Result

Three crystalline phases are supported by the full 9.90–100.09° 2θ pattern. Weight fractions are normalized over these modeled crystalline phases.

| Phase | Space group | Weight fraction | Covariance e.s.d. |
|---|---:|---:|---:|
| Monoclinic WO3 | P 21/c | 55.27 wt% | 0.09 wt%-point |
| Cu3WO6 | P a -3 | 36.71 wt% | 0.08 wt%-point |
| CuO (tenorite) | C 2/c | 8.02 wt% | 0.10 wt%-point |

The final GSAS-II fit has Rwp = 3.2255%, Rp = 2.5334%, Rexp = 2.4095%, and goodness-of-fit = 1.3406 for 8,301 observations and 24 refined variables. The phase fractions imply a crystalline Cu:W atomic ratio of about 1.06:1, consistent with the stated CuO/WO3 precursor chemistry.

## Evidence and model selection

Monoclinic WO3 accounts for the dominant 23.21°, 24.46°, 29.02°, 47.36°, and related families. Its 00l-related intensities change coherently and require strong preferred orientation. Cu3WO6 is independently supported by families near 15.76°, 20.37°, 33.08°, 34.31°, 36.81°, 43.45°, 58.19°, 63.88°, 70.80°, and 87.65°. Tenorite CuO was accepted only after coherent residual families near 35.7°, 38.9°, 49.0°, 53.6°, and 66–68° refined to a positive, stable scale.

Several physically plausible alternatives were challenged under a common nuisance model. The room-temperature monoclinic WO3 record COD 2311041 fit substantially better than the first monoclinic record tested. A triclinic WO3 record achieved only a marginal improvement after its metric moved close to the monoclinic cell; it was not justified as a separate phase. Orthorhombic WO3 refined to zero. Available exact CuWO4 database records were high-pressure structures and were physically inappropriate here, so a CuWO4 model was also made from the near-endmember Cu0.9Zn0.1WO4 prototype COD 2101690 by replacing Zn with Cu. On the final common profile it refined to only 0.03–0.04 wt% with an approximately 0.06 wt%-point covariance e.s.d., so neither its presence nor fraction is reliable and it was excluded.

The final baseline uses a smooth six-term Chebyshev background, one zero correction, refined polarization, and a nonnegative common X profile term. Isolated low-, middle-, and high-angle families show no remaining systematic position or width trend; freeing SH/L asymmetry collapsed to its neutral lower limit. Roughness reached different local solutions from different starts and was rejected. Shift, transparency, roughness, unused size/strain, extinction, and unsupported texture terms are neutral. Replay-stable phase terms are isotropic Cu3WO6 crystallite size (about 0.168 micrometres), isotropic CuO microstrain (about 5,890 microstrain), and a March-Dollase ratio of 0.717 along [1 0 -1] for WO3. The latter is the [001]-equivalent axis in this nonstandard P 21/c source setting and was supported over no texture and symmetry-distinct alternate axes; CuO texture trials were unsupported. Cells and phase scales were refined; source atomic coordinates were retained because phase R factors were already low and unconstrained coordinate refinement was not warranted. Exported structures pass composition, density, and metal–oxygen geometry checks.

## Remaining uncertainty

The tabulated e.s.d.s are least-squares covariance values only. They do not include model/source choice, strong WO3 texture, the uncalibrated instrumental profile, or the absence of supplied pointwise uncertainties. Reasonable accepted-model variants moved the major-phase fractions by a few weight-percentage points; practical absolute uncertainty is therefore closer to roughly 2–3 wt%-points for WO3 and Cu3WO6 and 1–2 wt%-points for CuO. No amorphous fraction can be measured without an internal or external standard. A distinct triclinic WO3 component and trace CuWO4 cannot be quantified reliably from this dataset. The Durbin-Watson value of 1.11 also indicates some residual correlation despite the low Rwp.

The final project was reopened and replayed over the full range three times. Rwp remained 3.2255%, and the last maximum shift/e.s.d. was 0.0027. `fit.csv`, the three submitted CIFs, and `result.json` were exported from that exact saved `final.gpx` state.
