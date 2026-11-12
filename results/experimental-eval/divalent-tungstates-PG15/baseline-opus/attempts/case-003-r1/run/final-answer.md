All deliverables are complete and verified. Final summary:

## Result

**Three crystalline phases** (a partially reacted CaCO₃ + WO₃ mixture; the 500 °C treatment converted only ~14 % of the tungsten):

| Phase | Space group | Weight fraction | stat. esd | realistic uncertainty |
|---|---|---|---|---|
| γ-WO₃ (monoclinic) | P2₁/c (#14) | 0.568 | 0.002 | ±0.015 |
| CaCO₃ (calcite) | R-3c (#167) | 0.314 | 0.002 | ±0.012 |
| CaWO₄ (scheelite) | I4₁/a (#88) | 0.118 | 0.001 | ±0.015 |

Rwp = 7.22 %, Rp = 5.30 %, GOF = 3.03 (8293 points, 66 variables).

## How it was established
- Candidates screened from the local COD-filtered database over the Ca–C–O–W chemistry; all observed peaks are indexed by the three phases, and **every** reflection of each phase above 2 % relative intensity is observed above background.
- A single refined sample displacement (−0.50 mm, cos θ) explains the common +0.29° shift of all three phases — a strong self-consistency check on the assignment.
- Polymorph discrimination by refinement: monoclinic γ-WO₃ (Rwp 7.2) vs triclinic δ-WO₃ (8.2) vs an older γ coordinate set (8.5); subcell/high-T WO₃ entries can't generate the superstructure lines.
- Six candidate 4th phases (CaO, portlandite, aragonite, vaterite, Ca₃WO₆, H₂WO₄) each refine to ≤ 0.3 wt % with ΔRwp ≤ 0.01 → no evidence for a 4th phase (detection limit ≈ 1 wt %).
- WO₃ (2 W + 6 O) and CaWO₄ (O) coordinates were refined; the resulting W–O/Ca–O distances were checked independently and are chemically sound.

## Stated limits (detailed in `report.md`)
Amorphous content cannot be quantified (no internal standard); microabsorption is uncorrected and likely biases calcite high / W-phases low — consistent with the bulk Ca/W = 1.24 found; ADPs had to be fixed at reference values; WO₃ oxygen positions are only ±0.04 Å; residual misfit is concentrated at the tops of the strongest peaks (profile-shape limitation of the uncalibrated lab line shape), not at unindexed positions.

Files written to the workspace root: `WO3.cif`, `CaCO3.cif`, `CaWO4.cif`, `fit.csv`, `result.json`, `report.md`, `final.gpx` (re-opened in a fresh process to confirm it reproduces exactly the submitted Rwp and fractions). Scripts, variant projects and logs are in `work/`.