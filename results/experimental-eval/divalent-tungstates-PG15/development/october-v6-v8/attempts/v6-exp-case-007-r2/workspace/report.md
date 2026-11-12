# PXRD phase analysis

The modeled crystalline product contains 78.047 +/- 0.146 wt% wolframite MgWO4, 14.602 +/- 0.076 wt% monoclinic WO3, and 7.351 +/- 0.153 wt% periclase MgO. These are one-standard-deviation least-squares errors and do not include model-systematic error. Fractions are normalized only over the modeled crystalline phases.

| Phase | Refined structure | Refined cell (angstrom, degrees) | Crystalline wt% |
|---|---|---|---:|
| MgWO4 | P2/c (No. 13), wolframite | a=4.68917, b=5.67310, c=4.92764, beta=90.7742 | 78.047 +/- 0.146 |
| WO3 | P21/c (No. 14), monoclinic | a=7.68878, b=7.53307, c=10.52729, beta=136.0935 | 14.602 +/- 0.076 |
| MgO | Fm-3m (No. 225), periclase | a=4.21131 | 7.351 +/- 0.153 |

## Evidence and refinement

The Mg-W-O precursor context and full-pattern screening identified atomistic COD models 9013902 (MgWO4), 2311041 (WO3), and 9000499 (MgO). Each model passed the supplied CIF audit and accounts for multiple reflections distributed through the scan. Matched leave-one-out refinements increased Rwp from 8.2707% to 51.71% without MgWO4, 18.73% without WO3, and 9.22% without MgO, supporting all three components rather than overlap-only scale factors.

Clean WO3 alternatives were carried through the same mature nuisance model. The selected P21/c model gave Rwp=8.2707%, compared with 8.4069% for a converged P-1 model (COD 2106293) and 11.9450% for Pnma (COD 2107312). A malformed candidate was rejected after CIF audit rather than refined.

The final GSAS-II fit used the supplied Cu K-alpha doublet, 10-100 degrees 2theta for refinement, a 12-term smooth Chebyshev-1 background, global U/W/X profile terms, one surface-roughness term, and specimen displacement of -512.20(75) micrometres. MgWO4 cell and coordinates were refined with weak March-Dollase [001] texture (ratio 0.9777(17)); WO3 and MgO coordinates/ADPs remained at their audited reference values. Phase-specific size/strain, axial divergence, extra texture, and joint zero/displacement branches were rejected as bounded, negative, redundant, unstable, highly correlated, or unsupported by whole-pattern improvement. Final statistics are Rwp=8.2707%, Rp=5.8696%, Rexp=2.8639%, and GOF=2.8946 for 8,284 observations and 38 variables. The saved full-grid profile was regenerated and passed the supplied GPX audit.

## Remaining uncertainty

The existence and approximate amount of a WO3 phase are secure, but its exact low-symmetry description is less definitive because the P-1 alternative is only 0.136 Rwp percentage point worse. Likewise, MgWO4 [001] and [110] texture axes are nearly tied, although omitting texture is materially worse; fractions change by only a few tenths of a percentage point across these nuisance alternatives. Correlated residual structure remains (GOF above one), so the covariance errors likely understate practical uncertainty. Without an internal standard, amorphous content and absolute crystalline yield cannot be determined; the reported fractions are conditional on the three-phase crystalline model.
