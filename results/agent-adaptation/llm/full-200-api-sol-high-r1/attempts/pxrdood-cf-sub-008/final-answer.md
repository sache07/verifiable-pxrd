## Primary solution

The pattern indexes on a hexagonal/trigonal cell with:

- \(a \approx 2.8985\) Å
- \(c \approx 12.1725\) Å
- \(Z=1\)
- space group \(P\overline{3}m1\) (No. 164)

The heavy-atom framework has an approximate \(c/2\) translation. Ordering one Li layer in every second interlayer gap removes that translation and permits the very weak 001 reflection near \(7.25^\circ\). The principal indexing is:

| \(2\theta\) (°) | hkl |
|---:|:---|
| 7.25 | 001, very weak |
| 14.54 | 002 |
| 29.33 | 004 |
| 35.75 | 100 |
| 36.52 | 101 |
| 38.78 | 102 |
| 42.31 | 103 |
| 44.63 | 006 |
| 46.88 | 104 |
| 52.31 | 105 |
| 58.45 | 106 |
| 64.23 | 110 |
| 65.22 | 107 |
| 66.24 | 112 |

The sulfur coordinate is estimated from the intensity sequence as \(z_{\rm S}\approx0.1465\), with an uncertainty of roughly 0.002–0.003.

```cif
data_Li_Nb2_S4_primary
_audit_creation_method              'Structure solution from powder XRD'
_chemical_name_common               'stage-2 lithium niobium sulfide'
_chemical_formula_sum               'Li Nb2 S4'
_chemical_formula_structural        'Li(NbS2)2'
_cell_formula_units_Z               1

_cell_length_a                      2.8985
_cell_length_b                      2.8985
_cell_length_c                      12.1725
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   120
_cell_volume                        88.565

_space_group_name_H-M_alt           'P -3 m 1'
_space_group_IT_number              164

_diffrn_radiation_probe             x-ray
_diffrn_radiation_wavelength        1.5406

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Li1  Li  0.000000  0.000000  0.000000  1.000
Nb1  Nb  0.333333  0.666667  0.250000  1.000
S1   S   0.000000  0.000000  0.146500  1.000
S2   S   0.000000  0.000000  0.646500  1.000
```

Here the symmetry generates the second Nb at \((2/3,1/3,3/4)\) and sulfur layers at \(z=0.3535\) and \(0.8535\).

## Surviving Li-site alternative

Cu Kα X-rays constrain the Nb/S framework well but only weakly constrain the lateral Li position. A chemically plausible off-axis Li site lowers the symmetry to \(P3m1\) while giving almost the same XRD pattern. The two possible off-axis Li domains are related by inversion/twinning.

```cif
data_Li_Nb2_S4_Li_off_axis
_audit_creation_method              'Li-site alternative from powder XRD'
_chemical_formula_sum               'Li Nb2 S4'
_chemical_formula_structural        'Li(NbS2)2'
_cell_formula_units_Z               1

_cell_length_a                      2.8985
_cell_length_b                      2.8985
_cell_length_c                      12.1725
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   120
_cell_volume                        88.565

_space_group_name_H-M_alt           'P 3 m 1'
_space_group_IT_number              156

_diffrn_radiation_probe             x-ray
_diffrn_radiation_wavelength        1.5406

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Li1  Li  0.333333  0.666667  0.000000  1.000
Nb1  Nb  0.333333  0.666667  0.250000  1.000
Nb2  Nb  0.666667  0.333333  0.750000  1.000
S1   S   0.000000  0.000000  0.146500  1.000
S2   S   0.000000  0.000000  0.353500  1.000
S3   S   0.000000  0.000000  0.646500  1.000
S4   S   0.000000  0.000000  0.853500  1.000
```

The \(P\overline{3}m1\) model is the preferred powder-XRD solution; neutron diffraction would be needed to distinguish the Li-site alternatives reliably.
