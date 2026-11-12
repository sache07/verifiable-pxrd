# Powder XRD phase analysis

## Result

Two crystalline phases are required. Fractions are normalized over the modeled crystalline material; they do not quantify amorphous material.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CaWO₄, scheelite | Tetragonal *I*4₁/*a* (frozen COD 7219229 starting model) | *a* = 5.23740, *c* = 11.33329 | 0.8516 (85.16 wt%) |
| WO₃, monoclinic | *P*2₁/*c* (frozen COD 2311041 starting model) | *a* = 7.69360, *b* = 7.55651, *c* = 10.51756, β = 135.94743 | 0.1484 (14.84 wt%) |

The formal GSAS-II fraction standard uncertainty is about 0.00046 for each phase. Model choice, background/profile correlation, and possible noncrystalline material make a practical uncertainty of roughly 1–2 wt% more realistic.

## Evidence

The broad dominant family at 18.27, 28.43, 31.21, 33.84, 46.90, 54.17, 57.65 and 76.10° 2θ is indexed by scheelite CaWO₄. The sharper triplet at 22.77, 23.19 and 23.99°, together with narrow companions near 26.19, 28.76, 33.13 and 49.49°, is indexed by monoclinic WO₃. This inventory is chemically consistent with partial conversion of WO₃ and CaCO₃ at 650 °C.

The chosen WO₃ reference gave the best stable, physical whole-pattern checkpoint. A second *P*2₁/*c* reference (COD 1528915) gave Rwp about 4.12% under the same screening sequence versus about 3.73% for COD 2311041 before final specimen/coordinate refinement. Orthorhombic and tetragonal WO₃ models were substantially worse. A triclinic same-composition branch was numerically unstable and therefore is not treated as rigorously excluded, but it did not provide a better stable physical model. Characteristic calcite and CaO families were not present, and no coherent residual reflection family remained after fitting CaWO₄ + WO₃.

The final refinement includes the reported Cu Kα₁/Kα₂ wavelengths, a smooth 14-term background, physically bounded polarization and surface roughness, phase-specific size/strain, isotropic phase-wide displacement parameters, and [001] uniaxial microstrain for WO₃. Marginal CaWO₄ texture and strain-anisotropy branches returned nearly random/isotropic values and were omitted. The requested staged polish selected its all-coordinate branch: Rwp improved from 3.466% to 3.405%, the CaWO₄/WO₃ fractions changed by only 0.03 wt% absolute, and its geometry audit found no short contacts or fraction collapse. Refined W–O distances are about 1.760 Å in CaWO₄ and 1.69–2.18 Å in distorted WO₃ octahedra.

## Fit and uncertainty

The final observed-data statistics are Rwp = 3.405%, Rp = 2.557%, Rexp = 3.138%, goodness of fit = 1.086, and χ² = 9772.24 for 8301 points. A fresh native GSAS-II replay, with no optimization, reproduced Rwp = 3.405% and reported no profile-validity flags.

The CaWO₄ topology and phase assignment are high confidence. The monoclinic WO₃ assignment is supported by many split reflections, but its individual oxygen coordinates are not independently precise: bounded oxygen-coordinate trials reached limits and were rolled back, while only stable interior coordinate shifts were retained. The angular zero also lies at the allowed −0.25° boundary and is correlated with specimen displacement and cell parameters, so cell and coordinate precision should not be inferred from printed digits alone. Surface-roughness parameter A likewise lies at its physical lower bound; it represents a supported low-angle intensity correction, not a uniquely measured surface property. Any amorphous or extremely minor crystalline Ca-bearing residue is outside the sensitivity of this crystalline normalization.
