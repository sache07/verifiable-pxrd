# Powder XRD phase analysis

The specimen is an essentially unreacted crystalline precursor mixture. The accepted model contains **monoclinic WO3 (69.98 wt%)** and **rutile beta-MnO2 (30.02 wt%)**. Fractions are normalized over these modeled crystalline phases; the scan does not determine an amorphous fraction.

| Phase | Space group / refined cell | Crystalline weight fraction |
|---|---|---:|
| Monoclinic WO3 | No. 14, reduced P21/n setting; a = 7.31456, b = 7.54441, c = 7.70110 A, beta = 90.7681 deg | 0.69981 (formal e.s.d. 0.00133) |
| Rutile beta-MnO2 | P42/mnm (No. 136); a = 4.40418, c = 2.87618 A | 0.30019 (formal e.s.d. 0.00133) |

## Evidence

The three dominant observed maxima at 23.443, 23.932, and 24.693 deg 2theta are the split monoclinic WO3 002/020/200 family (calculated at 23.465, 23.948, and 24.702 deg). The independent rutile MnO2 family is present at 29.007 (110), 37.667 (101), and 56.955 deg (211), together with its higher-angle reflections. These two structures account for every coherent reflection family across 9.903-100.095 deg.

The WO3 model is the physical monoclinic topology represented by COD 2311041, transformed to an equivalent reduced No. 14 setting before refinement. A lower-symmetry triclinic checkpoint gave only a small numerical gain by moving its metric toward monoclinic symmetry, so it was rejected as an over-parameterized description. Coordinate changes were capped at the stated reference-mismatch scale. The submitted geometries pass the occupancy/contact screen: W-O = 1.733-2.171 A and Mn-O = 1.884-1.897 A.

Residual-phase tests for MnWO4, Mn3WO6, and Mn3O4 drove their scales to zero. Mn2O3 produced only an approximately 1 wt% scale and a very small residual improvement without a unique, broadly supported reflection family; it was therefore rejected as an overlap fit. No crystalline tungstate product is reliably detected.

## Fit and uncertainty

The full-grid GSAS-II fit has Rwp = 5.5565%, Rp = 4.1054%, Rexp = 2.6932%, and goodness of fit = 2.0649 for 8301 points. An independent no-refinement forward replay from `final.gpx` reproduced Rwp = 5.5565% and raised no profile-physics flags.

The formal fraction e.s.d.s reflect counting statistics and the final scale/background step only. A more realistic systematic uncertainty is about 1-2 wt% because scale, displacement parameters, preferred orientation, surface roughness, and overlapping WO3/MnO2 intensities are correlated. Atomic oxygen coordinates are less certain than the phase identities and cells and should not be interpreted as single-crystal precision. Angular zero and specimen displacement are also strongly correlated; both were retained at physical values from controlled sequential refinements. Additional crystalline material below roughly 1-2 wt%, especially if strongly overlapped, cannot be excluded, and amorphous content cannot be quantified from this normalization.
