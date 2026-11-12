# Powder XRD phase analysis

## Result

The 700 °C product from WO3 and CuO contains four modeled crystalline phases. Weight fractions are normalized to the sum of those crystalline phases; they do not measure any amorphous content.

| Phase | Space group | Crystalline weight fraction | Formal refinement e.s.d. |
|---|---:|---:|---:|
| CuWO4 | P -1 | 64.2434 wt% | 0.028 wt% |
| Cu3WO6 | P a -3 | 13.3315 wt% | 0.020 wt% |
| WO3 | P -1 | 20.0302 wt% | 0.022 wt% |
| CuO | C 2/c | 2.3949 wt% | 0.019 wt% |

The final native GSAS-II replay on all 8,301 measured points gives Rwp = 2.56335%, Rp = 1.85913%, Rexp = 1.61295%, and goodness of fit = 1.58923. The calculation uses the supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio. The bounded polish selected its unchanged baseline branch; lower-Rwp coordinate branches were rejected because coordinate shifts did not converge. The final project replayed without changing the file and raised no profile or geometry review flags.

## Evidence and model selection

CuWO4 and Cu3WO6 each account for repeated reflection families across the full 10–100 degree range, not isolated peaks. Starting structures were COD 4000806 (CuWO4, P -1) and COD 1527404 (Cu3WO6, P a -3). These two phases alone left a coherent split family near 22.7–23.9 degrees and matching higher-angle residuals. Among equally developed WO3 starts, the triclinic P -1 model (COD 2106293) fit this splitting better than P21/n and Pnma alternatives (checkpoint Rwp 9.515%, 10.475%, and 19.190%, respectively), so P -1 WO3 was retained.

A remaining positive family, including the characteristic pair near 35.1 and 38.3 degrees and higher-order companions, required CuO. C2/c and Cc CuO starts were nearly profile-equivalent at an early equal checkpoint; the standard higher-symmetry C2/c model (COD 1011194) was retained because the data did not justify symmetry lowering. Cu2O did not account for this family and was rejected. After adding CuO, no coherent unassigned reflection family remained.

Cells, scales, background, supported atomic/displacement terms, specimen displacement, and supported size/strain terms were refined. Preferred orientation and surface roughness tests were not retained. Zero and specimen height were nearly inseparable, so zero was fixed at -0.052 degrees and only the specimen displacement was retained. Bound-limited crystallite-size terms for WO3 and CuO were fixed at an interior value rather than interpreted quantitatively.

## Remaining uncertainty

The listed e.s.d.s are covariance-based counting/refinement uncertainties and are smaller than likely model and overlap systematics. CuO is a well-supported minor phase, but its 2.39 wt% fraction has the largest relative systematic uncertainty. The exact C2/c-versus-Cc symmetry of this minor component cannot be distinguished reliably here.

The WO3 phase identity, low-symmetry cell, and fraction are supported by its full reflection family, but its detailed oxygen coordinates are weakly constrained by laboratory powder data. Further coordinate polishing was nonconvergent, so the conservative accepted physical basin was retained; the WO3 CIF should not be read as a high-precision oxygen-position determination. Likewise, no external standard was supplied, so an amorphous fraction or absolute crystalline yield cannot be determined.

`fit.csv`, all four CIFs, and `result.json` were exported from the exact accepted `final.gpx` model (SHA-256 `e5c57036e865833e1074377cc43c7748aa511304aafc4ad7659975b1ebbc5686`).
