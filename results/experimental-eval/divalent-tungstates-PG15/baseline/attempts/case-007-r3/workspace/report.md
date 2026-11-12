# Quantitative phase analysis

## Result

The pattern is described by three crystalline phases. Fractions are normalized over those modeled crystalline phases; they do not measure any amorphous content.

| Phase | Space group | wt% | Formal esd (wt%) | Refined cell |
|---|---:|---:|---:|---|
| MgWO4 | P 2/c | 77.59 | 0.16 | a = 4.695014, b = 5.680393, c = 4.933837 A, beta = 90.77457 deg |
| WO3 | P 21/c | 14.96 | 0.11 | a = 7.698500, b = 7.542025, c = 10.541363 A, beta = 136.09743 deg |
| MgO | F m -3 m | 7.46 | 0.15 | a = 4.216686 A |

The refined profile gives Rwp = 8.43%, Rp = 6.15%, Rexp = 2.86%, and GSAS-II goodness of fit = 2.95 over 8301 observations. `fit.csv` defines the difference as observed minus calculated.

## Evidence

The dominant wolframite-type MgWO4 model accounts for the main low-angle reflection at about 15.93 deg 2theta and the dense peak set through the full scan. Monoclinic WO3 is required by the resolved group near 23.45, 24.00, and 24.68 deg and by many weaker reflections. Rock-salt MgO is independently supported by its complete allowed sequence near 37.27, 43.20, 62.63, 74.95, 78.90, and 94.25 deg; omitting it leaves coherent positive residuals at those positions. This assemblage is chemically consistent with MgO + WO3 -> MgWO4 at 900 degC with residual starting oxides.

Reference models were COD 9013902 (MgWO4, P2/c), COD 2311041 (WO3, P21/c; neutron structure), and COD 9000499 (MgO, Fm-3m). The WO3 CIF retains a valid historical high-beta P21/c cell setting. Its W-O distances remain chemically plausible, as do the Mg/W coordination polyhedra in MgWO4.

## Refinement and uncertainty

GSAS-II used the supplied Cu Kalpha wavelengths (1.540598/1.544426 A) with Kalpha2/Kalpha1 fixed at 0.500. Because the input supplied no point uncertainties, sigma = sqrt(max(counts, 1)) was assigned. Refined terms included phase scales and cells, zero offset, a 15-term Chebyshev background, and empirical U/V/W peak-width terms. Phase-dependent isotropic size/strain terms were estimated in preliminary cycles and then held fixed; they should not be interpreted as calibrated crystallite sizes or microstrains. MgWO4 coordinates and the two WO3 W sites were refined in staged cycles; WO3 oxygen coordinates were retained from the neutron reference and all WO3 sites shared one refined isotropic displacement parameter.

The formal phase-fraction esds (0.11-0.16 wt%) are conditional and underestimate total uncertainty. Peak-profile alternatives changed individual fractions by at most about 0.4 wt%, but the lack of a measured instrumental profile, the inferred counting statistics, strong profile-parameter correlation, and serially correlated residuals make approximately +/-1 wt% absolute a more realistic working uncertainty. Oxygen coordinates in the minor WO3 phase are not independently determined by this laboratory X-ray pattern. Trace phases may remain below detection, and no amorphous fraction can be quantified without an internal standard.
