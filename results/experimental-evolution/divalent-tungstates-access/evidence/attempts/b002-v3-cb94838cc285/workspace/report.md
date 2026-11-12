# Powder XRD phase analysis

The best-supported crystalline model contains three phases:

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| MnWO4, wolframite | P 2/c | a=4.79694, b=5.70323, c=4.97221, β=91.1077 | 0.6220 |
| WO3, monoclinic | P 21/c | a=7.68747, b=7.53810, c=10.5122, β=136.032 | 0.2136 |
| Mn2WO5, analogue-derived | P 21/c | a=6.22231, b=8.91572, c=10.4894, β=124.079 | 0.1644 |

Fractions are normalized over these modeled crystalline phases; no amorphous fraction was determined.

## Evidence

The dominant reflection family is indexed by wolframite MnWO4 (starting reference COD 1520200). A second family is indexed by residual monoclinic WO3, consistent with unreacted precursor. COD 2311041 was retained for WO3 because it gives the same monoclinic family with physically normal distances; a competing WO3 record produced short O–O contacts after refinement and was rejected.

After those phases were fitted, a coherent residual family remained, including lines near 20.40, 31.74, 35.11, 46.49, and 54.36° 2θ. Ordinary Mn oxides and tested Mn–W–O references did not index this family. A systematic comparison of 136 accessible A2BO5 frameworks supported an Mn2WO5 composition. The selected start was made from P21/c Cu2AsO5 (COD 9011171) by Cu→Mn and As→W substitution and cell adaptation. With comparable lattice relaxation, this lower-symmetry model fit the two-phase residual substantially better than the leading Pnnm relatives (screen Rwp 11.87% versus 14.20%). In the final model, the major residual maxima all coincide with accepted-phase reflections to within 0.024°.

The independently regenerated, full-grid GSAS-II profile has Rwp=6.2618%, Rp=3.9619%, and GOF=3.1497 using Poisson count weights. Replay regenerated all reflections and structure factors from `final.gpx`, optimized no parameters, and reported no profile or physical-review flags. The empirical background remains positive over the full scan.

## Remaining uncertainty

The Mn2WO5 assignment is the chemically economical model for the otherwise unindexed family, but it is transferred from another chemistry rather than confirmed by an exact same-composition reference. Its cell and heavy-atom contribution are supported by the powder data; the detailed Mn/O substructure is not uniquely determined. Unconstrained light-atom trials produced large displacements or short contacts and were rolled back. Accordingly, the 16.44 wt% fraction and the Mn2WO5 coordinates should be treated as model-dependent rather than as a high-precision structure determination.

A weak isolated residual near 25.42° is not indexed by the three phases. It does not form a coherent additional reflection family, so a fourth crystalline phase and its fraction cannot be determined reliably from this pattern. The WO3/Mn2WO5 fraction split is also correlated with broadening and texture; formal covariance errors would understate that model uncertainty.
