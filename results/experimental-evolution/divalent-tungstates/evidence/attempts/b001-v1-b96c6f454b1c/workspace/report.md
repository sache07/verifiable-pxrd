# PXRD phase analysis

## Result

The crystalline model contains three phases. Fractions are normalized over these modeled crystalline phases only.

| Phase | Space group | Weight fraction | Formal esd |
|---|---:|---:|---:|
| MnWO4, wolframite | P 2/c (No. 13) | 0.75204 (75.20 wt%) | 0.00310 |
| WO3, gamma monoclinic | P 21/c (No. 14) | 0.19418 (19.42 wt%) | 0.00221 |
| Mn3O4, hausmannite | I 41/a m d (No. 141) | 0.05378 (5.38 wt%) | 0.00278 |

The final fit has Rp = 5.0081%, Rwp = 7.7313%, Rexp = 2.4845%, GOF = 3.1118, and chi-square = 80004.79 for 8301 points and 39 refined variables. The project converged with maximum shift/esd = 0.040. `fit.csv` was exported from this exact saved project; its calculated profile agrees with the reloaded project to 5e-9 counts (CSV rounding).

## Evidence and candidate screening

MnWO4 is required by its diagnostic wolframite peak family, including the low-angle 010 and 100 lines and the split reflections around 29.6-30.0 degrees. A MnWO4-only fit gave Rwp about 15.29%. Adding residual WO3 and reconverging background, scales, zero, and both cells reduced Rwp to about 11.90%; subsequent physically constrained profile and structure refinement reduced it to 7.887%. Hausmannite then accounts for independent residual families, especially its relatively isolated 103 line near 31.77 degrees and lines near 58.08 and 59.33 degrees. Its addition lowered Rwp to 7.731% with a positive scale.

No exact MnWO4 record was present in the supplied index. Stoichiometric-analogue searching identified wolframite parents. The selected parent, FeWO4 COD 9008124, is an ambient, fully occupied P 2/c structure without reported disorder; Fe2+ was replaced isovalently by Mn2+. ZnWO4 and MgWO4 wolframite parents gave the same chemically sensible topology. Thin-film FeWO4 records with anomalously large displacement parameters were rejected. The final MnWO4 geometry is physical: Mn-O = 2.072-2.198 A and W-O = 1.801-2.141 A, with bond-valence assignments Mn2+/W6+/O2-.

For WO3, fully occupied gamma-monoclinic records COD 2311041 and 1528915 were compared under the same modest model; COD 2311041 fitted slightly better and was retained. Orthorhombic WO3 was poorer. A triclinic control gave only a marginal early improvement while adding lower-symmetry cell freedom, so the exact WO3 polymorph is less secure than the chemical identification. The final WO3 octahedra have W-O = 1.685-2.199 A and valid W6+/O2- bond valences.

The selected Mn3O4 model is the fully occupied 295 K hausmannite record COD 9001963. Its occupied composition is pure Mn3O4 despite the source study discussing Fe substitution. The modern coordinates fit better than the idealized 1926 COD 1011262 record under an identical nuisance model (Rwp 7.7314% versus 7.7603%). The final tetrahedral Mn-O distance is 2.044 A and octahedral distances are 1.928/2.290 A, with Mn2+/Mn3+/O2- bond valences. An inconsistent doubled-cell record was rejected. Mn3WO6 was also rejected because its strong diagnostic reflections near 19.95 and 20.49 degrees are absent, and a scheelite-type MnWO4 control lacks the observed wolframite low-angle family.

The phase inventory uses only Mn-W-O compounds and is consistent with incomplete reaction of the reported Mn3O4 and WO3 precursors to MnWO4. The modeled crystalline Mn:W ratio is about 0.96:1. Feed masses were not supplied, so a stricter precursor mass-balance test is not possible.

## Refinement discipline

The metadata Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio were used. Since pointwise uncertainties were absent, weights were based on Poisson counting statistics. An eight-term Chebyshev-1 background was refined. Zero and specimen displacement were tested separately: zero gave the better initial fit (Rwp 15.292% versus 15.341%), while displacement refined to an implausible approximately 0.83 mm. Only zero was retained; its final value is -0.49720 degrees.

The low-dimensional global profile has U = 279.069 and V = -347.290 fixed after staged determination, with W = 119.678 and X = 3.355 refined; Y and Z are zero. The Gaussian width polynomial remains positive over the entire fitted range (minimum 11.63). No texture correction was used. All phase sizes are fixed at the GSAS-II 10 micrometre no-broadening limit. MnWO4 and Mn3O4 microstrain are zero and fixed. Only isotropic WO3 microstrain is active, at 6569 ppm; its large value is strongly supported by the broad WO3 peaks but is model-dependent. A MnWO4 size test ran to the no-broadening limit and correlated 98.5% with global X, while a strain test requested unphysical negative broadening, so both were rejected. There are no frozen variables or parameters at active bounds. The largest retained correlations are 0.907 for two nonstandard WO3 cell-metric terms and -0.884 for global W/X.

MnWO4 coordinates were refined. For broad, minority WO3 only the two W positions were refined and O positions were retained from the source. Mn3O4 atomic coordinates were fixed to the source because its approximately 5 wt% contribution cannot support reliable coordinate refinement. Occupancies and displacement parameters were not used as compensating variables.

## Remaining uncertainty

MnWO4 is identified with high confidence; WO3 and Mn3O4 are supported as residual precursor phases. The precise WO3 monoclinic-versus-triclinic polymorph assignment is moderately confident because its peaks are broad and overlap strongly. Full WO3 oxygen coordinates and any Mn3O4 coordinate deviations cannot be determined reliably from this pattern.

The quoted fraction esds are conditional counting-statistical values, not total uncertainties. The lack of a calibrated instrument profile, the large angular zero correction, correlated residuals (Durbin-Watson 0.281), and the model-dependent WO3 broadening introduce additional systematic uncertainty. The analysis does not quantify amorphous material, so the fractions must not be interpreted as absolute whole-sample mass fractions.
