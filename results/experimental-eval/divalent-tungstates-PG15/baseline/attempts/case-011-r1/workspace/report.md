# PXRD phase analysis

## Result

The crystalline pattern is explained by two phases:

| Phase | Structure | Crystalline weight fraction |
|---|---|---:|
| Monoclinic γ-WO₃ | `P 21/c` (No. 14), alternate cell setting; COD 2311041 | 0.7100 (formal s.u. 0.0018) |
| β-MnO₂ (pyrolusite) | `P 42/m n m` (No. 136); COD 1514110 | 0.2900 (formal s.u. 0.0018) |

These fractions are normalized only over the modeled crystalline phases. A realistic statement, allowing for profile-model and uncalibrated-instrument systematics, is approximately **71(2) wt% WO₃ and 29(2) wt% β-MnO₂**. They do not quantify amorphous material or the total bulk composition.

The final 8301-point GSAS-II refinement over 9.903–100.095° 2θ gives `Rwp = 6.105%`, `Rp = 4.441%`, `Rexp = 2.693%`, and goodness of fit `2.270`. Because point uncertainties were not supplied, the raw counts were fitted with the GSAS-II Poisson approximation (`w = 1/I`).

## Evidence

Monoclinic WO₃ accounts for the diagnostic 23.443/23.932/24.693° triplet and the associated groups at 26.931°, 33.59–34.48°, 42.19°, and 50.22°. β-MnO₂ is required independently by its 37.667°, 43.122°, 56.955°, 59.661°, and approximately 72.53° reflections. Together the two structures account for all reproducible peak families; the remaining largest residuals sit on already modeled intense peaks rather than forming another phase's line series.

Chemically allowed MnWO₄ and Mn₃WO₆ candidates were tested and rejected. In particular, MnWO₄ requires an intense 30–31° doublet that is absent. Alternative WO₃ polymorph/coordinate models also fit substantially worse under the same screening recipe (about 8.1% `Rwp` for the next monoclinic model and at least 15% for the tested orthorhombic/triclinic alternatives, before the final profile refinements). The result therefore indicates largely unreacted crystalline precursor oxides after the reported 300 °C treatment, with no resolved crystalline manganese tungstate.

The final model refined the phase scales, unit cells, a 12-term Chebyshev background, Bragg–Brentano specimen-height correction, effective polarization, and isotropic size/microstrain broadening. Wavelengths and the reported Kα₂/Kα₁ ratio were fixed to the metadata values. Preferred orientation refined to unity and was omitted; axial-divergence/specimen-height and atomic-coordinate trials were unstable or strongly correlated and were rejected.

## Uncertainty and limits

The atomic coordinates cannot be determined reliably from this broadened, overlapping two-phase powder pattern. They are retained from the cited COD structures; only the cells were refined. The WO₃ CIF uses a valid non-conventional `P 21/c` cell (`a = 7.69145 Å`, `b = 7.53452 Å`, `c = 10.53619 Å`, `β = 136.1125°`) equivalent to the usual monoclinic γ-WO₃ description. Refined β-MnO₂ has `a = 4.39775 Å` and `c = 2.87287 Å`.

The formal fraction errors are conditional least-squares values and are too optimistic. No calibrated instrumental profile, calibrant, pointwise uncertainties, particle-size distribution, or microabsorption correction was available; the large W/Mn absorption contrast can bias quantitative phase analysis. The low Durbin–Watson statistic (0.425) also reflects serially correlated profile mismatch around strong peaks. Thus the crystalline two-phase assignment is secure, but fractions should be treated as accurate to a few absolute weight percent, and amorphous content cannot be determined from this refinement.

Submitted structures are in `phase_WO3.cif` and `phase_beta_MnO2.cif`; `fit.csv` and `result.json` were exported directly from `final.gpx`.
