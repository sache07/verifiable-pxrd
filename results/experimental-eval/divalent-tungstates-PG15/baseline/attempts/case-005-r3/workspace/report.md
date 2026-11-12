# PXRD phase analysis

The pattern is explained by two crystalline phases: monoclinic WO3 and cubic spinel Co3O4. The reported fractions are normalized over these modeled crystalline phases only.

| Phase | Space group | Weight fraction | Structural model |
|---|---:|---:|---|
| WO3 | P 21/c (No. 14) | 73.89 wt% | `phase_1_WO3.cif` |
| Co3O4 | F d -3 m (No. 227) | 26.11 wt% | `phase_2_Co3O4.cif` |

The final Rietveld fit has Rp = 2.461%, Rwp = 3.439%, Rexp = 1.722%, and goodness of fit = 2.000 (8,301 observations and 28 refined variables). The background-subtracted Rwp is 5.628%. The refinement converged with a maximum shift/standard-uncertainty ratio of 0.0028.

## Evidence and model choice

The WO3 assignment accounts for the characteristic cluster near 23.46, 23.95, and 24.71 degrees 2theta, the 33.59--34.52 degree group, and lines near 50.26 and 56.24 degrees. Co3O4 accounts for its spinel series near 19.37, 31.64, 37.20, 45.14, 59.68, and 65.56 degrees. Together, these models account for all prominent crystalline peaks. The starting structures were COD 2311041 (WO3) and COD 9005896 (Co3O4).

A CoWO4 model was also tested because the sample was heated from Co3O4 and WO3 precursors. Its refined scale collapsed to the lower bound; the covariance-derived approximate 95% upper amount was about 0.2 wt% under that particular profile model. There is therefore no positive evidence for crystalline CoWO4, although trace material below this approximate sensitivity cannot be excluded.

Alternative orthorhombic and triclinic WO3 descriptions were evaluated. The triclinic model lowered the overall Rwp by only 0.029 percentage point, produced a nearly monoclinic metric, worsened the background-subtracted Rwp, and required two additional cell parameters. P21/c was therefore retained as the more parsimonious ambient WO3 description. Its submitted CIF uses a valid nonstandard cell (a = 7.69173, b = 7.53426, c = 10.54194 A, beta = 136.1543 degrees); an equivalent conventional cell is a = 7.30314, b = 7.53426, c = 7.69173 A, beta = 90.6967 degrees.

## Refinement and uncertainty

Because pointwise uncertainties were not supplied, count-statistical weights proportional to 1/intensity were used. Refined quantities included phase scales and cells, specimen displacement, a 15-term Chebyshev background, an effective polarization term, a common Gaussian profile contribution, phase-specific isotropic broadening, and the Co3O4 oxygen coordinate. A displacement of -0.702 mm was needed to describe the common peak-position offset. The atomic coordinates of WO3 were kept at the literature values because positional refinement was strongly correlated; atomic displacement parameters and detailed local geometry are consequently not determined reliably by this dataset.

The covariance-only standard uncertainty of each normalized fraction is 0.22 percentage point. Profile alternatives shifted the result by roughly 2 percentage points, so approximately +/-2 percentage points is a more realistic model-dependent uncertainty: WO3 about 73.9 +/- 2 wt% and Co3O4 about 26.1 +/- 2 wt%. Residual structure around the strongest peaks and the goodness of fit above one support this more cautious estimate. The fractions do not quantify amorphous material or absolute bulk phase content. Apparent coherent-domain sizes were profile-dependent and are not reported quantitatively because no calibrated instrumental profile was supplied.
