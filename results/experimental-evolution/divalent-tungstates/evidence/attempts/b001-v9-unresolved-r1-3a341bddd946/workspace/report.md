# PXRD phase analysis

## Result

The best-supported tested model contains four crystalline phases. Fractions are normalized over these modeled crystalline phases only; they do not measure amorphous material or absolute crystallinity.

| Phase | Space group | Weight fraction | Formal GSAS-II s.u. |
|---|---:|---:|---:|
| Fergusonite-related SrWO4 | C2/c (I2/a-equivalent setting) | 59.00% | 1.03 percentage points |
| Orthorhombic WO3 | Pnma | 15.66% | 0.47 percentage points |
| Orthorhombic SrCO3 | Pnma | 14.85% | 1.02 percentage points |
| Scheelite SrWO4 | I4_1/a | 10.48% | 0.73 percentage points |

The combined modeled SrWO4 fraction is 69.49%. This total is more robust than the 59.00/10.48% polymorph split. The exact values used in `result.json` come from the reopened `final.gpx` replay.

## Chemical and structural evidence

The metadata reports WO3 and SrCO3 precursors heated at 650 °C, but supplies no precursor amounts or ratio. A numerical precursor element balance therefore cannot be imposed without inventing a constraint. Using Sr2+, W6+, and O2-, the charge-balanced inventory challenge included SrWO4, Sr2WO5, Sr3WO6, Sr3W2O9, SrW2O7, and Sr2W3O11. Exact or adapted non-1:1 models were scale-tested under the same nuisance model. The exact Sr3W2O9 and tested Sr2WO5 models refined to zero scale; the positive Sr3W2O9-, Sr3WO6-, and SrW2O7-analogue scales improved mainly overlapped families or only one unique family, so they were not retained.

The dominant phase is modeled with a CaWO4 fergusonite parent (COD 1546035) adapted to SrWO4. The cell and the special-position Sr and W coordinates were refined; oxygen coordinates remain those of the parent. Refining oxygen coordinates gave 0.68–0.91 Å O–O contacts and was rejected. Independent CaMoO4, NdTaO4, direct-I2/a, scheelite, Pnma, and P2_1/c topology competitors were compared. In the final matched-nuisance replacement challenge, the no-texture C2/c control gave Rwp = 19.186%, versus 21.786% for the best tested SrCrO4-type P2_1/c replacement and about 22.23–22.26% for AgMnO4-/BaMnO4-type Pnma replacements. This supports retaining the C2/c topology, although it does not prove its oxygen substructure.

The scheelite model was adapted from SrMoO4 (COD 2300460). It has a positive replay-stable scale and improves two independent residual families near 27.2° and 32.64° 2theta. Replacing the C2/c phase with scheelite alone was markedly worse, so the two models represent competing metric families rather than duplicate records. Their refined scale correlation is moderate, r = -0.442.

Orthorhombic WO3 (COD 2107312) was preferred over tested monoclinic, triclinic, and tetragonal WO3 records. Orthorhombic SrCO3 (COD 9008198) has a positive stable scale and unique lines, consistent with unreacted precursor. A reviewed rhombohedral carbonate record had disorder and zero scale and was rejected.

All four submitted CIFs pass `learned/cif_health.py`: they are ordered, fully occupied, and have no hard contacts or oxygen-contact review flags. Minimum contacts are 1.719 Å (C2/c SrWO4), 1.762 Å (scheelite SrWO4), 1.788 Å (WO3), and 1.266 Å (the C–O bond in SrCO3).

## Refinement and profile checks

The full 9.9034–100.0946° range (8301 points) was replayed after reopening the project. The model uses the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, a 12-term Chebyshev background, one fitted nonnegative Gaussian W term (W = 61.1227; X = 0), and one sample-displacement correction (137.569 micrometres). Inactive phase terms are neutral: size = 10 micrometres, strain = 0, March ratio = 1, and roughness = 0. The only retained texture term is a C2/c [110] March–Dollase ratio of 0.74105. A scheelite texture term was rejected after cell reconvergence because it became 98.8% correlated with its scale. W+X, anisotropic-strain, roughness, polarization, and higher-order texture challenges were unsupported or bound and were removed. No parameters are frozen in the submitted project.

Direct half-height measurements below use the raw observed and calculated profiles after subtracting the refined background; crossings were linearly interpolated. Values in parentheses are left/right half-widths in degrees.

| Region | Observed position | Calculated position | Observed FWHM | Calculated FWHM |
|---|---:|---:|---:|---:|
| Low, isolated family | 23.8342° | 23.8559° | 0.1980° (0.0990/0.0991) | 0.2446° (0.1231/0.1215) |
| Middle, isolated family | 44.8280° | 44.8280° | 0.2388° (0.1105/0.1283) | 0.2609° (0.1223/0.1386) |
| High-angle residual family | 95.0091° | 94.6940° | 0.2205° (0.1137/0.1068) | 0.5944° (0.2187/0.3757) |

Final statistics are Rwp = 18.7715%, Rp = 12.2973%, Rexp = 2.8579%, and goodness-of-fit = 6.5683, with a final maximum shift/s.u. of 0.000092. The goodness-of-fit is materially above counting expectation, and the high-angle spot check shows a structured mismatch. Targeted tests of phase inventory, SrWO4 topology, WO3 polymorph, angular correction, common profile, and phase strain did not resolve it without bound, correlated, chemically implausible, or non-replay-stable terms.

## Remaining uncertainty

This is the best-supported model among those tested, but it is not a uniquely or fully resolved structure solution. In particular, the exact C2/c SrWO4 oxygen arrangement and the split between C2/c and scheelite SrWO4 cannot be determined reliably from this pattern. The reported formal fraction uncertainties omit model-selection error and are therefore too optimistic; the individual fractions should be treated as approximate. Coherent residuals could reflect an inadequately represented Sr–W–O structure, an unresolved weak phase, or uncalibrated profile behavior. No additional phase met the required positive replay-stable scale plus two independent non-coincident residual-family criterion, so none was added speculatively.
