The peak positions index best on a primitive monoclinic cell. The diagnostic low-angle indexing is:

| 2θ observed (°) | hkl |
|---:|:---|
| 9.93 | 100 |
| 11.97 | 001 |
| 15.35 | 101 |
| 15.79 | 10−1 |
| 19.93 | 200 |
| 23.01 | 201 |
| 23.60 | 20−1 |
| 24.07 | 002 |
| 25.84 | 102 |
| 26.72 | 010 |
| 30.09 | 300 |
| 30.99 | 202 |
| 31.89 | 20−2 |

This gives approximately \(a=8.906\), \(b=3.334\), \(c=7.391\) Å and \(\beta=88.36^\circ\). The most plausible symmetry and content are **P2/m, mP16, Z = 2**, with all atoms on the two mirror planes. The lattice assignment is considerably more secure than the individual coordinates; the latter should be regarded as a direct-space starting model for Rietveld refinement.

### Primary CIF

```cif
data_Nb6PdPt_primary
_audit_creation_method
;Powder indexing and constrained direct-space model.
 Cu Kalpha1 wavelength = 1.5406 Angstrom.
 Atomic coordinates should be refined against the original profile.
;

_chemical_name_common                  'niobium palladium platinum'
_chemical_formula_sum                  'Nb12 Pd2 Pt2'
_chemical_formula_structural           'Nb6PdPt'
_cell_formula_units_Z                   2

_cell_length_a                          8.906
_cell_length_b                          3.334
_cell_length_c                          7.391
_cell_angle_alpha                       90
_cell_angle_beta                        88.36
_cell_angle_gamma                       90
_cell_volume                            219.4

_symmetry_space_group_name_H-M          'P 2/m'
_symmetry_Int_Tables_number             10
_space_group_crystal_system             monoclinic
_space_group_IT_number                  10
_space_group_name_H-M_alt               'P 1 2/m 1'

_diffrn_radiation_type                  'Cu Kalpha1'
_diffrn_radiation_wavelength            1.5406

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
_atom_site_U_iso_or_equiv
Nb1  Nb  2  m  0.0832  0.0000  0.1765  1.0  0.006
Nb2  Nb  2  m  0.2168  0.0000  0.3895  1.0  0.006
Nb3  Nb  2  m  0.3631  0.0000  0.0712  1.0  0.006
Nb4  Nb  2  n  0.1024  0.5000  0.6820  1.0  0.006
Nb5  Nb  2  n  0.2577  0.5000  0.8890  1.0  0.006
Nb6  Nb  2  n  0.4215  0.5000  0.5730  1.0  0.006
Pd1  Pd  2  m  0.4680  0.0000  0.3260  1.0  0.005
Pt1  Pt  2  n  0.4685  0.5000  0.8270  1.0  0.005
```

### Surviving ordering alternative

The principal chemically plausible alternative is interchange of Pd and Pt between the two multiplicity-two sites:

```cif
data_Nb6PdPt_PdPt_swapped
_chemical_formula_sum                  'Nb12 Pd2 Pt2'
_chemical_formula_structural           'Nb6PdPt'
_cell_formula_units_Z                   2

_cell_length_a                          8.906
_cell_length_b                          3.334
_cell_length_c                          7.391
_cell_angle_alpha                       90
_cell_angle_beta                        88.36
_cell_angle_gamma                       90

_symmetry_space_group_name_H-M          'P 2/m'
_symmetry_Int_Tables_number             10

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
_atom_site_U_iso_or_equiv
Nb1  Nb  2  m  0.0832  0.0000  0.1765  1.0  0.006
Nb2  Nb  2  m  0.2168  0.0000  0.3895  1.0  0.006
Nb3  Nb  2  m  0.3631  0.0000  0.0712  1.0  0.006
Nb4  Nb  2  n  0.1024  0.5000  0.6820  1.0  0.006
Nb5  Nb  2  n  0.2577  0.5000  0.8890  1.0  0.006
Nb6  Nb  2  n  0.4215  0.5000  0.5730  1.0  0.006
Pt1  Pt  2  m  0.4680  0.0000  0.3260  1.0  0.005
Pd1  Pd  2  n  0.4685  0.5000  0.8270  1.0  0.005
```

The cell and monoclinic symmetry are strongly supported by the peak positions. The positional parameters and Pd/Pt ordering remain the portions most in need of whole-pattern Rietveld refinement.
