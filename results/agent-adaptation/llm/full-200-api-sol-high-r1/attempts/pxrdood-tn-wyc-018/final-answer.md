The peak positions index very closely on a **primitive cubic cell** with \(a \approx 6.185\) Å. Representative assignments are 100 at 14.30°, 110 at 20.29°, 111 at 24.91°, 200 at 28.85°, 220 at 41.25°, and 400 at 59.76°. The corresponding \(1/d^2\) values follow the primitive-cubic integer sequence.

A plausible ordered V₂O₅ model is the cubic **cP14, \(P\bar{4}3m\)** prototype with \(Z=2\). The cell and space-group assignment are considerably more secure than the internal coordinates; the latter should be treated as a chemically reasonable starting model for Rietveld or DFT refinement.

```cif
data_V2O5_cubic_candidate
_audit_creation_method
;Indexed from the supplied Cu Kalpha1 powder pattern.
Internal coordinates are a prototype starting model and are not
a substitute for a full Rietveld refinement.
;

_chemical_name_common              'cubic vanadium pentoxide'
_chemical_formula_sum              'V4 O10'
_chemical_formula_structural       'V2O5'
_cell_formula_units_Z              2

_cell_length_a                     6.1850
_cell_length_b                     6.1850
_cell_length_c                     6.1850
_cell_angle_alpha                  90
_cell_angle_beta                   90
_cell_angle_gamma                  90
_cell_volume                       236.68

_space_group_crystal_system        cubic
_space_group_name_H-M_alt          'P -4 3 m'
_space_group_IT_number             215

_diffrn_radiation_type             'Cu Kalpha1'
_diffrn_radiation_wavelength       1.5406

loop_
_atom_type_symbol
_atom_type_oxidation_number
V  5
O -2

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
V1  V  0.1600  0.1600  0.1600  1.0  0.010
O1  O  0.0000  0.0000  0.0000  1.0  0.015
O2  O  0.5000  0.0000  0.0000  1.0  0.015
O3  O  0.3100  0.0000  0.0000  1.0  0.015
```

The common ambient-pressure orthorhombic \(\alpha\)-V₂O₅ structure, \(Pmmn\), does **not** satisfactorily explain this pattern: its characteristic reflections near 15.4°, 21.7°, and 26.2° are absent, whereas the observed peaks follow a cubic \(1/d^2\) sequence.
