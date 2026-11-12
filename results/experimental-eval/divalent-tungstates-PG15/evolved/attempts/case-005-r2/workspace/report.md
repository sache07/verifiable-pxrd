# Phase analysis and refinement report

## Result

The modeled crystalline material is monoclinic tungsten trioxide, WO3 (space group P 21/c), plus cubic spinel Co3O4 (space group F d -3 m). The refined crystalline-phase fractions are:

| Phase | Weight fraction | Covariance esd | Practical estimate |
|---|---:|---:|---:|
| WO3 | 0.74894 | 0.00177 | about 75 ± 2 wt% |
| Co3O4 | 0.25106 | 0.00177 | about 25 ± 2 wt% |

Fractions are normalized only over the modeled crystalline phases. No amorphous fraction can be measured from this pattern without an internal standard. The ±2 wt% practical uncertainty reflects model dependence; it is more realistic than the much smaller covariance-only esd.

The final whole-pattern statistics are Rwp = 3.3752%, Rp = 2.4705%, Rexp = 1.7221%, goodness of fit = 1.9622, and reduced chi-squared = 3.8504. The final serialized-project replay had maximum shift/esd = 0.0092.

## Evidence and inventory decisions

The dominant peak families—including the resolved groups near 23.5–24.7° and 33.6–34.5° 2theta—are explained by monoclinic WO3. The residual after fitting WO3 contains the coherent spinel sequence near 19.3, 31.6, 37.2, 38.9, 56.0, 59.7, and 65.5° 2theta, which supports Co3O4 through multiple unique or partly overlapped families. This is also chemically consistent with the stated Co3O4/WO3 precursors and 500 °C treatment.

Several physical alternatives were challenged under the same restrained profile model. Monoclinic, triclinic, orthorhombic, and smaller-cell monoclinic WO3 records were screened; the ambient monoclinic neutron model from COD 2311041 gave the stable physical solution. A lower-symmetry triclinic trial wandered on replay, and the other WO3 polymorphs fit substantially worse. The first Co3O4 record collapsed because of its starting cell, but an independent full-occupancy record (COD 9005896) refined cleanly, so the record—not the phase—was rejected.

No usable exact CoWO4 entry was present in the supplied index. Following the analogue search, CoWO4 models made independently from CoMoO4 and FeWO4 wolframite parents were geometry-screened and tested. Both repeatedly refined to the GSAS-II scale floor, as did an exact CoO model. They are therefore unsupported, not claimed absent below an unknown detection limit. No remaining residual family coherently supports a third crystalline phase.

## Structural and profile model

The metadata Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio were fixed. Because pointwise uncertainties were not supplied, counting uncertainties were taken as sqrt(counts). The final Bragg–Brentano model uses a smooth six-coefficient Chebyshev background, one specimen-displacement correction, positive common U/W/X terms, a one-parameter low-angle surface-roughness correction, and isotropic WO3 microstrain. The background remains smooth and positive. Low-, middle-, and high-angle isolated families show no remaining common position or width trend. Phase-size trials ran to ineffective bounds, phase strain on Co3O4 became nonphysical, and no coherent family-dependent broadening justified anisotropy.

Polarization and roughness were compared before texture. Polarization alone was plausible, but fitting it together with roughness produced strong correction/scale correlations; the conventional fixed polarization of 0.5 and the nested roughness term were retained. Releasing axial asymmetry was 98.7% correlated with specimen displacement and drifted on replay, so it was removed. Symmetry-distinct March–Dollase axes gave WO3 ratios of 0.994–1.004, while Co3O4 texture was unidentifiable; all texture terms were pruned.

Cells were refined to a = 7.6914(28), b = 7.53411(21), c = 10.542(5) Å, beta = 136.157(5)° for WO3 (the nonstandard P 21/c setting of the source model), and a = 8.08100(26) Å for Co3O4. Full occupancy and ordered stoichiometry were retained. The Co3O4 oxygen parameter refined to u = 0.2624(8), giving plausible tetrahedral and octahedral Co–O distances near 1.92–1.93 Å. WO3 has physically plausible distorted WO6 octahedra (nearest W–O distances about 1.71–2.16 Å).

Detailed WO3 coordinates and displacement parameters cannot be determined reliably from this powder pattern: trial coordinate refinement was highly correlated and replay-unstable, and the parent reported zero displacement terms. Its neutron-parent coordinates were therefore fixed, and the zero WO3 Uiso values in the CIF should be treated as placeholders rather than measured thermal parameters. The Co3O4 oxygen coordinate is modestly constrained; its other coordinates and displacement terms remain sourced values.

The low Durbin–Watson value (0.558) and goodness of fit above one show residual serial structure beyond counting noise, so neither the structural precision nor the covariance fraction esds should be over-interpreted. Changing the plausible angular-intensity correction moves the WO3 fraction from about 0.728 to 0.749; this is the basis for the stated approximately ±0.02 absolute systematic fraction uncertainty.

All submitted CIFs, phase fractions, and the profile in `fit.csv` were exported from the reopened `final.gpx`; `final_audit.json` records the two replay states and file checksums.
