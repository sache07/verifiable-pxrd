# Powder XRD phase analysis

The crystalline model contains **scheelite CaWO4 (79.88 wt%)**, **monoclinic WO3 (13.82 wt%)**, and **calcite CaCO3 (6.30 wt%)**. Fractions are normalized over these modeled crystalline phases; amorphous material was not quantified.

| Phase | Space group | Refined cell (A, degrees) | Weight fraction |
|---|---|---|---:|
| CaWO4, scheelite | I 41/a | a = 5.23595, c = 11.33075 | 0.79880 |
| WO3, monoclinic | P 21/c | a = 7.68883, b = 7.55200, c = 10.51013, beta = 135.9417 | 0.13815 |
| CaCO3, calcite | R -3 c | a = 4.94075, c = 17.24721 | 0.06304 |

## Evidence

The dominant reflections at approximately 18.27, 28.43, 31.21, 33.84, 38.92 and 46.89 degrees are indexed by scheelite CaWO4. The sharper family near 22.77, 23.18, 23.99, 26.19 and 32.88 degrees requires monoclinic WO3. After those two phases, a coherent positive family near 29.1, 35.7, 42.8, 48.2 and 57.0 degrees gives a stable calcite contribution. Remaining large residuals are paired positive/negative lobes around modeled strong peaks, rather than a new independent peak family.

All available same-formula WO3 and CaWO4 structures were inspected, and topology-diverse carbonate and plausible Ca-W-O/Ca-O alternatives were screened under common nuisance settings. P 21/c WO3 COD 2311041 was the best stable full-profile WO3 model. Ambient R -3 c calcite was preferred over a numerically lower-Rwp R -3 m model because the latter required about 3.5% cell distortion and extreme broadening. The detailed statuses, including divergent branches retained as unknown rather than rejected, are in `candidate_ledger.json`.

Limited coordinate refinement moved only the scheelite oxygen and the two WO3 tungsten sites by plausible small amounts. Refining all WO3 oxygen coordinates caused large, unstable displacements and was rolled back. One reproducible WO3 [100] uniaxial microstrain term was retained; texture and surface roughness were not supported. Every submitted CIF passes the occupancy/contact screen, with chemically reasonable nearest contacts.

## Fit and uncertainty

Fresh atomic replay of `final.gpx` over all 8301 points gives **Rwp = 3.70768%**, weighted chi-square **11586.7399**, and GOF **1.18252**, with no replay profile warnings. `fit.csv` is generated from that replay, not from cached calculated arrays.

CaWO4 and WO3 identities and their approximate fractions are well supported. Calcite is clearly detected, but its exact cell and fraction are less reliable because its peaks are weak, broad, and overlap the major phases. Plausible fixed calcite profiles gave roughly 4-7 wt%; varying its fixed isotropic displacement over the full laboratory range with the submitted profile gave about 6.0-6.8 wt%. The reported 6.30 wt% should therefore be read as approximately 6 wt%, with a systematic uncertainty of a few weight percent; the refined calcite metric is also not reliable at the precision printed in the CIF.
