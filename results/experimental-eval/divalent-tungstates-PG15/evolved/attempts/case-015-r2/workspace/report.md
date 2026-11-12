# Crystalline phase analysis

## Result

The 900 °C product is a three-phase crystalline mixture dominated by wolframite ZnWO4, with unreacted WO3 and ZnO. Fractions are normalized over the modeled crystalline phases; parenthesized values are formal one-standard-uncertainty values from the least-squares covariance matrix.

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| ZnWO4 | wolframite, P 2/c | 74.14(12)% |
| WO3 | triclinic, P -1 | 18.38(10)% |
| ZnO | wurtzite, P 63mc | 7.48(10)% |

For the full 9.9034–100.0949° 2theta range, the final refinement has Rp = 4.736%, Rwp = 6.011%, Rexp = 3.792%, and goodness of fit = 1.588 (8,301 observations and 28 refined variables). Poisson weights, 1/count, were used because pointwise uncertainties were not supplied.

## Evidence and model selection

The dominant P 2/c ZnWO4 model accounts coherently for the strong families near 15.5, 19.0, 23.9, 24.6, 30.7, 36.5, 38.5, 41.4, and 48.9° 2theta. WO3 is required by residual families including those near 23.17, 33.35, and 34.30°. Weak wurtzite ZnO was retained because a positive, replay-stable scale accounts for a coherent set near 31.9, 34.4, 56.7, and 62.9°, including peaks that are unique or only partly overlapped. Removing it leaves those residuals. This inventory is also chemically consistent with the stated WO3 and ZnO precursors.

Exact-composition database records were available, so cross-chemistry substitution was not needed. The starting records were COD 1520641 (ZnWO4), 2106293 (WO3), and 9004178 (ZnO). Monoclinic P21/n and triclinic P-1 WO3 records were compared under the same nuisance model. The triclinic model reduced Rwp from about 6.24% to 5.94% on the common 10–100° comparison range. A second P21/n/neutron record fitted poorly (about 12.3%) and drove nuisance terms to unphysical behavior. The monoclinic/triclinic choice changes any fraction by less than 0.3 weight-percentage point.

The accepted baseline uses the reported Cu Kalpha1/Kalpha2 doublet and fixed 0.5 intensity ratio, a six-coefficient smooth Chebyshev background, one refined zero correction, positive common W/X broadening, axial asymmetry, and a physical surface-roughness correction. Only WO3 required replay-stable isotropic microstrain (about 2,637 microstrain). Phase-size terms, preferred orientation along several symmetry-distinct axes, extinction, extra polarization freedom, and anisotropic WO3 strain were unsupported, correlated, bound-seeking, or unstable and were removed. A specimen-displacement alternative was marginally worse, and freeing U drove it negative, so both were rejected. The final background remains smooth and nonnegative, and isolated low-, middle-, and high-angle families have consistent positions, widths, and asymmetry.

Atomic coordinates and occupancies were kept from the source records; only unit cells were refined because this powder pattern does not justify unconstrained coordinate refinement. The exported structures retain full occupancies and plausible geometry: ZnWO4 has W–O = 1.795–2.139 Å and Zn–O = 2.024–2.224 Å, triclinic WO3 has W–O = 1.716–2.221 Å, and ZnO has Zn–O = 1.977–1.992 Å.

## Remaining uncertainty

The presence and approximate amount of all three phases are reliable within this crystalline model, but the exact WO3 symmetry is not fully resolved: its triclinic distortions are small and its reflections are broadened and overlapped, so P -1 is the better-fitting model rather than an unambiguous symmetry determination. The formal fraction uncertainties are lower bounds because they omit database-model choice, roughness/scale correlation, microabsorption, and sample-preparation effects. No internal standard was provided, so amorphous material and therefore absolute whole-sample phase fractions cannot be determined; the reported fractions apply only to the modeled crystalline material. Very weak additional crystalline phases below the residual sensitivity cannot be excluded.

`final.gpx`, the three CIF files, `fit.csv`, and `result.json` were generated from the same final save/reopen refinement. The replay converged without singularities, with maximum final shift/s.u. = 0.042, and numerical checks confirmed exact agreement between the project arrays, exported profile, fit statistics, and normalized fractions.
