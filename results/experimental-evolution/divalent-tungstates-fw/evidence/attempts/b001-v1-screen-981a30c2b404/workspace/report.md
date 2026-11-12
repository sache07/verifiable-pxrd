# Powder XRD phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases.

| Phase | Structural model | Weight fraction | Formal 1σ |
|---|---|---:|---:|
| ZnWO₄ | wolframite, *P*2/*c* | 0.701415 (70.1415 wt%) | 0.000743 |
| ZnO | wurtzite, *P*6₃*mc* | 0.085459 (8.5459 wt%) | 0.000595 |
| WO₃ | monoclinic, *P*2₁/*c* | 0.213127 (21.3127 wt%) | 0.000529 |

The independently replayed, full-grid fit has Rwp = 3.6693%, Rp = 2.8026%, and goodness of fit = 1.3659 for 8,301 points. The saved-project Rwp over its 10–100° fit interval is 3.6713%.

## Evidence and model selection

The ZnWO₄, ZnO, and WO₃ assignments each account for a coherent family of observed lines. Under the same restrained fixed-coordinate comparison, the complete three-phase model gave Rwp = 11.578%. Deleting ZnO, WO₃, or ZnWO₄ worsened Rwp to 12.552%, 20.874%, and 36.991%, respectively. No remaining residual family supported a fourth crystalline phase.

All serious candidate CIFs were normalized and physically screened before comparison. For ZnWO₄, the best passing framework was a wolframite analogue derived from COD 1520642 (Zn₀.₈₉Cd₀.₁₁WO₄), with every mixed Cd/Zn cation occupancy mapped to Zn before fitting. Its fixed-coordinate Rwp was 11.578%, compared with 11.877% for the mapped MgWO₄ wolframite, 12.635% for mapped MnWO₄, and much poorer scheelite/fergusonite alternatives. Wurtzite ZnO was strongly preferred to rocksalt ZnO. The selected WO₃ source, COD 2311041 (*P*2₁/*c*), gave Rwp = 11.578%; the next passing candidate (*P*1̅) gave 12.693%, while orthorhombic, tetragonal, and hexagonal models were substantially worse. Two other WO₃ CIFs were excluded after the physical screen flagged implausibly close oxygen sites.

After inventory/source selection, the refinement stabilized background, scales, cells, angular zero, common profile terms, and polarization. Retained phase-specific effects were [001] March–Dollase texture for WO₃ (ratio 1.3021), and isotropic ZnWO₄ size/strain broadening (0.257 µm and 2,951 ppm). Only ZnWO₄ atomic coordinates were selectively refined; the exported structure still passes the contact/occupancy screen. ZnO and WO₃ coordinates remain at their defensible parent values because ZnO coordinate refinement was negligible and WO₃ coordinate shifts were unstable across restarts. Roughness and weak ZnO/ZnWO₄ texture terms were rejected.

A controlled restart from different profile values with ten background terms converged without frozen parameters to Rwp = 3.6651%; its fractions differed from the selected simpler eight-term model by at most 0.04 percentage point, so the two extra background terms were not retained. A specimen-displacement branch was worse (Rwp = 3.7537%) and showed coupled cell contraction, so the zero-offset branch was selected. The final project has no frozen/bound parameters; the largest absolute correlation is 0.921, and the ZnWO₄ size–strain correlation is 0.915.

## Remaining uncertainty

The tabulated uncertainties are covariance estimates and do not include source-model, preferred-orientation, microabsorption, or other systematic errors. Plausible nuisance branches changed any fraction by no more than about 0.10 percentage point, but that is a sensitivity check rather than a complete uncertainty interval. The ZnWO₄ framework is analogue-derived, and its refined oxygen positions are less secure than the phase identity and lattice. The WO₃ coordinates cannot be determined reliably from this pattern beyond the selected parent model. Fractions are relative to the modeled crystalline material only: without an internal standard, amorphous content and absolute crystallinity cannot be quantified. Trace crystalline phases below the residual/detection level also cannot be excluded.

Independent replay confirmed that `final.gpx`, the three submitted CIFs, the phase fractions, and `fit.csv` agree. All three final CIFs pass the supplied physical screen with no flagged contacts.
