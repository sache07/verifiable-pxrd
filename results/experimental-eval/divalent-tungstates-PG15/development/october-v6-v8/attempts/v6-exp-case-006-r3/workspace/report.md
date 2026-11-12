# PXRD phase analysis

## Result

The measured crystalline material is predominantly triclinic copper tungstate, with a small monoclinic tungsten trioxide remainder. Weight fractions are normalized over the modeled crystalline phases; amorphous material was not quantified.

| Phase | Structural model | Weight fraction | Refined cell (Å, °) |
|---|---|---:|---|
| CuWO₄ | triclinic *P* -1 | 97.776 wt% | a=4.70702, b=5.84088, c=4.87996; α=91.6554, β=92.5342, γ=82.7494 |
| WO₃ | monoclinic *P* 2₁/c | 2.224 wt% | a=7.68413, b=7.53964, c=10.51599; β=136.0571 (valid non-standard setting) |

The formal least-squares uncertainty is ±0.057 wt% for each fraction. This is not an accuracy estimate: uncertainty from profile choice, preferred orientation, structural choice for the minor phase, and the assumed counting errors is larger, plausibly several tenths of a weight percent. Fractions are conditional on the two-phase crystalline model.

The final 10–100° refinement gives Rwp=6.5346%, Rp=4.7319%, GOF=2.6932, with 8,284 observations and 50 variables. The exported full 9.903–100.095° profile has Rwp=6.5282% over 8,301 points. Pointwise uncertainties were not supplied, so Poisson uncertainties (sqrt(counts)) were used.

## Evidence and model selection

The *P* -1 CuWO₄ atomistic model (COD 4000806 topology) explains the dominant peak set and refined to the expected ambient-type CuWO₄ metric. Its coordinates and W isotropic displacement parameter were refined. The exported model has sensible Cu–O and W–O contacts, full occupancies, and no CIF-audit flags.

After CuWO₄ refinement, coherent residual maxima at approximately 23.43, 24.67, 33.56–34.45, 42.18, 51.02, 55.04, 60.32, 72.21, and 77.18° 2θ were reproduced by WO₃. Removing WO₃ and reconverging all remaining variables raises Rwp from 6.5346% to 7.1073%. WO₃ improves weighted residuals in eight of nine 10° regions, demonstrating multi-peak, full-pattern support rather than overlap-only credit.

The submitted *P* 2₁/c WO₃ model uses the COD 2311041 topology. Its scale and cell were refined; atomic coordinates were held to the source topology and conservative positive Uiso values were fixed because a 2.2 wt% component does not support detailed coordinate/ADP refinement. A matched Pnma replacement was markedly worse (Rwp 6.7758%). A pseudo-triclinic WO₃ replacement was numerically near the selected model (Rwp 6.5412%) but failed the stability criterion (maximum shift/esd 23.2). Thus WO₃ itself is secure, but the exact symmetry of this minor component is only moderately certain; *P* 2₁/c is the smallest stable atomistic model supported here.

CuO, monoclinic CuWO₄, and Cu₃WO₆ were retested individually from the mature model. CuO refined to 0.06±0.10 wt%, the additional CuWO₄ scale collapsed, and Cu₃WO₆ gave only a 0.0024 percentage-point Rwp change at about 0.13 wt% without independent multi-peak support; none was retained. Two malformed WO₃ library candidates were rejected after short O–O contacts (1.575 and 0.464 Å). Trace phases below roughly a few tenths of a weight percent cannot be excluded reliably, and no fraction is assigned to them.

## Refinement integrity

The nuisance model comprises a 12-term Chebyshev-1 background, sample displacement, global U/V/W/X/Y peak-shape terms, and weak CuWO₄ [001] March–Dollase texture (ratio 0.98498). A zero-only angular model was worse (Rwp 6.7004%); the apparently better joint zero/displacement branch was rejected because those parameters correlated at 99.99% and also coupled strongly to the cells. Size, microstrain, axial-divergence, roughness, and redundant polarization refinements were rejected for negligible benefit, bounds, or excessive correlation. Removing the retained weak texture worsened Rwp to 6.5682%.

The final refinement converged with maximum shift/esd 0.014 and no dropped variables. Fresh profile regeneration exactly reproduces the profile saved in `final.gpx`; all regenerated Gaussian and Lorentzian total widths remain positive. Both submitted CIFs pass composition, occupancy, duplicate-site, symmetry-expansion, and contact audits without flags.
