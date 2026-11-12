# b001 curation ledger

| Question / prediction | Evidence obtained | Decision |
|---|---|---|
| Common exact-reference cases should be recoverable while exposing refinement/export failures. | c01–c03 pass generation audits; c03's 2.83 wt% CaO and 6.75 wt% calcite each change the profile by about 1.2 noise units. | Keep one clean control, one unreacted control, and one four-phase completion case. |
| Hidden ZnWO4 should retain an easy chemically sensible framework route. | With all exact ZnWO4 entries removed, MgWO4 COD 9013902 survives at tier 1 with 0.81% cell mismatch. | Keep as the easier principal adaptation case. |
| A hidden secondary Ca3WO6 phase can test off-stoichiometric recovery without requiring ab initio solution. | Removing exact Ca3WO6 alone leaves near-identical Ca3OsO6; removing both leaves tier-1 Ca2CoWO6 at 3.97% mismatch. The 13.9 wt% phase has omission RMS 3.94 noise units. | Use explicit withholding of 1563081 and 1562666. |
| A second framework should require more than repeating the Zn substitution. | PbWO4 with exact entries and EuWO4 removed leaves tier-1 CaWO4 at 5.65% mismatch. All three phases remain detectable at low counts. | Keep as the harder scheelite adaptation case. |
| CuWO4 could provide a distorted low-symmetry adaptation. | Selected COD block was from a high-pressure series rather than a defensible ambient product source. | Exclude before freeze. |
| Litharge could serve as the residual Pb precursor. | Preview exposed GSAS-II/pymatgen oxygen-multiplicity disagreement after origin-setting handling. | Exclude and use published cerussite, accounting for CO2 loss. |
| The first room-temperature monoclinic WO3 source should be physically uncontroversial. | Freeze preflight flagged every WO3-containing case; scorer audit traced this to four 1.575 A O--O contacts in COD 1528915. Published neutron model COD 2311041 passes with no flagged contacts, as do all of its final case perturbations. | Preserve failed request `freeze-b001`; replace the shared WO3 source and resubmit as `freeze-b001-v2`. |

Next evidence: three independent P0 attempts on every frozen case, followed by attempt-level trajectory and workspace diagnosis.
