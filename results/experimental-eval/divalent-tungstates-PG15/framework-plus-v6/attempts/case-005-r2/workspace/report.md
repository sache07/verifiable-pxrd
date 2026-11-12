# Powder-XRD phase analysis

The modeled crystalline material contains monoclinic gamma-WO3 and spinel Co3O4. Fractions are normalized over these crystalline phases only.

| Phase | Refined cell | Weight fraction |
|---|---|---:|
| gamma-WO3, P 21/c | a = 7.30747, b = 7.53857, c = 10.54822 A; beta = 133.1555 deg | 0.76314 (76.31 wt%) |
| Co3O4 spinel, F d -3 m | a = 8.08599 A | 0.23686 (23.69 wt%) |

## Evidence

The Cu K-alpha pattern (Kalpha1 = 1.540598 A, Kalpha2/Kalpha1 = 0.5) contains the characteristic split low-angle WO3 family near 23.46, 23.95 and 24.71 degrees and the accompanying monoclinic families through the full 9.90-100.09 degree range. A P 21/c neutron parent (COD 2311041) gave a physically valid model and outperformed an older P 21/c record; a triclinic low-temperature WO3 record gave a slightly poorer fit and unsupported extra splitting near 33-35 degrees. Co3O4 is independently supported by coherent families near 19.37, 31.64, 37.20, 38.91, 45.14, 59.68, 65.55, 77.63 and 94.35 degrees. The retained spinel parent was COD 9005896; an alternate database record was rejected for an impossible short contact. Both exported structures pass the occupancy/contact screen.

Wolframite-type CoWO4 was kept on the watch list because it is chemically plausible after heating Co3O4 and WO3 at 500 C. The available exact record was malformed, so four Co-substituted wolframite/scheelite analogues were tested. On the final common profile, two analogues refined to zero and the other two to only 0.10-0.14 wt%, with less than 0.001 percentage-point improvement in Rwp and no coherent diagnostic family around 30.3 degrees. CoWO4 is therefore not included. A trace amount at roughly the 0.2 wt% level or below cannot be determined reliably from this pattern/model.

## Refinement and uncertainty

The final GSAS-II model uses one specimen-displacement correction (-672 micrometers), a smooth positive background, common instrumental broadening, and phase-specific size/strain. The common Gaussian U term was neutralized at zero after a fixed-U grid showed that larger values only traded against phase microstrain and worsened the fit. Both size and strain remained supported by ablation tests; WO3 required uniaxial microstrain along 010. Texture trials on symmetry-distinct axes did not show reproducible multi-family support and were removed. Surface-roughness parameters were strongly mutually correlated, so their accepted attenuation curve was fixed rather than reported as independently determined.

Cells and the Co3O4 oxygen parameter were refined. Refining six WO3 W coordinates reduced chi-square by only about 32 while producing 96-97% parameter correlations, and unrestricted WO3 oxygen refinement produced implausibly large shifts. Those coordinates and tied displacement parameters are therefore not reliably determined by these X-ray data and were retained from the physical neutron parent (Uiso = 0.005 A2).

Independent atomic replay of `final.gpx`, ignoring its cached calculated profile, gives Rwp = 3.0612%, Rp = 2.1952%, reduced chi-square = 3.1696 and goodness-of-fit = 1.7803; no negative-width/background or other replay flags were raised. Residual structure-factor/profile mismatch remains strongest around 23-25, 33-35 and 50-51 degrees, so the formal fraction e.s.d. (0.18 wt%) understates model uncertainty. A practical uncertainty of about +/-1 wt% for each reported crystalline fraction is more defensible. No amorphous fraction can be quantified without an external standard.
