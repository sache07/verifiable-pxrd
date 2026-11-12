# Powder XRD phase analysis

## Result

The crystalline model contains three phases. Fractions are normalized over these modeled crystalline phases only.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MnWO4, wolframite | P 2/c | a=4.79563, b=5.71049, c=4.97858, β=91.1259 | 68.996% |
| Mn3WO6 | R -3 | a=8.89251, c=10.45981 | 15.296% |
| WO3, monoclinic | P 21/c | a=7.69255, b=7.53874, c=10.52471, β=136.0798 | 15.709% |

The final fresh atomic forward replay on all 8,301 observations gives Rwp=2.0053%, Rp=1.5348%, Rexp=1.7712%, and goodness of fit=1.1322. Statistics use `w = 1/max(Iobs,1)` because pointwise standard uncertainties were not supplied. `fit.csv` is this replayed profile, not a cached GSAS-II calculated array.

## Evidence

The dominant reflections are indexed and intensity-matched by ordinary monoclinic wolframite MnWO4 (initial reference COD 1520200). Its refined lattice and chemistry agree with reaction of the reported WO3 and Mn3O4 precursors at 800 °C. Coherent residual triplets and higher-angle reflections match monoclinic WO3; the submitted physically valid P 21/c model was initialized from COD 2311041.

After MnWO4 and WO3 were included, the remaining coherent peaks could not be closed by ordinary manganese-oxide references. MnO (rocksalt and wurtzite), hausmannite/Pbcm Mn3O4, Mn2O3, and rutile MnO2 were tested by replacement or addition in the same multiphase state with the other phases and nuisance settings fixed. Stable Mn3O4 trials collapsed below 0.4 wt%; MnO models either left the diagnostic residual or worsened the common-state fit when retained with the successful residual phase.

Residual-directed prototype transfer then tested distinct target-composition models: R -3, C 2/c, and P 21/c Mn3WO6 frameworks, plus P 21 21 21 and P -31m Mn2WO6 frameworks. The R -3 Mn3WO6 model, obtained by Te→W transfer from the Mn3TeO6 framework (COD 2211528), was the only model that removed the full residual family without boundary-like behavior. In the fixed comparison it reduced Rwp from about 17.2% to 9.7% before subsequent ordinary refinement. The final WO3/Mn3WO6 mass ratio is 1.027, close to 1.043 for a 2 WO3 : 1 Mn3WO6 molar pair; that pair also has an overall Mn:W ratio of 1:1. This provides an independent compositional check. Aborted lower-tungsten-oxide atom-typing trials and a numerically invalid alternate Pbcm trial were treated as unknown, not as negative evidence.

The final state was selected only after resuming ordinary joint refinement and replaying fresh GSAS-II structure factors/reflection lists over the complete measured grid. All three exact submitted CIFs pass the supplied geometry/occupancy screen with no flagged contacts, and the replay reports no negative-width, background, displacement-tensor, or polarization flags.

## Remaining uncertainty

The Mn3WO6 identification is strongly supported by the profile and elemental balance, but its detailed atomic coordinates are less certain because the starting framework is analogue-derived and oxygen positions are weakly constrained by laboratory X-ray data. The WO3 cell is in an unusual but valid P 21/c setting. Instrument broadening was not independently calibrated; profile U reached the adopted upper bound, and angular zero/sample displacement are correlated (sample displacement was fixed for the final cycles). These correlations make formal coordinate and fraction standard uncertainties optimistic, so no reliable error bars are quoted.

The reported fractions do not quantify amorphous material or any phase below the detection/modeling limit. No additional crystalline phase is required by the final residual, but aborted prototype trials remain unresolved rather than disproved.
