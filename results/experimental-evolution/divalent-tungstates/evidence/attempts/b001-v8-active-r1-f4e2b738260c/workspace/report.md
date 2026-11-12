# Quantitative phase analysis

## Result

The pattern is modeled with five crystalline phases. Fractions are normalized over those modeled crystalline phases; they do not measure amorphous material.

| Phase | Space group | Weight fraction | Structural confidence |
|---|---:|---:|---|
| PbWO4, scheelite | I4_1/a | 54.32 wt% | High |
| WO3, monoclinic | P2_1/c | 23.29 wt% | High |
| Pb3O4, minium | P4_2/mbc | 17.71 wt% | High |
| PbO, massicot | Pbcm | 3.33 wt% | High |
| Pb3WO6-like | Pnma | 1.35 wt% | Tentative analogue |

The final full-range, reopened-project replay gives Rwp = 2.9948%, Rp = 2.2931%, Rexp = 2.4853%, and GOF = 1.2079 for 8,301 observations and 40 refined variables. The formal GSAS-II fraction standard uncertainties are recorded in `result.json`, but they exclude model selection, microabsorption, and structural-systematic uncertainty.

## Evidence and model selection

The dominant line families identify scheelite PbWO4 (including 27.81, 30.02, 33.16, 45.13, and 47.37 degrees 2theta), monoclinic WO3 (the 23.53/24.02/24.85 degree triplet and its higher-angle families), and tetragonal Pb3O4 (26.81, 31.22, 32.55, 50.38, and 52.52 degrees). Orthorhombic massicot accounts for a strong coherent residual family led by about 29.52 degrees, with corroborating lines near 30.80, 38.27, 53.59, and 56.40 degrees.

The retained source models were COD 9009811 (PbWO4), 2311041 (WO3), 9012124 (Pb3O4), and 2310433 (massicot). Competing records/polymorphs were fitted one at a time under the same nuisance model. Alternate scheelite and WO3 records fitted worse; monoclinic PbWO4 was grossly incompatible; orthorhombic Pb3O4 was slightly worse; tetragonal PbO, Pb2WO5, and cubic Pb3WO6 analogues refined to zero scale.

After balancing Pb/W/O and searching charge-balanced non-1:1 products, a Pnma Pb3WO6 model was adapted by W-for-U substitution in the physical UPb3O6 analogue COD 2310493. It matches independent positive residuals, especially the family near 29.31 degrees, and lowers Rwp from 3.0778% for the converged four-phase model to 2.9948%. The approximate BIC change is -417 despite four added scale/cell variables, so a weak extra phase is supported. However, no exact Pb3WO6 record was available and its atomic coordinates were not refined. Its exact structure therefore cannot be determined reliably from this pattern. The submitted 1.35 wt% is model-dependent: fixing its Uiso between 0.005 and 0.050 A^2 changed the fraction from about 1.27 to 1.92 wt%; freeing Uiso drove it to a bound and was rejected as overfitting. Treat this phase as Pb3WO6-like and its fraction as semiquantitative.

A disordered Pb7W8O28.8 record remained at about 0.6 wt% on re-challenge, but its strongest calculated line lies on a negative residual, the model has extensive partial occupancy, and the small fit gain was not complementary. It was not retained.

## Profile and physical checks

The Cu K-alpha doublet and reported K-alpha2/K-alpha1 ratio of 0.5 were used. The accepted model has a common zero correction of +0.44140 degrees and a nonnegative W/X profile. U, V, Y, Z, strain, roughness, texture, and excess asymmetry were neutralized; only isotropic size broadening for PbWO4 (about 65 nm) and Pb3O4 (about 34 nm) survived replay. Polarization was fixed at its physical upper value of 1.0. Size-versus-strain, roughness, texture, alternate-source, and extra-phase causes were tested from saved baselines; bound or non-replay-stable terms were pruned.

Representative observed/calculated checks were: WO3 at 23.530/23.541 degrees with FWHM 0.131/0.143 degrees; PbWO4 at 27.811/27.811 with FWHM 0.250/0.256; PbWO4 at 45.132/45.121 with FWHM 0.323/0.315; and PbWO4 at 86.012/86.012 with FWHM 0.539/0.520. High-angle left/right half-widths at 86 degrees were 0.168/0.371 observed and 0.160/0.361 calculated. The residual mismatch is modest but explains the GOF above one.

All final CIFs pass `learned/cif_health.py` with full occupancies and no hard contacts. The tentative Pnma model has W-O distances of 1.892-2.182 A and Pb-O distances of 2.175-3.176 A; bond-valence assignment gives W(VI), Pb(II), and O(-II). The modeled bulk Pb/W molar ratio is 0.977. Back-calculation to WO3 + Pb3O4 implies about 0.74 wt% O2 loss per gram of crystalline product, chemically consistent with partial Pb3O4 reduction at 500 C. No amorphous fraction or crystalline phase below the pattern's practical detection limit can be quantified reliably.
