# Powder XRD phase analysis

The 700 °C ZnO + WO3 reaction product is a three-phase crystalline mixture. The
reported fractions are normalized over the modeled crystalline phases:

| Phase | Space group | Weight fraction | Refined cell (A, degrees) |
|---|---:|---:|---|
| ZnWO4, wolframite | P2/c | 0.74890 (74.89 wt%) | a=4.70480, b=5.73157, c=4.94246, beta=90.59868 |
| WO3, monoclinic | P21/c | 0.18706 (18.71 wt%) | a=7.30554, b=7.54308, c=10.52855, beta=133.01699 |
| ZnO, wurtzite | P63mc | 0.06404 (6.40 wt%) | a=3.25699, c=5.22392 |

The final full-grid fit has Rwp = 3.6863%, chi-square = 21947.11 and goodness of
fit = 1.6303 for 8301 observations and 44 refined parameters, using counting
weights `1/max(counts,1)`.

## Evidence and model selection

The dominant peaks at approximately 18.99, 23.9/24.6, 30.5/30.8, 36.4 and
38.4 degrees 2theta form the wolframite ZnWO4 fingerprint. No exact ZnWO4 CIF
was available, so two fractional-solid-solution wolframite parents were
converted to pure ZnWO4; both converged toward the same P2/c model. A [100]
March-Dollase term was independently selected from five axes (Rwp 22.29% versus
25.91-28.65% for the alternatives).

The positive residual family near 23.2, 26.7, 28.7-29.0 and 33.4-35.8 degrees
is explained by residual monoclinic WO3. Nine exact-WO3 structures were screened
with common nuisance settings. P21/c COD 2311041 gave a stable contribution and
sound geometry. The close P-1 metric candidate gave a slightly lower
over-flexible Rwp but developed impossible short contacts, so it was rejected.
Wurtzite ZnO then lowered Rwp from 8.21% to 6.57%; rocksalt and zincblende scales
collapsed below 0.2 wt%.

Refinement was staged through scale/background, shift and cells, limited
coordinates, isotropic profiles, and one supported anisotropic term. The final
model uses [001] uniaxial microstrain only for WO3. A surface-roughness trial was
rolled back because it hit a boundary and was nearly singular. No Pawley or Le
Bail intensities are used. After three-phase closure, residuals alternate around
existing peaks rather than forming another coherent positive peak family.

## Remaining uncertainty and validation

The ZnWO4 topology and the presence of both precursor phases are well supported.
The exact low-symmetry oxygen distortion in WO3 is less uniquely determined by
this powder pattern; its oxygen coordinates were therefore kept at the selected
published P21/c model. One W site was fixed at its published position and only
the other W site was fitted; this removed the strong two-site coordinate
correlations at a small Rwp cost. [010] was a close second to [001] in the WO3
strain-axis screen. The ZnO internal coordinate was also kept at its published value.
Thus the CIFs are suitable phase models, but fine WO3 positional details should
not be interpreted as a unique single-crystal solution.

Fraction digits are retained for reproducibility, not as absolute accuracy.
They exclude amorphous material, which cannot be quantified without an internal
standard, and model/profile systematics dominate the last digits. No additional
crystalline phase fraction can be determined reliably from the remaining
residuals, so none is claimed.

Independent read-only replay of `final.gpx` regenerated Rwp = 3.6863% with no
profile review flags and exactly the reported fractions. The submitted CIFs
match the replayed project models. All sites have unit occupancy; the shortest
cation-O distances are 1.819 A (ZnWO4), 1.732 A (WO3), and 1.979 A (ZnO), with
no hard-contact or close O-O flags.
