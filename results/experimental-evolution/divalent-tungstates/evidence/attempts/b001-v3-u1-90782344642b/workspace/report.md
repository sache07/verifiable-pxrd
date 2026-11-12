# PXRD phase analysis

## Result

The crystalline product is a three-phase mixture:

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| ZnWO4, wolframite | P 2/c, COD 1520641 | 0.73135 (73.14 wt%) |
| ZnO, wurtzite | P 63 m c, COD 9004178 | 0.08450 (8.45 wt%) |
| WO3, room-temperature monoclinic | P 21/c, COD 2311041 | 0.18415 (18.42 wt%) |

Fractions are normalized over these modeled crystalline phases. Formal least-squares uncertainties are 0.15, 0.13, and 0.11 weight-percentage points, respectively, but these do not include specimen and model systematics.

The final fit over the nominal 10–100° 2θ range has Rwp = 2.9083%, Rp = 2.2875%, GOF = 1.0540, and Durbin–Watson = 1.8515 for 8,284 observations and 40 variables. A final project reopen/replay converged with no SVD zeros or frozen variables and a maximum shift/ESD of 0.00073.

## Evidence and model selection

The phase inventory is chemically consistent with reaction of the reported ZnO and WO3 precursors at 600 °C: wolframite ZnWO4 is the dominant product, with both precursors remaining. Independent diagnostic families include ZnWO4 peaks near 15.53, 18.90, 30.44/30.68, 38.31, 41.29, 51.70, and 61.63°; wurtzite ZnO peaks near 31.79, 34.46, 47.59, 56.59, 62.90, and 67.97°; and the characteristic monoclinic WO3 multiplets around 23–24.5 and 33–34.2°.

All selected records have the exact occupied composition, full occupancies, no mixed sites, and physically reasonable geometry. COD 1520641 is an ambient-temperature single-crystal wolframite model; COD 9004178 is ambient wurtzite ZnO; COD 2311041 is the established neutron-derived monoclinic WO3 model. Two nominal “ZnWO4” triclinic records were rejected because their occupied sites contain Cu/Zn solid solutions. High-pressure rocksalt and thin-film cubic ZnO records were also rejected. WO3 records with incompatible source conditions or sub-ångström/very short contacts were excluded before fitting.

Physically valid WO3 alternatives were compared with the same preliminary three-phase profile schedule and diagnostic windows. P 21/c COD 2311041 gave Rwp 3.6789%; triclinic P-1 COD 2106293 gave 3.7155% despite three extra cell degrees of freedom; and orthorhombic Pnma COD 2107312 gave 5.2753% with clear multiplet mismatch. No analogue substitution was needed.

Cu Kα1/Kα2 wavelengths of 1.540598/1.544426 Å and the reported 0.5 intensity ratio were used. Because pointwise uncertainties were absent, Poisson weights, σ = sqrt(counts), were assumed. The final model uses a 12-term Chebyshev background, all phase scales and cells, one common zero correction, refined polarization, and a nonnegative common U/W/X profile. Specimen displacement was worse than zero correction. Roughness sought an unphysical negative coefficient with 99.95% internal correlation; SH/L was unstable and 97% correlated with zero; and both were rejected. Texture-axis trials produced near-unity March–Dollase ratios and improved one family while worsening others, so no preferred orientation was retained.

Supported phase broadening is an effective isotropic ZnWO4 size of 0.0775 µm and isotropic WO3 microstrain of 3,550 µstrain. ZnO broadening returned to the 10 µm neutral limit or negative strain and was removed. Removing U, polarization, ZnWO4 size, or WO3 strain from the final structural model raised Rwp to 2.927%, 3.076%, 3.296%, and 3.030%, respectively. The broadening values correlate with the common profile and should not be treated as independent microstructural measurements.

ZnWO4 coordinates were supported by the data and refined without dominant coordinate correlations. The exported geometry remains physical: W–O = 1.810–2.173 Å, Zn–O = 1.998–2.165 Å, and shortest O–O = 2.560 Å. ZnO and WO3 internal coordinates were retained from their source structures. In particular, a ZnO O-z trial gave only a 0.0044-point Rwp gain while distorting Zn–O bonds to 1.899/2.004 Å, so that coordinate is not reliably determined here.

## Remaining uncertainty

No coherent unmodeled peak family remains: the largest positive standardized residuals at about 23.62 and 34.19° coincide with modeled WO3 reflections, and no comparably strong residual maximum lies more than 0.15° from a significant modeled reflection. Trace crystalline phases below the pattern's detection limit cannot be excluded.

The phase identities are high-confidence, but absolute fractions are less certain than their formal covariance errors. There is no internal standard, calibrated instrumental profile, or independent absorption/microabsorption correction, and amorphous material cannot be quantified. A practical uncertainty of a few absolute weight-percent is therefore more realistic than the formal errors. The crystalline inventory corresponds to an overall Zn/W molar ratio of about 1.08 if no amorphous phase or volatilization is assumed, which is plausible for a mildly Zn-rich feed but is not an independent composition measurement.

The submitted CIFs, fractions, and `fit.csv` were all exported from `final.gpx` after the final native replay.
