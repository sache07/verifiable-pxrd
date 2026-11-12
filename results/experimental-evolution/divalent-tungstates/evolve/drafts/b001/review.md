# Batch b001 prospective review

## Scientific scope

This six-case learning panel samples the laboratory's stated reaction family without claiming that any synthetic realization proves an experimental phase field. Every recipe starts from WO3 and one allowed divalent-metal source, accounts for every source element, and is mass-balanced to the nominal 1:1 metal dose. The progression separates routine project/refinement competence from full-reference multiphase inventory and then from reference adaptation in increasingly confounded mixtures.

All 12 registered models are published, ordered structures with one parsed model, no occupancy warnings, broad-screen densities of 3.82--9.71 g cm-3, and minimum separations of 1.29--2.31 A. The final monoclinic WO3 model is the neutron-diffraction structure COD 2311041. Source screening rejected a malformed historical WO3 record (COD 1010618, 0.46 A contact), a 1960 WO3 model with 1.575 A O--O contacts, a split/disordered BaWO4 record, a 1947 Pb3O4 model with 1.793 A O--O contacts, and a litharge CIF whose P4/nmm expansion disagreed between pymatgen and GSAS-II. The replacements--WO3 COD 2311041, 293 K minium COD 9012124, and orthorhombic PbO COD 2310433--all pass the scorer's physical screen and the independent GSAS-II unit-cell-mass check. Every final case-specific perturbed reference also has physical status `pass` with zero flagged contacts.

## Cases

| Case | Prospective role and concrete difficulty | True crystalline mixture (wt%) | Reference condition |
|---|---|---|---|
| b001-c01 | Easy end-to-end control: exact scheelite reference, zero offset, no specimen effects; only normal registered-to-sample mismatch and counting noise remain. | CaWO4 100 | Full |
| b001-c02 | Low-count full-reference partial reaction. The 7.3% ZnO is the likely inventory failure; ZnWO4 is small-domain while WO3 carries anisotropic strain, so a single shared peak-shape story is inadequate. | ZnWO4 72.0, ZnO 7.28, WO3 20.72 | Full |
| b001-c03 | Carbonate-derived three-phase mixture plus hidden product. The solver must distinguish SrCO3 and WO3, then recognize and adapt a scheelite analogue while handling phase-specific texture/strain. | SrWO4 59.06, SrCO3 15.93, WO3 25.02 | Withhold all SrWO4; surviving tier 1. Nearest CaWO4 COD 7219229, Ca->Sr, framework RMS 0.0226, cell mismatch 4.3%. |
| b001-c04 | Mixed-valence precursor mixture plus hidden product. The major missing wolframite is recoverable, but 6.27% broadened Mn3O4 is only weakly omission-detectable and can be lost after a superficially convincing major-phase fit. | MnWO4 74.67, Mn3O4 6.27, WO3 19.06 | Withhold all MnWO4; surviving tier 1. Nearest ZnWO4 COD 1520641, Zn->Mn, framework RMS 0.0171, cell mismatch 2.08%. |
| b001-c05 | Secondary off-stoichiometric recovery: Ca3WO6 is only 10.69% and overlaps major CaWO4 and WO3. Ca3WO6 and two WO3 units balance each other around the overall Ca:W=1 dose. It shares the instrument session with c01, providing a clean-vs-complex Ca comparison without telling solvers the calibration. | CaWO4 76.92, Ca3WO6 10.69, WO3 12.39 | Withhold COD 1563081; surviving tier 1. Nearest Ca3OsO6 COD 1562666, Os->W, framework RMS 0.0085, cell mismatch 0.38%. |
| b001-c06 | Four-phase heavy-atom inventory and coupled refinement. The 5.43% PbO is broadened and overlaps PbWO4/Pb3O4/WO3; all references are present, so failure isolates search completeness and refinement discipline rather than adaptation. | PbWO4 55.34, Pb3O4 16.68, PbO 5.43, WO3 22.56 | Full |

## Generation audit

The final `preview-v3` used the frozen laboratory protocol and registered pool hash `88ad9680...`. All six cases passed the generator's strict-recovery checks. Oracle known-phase Rwp spans 2.23--2.85%, and the maximum absolute oracle fraction error is 0.00190. Omission RMS values in noise units are:

| Case | Components in manifest order | Omission RMS |
|---|---|---|
| c01 | CaWO4 | 15.708 |
| c02 | ZnWO4 / ZnO / WO3 | 6.410 / 0.989 / 2.676 |
| c03 | SrWO4 / SrCO3 / WO3 | 7.912 / 1.283 / 3.672 |
| c04 | MnWO4 / Mn3O4 / WO3 | 11.968 / 0.612 / 4.080 |
| c05 | CaWO4 / Ca3WO6 / WO3 | 18.900 / 3.587 / 5.606 |
| c06 | PbWO4 / Pb3O4 / PbO / WO3 | 10.270 / 2.829 / 1.436 / 3.842 |

The panel deliberately retains weak but detectable minor phases in c02 and c04. It also spans zero-offset/specimen control, ordinary offset and displacement, roughness, phase-specific size/strain, and texture. Those realizations establish nuisance diversity for diagnosis but are not encoded as future-sample knowledge.

## Prospective learning questions

1. Does P0 complete the full phase inventory before committing to a refinement model, especially for weak residual oxides?
2. When the exact product is absent, does it search by structure family, substitute chemistry, preserve symmetry, and refine the analogue's cell rather than settling for a compositionally wrong decoy?
3. Does it refine global position/background/profile terms and phase-specific size/strain/texture in a stable order, revisit residual peaks, and save a consistent final project?
4. Are failures dominated by phase discovery, adaptation mechanics, or final GSAS-II execution/export? The three independent baselines will separate systematic gaps from rollout variance.
