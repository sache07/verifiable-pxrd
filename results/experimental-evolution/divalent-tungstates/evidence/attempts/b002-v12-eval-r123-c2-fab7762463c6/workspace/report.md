# PXRD phase analysis

The pattern is modeled by three crystalline phases, with weight fractions normalized over those phases:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| MgWO4 (wolframite) | monoclinic P2/c, COD 9013902 | 0.51334 (51.33 wt%) |
| WO3 | monoclinic P21/c, COD 2311041 | 0.41163 (41.16 wt%) |
| MgO (periclase) | cubic Fm-3m, COD 9000499 | 0.07503 (7.50 wt%) |

The full-range GSAS-II replay converged without singularities at Rwp = 2.3048%, Rp = 1.7769%, Rexp = 1.5271%, and goodness of fit = 1.509. The formal GSAS-II fraction standard uncertainties are 0.00073, 0.00069, and 0.00091, respectively. Model/source trials indicate a more realistic systematic uncertainty of roughly 1 wt% absolute for each major phase and about 0.3–0.5 wt% for MgO.

## Evidence

MgWO4 accounts for the characteristic 15.58°, 18.88°, 23.82°, and 30.41°/30.73° families. Monoclinic WO3 accounts for the resolved 23.13°/23.57°/24.37° triplet and independent families near 33–34°, 41.5°, 50°, and 56°. The lower-symmetry triclinic WO3 competitor was slightly favored at the neutral common-profile checkpoint, but the ranking reversed after phase-width terms were tested; after cross-seeding all shared nuisance values and giving each source its own width/texture loop, monoclinic WO3 remained better (Rwp 2.306% versus 2.445% for the best triclinic trial). Tetragonal, orthorhombic, hexagonal, and the alternate monoclinic record were substantially poorer.

MgO is weak but robust. Removing it raises Rwp to 3.013%. Its scale returns to 7.50 wt% from both 0.2x and 5x starting values, and independent 200, 220, 222, and 400 families at approximately 42.91°, 62.31°, 78.65°, and 94.07° each reduce local residuals. Thus it is not retained solely through an overlapped line or scale/background compensation.

The accepted profile uses a smooth 10-term Chebyshev background, one zero correction, nonnegative U/W/X broadening, and refined polarization. MgWO4 needs a replay-stable [010] March-Dollase term (ratio 1.300); WO3 needs uniaxial microstrain and a weak [110] March-Dollase term. Size/strain trials for MgWO4 and MgO returned to neutral values or forced common profile terms to bounds and were rejected. Roughness and higher background orders were unsupported. Isolated low-, middle-, and high-angle peak audits showed no repeated axial asymmetry beyond the modeled Cu K-alpha doublet, so SH/L remained fixed.

All candidate source models used in the serious comparisons were screened with `learned/cif_health.py`; all three exported CIFs pass the final geometry/occupancy screen. Atomic coordinates were retained from the vetted records because the broadened, overlapping laboratory pattern does not determine independent coordinate refinements reliably; unit cells were refined.

## Remaining uncertainty

The fractions are crystalline-phase-normalized because there is no internal standard, so amorphous content cannot be measured. No precursor amounts or MgO:WO3 ratio were supplied in the metadata, preventing an independent mass-balance closure test. Pointwise uncertainties were also absent; Poisson counting weights were used. The monoclinic WO3 assignment is favored reproducibly, but the exact low-symmetry atomic distortion is less secure than the phase composition because broadening masks some subtle splitting.
