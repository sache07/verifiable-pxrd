# Powder XRD phase analysis

## Result

The crystalline specimen is modeled as zinc tungstate plus residual unreacted oxides. Fractions are normalized over the modeled crystalline phases only.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| ZnWO4 | wolframite, `P 2/c`, COD 1520641 | 0.7424 (74.24 wt%) |
| WO3 | monoclinic, `P 21/c`, COD 2311041 | 0.2028 (20.28 wt%) |
| ZnO | wurtzite, `P 63 m c`, COD 9004178 | 0.0548 (5.48 wt%) |

The final full-grid fit has Rwp = 6.9609%, Rp = 5.4351%, Rexp = 3.7916%, and GOF = 1.8371 for 8,301 observations. The submitted `final.gpx` reproduces these values; `fit.csv` is exported directly from its observed and calculated arrays.

## Evidence and model selection

The precursor metadata (WO3 + ZnO, 900 °C) supports ZnWO4 formation with residual starting oxides. The dominant reflection family is indexed by monoclinic wolframite ZnWO4. Distinct residual families, including the characteristic wurtzite ZnO group near 31.8–36.3° 2theta and higher-angle ZnO lines, require ZnO; the remaining low-angle and mid-angle family is indexed by monoclinic WO3. All three refined scales are positive, and no coherent residual reflection family remains after the three-phase model. Converting the refined phase masses to metal moles gives Zn/W about 0.94, reasonably close to the nominal 1:1 precursor ratio given the quantitative uncertainties.

For WO3, exact-composition monoclinic references gave close profile fits. COD 2311041 was selected because it retains physical geometry, whereas the close numerical alternative COD 1528915 contained an implausibly short O–O contact. The exported structures have minimum relevant distances of W–O 1.865 Å, Zn–O 1.974 Å, and O–O 2.523 Å for ZnWO4; W–O 1.738 Å and O–O 2.513 Å for WO3; and Zn–O 1.974 Å for ZnO. The large beta angle in the WO3 CIF is a valid nonconventional `P 21/c` setting.

Refinement used bounded, replay-checked changes: scales/background; cells with calibration alternation; small heavy-atom and bounded oxygen-coordinate moves; then polarization, surface roughness, weak March–Dollase texture, isotropic displacement parameters, and phase sizes. Nonphysical coordinate, strain, and simultaneously refined zero/height branches were rolled back. The final cells are ZnWO4 `a=4.69089, b=5.71876, c=4.92643 Å, beta=90.6302°`; WO3 `a=7.69309, b=7.53559, c=10.53020 Å, beta=136.0849°`; and ZnO `a=3.24948, c=5.20816 Å`.

## Remaining uncertainty

Phase identification and topology are reliable, but the fractions should not be interpreted at the last reported decimal. Profile, thermal-factor, texture, and surface-roughness terms are correlated, several instrument/specimen terms lie at their allowed bounds, and zero offset and specimen height cannot be determined independently. Reasonable bounded model perturbations suggest practical crystalline-phase uncertainties of about ±1 wt% for ZnWO4 and WO3 and ±0.5 wt% for ZnO. The minor ZnO phase has only 16 contributing reflections, so its exact fraction, size, and displacement parameter are the least certain. A concise defensible composition is therefore approximately 74(1) wt% ZnWO4, 20(1) wt% WO3, and 5.5(5) wt% ZnO.

The atomic topologies are determined, but the refined coordinates and displacement parameters—especially for minor ZnO and residual WO3—are not high-precision single-crystal structure determinations. Rwp remains above Rexp, with residual profile/intensity mismatch concentrated in overlapping and high-angle regions. No amorphous content can be quantified from this normalization, and any amorphous or extremely poorly crystalline material is excluded from the reported fractions.
