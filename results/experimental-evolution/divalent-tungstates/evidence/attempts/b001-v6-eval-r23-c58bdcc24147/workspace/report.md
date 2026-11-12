# Phase analysis and Rietveld refinement

## Result

The modeled crystalline product contains three phases. Fractions are normalized only over these crystalline phases; no amorphous fraction can be obtained from this dataset.

| Phase | Space group | Weight fraction | Refined cell |
|---|---:|---:|---|
| MnWO4 (wolframite) | P 2/c (No. 13) | 74.83(28)% | a = 4.79940 Å, b = 5.70743 Å, c = 4.97618 Å, beta = 91.1257° |
| WO3 | P 21/c (No. 14) | 19.67(19)% | a = 7.69007 Å, b = 7.55227 Å, c = 10.51540 Å, beta = 136.0241° (nonstandard but valid setting) |
| Mn3O4 (hausmannite) | I 41/a m d (No. 141) | 5.50(27)% | a = 5.76611 Å, c = 9.50785 Å |

The final full-range fit has Rwp = 7.7118%, Rp = 5.1349%, Rexp = 2.4903%, and GOF = 3.1028. The saved/reopened project converged with maximum shift/esd = 0.0013.

## Evidence and model selection

The precursor context (WO3 + Mn3O4 heated at 700 °C) and the dominant families at approximately 15.1, 18.1, 23.3, and the split 29.6/30.0° pair identify a wolframite-type divalent tungstate. No exact MnWO4 entry was present in the supplied index, so `learned/stoichiometric_analogues.py` was used. FeWO4, ZnWO4, and MgWO4 parents were physically screened. The ZnWO4 structure (COD 1520641) with Mn substituted for Zn gave the correct P 2/c topology; refinement replayed from independent ZnWO4 and MgWO4 coordinate starts to the same minimum. The refined octahedra remain physical: Mn–O = 2.051–2.186 Å and W–O = 1.820–2.154 Å, with full occupancy and no modeled disorder.

Residual families near 22.7–23.9, 32.8–33.7, 41.45, and 46.83° require WO3. Under the final common profile, monoclinic P 21/c WO3 (COD 2311041) is both simpler and better than the triclinic alternative: Rwp = 7.7118% versus 7.7414%, while the triclinic angles drifted toward 90° on disk replay. A different physical monoclinic coordinate record (COD 1528915) gave Rwp = 7.9533%, showing why an individual poor record did not justify rejecting the phase. The WO3 peaks require one replay-stable isotropic Lorentzian size term, 75.7(2.5) nm; microstrain alone fit worse, and the combined model did not support an independent strain term.

Weak families including 31.77, 43.98, 50.09, 58.08, and 59.32° support residual hausmannite Mn3O4, which is also chemically plausible as unreacted precursor. Removing it and reconverging the remaining model raises Rwp from 7.7118% to 7.8809%. MnO and Mn3WO6 scales collapsed to zero in watch-list tests, and Mn2O3 produced no coherent multi-family improvement.

## Refinement baseline

All 8,301 measured points from 9.9034 to 100.0946° 2theta were used. Cu Kalpha1/Kalpha2 wavelengths and the reported 0.5 intensity ratio were fixed to the metadata values. Since pointwise uncertainties were absent, sigma = sqrt(counts) was used. The shared baseline contains a smooth six-coefficient Chebyshev background, refined effective polarization (0.9126), nonnegative W/X profile terms, and SH/L axial asymmetry. One reflection-geometry specimen-displacement correction was used; the refined 787 µm value should be regarded as an effective sample-height/instrument offset because no calibrant was supplied. A zero-only alternative failed physical replay.

Unused roughness, transparency, extinction, texture, and MnWO4/Mn3O4 size/strain terms are neutral and fixed. U refined to its zero bound. Symmetry-distinct texture axes gave small, axis-ambiguous gains, while uniaxial size/strain trials were bound-hit, singular, or replay-unstable, so none were retained. Only MnWO4 atomic coordinates were refined; the broad WO3 and weak Mn3O4 data do not determine their atomic coordinates reliably, so those coordinates remain at their selected parent-record values.

## Remaining uncertainty

Parenthesized fraction errors are GSAS-II covariance estimates, not total uncertainties. The GOF above unity and residual low-angle peak-center/shape trends (up to about 0.04° at the lowest isolated MnWO4 families) show remaining instrumental/profile systematics. Cell and coordinate errors are therefore likely larger than their formal values.

The Mn3O4 phase assignment is supported, but its exact fraction is less reliable than the formal 0.27% error. Allowing an extreme broadening model moved it toward 9 wt%, but required roughly 1.4% microstrain and multi-degree high-angle FWHM, acting as a background surrogate; it was rejected. A realistic systematic statement is therefore approximately 5–9 wt% Mn3O4, with 5.50 wt% reported for the physically restrained model. WO3 symmetry and approximate fraction are reliable, but its detailed atomic structure is not uniquely determined by these broad, overlapping peaks. Any amorphous or unidentified content is outside the reported normalization.
