# PXRD phase analysis

## Result

The modeled crystalline material is predominantly triclinic CuWO4 with a small monoclinic WO3 residue. Exact project-normalized values are used in `result.json` and `final.gpx`.

| Phase | Structural model | Refined cell | Submitted crystalline fraction | Conservative reporting |
|---|---|---|---:|---:|
| CuWO4 | P -1 (No. 2) | a = 4.71346, b = 5.84897, c = 4.88673 Å; alpha = 88.3453, beta = 92.5326, gamma = 97.2493 degrees | 97.5425 wt% | 97.5 +/- 0.2 wt% |
| WO3 | P 21/n setting (No. 14; equivalent to standard P 21/c) | a = 7.31027, b = 7.54902, c = 7.69860 Å; beta = 90.8779 degrees | 2.4575 wt% | 2.5 +/- 0.2 wt% |

The final full-range fit (9.9034-100.0949 degrees 2-theta, 8301 points) has Rwp = 4.3167%, Rp = 3.3504%, Rexp = 2.4333%, and goodness of fit = 1.7786. The last save/reopen replay converged with maximum shift/esd = 0.0046.

## Evidence and model selection

CuWO4 is supported by the precursor chemistry (CuO + WO3, 800 degrees C) and by the complete strong-peak sequence. High-pressure exact-composition records were rejected as source-condition-inappropriate. The starting structure was the ambient neutron Cu0.9Zn0.1WO4 model COD 2101690, with its mixed divalent site replaced by fully occupied Cu. The refined model remains chemically physical: bond-valence analysis gives Cu2+/W6+/O2-, Cu-O distances are 1.933-1.989 Å (four) plus 2.355-2.418 Å (two), and W-O distances are 1.770-2.249 Å.

The second phase is required by coherent residual families, especially the partly isolated WO3 groups near 33.58/33.89, 55.05-56.35, and 76.94 degrees. Rwp decreased from 5.428% for the refined major-phase-only model to 4.459% for the two-phase common baseline, and then to 4.317% after the accepted intensity correction. The submitted model derives from ambient COD 2311041, transformed to a Niggli P 21/n setting; its cell and scale were refined, while its atomic coordinates were held at the prototype values. An ambient triclinic WO3 alternative gave Rwp = 4.637% before the final intensity correction, versus 4.459% for the monoclinic model, despite having more cell variables. CuO (C2/c and Cc), Cu3WO6, and Cu2WO4 challenges all refined to zero scale under the final common profile.

## Refinement controls

Raw counts were retained and sqrt(counts) working uncertainties were used because pointwise uncertainties were not supplied. The model uses the reported Cu K-alpha wavelengths and K-alpha2/K-alpha1 ratio, an eight-term smooth Chebyshev background, one zero correction (+0.3612 degrees), positive common U/W/X profile terms, and SH/L axial asymmetry. A one-parameter low-angle surface correction (SurfRoughB = 0.04933 with SurfRoughA fixed at zero) was retained because it corrected several isolated-family intensity ratios and was stable at 0.050-0.053 when the background order was varied. The two-parameter roughness form was non-identifiable and was rejected.

Observed/calculated FWHM checks for isolated CuWO4 families were 0.149/0.142 degrees at 15.62 degrees, 0.157/0.154 degrees at 24.45 degrees, and 0.162/0.164 degrees at 31.17 degrees. High-angle group envelopes and K-alpha doublets showed no monotonic position or width drift, and the remaining profile residuals did not define a coherent hkl-dependent broadening trend. Isotropic size improved Rwp by only 0.0015 percentage point and was 99% correlated with instrument X; isotropic strain worsened the fit and was strongly correlated with U/X. Both were returned to neutral values. Six symmetry-distinct March-Dollase axes stayed within about 0.7% of random orientation after the surface correction and were pruned. Polarization refinement traded strongly against atomic displacement factors and was also pruned; the fixed value is 0.70.

## Remaining uncertainty

The least-squares phase-fraction esd is only 0.0368 wt%, but it is optimistic because the counting uncertainties were inferred and model choices dominate. Alternate ambient WO3 records/settings, background orders, and accepted/rejected intensity corrections give a more realistic approximately 0.2 wt% uncertainty, reflected in the rounded values above. The surface parameter is 95% correlated with absolute scale, so its physical roughness magnitude is not independently reliable; the normalized CuWO4/WO3 ratio is much more stable.

At about 2.5 wt%, monoclinic WO3 is reliably detected, but its oxygen coordinates cannot be refined reliably from this pattern and the precise low-temperature WO3 variant is less certain than the phase identity. Crystallite size and microstrain also cannot be determined reliably. Fractions are normalized only over the modeled crystalline phases; amorphous content and trace phases below the diffraction detection limit are not quantified.
