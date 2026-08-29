The pattern is best indexed by an **orthorhombically distorted, doubled HfFe₆Ge₆-type superstructure**, Pearson symbol **oC52**, with approximate cell

\[
a=8.780\ \text{Å},\quad b=5.143\ \text{Å},\quad c=15.207\ \text{Å},
\]

in **Cmmm (No. 65), \(Z=4\)**. Representative indexing includes 002 at 11.63°, 200 at 20.21°, 202/004 at 23.38°, 204 at 31.09°, 020 at 34.87°, 220 at 40.64°, 400/206 at 41.08°, and 402 at 42.84°. The metric is close to \(a_o=\sqrt3a_h,\ b_o=a_h,\ c_o=2c_h\).

The internal coordinates below are a parent-derived powder solution; small shifts, particularly along \(c\), should be refined against the complete profile.

### Primary structure: orthorhombic oC52 model

```cif
data_ZrCo6Ge6_oC52
_audit_creation_method              'powder indexing and parent-structure constrained solution'
_chemical_name_common               'zirconium cobalt germanide'
_chemical_formula_structural        'ZrCo6Ge6'
_chemical_formula_sum               'Zr4 Co24 Ge24'
_cell_formula_units_Z               4

_symmetry_cell_setting              orthorhombic
_symmetry_space_group_name_H-M      'C m m m'
_symmetry_Int_Tables_number         65
_space_group_name_H-M_alt           'C m m m'
_space_group_IT_number              65

_cell_length_a                      8.7802
_cell_length_b                      5.1432
_cell_length_c                      15.2074
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        686.5

_diffrn_radiation_probe             x-ray
_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1   'x,y,z'
2   '-x,y,z'
3   'x,-y,z'
4   'x,y,-z'
5   '-x,-y,z'
6   '-x,y,-z'
7   'x,-y,-z'
8   '-x,-y,-z'
9   'x+1/2,y+1/2,z'
10  '-x+1/2,y+1/2,z'
11  'x+1/2,-y+1/2,z'
12  'x+1/2,y+1/2,-z'
13  '-x+1/2,-y+1/2,z'
14  '-x+1/2,y+1/2,-z'
15  'x+1/2,-y+1/2,-z'
16  '-x+1/2,-y+1/2,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_B_iso_or_equiv
Zr1  Zr  2  0.00000  0.00000  0.00000  1.0  0.5
Zr2  Zr  2  0.00000  0.00000  0.50000  1.0  0.5
Co1  Co  4  0.00000  0.50000  0.1260   1.0  0.5
Co2  Co  4  0.00000  0.50000  0.6215   1.0  0.5
Co3  Co  8  0.25000  0.25000  0.1268   1.0  0.5
Co4  Co  8  0.25000  0.25000  0.6260   1.0  0.5
Ge1  Ge  4  0.3333   0.00000  0.00000  1.0  0.5
Ge2  Ge  4  0.3333   0.00000  0.50000  1.0  0.5
Ge3  Ge  8  0.3333   0.00000  0.2505   1.0  0.5
Ge4  Ge  4  0.00000  0.00000  0.1668   1.0  0.5
Ge5  Ge  4  0.00000  0.00000  0.6655   1.0  0.5
```

### Surviving higher-symmetry alternative

A substantial subset of the reflections is also described by the undistorted **HfFe₆Ge₆ parent**, **P6/mmm**, with \(a_h\approx5.070\) Å and \(c_h\approx7.604\) Å. It does not account for all of the weaker/split superstructure reflections as well as the oC52 model.

```cif
data_ZrCo6Ge6_hP13_parent
_audit_creation_method              'higher-symmetry parent alternative'
_chemical_formula_structural        'ZrCo6Ge6'
_chemical_formula_sum               'Zr Co6 Ge6'
_cell_formula_units_Z               1

_symmetry_cell_setting              hexagonal
_symmetry_space_group_name_H-M      'P 6/m m m'
_symmetry_Int_Tables_number         191
_space_group_name_H-M_alt           'P 6/m m m'
_space_group_IT_number              191

_cell_length_a                      5.0696
_cell_length_b                      5.0696
_cell_length_c                      7.6037
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   120
_cell_volume                        169.2

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

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
Zr1  Zr  1  a  0.00000  0.00000  0.00000  1.0  0.5
Co1  Co  6  i  0.50000  0.00000  0.2520   1.0  0.5
Ge1  Ge  2  c  0.33333  0.66667  0.00000  1.0  0.5
Ge2  Ge  2  d  0.33333  0.66667  0.50000  1.0  0.5
Ge3  Ge  2  e  0.00000  0.00000  0.3340   1.0  0.5
```

The **Cmmm oC52 model is the preferred assignment**; the P6/mmm file is primarily useful as a constrained starting model or average structure.
