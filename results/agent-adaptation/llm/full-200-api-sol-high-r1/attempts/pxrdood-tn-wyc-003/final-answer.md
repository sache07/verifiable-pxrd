The peak positions index most closely as a slightly tetragonally distorted body-centred lattice:

| Observed 2θ (°) | Approximate assignment |
|---:|---|
| 33.81 | 110, with 101 nearly coincident |
| 60.04 | 112 |
| 60.49 | 211 / overlapping component |
| 70.72 | 202 |
| 71.12 | 220 |
| 80.72 | unresolved 103/301/310 group |

The 112/202 shifts give \(a^2/c^2 \approx 0.980\), hence \(c/a\approx1.010\). The resulting average cell is \(a\approx3.746\) Å and \(c\approx3.783\) Å.

## Primary average structure CIF

```cif
data_Au_bct_average
_audit_creation_method              'Indexed from supplied Cu Kalpha1 powder pattern'
_chemical_name_common               'body-centred tetragonal gold, average structure'
_chemical_formula_structural        'Au'
_chemical_formula_sum               'Au'
_cell_formula_units_Z               2

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_space_group_name_H-M_alt           'I 4/m m m'
_space_group_IT_number              139

_cell_length_a                      3.7463
_cell_length_b                      3.7463
_cell_length_c                      3.7834
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        53.10

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,z'
3  '-y,x,z'
4  'y,-x,z'
5  '-x,y,-z'
6  'x,-y,-z'
7  'y,x,-z'
8  '-y,-x,-z'
9  'x+1/2,y+1/2,z+1/2'
10 '-x+1/2,-y+1/2,z+1/2'
11 '-y+1/2,x+1/2,z+1/2'
12 'y+1/2,-x+1/2,z+1/2'
13 '-x+1/2,y+1/2,-z+1/2'
14 'x+1/2,-y+1/2,-z+1/2'
15 'y+1/2,x+1/2,-z+1/2'
16 '-y+1/2,-x+1/2,-z+1/2'

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
Au1 Au 2 a 0 0 0 1.0 0.005
```

### Important qualification

This is an **average positional solution**, not an unambiguous full structure solution. Ideal \(I4/mmm\) Au should also produce 002 and 200 peaks near approximately 48.1° and 48.6° 2θ, respectively; these are absent from the supplied pattern. That absence indicates either:

- a more complex extinction-bearing Au superstructure,
- very strong texture/non-random sampling, or
- more than one closely related phase, as also suggested by the duplicated peaks near 60° and 71°.

The available six peak groups determine the pseudo-body-centred tetragonal metric well, but do not provide enough independent intensities to determine a unique multi-atom superstructure without fabricating atomic coordinates.
