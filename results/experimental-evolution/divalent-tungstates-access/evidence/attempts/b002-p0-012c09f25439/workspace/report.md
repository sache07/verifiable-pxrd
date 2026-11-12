# Powder XRD phase analysis

The pattern is modeled as three crystalline phases. Fractions are normalized over those phases; no internal standard was supplied, so an amorphous fraction cannot be measured.

| Phase | Structural model | Refined cell (Å, °) | Crystalline wt.% |
|---|---|---|---:|
| ZnWO4, wolframite | monoclinic P2/c | a=4.70721, b=5.74015, c=4.93839, β=90.6409 | 81.81 |
| WO3 | monoclinic P21/n | a=7.31803, b=7.53171, c=7.71385, β=90.9048 | 12.99 |
| ZnO, wurtzite | hexagonal P63mc | a=3.25894, c=5.18970 | 5.19 |

The result is chemically consistent with the ZnO + WO3 precursors fired at 700 °C: ZnWO4 is the dominant reaction product, while both precursors remain. The wolframite model accounts for the dominant reflections near 19.2, 24.8, 31.0, 36.7, 41.6, and 54.2° 2θ. The 23–25° multiplet and related reflections require monoclinic WO3. Weak but coherent residuals at the wurtzite ZnO positions (including approximately 31.9, 36.6, 47.9, 56.8, 62.9, and 68.1°) establish the third phase. Adding either residual phase removed multiple matched peaks, rather than only improving isolated bins; no fourth crystalline phase was supported.

The final full-range Cu Kα1/Kα2 Rietveld profile has Rp = 3.439%, Rwp = 4.684%, and reduced χ² = 3.134 over 8,301 points. It uses atomic structure factors throughout (no Pawley or Le Bail intensities), positive background and peak widths, phase-specific broadening, and March–Dollase corrections supported by the intensity residuals. The saved `final.gpx` was reloaded and independently regenerated without profile-review flags.

Uncertainty is dominated by preferred orientation and overlap of the minor-phase peaks with ZnWO4. A realistic interpretation is about ±2–3 wt.% for ZnWO4 and WO3 and ±1–2 wt.% for ZnO; the 5.19 wt.% ZnO value is therefore less precise than its digits imply. The ZnWO4 topology and phase assignment are reliable, but its starting coordinates were adapted from a wolframite analogue because an exact ZnWO4 reference was unavailable in the supplied library. For WO3, the heavy-atom positions are constrained by the X-ray data, while the oxygen-only refinement was unstable; its oxygen coordinates were retained from the P21/n reference. That older WO3 oxygen sublattice includes short O–O contacts (~1.58 Å), so the submitted WO3 CIF is reliable for phase identification and cell metrics but not for precise oxygen geometry or bond analysis.
