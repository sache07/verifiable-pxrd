# Powder XRD phase analysis

The pattern is explained by three crystalline phases. Weight fractions are normalized over those phases; without an internal standard, this analysis does not determine an amorphous fraction.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| ZnWO4 | P 1 2/c 1 (No. 13) | a=4.70266, b=5.73483, c=4.93362; α=90.000, β=90.638, γ=90.000 | 81.88 wt% (formal 1σ 0.09 wt%) |
| WO3 | P 1 21/c 1 (No. 14) | a=7.31160, b=7.52298, c=10.53829; α=90.000, β=133.018, γ=90.000 | 13.18 wt% (formal 1σ 0.05 wt%) |
| ZnO | P 63 m c (No. 186) | a=3.25591, b=3.25591, c=5.18407; α=90.000, β=90.000, γ=120.000 | 4.94 wt% (formal 1σ 0.09 wt%) |

## Evidence

The dominant peak set indexes as wolframite ZnWO4. A W-bearing wolframite parent (COD 9008131, with the divalent site changed to Zn) gave the correct intensity topology; refining its eight symmetry-independent coordinates removed the large residual near 41.6° 2θ. The remaining peaks require monoclinic WO3 and wurtzite ZnO. For WO3, the P21/c COD 2311041 model gave a better whole-pattern fit than the older monoclinic and triclinic alternatives, while retaining a metric within the expected reference mismatch. ZnO accounts for the characteristic wurtzite residuals near 31.8, 34.5, and 36.3°.

The final full-grid atomic replay gives Rwp=2.802%, Rp=2.100%, GOF=1.061, and a Poisson-standardized residual RMS of 1.059. No coherent unmodeled peak remains; the largest point residual is about 4.5 counting-statistics standard deviations.

## Remaining uncertainty

The formal scale-covariance errors in the table are smaller than model uncertainty. Comparisons among acceptable structural/profile branches suggest a practical abundance uncertainty of roughly ±0.5 wt% per phase. The WO3 oxygen coordinates could not be refined reliably: unconstrained/broadly bounded refinement drove several sites to bounds and produced an implausibly short W-O contact, so the submitted WO3 model refines the X-ray-sensitive W positions but retains the published oxygen framework. The ~5 wt% ZnO microstrain is also weakly determined, though its phase identity and scale are stable.

Because no calibrated profile was supplied, zero, specimen displacement, and lattice parameters are strongly correlated. The final cycles fix an in-range zero at 0.06961° and refine the displacement (-474.3 µm); this choice stabilizes the cells without changing the phase inventory or fractions. Preferred orientation is required for ZnWO4 [111], WO3 [110], and ZnO [001].

The submitted CIFs, fractions, and fit.csv were exported from final.gpx.
