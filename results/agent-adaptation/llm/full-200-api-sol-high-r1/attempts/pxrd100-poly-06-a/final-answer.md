The composition is interpreted as **LiNi₂O₄**. The reflection envelopes index as a strongly distorted spinel:

- the cubic-spinel 111 reflection splits into four components near 18.79, 18.91, 18.98, and 19.15°;
- the three axial 400-type reflections occur near 44.01, 44.44, and 45.65°;
- the 220 family is reproduced near 30.85–31.72°.

This gives a pseudo-cubic triclinic metric of approximately  
\(a=8.2247\), \(b=8.1483\), \(c=7.9445\) Å,  
\(\alpha=90.964^\circ\), \(\beta=90.658^\circ\), \(\gamma=90.118^\circ\).

The primary CIF below is a **P-1 metric-distorted normal-spinel model**, with Li tetrahedral, Ni octahedral, and atomic coordinates constrained to the parent spinel topology. The powder data establish the metric and topology much more securely than the individual low-symmetry atomic displacements, especially for Li.

### Primary structure: triclinically distorted LiNi₂O₄ spinel

```cif
data_LiNi2O4_triclinic_distorted_spinel
_audit_creation_method            'Powder indexing; coordinates constrained to spinel parent'
_chemical_name_common             'triclinically distorted lithium nickel oxide spinel'
_chemical_formula_structural      'LiNi2O4'
_chemical_formula_sum             'Li Ni2 O4'
_cell_formula_units_Z             8

_cell_length_a                    8.2247
_cell_length_b                    8.1483
_cell_length_c                    7.9445
_cell_angle_alpha                 90.964
_cell_angle_beta                  90.658
_cell_angle_gamma                 90.118

_space_group_name_H-M_alt         'P -1'
_space_group_IT_number            2

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_B_iso_or_equiv
Li01 Li  0.125000  0.125000  0.125000  1.0  0.50
Li02 Li  0.125000  0.625000  0.625000  1.0  0.50
Li03 Li  0.625000  0.125000  0.625000  1.0  0.50
Li04 Li  0.625000  0.625000  0.125000  1.0  0.50

Ni01 Ni  0.500000  0.500000  0.500000  1.0  0.50
Ni02 Ni  0.500000  0.000000  0.000000  1.0  0.50
Ni03 Ni  0.000000  0.500000  0.000000  1.0  0.50
Ni04 Ni  0.000000  0.000000  0.500000  1.0  0.50
Ni05 Ni  0.500000  0.250000  0.250000  1.0  0.50
Ni06 Ni  0.000000  0.250000  0.750000  1.0  0.50
Ni07 Ni  0.250000  0.500000  0.250000  1.0  0.50
Ni08 Ni  0.250000  0.000000  0.750000  1.0  0.50
Ni09 Ni  0.250000  0.250000  0.500000  1.0  0.50
Ni10 Ni  0.250000  0.750000  0.000000  1.0  0.50

O01  O   0.261000  0.261000  0.261000  1.0  0.70
O02  O   0.261000  0.761000  0.761000  1.0  0.70
O03  O   0.761000  0.261000  0.761000  1.0  0.70
O04  O   0.761000  0.761000  0.261000  1.0  0.70
O05  O   0.261000  0.989000  0.989000  1.0  0.70
O06  O   0.261000  0.489000  0.489000  1.0  0.70
O07  O   0.761000  0.989000  0.489000  1.0  0.70
O08  O   0.761000  0.489000  0.989000  1.0  0.70
O09  O   0.989000  0.261000  0.989000  1.0  0.70
O10  O   0.989000  0.761000  0.489000  1.0  0.70
O11  O   0.489000  0.261000  0.489000  1.0  0.70
O12  O   0.489000  0.761000  0.989000  1.0  0.70
O13  O   0.989000  0.989000  0.261000  1.0  0.70
O14  O   0.989000  0.489000  0.761000  1.0  0.70
O15  O   0.489000  0.989000  0.761000  1.0  0.70
O16  O   0.489000  0.489000  0.261000  1.0  0.70
```

### Surviving average-structure alternative

If the splitting is produced by coherent domains, anisotropic strain, or closely related polymorphs rather than a homogeneous triclinic distortion, the corresponding average structure is the normal cubic spinel:

```cif
data_LiNi2O4_cubic_average_spinel
_audit_creation_method            'Average parent structure of triclinic powder solution'
_chemical_name_common             'lithium nickel oxide spinel'
_chemical_formula_structural      'LiNi2O4'
_chemical_formula_sum             'Li Ni2 O4'
_cell_formula_units_Z             8

_cell_length_a                    8.1050
_cell_length_b                    8.1050
_cell_length_c                    8.1050
_cell_angle_alpha                 90
_cell_angle_beta                  90
_cell_angle_gamma                 90

_space_group_name_H-M_alt         'F d -3 m'
_space_group_IT_number            227

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
Li1 Li  8   a  0.125000  0.125000  0.125000  1.0  0.50
Ni1 Ni  16  d  0.500000  0.500000  0.500000  1.0  0.50
O1  O   32  e  0.261000  0.261000  0.261000  1.0  0.70
```

The cubic model captures the average peak positions but not the extensive resolved splitting, so the triclinic distorted-spinel model is the preferred interpretation.
