# PXRD phase analysis

## Result

The pattern is best described by five crystalline contributions. Fractions are normalized to the modeled crystalline material; amorphous content cannot be measured without an internal standard.

| Phase | Structural model | Weight % | Assessment |
|---|---|---:|---|
| PbWO4 | scheelite, I41/a (COD 9009811) | 63.55 ± 0.24 | well supported |
| WO3 | monoclinic, P21/c (COD 2311041) | 10.61 ± 0.19 | well supported |
| PbO | massicot, Pbcm (COD 2310433) | 6.69 ± 0.13 | well supported |
| Pb2WO5 | C2/m Pb2MoO5 prototype (COD 7220560), Mo replaced by W | 16.56 ± 0.21 | provisional structure |
| Pb3O4 | minium, P42/mbc (COD 9012124) | 2.59 ± 0.13 | tentative minor phase |

The uncertainties in the table are conditional least-squares ESDs, not total uncertainties. Inventory and source-model uncertainty is appreciably larger for Pb2WO5 and Pb3O4.

## Evidence

The PbO + WO3 precursor context and 500 °C treatment are consistent with dominant scheelite PbWO4, residual precursors, and a lead-rich tungstate intermediate. Coherent families accounted for by the final model include PbWO4 near 27.67, 33.03, 45.00, 47.27, 51.46, 55.52, 56.80, and 72.27° 2θ; the diagnostic monoclinic WO3 group at 23.36, 23.85, and 24.63°; and massicot PbO peaks near 29.35, 30.55, 38.07, 53.31, 56.30, and 60.52°.

No exact Pb2WO5 record was present in the screened database subset. A stoichiometric-analogue search selected C2/m Pb2MoO5 as the closest physical parent. Replacing Mo by W accounts for a recurring family near 25.89, 31.03, 43.37, 50.93, 59.65, and 64.32° and lowered the common-profile Rwp from about 17.5% to 14.7% before later profile improvements. Its refined geometry remains physical: tetrahedral W–O distances are 1.766–1.793 Å. A Pb2CrO5 parent gave a materially worse fit and implausibly short starting W–O geometry.

Weak residual families near 31.41, 45.96, 48.33, 52.33, 57.29/57.96, and 63.04° support an ambient tetragonal minium contribution. Removing it increases Rwp from 12.95% to 13.25%. Its evidence is nevertheless modest and overlap-sensitive.

Competing records were explicitly revisited under a common restrained profile. Raspite PbWO4 refined to essentially zero scale; defect-scheelite Pb7W8O28.8 was collinear and unstable; litharge PbO was worse than massicot; and a low-temperature orthorhombic Pb3O4 record was worse than ambient tetragonal minium. A triclinic WO3 model improved Rwp by only 0.016 percentage point while adding lower-symmetry freedom, so the standard room-temperature monoclinic model was retained. All exported CIFs parse with the stated compositions and space groups, and their short-contact geometry is physically plausible.

## Refinement and fit quality

GSAS-II refinement used all 8,282 points from 10.0094 to 99.9944° with the reported Cu Kα1/Kα2 wavelengths and fixed Kα2/Kα1 ratio 0.5. Atomic coordinates and displacement parameters were retained from the screened source structures; scales and unit cells were refined. The common baseline comprises an eight-term smooth Chebyshev background, one zero correction, nonnegative W/X profile terms, polarization, and one SH/L asymmetry term. U repeatedly reached its physical lower bound and was fixed at zero; unused V/Y/Z, phase strain, phase broadening, extinction, specimen shift/transparency, and roughness terms were neutralized.

Phase-by-phase size and strain trials either reached bounds, gave negligible improvement, or acted as fraction surrogates and were rejected. Axis challenges supported only [100] March–Dollase terms for massicot PbO (0.8653) and the Pb2WO5 analogue (1.2313); texture terms for the other phases were unsupported. The selected model was saved, reopened, and replayed over the complete range before export.

Final statistics are Rwp = 12.952%, Rp = 8.750%, Rb = 10.455%, expected Rwp = 3.502%, and GOF = 3.707 (35 variables, 8,282 observations). Because pointwise uncertainties were not supplied, these statistics use counting-statistical weights inferred from the measured counts. The low Durbin–Watson value (0.167) and structured residuals show that systematic profile/intensity mismatch remains, so the formal ESDs should not be read as full accuracy estimates.

The Pb2WO5 formula/structure cannot be established uniquely from this powder pattern: its 16.56 wt% value is conditional on the substituted prototype. The Pb3O4 result is also not quantitatively reliable at the formal-ESD level: fixing its ambient literature cell gives Rwp = 13.13% and 1.70 wt%, versus 2.59 wt% with its cell refined. It should therefore be treated as a roughly 2 wt% tentative contribution. No further candidate produced a replay-stable positive scale supported by coherent independent reflections.
