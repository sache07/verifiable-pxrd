# Powder XRD phase analysis

The 900 °C SrCO3 + WO3 specimen is modeled by three crystalline phases: scheelite SrWO4, residual WO3, and Sr3W2O9. Fractions normalized over these modeled crystalline phases are **69.87 wt% SrWO4**, **11.54 wt% WO3**, and **18.59 wt% Sr3W2O9**. No amorphous fraction was determined.

## Evidence

- Scheelite SrWO4 (COD 1546036, I 41/a) explains the dominant reflection set. Its refined cell is a = 5.42381 Å and c = 11.97091 Å.
- A physical triclinic WO3 model (COD 2106293, P -1; a/b/c = 7.30802/7.54484/7.69462 Å) accounts for the residual precursor family. A slightly better-fitting alternative COD entry was rejected because it generated a 1.57 Å O–O contact; the submitted model has normal distorted WO6 geometry.
- Exact-composition Sr3W2O9 (COD 2311977 topology, C 2/c) gives a stable positive scale and indexes the previously unassigned family, including reflections near 29.77, 30.90, 32.56, 56.97, and 61.22° 2theta. Its metric required residual-guided adaptation to a/b/c = 10.78762/5.85021/12.03885 Å, beta = 98.0637°. After this phase was included, no separate coherent fourth reflection family remained.
- The final full-grid atomic replay has Rwp = 12.951%, Rp = 9.173%, and GOF = 3.669 over 8282 points. The replay reported no negative-background, peak-width, displacement-tensor, or other physical-review flags.

## Remaining uncertainty

SrWO4 is secure. WO3 is secure as a composition/precursor assignment, but its exact low-symmetry polymorph and oxygen coordinates are less well constrained by this overlapped powder pattern. Sr3W2O9 is the least certain structure: its coherent peak family and positive abundance are robust, while the adapted metric, minor-phase light-atom coordinates, and [111] texture term are correlated; the texture ratio reached the imposed physical limit (1.4). Its reported fraction should therefore be regarded as approximate (several wt% systematic uncertainty), and the other fractions inherit that covariance. Unconstrained minor-phase oxygen refinements were rejected as unreliable. Fractions describe only the modeled crystalline material.

The submitted CIFs and `fit.csv` were exported from, or freshly replayed from, `final.gpx`; the project retains the original observed scan and all accepted profile, calibration, background, and atomic parameters.
