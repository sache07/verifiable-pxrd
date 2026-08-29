The peak positions index closely to a primitive monoclinic cell. In the standard unique-\(b\) setting:

- Space group: \(P2/m\) (No. 10)
- \(a=6.542\), \(b=3.489\), \(c=5.934\) Å
- \(\beta=91.476^\circ\)
- \(Z=1\)

The strongest indexing checks are \(100=13.53^\circ\), \(001=14.92^\circ\), \(10\bar1=19.93^\circ\), \(101=20.45^\circ\), \(010=25.51^\circ\), \(200=27.25^\circ\), and \(002=30.10^\circ\). Sulfur coordinates are approximate powder-derived values. Ti and Cr have similar Cu-\(K\alpha\) scattering, so their ordering is the principal surviving ambiguity.

### Primary structure

```cif
data_AgCrTiS4_primary
_audit_creation_method              'Indexed and structure-modelled from supplied powder XRD'
_chemical_name_common               'silver chromium titanium sulfide'
_chemical_formula_structural        'AgCrTiS4'
_chemical_formula_sum               'Ag1 Cr1 Ti1 S4'
_cell_formula_units_Z               1

_cell_length_a                       6.542
_cell_length_b                       3.489
_cell_length_c                       5.934
_cell_angle_alpha                    90
_cell_angle_beta                     91.476
_cell_angle_gamma                    90
_cell_volume                         135.4

_space_group_crystal_system          monoclinic
_space_group_name_H-M_alt            'P 1 2/m 1'
_space_group_IT_number               10

_diffrn_radiation_type               'Cu Kalpha1'
_diffrn_radiation_wavelength         1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y,-z'
3  '-x,-y,-z'
4  'x,-y,z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Ti1 Ti 1 a  0.0000  0.0000  0.0000  1.0
Ag1 Ag 1 c  0.5000  0.0000  0.0000  1.0
Cr1 Cr 1 f  0.0000  0.5000  0.5000  1.0
S1  S  2 m  0.2780  0.0000  0.3270  1.0
S2  S  2 n  0.7220  0.5000  0.1730  1.0
```

### Surviving Ti/Cr-ordering alternative

This model has the same lattice and sulfur framework, with Ti and Cr exchanged between the two transition-metal sites.

```cif
data_AgCrTiS4_TiCr_swapped
_audit_creation_method              'Alternative Ti/Cr ordering from supplied powder XRD'
_chemical_formula_structural        'AgCrTiS4'
_chemical_formula_sum               'Ag1 Cr1 Ti1 S4'
_cell_formula_units_Z               1

_cell_length_a                       6.542
_cell_length_b                       3.489
_cell_length_c                       5.934
_cell_angle_alpha                    90
_cell_angle_beta                     91.476
_cell_angle_gamma                    90

_space_group_crystal_system          monoclinic
_space_group_name_H-M_alt            'P 1 2/m 1'
_space_group_IT_number               10

_diffrn_radiation_wavelength         1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y,-z'
3  '-x,-y,-z'
4  'x,-y,z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Cr1 Cr 1 a  0.0000  0.0000  0.0000  1.0
Ag1 Ag 1 c  0.5000  0.0000  0.0000  1.0
Ti1 Ti 1 f  0.0000  0.5000  0.5000  1.0
S1  S  2 m  0.2780  0.0000  0.3270  1.0
S2  S  2 n  0.7220  0.5000  0.1730  1.0
```

Distinguishing these two ordering models reliably would require neutron diffraction, anomalous XRD, or independent local-chemistry information.
