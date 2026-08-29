The pattern indexes uniquely to a primitive monoclinic cell. The systematic absence of \(h0l\) reflections with odd \(l\) supports **\(P2/c\) (No. 13)**. Representative indexing is 010 at 9.47°, 020 at 19.00°, 100 at 19.57°, 110 at 21.79°, 120 at 27.41°, 002 at 28.67°, 102 at 34.25°, and 130 at 34.96°.

Refined metric:

\[
a \simeq 4.536\ \text{Å},\quad
b \simeq 9.332\ \text{Å},\quad
c \simeq 6.228\ \text{Å},\quad
\beta \simeq 87.63^\circ,\quad Z=2.
\]

The cell and space-group assignment are considerably more secure than the light-atom coordinates. The CIF below is a chemically constrained \(P2/c\) starting model; its coordinates should be finalized by Rietveld refinement against the original profile before deposition.

```cif
data_MnP2O7_primary
_audit_creation_method
;Powder indexing followed by a chemically constrained direct-space
 model. Cell and space group are pattern-derived; atomic coordinates
 are a starting model for Rietveld refinement.
;

_chemical_name_common                 'manganese(IV) diphosphate'
_chemical_formula_sum                 'Mn P2 O7'
_chemical_formula_structural          'Mn(P2O7)'
_chemical_formula_weight              228.879
_cell_formula_units_Z                 2

_symmetry_space_group_name_H-M        'P 1 2/c 1'
_symmetry_Int_Tables_number           13
_space_group_crystal_system           monoclinic

_cell_length_a                        4.536
_cell_length_b                        9.332
_cell_length_c                        6.228
_cell_angle_alpha                     90
_cell_angle_beta                      87.63
_cell_angle_gamma                     90
_cell_volume                          263.4

_exptl_crystal_density_diffrn         2.886
_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y,-z+1/2'
3  '-x,-y,-z'
4  'x,-y,z+1/2'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Mn  4
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
Mn1 Mn 2 e  0.0000  0.3500  0.2500  1.0  0.50
P1  P  4 g  0.2150  0.1060  0.1240  1.0  0.50
O1  O  2 a  0.0000  0.0000  0.0000  1.0  0.70
O2  O  4 g  0.5060  0.0310  0.1630  1.0  0.70
O3  O  4 g  0.0660  0.1480  0.3380  1.0  0.70
O4  O  4 g  0.2720  0.2390  0.9880  1.0  0.70
```

The principal crystallographic alternative is the centrosymmetric subgroup **\(P\bar1\)** using the same metric, but it is not favored because the observed strong reflections satisfy the \(P2/c\) extinction condition.
