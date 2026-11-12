Done. Summary of the analysis:

**Phases found (2 crystalline phases):**

| Phase | Space group | Weight fraction |
|---|---|---|
| CuWO4 (triclinic copper tungstate) | P-1 | 97.5 wt% |
| γ-WO3 (unreacted precursor) | P2₁/n | 2.5 ± 0.2 wt% |

**Fit:** Rwp = 3.78 %, Rp = 2.98 %, Rexp = 2.42 %, GOF = 1.56 over 8301 points and 66 variables; R(F) = 1.34 % (CuWO4) / 2.62 % (WO3).

**How it was established.** I screened all Cu–W–O, Cu–O and W–O entries in the bundled COD-filtered database by pattern simulation. Every strong line matches triclinic CuWO4, but all observed positions sit ~0.27° high with a cos θ dependence — a Bragg–Brentano sample-displacement error, which refines as one parameter (removing it raises χ² ~100×). A CuWO4-only model leaves a residual triplet at 23.44/23.91/24.68° plus lines at 26.9/33.6/33.9°, all indexing as γ-WO3; its refined cell matches literature γ-WO3 to <0.01 Å, and including it drops Rwp from 8.58 % to 3.78 %. CuO and Cu2O refine to 0.00 wt%; Cu3WO6 and Cu2WO4 are excluded because their strongest calculated lines are absent (≤0.6 % of max intensity); the high-pressure CuWO4-II polymorph gives no significant improvement.

**Stated limitations** (detailed in `report.md`): the ±0.03 wt% statistical esd is optimistic — ±0.2 wt% from model-variant spread is realistic; no microabsorption correction; the WO3 structure is scaled only, not refined (its Uiso diverges at 2.5 wt%, and δ/ε-WO3 distortions can't be excluded); CuWO4 oxygen positions are only approximately determined under W-dominated lab-XRD scattering (shortest Cu–O comes out 0.09 Å short of the single-crystal value).

**Deliverables:** `CuWO4.cif`, `WO3.cif`, `fit.csv`, `fit.png`, `result.json`, `report.md`, `final.gpx` (the project all numbers come from), plus `scripts/` and intermediate projects in `work/`.