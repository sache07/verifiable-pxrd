# PXRD phase analysis

The submitted two-phase model is **gamma-WO3 (P2_1/c), 71.79 wt%**, and **beta-MnO2/pyrolusite (P4_2/mnm), 28.21 wt%**. Fractions are normalized over modeled crystalline material. The final fit has Rwp = 5.8343%, Rp = 4.2754%, and GOF = 2.1690.

| Phase | Refined cell (A, degrees) | Weight fraction |
|---|---|---:|
| gamma-WO3, P2_1/c | a = 7.69783, b = 7.54065, c = 10.54456, beta = 136.1107; V = 424.332 A3 | 0.71789 |
| beta-MnO2, P4_2/mnm | a = 4.40102, c = 2.87547; V = 55.6949 A3 | 0.28211 |

The WO3 cell is an equivalent transformed P2_1/c setting rather than the commonly tabulated near-orthogonal setting. Both exported CIFs pass composition, occupancy, symmetry-expansion, duplicate-site, and contact screening.

## Evidence and refinement

The dense low-symmetry WO3 peak family, including the split cluster near 23-25 degrees 2theta and its higher-angle sequence, is reproduced by an atomistic gamma-WO3 model (COD 2311041). One W-site coordinate was supported by a matched full-pattern test; removing that adjustment increased Rwp from 5.834% to 5.930%. Oxygen coordinates and displacement parameters were kept at source values because their refinements were unstable or disproportionately large for laboratory X-ray data.

The second phase is required by multiple rutile-MnO2 reflections, notably near 28.99, 37.65, 41.31, 56.95, and 59.65 degrees 2theta. Removing MnO2 from the mature model increased Rwp to 11.526%. A small [001] March-Dollase term was retained (ratio about 1.12); the near-tied [110] description changes the MnO2 fraction by roughly 0.4 wt%.

The final profile uses the supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, a refined zero offset, global W and Y width terms, an effective polarization of 0.749, and an isotropic WO3 coherent-domain size of about 0.100 micrometre. Negative, boundary-limited, or strongly correlated U/V/X/Z, roughness, axial-divergence, and phase-strain branches were rejected. Removing polarization, Y, or WO3 size increased Rwp to 5.862%, 6.488%, and 6.756%, respectively. The regenerated profile in `fit.csv` agrees exactly with `final.gpx`.

## Alternatives and uncertainty

A triclinic P-1 WO3 model is genuinely near-tied. After identical profile treatment and one W-site refinement it reached Rwp = 5.8321%, only 0.0022 percentage point below the selected model, while requiring two additional cell degrees of freedom and twice as many independent atomic sites; its refined metric also became nearly monoclinic. P2_1/c is therefore selected as the smaller interpretable model, but the WO3 symmetry is not uniquely established by this powder pattern alone.

Mn2O3, Mn3O4, Mn3WO6, MnWO4, alpha-MnO2, and mixed Mn-W oxide candidates were retested from the mature baseline. None passed the required multi-peak test. In particular, a nominal 1.1 wt% Mn2O3 scale mainly improved the residual near 33.27 degrees and overlaps near 55.50 degrees while predicting strong unsupported peaks near 38.55, 66.10, and 82.15 degrees; it was not included. Thus any trace third component cannot be identified or quantified reliably.

The least-squares fraction uncertainty is about 0.15 wt% per phase, but it excludes model choice, form-factor, texture, and uncalibrated-profile effects. A more realistic absolute uncertainty is approximately 2 wt% per phase. The fractions do not measure amorphous content because no internal standard was supplied.
