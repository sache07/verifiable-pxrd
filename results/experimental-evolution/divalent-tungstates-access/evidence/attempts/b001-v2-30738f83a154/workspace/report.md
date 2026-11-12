# Powder XRD phase analysis

The metadata describes the 800 C product of WO3 and Mn3O4 measured in reflection geometry with Cu Kalpha1/Kalpha2 radiation (1.540598/1.544426 A, intensity ratio 0.5). The full 9.903-100.095 degree 2theta range was modeled.

The crystalline pattern is modeled by MnWO4, WO3, and a rhombohedral Mn3WO6 phase. The normalized crystalline weight fractions are 68.126%, 16.323%, and 15.552%, respectively. No amorphous fraction was determined.

| Phase | Space group | Refined cell (A, degrees) | Weight fraction |
|---|---|---|---:|
| MnWO4 | P 2/c (No. 13) | a=4.80041, b=5.71588, c=4.98314, beta=91.1271 | 0.681255 |
| WO3 | P 21/c (No. 14) | a=7.70032, b=7.54496, c=10.53642, beta=136.0829 (nonstandard setting) | 0.163227 |
| Mn3WO6 | R -3 (No. 148) | a=b=8.90113, c=10.46984, gamma=120 | 0.155517 |

## Fit and verification

The final GSAS-II model was replayed from its saved atoms and profile parameters on all 8,301 measured points, without using its cached calculated curve or optimizing any parameter. That replay gives Rwp=2.85743%, Rp=2.21621%, chi-square sum=21,537.40, and reduced chi-square=2.59957 for Poisson-proxy weights `1/max(Iobs,1)`. The replay left the project hash unchanged and raised no profile-review flags. `fit.csv` is the observed/calculated/difference profile from this replay.

All submitted CIFs pass the broad geometry/occupancy screen. Their minimum interatomic contacts are 1.738 A (MnWO4), 1.716 A (WO3), and 1.912 A (Mn3WO6); calculated densities are 7.356, 7.253, and 6.167 g cm-3, respectively.

## Phase evidence

MnWO4 and WO3 were identified by ordinary reference matching and then refined jointly. The retained models derive from COD 1520200 (MnWO4, P 2/c) and COD 2311041 (WO3, P 21/c). For WO3, the physically valid P 21/c replacement gave Rwp=3.769% in the same replacement state, compared with 3.813% for a physically valid triclinic P -1 alternative. An earlier rounded WO3 reference was rejected because it generated a 1.58 A O-O contact; it has exactly zero scale in `final.gpx` and is not submitted.

Coherent residual peaks remained after the ordinary references. Residual-directed prototype transfer tested distinct Mn-W-O candidates in common multiphase states. The retained Mn3WO6 model was made by Te-to-W substitution in the R -3 Mn3TeO6 framework (COD 2211528). After common profile/cell relaxation, this model reached Rwp=13.73%, versus 17.21% for the Pnnm Mn2WO5 transfer. C 2/c Mn3WO6 analogues and P 21 21 21/P 4/nmm Mn2WO6 variants were worse. Cross-additions gave only 0.49-0.84 wt% for the competing secondary model, so both were not retained. The final R -3 cell is also reproducible through subsequent ordinary refinement.

Mn3O4 precursor models were retested with the final three-phase model and all accepted phases/nuisance terms fixed. Two Pbcm settings converged reproducibly from four starting scales to only 0.077 and 0.059 wt%, changing Rwp by less than 0.001 percentage point; these amounts are below reliable quantification and were omitted. Spinel Mn3O4 trials repeatedly froze at the lower scale bound, so those trials are treated as unknown rather than proof of absence. A trace spinel precursor therefore cannot be excluded reliably.

## Remaining uncertainty

The Mn3WO6 symmetry, cell, and contribution to the profile are supported, but its atomic coordinates are transferred from an analogue rather than independently solved from this powder pattern. In particular, its oxygen coordinates and any defect chemistry cannot be determined reliably here. The WO3 internal coordinates were likewise held to the physically screened reference while its cell and profile were refined.

Several nuisance parameters are at or near imposed physical bounds (notably U, zero, polarization, and one roughness term), and size/strain/fraction correlations are not represented by the final-cycle covariance alone. The printed fractions are exact project values for reproducibility; a practical uncertainty of roughly 1-2 wt% is more realistic than their displayed digits. Trace Mn3O4 and amorphous material remain unquantified.
