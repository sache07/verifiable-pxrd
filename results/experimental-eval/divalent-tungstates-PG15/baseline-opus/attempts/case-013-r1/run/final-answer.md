Done. Here's what the analysis found.

## Result — 5 crystalline phases (Rwp = 10.60 %, Rp = 7.05 %, Rexp = 3.49 %, GOF = 3.03)

| phase | formula | SG | wt % | realistic unc. |
|---|---|---|---|---|
| stolzite (scheelite PbWO4) | PbWO4 | I4₁/a | 60.2 | ±3 |
| Pb2WO5 (Pb2MoO5 type) | Pb2WO5 | C2/m | 12.8 | ±4 |
| γ-WO3 (unreacted) | WO3 | P2₁/n | 10.1 | ±2 |
| massicot β-PbO | PbO | Pbcm | 9.2 | ±5 |
| litharge α-PbO | PbO | P4/nmm | 7.7 | ±5 |

So: a partially reacted, slightly Pb-rich charge (derived Pb/W = 1.26) — mostly converted to PbWO4, with the 2:1 intermediate Pb₂WO₅ plus leftover PbO (both polymorphs, nanocrystalline) and WO₃.

**Key analysis steps**
- The whole pattern carries a **+0.25° 2θ offset** (all phases shifted equally); modeled as specimen displacement. Without it every cell is ~0.4 % too small and identification goes wrong.
- A **Suortti surface-roughness correction** was needed (strongly absorbing specimen); without it the high-angle PbWO4 peaks are under-calculated by ~20 % and the displacement parameters collapse to zero.
- Pb₂WO₅ was found by indexing the residual: 23 of 28 residual lines index on a monoclinic cell within ~1 % of Pb₂MoO₅, with matching intensity ranking. Each minor phase was verified by leave-one-out refinements (ΔRwp +2.2 to +3.8 %).
- I found and fixed a trap: the COD litharge entry imports into GSAS-II with Pb on a 4-fold site (stoichiometry Pb₂O). Rebuilding it correctly dropped Rwp from 11.2 → 10.3 % and shifted the PbO fractions substantially.

**Stated limits** (detailed in `report.md`): one peak at 30.15/30.24° (1.7 % of Bragg intensity, 30σ) is unexplained — a Le Bail test shows the refined C2/m lattice has no reflection there, which hints the real Pb₂WO₅ is a primitive variant; the α/β-PbO split is poorly conditioned (total PbO ≈ 17 wt % is the robust number); oxygen positions are not refinable from these Pb/W-dominated data, so all coordinates are held at reference values (free refinement gave W–O 1.68 Å for 0.25 % Rwp gain); amorphous content is not quantified.

**Files** (workspace root, duplicated in `out/`): `stolzite.cif`, `Pb2WO5.cif`, `WO3.cif`, `massicot.cif`, `litharge.cif`, `fit.csv`, `result.json`, `final.gpx`, `fit_plot.png`, `report.md`.