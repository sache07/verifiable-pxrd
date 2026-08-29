The pattern is best indexed by a primitive orthorhombic cell with approximately

\[
a=4.660\ \text{Å},\quad b=6.974\ \text{Å},\quad c=10.405\ \text{Å}.
\]

The axial absences \(h00:h=2n\), \(0k0:k=2n\), with observable \(00l\), favor \(P2_12_12\) (No. 18). Representative assignments include 001 at 8.49°, 002 at 17.03°, overlapping 003/020/102 near 25.8°, 120 near 32.1°, 004 near 34.4°, 200 at 38.61°, 130/005 near 43.46°, and 006 near 52.75°.

The cell and structure class are considerably better determined than the fractional coordinates. The CIF below is a chemically constrained direct-space model, with alternating La–N and Ga–Sb substructures. Its coordinates should be regarded as starting values for a final Rietveld refinement.

```cif
data_LaGaSbN_primary
_audit_creation_method
'Powder-pattern indexing followed by chemically constrained direct-space modelling; fractional coordinates are provisional'
_audit_creation_date              2026-03-27

_chemical_name_common             'lanthanum gallium antimonide nitride'
_chemical_formula_structural      'LaGaSbN'
_chemical_formula_sum             'La4 Ga4 Sb4 N4'
_cell_formula_units_Z             4
_chemical_formula_weight          344.395

_symmetry_cell_setting            orthorhombic
_symmetry_space_group_name_H-M    'P 21 21 2'
_symmetry_Int_Tables_number       18

_cell_length_a                    4.660
_cell_length_b                    6.974
_cell_length_c                    10.405
_cell_angle_alpha                 90
_cell_angle_beta                  90
_cell_angle_gamma                 90
_cell_volume                      338.0

_exptl_crystal_density_diffrn     6.77

_diffrn_radiation_type            'Cu Kalpha1'
_diffrn_radiation_wavelength      1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,z'
3  'x+1/2,-y+1/2,-z'
4  '-x+1/2,y+1/2,-z'

loop_
_atom_type_symbol
_atom_type_oxidation_number
La  3
Ga  3
Sb -3
N  -3

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
La1 La 4 c  0.6000  0.1500  0.1500  1.0  0.8
Ga1 Ga 4 c  0.1000  0.6500  0.5500  1.0  0.8
Sb1 Sb 4 c  0.6000  0.6500  0.6500  1.0  0.8
N1  N  4 c  0.1000  0.1500  0.0500  1.0  1.0
```

**Confidence assessment**

- Cell dimensions: high confidence.
- Primitive orthorhombic metric: high confidence.
- \(P2_12_12\) assignment: moderate confidence.
- Atomic coordinates: provisional; the powder pattern alone does not uniquely determine all twelve positional parameters. No alternative cell indexes the principal reflections comparably well enough to justify a second primary CIF.
