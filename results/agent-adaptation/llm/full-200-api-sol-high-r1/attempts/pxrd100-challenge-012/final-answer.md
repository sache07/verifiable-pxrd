The reflections index on a cubic body-centered cell with \(a \approx 8.005\) Å. Representative assignments are 110 at 15.64°, 211 at 27.27°, 220 at 31.59°, 222 at 38.94°, 400 at 45.28°, 422 at 56.25°, 440 at 65.96°, 620 at 74.97°, and 444 at 83.61°. The dominant subcell is \(a_p\approx4.0025\) Å.

The weak \(h+k+l=2n\) supercell reflections support an \(a^+a^+a^+\)-tilted **Im-3** model. No odd-sum supercell reflections are detected, despite the large V/Mo X-ray contrast, so long-range rock-salt V/Mo ordering is not supported. V and Mo are therefore placed statistically on the same octahedral site. The oxygen coordinate is less certain than the cell and symmetry; \(y=z\approx0.200\) is a reasonable powder-derived starting value.

### Primary CIF

```cif
data_Sr2VMoO6_Im-3
_audit_creation_method              'Structure solution from supplied Cu Kalpha1 powder pattern'
_chemical_name_common               'strontium vanadium molybdenum oxide'
_chemical_formula_sum               'Sr2 V Mo O6'
_chemical_formula_structural        'Sr2(V0.5Mo0.5)2O6'
_cell_formula_units_Z               4

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_symmetry_space_group_name_H-M      'I m -3'
_symmetry_Int_Tables_number         204
_space_group_name_H-M_alt           'I m -3'
_space_group_IT_number              204

_cell_length_a                      8.0050
_cell_length_b                      8.0050
_cell_length_c                      8.0050
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        512.96

loop_
_atom_type_symbol
_atom_type_oxidation_number
Sr  2
V   4
Mo  4
O  -2

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
Sr1  Sr  2   a  0.00000  0.00000  0.00000  1.000  0.50
Sr2  Sr  6   b  0.00000  0.50000  0.50000  1.000  0.50
V1   V   8   c  0.25000  0.25000  0.25000  0.500  0.40
Mo1  Mo  8   c  0.25000  0.25000  0.25000  0.500  0.40
O1   O  24   g  0.00000  0.20000  0.20000  1.000  0.80
```

### Lower-symmetry interpretation if the weak supercell peaks are excluded

If the weak peaks are from a minor phase or are otherwise omitted, the dominant reflections alone reduce to a cubic disordered perovskite, \(Pm\bar3m\), with \(a_p\approx4.0025\) Å:

```cif
data_Sr2VMoO6_average_Pm-3m
_audit_creation_method              'Average subcell alternative'
_chemical_formula_sum               'Sr V0.5 Mo0.5 O3'
_chemical_formula_structural        'Sr(V0.5Mo0.5)O3'
_cell_formula_units_Z               1

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_symmetry_space_group_name_H-M      'P m -3 m'
_symmetry_Int_Tables_number         221
_space_group_name_H-M_alt           'P m -3 m'
_space_group_IT_number              221

_cell_length_a                      4.0025
_cell_length_b                      4.0025
_cell_length_c                      4.0025
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        64.12

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
Sr1  Sr  1  a  0.00000  0.00000  0.00000  1.000  0.50
V1   V   1  b  0.50000  0.50000  0.50000  0.500  0.40
Mo1  Mo  1  b  0.50000  0.50000  0.50000  0.500  0.40
O1   O   3  c  0.00000  0.50000  0.50000  1.000  0.80
```

The **Im-3 disordered, tilted model is preferred** because it accounts for the complete weak-reflection sequence as well as the strong perovskite peaks.
