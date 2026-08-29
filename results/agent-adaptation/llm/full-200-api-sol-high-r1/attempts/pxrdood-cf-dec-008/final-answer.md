The pattern indexes on a primitive hexagonal cell with approximately:

- \(a = 5.557\) Å
- \(c = 4.468\) Å
- \(V \approx 119.5\) Å³
- \(Z=1\)

Representative indexing is 100, 001, 101, 110, 200, 111, 002, 201, 102, 210, … for peaks at 18.42°, 19.86°, 27.21°, 32.18°, 37.34°, 38.11°, 40.34°, 42.64°, 44.69°, and 50.10° 2θ.

The preferred structural model is trigonal \(P\overline{3}m1\), with N and Bi on the two axial special positions and Ti on a sixfold orbit. The Ti coordinates are approximate because Cu X-ray data are comparatively insensitive to N and because no instrumental/profile model was supplied.

### Primary structure: `Ti6BiN_P-3m1.cif`

```cif
data_Ti6BiN_primary
_audit_creation_method                'Indexed and fitted from supplied Cu Kalpha1 powder pattern'
_chemical_name_common                 'titanium bismuth nitride'
_chemical_formula_sum                 'Ti6 Bi N'
_chemical_formula_structural          'Ti6BiN'
_cell_formula_units_Z                 1

_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

_space_group_name_H-M_alt             'P -3 m 1'
_space_group_IT_number                164

_cell_length_a                        5.5570
_cell_length_b                        5.5570
_cell_length_c                        4.4675
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     120
_cell_volume                          119.47

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_Wyckoff_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
N1    N     1a   1   0.0000   0.0000   0.0000   1.0
Bi1   Bi    1b   1   0.0000   0.0000   0.5000   1.0
Ti1   Ti    6i   6   0.1900   0.8100   0.0610   1.0
```

The corresponding six Ti positions are generated as two symmetry-related Ti\(_3\) triangles at approximately \(z=0.061\) and \(z=0.939\).

A higher-symmetry limiting model, in which the Ti layers collapse onto the N plane, cannot be eliminated conclusively from the powder data alone.

### Surviving alternative: `Ti6BiN_P6mmm.cif`

```cif
data_Ti6BiN_alternative_P6mmm
_audit_creation_method                'Higher-symmetry limiting model from supplied powder pattern'
_chemical_formula_sum                 'Ti6 Bi N'
_chemical_formula_structural          'Ti6BiN'
_cell_formula_units_Z                 1

_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

_space_group_name_H-M_alt             'P 6/m m m'
_space_group_IT_number                191

_cell_length_a                        5.5570
_cell_length_b                        5.5570
_cell_length_c                        4.4675
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     120
_cell_volume                          119.47

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_Wyckoff_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
N1    N     1a   1   0.0000   0.0000   0.0000   1.0
Bi1   Bi    1b   1   0.0000   0.0000   0.5000   1.0
Ti1   Ti    6j   6   0.1900   0.3800   0.0000   1.0
```

The \(P\overline{3}m1\) model is preferred because the nonzero Ti \(z\) displacement better accounts for the relative intensities of reflections having the same \(hk\) indices but different \(l\). Neutron diffraction or total-scattering data would be needed to determine the N environment and Ti displacement reliably.
