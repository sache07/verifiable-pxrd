The pattern is indexed by a **√3×√3 trimerized hexagonal cell**, with approximately:

- \(a = 5.805\) Å
- \(c = 5.980\) Å
- space group **P 3 1 m** (No. 157)
- \(Z=3\)

Diagnostic reflections include 001 at 14.80°, 002 at 29.83°, 110 at 31.07°, overlapping 102/200 near 35.7°, 201 at 38.83°, 211 near 50.56°, 222 near 72.30°, 400 near 75.59°, and 410 near 89.65°. This is the low-symmetry V-trimerized derivative of the parent 1T-LiVS₂ structure. The V coordinate gives a short intratrimer V–V distance of about 3.00 Å.

Because Li scatters weakly with Cu X-rays, its position—and the small sulfur relaxations—are chemically constrained rather than independently determined with high precision.

```cif
data_LiVS2_trimerized
_audit_creation_method
'Indexed and constrained structure solution from Cu Kalpha1 powder XRD'
_audit_creation_date              2025-01-01

_chemical_name_common             'lithium vanadium disulfide'
_chemical_formula_structural      'LiVS2'
_chemical_formula_sum             'Li3 V3 S6'
_cell_formula_units_Z             3

_diffrn_radiation_type            'Cu Kalpha1'
_diffrn_radiation_wavelength      1.5406

_symmetry_cell_setting            trigonal
_symmetry_space_group_name_H-M    'P 3 1 m'
_symmetry_Int_Tables_number       157

_cell_length_a                    5.8050(30)
_cell_length_b                    5.8050(30)
_cell_length_c                    5.9800(30)
_cell_angle_alpha                 90
_cell_angle_beta                  90
_cell_angle_gamma                 120
_cell_volume                      174.55

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-y,x-y,z'
3  'y-x,-x,z'
4  'x-y,-y,z'
5  'y,x,z'
6  '-x,y-x,z'

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
V1   V    3  c  0.2980(8)  0.0000     0.0000     1.0  0.50
Li1  Li   3  c  0.333333   0.0000     0.5000     1.0  1.00
S1   S    1  a  0.0000     0.0000     0.2500(5)  1.0  0.60
S2   S    2  b  0.333333   0.666667   0.2500(5)  1.0  0.60
S3   S    3  c  0.666667   0.0000     0.7500(5)  1.0  0.60
```

The untrimerized parent **P-3m1** model does not account for the √3×√3 reflections and is therefore not retained as a surviving alternative.
