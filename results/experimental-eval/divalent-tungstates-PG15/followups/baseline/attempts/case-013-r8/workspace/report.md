# Powder diffraction phase analysis

The pattern is best described by four crystalline phases: scheelite PbWO4,
monoclinic WO3, orthorhombic massicot PbO, and tetragonal litharge PbO. The
fractions below are normalized over these modeled crystalline phases only.

| Phase | Space group | wt.% | formal s.u. (wt.%) | Refined CIF |
|---|---:|---:|---:|---|
| PbWO4_scheelite | I 41/a | 74.03 | 0.27 | [phase_pbwo4_scheelite.cif](phase_pbwo4_scheelite.cif) |
| WO3_monoclinic | P 21/c | 11.61 | 0.25 | [phase_wo3_monoclinic.cif](phase_wo3_monoclinic.cif) |
| PbO_massicot | P b c m | 9.31 | 0.15 | [phase_pbo_massicot.cif](phase_pbo_massicot.cif) |
| PbO_litharge | P 4/n m m | 5.06 | 0.13 | [phase_pbo_litharge.cif](phase_pbo_litharge.cif) |

## Evidence

The dominant peak set (including the intense reflections near 27.70, 45.03,
and 55.54 degrees 2theta) indexes as scheelite PbWO4. The characteristic WO3
cluster near 23.4--24.7 degrees and its higher-angle reflections require
monoclinic WO3. The remaining precursor-like peaks require both PbO polymorphs:
massicot accounts for, among others, intensity near 29.35, 30.62, and 38.09
degrees, while litharge accounts for its distinct 29.00, 32.11, and 35.95
degree family. This assignment is chemically consistent with partial reaction
of PbO and WO3 at the reported 500 degrees C.

Quantitatively, adding the precursor phases lowered Rwp from about 18.1% for
PbWO4 alone to 13.559% for the submitted four-phase model.
Alternative WO3 cells/polymorphs were compared; the chosen room-temperature
monoclinic model gave the best balance of fit and structural parsimony.
Pb7W8O28.8, Pb3O4, PbO2, and monoclinic PbWO4 trials did not refine to stable
positive additional fractions.

## Refinement and uncertainty

GSAS-II Rietveld refinement used Cu Kalpha1/Kalpha2 wavelengths 1.540598 and
1.544426 angstrom with the reported 0.5 intensity ratio, a 20-term smooth
Chebyshev background, refined phase scales and unit cells, and a common
pseudo-Voigt profile. Atomic coordinates were retained from the cited database
models because this overlapping multiphase laboratory pattern does not support
independent coordinate refinement. The fitted interval is 10.02--99.98 degrees
2theta (8280 points). With no supplied
pointwise uncertainties, Poisson counting uncertainties sqrt(I) were used.
The fit statistics are Rwp = 13.559%, Rp = 9.124%,
Rexp = 3.502%, and goodness of fit = 3.882.

The tabulated fraction s.u.'s are least-squares values and understate systematic
uncertainty from peak overlap, background, profile choice, and the uncalibrated
instrument function. Weak unassigned intensity remains, especially near 25.92,
30.16, and 31.04 degrees 2theta, and some strong-peak shapes are imperfect.
No fifth phase could be identified and quantified reliably, so its structure
and fraction are explicitly undetermined and it is omitted from the normalized
fractions. Absolute amorphous content likewise cannot be obtained without an
internal standard.

The submitted [final.gpx](final.gpx) is the project from which all four CIFs,
[fit.csv](fit.csv), the fractions, and the reported statistics were generated.
