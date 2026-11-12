# Powder XRD phase analysis

## Result

The crystalline pattern is modeled with three phases:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| ZnWO4, wolframite | P2/c | 0.81750 (81.75 wt%) |
| WO3, monoclinic | P2_1/c | 0.13154 (13.15 wt%) |
| ZnO, wurtzite | P6_3mc | 0.05096 (5.10 wt%) |

Fractions are `HAP scale × unit-cell mass`, normalized over the three modeled
crystalline phases. Scale-covariance-only standard uncertainties are about
0.19, 0.11, and 0.18 wt%, respectively, but these omit model selection,
texture, and profile systematics; uncertainties of roughly 1–2 wt% are more
realistic, especially for ZnO.

The independently regenerated full-grid profile has Rwp = 9.299%, Rp =
5.158%, Rexp = 2.646%, and goodness of fit = 3.522 for 8,301 points and 37
refined parameters. The replay recalculated all structure factors from
`final.gpx`, optimized no parameters, left the project unchanged, and produced
no physical-profile review flags.

## Evidence

The dominant families at approximately 15.78, 19.2, 24.1/24.8, 31.0, 36.7,
and 41.6 degrees 2-theta select the wolframite ZnWO4 topology. A CoMoO4
wolframite parent was transformed by Co→Zn and Mo→W, then its cell and limited
symmetry-allowed coordinates were refined. The final cell is a = 4.70685,
b = 5.73902, c = 4.93803 A, beta = 90.6182 degrees. A March-Dollase [111]
term is strongly supported (ratio 0.714); other tested axes gave much poorer
fits. The submitted structure has no short contacts (minimum W–O 1.890 A,
minimum O–O 2.597 A).

Residual families near 23.4–24.8 and 33–35 degrees require unreacted WO3.
Common-project replacement trials over all available exact-formula WO3
records favored monoclinic COD 2311041 (initial common-setting Rwp 18.86%
versus 20.83–23.07% for the clearly different orthorhombic, tetragonal, and
hexagonal candidates). Its final oblique-setting cell is a = 7.71529,
b = 7.53006, c = 10.54509 A, beta = 136.05495 degrees. A [110]
March-Dollase term was uniquely favored from a common corrected project (Rwp
9.80% without that WO3 texture and 9.43% with it). Sequential W-coordinate
changes were stable; oxygen-coordinate trials moved individual O sites by
0.3–0.9 A, oscillated, or became correlated, so those unphysical refinements
were rolled back. The submitted WO3 has minimum W–O 1.683 A and minimum O–O
2.540 A.

Narrow contributions near 32.0, 34.9, 36.7, 47.9, and 63.4 degrees identify
wurtzite ZnO. Its corrected cell, a = 3.25653 and c = 5.18875 A, escaped an
earlier false local minimum and lowered Rwp by about 0.42 percentage point.
An isotropic microstrain of 7,396(559) ppm is supported and lowers Rwp by a
further 0.13 point. Uniaxial variants hit the 8,000 ppm limit and were rejected.
Crystallite size is not independently determined because refining it with
microstrain gave a 0.946 correlation; it remains fixed at 0.5 micrometre. The
submitted ZnO has minimum Zn–O 1.977 A and minimum O–O 3.204 A.

Phase closure included charge-balanced Zn3WO6, Zn2WO5, and ZnW2O7 analogue
routes as well as second WO3 polymorphs. Stable off-stoichiometric additions
were below 0.12 wt% with negligible gains. A triclinic WO3 addition stabilized
at only 0.7–1.2 wt%, mainly duplicated the three strongest retained-WO3 lines,
and improved Rwp by only about 0.05 point after eight extra cell/scale degrees
of freedom. It is therefore not asserted as a separate phase; trace triclinic
WO3 at about the 1 wt% level cannot be excluded reliably. Candidate branches
that failed import or diverged remain marked `unknown`, not rejected, in
`candidate_ledger.md`.

## Remaining uncertainty

The largest remaining positive residual is near 41.56 degrees, with
peak-shape residuals also around 31, 36.7, and 54.2 degrees. No screened extra
phase supplied a coherent family that closed these residuals, and adding
profile or coordinate freedom either hit bounds, became strongly correlated,
or produced implausible geometry. Consequently, Rwp remains above the
counting-statistical floor. The three phase identities and the wolframite
topology are reliable, but minor-phase fractions are profile-dependent and a
sub-percent WO3 polymorph cannot be resolved confidently.

The final CIFs have unit occupancies, chemically plausible densities, no
contacts below 0.8 A, and no O–O contacts below the 1.8 A review threshold.
Surface roughness, a separate sample-shift term, ZnO texture, WO3 anisotropic
strain, and unstable oxygen-coordinate refinements were not retained.
