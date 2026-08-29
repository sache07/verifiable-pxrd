The dominant peaks index as a rock-salt lattice:

| Observed 2θ (°) | Assignment | Calculated 2θ (°) |
|---:|:---:|---:|
| 28.54 | 200 | 28.53 |
| 40.79 | 220 | 40.79 |
| 50.5–50.6 | 222 | 50.53 |
| 59.08 | 400 | 59.07 |
| 66.9 | 420 | 66.9 |
| 74.2–74.4 | 422 | 74.3 |
| 88.3–88.5 | 440 | 88.4 |

This gives \(a \approx 6.251\) Å. The cation site is approximately 80% K and 20% Na, giving \((\mathrm{K}_{0.8}\mathrm{Na}_{0.2})\mathrm{Cl}\), equivalent to K₄NaCl₅.

With Cu radiation, the average cation scattering factor is close to that of Cl. Consequently, odd rock-salt reflections such as 111 and 311 are almost cancelled, explaining their apparent absence. The weak sub-percent features may indicate short-range K/Na ordering, strain, or a minor secondary contribution, but they do not uniquely determine an ordered supercell. The defensible primary result is therefore the disordered average structure.

```cif
data_K4NaCl5_average_rocksalt
_audit_creation_method              'Indexed from supplied powder XRD pattern'
_chemical_name_common               'potassium sodium chloride, K4NaCl5'
_chemical_formula_structural        '(K0.8Na0.2)Cl'
_chemical_formula_sum               'K0.8 Na0.2 Cl'
_cell_formula_units_Z               4

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_cell_length_a                      6.2510(10)
_cell_length_b                      6.2510(10)
_cell_length_c                      6.2510(10)
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        244.3

_space_group_name_H-M_alt           'F m -3 m'
_space_group_IT_number              225

loop_
_atom_type_symbol
_atom_type_oxidation_number
K    1
Na   1
Cl  -1

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Cl1   Cl   4   a   0.000000   0.000000   0.000000   1.000
K1    K    4   b   0.500000   0.500000   0.500000   0.800
Na1   Na   4   b   0.500000   0.500000   0.500000   0.200
```

A CsCl-type model with \(a\approx3.1255\) Å is mathematically close for the dominant peak sequence, but it implies an implausibly small volume and K–Cl distance unless the sample is under extreme pressure. It is therefore not retained as a chemically reasonable alternative.
