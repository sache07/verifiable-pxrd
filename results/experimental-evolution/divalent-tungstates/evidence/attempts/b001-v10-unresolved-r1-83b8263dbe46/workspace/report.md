# PXRD phase analysis

The pattern is best described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases; they do not measure amorphous material.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO₄, scheelite | I4₁/a | a = 5.39313, c = 11.89970 | 58.37 wt% |
| WO₃, triclinic | P-1 | a = 7.28862, b = 7.55542, c = 7.69428; α = 90.0914, β = 90.8795, γ = 90.1039 | 26.06 wt% |
| SrCO₃, strontianite | Pnma | a = 6.02703, b = 5.09688, c = 8.39327 | 15.57 wt% |

The formal counting-statistical uncertainties are 0.17, 0.14, and 0.17 percentage points, respectively. They are much smaller than model uncertainty. A more realistic interpretation is approximately ±1–2 wt% absolute because preferred orientation, profile anisotropy, and the choice of structural parent affect scale factors. No precursor amounts or WO₃:SrCO₃ ratio were supplied, so a fixed mass-balance closure could not be applied.

## Evidence and model selection

Scheelite SrWO₄ accounts for the strong families near 17.456, 27.203, 44.828, 55.53, and 72.66° 2θ. Triclinic WO₃ accounts for the characteristic 22.51/22.94/23.82° triplet and families near 33.59 and 76.10°. Strontianite SrCO₃ is required by independent peaks near 24.65/25.29°, 34.6–36.0°, and 43–47°. Its multiple independent families and stable positive scale support retention as unreacted precursor.

The SrWO₄ model was adapted from scheelite CaWO₄ (COD 7219229) by Ca→Sr substitution and cell refinement. Under the same restored nuisance model it gives Rwp = 3.993%, compared with 4.147% for the passing SrMoO₄-derived alternative. WO₃ COD 2106293 (P-1) gives Rwp = 3.993%, compared with 4.664% for the passing P2₁/c record COD 2311041. SrCO₃ uses COD 9008198.

Directional strain was required for WO₃: removing it worsened Rwp to 4.719%, while an isotropic-size branch remained stuck at the neutral 10 µm value. The selected [101] strain axis was replay-stable and slightly better than [010] (Rwp 3.993% versus 3.995%); [100], [001], [011], and [110] were worse. This near-tie means the exact broadening direction is not uniquely determined. SrWO₄ [112] strain also reappeared from a neutral start, although its gain was modest. Axial [001] March–Dollase texture for WO₃ was strongly favored over no texture and a diagonal [101] model.

Low/middle/high-angle profile checks support the selected broadening. For SrWO₄, observed/calculated FWHM values are 0.172/0.176° at 17.456°, 0.240/0.235° at 44.82°, and 0.337/0.335° at 72.65°. For WO₃ they are 0.210/0.231° at 22.52°, 0.245/0.252° at 33.56°, and 0.378/0.412° at 76.10°. The calculated SrWO₄ peaks remain about 0.02–0.03° too narrow around 86–95°, which is a residual profile limitation.

The charge-balanced Sr₃W₂O₉ candidate (COD 2311977) was explicitly tested after health screening. Starting scales differing by a factor of ten both collapsed to 10⁻¹², and its strongest expected families did not form two coherent residual groups, so it was not retained. No WO₃ polymorph coexistence or other weak phase met the replay-stability gate.

## Refinement and uncertainty

The full 9.903–100.095° range was refined with the reported Cu Kα₁/Kα₂ wavelengths and fixed 0.5 intensity ratio. Poisson counting weights were used because pointwise uncertainties were not supplied. The final model uses a six-term smooth background, one specimen-displacement correction, nonnegative U/W/X profile terms (U fixed at zero), refined polarization, neutral roughness, neutral size, and only the supported phase-strain and March–Dollase terms. Final statistics are Rp = 2.965%, Rwp = 3.993%, Rexp = 2.861%, and goodness-of-fit = 1.398 for 8,301 observations and 31 refined variables.

All three final CIFs pass `learned/cif_health.py` with ordered full-occupancy sites and no hard contacts. Atomic coordinates and occupancies were retained from the literature models; only cells and powder-profile quantities were refined. Thus the phase identities and crystalline fractions are well supported, but this powder pattern does not independently determine detailed atomic displacements. The nearly monoclinic metric of P-1 WO₃ also leaves some symmetry uncertainty despite its clear fit advantage over the tested P2₁/c model.

The submitted `final.gpx` was reopened and replayed over the full range before exporting the CIFs, `fit.csv`, and `result.json`.
