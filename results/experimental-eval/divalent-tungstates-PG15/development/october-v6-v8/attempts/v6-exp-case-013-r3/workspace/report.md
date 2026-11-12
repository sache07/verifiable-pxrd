# Quantitative phase analysis

The pattern was measured in reflection geometry with Cu Kα radiation over 10.009–99.994° 2θ. The sample context is a PbO + WO₃ mixture heated at 500 °C. A four-phase atomistic Rietveld model gives the following crystalline-phase composition:

| Phase | Space group | Weight fraction | Formal e.s.d. |
|---|---:|---:|---:|
| PbWO₄, scheelite | *I*4₁/*a* (88) | 76.15 wt% | 0.31 wt% |
| γ-WO₃ | *P*-1 (2) | 8.62 wt% | 0.28 wt% |
| PbO, massicot | *Pbcm* (57) | 10.31 wt% | 0.27 wt% |
| PbO, litharge | *P*4/*nmm* (129) | 4.92 wt% | 0.15 wt% |

These fractions are normalized over the four modeled crystalline phases only. They exclude any amorphous material and a weak unresolved crystalline residual; consequently, the listed values are conditional rather than absolute whole-sample fractions. The quoted e.s.d.s are least-squares errors and understate uncertainty from model choice and peak overlap.

## Fit and structural model

The final refinement has Rwp = 14.936%, Rp = 10.602%, Rexp = 3.500%, and goodness of fit = 4.267 (8,282 points; 7 refined variables). It converged with no singular variables and a maximum shift/e.s.d. of 0.00165. The larger-than-unity goodness of fit reflects systematic residual intensity as well as the absence of supplied pointwise standard uncertainties.

The starting atomistic models were scheelite PbWO₄ (COD 9009811), γ-WO₃ (COD 2106293), massicot PbO (COD 2310433), and litharge PbO (COD 9012700). Unit cells were settled in staged refinements. The final cycle refined four scales, one global Gaussian-width term, polarization, and isotropic microstrain for massicot; atomic coordinates, occupancies, displacement parameters, and the settled cells were held fixed to avoid overfitting overlapping minor phases. All exported CIFs pass the supplied composition, occupancy, duplicate-site, symmetry-expansion, and contact audit without flags. Regeneration from `final.gpx` reproduces the saved calculated profile exactly, and all total peak widths remain positive.

## Identification evidence

Each retained phase has positive scale and support from multiple reflections. Matched leave-one-phase-out fits increase Rwp from 14.936% to 38.247% without scheelite PbWO₄, 15.684% without γ-WO₃, 17.091% without massicot, and 15.890% without litharge. Thus, both PbO polymorphs are independently required rather than one merely dividing an overlap with the other.

Structurally distinct alternatives were tested against the mature four-phase baseline. A Pb-deficient Pb₇W₈O₈.₈ scheelite-related replacement gave Rwp = 16.004%; a monoclinic WO₃ replacement gave 15.343%; and raspite PbWO₄ refined to zero scale. Wolframite-type PbWO₄ and Pb₃O₄ models relied on overlap or predicted strong absent peaks and were rejected. Optional size, strain, texture, axial, and envelope terms were retained only when they gave stable full-range improvement; only massicot microstrain and the reported global terms passed matched removal tests.

## Remaining uncertainty

Weak but coherent residual maxima remain near 25.907, 26.776, 27.950, 30.178, 31.036, 33.524, 46.369, 48.444, and 54.747° 2θ. Tested Pb₃WO₆-related cells either improved essentially one angular region while worsening most of the pattern, had implausible contacts/split sites, or required over-flexible low symmetry. No candidate simultaneously passed geometry, absent-peak, and multi-region full-pattern tests. This component therefore cannot be assigned an atomistic structure or reliable fraction from these data and is intentionally omitted from the normalized phase fractions.
