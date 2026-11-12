# Powder XRD phase analysis

## Result

The pattern is modeled by three crystalline phases. Fractions are normalized over those modeled crystalline phases only.

| Phase | Space group | Refined cell (A, deg) | Weight fraction |
|---|---:|---|---:|
| MnWO4 (wolframite) | P2/c | 4.79880, 5.70545, 4.97423; beta 91.1065 | 61.43% |
| WO3 (monoclinic) | P21/c | 7.68814, 7.53883, 10.51516; beta 136.0464 | 22.36% |
| Mn2WO5 | P21/c | 6.22280, 8.91930, 10.49505; beta 124.1054 | 16.21% |

The independently regenerated atomic-model profile gives **Rwp = 6.63292%**, Rp = 4.32799%, and GOF = 3.3299 over all 8301 measured points. The fresh replay performed no parameter optimization and reproduced the saved Rwp exactly.

## Evidence

- MnWO4 matches the wolframite reference (COD 1520200) in peak positions and intensities. Its cell and symmetry-allowed coordinates were refined.
- A later, physically sound monoclinic WO3 model (COD 2311041) was selected. In the same multiphase nuisance state it improved Rwp from 7.031% to 6.772% before further ordinary refinement. The initially tried 1960 WO3 coordinates had a 1.58 A full-occupancy O...O contact and were not submitted. A P-1 WO3 analogue refined close to pseudo-monoclinic metrics, so the simpler P21/c assignment was retained; a symmetry ambiguity at that level remains possible.
- Coherent residual peaks in the MnWO4 + WO3 model were best explained by a P21/c Mn2WO5 framework transferred from Cu2AsO5 (COD 9011171; Cu->Mn, As->W). In matched common-state screening this model lowered Rwp from 16.874% to 14.699%; Pnnm Mn2WO5 alternatives were poorer and their scales collapsed when included beside P21/c.
- Mn3O4 precursor, Mn2O3, MnO2, alternate Pnnm Mn2WO5, and the highest residual-correlation oxide candidates all refined to numerical zero or unstable trace scale in the converged common state. Rocksalt/wurtzite MnO remained below about 0.4 wt% with unstable cell/scale and therefore is not reliably identified or quantified. Failed or aborted trials were treated as unknown, not as rejection evidence.

## Uncertainty and physical checks

The Mn2WO5 phase identity, cell, and approximate fraction are supported by the residual improvement, but its detailed coordinates are less secure than those of MnWO4 and WO3 because no direct same-composition reference was available and oxygen contributes weakly to Cu X-ray scattering. The submitted model uses only a bounded 10% profile-directed displacement from the transferred prototype; stronger coordinate moves generated short contacts and were rejected.

All three submitted CIFs pass the occupancy/contact screen. Their shortest O...O distances are 2.53 A (MnWO4), 2.54 A (WO3), and 2.58 A (Mn2WO5); the shortest Mn2WO5 W-O distance is 1.68 A. No negative ADP, peak-width, or background warning was raised by replay.

The angular zero is at the allowed +0.25 deg bound and is correlated with a +519.6 um specimen shift; X is at its allowed 0.1 lower bound. Thus absolute cell uncertainties are more systematic than the least-squares covariance alone suggests. Fractions should be read at roughly the 0.5-1 wt% systematic level rather than as exact values. Amorphous material, if present, is not measured by this normalization.
