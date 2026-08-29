The pattern is consistent with a large primitive cubic cell, \(a \approx 10.72\) Å. Combining the indexing, composition, plausible cell density, and known rare-earth-rich \(R_5\)Mg chemistry gives a **Gd\(_5\)Mg-type model**, Pearson symbol **cP36**, space group **\(P\bar{4}3m\) (No. 215)**, as the preferred solution.

Because Mg scatters very weakly relative to Yb with Cu radiation, the internal coordinates are substantially less certain than the lattice and structure type. The CIF below should therefore be regarded as a prototype-constrained starting model for Rietveld refinement.

### Primary CIF

```cif
data_Yb5Mg_primary
_audit_creation_method
'Indexed from supplied Cu Kalpha1 powder pattern; Gd5Mg-type starting model'

_chemical_name_common                 'ytterbium magnesium (5/1)'
_chemical_formula_structural          'Yb5Mg'
_chemical_formula_sum                 'Mg6 Yb30'
_cell_formula_units_Z                 6

_cell_length_a                        10.720(15)
_cell_length_b                        10.720(15)
_cell_length_c                        10.720(15)
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90
_cell_volume                          1231.9(5)

_space_group_name_H-M_alt             'P -4 3 m'
_space_group_IT_number                215

_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

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
Yb1  Yb   6  f   0.2491  0       0       1.0  0.8
Yb2  Yb  12  h   0.1667  0.5     0       1.0  0.8
Yb3  Yb  12  i   0.3742  0.3742  0       1.0  0.8
Mg1  Mg   6  g   0.2510  0.5     0.5     1.0  1.0
```

The cubic indexing is supported particularly by the low-angle groups near 14.4°, 16.5°, 18.5°, 25.0°, 27.5°, 29.1°, 31.2°, and 33.4°, and by their higher-angle repetitions. Some peak positions are displaced from an exact cubic metric by more than expected from counting statistics, which may indicate unresolved splitting, anisotropic strain, or a symmetry-lowered derivative.

### Surviving lower-symmetry alternative

A primitive chiral, filled-\(\beta\)-Mn derivative in \(P2_13\), with the same approximate metric, is the main alternative. It has a less favorable cell density and is therefore not preferred, but powder data alone may not cleanly distinguish it without a full profile refinement.

```cif
data_Yb5Mg_alternative_P213
_audit_creation_method
'Lower-symmetry filled-beta-Mn alternative; prototype starting coordinates'

_chemical_name_common                 'ytterbium magnesium (5/1)'
_chemical_formula_structural          'Yb5Mg'
_chemical_formula_sum                 'Mg4 Yb20'
_cell_formula_units_Z                 4

_cell_length_a                        10.720(15)
_cell_length_b                        10.720(15)
_cell_length_c                        10.720(15)
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90

_space_group_name_H-M_alt             'P 21 3'
_space_group_IT_number                198

_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

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
Mg1  Mg   4  a   0.3750  0.3750  0.3750  1.0  1.0
Yb1  Yb   4  a   0.0635  0.0635  0.0635  1.0  0.8
Yb2  Yb   4  a   0.5635  0.5635  0.5635  1.0  0.8
Yb3  Yb  12  b   0.1250  0.2020  0.4520  1.0  0.8
```

**Recommended primary assignment:** Gd\(_5\)Mg-type, \(P\bar{4}3m\), \(a=10.72(2)\) Å. The Yb/Mg site assignment is robust from stoichiometry, while the positional parameters should be refined against the full profile.
