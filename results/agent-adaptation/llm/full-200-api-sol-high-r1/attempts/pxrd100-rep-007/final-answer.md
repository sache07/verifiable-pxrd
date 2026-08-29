The pattern indexes as a **primitive hexagonal CaCu₅-type structure**, space group **P6/mmm (No. 191)**. The refined lattice parameters are approximately:

- \(a = 5.0054(4)\) Å  
- \(c = 3.9170(5)\) Å  
- \(V = 84.989\) Å³, \(Z=1\)

Representative indexing is: 100 at 20.47°, 001 at 22.68°, 101 at 30.74°, 110 at 35.85°, 200 at 41.64°, 111 at 42.85°, 002 at 46.32°, and 201 at 47.93°.

The average atomic framework is unambiguous. Ni and Zn have weak Cu Kα scattering contrast, so their partition between the 2c and 3g transition-metal sites is less certain. The slightly stronger 001 and cancellation-sensitive reflections favor **Zn disorder on 2c**; that is the primary model below. The alternative with Zn on 3g is also given.

## Primary CIF — Zn/Ni disorder on 2c

```cif
data_CeNi4Zn_primary
_audit_creation_method              'Powder-pattern indexing and CaCu5-type structure assignment'
_chemical_name_common               'cerium nickel zinc'
_chemical_formula_structural        'CeNi4Zn'
_chemical_formula_sum               'Ce1 Ni4 Zn1'
_cell_formula_units_Z               1

_symmetry_space_group_name_H-M       'P 6/m m m'
_space_group_name_H-M_alt           'P 6/m m m'
_space_group_IT_number              191

_cell_length_a                       5.0054(4)
_cell_length_b                       5.0054(4)
_cell_length_c                       3.9170(5)
_cell_angle_alpha                    90
_cell_angle_beta                     90
_cell_angle_gamma                    120
_cell_volume                         84.989(18)

_exptl_crystal_density_diffrn        8.602
_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength         1.5406

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Ce1  Ce  1a  0.000000  0.000000  0.000000  1.000000
Ni1  Ni  2c  0.333333  0.666667  0.000000  0.500000
Zn1  Zn  2c  0.333333  0.666667  0.000000  0.500000
Ni2  Ni  3g  0.500000  0.000000  0.500000  1.000000
```

This gives, per unit cell, Ce₁Ni₄Zn₁.

## Surviving occupational alternative — Zn/Ni disorder on 3g

```cif
data_CeNi4Zn_Zn_on_3g_alternative
_audit_creation_method              'Occupational alternative consistent with the powder peak positions'
_chemical_name_common               'cerium nickel zinc'
_chemical_formula_structural        'CeNi4Zn'
_chemical_formula_sum               'Ce1 Ni4 Zn1'
_cell_formula_units_Z               1

_symmetry_space_group_name_H-M       'P 6/m m m'
_space_group_name_H-M_alt           'P 6/m m m'
_space_group_IT_number              191

_cell_length_a                       5.0054(4)
_cell_length_b                       5.0054(4)
_cell_length_c                       3.9170(5)
_cell_angle_alpha                    90
_cell_angle_beta                     90
_cell_angle_gamma                    120
_cell_volume                         84.989(18)

_exptl_crystal_density_diffrn        8.602
_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength         1.5406

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Ce1  Ce  1a  0.000000  0.000000  0.000000  1.000000
Ni1  Ni  2c  0.333333  0.666667  0.000000  1.000000
Ni2  Ni  3g  0.500000  0.000000  0.500000  0.666667
Zn1  Zn  3g  0.500000  0.000000  0.500000  0.333333
```

The lattice and CaCu₅ framework are secure; distinguishing these occupational models would benefit from neutron diffraction or anomalous/synchrotron XRD near the Zn absorption edge.
