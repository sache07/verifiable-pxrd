The pattern indexes as an orthorhombic, approximately pseudocubic superstructure. The diagnostic low-angle reflections are consistent with \(200\), \(020\), and \(002\), giving:

- \(a \approx 12.95\) Å
- \(b \approx 12.73\) Å
- \(c \approx 10.45\) Å
- \(V \approx 1724\) Å³
- \(Z=8\)

The most plausible structure is the orthorhombic **Y₅Sn₃ structure type**, Pearson symbol **oP64**, space group **Pbca (No. 61)**. For example, the observed 400, 040, and 004 reflections occur at approximately 27.53°, 28.00°, and 34.27°, respectively.

The powder pattern determines the cell and structure type much more robustly than the 24 independent positional parameters. Consequently, the coordinates below are a symmetry-compatible, pseudocubic starting model for subsequent Rietveld refinement, rather than single-crystal-quality coordinates.

```cif
data_Y5Sn3_Pbca
_audit_creation_method
'Indexed from supplied Cu Kalpha1 powder pattern; internal coordinates are a Pbca starting model'

_chemical_name_common                    'yttrium tin, Y5Sn3'
_chemical_formula_sum                    'Y40 Sn24'
_chemical_formula_structural             'Y5Sn3'
_cell_formula_units_Z                    8

_cell_length_a                           12.954
_cell_length_b                           12.733
_cell_length_c                           10.453
_cell_angle_alpha                        90
_cell_angle_beta                         90
_cell_angle_gamma                        90
_cell_volume                             1724.3

_space_group_crystal_system              orthorhombic
_space_group_name_H-M_alt                'P b c a'
_space_group_IT_number                   61

_exptl_crystal_density_diffrn            6.17
_diffrn_radiation_wavelength             1.5406

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
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_B_iso_or_equiv
Y1   Y    8 c   0.119  0.132  0.121  1.0  0.50
Y2   Y    8 c   0.137  0.109  0.374  1.0  0.50
Y3   Y    8 c   0.108  0.386  0.132  1.0  0.50
Y4   Y    8 c   0.389  0.127  0.112  1.0  0.50
Y5   Y    8 c   0.116  0.362  0.390  1.0  0.50
Sn1  Sn   8 c   0.366  0.141  0.382  1.0  0.50
Sn2  Sn   8 c   0.395  0.369  0.116  1.0  0.50
Sn3  Sn   8 c   0.371  0.392  0.365  1.0  0.50
```

Representative indexing supporting this assignment:

| \(2\theta_{\rm obs}\) | Approximate reflection |
|---:|:---|
| 13.66° | 200 |
| 13.90° | 020 |
| 16.95° | 002 |
| 19.54° | 220 / overlapping reflections |
| 25.84° | 222 region |
| 27.53° | 400 |
| 28.00° | 040 |
| 30.9° | 420 region |
| 31.28° | 240 region |
| 32.50° | 402 region |
| 34.27° | 004 |
| 35.3–35.7° | 422 / 242 region |

A Mn₅Si₃-type \(P6_3/mcm\) model is not retained: it cannot account naturally for the separate 200/020/002 sequence and their 400/040/004 harmonics.
