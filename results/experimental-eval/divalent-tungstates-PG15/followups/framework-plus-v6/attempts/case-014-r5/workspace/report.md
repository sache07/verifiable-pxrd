# Powder XRD phase analysis

The 10.0094–99.9944° 2θ Cu Kα pattern is modeled by three crystalline phases. Fractions below are normalized over those modeled crystalline phases; the uncertainties in parentheses are GSAS-II covariance estimates, not total systematic errors.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO₄ (scheelite) | *I*4₁/*a* | a = 5.41929, c = 11.96103 | 63.539(223)% |
| WO₃ | *P*2₁/*c* | a = 7.69528, b = 7.54047, c = 10.52589, β = 136.05977 | 9.491(151)% |
| Sr₂WO₅ | *Pnma* | a = 7.25412, b = 5.54875, c = 10.89526 | 26.970(215)% |

The full-range refinement has Rwp = 7.2063%, Rp = 5.5396%, expected Rwp = 3.5351%, and goodness of fit = 2.0411 for 8,282 observations and 33 refined variables. A fresh, zero-parameter replay from `final.gpx` reproduces the profile and fractions and raises no negative-background, peak-width, polarization, or displacement-tensor flags.

## Evidence and model selection

The dominant peak positions and relative intensities select tetragonal scheelite SrWO₄ (starting record COD 1546036). Its cell and oxygen coordinate were refined with soft W–O and Sr–O distance restraints; the final geometry passes the contact screen. The weaker monoclinic families are consistently described by the physical *P*2₁/*c* WO₃ record COD 2311041. An older WO₃ record with an implausibly short O–O contact was rejected, and a triclinic candidate fit substantially worse.

The remaining strong, coherent families require an Sr-rich ternary phase. No exact Sr₂WO₅ database entry was available, so the submitted *Pnma* model was built by isovalent Ba²⁺→Sr²⁺ and Re⁶⁺→W⁶⁺ substitution in the Ba₂ReO₅ prototype (COD 1529756). Its scale and cell refine stably, it accounts for several unique or only partly overlapped families, and it passes composition, occupancy, and interatomic-contact checks. Replacing it with tested Sr₃WO₆ prototypes increases Rwp from about 7.2% to about 16% before any trace-phase challenge.

The common profile used the metadata Cu Kα₁/Kα₂ wavelengths and 0.5 intensity ratio, an eight-term smooth Chebyshev background, one specimen-displacement correction, nonnegative W/X peak-width terms, axial asymmetry, and a low-angle surface-roughness correction. Isotropic crystallite size was retained for WO₃ and Sr₂WO₅. Uniaxial size/strain and preferred-orientation trials were unstable, bound-limited, or unsupported by multiple families and were removed. SrCO₃ refined to a negligible scale and collapsed on cell release. A high-pressure fergusonite SrWO₄ record was chemically inappropriate and lacked its diagnostic splitting.

## Remaining uncertainty

The Sr₂WO₅ phase identity, cell, and approximate amount are well supported, but its detailed oxygen coordinates are provisional: unconstrained coordinate refinement was unstable, so the analogue coordinates were retained. They should not be interpreted as a definitive structure solution. Surface roughness is highly correlated with absolute phase scales; normalized fractions were stable in roughness sensitivity trials, but their true systematic uncertainty is larger than the formal errors in the table. Without an internal standard, amorphous material cannot be measured and the reported fractions are not absolute whole-sample fractions.

Sr₃WO₆-like fourth-phase trials can absorb less than roughly 1 wt% of residual intensity, but different prototypes produce incompatible cells and no coherent set of unique peaks. A trace Sr-rich impurity therefore cannot be excluded, but neither its structure nor its fraction can be determined reliably from this pattern and it is not included in the quantified inventory.
