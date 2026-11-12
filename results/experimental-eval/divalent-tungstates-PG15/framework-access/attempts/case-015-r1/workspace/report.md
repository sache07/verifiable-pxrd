# Powder XRD phase analysis

## Result

The crystalline pattern is modeled by three Zn-W-O phases. Weight fractions are normalized over these modeled crystalline phases; they do not quantify any amorphous material.

| Phase | Structural model | Refined cell | Weight fraction |
|---|---|---|---:|
| Zinc tungstate, ZnWO4 (wolframite) | P 2/c (No. 13) | a = 4.69135 Å, b = 5.71933 Å, c = 4.92693 Å, beta = 90.6308° | 0.74581 (74.58 wt%) |
| Zinc oxide, ZnO (wurtzite) | P 63 m c (No. 186) | a = 3.25044 Å, c = 5.20866 Å | 0.06371 (6.37 wt%) |
| Tungsten trioxide, WO3 (monoclinic) | P 21/c (No. 14) | a = 7.30520 Å, b = 7.53707 Å, c = 10.5338 Å, beta = 133.098° | 0.19047 (19.05 wt%) |

The WO3 cell is an obtuse-beta setting of the room-temperature monoclinic structure.

## Evidence and refinement

The ZnO + WO3 precursor chemistry limits the expected elements to Zn, W, and O. The dominant reflections at about 19.0°, 23.9/24.6°, 30.6°, 36.5°, 38.5°, and 41.4° 2theta form the characteristic P 2/c ZnWO4 wolframite pattern. Residual peak families require both wurtzite ZnO and monoclinic WO3. In initial structure screens, ZnWO4 alone gave Rwp about 22%; adding only ZnO remained above 21%, adding only WO3 reduced it to about 15.7%, and the three-phase model was best before detailed refinement. Cubic ZnO, triclinic ZnWO4, and alternative WO3 candidates were inferior or less stable in constrained refinements.

GSAS-II refinement used the full 9.9034–100.0949° range and the stated Cu Kalpha1/Kalpha2 doublet. Refined terms included phase scales and cells, crystallite-size broadening, WO3 microstrain, background, axial divergence, surface roughness, polarization, and selected atomic coordinates. The ZnWO4 [001] March-Dollase ratio is 0.9867, indicating only marginal preferred orientation. The final native forward replay gives Rwp = 6.1982%, Rp = 4.7754%, Rexp = 3.7916%, and chi-square = 22182.46 for 8301 points. Replay regenerated structure factors and reflection lists from `final.gpx`; it exactly reproduced `fit.csv`, retained a positive background, and raised no physical-profile warnings.

## Remaining uncertainty

The three phase identities are well supported. Fractions are more model-dependent than counting-statistical errors suggest because phase scales correlate with polarization and surface roughness; an approximate practical uncertainty is 1–2 wt% absolute, and no amorphous fraction can be inferred from these data.

The exact WO3 oxygen coordinates are not determined as reliably as its phase identity, cell, or tungsten framework: oxygen scatters weakly relative to W, and correlated monoclinic WO3 variants fit similarly. ZnO's internal oxygen coordinate and all isotropic displacement parameters were therefore not independently interpreted; Uiso was held at 0.005 Å². The submitted coordinates are a physically screened refinement model, but those light-atom details should not be treated as a unique structure determination from this powder pattern alone.
