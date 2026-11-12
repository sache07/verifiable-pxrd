# Powder XRD phase analysis

## Result

The pattern is described by two crystalline phases:

| Phase | Structural model | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| Monoclinic WO3 | COD 2311041, P 21/c | a = 7.69443 A, b = 7.53798 A, c = 10.54705 A, beta = 136.1613 deg | 0.72029(27), or 72.03(27) wt% |
| Bixbyite Mn2O3 | COD 1514230, Ia-3 | a = 9.41460 A | 0.27971(27), or 27.97(27) wt% |

Fractions are normalized over these modeled crystalline phases. No internal
standard was supplied, so an amorphous fraction or absolute crystalline yield
cannot be determined.

The full-range refinement (9.9034--100.0949 deg 2theta, 8301 points) gives
Rwp = 6.780%, Rp = 4.933%, Rexp = 2.662%, and goodness of fit = 2.550. The
reported Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio were used.
Because pointwise uncertainties were not supplied, Poisson counting
uncertainties, sigma = sqrt(max(counts, 1)), were assumed.

## Evidence

The diagnostic monoclinic WO3 family is present as the resolved group near
23.43, 23.91, and 24.68 deg and the dense group near 33.57, 33.91, and
34.47 deg. Bixbyite Mn2O3 accounts for the separate cubic sequence headed by
the 222 reflection near 33.25 deg and continuing through the 400, 332, 440,
and 622 families. The refined cells reproduce these families throughout the
measured range. After both phases are included, the largest residual features
occur on already modeled WO3/Mn2O3 peaks or within their overlapping tails;
there is no remaining coherent, separately indexable reflection family.

Exact-composition tungstate candidates were tested. MnWO4 is contradicted by
the absence of its characteristic low-angle reflections near 15.5 and
18.5 deg and its 30.0--30.5 deg pair. Mn3WO6 is likewise contradicted by the
absence of its characteristic reflections near 19.95 and 20.49 deg. Alternative
WO3 and Mn2O3 settings gave poorer or metrically collapsed solutions; the
accepted P 21/c WO3 and Ia-3 Mn2O3 models retained ordinary geometry and
stable positive scales.

Cells, scales, background, specimen displacement, and bounded phase-profile
terms were refined. A uniaxial [110] microstrain term for WO3 is supported by
the reflection-dependent widths; Mn2O3 was retained with isotropic broadening.
Preferred-orientation tests stayed effectively at unity and were omitted.
Coordinate-refinement trials did not provide a stable improvement and caused
unnecessarily large oxygen shifts, so the vetted reference coordinates were
restored. The final geometries are chemically ordinary: W--O distances span
1.714--2.159 A and Mn--O distances span 1.896--2.246 A; calculated densities
are 7.269 and 5.027 g cm-3, respectively.

## Remaining uncertainty

The phase identities and topologies are well supported, but this laboratory
powder pattern does not independently determine subtle oxygen displacements or
atomic displacement parameters. In particular, zero WO3 Uiso entries in its
CIF are reference placeholders, not a claim of zero thermal motion. The formal
fraction uncertainty from the least-squares covariance is 0.27 wt% for each
phase, but model, overlap, microabsorption, and specimen-systematic effects are
not included; a more realistic uncertainty is about +/-2 wt% absolute. Trace
phases below the pattern's detection sensitivity cannot be excluded.

The submitted CIFs, `fit.csv`, and fractions were exported from the same
replayable `final.gpx` checkpoint.
