# Powder XRD phase analysis

For the CaO + WO₃ synthesis heated at 800 °C, the Cu Kα pattern is modeled by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Structural model | Weight fraction | Refined cell (Å, °) |
|---|---|---:|---|
| CaWO₄, scheelite | COD 7219229, *I*4₁/*a* | 0.69935(96) | a = 5.24667, c = 11.37712 |
| Ca₃WO₆, ordered double-perovskite-type | Ca₂MgWO₆ parent COD 2013468 with Mg→Ca, *P*2₁/*n* | 0.13929(80) | a = 5.80696, b = 5.54925, c = 8.00243, β = 90.0494 |
| WO₃, monoclinic | COD 2311041, *P*2₁/*c* | 0.16136(68) | a = 7.68347, b = 7.53686, c = 10.50872, β = 136.0631 |

The Ca₃WO₆ assignment is supported by a coherent residual family at approximately 19.35, 22.04, 31.45, 37.44, 45.13, and 56.9° 2θ. Its first five lines index consistently in the refined monoclinic double-perovskite cell. Multiple ordered tungstate parents were mapped and carried through matched refinements; the Ca₂MgWO₆ lineage was the best physical, chemically nearest model. The monoclinic WO₃ source was selected by a matched swap against a triclinic alternative. An initially useful rounded WO₃ reference was rejected because it generated a 1.58 Å O–O contact.

All three phases are required: matched deletion refinements increased Rwp from about 3.84% to 38.05% without CaWO₄, 9.77% without Ca₃WO₆, and 13.81% without WO₃. A rock-salt CaO trial refined to zero scale and was removed. The submitted fit has Rwp = 3.8215%, Rp = 2.9629%, and goodness of fit = 1.4668. Independent nuisance starts reproduced the profile, cells, structures, and fractions. The correlated X/Z peak-width subspace was retained because those starts converged to the same calculated curve and positive analytic widths; independent replay of `final.gpx` produced no physical-profile review flags.

The parent Ca₃WO₆ oxygen framework is retained. Unrestrained oxygen refinements produced O–O contacts near 2.11 Å, and the prescribed coupled soft-restraint retry remained unstable, so those ligand coordinates cannot be determined reliably from this pattern. Only the physical general Ca-site displacement was retained. The parent oxygen geometry, not the lower-Rwp contact-bearing variant, is submitted. Fraction ESDs in the table are covariance-only estimates; source/model uncertainty is larger. Without an internal standard, no amorphous fraction is quantified, and very small additional crystalline components below the residual detection limit cannot be excluded.
