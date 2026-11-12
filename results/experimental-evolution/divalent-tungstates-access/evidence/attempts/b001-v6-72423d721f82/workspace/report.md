# Powder XRD phase analysis

The 800 °C product from Mn3O4 and WO3 is a three-phase crystalline mixture. Weight fractions are normalized over these modeled crystalline phases; amorphous material, if present, is not quantified.

| Phase | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| MnWO4, wolframite | P 2/c | 0.69994 (69.99 wt%) | a=4.79447, b=5.70878, c=4.97690, β=91.1264 |
| Mn3WO6 | R -3 | 0.14679 (14.68 wt%) | a=8.88973, c=10.45694 |
| WO3, monoclinic | P 21/n | 0.15327 (15.33 wt%) | a=7.30008, b=7.53701, c=7.69023, β=90.8827 |

The full 9.9034–100.0946° 2θ grid gives Rwp=2.5098%, Rp=1.9230%, and goodness-of-fit=1.4161 (8301 observations). The saved `final.gpx`, CIFs, fractions, and `fit.csv` all come from this same replayable state.

## Evidence and model choice

Wolframite MnWO4 accounts for the dominant families near 15.9, 18.9, 24.1/24.6, and 30.4/30.8° and was modeled from the exact-composition COD 1520200 structure. A coherent second family at about 20.0/20.5, 28.8, 31.9, 35.3, 45.9/46.7, 54–57, and 66–68° requires rhombohedral Mn3WO6. Its model uses the isovalent Te(VI)→W(VI) substitution in the R -3 Mn3TeO6 topology (COD 2211528), followed by bounded cell and coordinate refinement. Residual precursor peaks around 23.5–24.7 and 33.7–34.5° require monoclinic WO3.

The supplied staged coordinate polish was run once. Its original WO3 parent (COD 1528915) was rejected during review because it contains a nonphysical 1.58 Å O–O contact. The equivalent exact-composition neutron structure COD 2311041 was used instead; this both restored physical geometry and materially improved the fit. Final minimum contacts are chemically ordinary: Mn3WO6 has W–O ≥1.896 Å and O–O ≥2.597 Å; MnWO4 has W–O ≥1.758 Å and O–O ≥2.429 Å; WO3 has W–O ≥1.714 Å and O–O ≥2.539 Å. No additional coherent reflection family remains, and an extra Pbcn Mn2WO6 prototype was not supported.

## Remaining uncertainty

The Mn3WO6 phase identity and reflection family are well supported, but its detailed oxygen coordinates are less secure than those of the exact-reference phases because the starting topology is cross-chemistry-derived and this is a minority, overlapping phase. The WO3 isotropic microstrain reached the calibrated 8000 ppm ceiling, so its size/strain separation is not reliable. Weak preferred-orientation, anisotropic-strain, and surface-roughness branches were rejected after they collapsed to unity/isotropic/lower-bound values.

The quoted fraction e.s.d.s in `result.json` are conditional least-squares errors and are much smaller than likely systematic uncertainty from profile overlap, reference coordinates, and calibration. The relative crystalline fractions are stable, but they should not be interpreted as an absolute bulk assay or as evidence that no amorphous component exists.
