# Powder XRD phase analysis

The pattern is described by three crystalline phases:

| Phase | Structure | Refined cell | Weight fraction* |
|---|---|---|---:|
| ZnWO4 | wolframite, P2/c | a = 4.70308 Å, b = 5.72968 Å, c = 4.94078 Å, β = 90.5991° | 0.7485 (74.85 wt%) |
| WO3 | monoclinic, P21/c | a = 7.30374 Å, b = 7.54004 Å, c = 10.52577 Å, β = 133.0211° | 0.1851 (18.51 wt%) |
| ZnO | wurtzite, P63mc | a = 3.25621 Å, c = 5.22334 Å | 0.0664 (6.64 wt%) |

*Fractions are normalized over the modeled crystalline phases. There was no internal standard, so amorphous material, if present, is not quantified.

## Evidence

The dominant wolframite ZnWO4 model accounts for the characteristic peaks near 15.6°, 19.0°, 23.9–24.6°, 30.5–31.3°, 36.4°, and 38.4° 2θ. Monoclinic WO3 is required by its low-angle cluster near 23.2–24.6° and additional peaks near 26.7°, 28.7–29.0°, and 33.4–34.3°. After fitting those phases, broad residual maxima at approximately 31.8°, 34.4°, 47.5°, 56.6°, and 62.9° identify residual wurtzite ZnO. This assemblage is chemically consistent with partial reaction of the stated WO3 and ZnO precursors at 700 °C.

The final GSAS-II Rietveld fit uses the stated Cu Kα1/Kα2 doublet and the complete 9.903–100.095° grid. It gives Rwp = 2.2839%, Rp = 1.6837%, and GOF = 1.0102; the counting-statistics minimum is about 2.27%. A direct, no-refinement replay of `final.gpx` reproduced the same Rwp and passed the phase/CIF/fraction consistency and contact checks.

## Remaining uncertainty

All three phase identities are reliable, and no fourth crystalline phase is supported above the residual noise. The broad, overlapping ZnO peaks make its abundance less precise than the formal least-squares error suggests; a realistic systematic uncertainty is roughly 1–2 percentage points for the reported phase fractions. The metal sublattices and cells are well constrained, but the detailed oxygen coordinates in monoclinic WO3 and the ZnO internal coordinate are less certain because oxygen scatters weakly in laboratory X-ray data. Those coordinates were therefore kept close to physically valid published parent structures rather than allowed to absorb profile imperfections.
