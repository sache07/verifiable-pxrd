The pattern indexes as a body-centered tetragonal, zinc-blende-derived superstructure. The diagnostic reflections are approximately 002 at 15.27°, 101 at 17.07°, 110 at 21.64°, and 112 at 26.59°. The strongest higher-angle overlap, 220/204, occurs near 44.11°. These give:

- \(a = 5.804(1)\) Å
- \(c = 11.596(2)\) Å
- \(c/2a = 0.9990\)
- Space group \(I\overline{4}2m\) (No. 121)
- Stannite-type cation ordering
- \(Z=2\)

The selenium coordinates are very close to the ideal tetrahedral values \(x=0.25,\ z=0.125\). The powder data do not reliably distinguish Au and In interchange between the 2a and 2b sites, so that interchange is retained as an alternative.

### Primary CIF

```cif
data_Zn2InAuSe4_stannite
_audit_creation_method              'Indexed and modeled from supplied Cu Kalpha1 powder pattern'
_chemical_name_common               'zinc indium gold selenide'
_chemical_formula_structural        'Zn2InAuSe4'
_chemical_formula_sum               'Au1 In1 Se4 Zn2'
_cell_formula_units_Z               2

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_space_group_crystal_system         tetragonal
_space_group_name_H-M_alt           'I -4 2 m'
_space_group_IT_number              121

_cell_length_a                      5.8040(10)
_cell_length_b                      5.8040(10)
_cell_length_c                      11.5960(20)
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        390.63(16)

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1   'x,y,z'
2   '-x,-y,z'
3   'y,-x,-z'
4   '-y,x,-z'
5   'x,-y,-z'
6   '-x,y,-z'
7   'y,x,z'
8   '-y,-x,z'
9   'x+1/2,y+1/2,z+1/2'
10  '-x+1/2,-y+1/2,z+1/2'
11  'y+1/2,-x+1/2,-z+1/2'
12  '-y+1/2,x+1/2,-z+1/2'
13  'x+1/2,-y+1/2,-z+1/2'
14  '-x+1/2,y+1/2,-z+1/2'
15  'y+1/2,x+1/2,z+1/2'
16  '-y+1/2,-x+1/2,z+1/2'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Au   1
In   3
Zn   2
Se  -2

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
Au1  Au  a  2  0.0000  0.0000  0.0000  1.000  0.8
In1  In  b  2  0.0000  0.0000  0.5000  1.000  0.8
Zn1  Zn  d  4  0.0000  0.5000  0.2500  1.000  0.8
Se1  Se  i  8  0.2500  0.2500  0.1250  1.000  0.8
```

### Surviving Au/In site-interchange alternative

This model has the same cell, space group, and selenium framework. With nearly ideal Se coordinates, conventional powder intensities are close to homometric for this interchange.

```cif
data_Zn2InAuSe4_stannite_AuIn_swapped
_audit_creation_method              'Au/In site-interchange alternative'
_chemical_formula_structural        'Zn2InAuSe4'
_chemical_formula_sum               'Au1 In1 Se4 Zn2'
_cell_formula_units_Z               2

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_space_group_crystal_system         tetragonal
_space_group_name_H-M_alt           'I -4 2 m'
_space_group_IT_number              121

_cell_length_a                      5.8040(10)
_cell_length_b                      5.8040(10)
_cell_length_c                      11.5960(20)
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90

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
In1  In  a  2  0.0000  0.0000  0.0000  1.000  0.8
Au1  Au  b  2  0.0000  0.0000  0.5000  1.000  0.8
Zn1  Zn  d  4  0.0000  0.5000  0.2500  1.000  0.8
Se1  Se  i  8  0.2500  0.2500  0.1250  1.000  0.8
```

The first model is preferred on the usual stannite chemical-ordering convention: the lower-valent Au site is 2a and the higher-valent In site is 2b. Resonant/anomalous diffraction near an Au or In absorption edge would be needed to determine that ordering unambiguously.
