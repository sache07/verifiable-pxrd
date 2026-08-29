The pattern indexes best as a **monoclinic BaHfS₃ phase**, with a doubled \(b\) axis and systematic absence of 010, consistent with **\(P2_1/m\) (No. 11), \(Z=4\)**. Refined metric parameters are approximately:

\[
a=7.591\ \text{Å},\quad b=8.482\ \text{Å},\quad c=7.317\ \text{Å},\quad
\beta=97.50^\circ .
\]

Diagnostic assignments include 100 at 11.75°, 001 at 12.19°, \(10\bar1\) at 15.81°, 020 at 20.93°, 200 at 23.62°, 040 at 42.61°, and 060 at 66.05°.

The lattice and space-group assignment are substantially more secure than the internal coordinates. The CIF below is a chemically constrained, Rietveld-ready starting model; sulfur coordinates in particular should be refined against the full profile.

```cif
data_BaHfS3_monoclinic
_audit_creation_method
'Powder indexing followed by chemically constrained direct-space modelling'

_chemical_name_common                 'barium hafnium sulfide'
_chemical_formula_sum                 'Ba4 Hf4 S12'
_chemical_formula_structural          'BaHfS3'
_cell_formula_units_Z                 4

_cell_length_a                        7.591
_cell_length_b                        8.482
_cell_length_c                        7.317
_cell_angle_alpha                     90
_cell_angle_beta                      97.50
_cell_angle_gamma                     90

_space_group_crystal_system           monoclinic
_space_group_name_H-M_alt             'P 21/m'
_space_group_IT_number                11

_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y+1/2,-z'
3  '-x,-y,-z'
4  'x,-y+1/2,z'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba  2
Hf  4
S  -2

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Ba1  Ba  4  0.2700  0.0000  0.7400  1.0  0.0076
Hf1  Hf  4  0.2450  0.0000  0.2550  1.0  0.0063
S1   S   2  0.2450  0.2500  0.2550  1.0  0.0101
S2   S   2  0.7550  0.2500  0.7450  1.0  0.0101
S3   S   2  0.0000  0.0000  0.0000  1.0  0.0101
S4   S   2  0.5000  0.0000  0.0000  1.0  0.0101
S5   S   2  0.0000  0.0000  0.5000  1.0  0.0101
S6   S   2  0.5000  0.0000  0.5000  1.0  0.0101
```

A formally possible subcell interpretation is \(b\simeq4.241\) Å in \(P2/m\), but it is disfavored by the missing low-angle 010 reflection and by the observed 020–040–060 sequence. The commonly reported orthorhombic \(Pnma\) BaHfS₃ perovskite is not compatible with the strong reflections at 11.75° and 12.19°.
