# Powder XRD phase analysis

## Result

The crystalline model contains three phases. Fractions are normalized over these modeled crystalline phases.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---:|---|---:|
| monoclinic WO3 | P 21/c | a=7.30638, b=7.53834, c=10.54406, beta=133.14660 | 0.56294 (56.29 wt%) |
| calcite CaCO3 | R -3 c | a=4.98887, c=17.06819 | 0.31821 (31.82 wt%) |
| scheelite CaWO4 | I 41/a | a=5.24378, c=11.37869 | 0.11885 (11.88 wt%) |

The covariance-only standard uncertainties are 0.16, 0.20, and 0.10 percentage point, respectively. They do not include model-choice uncertainty; physically acceptable fixed-Uiso and texture trials indicate a more realistic systematic uncertainty of roughly one percentage point (absolute) for the major-phase fractions.

## Evidence and refinement

The precursor context (CaCO3 + WO3 heated at 500 °C) is consistent with partial formation of CaWO4 and residual starting materials. Monoclinic WO3 is identified by its resolved 23.42/23.90/24.66° triplet and associated 33.56–34.46° and higher-angle families. Calcite has independent support at 29.71, 39.71, and 43.46°. Scheelite CaWO4 is supported by the 29.02, 31.73, 49.38, and 54.58° families. Low-, middle-, and high-angle isolated lines show no remaining common position or width trend in the final profile.

Room-temperature COD records 2311041 (WO3), 1547347 (calcite), and 7219229 (CaWO4) supplied the screened parent atom models. Their cells, scales, and supported profile terms were refined in GSAS-II against the complete 9.9904–100.0950° Cu K-alpha doublet scan. The final native replay gives Rwp=7.36261%, Rp=5.44232%, chi-square=78419.98, and GOF=3.08067 for 8293 points and 30 refined variables. The replayed background is smooth and positive (338–3564 counts), and GSAS-II reported no negative-width, negative-background, or other profile-review flags.

The physically retained nuisance model uses one specimen displacement (-560.6 micrometres), W=13.876 with nonnegative fixed U=0 and X=0.1, fixed SH/L=0.03, and refined polarization 0.7411. Supported phase terms were WO3 size plus [010] uniaxial strain, calcite isotropic strain and [001] March-Dollase texture, and scheelite isotropic strain plus [111] texture. Roughness, an additional zero correction, calcite/scheelite strain anisotropy, and other texture axes were rejected by replayed comparisons or parameter correlation.

Alternative WO3 records were challenged under the same nuisance model. A triclinic model gave Rwp about 9.66% and drove width/size terms to unphysical limits; another P 21/c record had the wrong 23–25° intensity distribution and a 1.575 Å O–O contact. A CaO watch-list trial refined to only about 0.08 wt% (approximately 2.3 sigma), with inconsistent residual signs across its reflection family and negligible Rwp improvement, so CaO is not identified or quantified reliably and is omitted.

## Remaining uncertainty

Unconstrained atomic-coordinate and displacement refinements moved WO3/CaWO4 oxygen sites beyond the stated physical reference-mismatch range and pushed common Uiso above 0.020 Å². Those overfit terms were rejected. The one robust coordinate response was the WO3 W sublattice: its direction gave a large, replay-stable improvement and was projected to an interior 0.0382 Å RMS displacement (below the 0.04 Å physical limit), then fixed. Oxygen, calcite, and scheelite coordinates remain at their screened parents. The submitted CIFs use refined cells and fixed physically plausible common Uiso values (0.008, 0.019, and 0.010 Å² for WO3, CaCO3, and CaWO4). Detailed oxygen shifts and ADPs cannot be determined reliably from this pattern. The scheelite coherent-domain size also reached the 0.04 micrometre lower physical limit and was fixed there; that size value is not independently reliable.

`fit.csv` is generated from a fresh native replay of `final.gpx`, rather than copied from cached refinement arrays. The submitted CIFs are byte-identical to the replay exports from the saved project.
