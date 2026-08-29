The pattern indexes as a **primitive tetragonal CaBe₂Ge₂-type structure**, space group **P4/nmm (No. 129)**. The refined metric is approximately:

- \(a = 4.399(2)\) Å
- \(c = 10.036(5)\) Å
- \(V \approx 194.2\) Å³

Representative indexing is 001 at 8.80°, 002 at 17.66°, 101 at 22.05°, 003/102 at 26.63/26.93°, 110 at 28.68°, 111 at 30.05°, 103/112 at 33.63/33.88°, 004 at 35.75°, and 200 at 41.00°. The absence of 100 and presence of 110 support the P4/nmm assignment.

Cu X-rays cannot reliably distinguish La from Ce because their scattering factors are nearly identical. The primary CIF therefore uses a 1:1 La/Ce mixed rare-earth site. Internal \(z\) coordinates are approximate and should not be interpreted as single-crystal precision.

### Primary structure: disordered P4/nmm average model

```cif
data_LaCeGe4Pt4_average
_audit_creation_method
'Powder indexing and CaBe2Ge2-type prototype fit'
_chemical_formula_sum                 'La1 Ce1 Ge4 Pt4'
_chemical_formula_weight              1349.88
_cell_formula_units_Z                 1

_cell_length_a                        4.3993
_cell_length_b                        4.3993
_cell_length_c                        10.036
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90
_cell_volume                          194.2

_space_group_name_H-M_alt             'P 4/n m m'
_space_group_IT_number                129

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
La1   La   2   c   0.25000   0.25000   0.2500   0.500
Ce1   Ce   2   c   0.25000   0.25000   0.2500   0.500
Pt1   Pt   2   a   0.75000   0.25000   0.0000   1.000
Pt2   Pt   2   c   0.25000   0.25000   0.6250   1.000
Ge1   Ge   2   b   0.75000   0.25000   0.5000   1.000
Ge2   Ge   2   c   0.25000   0.25000   0.8750   1.000
```

### Surviving alternative: ordered La/Ce model

An ordered arrangement in which the two rare-earth layers are respectively La and Ce lowers the symmetry to approximately **P4mm (No. 99)**. Its powder pattern is effectively indistinguishable from the average model because La and Ce differ by only one electron. The origin is shifted by \((-1/4,-1/4,0)\) relative to the primary CIF.

```cif
data_LaCeGe4Pt4_ordered
_audit_creation_method
'La/Ce ordered derivative of the P4/nmm CaBe2Ge2-type average structure'
_chemical_formula_sum                 'La1 Ce1 Ge4 Pt4'
_chemical_formula_weight              1349.88
_cell_formula_units_Z                 1

_cell_length_a                        4.3993
_cell_length_b                        4.3993
_cell_length_c                        10.036
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90
_cell_volume                          194.2

_space_group_name_H-M_alt             'P 4 m m'
_space_group_IT_number                99

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
La1    La   1   a   0.00000   0.00000   0.2500   1.000
Ce1    Ce   1   b   0.50000   0.50000   0.7500   1.000
Pt1    Pt   2   c   0.50000   0.00000   0.0000   1.000
Pt2A   Pt   1   a   0.00000   0.00000   0.6250   1.000
Pt2B   Pt   1   b   0.50000   0.50000   0.3750   1.000
Ge1    Ge   2   c   0.50000   0.00000   0.5000   1.000
Ge2A   Ge   1   a   0.00000   0.00000   0.8750   1.000
Ge2B   Ge   1   b   0.50000   0.50000   0.1250   1.000
```

The **P4/nmm mixed-site model is the preferred powder solution**. Determining whether La and Ce are actually layer-ordered would require anomalous diffraction near a La or Ce absorption edge, neutron diffraction, or local chemical analysis.
