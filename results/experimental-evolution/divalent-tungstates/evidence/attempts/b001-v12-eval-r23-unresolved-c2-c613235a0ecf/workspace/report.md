# Phase analysis and quantitative refinement

The pattern is described by four crystalline phases. Weight fractions are normalized over these phases only.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| PbWO4, scheelite | I41/a, COD 9009811 | 0.58618(15) |
| WO3, monoclinic | P21/n (No. 14), COD 1528915 | 0.21674(11) |
| Pb3O4, tetragonal | P42/mbc, COD 1537983 | 0.14831(14) |
| PbO, orthorhombic massicot | Pbcm, COD 2310433 | 0.04877(9) |

## Evidence

Scheelite PbWO4 accounts for the dominant families at 27.81, 30.03, 33.15, 45.11, 47.37, 51.57, 55.61, and 72.34 degrees 2theta. Monoclinic WO3 is required by the resolved 23.54/24.02/24.85 degree triplet and independent higher-angle families near 33.68, 34.05/34.52, 47.63/48.66, and 50.43 degrees. Pb3O4 has independent families at 26.81, 31.22, 32.54, 50.25, 52.51, 56.43, and 63.70 degrees. Orthorhombic PbO is supported by families near 29.53/30.82, 38.25, 45.56, 51.17, and 60.72 degrees. Its scale remained positive and replay-stable; removing PbO and reconverging increased Rwp from 3.94% to 5.15%.

Exact-formula alternatives were challenged at common checkpoints. The second scheelite PbWO4 record (COD 1527935) and monoclinic PbWO4 were worse than COD 9009811. Alternate monoclinic, triclinic, and orthorhombic WO3 records were worse or drove profile terms to bounds. Tetragonal Pb3O4 clearly beat its orthorhombic competitor (inventory-stage Rwp 8.29% versus 9.73%), while tetragonal PbO collapsed to zero scale and orthorhombic PbO remained stable. A partially occupied Pb7W8O28.8 record gave only a marginal inventory-stage change (Rwp 9.861% versus 9.867% for stoichiometric PbWO4), without independent superstructure evidence, and was rejected. No coherent unmatched families remained to justify a non-1:1 analogue. The refined phase amounts imply Pb:W about 0.97:1, consistent with near-equimolar Pb/W closure, but metadata supplied no precursor quantities to impose as a constraint.

## Refinement and fit quality

The final GSAS-II replay used the complete 9.9034-100.0946 degree range, the reported Cu Kalpha1/Kalpha2 wavelengths and fixed 0.5 Kalpha2/Kalpha1 ratio, a smooth 12-coefficient Chebyshev background, one zero correction, common W broadening, axial SH/L, and one surface-roughness term. Supported phase terms were isotropic size for PbWO4 and Pb3O4, isotropic strain for WO3, [010] uniaxial strain for PbO, and low-index March-Dollase corrections for WO3 [001] and Pb3O4 [211]. Unsupported size/strain, polarization, extra roughness, and texture terms were pruned. Three complete-range replays converged with no frozen or bound variables and unchanged fractions.

Final statistics are Rwp = 3.936%, Rp = 2.910%, Rexp = 2.485%, GOF = 1.587, and chi-square = 20823.1 for 8301 points and 38 refined variables. An isolated-line audit also supports the retained profile: observed/calculated peak positions and FWHM were 27.811/27.811 and 0.248/0.251 degrees at low angle, 45.132/45.121 and 0.322/0.310 degrees at middle angle, and 72.364/72.353 and 0.434/0.447 degrees at high angle. Corresponding observed versus calculated left/right half-widths were 0.119/0.130 versus 0.120/0.131, 0.145/0.177 versus 0.130/0.180, and 0.168/0.265 versus 0.164/0.283 degrees.

All retained source and final CIFs were screened with `learned/cif_health.py`. Final PbWO4 and PbO pass. WO3 and Pb3O4 are flagged for review, not failure, because their ordered source coordinates contain short O-O contacts (1.578 and 1.794 angstrom, respectively); neither has hard contacts, invalid occupancy, or partial sites. The health tool reports the standard P21/c setting for the exported P21/n WO3 model; both are settings of space-group No. 14. Better-health alternate WO3/Pb3O4 polymorph records did not reproduce the observed peak positions and splittings.

## Remaining uncertainty

The parent atomic coordinates were retained and only unit cells, scales, and profile/intensity terms were refined, so the CIFs are phase models rather than independent atom-level structure solutions. The parenthetical fraction errors are conditional GSAS-II covariance estimates; realistic errors are larger because preferred orientation, surface roughness, absorption, and source-model systematics are not fully represented. No point uncertainties were supplied, so Poisson estimates (`sigma = sqrt(counts)`) were used. Fractions therefore should be regarded as approximately percent-level in absolute accuracy, especially for the 4.9 wt% PbO phase. They are normalized crystalline fractions: amorphous material and trace phases below the pattern's practical detection limit cannot be quantified without an internal standard.
