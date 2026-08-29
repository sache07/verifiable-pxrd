The pattern indexes on a pseudorthorhombic double-perovskite cell:

- \(a \approx 5.778\) Å
- \(b \approx 5.596\) Å
- \(c \approx 8.021\) Å
- \(\beta \approx 90^\circ\)
- \(Z=2\)

Representative indexing is 100 at 15.33°, 101 at 18.92°, 011 at 19.33°, overlapping 110/002 near 22.1°, 111 at 24.76°, 200 at 30.94°, 112 at 31.49°, and 020 at 31.96°. The strong 101/011 reflections indicate rock-salt Sc/Ta ordering.

Weak parent-forbidden reflections, particularly 100 and 201, favor a small symmetry lowering from centrosymmetric \(P2_1/n\) to \(P2_1\). The absence of a strong 001 peak argues against complete layered Sr/Ca order; the primary model therefore has statistical Sr/Ca mixing over two symmetry-independent A sites. Oxygen coordinates are constrained to a tilted corner-sharing perovskite framework and should be regarded as powder-derived starting coordinates for Rietveld refinement.

### Primary model: \(P2_1\)

```cif
data_SrCaScTaO6_P21
_audit_creation_method              'Powder-pattern indexing and double-perovskite model'
_chemical_name_common               'strontium calcium scandium tantalate'
_chemical_formula_sum               'Sr Ca Sc Ta O6'
_chemical_formula_structural        '(Sr0.5Ca0.5)2ScTaO6'
_cell_formula_units_Z               2

_cell_length_a                      5.7775
_cell_length_b                      5.5957
_cell_length_c                      8.0205
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        259.3

_symmetry_space_group_name_H-M      'P 1 21 1'
_space_group_IT_number              4

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y+1/2,-z'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Sr  2
Ca  2
Sc  3
Ta  5
O  -2

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Sr1  Sr  0.7540  0.0180  0.0060  0.500  0.006
Ca1  Ca  0.7540  0.0180  0.0060  0.500  0.006
Sr2  Sr  0.7420  0.9760  0.4970  0.500  0.006
Ca2  Ca  0.7420  0.9760  0.4970  0.500  0.006
Sc1  Sc  0.2492  0.0015  0.2488  1.000  0.005
Ta1  Ta  0.2510  0.9985  0.7506  1.000  0.004
O1   O   0.2520  0.0100  0.9900  1.000  0.009
O2   O   0.2470  0.9860  0.5090  1.000  0.009
O3   O   0.5080  0.2580  0.2440  1.000  0.009
O4   O   0.9910  0.2570  0.2560  1.000  0.009
O5   O   0.5120  0.7390  0.2420  1.000  0.009
O6   O   0.9950  0.7390  0.2580  1.000  0.009
```

### Surviving higher-symmetry alternative: \(P2_1/n\)

This is the centrosymmetric average structure obtained by symmetrizing the primary model. It is viable if the weak 100/201 features are extrinsic, defect-related, or below the reliability of the profile.

```cif
data_SrCaScTaO6_P21n
_audit_creation_method              'Centrosymmetric average of the P21 powder model'
_chemical_name_common               'strontium calcium scandium tantalate'
_chemical_formula_sum               'Sr Ca Sc Ta O6'
_chemical_formula_structural        '(Sr0.5Ca0.5)2ScTaO6'
_cell_formula_units_Z               2

_cell_length_a                      5.7775
_cell_length_b                      5.5957
_cell_length_c                      8.0205
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        259.3

_symmetry_space_group_name_H-M      'P 1 21/n 1'
_space_group_IT_number              14

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y+1/2,-z'
3  '-x+1/2,-y,-z+1/2'
4  'x+1/2,-y+1/2,z+1/2'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Sr  2
Ca  2
Sc  3
Ta  5
O  -2

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Sr1  Sr  0.7560  0.0210  0.0045  0.500  0.006
Ca1  Ca  0.7560  0.0210  0.0045  0.500  0.006
Sc1  Sc  0.2500  0.0000  0.2500  1.000  0.005
Ta1  Ta  0.2500  0.0000  0.7500  1.000  0.004
O1   O   0.2525  0.0120  0.9905  1.000  0.009
O2   O   0.5065  0.2595  0.2430  1.000  0.009
O3   O   0.9895  0.2590  0.2570  1.000  0.009
```

The preferred interpretation is therefore a strongly Sc/Ta-ordered, tilted double perovskite with a weak polar \(P2_1\) distortion and substantially disordered Sr/Ca A sites.
