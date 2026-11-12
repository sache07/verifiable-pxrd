# Powder XRD phase analysis

The pattern is described by four crystalline phases. Weight fractions are normalized over these modeled crystalline phases:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| CuWO4 (copper(II) tungstate) | P -1 | 0.6463 (64.63 wt%) |
| WO3 | P 21/c | 0.1933 (19.33 wt%) |
| Cu3WO6 | P a -3 | 0.1336 (13.36 wt%) |
| CuO (tenorite) | C 2/c | 0.0269 (2.69 wt%) |

## Method and evidence

The original counts were refined in GSAS-II with the Cu K-alpha doublet specified in `metadata.json` (1.540598/1.544426 A, K-alpha2/K-alpha1 = 0.5). Because pointwise uncertainties were not supplied, counting-statistical weights, sigma = sqrt(max(counts, 1)), were used. Candidate structures were screened from COD references and then refined by staged Rietveld analysis: scale/background, cells and specimen displacement, instrumental and phase broadening, preferred orientation, common isotropic displacement parameters, and supported atomic coordinates.

Triclinic CuWO4 is required by the dominant peak set and accounts for most intensity. Monoclinic P 21/c WO3 gave the best fit among tested WO3 polymorphs. Cu3WO6 is independently supported by lines near 15.18, 19.79, 32.49, 33.77, 42.87, 49.69, 57.60, and 63.29 degrees 2-theta that remained after fitting CuWO4 and WO3. The weaker residual peaks near 35.10, 38.32, and 48.45 degrees identify tenorite CuO. No coherent unmodeled peak family remained to justify another crystalline phase.

The replayed final model gives Rwp = 2.0849%, Rp = 1.5454%, Rexp = 1.6141%, chi-square = 13813.13, and goodness of fit = 1.2917 over 8301 points. Fresh GSAS-II calculation from the saved parameters, rather than the project's cached calculated profile, reproduces this Rwp without profile-review warnings. Refined structures also retain plausible nearest-neighbor distances (minimum W-O about 1.69-1.79 A and Cu-O about 1.93 A).

## Uncertainty and limitations

The phase identities and the three larger fractions are well supported by multiple non-overlapping reflections. The 2.69 wt% CuO fraction is less reliable in relative terms because it is based on weak, partly overlapped peaks; a conservative interpretation is approximately 2-3 wt%. Absolute fraction uncertainties are also limited by the absence of an external standard, supplied pointwise uncertainties, and an amorphous-phase model. The reported fractions therefore quantify only the modeled crystalline material and cannot determine amorphous content.

The exact oxygen coordinates, especially in minor CuO and the lower-symmetry WO3 model, are less certain than the phase identities and unit cells. Some specimen/profile quantities reached physically allowed edges, and the CuWO4 isotropic atomic-displacement parameter was highly correlated with polarization; these microstructural and nuisance parameters should not be interpreted quantitatively. They do not create additional phase peaks, but they are a source of systematic uncertainty in the last few tenths of a weight percent.

Reference starting models were COD 4000806 (CuWO4), 2311041 (WO3), 1527404 (Cu3WO6), and 1011194 (CuO). The submitted CIFs contain the refined cells, coordinates, and displacement parameters.
