The pattern indexes on a nearly cubic primitive cell with a strong pseudo-body-centering condition. The dominant indexing is:

| 2θ (°) | hkl |
|---:|:---|
| 19.48 | 110 |
| 27.7 | 200 |
| 34.1 | 211 |
| 39.56 | 220 |
| 44.4 | 310 |
| 53.2 | 321 |
| 57.1 | 400 |
| 60.8 | 330/411 |
| 64.6 | 420 |
| 68.3 | 332 |
| 71.8 | 422 |

The average cell is \(a\approx6.44\) Å. The composition and reflection statistics are consistent with a cP20 \(P\bar{4}3m\) model containing an N-centered Mn octahedron and twelve oxygen positions. The asymmetric shoulders can be represented by a small orthorhombic distortion; that alternative is provided after the primary CIF.

### Primary structure: cubic average model

```cif
data_Mn7NO12_primary
_audit_creation_method             'powder indexing and constrained direct-space model'
_chemical_name_common              'manganese oxynitride, average cubic structure'
_chemical_formula_sum              'Mn7 N O12'
_chemical_formula_structural       'Mn7NO12'
_cell_formula_units_Z              1

_cell_length_a                     6.4400
_cell_length_b                     6.4400
_cell_length_c                     6.4400
_cell_angle_alpha                  90
_cell_angle_beta                   90
_cell_angle_gamma                  90
_cell_volume                       267.09

_space_group_name_H-M_alt          'P -4 3 m'
_space_group_IT_number             215

_exptl_crystal_density_diffrn      3.67
_diffrn_radiation_type             'Cu Kalpha1'
_diffrn_radiation_wavelength       1.5406

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_Wyckoff_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_B_iso_or_equiv
Mn1  Mn  1a   1  0.0000  0.0000  0.0000  1.0  0.50
N1   N   1b   1  0.5000  0.5000  0.5000  1.0  0.70
Mn2  Mn  6g   6  0.2050  0.5000  0.5000  1.0  0.50
O1   O   12i 12  0.3525  0.3525  0.2950  1.0  0.80
```

This gives Mn–N ≈ 1.90 Å and edge-bridging Mn–O distances near 1.88–1.95 Å in the Mn\(_6\)NO\(_{12}\) unit.

### Surviving alternative: weak orthorhombic distortion

The repeatable low-angle shoulders can instead be fitted by approximately

\[
a=6.494,\quad b=6.454,\quad c=6.426\ {\rm Å}.
\]

A symmetry-lowered \(P222\) realization of the same structural model is:

```cif
data_Mn7NO12_orthorhombic_alternative
_audit_creation_method             'orthorhombically distorted derivative of cubic model'
_chemical_formula_sum              'Mn7 N O12'
_chemical_formula_structural       'Mn7NO12'
_cell_formula_units_Z              1

_cell_length_a                     6.4940
_cell_length_b                     6.4540
_cell_length_c                     6.4260
_cell_angle_alpha                  90
_cell_angle_beta                   90
_cell_angle_gamma                  90
_cell_volume                       269.35

_space_group_name_H-M_alt          'P 2 2 2'
_space_group_IT_number             16

_diffrn_radiation_type             'Cu Kalpha1'
_diffrn_radiation_wavelength       1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,z'
3  '-x,y,-z'
4  'x,-y,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_B_iso_or_equiv
Mn1  Mn  1  0.0000  0.0000  0.0000  1.0  0.50
N1   N   1  0.5000  0.5000  0.5000  1.0  0.70
Mn2  Mn  2  0.2050  0.5000  0.5000  1.0  0.50
Mn3  Mn  2  0.5000  0.2050  0.5000  1.0  0.50
Mn4  Mn  2  0.5000  0.5000  0.2050  1.0  0.50
O1   O   4  0.3525  0.3525  0.2950  1.0  0.80
O2   O   4  0.3525  0.2950  0.3525  1.0  0.80
O3   O   4  0.2950  0.3525  0.3525  1.0  0.80
```

The cubic model should be treated as the primary average structure. The powder pattern strongly determines the cell and heavy-atom framework, but Cu X-ray data alone constrain the N position and individual oxygen coordinates considerably less strongly than the Mn substructure.
