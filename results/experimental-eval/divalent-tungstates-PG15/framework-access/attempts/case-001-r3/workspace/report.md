# Powder XRD phase analysis

## Result

The crystalline pattern is modeled as an essentially unreacted precursor mixture:

| Phase | Structural model | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| Witherite, BaCO₃ | Pmcn setting of Pnma (No. 62) | a = 5.30698, b = 8.91256, c = 6.43133 | 0.5500 |
| Monoclinic WO₃ | P2₁/c (No. 14) | a = 7.69086, b = 7.53569, c = 10.53722, β = 136.1111° | 0.4500 |

Fractions are normalized over these two modeled crystalline phases. They do not measure amorphous material or any phase below the diffraction detection limit.

## Evidence and refinement

The split WO₃ multiplet at about 23–25° 2θ and its complete medium/high-angle reflection series require monoclinic WO₃. The remaining strong lines and their high-angle continuations are indexed by orthorhombic witherite BaCO₃. Together, the two atomic models account for all reproducible peaks over the full 9.903–100.095° scan. This is chemically plausible for BaCO₃ + WO₃ after only 60 minutes at 400 °C.

Starting models were COD 9010928 (BaCO₃) and COD 2311041 (WO₃). Cells, phase scales, common isotropic displacement factors, physically bounded profile/specimen terms, and a modest BaCO₃ [110] March–Dollase correction were refined. Atomic-coordinate changes were regularized to the laboratory's reference-mismatch envelope (about 0.03–0.05 Å RMS by element), avoiding the chemically implausible oxygen shifts obtained from an unconstrained coordinate refinement. The exported structures have sensible local geometry: C–O = 1.28–1.36 Å, Ba–O = 2.72–2.87 Å, and W–O = 1.73–2.17 Å.

Fresh atomic replay of `final.gpx`, without optimization or cached calculated intensities, gives Rwp = 5.898%, Rp = 4.492%, Rexp = 3.481%, and goodness of fit = 1.697 on all 8301 points. Replay reports no negative background, negative analytic peak width, invalid polarization, or negative displacement-parameter flags. `fit.csv` is the profile from that replay.

## Alternatives and uncertainty

Adding BaWO₄, Ba₃W₂O₉, or Ba₃WO₆ produced only approximately 0.4, 0.2, and 0.1 wt% respectively in exploratory fits, with no independent diagnostic peaks; these unstable trace scales were treated as residual leakage rather than identified phases. A triclinic P-1 WO₃ model was also tested, but gave a poorer whole-profile fit with substantially more positional freedom. The monoclinic assignment is therefore preferred, although laboratory peak overlap does not determine every WO₃ oxygen coordinate uniquely.

The phase fractions have an estimated systematic uncertainty of roughly ±0.02 in absolute weight fraction. The main sources are overlap of the two precursor patterns and correlation among polarization, displacement factors, surface correction, and phase scales. Angular zero and specimen displacement are also strongly correlated in a single Bragg–Brentano scan. Crystalline impurities below roughly 0.5–1 wt% cannot be excluded reliably, and no amorphous fraction can be determined from these data alone.
