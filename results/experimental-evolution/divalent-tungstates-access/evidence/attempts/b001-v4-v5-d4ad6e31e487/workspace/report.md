# Powder XRD phase analysis

The pattern is described by four crystalline phases. Weight fractions are normalized over those phases only.

| Phase | Space group | Weight fraction | Main evidence |
|---|---:|---:|---|
| CuWO4 | P -1 | 64.918(40)% | Triclinic CuWO4 families including 29.08, 30.06, 31.34, and 31.50 deg 2theta |
| Cu3WO6 | Pa-3 | 13.150(29)% | Distinct peaks at 15.18, 19.79, 32.49, and 33.78 deg 2theta |
| WO3 | P 21/c | 19.247(25)% | Characteristic monoclinic triplet at 22.66, 23.04, and 23.90 deg 2theta |
| CuO | C 2/c | 2.685(35)% | Coherent tenorite family at 35.08, 38.31, 48.43, 58.10, and 67.69 deg 2theta |

Numbers in parentheses are formal one-sigma least-squares uncertainties on the last shown digits; they do not include model systematics. The phase inventory gives Cu/W = 1.021 on a molar basis, providing an independent near-equimolar closure for the CuO + WO3 precursor chemistry.

The ambient P -1 CuWO4 model was strongly preferred to the high-pressure P 2/c alternative. Monoclinic room-temperature WO3 gave the best physical topology checkpoint (initial three-phase Rwp 8.16%, versus 8.39% for triclinic and 18.04% for orthorhombic WO3; tetragonal and hexagonal scales collapsed). For CuO, C 2/c tenorite and a Cc subgroup fitted almost identically after cell relaxation, but the Cc coordinate refinement was singular and perfectly correlated; the standard C 2/c tenorite geometry was therefore retained. After CuO was included, every coherent residual family indexed to an accepted phase.

Cells, scale factors, heavy- and light-atom coordinates, common isotropic displacement factors where supported, and profile terms were refined in stages with geometry rollback. Final cation-oxygen distances remain physical: W-O 1.72-2.18 A, Cu-O 1.91-2.37 A in the tungstates, and the expected 1.93-1.97 A short Cu-O contacts in tenorite. WO3 required supported [001] uniaxial microstrain (about 1502/2212 ppm equatorial/axial) and a very weak [010] March-Dollase term (1.011). No coherent unassigned peak family remains.

The full 8301-point refinement has Rwp = 1.7178%, Rp = 1.2808%, expected Rwp = 1.6163%, goodness-of-fit = 1.069, and reduced chi-squared = 1.143. The difference column in `fit.csv` is observed minus calculated.

No external standard was supplied, so amorphous material and the absolute crystalline yield cannot be determined reliably; the reported fractions apply only to the modeled crystalline material. The weak CuO fraction is more sensitive than its formal error suggests to displacement-factor/scale correlation, and exact oxygen coordinates are less certain than the phase topologies. Coherent-domain sizes for Cu3WO6, WO3, and CuO refined beyond the allowed 1.5 micrometre upper bound and are therefore only lower limits, not reliable size determinations.
