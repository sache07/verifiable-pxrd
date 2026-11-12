# PXRD phase analysis

The pattern is modeled by four crystalline phases. Weight fractions are normalized over these phases only.

| Phase | Structure and source | Weight fraction |
|---|---|---:|
| Stolzite, PbWO4 | I41/a, COD 9009811 | 57.93 wt% |
| Monoclinic WO3 | P21/c, COD 2311041 | 20.21 wt% |
| Minium, Pb3O4 | P42/mbc, COD 9012124 | 16.97 wt% |
| Massicot, PbO | Pbcm, COD 2310433 | 4.89 wt% |

The full-range Rietveld fit gives Rwp = 2.8201%, Rp = 2.1740%, Rexp = 2.4853%, and goodness of fit = 1.1368 (8,301 points from 9.9034 to 100.0946 degrees 2theta). The final refined cells are PbWO4 a = 5.46601, c = 12.05831 A; WO3 a = 7.69129, b = 7.53449, c = 10.52312 A, beta = 136.1928 degrees in the source's nonconventional P21/c setting; Pb3O4 a = 8.80184, c = 6.55883 A; and PbO a = 5.87839, b = 5.48485, c = 4.75004 A.

## Evidence

The chemistry is internally consistent with the reported WO3/Pb3O4 precursor inventory: PbWO4 is the dominant reaction product, while WO3 and Pb3O4 remain and PbO is a plausible lead-oxide byproduct. No precursor amounts were supplied, so no fixed bulk balance was available or varied. All coherent peak families are accounted for, so a non-1:1 analogue search was not warranted.

Diagnostic families include the WO3 23.53/24.02/24.83 degree triplet; dominant PbWO4 peaks at 27.81, 30.03, 33.17, 45.13, and 47.39 degrees; Pb3O4 peaks at 14.69, 26.79, 29.07, 31.20, 32.54, and 52.53 degrees; and PbO families at 29.52, 38.24, 53.58, and 60.73 degrees. Removing PbO and reconverging raises Rwp to 4.454%, with strong positive residuals at several non-coincident PbO families, so its 4.9 wt% scale is not an overlap artifact.

Representative local peak-shape checks are below. Each entry is position, FWHM, and left/right half-width in degrees; the high-angle right broadening includes the reported Cu Kalpha doublet.

| Family | Observed | Calculated |
|---|---|---|
| Pb3O4 110 | 14.685; 0.278; 0.174/0.103 | 14.641; 0.250; 0.120/0.130 |
| WO3 20-2 | 23.530; 0.125; 0.051/0.074 | 23.530; 0.124; 0.052/0.072 |
| PbWO4 112 | 27.811; 0.237; 0.114/0.124 | 27.811; 0.240; 0.114/0.125 |
| PbO 002 | 38.232; 0.261; 0.103/0.158 | 38.254; 0.283; 0.146/0.136 |
| PbWO4 024 | 45.132; 0.295; 0.133/0.162 | 45.121; 0.285; 0.116/0.169 |
| Pb3O4 332 | 52.532; 0.284; 0.134/0.150 | 52.532; 0.326; 0.159/0.167 |
| PbWO4 040 | 68.973; 0.351; 0.119/0.232 | 68.984; 0.359; 0.135/0.225 |
| PbWO4 512 | 94.042; 0.458; 0.145/0.313 | 94.042; 0.428; 0.130/0.298 |

Every retained source and its principal competitor was geometry-screened before fitting. Final-source replays favored the selected records: the closest Pb3O4 competitors gave Rwp 2.867% (orthorhombic Pbam) and 2.894% (alternate tetragonal), the alternate monoclinic WO3 record gave 3.240%, and the alternate orthorhombic PbO record gave 2.853% with an unstable supercell metric. Raspite PbWO4, orthorhombic WO3, litharge PbO, and other records either fit much worse or collapsed. All four exported CIFs pass the final geometry/occupancy health screen.

The final model uses an eight-term smooth Chebyshev background, one sample-displacement correction (-730.0 micrometres), positive U/W instrumental width terms, isotropic phase size/strain terms, and no texture or roughness. Anisotropic broadening, March-Dollase texture, X broadening, and roughness/polarization combinations were rejected because they collapsed, violated physical bounds, were axis-nonunique, or failed replay stability. The saved project was reopened and reconverged over the complete range before export; its final maximum shift/esd was 0.0011.

## Remaining uncertainty

The tabulated formal one-sigma fraction errors are approximately 0.06-0.10 wt%, but they are conditional least-squares errors using count-based weights because pointwise uncertainties and a calibrated instrumental profile were not supplied. They do not include source-model, absorption, microabsorption, or sample-preparation systematics; a practical interpretation should allow several tenths of a wt% absolute, especially for PbO. Atomic coordinates were retained from the selected COD structures and only cells, scales, and profile terms were refined, so detailed oxygen coordinates are not independently determined by this laboratory pattern. Absolute amorphous content and absolute sample weight fractions cannot be determined without an external standard; the submitted fractions apply only to the modeled crystalline material.
