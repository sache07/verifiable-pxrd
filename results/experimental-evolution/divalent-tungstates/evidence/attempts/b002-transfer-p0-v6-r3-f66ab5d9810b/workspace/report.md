# Quantitative phase analysis

The pattern is modeled by four crystalline phases. Fractions below are normalized to the modeled crystalline material; they do not measure amorphous content.

| Phase | Space group | Weight % (formal esd) | Refined cell |
|---|---:|---:|---|
| BaWO4 | I 41/a | 63.46 ± 0.16 | a=5.63041, c=12.69405 Å |
| WO3 | P 21/c | 12.37 ± 0.13 | a=7.68896, b=7.54081, c=10.51553 Å, β=136.0739° |
| BaCO3 | P m c n | 8.11 ± 0.18 | a=5.30944, b=8.91651, c=6.43791 Å |
| Ba3W2O9 | R -3 c | 16.06 ± 0.10 | a=10.13466, c=13.95719 Å |

The refined fractions imply an overall Ba:W atomic ratio of 1.020, chemically consistent with a near-equimolar Ba/W precursor inventory. The final full-range fit (9.9034–100.0946° 2θ) has Rwp=3.256%, Rp=2.517%, Rexp=3.017%, and GOF=1.081. The last maximum shift/esd was 0.002; no parameters were frozen at bounds.

## Phase evidence and model selection

- **BaWO4:** The dominant scheelite I41/a peak set and its low-, middle-, and high-angle doublets are reproduced by a fully occupied scheelite model. The sole exact COD record (1527204) uses split half-occupied oxygen sites and gives short 1.47/1.80 Å W–O contacts; it fit worse than a physical fully occupied model. I41/a BaMoO4, SrWO4, and CaWO4 parents were screened because the A-site and tetrahedral-site substitutions preserve the scheelite topology. The retained oxygen site gives a tetrahedral W–O distance near 1.83 Å. An unconstrained oxygen refinement lowered Rwp but lengthened W–O to about 1.97 Å, so it was rejected as nonphysical.
- **WO3:** Monoclinic gamma-WO3 (COD 2311041, P21/c setting) accounts for the residual precursor families. A second monoclinic record (1528915) was close but worse; triclinic 2106293 and orthorhombic 2107312 were clearly poorer under the same nuisance model. The powder data support the monoclinic topology and cell, but not subtle oxygen-displacement distinctions between closely related gamma-WO3 descriptions.
- **BaCO3:** Ambient witherite gives nonzero scale and coherent partly isolated families. COD 9010928 supplied the supported Ba sublattice and Pmcn setting, but its carbonate geometry contained a 1.41 Å C–O contact. Carbonate coordinates from the physical alternate exact Pnma record 1011149 were transformed into the same setting, giving three approximately 1.24 Å C–O bonds and a slightly better fit. The complete 1011149 intensity model and a substituted SrCO3 prototype were both poorer under the same nuisance model; the high-temperature trigonal record 1539129 was also worse.
- **Ba3W2O9:** COD 1533878 (R-3c) was identified from a residual family at approximately 26.28, 30.82, 37.67, 40.80, 43.02, 51.85, 53.71, and 63.07° 2θ. Their common scale and cell persist after the common profile is rebuilt, supporting a genuine secondary reaction product rather than a single-peak assignment.

## Refinement adequacy

The Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio were fixed from the metadata. A smooth six-term Chebyshev background, one zero correction (0.28004°), effective polarization (0.98592), and a common nonnegative U/W/X profile (4.722/17.508/2.899) reproduce isolated low-, middle-, and high-angle peak positions and widths. SH/L asymmetry, surface roughness, phase size, and preferred orientation were replayed and rejected: symmetry-distinct axial and diagonal March-Dollase trials changed Rwp by at most 0.004 percentage points without coherent multi-family support. Isotropic microstrain was retained only for the three broader minor phases (WO3 2862, BaCO3 6307, Ba3W2O9 1518 in GSAS-II microstrain units); BaWO4 strain and all size trials were unsupported or reached bounds. The background remains positive and smooth.

## Remaining uncertainty

No pointwise standard uncertainties or calibrated instrumental profile were supplied. GSAS-II counting-statistics weights make the tabulated esds formal and smaller than realistic model uncertainty; minor-phase fractions are likely uncertain at roughly the 1–3 wt% level because scale, broadening, overlap, and source-coordinate choices are coupled. The relatively large fitted zero correction also makes absolute cell errors more systematic than their formal esds. Atomic coordinates for the minor phases and the BaWO4 oxygen site cannot be determined reliably from this pattern and were therefore retained from physically screened source/prototype structures. Absolute amorphous content cannot be determined without an internal standard, so all reported fractions are crystalline-normalized.

The submitted [final.gpx](final.gpx) was reopened and replayed over the complete measured range before [fit.csv](fit.csv), [result.json](result.json), and the four phase CIFs were exported from that exact project state.
