The pattern indexes as a primitive tetragonal, cation-ordered fluorite derivative:

- Space group: **P4/mmm** (No. 123)
- \(a = 3.9285(3)\) Å, \(c = 5.6150(5)\) Å, \(Z=1\)
- Representative indexing: 15.77° (001), 22.62° (100), 27.69° (101), 31.85° (002), 32.20° (110), 45.92° (112), and 46.18° (200).
- O and F are modeled as statistically mixed on the fluorite-anion site. Their ordering cannot be determined reliably from Cu Kα X-ray data because their scattering factors are very similar.

```cif
data_YBiO2F2_average
_audit_creation_method              'Structure solution from powder XRD'
_chemical_name_common               'Yttrium bismuth oxide fluoride'
_chemical_formula_structural        'YBi(OF)2'
_chemical_formula_sum               'Bi1 F2 O2 Y1'
_chemical_formula_weight            367.88
_cell_formula_units_Z               1

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_cell_length_a                      3.9285(3)
_cell_length_b                      3.9285(3)
_cell_length_c                      5.6150(5)
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        86.657(15)

_space_group_crystal_system         tetragonal
_space_group_name_H-M_alt           'P 4/m m m'
_space_group_IT_number              123

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1   'x,y,z'
2   '-y,x,z'
3   '-x,-y,z'
4   'y,-x,z'
5   '-x,y,z'
6   'x,-y,z'
7   'y,x,z'
8   '-y,-x,z'
9   'x,y,-z'
10  '-y,x,-z'
11  '-x,-y,-z'
12  'y,-x,-z'
13  '-x,y,-z'
14  'x,-y,-z'
15  'y,x,-z'
16  '-y,-x,-z'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Bi  3
Y   3
O  -2
F  -1

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Bi1  Bi  1  a  0.00000  0.00000  0.00000  1.000  0.010
Y1   Y   1  d  0.50000  0.50000  0.50000  1.000  0.010
O1   O   4  i  0.00000  0.50000  0.25000  0.500  0.015
F1   F   4  i  0.00000  0.50000  0.25000  0.500  0.015

_refine_special_details
;
Average tetragonal cation-ordered fluorite structure. The refined metric
corresponds to a pseudocubic fluorite cell with a_pc = sqrt(2)*a =
5.5557 A and c/a_pc = 1.0107. O and F occupy the same average anion
site with equal occupancy. The powder pattern does not uniquely
determine local O/F ordering or small departures of the anion z
coordinate from 1/4.
;
```

Specific O/F-ordered lower-symmetry variants remain possible, but the supplied X-ray pattern does not select a unique ordered arrangement; the CIF above is therefore the appropriate primary average structure.
