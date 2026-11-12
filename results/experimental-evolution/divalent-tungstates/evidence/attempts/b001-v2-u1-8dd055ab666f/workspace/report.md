# Phase analysis and Rietveld refinement

The pattern is modeled as four crystalline phases. Weight fractions are normalized over those modeled crystalline phases:

| Phase | Space group | Weight fraction | Submitted structure |
|---|---:|---:|---|
| PbWO4, scheelite | I 41/a (No. 88) | 0.5862 (formal e.s.d. 0.0021) | `phase_PbWO4_scheelite.cif` |
| WO3, monoclinic | P 21/c (No. 14) | 0.1955 (0.0015) | `phase_WO3_monoclinic.cif` |
| Pb3O4, minium | P 42/m b c (No. 135) | 0.1702 (0.0021) | `phase_Pb3O4_minium.cif` |
| PbO, massicot | P b c m (No. 57) | 0.0481 (0.0012) | `phase_PbO_massicot.cif` |

The full-range final fit has Rwp = 5.768%, Rp = 4.001%, Rexp = 2.485%, and goodness of fit = 2.325 for 8,301 points and 32 refined parameters. The replay-checked project is `final.gpx`; `fit.csv` contains the observed, calculated, and observed-minus-calculated profiles.

## Evidence

The strongest broad peak family is the scheelite PbWO4 pattern, while the sharp 23.52/24.01/24.83° triplet and its higher-angle families identify monoclinic WO3. Adding ambient-pressure Pb3O4 to the PbWO4 + WO3 model reduced Rwp from about 10.31% to 8.83% before the supported phase-width terms were introduced. A remaining pair at approximately 29.52° and 30.80° is diagnostic of orthorhombic massicot PbO; adding it to the stabilized three-phase model reduced Rwp from 6.96% to 6.27%, and its independently supported size broadening reduced the residual further. Residual WO3 and Pb3O4 are also chemically consistent with incomplete reaction of the two precursors at 500 °C.

Candidate records were screened for occupied composition, experimental conditions, symmetry, disorder, and geometry before refinement. Ambient, fully occupied COD records 9009811 (PbWO4), 2311041 (WO3), 9012124 (Pb3O4), and 2310433 (massicot) were selected. Raspite PbWO4 fit very poorly. A Pb-deficient, occupancy-disordered Pb7W8O28.8 record produced a slightly worse but similar profile because its average structure is scheelite-related; the diffraction data alone do not tightly exclude small Pb-vacancy nonstoichiometry, but the full-occupancy PbWO4 model is chemically cleaner and fits slightly better. Alternate WO3 and Pb3O4 records were inferior or had unsuitable pressure/geometry provenance.

No exact Pb2WO5 database entry was available, so Pb2MoO5, Pb2CrO5, and Pb2TeO5 stoichiometric prototypes were inspected after chemically explicit W substitution. The physically plausible Pb2MoO5-derived model had poor diagnostic-peak agreement and a weak, high-R-factor scale contribution. PbO2 and litharge converged to effectively zero scale with unstable cells. These trials do not support a fifth crystalline phase.

One specimen-displacement correction was used; zero was not co-refined. Its angular dependence fit the observed peak offsets better than a zero-only branch. The common instrument envelope was fixed at U = 5, W = 20, X = 0 from the sharp lower-width envelope because broader global-instrument branches obscured the sharp phases and changed fractions. Supported phase terms were isotropic size for PbWO4 (about 49 nm), Pb3O4 (31 nm), and massicot (43 nm), plus isotropic WO3 microstrain (about 2440 microstrain). Size-only and strain-only branches were compared separately; combined or anisotropic terms, preferred orientation, and extra asymmetry were not supported. Only the Pb2+ coordinate pair in Pb3O4 was retained as a refined atomic parameter. Other coordinate trials were rejected when weak/correlated or chemically implausible—for example, free scheelite oxygen shifted the W–O distance from 1.775 to 2.063 Å.

## Remaining uncertainty

The quoted e.s.d.s are covariance-derived precision within this model, not complete accuracy estimates. No external standard or calibrated instrument profile was supplied, pointwise uncertainties were absent, and Poisson counting uncertainties were therefore used. Exact systematic uncertainties on the fractions cannot be determined reliably from this dataset alone; the 4.8 wt% massicot fraction is the least secure and is particularly coupled to its broadening model. The fractions also say nothing about amorphous material or unmodeled content.

Phase identity and space group are more secure than detailed oxygen coordinates. Most atomic coordinates were therefore retained from vetted source structures, and the data do not independently establish subtle PbWO4 vacancy stoichiometry. Remaining positive residuals near 55.6° and 72.3° coincide with overlapping reflections of the modeled phases rather than a coherent unmatched peak family. The final project was saved, reopened, and replay-refined over 9.903–100.095° 2theta; it converged with maximum shift/e.s.d. 0.010 and no frozen variables before the CIFs, fractions, and profile were exported.
