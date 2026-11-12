All deliverables are written. Final verification passes: `final.gpx` reopens and reproduces R_wp = 5.343 % and the reported fractions.

## Result

**Two crystalline phases — no third phase is detectable:**

| Phase | Space group | Weight fraction | CIF |
|---|---|---|---|
| γ-WO₃ (monoclinic, unreacted precursor) | *P*2₁/*n* | **70.3 wt%** (e.s.d. 0.14; realistic ±1.5) | `WO3.cif` |
| CoWO₄ (wolframite) | *P*2/*c* | **29.7 wt%** (e.s.d. 0.14; realistic ±1.5) | `CoWO4.cif` |

R_wp = 5.34 %, R_p = 4.09 %, GOF = 1.63, 8301 points, 37 variables; R_F = 2.15 % (WO₃, 439 refl.) and 2.35 % (CoWO₄, 140 refl.). Refined cells match literature γ-WO₃ (7.30604(42), 7.53635(44), 7.69312(44) Å, β = 90.8054(37)°) and CoWO₄ (4.66944(29), 5.68363(35), 4.94991(33) Å, β = 90.056(9)°). The fractions imply Co : W ≈ 1 : 4.1, i.e. a WO₃-rich charge in which all the CoO was consumed.

**Key findings along the way**

- Phase ID is unambiguous: the 23.17/23.67/24.41° triplet is γ-WO₃; 19.06, 30.71, 31.51, 36.45, 38.60, 52.13, 65.13° are CoWO₄. Co₃O₄ and CoO were each added as a third phase and both refined to exactly zero weight with no R_wp change.
- The dominant systematic was **not** structural: without an angle-dependent reflection-geometry correction the fit stalls near R_wp ≈ 8 % and drives all U_iso negative. Adding the Suortti surface-roughness correction (A = 0.146, B = 0.780) with physical U_iso dropped R_wp to 5.34 % and stabilised the fractions.
- The available structure database's usual monoclinic WO₃ entry (COD 1528915) contains an impossible 1.58 Å O···O contact, so I transformed COD 2311041 into the conventional *P*2₁/*n* setting instead.

**Stated limits** (detailed in `report.md`): oxygen positions are not determinable (releasing them lowers R_wp to 5.18 % but produces a 1.51 Å W–O bond, so they are held at literature values); U_iso, amorphous content, and the microstrain/size split are not determined; absolute cell accuracy is limited by the −111 µm sample displacement to roughly ±0.002 Å rather than the quoted e.s.d.s.

One note: a background comparison job was stopped when it hit its time limit, but its first variant had already completed and the conclusion from it (Kα₂/Kα₁ refines to 0.61, consistent with the reported 0.5) is included above.