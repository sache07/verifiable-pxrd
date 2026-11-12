# Powder XRD phase analysis

The pattern is described by two crystalline phases: **triclinic WO₃ (P -1), 72.27 wt%**, and **wolframite CoWO₄ (P 2/c), 27.73 wt%**. These fractions are normalized over the modeled crystalline phases. The covariance-only standard uncertainty is 0.18 wt% for each fraction, but a more realistic uncertainty is about ±1.5 wt% absolute because the result depends on atomic displacement and peak-profile assumptions. Amorphous material, if present, is not measured by this normalization.

## Evidence

The 23.2–24.4° triplet and the WO₃ peak families across the full scan select the triclinic model. Under the same preliminary nuisance model, triclinic WO₃ gave Rwp 6.07%, compared with 6.37–6.98% for two monoclinic records and 11.05% for an orthorhombic record. The strong feature near 30.7° and its low-, middle-, and high-angle families require wolframite CoWO₄. Because the available exact CoWO₄ database record was malformed, the starting P 2/c model was made by the chemically direct isovalent Mo→W substitution in CoMoO₄-II (COD 7205001), then its cell and atomic coordinates were refined.

The final full-range refinement has Rwp = 4.787%, Rp = 3.780%, Rexp = 3.280%, and GOF = 1.459 for 8,301 points. It uses the supplied Cu Kα doublet, one zero correction (+0.06616°), a smooth positive eight-coefficient background, restrained surface roughness, and phase-size broadening. WO₃ additionally needs replay-stable [100] uniaxial microstrain (5,125/4,257 ppm) and weak [111] March–Dollase texture (0.9569). CoWO₄ microstrain refined to zero and was removed. Alternative asymmetry, polarization, extra texture, and redundant broadening terms were rejected when they were negligible, bound-limited, or strongly correlated.

Final nonnegative-scale challenges drove both Co₃O₄ and residual CoO to zero. Their one-sigma scale-equivalent limits were approximately 0.15 and 0.11 wt%, respectively, so this scan does not reliably establish either phase (roughly 0.3–0.5 wt% practical upper limits under the tested models).

## Structural checks and uncertainty

Both exported CIFs have full occupancy and plausible geometry. Refined WO₃ has W–O distances of 1.722–2.243 Å and a minimum O–O separation of 2.562 Å. Refined CoWO₄ has W–O = 1.790–2.173 Å, Co–O = 2.037–2.194 Å, and minimum O–O = 2.554 Å. Unconstrained WO₃ oxygen-coordinate refinement was rejected despite a small fit improvement because it generated a 1.60 Å W–O contact; the submitted WO₃ oxygen substructure therefore remains reference-led and is less certain than its cell and W positions. The CoWO₄ model is also prototype-derived, although its refined geometry and complete peak-family agreement support the assignment.

`final.gpx` was reopened and replayed over 9.9034–100.0949° 2θ before export. It contains no frozen variables; the final maximum shift/esd was 0.503. `fit.csv`, both CIFs, and the fractions above were exported from that exact saved project.
