# Powder X-ray diffraction analysis

## Result

The crystalline pattern is explained by two residual precursor phases: monoclinic WO3 (76.07 wt%) and spinel Co3O4 (23.93 wt%), normalized over the modeled crystalline material. Their covariance-only 1-sigma fraction uncertainty is 0.20 percentage point. A more realistic uncertainty is about 1–2 wt% because source-model, background, profile, absorption and microstructural systematics are not represented by that covariance estimate.

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| WO3 | P 21/c | a=7.30618, b=7.53713, c=10.54637, beta=133.15369 | 0.760717 |
| Co3O4 | F d -3 m | a=8.08443 | 0.239283 |

The independently regenerated full-range fit gives Rwp=3.358%, Rp=2.441% and goodness of fit=1.953 for 8301 points and 26 refined parameters. The replay recalculated atomic structure factors and reflection lists from `final.gpx`, used no optimization, left the project unchanged, and raised no physical profile-review flags.

## Evidence and model selection

WO3 is required by the resolved 23.46/23.95/24.71 degree triplet and its repeated higher-angle families. Co3O4 is independently required by coherent peaks near 19.37, 31.63, 37.20, 38.90, 45.15, 59.67 and 65.55 degrees. The selected starting structures were COD 2311041 (WO3, P 21/c) and COD 9005896 (Co3O4, F d -3 m); both final CIFs pass the geometry/occupancy screen. Alternate P 21/c and Pnma WO3 records fit worse. A triclinic WO3 record gave a slightly lower early-stage residual but required large source-cell angle distortions toward a monoclinic metric, so it was rejected as a lower-symmetry overfit. A malformed WO3 record and a physically defective alternate Co3O4 record were also rejected.

A diagnostic wolframite CoWO4 model (W substituted into a complete CoMoO4 prototype because the exact local CoWO4 record was incomplete) and rocksalt CoO were each challenged under the same common profile. Both scales collapsed to the nonnegative floor (modeled fractions below 2e-14), and neither has coherent unique residual families. They are therefore not reported as phases; trace quantities below this pattern's practical detection capability cannot be excluded.

## Refinement scope and uncertainty

The physically retained nuisance model uses a six-term smooth background, phase scales and cells, one specimen-displacement correction (-643.8 micrometres in the GSAS-II convention), a common nonnegative peak profile, isotropic phase size, uniaxial [010] WO3 microstrain, isotropic Co3O4 microstrain, and polarization. Surface roughness, preferred orientation, extra asymmetry and unsupported anisotropy were tested and pruned. The final accepted parameter set remained converged through two save/reopen replays (maximum shift/sigma below 0.006).

WO3 tungsten coordinates, its common isotropic displacement parameter, and the spinel oxygen coordinate were replay-stable and retained. Refining all WO3 oxygen coordinates produced alternating solutions (maximum shifts up to about 4.8 sigma), so those oxygen positions cannot be determined reliably from this powder pattern and remain at the source-model values. This limitation has little effect on the phase identities but is relevant if the CIF is used for detailed WO6 bond geometry. Amorphous content, if present, is not quantified because no internal standard was measured.
