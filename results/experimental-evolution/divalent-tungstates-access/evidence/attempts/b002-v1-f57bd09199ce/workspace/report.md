# Powder XRD phase analysis

## Result

The pattern is modeled by three crystalline phases. Fractions are normalized over those phases:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| ZnWO4 | wolframite, P2/c | 0.83195 (83.20 wt%) |
| WO3 | low-symmetry monoclinic, P2_1/c | 0.11525 (11.53 wt%) |
| ZnO | wurtzite, P6_3mc | 0.05280 (5.28 wt%) |

An independent atomic forward replay of `final.gpx` gives Rwp = 10.8816%, Rp = 6.4534%, Rexp = 2.6464%, and goodness of fit = 4.112 on all 8301 points. `fit.csv` is the replayed observed/calculated/difference profile, not a cached GSAS-II curve.

## Evidence

The dominant peak families select a wolframite P2/c topology. With no exact ZnWO4 entry in the supplied library, target-composition models were constructed from CoMoO4-II, MnReO4 and ScNbO4 wolframites and compared with triclinic ZnMoO4, scheelite CdWO4 and fergusonite CaWO4 analogues. The CoMoO4-II-derived wolframite model was clearly best; the symmetry/topology controls either fit poorly, collapsed in scale, or did not complete reproducibly.

All supplied exact-formula WO3 and ZnO structures were enumerated. Low-symmetry monoclinic/triclinic WO3 models gave the only large, stable second-phase contribution; COD 2311041 was retained because it gave the best common-screen Rwp and has neutron-derived oxygen positions. Of wurtzite, rocksalt and zincblende ZnO, only wurtzite made a reproducible positive contribution in the closed model. The resulting elemental mole ratio is Zn:W = 1.048, independently consistent with near-balanced ZnO/WO3 precursor chemistry.

The sole retained non-isotropic nuisance term is March-Dollase texture on ZnWO4 [111] (ratio 0.697). Identical [001], [100], [010] and [110] trials gave negligible or much smaller improvements. Remaining large positive residuals occur at modeled reflections and are paired with nearby negative lobes—for example +41.557° versus a calculated 41.581° reflection, bracketed by negative residuals at 41.329° and 41.840°. Similar pairs occur near 31.0°, 24.1° and 19.2°. This supports intensity/shape/calibration mismatch rather than a coherent fourth peak family.

## Physical checks and uncertainty

Unconstrained ZnWO4 oxygen refinement was rejected: although it lowered Rwp to 10.41%, it shortened O-O to 1.745 Å. The submitted analogue-constrained model has minimum O-O, W-O and Zn-O distances of 2.471, 1.786 and 2.002 Å. Minimum W-O in WO3 is 1.672 Å and Zn-O in ZnO is 1.979 Å. Occupancies and displacement parameters are physical, and independent GSAS-II replay returned no profile-review flags.

The ZnWO4 topology and all three phase identities are reliable, but its oxygen coordinates are not independently determined by this pattern. The exact WO3 distortion is also not unique: triclinic and another monoclinic description fit almost as well, so the submitted P2_1/c CIF should be interpreted as the best representative of the low-symmetry WO3 family. Formal fraction uncertainties cannot be assigned reliably because preferred orientation, scale, and calibration are correlated; the fractions are best read to about the nearest 1 wt%.

The fitted zero offset (+0.403°) is correlated with lattice terms and unmodeled specimen displacement. Bounded zero/displacement branches did not complete reproducibly and were marked unknown rather than retained. Consequently, absolute lattice parameters carry more uncertainty than the phase inventory. The candidate decisions are recorded in `candidate_ledger.csv`.
