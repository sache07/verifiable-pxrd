Done. All deliverables are in the workspace root.

## Result

The sample is the **unreacted precursor mixture** — no Mn–W–O compound formed at 300 °C.

| Phase | Identity | Space group | Weight fraction | CIF |
|---|---|---|---|---|
| WO₃ | γ-WO₃ (monoclinic) | *P*2₁/*n* (14), *Z* = 8 | **70.3 wt%** | `WO3_gamma_monoclinic.cif` |
| MnO₂ | β-MnO₂, pyrolusite (rutile) | *P*4₂/*mnm* (136), *Z* = 2 | **29.7 wt%** | `MnO2_pyrolusite.cif` |

R<sub>wp</sub> = 6.83 %, R<sub>p</sub> = 5.03 %, R<sub>exp</sub> = 2.69 %, *S* = 2.54 (8301 points, 40 variables). The refined ratio corresponds to MnO₂:WO₃ = 1.13:1 molar, i.e. a near-equimolar mix.

**Evidence:** the 002/020/200 triplet at 23.44/23.93/24.69° fixes γ-WO₃, and the residual peaks left by a WO₃-only fit (29.01, 37.68, 56.96, 59.66, 65.1, 67.5, 72.5°) index exactly as pyrolusite 110/101/211/220/002/310/301 with a near-regular MnO₆ octahedron (Mn–O 1.89 Å). Seven candidate third phases (MnWO₄, Mn₂O₃, Mn₃O₄, MnO, ramsdellite-MnO₂, tetragonal WO₃) each refined to ≤1.2 wt% with no fit improvement.

**Stated limits** (detailed in `report.md`):
- Weight fractions carry a realistic **±3 wt%**, not the ±0.2 wt% least-squares esd — the value moves between 70 and 74 wt% WO₃ across defensible peak-shape/displacement models.
- Lattice parameters are ~**+0.15 % systematically large** in *both* phases, from an uncorrected 2θ zero (+0.393°) on an uncalibrated instrument; relative metrics are sound, absolute ones are not.
- **Oxygen positions are not determined.** Refining them freely reached R<sub>wp</sub> ≈ 5.2 % but produced 1.2–1.3 Å W–O distances and negative U<sub>iso</sub> — absorbed misfit, not structure. The submitted CIFs hold O at published coordinates, so they are lattice-refined literature models rather than independent structure determinations.
- A few-wt% triclinic δ-WO₃ component cannot be excluded but is not separable from anisotropic strain broadening of γ-WO₃ at this profile quality, so it was not included.
- U<sub>iso</sub>(Mn) pinned at its 0.025 Å² bound, likely signalling stacking disorder in the MnO₂ — the main reason the MnO₂ fraction is the less certain of the two.