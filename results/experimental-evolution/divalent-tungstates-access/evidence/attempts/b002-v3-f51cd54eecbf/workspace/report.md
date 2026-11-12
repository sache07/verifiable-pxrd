# Powder XRD phase analysis

The crystalline pattern is modeled by four phases, normalized to 100 wt% of the modeled crystalline material:

| Phase | Space group | Weight fraction | Assessment |
|---|---:|---:|---|
| MnWO4, wolframite | P 2/c | 61.07 wt% | Secure major phase |
| WO3, monoclinic | P 21/c | 22.08 wt% | Secure residual precursor |
| Mn2WO6 | P 21/c | 13.84 wt% | Provisional structure/composition assignment |
| Mn3O4, hausmannite | I 41/a m d | 3.02 wt% | Weak but supported residual precursor |

The formal GSAS-II scale-factor uncertainties are 0.26, 0.15, 0.17, and 0.30 wt percentage points, respectively. These are counting-statistical refinement uncertainties only. They exclude model choice, peak overlap, preferred orientation, and profile-systematic errors; the Mn2WO6 and Mn3O4 fractions are therefore not reliable at that formal precision. No amorphous content was measured, so the values must not be interpreted as absolute bulk fractions if amorphous material is present.

## Evidence

The dominant peak set and its refined monoclinic cell (a = 4.79775, b = 5.70428, c = 4.97317 A, beta = 91.1078 degrees) match wolframite MnWO4. A second extensive family matches monoclinic WO3 (a = 7.29808, b = 7.53976, c = 10.51487 A, beta = 133.027 degrees), consistent with the stated WO3 precursor.

After those phases were fitted, a coherent family at approximately 19.86, 25.43, 31.78, 35.09, 46.48, and 56.48 degrees 2-theta remained. It is indexed by a P 21/c cell refined to a = 4.02895, b = 6.98030, c = 6.16944 A, beta = 110.629 degrees. A reaction-plausible Mn2WO6 model accounts for this family. Competing tetragonal and orthorhombic frameworks and ordinary Mn/W oxide references did not close the family comparably. Multiple physical direct-space coordinate starts were treated with comparable cell, scale, texture, and profile refinement. The retained model has no short contacts (minimum O-O 1.87 A; shortest Mn-O 1.73 A), whereas lower-residual unconstrained oxygen solutions generated impossible contacts and were rolled back.

The remaining isolated intensity near 32.48 degrees is accounted for by tetragonal hausmannite Mn3O4. Its scale remains positive and significant in the complete four-phase refinement. Mn2O3 and orthorhombic Mn3O4 controls collapsed toward zero scale when their clean reference cells were retained. No coherent unassigned reflection family remains after the four accepted phases are included.

## Fit and limitations

Independent full-grid regeneration from `final.gpx` gives Rwp = 12.570%, Rp = 7.287%, and goodness of fit = 6.316 over 8301 points. The replay produced no negative-background, peak-width, or displacement-parameter warnings. `fit.csv` contains observed, freshly calculated, and observed-minus-calculated intensities on the complete original grid.

The P 21/c Mn2WO6 assignment is the principal uncertainty. Its indexed reflection family is real, but broad overlapping peaks, boundary broadening/texture parameters, and weak oxygen scattering prevent a unique determination of its light-atom arrangement; the submitted CIF is a physically screened provisional model, not a definitive structure solution. The weak Mn3O4 abundance is likewise model-sensitive. Residual errors at already indexed peaks are attributed to remaining intensity/profile imperfections rather than evidence for another phase.
