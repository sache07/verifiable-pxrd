# Powder XRD phase analysis

The 700 °C product is modeled by four crystalline phases. Weight fractions are
normalized only over these modeled crystalline phases.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| CuWO4 | triclinic P-1, COD 4000806 | 0.63786 (63.79 wt%) |
| WO3 | monoclinic P21/c, COD 2311041 | 0.19996 (20.00 wt%) |
| Cu3WO6 | cubic Pa-3, COD 1527404 | 0.13755 (13.76 wt%) |
| CuO | monoclinic C2/c, COD 1011194 | 0.02463 (2.46 wt%) |

## Evidence and phase closure

The dominant split-peak family is matched by triclinic CuWO4. Under common
single-phase nuisance settings its Rwp was 32.371%, compared with 51.877--55.025%
for the same-formula P2/c model and Cu-substituted Zn/Fe/Mg/Mn/Cd tungstate or
W-substituted CuMoO4 prototypes. Monoclinic WO3 is chemically consistent with
unreacted WO3 precursor and reduced the common two-phase Rwp to 19.968%; the
selected COD 2311041 model outperformed the other physically valid WO3
polymorphs. Cubic Cu3WO6 accounts for the sharp families near 15, 20, and
33--35° 2theta. Adding it in either order gave the same three-phase solution
(Rwp 10.336%, approximately 15.1 wt% Cu3WO6 before later refinement). C2/c CuO
then closed the coherent residual family near 32.5, 35.6, 38.7°, and at higher
angles; it was marginally better than the lower-symmetry Cc alternative under
identical four-phase settings.

Closure tests rejected Cu4O3 and an additional WO3 polymorph because their
scales collapsed. Extra P2/c CuWO4 contributed only 0.099 wt%. Cu2WO4 gave only
0.143 wt% and required a strongly distorted cell. The Cu2O trial diverged and
is therefore unknown rather than rejected; a trace amount below the practical
detection limit cannot be excluded. The largest final residuals are paired
negative/positive lobes around strong modeled peaks, not a coherent one-sign
family attributable to another phase.

## Refinement and checks

The refinement used the stated Cu Kalpha1/Kalpha2 wavelengths and intensity
ratio over the complete 9.903--100.095° grid. It included a smooth Chebyshev
background, phase scales and cells, an angular zero term, a reduced common
profile, polarization, common positive isotropic displacement parameters for
the three larger phases, and only supported coordinate subsets. The
uncalibrated scan required a GSAS-II zero value of -0.49133°. A full profile
trial drove U to its boundary, so U was fixed at zero; the retained V/W/X
profile has a positive analytic width over the full range. Only one supported
anisotropic term was retained: uniaxial [100] microstrain for CuWO4. Texture and
sample-displacement trials were negligible and omitted. Crystallite-size values
were fixed nuisance limits and are not interpreted as measured sizes.

The final saved fit has Rwp = 3.1926%, Rp = 2.4261%, and goodness of fit =
1.9772. A read-only native GSAS-II replay regenerated the atomic structure
factors and profile without optimization, reproduced the submitted curve to
numerical precision, and reported no profile-review flags. All exported CIFs
have full site occupancies and reidentify in the expected space groups. Minimum
cation--oxygen distances are 1.71--1.93 Å and minimum O--O distances are
2.45--2.61 Å; no short-contact or negative-displacement failure remains.

## Remaining uncertainty

These fractions do not quantify amorphous material because no internal
standard was supplied. Systematic uncertainty from the uncalibrated zero,
profile overlap, and reference-model dependence is more important than the
least-squares precision; CuO at 2.46 wt% has the largest relative uncertainty,
so the rounded inventory (about 64:20:14:2.5 wt%) is more defensible than all
reported digits. WO3 and Cu3WO6 oxygen coordinates were not freely refined
because unrestricted oxygen branches produced implausibly short bonds; their
topologies and fractions are supported, but subtle oxygen defects, partial
occupancy, or solid solution cannot be determined reliably from this pattern.
