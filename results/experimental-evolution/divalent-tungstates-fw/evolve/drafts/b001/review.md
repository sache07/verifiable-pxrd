# b001 prospective scientific review

## Decision

Freeze this six-case panel as the first training batch. It spans a clean end-to-end control, an unreacted control, a four-phase completion problem, and three reference-adaptation problems of increasing practical difficulty. All six final previews pass the frozen generator's handoff checks and are eligible for strict recovery. This review is prospective: no solver result was seen when the cases were chosen.

## Source audit

The final pool contains ten ordered models from the frozen filtered COD, with densities of 2.71–8.37 g cm-3 and minimum separations of 1.20–2.41 A. Registration produced no parser warnings, and every final case reference passes the scorer physical screen with zero flagged contacts. Calcite COD 1547347 had a metadata typo (`C Ca O`) despite complete CaCO3 atom sites; only `_chemical_formula_sum` was corrected. CaO COD 1563196 used the nonstandard type token `CA`; only that token was changed to `Ca`. Both repairs preserve all lattice, symmetry, coordinate, occupancy, and displacement data and retain their source parents.

Source-condition and physical review led to three exclusions. CuWO4 COD 4000806 belongs to a pressure-series block in a high-pressure study, so it was not used as an ambient fired product. PbO COD 9012700 was excluded after a preview showed an origin-setting incompatibility that made GSAS-II and pymatgen disagree on oxygen multiplicity; it was replaced by published orthorhombic cerussite. The initially selected room-temperature WO3 COD 1528915 has four 1.575 A O--O contacts and triggered the scorer's oxide review, so it was replaced by the published monoclinic neutron-diffraction model COD 2311041, which passes outright. These are curation exclusions, not solver failures.

## Case roles

| Case | Generating inventory | Availability and concrete role |
|---|---|---|
| b001-c01 | 100 wt% CaWO4 | Fully referenced, zero-offset/specimen control. Isolates retrieval, instrument/background refinement, reference-mismatch refinement, and correct final project export. |
| b001-c02 | 46.0 wt% BaCO3 + 54.0 wt% WO3 | Fully referenced 250 C unreacted 1:1-molar charge. Low counts and specimen effects test two-phase identification and quantitation without reaction inference. |
| b001-c03 | 63.1 wt% CaWO4 + 27.3 wt% WO3 + 6.75 wt% CaCO3 + 2.83 wt% CaO | Fully referenced balanced partial carbonate reaction. The two weak phases require residual-led completion and restrained multiphase refinement. |
| b001-c04 | 72.0 wt% ZnWO4 + 20.7 wt% WO3 + 7.28 wt% ZnO | Exact ZnWO4 composition withheld. Easier principal missing-reference case: nearest survivor is tier-1 MgWO4, COD 9013902 (Mg->Zn, framework RMS 0.0114, 0.81% cell mismatch). |
| b001-c05 | 70.0 wt% CaWO4 + 16.1 wt% WO3 + 13.9 wt% Ca3WO6 | Secondary off-stoichiometric phase. COD 1563081 and nearly isometric Ca3OsO6 COD 1562666 are withheld; nearest survivor is tier-1 Ca2CoWO6 COD 7222332 (Co->Ca, RMS 0.0624, 3.97% mismatch). Tests residual-led discovery plus adaptation of a nonprincipal phase. |
| b001-c06 | 66.0 wt% PbWO4 + 18.2 wt% PbCO3 + 15.8 wt% WO3 | Low-count 68 mol% reacted carbonate charge after CO2 loss. Exact PbWO4 entries 1527935/9009811/9007617 and unusually close EuWO4 1561850 are withheld; nearest survivor is tier-1 CaWO4 COD 7219229 (Ca->Pb, RMS 0.0294, 5.65% mismatch). This is the harder principal adaptation in a second framework family. |

The reaction inventories conserve the supplied metal ratio. Carbonate cases account for solid CO2 loss. Ca3WO6 is chemically plausible as a local Ca-rich intermediate in an unre-ground 1:1 charge because its 0.1 mol fraction is balanced by 0.2 mol residual WO3.

## Generation audit

| Case | Oracle Rwp (%) | Maximum oracle fraction error | Omission RMS / noise unit by phase |
|---|---:|---:|---|
| b001-c01 | 3.55 | 0.0000 | CaWO4 8.20 |
| b001-c02 | 1.87 | 0.00241 | BaCO3 3.00; WO3 4.25 |
| b001-c03 | 2.76 | 0.00061 | CaWO4 17.91; CaO 1.23; CaCO3 1.20; WO3 9.13 |
| b001-c04 | 2.65 | 0.00039 | ZnWO4 12.85; ZnO 2.14; WO3 7.38 |
| b001-c05 | 2.61 | 0.00061 | Ca3WO6 3.95; CaWO4 18.05; WO3 5.76 |
| b001-c06 | 3.38 | 0.00106 | PbWO4 4.54; PbCO3 1.32; WO3 1.25 |

The weak components in c03 and c06 are deliberately near the noise-limited detection boundary but remain independently detectable in the frozen audit. The audit establishes recoverability with known structures and generating background family; it does not prove uniqueness against every polymorph or decoy.

Final hashes: manifest `62ca5bb0bf8e1e74af6e70223133fda58bd549c2f87cd288a793af6c8670649f`; source pool `784fcc2152122c7f09914daa2029708b8624926c0cef670c61dcc9d2b4754269`.
