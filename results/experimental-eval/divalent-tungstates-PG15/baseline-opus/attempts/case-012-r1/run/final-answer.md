Done. Here's what the data show and what I delivered.

## Result

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---|
| **NiWO4** (wolframite) | *P*2/*c* | 4.60101(11), 5.66369(15), 4.91076(14), β 89.980(10) | **76.0 wt%** |
| **γ-WO3** (monoclinic) | *P*2₁/*n* | 7.30333(28), 7.53483(30), 7.69010(30), β 90.815(4) | **24.0 wt%** |

**Rwp = 4.33 %, Rp = 3.38 %, GOF = 1.25**, 8282 points (10–100° 2θ), 44 parameters.

Files written to the workspace root: `NiWO4.cif`, `WO3.cif`, `fit.csv` (2θ, obs, calc, diff, background), `result.json`, `report.md`, `final.gpx`. Scripts and intermediate trial projects are in `work/`.

## Evidence

- NiWO4 explains the strongest peak (30.87°, (111)/(-111)) plus 19.20, 23.89, 24.84, 31.49, 36.5, 39.05, 41.61, 52.27, 54.57°; γ-WO3 explains the 23.04/23.52/24.28° triplet and the 33.2–34.1° group. No unassigned peaks remain anywhere in the pattern.
- **No unreacted NiO**: its strongest line (43.3°) is absent; added as a third phase it refines to 0.08 ± 0.10 wt% with zero change in Rwp. Reduced tungsten oxides were also tested and rejected.
- Implied bulk W:Ni ≈ 1.42, i.e. the charge was W-rich and all NiO was consumed.

## Limits I want to flag

- **O positions are assumed, not measured.** Freeing the NiWO4 oxygens lowers Rwp to ~4.09 % but drives bond-valence sums to 2.4 (Ni²⁺) and 4.8 (W⁶⁺) — systematic-error absorption, not structure. Both CIFs keep published O coordinates (NiWO4 wolframite; WO3 from Loopstra & Boldrini's neutron refinement, which I re-expressed in the conventional *P*2₁/*n* cell and verified reproduces the original pattern exactly). Refined heavy-atom positions give correct chemistry (BVS 1.90 / 6.45 / 6.35).
- The ±0.11 wt% esd is counting statistics only. Across every model variant I tested (background terms, zero-offset vs displacement, three WO3 starting models, two profile parameterisations, polarization 0.5–0.95, preferred orientation, O free/fixed) WO3 stayed in 23.4–25.0 wt%; a realistic figure is **24 ± 2 wt%**.
- Any amorphous content is invisible (no internal standard), so fractions are over the modelled crystalline phases only. Profile/microstrain parameters and the refined polarization (0.706) are effective values — no calibrated instrument profile was supplied. NiWO4's β is only ~2σ from 90°, and a minor triclinic δ-WO3 admixture can be neither confirmed nor excluded.