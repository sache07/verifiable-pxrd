# Powder XRD phase analysis

The pattern is a multiphase Pb–W–O mixture rather than a single PbWO₄ product. A seven-phase GSAS-II Rietveld model gives an independently regenerated whole-pattern fit of **Rwp = 8.180%**, **Rp = 5.872%**, and last-cycle **GOF = 2.337** over all 8,282 measured points (10.009–99.994° 2θ). The difference column in `fit.csv` is observed minus calculated.

| Crystalline phase | Space group | Weight fraction | Assessment |
|---|---:|---:|---|
| Scheelite PbWO₄ | I 41/a | 51.58 wt% | Secure dominant phase |
| Massicot PbO | Pbcm | 6.10 wt% | Secure |
| Monoclinic WO₃ | P 21/c | 10.55 wt% | Secure identity and lattice |
| Litharge PbO | P 4/nmm | 8.15 wt% | Secure |
| Pb₂WO₅ | C 2/m | 12.80 wt% | Phase is supported; detailed oxygen framework is analogue-derived |
| Pb₃WO₆ | P 21/m | 10.05 wt% | Phase is supported; detailed oxygen framework is analogue-derived |
| Pb₃O₄ (minium) | P 42/mbc | 0.77 wt% | Tentative trace assignment |

## Evidence

Candidate structures were restricted to the Pb–W–O chemistry implied by PbO and WO₃ precursors, then tested against the complete Cu Kα1/Kα2 profile. Scheelite PbWO₄ accounts for the strongest product reflections, while separate residual line families require both PbO polymorphs and monoclinic WO₃. Pb₂WO₅ and Pb₃WO₆ are needed to account for persistent intermediate-phase peaks, including the residual family near 30.2° and 46.4° 2θ; a five-phase model remained near Rwp ≈ 10.1%. The stable six-phase model gave Rwp = 8.276%. Adding Pb₃O₄ reduced Rwp only to 8.180%, so its sub-1 wt% assignment is reported as tentative rather than definitive.

The PbWO₄, massicot, WO₃, litharge, and Pb₃O₄ models originate from COD entries 9009811, 2310433, 1528915, 9012700, and 1537983, respectively. No exact database models were available for the two intermediate tungstates: Pb₂WO₅ was initialized from isovalent Pb₂MoO₅ (COD 7220560, Mo→W), and Pb₃WO₆ from the unique matching Pb₃SO₆ framework (COD 8103588, S→W). Their cells and bounded coordinates were refined against this pattern. Preferred orientation was required, most strongly for litharge and Pb₃WO₆, and Pb₂WO₅ required anisotropic microstrain.

## Uncertainty and limitations

Fractions are normalized over the modeled crystalline phases only; this measurement does not determine amorphous content. Strong peak overlap, preferred orientation, and correlations among specimen displacement, zero shift, scale, and profile terms make formal fraction standard uncertainties unreliable. In practical terms, the major-phase values should be treated as semiquantitative (roughly a few absolute wt% systematic uncertainty), not exact composition measurements.

The 0.77 wt% Pb₃O₄ fraction is below a robust quantitative level and could plausibly represent an overlapping trace phase or residual model error; neither its identity nor its fraction is reliable enough for a definitive claim. The identities and unit cells of Pb₂WO₅ and Pb₃WO₆ are better supported than their individual light-atom coordinates. The submitted WO₃ and Pb₃O₄ models also retain short O–O contacts present in their source COD structures (about 1.60 and 1.79 Å); there are no impossible contacts below 0.8 Å, but these coordinates merit crystallographic review. Pointwise experimental standard uncertainties were not supplied, so count-statistic weights were used for the reported fit statistics.
