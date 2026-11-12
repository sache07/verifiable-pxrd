# Powder diffraction phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized over the modeled crystalline phases; they do not measure amorphous material.

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| SrWO4 (scheelite) | adapted from EuWO4, COD 1561850, *I* 41/*a* | 61.79 wt% |
| WO3 (monoclinic) | COD 2311041, *P* 21/*c* | 23.46 wt% |
| SrCO3 (strontianite) | COD 9008198, *P n m a* | 14.75 wt% |

The final fit has Rwp = 3.796%, Rp = 2.845%, expected Rwp = 2.861%, and GOF = 1.329 for 8301 observations and 25 refined variables. The exact fractions and statistics are in `result.json`.

## Evidence and model selection

The dominant scheelite phase is established by its diagnostic reflections near 17.46, 27.20, 32.64, 44.83, 47.14, and 55.53 degrees 2theta. Coherent residual families near 22.51/22.94/23.83 degrees and 24.65/25.30 degrees identify monoclinic WO3 and orthorhombic SrCO3, respectively. Starting from SrWO4 alone gave Rwp = 12.08%; adding WO3 reduced it to 7.70%, and adding SrCO3 reduced it to 7.27% before the final parent/profile refinements. Carbonate could not replace WO3.

No exact SrWO4 entry was available in the supplied candidate inventory, so cross-chemistry scheelite analogues were inspected before substitution. The selected EuWO4 parent is a clean, room-temperature *I* 41/*a* model with full occupancies; Eu2+ to Sr2+ is an isovalent, closely size-matched substitution. It fitted better under the same modest nuisance model than adapted SrMoO4 and CaWO4 parents. A BaWO4 record with duplicated half-occupied oxygen sites and a 1.17 Angstrom contact, and a high-pressure SrCrO4 record, were rejected. Only the SrWO4 cell was refined: a trial oxygen-coordinate refinement was rejected because its lower residual required distorted coordination. The submitted model retains W-O = 1.769 Angstrom and Sr-O = 2.569-2.599 Angstrom.

For WO3, the selected clean neutron-derived *P* 21/*c* record outperformed tested *P* 21/*n*, *P n m a*, triclinic, and tetragonal alternatives under the same nuisance model. Their respective Rwp values were approximately 7.27%, 7.65%, 7.99%, 8.06%, and 11.69% at that comparison stage. The tetragonal model also required implausible cell compensation. The submitted WO3 geometry has W-O distances of 1.718-2.163 Angstrom. The selected SrCO3 model is fully occupied, gives physical C-O distances of 1.291-1.304 Angstrom, and fits the carbonate-specific reflections; a disordered rhombohedral record was rejected.

A tested Sr3W2O9 fourth phase refined to 0.026(62) wt%, produced no meaningful Rwp improvement, and had an indeterminate cell when released. It was therefore excluded. Remaining prominent residuals occur mainly at reflections already assigned to the three modeled phases rather than as a coherent unmatched peak family.

The chemical balance independently supports the inventory: the residual WO3 and SrCO3 are nearly equimolar, and the total modeled Sr:W molar ratio is approximately 0.996, consistent with incomplete reaction of the stated 1:1 precursors at 650 degrees C.

## Refinement and uncertainty

The GSAS-II model uses the stated Cu Kalpha1/Kalpha2 wavelengths and ratio, a six-term Chebyshev background, and specimen displacement while zero is fixed. Displacement was favored over a separately tested zero-only model (Rwp 3.796% versus 3.825%) and the two correlated corrections were never co-refined. The global U/W/X profile remains nonnegative across the fitted range. Default phase broadening was neutralized before testing: unused microstrain is zero and size is fixed at its large neutral value. Only supported terms were retained: isotropic WO3 microstrain of 4457 ppm and moderate March-Dollase corrections for SrWO4 [110] and WO3 [2 0 -2]. SrWO4 size/strain, SrCO3 broadening, carbonate texture, anisotropic broadening, and atomic-coordinate refinement were not supported. All atomic coordinates and occupancies are fixed in the final model. The final project has no frozen variables, and replay changes Rwp by less than 0.000004 percentage point.

Because the input contains no point uncertainties, Poisson standard deviations estimated from the counts were used. The least-squares fraction standard errors are only 0.12-0.15 wt% and do not include candidate, preferred-orientation, absorption, or profile-model systematics. Across physically defensible parent and nuisance-model trials, fractions moved by roughly 2-3 wt% absolute; that is a more realistic practical uncertainty than the formal errors. The identities of all three reported phases are reliable, but a fourth trace structure or its fraction cannot be determined reliably from this pattern. Amorphous content likewise cannot be quantified without an internal standard, so the reported fractions apply only to the modeled crystalline material.

The submitted CIFs, fractions, and `fit.csv` were exported from the final saved and replay-checked `final.gpx` project.
