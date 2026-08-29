The pattern indexes most consistently as an **orthorhombic Pbca cell** with approximately

\[
a=13.15\ \text{Å},\quad b=11.20\ \text{Å},\quad c=7.89\ \text{Å},\quad Z=8.
\]

Representative assignments are 13.45° (200), 15.81° (020), 20.87° (220), 26.30° (202), 27.10° (400), 31.53° (420), 34.79° (240), 35.50° (402), 41.16° (600), and 44.38° (620). The resulting density is about 4.02 g cm\(^{-3}\).

The lattice and space-group assignment are considerably more secure than the light-atom coordinates. The following is a chemically constrained direct-space model suitable as a starting point for Rietveld refinement; the coordinates should not be regarded as publication-quality without refinement against the original instrumental profile.

```cif
data_Ga3PO7_Pbca_candidate
_audit_creation_method
;Powder indexing followed by a chemically constrained direct-space
 model. Atomic coordinates are provisional and require Rietveld
 refinement.
;

_chemical_name_common               'gallium oxide phosphate'
_chemical_formula_sum               'Ga3 P O7'
_chemical_formula_structural        'Ga3PO7'
_chemical_formula_weight            352.136

_cell_length_a                      13.151
_cell_length_b                      11.202
_cell_length_c                       7.892
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                      1162.9
_cell_formula_units_Z                8

_exptl_crystal_density_diffrn        4.02
_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength         1.5406

_space_group_crystal_system         orthorhombic
_space_group_name_H-M_alt           'P b c a'
_space_group_IT_number              61

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '1/2-x,-y,1/2+z'
3  '-x,1/2+y,1/2-z'
4  '1/2+x,1/2-y,-z'
5  '-x,-y,-z'
6  '1/2+x,y,1/2-z'
7  'x,1/2-y,1/2+z'
8  '1/2-x,1/2+y,z'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Ga  3
P   5
O  -2

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_B_iso_or_equiv
Ga1 Ga 8 c 0.1273 0.1128 0.1374 1.0 0.7
Ga2 Ga 8 c 0.3652 0.1483 0.3817 1.0 0.7
Ga3 Ga 8 c 0.1194 0.3647 0.6172 1.0 0.7
P1  P  8 c 0.3682 0.3861 0.1286 1.0 0.8
O1  O  8 c 0.4840 0.3821 0.1350 1.0 1.0
O2  O  8 c 0.3291 0.5124 0.1402 1.0 1.0
O3  O  8 c 0.3296 0.3249 0.2870 1.0 1.0
O4  O  8 c 0.3313 0.3218 0.9680 1.0 1.0
O5  O  8 c 0.1936 0.2251 0.3542 1.0 1.0
O6  O  8 c 0.2451 0.1119 0.6178 1.0 1.0
O7  O  8 c 0.1168 0.4835 0.4032 1.0 1.0
```

The principal surviving ambiguity is a lower-symmetry subgroup of `Pbca` caused by weak superstructure reflections, but the peak positions do not require such a reduction. The `Pbca`, \(Z=8\) model is therefore the preferred indexing solution.
