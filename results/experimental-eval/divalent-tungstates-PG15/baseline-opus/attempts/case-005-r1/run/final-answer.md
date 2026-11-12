Done. Here's what the analysis found and what was delivered.

## Result

The 500 °C product is **not a new compound** — the pattern is quantitatively accounted for by the two precursors:

| Phase | Space group | CIF | Weight fraction |
|---|---|---|---|
| γ-WO3 (monoclinic) | *P*2₁/*n* | `WO3.cif` | 0.752 ± 0.002 |
| Co3O4 (spinel) | *Fd*-3*m* | `Co3O4.cif` | 0.248 ± 0.002 |

Rwp = 2.78 %, Rp = 2.13 %, GOF = 1.62 (background-subtracted R′wp = 11.8 %, since the background is ~17 % of the tallest peak). Phase residuals: RF = 2.9 % (WO3, 440 refl.), 3.4 % (Co3O4, 22 refl.).

Key points of evidence:
- The strongest triplet (23.47/23.95/24.71°) is the γ-WO3 (002)/(020)/(200) group; the rest index on *Fd*-3*m* with a = 8.0838 Å = stoichiometric Co3O4.
- **All peaks sit ~0.35° too high at low angle, falling off as cos θ** — a −669 µm specimen displacement, not a lattice effect. Ignoring it makes both phases look ~1 % compressed; refining it reproduces literature cells for both.
- The refined ratio is 3.15 WO3 : 1 Co3O4 (Co:W = 0.95:1), i.e. the untouched 1:1 Co:W batch of an intended CoWO4 synthesis — internally consistent with no reaction (CoWO4 normally needs ≳600–700 °C).
- CoWO4 was explicitly tested as a third phase: its fraction refines to zero and the difference curve at its strongest line (30.9°) is flat; upper bound ≲1.5 wt%.

## Stated limitations
- Atomic coordinates/ADPs are **not** determined — freely refined Uiso went unphysical (negative for W) while lowering Rwp, so literature coordinates were held fixed; only cells, scales and profile terms were refined.
- Weight fractions span 74.4–75.4 wt% WO3 across acceptable model variants, so 75 ± 1 / 25 ± 1 wt% is the defensible figure; microabsorption is uncorrected and amorphous content is not quantified (no internal standard).
- Residual ~10σ misfits at 34.16/50.26° lie on existing WO3 reflections (anisotropic strain / possible ε-WO3 domains), not at new positions.

Files in the workspace: `WO3.cif`, `Co3O4.cif`, `fit.csv` (+ `fit.png`), `result.json`, `report.md`, `final.gpx` (+ `final.lst`), with the scripts in `scripts/` and model-comparison runs in `work/`.