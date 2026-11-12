# PXRD phase analysis

The pattern is modeled as three crystalline phases. Weight fractions are normalized only over these modeled crystalline phases.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| WO3 | triclinic P -1 (No. 2) | 0.7146(22) |
| Mn2O3 | cubic Ia-3 (No. 206) | 0.2747(19) |
| MnWO4 | wolframite, P 2/c (No. 13) | 0.0108(13) |

The final fit has Rp = 4.986%, Rwp = 6.829%, and goodness of fit = 2.566 for 8,288 fitted observations and 15 refined variables. The full exported grid gives Rwp = 6.822%. Cu K-alpha1/K-alpha2 wavelengths and the reported 0.5 intensity ratio were used. Because pointwise uncertainties were not supplied, counting uncertainties were estimated from the raw counts.

## Evidence and model selection

The major phases were matched to audited atomistic models COD 2106293 (WO3) and COD 1514230 (Mn2O3). Their refined cells are a = 7.30249, b = 7.53444, c = 7.69097 A, alpha = 89.9792, beta = 90.6677, gamma = 89.9581 degrees for WO3, and a = 9.40989 A for Mn2O3. Removing either major phase produced large whole-pattern deterioration (Rwp approximately 34.6% without WO3 and 10.8% without Mn2O3). Matched replacements with monoclinic P21/c WO3, cubic I213 Mn2O3, or orthorhombic Pbca Mn2O3 were substantially worse (Rwp 9.99%, 7.31%, and 7.07%, respectively).

Weak residual peaks at approximately 15.8, 18.7, 30.3, 30.7, 41.5, 53.8, and 65.2 degrees support a trace wolframite MnWO4 model (COD 1520200). Its removal from the mature model raises Rwp from 6.8291% to 6.8554%. A Mn3WO6 trial gave only a 0.0047 percentage-point Rwp reduction, below the preset material-improvement margin, and its strongest contributions were overlap-dominated rather than uniquely supported; it was therefore rejected.

The selected nuisance model uses a specimen displacement, positive global U/X profile terms, refined polarization, a very small WO3 [001] March-Dollase correction, and isotropic microstrain for Mn2O3 and MnWO4. Matched leave-outs materially worsened the fit. A joint zero/displacement branch was rejected because the two parameters were 99.94% correlated. All submitted CIFs pass composition, occupancy, symmetry, duplicate-site, and contact screening; `final.gpx` passes convergence, profile-regeneration, and positive-total-width audits.

## Remaining uncertainty

The major-phase identities and proportions are robust. The approximately 1 wt% MnWO4 component is less secure quantitatively: its cell and atom coordinates were held to the audited literature model because cell refinement was unstable, and its broadening requires a large, weakly determined microstrain of about 2.08(1.03)%. This term is stable and improves five of six angle regions, but it correlates moderately with the trace scale, so the formal 0.13 wt% fraction e.s.d. understates model-dependent uncertainty. The MnWO4 result should be interpreted as a supported trace phase at roughly 1 wt%, not a high-precision assay.

Atomic coordinates and displacement parameters were not refined. No internal standard was present, so amorphous content cannot be measured and the reported fractions must not be interpreted as absolute bulk mass fractions. Residual autocorrelation and goodness of fit above one indicate remaining systematic profile/structural mismatch, but no additional atomistic phase passed the full-pattern acceptance tests.
