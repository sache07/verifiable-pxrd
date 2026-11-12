# Quantitative phase analysis

The crystalline model contains three phases. Fractions are normalized over these modeled crystalline phases:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| Tungsten(VI) oxide, WO3 | triclinic, P -1 | 0.6054 (60.54 wt%) |
| Calcite, CaCO3 | R -3 c (hexagonal setting) | 0.2727 (27.27 wt%) |
| Scheelite calcium tungstate, CaWO4 | I 41/a | 0.1220 (12.20 wt%) |

The regenerated full-pattern fit has Rwp = 7.611%, Rp = 5.668%, and goodness of fit = 3.184 (8,293 observations and 29 refined variables). The refined sample displacement is about -503 micrometres for the configured 200 mm diffractometer radius. The model also includes effective isotropic coherent-domain terms for CaWO4 (~31 nm) and WO3 (~106 nm), weak surface roughness, and calcite (104) March-Dollase preferred orientation. These size values are model-dependent because no independently calibrated instrumental profile was supplied.

## Evidence for the assignments

The triclinic WO3 model accounts for the resolved 23.42/23.90/24.67 degree triplet and additional reflections near 26.91, 33.57/33.90, and 50.21 degrees 2theta. Scheelite CaWO4 is supported by distinct reflections near 18.90, 31.72, and 45.70 degrees, while calcite is supported by peaks near 29.71, 36.29, 43.46, 47.78, and 48.78 degrees. In matched leave-one-phase-out refinements, removing WO3, CaWO4, or calcite raised Rwp from approximately 7.7% to 48.3%, 14.5%, and 14.3%, respectively, so each phase has multi-peak, full-pattern support.

Candidate structures were checked for composition, occupancies, symmetry expansion, duplicate sites, and short contacts. A tempting alternative WO3 entry was rejected for an implausible 1.575 A O--O contact. Under the mature three-phase nuisance model, the selected triclinic WO3 model gave Rwp = 7.611%, compared with 7.814% for a chemically valid monoclinic alternative; an orthorhombic alternative was substantially worse. Fergusonite CaWO4 and aragonite CaCO3 alternatives did not retain stable positive support. No coherent residual peak family justified a fourth atomistic phase.

## Remaining uncertainty

The stated fractions are crystalline-normalized and do not measure amorphous material. Their formal one-standard-deviation scale-factor uncertainties are approximately 0.19, 0.24, and 0.11 wt% for WO3, calcite, and CaWO4, but these are lower bounds because pointwise experimental uncertainties and an instrumental profile standard were unavailable. The WO3 polymorph assignment is the main structural uncertainty: triclinic P -1 is preferred by complete-pattern comparison, but the monoclinic alternative remains moderately plausible. Replacing it changed individual phase fractions by less than about 0.7 wt% absolute. Atomic coordinates, occupancies, and displacement parameters were retained from audited reference structures; the data support the phase identities and bulk fractions more reliably than independent coordinate refinement.

The final GSAS-II state is in `final.gpx`; `fit.csv` is its regenerated observed/calculated/difference profile. The CIFs were exported directly from that same state.
