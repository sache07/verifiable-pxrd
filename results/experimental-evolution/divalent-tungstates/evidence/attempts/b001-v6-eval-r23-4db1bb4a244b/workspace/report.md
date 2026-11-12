# Quantitative phase analysis

## Result

Four crystalline phases are required. Weight fractions are normalized over those four phases only.

| Phase | Space group | wt% (formal 1σ) | Starting record | Refined CIF |
|---|---:|---:|---:|---|
| PbWO4 (scheelite) | I 41/a | 55.230 ± 0.109 | 9009811 | `phase_1_PbWO4_scheelite.cif` |
| WO3 (ambient monoclinic) | P 1 21/c 1 | 22.661 ± 0.101 | 2311041 | `phase_2_WO3_monoclinic.cif` |
| Pb3O4 (minium) | P 42/m b c | 16.481 ± 0.089 | 9012124 | `phase_3_Pb3O4_minium.cif` |
| PbO (massicot) | P b c m | 5.628 ± 0.078 | 2310433 | `phase_4_PbO_massicot.cif` |

The final full-range replay gives Rwp = 2.6101%, Rp = 1.9955%, Rexp = 2.4853%, GOF = 1.0522, and Durbin–Watson = 1.870.

## Evidence and model

- Scheelite PbWO4 accounts for the broad families at about 27.8, 30.0, 33.1, 47.4, 55.6, and 69.0° 2θ. The 290 K synthetic scheelite record COD 9009811 was physically consistent; monoclinic raspite refined to only 0.011(54) wt% on the final common profile and is not detected.
- Ambient monoclinic WO3 is required by the sharp 23.52/24.01/24.83° triplet and many sharp mid/high-angle lines. COD 2311041 is the neutron structure in the alternative P21/c cell and fit better than the older exact record.
- Tetragonal Pb3O4 (minium) is supported by broad families including those near 31.2, 32.5, 52.5, and 63.7°. The selected record is the 293 K synthetic structure COD 9012124.
- Orthorhombic PbO (massicot) is supported by coherent families near 30.8, 33.0, 45.5, and higher angles. Tetragonal litharge collapsed to the scale lower bound and is not detected.

The metadata Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio were fixed. The baseline uses a six-term smooth Chebyshev background, one specimen-displacement correction (-729.3 µm in the GSAS-II convention), a shared interior polarization coefficient (0.8350), and positive U/W/X = 41.750/5.391/5.456; V/Y/Z, roughness, transparency, and texture remain neutral. SH/L stayed at its minimal fixed value because repeated low-angle asymmetry was absent.

Isolated low-, middle-, and high-angle families support size-dominated broadening for PbWO4 (0.0628 µm), size plus strain for Pb3O4 (0.0683 µm and 7293 ppm), and strain-dominated broadening for PbO (10289 ppm). WO3 needed no phase-width term. Shared isotropic displacement terms were supported for WO3 (0.01512 Å²) and PbO (0.00772 Å²); PbWO4 and Pb3O4 displacement trials went to zero and were pruned. Five symmetry-distinct PbWO4 texture tests returned March–Dollase ratios 0.992–1.002 and were rejected.

The exported structures also pass a nearest-neighbour geometry screen: shortest W–O contacts are 1.71–1.77 Å and shortest Pb–O contacts are 2.13–2.61 Å, with no unphysical short contacts.

## Remaining uncertainty

The phase identities are well constrained by multiple coherent reflection families. The tabulated fraction uncertainties are covariance-only values and are smaller than the true accuracy: no pointwise uncertainties or calibrated instrument profile were supplied, so Poisson weights and a jointly refined common profile were used. Accepted/pruned intensity-model variants moved the major-phase fractions by roughly 1–2 wt% absolute; that is a more realistic systematic scale than the formal errors. The minor PbO amount is less secure than the three major fractions, though its orthorhombic identity is supported.

Atomic coordinates were retained from the cited records; cells, scales, common profile, selected broadening terms, polarization, and the two supported shared Uiso terms were refined. No amorphous fraction can be inferred from this normalization. Additional phases below roughly 0.15 wt% (about the 3σ raspite challenge level) cannot be excluded reliably.
