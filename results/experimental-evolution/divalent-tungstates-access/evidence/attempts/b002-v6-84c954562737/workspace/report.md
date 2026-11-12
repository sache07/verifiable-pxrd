# Powder XRD phase analysis

The 800 °C product is modeled as a five-phase crystalline mixture. Fractions are normalized only over the modeled crystalline material; this analysis does not determine an amorphous fraction.

| Phase | Structural model | Weight fraction (wt%) |
|---|---|---:|
| MnWO4, wolframite | monoclinic P 2/c | 68.86 ± 0.41 |
| WO3 | monoclinic P 21/c | 24.70 ± 0.22 |
| MnO | rocksalt F m -3 m | 2.40 ± 0.23 |
| Mn3O4, orthorhombic model | Pbcm post-spinel-type | 2.75 ± 0.38 |
| Mn3O4, hausmannite | tetragonal I 41/amd | 1.29 ± 0.27 |

The uncertainties in the table are GSAS-II internal scale/covariance estimates and do not include phase-model uncertainty. The fresh atomic replay of `final.gpx` gives Rwp = 16.189% and Rp = 9.251% on the complete measured grid (8301 points); the saved 10–100° refinement has Rwp = 16.194% and GOF = 8.14.

## Evidence

Wolframite MnWO4 accounts for the dominant families, including the reflections near 15.47, 18.43, 23.67, 24.19, 29.99, and 30.42° 2θ. Residual precursor reflections near 23.08–24.2°, 28.62°, and 33.2–34.2° require WO3. A physical monoclinic WO3 model was selected over a reference with an impossible 1.58 Å O–O contact; the submitted model has minimum O–O = 2.54 Å and normal W–O distances. A triclinic WO3 trial fit only slightly better, but its metric refined toward monoclinic symmetry, so the chemically ordinary room-temperature monoclinic model was retained.

Rock-salt MnO is supported by the coherent sequence around 35.11, 40.5, 58–59, and 70–74°. The orthorhombic Mn3O4 model indexes the residual family near 19.86, 25.43, 31.76, and 46.49°, while weak tetragonal Mn3O4 is needed principally for the 32.48° reflection and overlapping hausmannite lines. With all five phases present, no coherent residual reflection family remains unindexed.

## Remaining uncertainty

The major MnWO4 and WO3 assignments are robust. The two Mn3O4 polymorphs are weak and correlated: their combined fraction is about 4.0 wt%, but the split between 1.3 wt% tetragonal and 2.8 wt% orthorhombic material is not reliable at the precision suggested by the internal errors. In particular, the orthorhombic assignment uses a high-pressure post-spinel-type reference whose cell was indexed and expanded to the observed ambient pattern; its exact topology and metastable presence after an 800 °C synthesis remain provisional. MnO is supported by several reflections, but its 2.4 wt% fraction is also profile-model dependent.

The prescribed staged polish was run once. Its nominal best branch was rejected because absolute geometry review exposed the nonphysical contact already present in the starting WO3 reference. The submitted `final.gpx` instead contains the physical exact-composition WO3 replacement followed by bounded phasewise coordinate refinement; every bound-hit atom was restored, all submitted CIFs pass the hard-contact/occupancy screen, and a fresh read-only GSAS-II replay reports no profile validity flags.
