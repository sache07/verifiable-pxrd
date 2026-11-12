# Powder XRD phase analysis

The 900 °C CoO + WO3 specimen is modeled as two monoclinic crystalline phases. Fractions are normalized over those modeled crystalline phases; they do not quantify amorphous material.

| Phase | Space group | Refined cell | Crystalline wt. fraction |
|---|---|---|---:|
| CoWO4 (wolframite) | P 2/c | a = 4.66956 Å, b = 5.68304 Å, c = 4.94978 Å, beta = 90.0027° | 0.28499 (28.50 wt%) |
| WO3 | P 21/c | a = 7.30628 Å, b = 7.53605 Å, c = 10.5360 Å, beta = 133.107° | 0.71501 (71.50 wt%) |

The independently regenerated full-range profile gives Rwp = 4.9502%, Rp = 3.8357%, and goodness of fit = 1.5101 for 8,301 points. The scale-only covariance gives about 0.10 wt% one-sigma uncertainty on either fraction, but this is smaller than the likely structure/profile systematic uncertainty; the major-phase fractions are best interpreted to roughly 0.5–1 wt%.

## Evidence and model selection

The WO3 assignment is supported by the characteristic 23.18/23.67/24.40° triplet and families near 33.34–34.20° 2theta. A monoclinic neutron WO3 parent (COD 2311041) gave physical W–O geometry and decisively removed residuals left by the older and alternate WO3 records. CoWO4 is required by coherent families near 15.61, 19.05, 30.70, 36.44, 38.61, 44.38, 47.27, and 52.14° 2theta.

No usable exact CoWO4 record was available, so several isostructural wolframite parents were challenged under the same profile. The submitted P 2/c model is derived from FeWO4 (COD 9008124) by the chemically conservative Fe2+ to Co2+ site substitution; FeWO4 and MgWO4 parents were close, with the Fe parent marginally best. The refined composition, lattice, and phase assignment are reliable, but the CoWO4 oxygen coordinates are not independently determined by this overlapped Cu X-ray pattern. Oxygen coordinates were therefore retained from the physical parent rather than accepting unstable unconstrained shifts. The same caution applies, less severely, to the detailed WO3 oxygen coordinates.

The final width model uses isotropic size broadening for both phases and [100] uniaxial microstrain only for WO3. Mild [001] CoWO4 and [110] WO3 March–Dollase terms are supported: removing texture raises Rwp to 5.013%. Low-angle surface roughness is also required; removing it raises Rwp to 7.19%. Collinear common-width and size terms, and a roughness parameter driven to a limit, were pruned or fixed just inside the physical range. The saved model then reproduced on repeated save/reopen cycles without frozen parameters, and independent atomic replay raised no negative-width, background, or displacement-parameter flags.

CoO and Co3O4 were revisited as weak-phase candidates. Co3O4 collapsed to zero scale. CoO refined to only about 0.2 wt% in a provisional model, produced no credible unique reflection family, and gave a negligible fit change; its presence and fraction cannot be determined reliably, so it is not included. No other coherent crystalline residual family was found.
