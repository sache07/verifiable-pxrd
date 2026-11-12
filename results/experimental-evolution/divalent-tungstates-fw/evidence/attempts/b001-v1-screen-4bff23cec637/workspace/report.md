# Powder XRD phase analysis

## Result

The crystalline model contains three Ca–W–O phases. Fractions are normalized over those modeled crystalline phases:

| Phase | Structure model | Weight fraction |
|---|---|---:|
| Scheelite CaWO4 | I4_1/a, COD 7219229 parent | 71.27% |
| Monoclinic WO3 | P2_1/c, COD 2311041 parent | 16.06% |
| Ca3WO6 | P2_1/c ordered-perovskite analogue derived from Sr2MnWO6 (COD 1532958; Sr and Mn mapped to distinct Ca sites) | 12.68% |

The final whole-pattern fit has Rwp = 4.758%, Rp = 3.558%, Rexp = 2.612%, and goodness of fit = 1.822. All three submitted CIFs pass the supplied geometry/occupancy screen. An independent no-refinement GSAS-II replay reproduced the phase fractions exactly and Rwp = 4.757834%, with no profile-review flags; each exported CIF also matches its replayed project phase numerically.

## Evidence and model selection

The dominant scheelite family includes 18.50, 28.57, 31.32, 34.03 and 46.96 degrees 2theta. A second family at 23.02/23.45/24.27, 26.51, 28.89 and 33.15 degrees identifies monoclinic WO3. With those two phases fitted, a coherent residual family remained at about 18.76, 19.35, 22.04, 30.65, 31.45, 32.11, 36.54/37.44, 45.14, 50.84 and 56.85 degrees. Ordered A2BWO6 frameworks were therefore tested after mapping all non-W cation sites to Ca. The low-symmetry Ca3WO6 model accounts for that full family; deleting Ca3WO6 raises Rwp from 4.76% to 10.97%. Deleting WO3 or CaWO4 raises it to 15.57% or 47.12%, respectively.

All serious CIF candidates were normalized before refinement and screened physically. Fixed-coordinate comparisons selected scheelite over high-pressure fergusonite CaWO4 (about 13.5% versus 46.3% Rwp in the two-phase comparison). For WO3, monoclinic and triclinic passing sources were nearly tied; the selected higher-symmetry room-temperature neutron model was preferred. A nominally slightly better old monoclinic source was rejected because the supplied screen flags 1.575 A O–O contacts. For Ca3WO6, the selected P2_1/c Sr2MnWO6-derived parent gave 9.23% Rwp in the common fixed-coordinate three-phase test, compared with 9.26% for the Sr2Fe parent, 9.35% for Pnma, 12.18% for the high-symmetry control, and zero support for the tetragonal control.

The retained nuisance terms are a one-parameter Suortti roughness correction, [001] March–Dollase texture and isotropic size broadening for WO3, and a shift-only specimen-displacement term. Each survived 6/8/10-term background restarts. Simultaneous zero plus displacement (>99.8% correlation), refined U or SH/L terms, simultaneous size plus strain, a second roughness parameter, and refined polarization were rejected as bounded, redundant, or strongly correlated. CaO and triclinic-WO3 additions refined to zero; Ca–W bronze and fergusonite additions stayed below 0.1 wt% with negligible fit change.

Coordinates were refined last and selectively. Only the scheelite O site and the analogue-derived Ca site in Ca3WO6 were retained; both improvements reproduced across background branches and the resulting structures pass. WO3 coordinates remain at the published parent because their improvements were weak/unstable. Unrestrained Ca3WO6 oxygen refinement produced impossible 0.50–0.60 A contacts and was rejected; those O sites remain at the defensible parent framework.

## Uncertainty

Formal covariance-only fraction standard uncertainties are 0.08, 0.06, and 0.06 percentage points, but they exclude source/model systematics. The 6-, 8- and 10-background branches changed each fraction by less than 0.03 percentage point. A conservative interpretation is about +/-1 percentage point absolute for each fraction. Ca3WO6 is securely required as a phase, but its exact light-atom coordinates are not reliably determined by this Cu X-ray pattern; the submitted oxygen sublattice is therefore the physically passing parent analogue rather than an unstable apparent optimum.
