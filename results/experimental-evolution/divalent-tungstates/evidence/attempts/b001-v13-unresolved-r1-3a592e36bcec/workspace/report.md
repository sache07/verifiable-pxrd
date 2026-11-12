# Crystalline phase analysis

The pattern is described by four crystalline phases. Weight fractions are normalized over these modeled crystalline phases.

| Phase | Structure | Weight fraction | Formal GSAS-II e.s.d. |
|---|---|---:|---:|
| PbWO4 | scheelite, `I 41/a` | 0.58203 (58.20 wt%) | 0.00145 |
| WO3 | monoclinic, `P 21/c` | 0.20048 (20.05 wt%) | 0.00095 |
| Pb3O4 | minium, `P 42/m b c` | 0.17298 (17.30 wt%) | 0.00132 |
| PbO | massicot, `P b c m` | 0.04450 (4.45 wt%) | 0.00092 |

This inventory is chemically consistent with the metadata: PbWO4 is the reaction product from WO3 and Pb3O4 at 500 °C, while monoclinic WO3 and Pb3O4 remain as unreacted precursor phases and massicot PbO is a minor lead-oxide phase.

## Evidence and model selection

The final Cu Kα1/Kα2 Rietveld replay used the full measured range, 9.9034–100.0946° 2θ. It converged without frozen or dropped variables at `Rwp = 3.2699%`, `Rp = 2.4554%`, and goodness of fit `1.3192` (8301 observations, 44 variables). Refined terms were phase scales and cells, a smooth 18-term Chebyshev background, zero shift, polarization, W/X profile terms, and the supported size/texture terms. Atomic coordinates and occupancies were retained from the cited source records.

All retained and competing CIFs were screened with `learned/cif_health.py` before fitting, and all four exported CIFs pass the final geometry/occupancy check. Structurally distinct exact-formula records were compared rather than co-added. In the rebuilt four-phase basis:

- The retained PbWO4 record returned to `Rwp = 3.271%` when seeded from the competing nuisance/topology basin; the competing scheelite record converged at `Rwp = 4.29%`. Its apparent PbWO4 anisotropy and texture converged essentially neutral and were pruned.
- Alternative WO3 records gave `Rwp >= 3.73%` or required bound/singular width terms. The retained monoclinic record remained preferred.
- The tested orthorhombic Pb3O4 alternative gave `Rwp = 6.54%` with bound parameters, versus the retained tetragonal minium model.
- PbO is replay-stable with positive scale and several independent families, including massicot 200 near 30.79°, 220 near 45.59°, and 202 near 49.64° 2θ. A three-phase model leaves coherent residuals and was about `Rwp = 4.70%`. The structurally distinct PbO supercell was tested over every symmetry-inequivalent simple low-index size and March-Dollase axis; its best valid combined branch reached only `Rwp = 3.297%` and required a substantial long-axis contraction. The tetragonal PbO record collapsed to effectively zero scale in its valid scale gate; a later setting-import branch was invalid and was not used for ranking. Massicot therefore wins the physical-record comparison; the alternatives do not coexist in the submitted model.

Complete low-index axis surveys included unequal-index and sign-distinct directions where symmetry required them. Low-seed collective width/strain releases were also replayed. Strain branches collapsed, bound, or dropped parameters, so all microstrain terms were restored to zero. The accepted model retains isotropic PbWO4 size broadening, uniaxial size broadening for Pb3O4 and PbO, and one supported PbO March-Dollase term. WO3 size is fixed at the inactive 10 µm value; all other inactive sizes, textures, strain, and roughness terms are literal neutral values. Background orders from 6 through 20, polarization, asymmetry, and roughness were challenged; 18 coefficients were selected at the improvement elbow, asymmetry was retained, and roughness was rejected.

## Remaining uncertainty

The tabulated e.s.d.s are covariance estimates and do not include source, background, preferred-orientation, or line-broadening model uncertainty. Across acceptable profile/background variants, major-phase fractions moved by roughly 0.1–0.4 weight-percentage point and PbO by about 0.1–0.2 point; those spreads are more realistic than the last quoted digits. PbO is securely detected, but its fraction is the most sensitive to texture and anisotropic broadening.

The fractions are normalized only over the modeled crystalline phases. Without an internal standard, amorphous material and absolute crystalline content cannot be determined. The CIFs are refined powder-fit models with database atomic coordinates, not independent unconstrained structure determinations. No additional phase met the required positive-scale, multi-family, replay-stability gate.

The submitted `final.gpx`, CIF files, `fit.csv`, and `result.json` were all generated from the same reopened full-range project.
