# PXRD phase analysis

The 500 °C product from PbO and WO3 is modeled as nine crystalline Pb-W-O/Pb-O/W-O phases. Fractions below are normalized to the modeled crystalline material only; no amorphous fraction was measured.

| Phase | Model | Crystalline wt% | Confidence |
|---|---|---:|---|
| PbWO4, stolzite | I41/a, COD 9009811 | 54.52 ± 0.23 | high |
| Pb2WO5 | C2/m Pb2MoO5 prototype, Mo6+ → W6+ | 11.48 ± 0.16 | moderate |
| Pb3WO6 | Pnam Pb3UO6 prototype, U6+ → W6+ | 2.23 ± 0.19 | tentative |
| PbO, massicot | Pbcm, COD 2310433 | 5.75 ± 0.15 | high |
| PbO, litharge | P4/nmm, COD 9012700 | 5.91 ± 0.20 | moderate |
| WO3, monoclinic | P21/c, COD 2311041 | 9.41 ± 0.17 | high |
| Pb2O3, monoclinic | geometry-constrained COD 2311012 variant | 7.44 ± 0.23 | tentative structure; required phase contribution |
| PbO2, orthorhombic | Pbcn, COD 1531016 | 1.08 ± 0.11 | tentative |
| Pb3O4, minium | P42/mbc, COD 9012124 | 2.17 ± 0.19 | tentative |

The ± values are one-standard-uncertainty covariance estimates in percentage points. They exclude phase-model, peak-overlap, background, texture, and instrument-profile systematics and are therefore substantially more precise than the defensible absolute accuracy, especially for the tentative phases.

## Evidence and model selection

Stolzite accounts for the dominant peak families. The two PbO polymorphs and residual WO3 account for distinct residual families expected from incompletely reacted PbO/WO3 precursors. Pb2WO5 had no exact screened entry, so isovalent Pb2MoO5 and Pb2CrO5-type parents were tested before cell refinement; the Mo6+ → W6+ model gave the better fit and physical W-O/Pb-O geometry. Pb3WO6 is an isovalent U6+ → W6+ prototype assignment and is correspondingly less certain.

Refitted leave-one-phase-out tests retained all four weakest assignments. Relative to final Rwp = 10.579%, omission raised Rwp to 10.672% for Pb3WO6, remained above 11.78% for Pb2O3 while the reduced model searched another basin, reached 10.645% for orthorhombic PbO2, and reached 10.755% for minium. Thus these components improve coherent full-pattern intensity rather than only a single peak, but PbO2 and Pb3O4 remain tentative because they are low-abundance and strongly overlapped.

The deposited Pb2O3 record has nonphysical 1.33 Å Pb-O and 1.72 Å O-O contacts. Both Pb sites were retained and only O1 was geometry-constrained. Two physical O1 variants produced nearly indistinguishable fixed-profile fits; the submitted variant was marginally better and has minimum Pb-O, Pb-Pb, and O-O distances of about 2.02, 3.28, and 2.29 Å after cell refinement. Its released cell showed a nearly flat, oscillatory a/c tradeoff, so the final project fixes the cell at the converged midpoint while retaining its scale and isotropic strain. Consequently, a Pb2O3-like diffraction contribution is strongly required, but its O1 position, detailed structure, cell precision, and 7.44 wt% fraction cannot be determined reliably to the quoted covariance precision from this powder pattern alone.

The exported models are fully occupied and passed a periodic-distance audit. Rechallenged watch-list phases—raspite PbWO4, Pb2O, rutile PbO2, orthorhombic Pb3O4, Pb7W8O28.8, and two Pb5WO8 analogues—each collapsed to the zero-scale bound under the final common profile. The alternative Pb2WO5 parent was also inferior. These results reject those records, not every possible disordered or unreported Pb-W-O structure.

## Refinement and remaining uncertainty

The full 10.009-99.994° 2θ range was refined with the reported Cu Kα1/Kα2 doublet, a smooth six-term Chebyshev-1 background, one specimen-shift correction, and a common nonnegative W/X profile. U and V were fixed at zero; a released U trial refined significantly negative and was rejected. SH/L was estimated and then fixed because of its strong correlation with specimen displacement. Crystallite-size trials were unsupported or reached bounds. A tetragonal uniaxial-width challenge for stolzite required negative equatorial broadening when unconstrained; the admissible boundary model retained only a positive [001] component (2662, screened at about 2664 ± 340) and improved the high-angle family widths. It was fixed after replay. Replay-stable isotropic strain terms were retained for massicot, litharge, WO3, Pb2O3, and minium; the massicot term was retained because its independent trial was positive and removing it worsened χ² and replay stability. Preferred-orientation trials and unused roughness, extinction, generalized strain, and size terms were rejected or neutralized.

The saved/reopened final project converged with maximum shift/s.u. = 0.003. Fit statistics are Rwp = 10.579%, Rp = 8.113%, Rexp = 3.492%, and goodness of fit = 3.030 for 8,282 observations and 46 refined parameters. The elevated goodness of fit and visible residual structure indicate remaining model/instrument systematics; pointwise experimental uncertainties were unavailable, so Poisson counting weights were used.

The Pb2WO5 and Pb3WO6 atomic arrangements are prototype-based rather than independently solved, and their exact structures are not reliable. The Pb2O3, PbO2, and Pb3O4 fractions are semi-quantitative because of structural ambiguity and overlap. No conclusion about amorphous content can be drawn. `final.gpx`, the exported CIFs, `fit.csv`, and `result.json` all derive from the same final project state.
