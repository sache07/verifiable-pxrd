The pattern is best indexed by a primitive, nearly cubic orthorhombic cell:

\[
a \approx 4.994\ \text{Å},\quad b \approx 4.922\ \text{Å},\quad c \approx 4.872\ \text{Å}.
\]

The splitting of the low-angle reflections near 17.75–18.20°, 25.4–25.7°, and 35.9–36.9° rules out an exactly cubic metric. A chemically reasonable solution is an orthorhombically distorted tetrahedral \( \mathrm{YRh_4B_4} \) structure in \(P222\), with one formula unit per cell. The boron coordinates are substantially less certain than the heavy-atom framework because Cu X-ray scattering from B is weak.

```cif
data_YRh4B4_primary
_audit_creation_method              'Powder-pattern indexing and constrained structure solution'
_chemical_name_common               'yttrium tetrarhodium tetraboride'
_chemical_formula_sum               'B4 Rh4 Y'
_chemical_formula_structural        'YRh4B4'
_chemical_formula_weight            543.79

_symmetry_space_group_name_H-M       'P 2 2 2'
_symmetry_Int_Tables_number          16
_space_group_crystal_system          orthorhombic

_cell_length_a                       4.994
_cell_length_b                       4.922
_cell_length_c                       4.872
_cell_angle_alpha                    90
_cell_angle_beta                     90
_cell_angle_gamma                    90
_cell_volume                         119.75
_cell_formula_units_Z                1

_exptl_crystal_density_diffrn        7.54
_diffrn_radiation_type               'Cu Kalpha1'
_diffrn_radiation_wavelength         1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,z'
3  '-x,y,-z'
4  'x,-y,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Y1   Y    1   0.5000   0.5000   0.5000   1.0   0.008
Rh1  Rh   4   0.1640   0.1640   0.2020   1.0   0.006
B1   B    4   0.8750   0.3750   0.1250   1.0   0.012
```

The inverted coordinate set—Rh at approximately `(0.836, 0.836, 0.798)` and B at `(0.125, 0.625, 0.875)`—is powder-diffraction equivalent and represents the opposite structural hand. Several subsidiary maxima, especially around 31.7°, 36.3°, and 48.6–49.2°, suggest either a minor secondary phase or additional symmetry lowering; they do not justify a unique second structural model from this pattern alone.
