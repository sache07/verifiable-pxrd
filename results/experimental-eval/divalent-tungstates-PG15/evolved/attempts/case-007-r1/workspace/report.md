# Quantitative phase analysis

## Result

The crystalline pattern is modeled by three phases. Weight fractions are normalized only over those modeled crystalline phases.

| Phase | Space group | Weight fraction | Refined cell |
|---|---:|---:|---|
| MgWO4, wolframite | P 2/c | 78.58 wt% | a = 4.69456, b = 5.68017, c = 4.93352 Å, β = 90.7737° |
| WO3, monoclinic | P 21/c | 14.00 wt% | a = 7.69781, b = 7.54308, c = 10.53900 Å, β = 136.0892° |
| MgO, periclase | F m -3 m | 7.42 wt% | a = 4.21651 Å |

Final whole-pattern statistics are Rwp = 9.344%, Rp = 6.968%, and goodness-of-fit = 3.267 (8284 observations, 24 variables). The final save/reopen replay converged with maximum shift/s.u. = 0.006.

## Evidence and model selection

- MgWO4 is supported by the wolframite families at 15.93° (010), 19.23° (100), 24.21° (011), 30.80/31.11°, and many middle/high-angle families. The retained COD 9013902 model is a synthetic, ambient-pressure, fully occupied P2/c structure with sensible MgO6 and WO6 coordination. A weak [110] March–Dollase correction is required (final parameter about 1.087): under the completed three-phase inventory, Rwp is 9.344% versus 9.731% without texture and 9.51–9.55% for competing tested axes.
- WO3 is identified by the characteristic 23.43/23.91/24.68° triplet and coherent families near 33.57–34.48°, 48.56–50.21°, and higher angle. The full-occupancy neutron P21/c model (COD 2311041) preserves complete distorted WO6 octahedra. Under the same final nuisance model it outperforms triclinic (Rwp 9.613%), an alternate monoclinic record (9.822%), orthorhombic (12.586%), and hexagonal (19.180%) WO3. Competing WO3 texture axes improve Rwp by at most 0.014 percentage point and do not give a coherent axial-family trend, so no WO3 texture term is retained.
- MgO is supported independently by all six accessible rocksalt families: 111, 200, 220, 311, 222, and 400 at 37.23, 43.20, 62.57, 74.93, 78.86, and 94.24°. Adding it to the two-phase common-profile model lowers Rwp from 10.303% to 9.344%. Their extracted Fobs²/Fcalc² ratios are close to unity, so MgO texture is not justified.
- Oxygen-deficient W18O49 was re-challenged as a weak watch-list phase. With its source cell fixed it reached only 0.49 wt% and changed Rwp by 0.015 point, while several of its strongest unique or partly overlapped families coincide with negative residuals. Freeing its cell worsened Rwp to 9.48%. It is therefore not a reliable detection and is excluded. The other indexed Mg–W–O records are either a 900 °C-incompatible dihydrate or contain a dummy oxygen site rather than a usable alternate structure.

## Refinement and physical checks

The raw counts were fitted from 10.0° to 100.0° 2θ with Cu Kα1/Kα2 wavelengths and the reported 0.5 intensity ratio fixed. Because pointwise uncertainties were absent, sqrt(counts) Poisson uncertainties were used. The baseline uses a smooth six-coefficient Chebyshev background (positive over the fit range, 242–2106 counts), one zero correction, a nonnegative common U/W/X profile, refined effective polarization, and a fixed replay-stable SH/L asymmetry value. Isolated low-, middle-, and high-angle profiles were checked for position, width, and asymmetry; no monotonic mismatch remained.

Phase scales and cells were refined. Atomic coordinates, occupancies, and displacement parameters were kept at the physically screened literature values because this mixed-phase laboratory X-ray pattern does not determine them independently. Size, microstrain, anisotropic broadening, roughness, extinction, and other unused nuisance terms were neutral/fixed. Isotropic size/strain and symmetry-distinct uniaxial-size trials either reached neutral/bounds, became nonphysical, drifted on replay, or changed Rwp negligibly, and were pruned.

## Remaining uncertainty

The phase identities and refined metrics are reliable, but the fractions are semi-quantitative. Formal covariance e.s.d.s are 0.17, 0.08, and 0.18 wt-percentage points for MgWO4, WO3, and MgO, respectively; these are smaller than realistic systematic uncertainty from overlap, preferred orientation, source structures, and the uncalibrated instrumental profile. About 1–2 wt-percentage points absolute is a more conservative interpretation. No amorphous fraction can be obtained from this normalization. The largest remaining residuals are low-angle MgWO4/WO3 intensity/profile residuals, not a coherent additional peak family.

The submitted CIFs, `fit.csv`, phase fractions, and statistics were all exported from the reopened `final.gpx` project.
