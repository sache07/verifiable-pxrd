The dominant reflections index on an approximately orthorhombic primitive cell:

\[
a=6.823\ \text{Å},\quad b=6.532\ \text{Å},\quad c=9.316\ \text{Å}.
\]

Representative assignments are 002 at 19.04°, 200 at 26.10°, 020 at 27.29°, 202 at 32.51°, 220 at 38.12°, 004 at 38.63°, 204 at 47.21°, 400 at 53.70°, and 006 at 59.49°. The systematic absences and the likely eight formula units per cell favor **Pbca (No. 61)**. The implied density is approximately 10.1 g cm⁻³.

The lattice and space-group assignment are considerably more secure than the atomic coordinates. The latter are a provisional Pbca parent model; the pattern contains unresolved/split features, especially near 38.8°, indicating either a weak secondary metric, lower symmetry, or anisotropic splitting. Consequently, the CIF should be treated as a starting model for Rietveld refinement rather than a completed refinement.

### Primary provisional CIF

```cif
data_CrGaBW_primary
_audit_creation_method
;Powder indexing followed by provisional Pbca parent-structure placement.
 Atomic coordinates and displacement parameters have not been Rietveld refined.
;

_chemical_name_common                 'chromium gallium tungsten boride'
_chemical_formula_sum                 'B Cr Ga W'
_cell_formula_units_Z                 8

_diffrn_radiation_probe               x-ray
_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

_space_group_crystal_system           orthorhombic
_space_group_name_H-M_alt             'P b c a'
_space_group_IT_number                61

_cell_length_a                        6.8228
_cell_length_b                        6.5320
_cell_length_c                        9.3160
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90

_exptl_crystal_density_diffrn         10.12

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
W1   W    8 c   0.1270  0.1180  0.1420  1.0  0.006
Cr1  Cr   8 c   0.3690  0.1320  0.5030  1.0  0.008
Ga1  Ga   8 c   0.1120  0.3810  0.6520  1.0  0.008
B1   B    8 c   0.3860  0.3660  0.0060  1.0  0.012
```

### Occupational alternative: Cr/Ga interchange

The Cu-XRD pattern should constrain W well but is much less robust for B and may retain a Cr/Ga assignment ambiguity without a full profile refinement.

```cif
data_CrGaBW_CrGa_swap_alternative
_audit_creation_method
;Occupational alternative to the provisional Pbca model.
 Cr and Ga are interchanged relative to the primary model.
;

_chemical_formula_sum                 'B Cr Ga W'
_cell_formula_units_Z                 8

_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

_space_group_crystal_system           orthorhombic
_space_group_name_H-M_alt             'P b c a'
_space_group_IT_number                61

_cell_length_a                        6.8228
_cell_length_b                        6.5320
_cell_length_c                        9.3160
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
W1   W    8 c   0.1270  0.1180  0.1420  1.0  0.006
Ga1  Ga   8 c   0.3690  0.1320  0.5030  1.0  0.008
Cr1  Cr   8 c   0.1120  0.3810  0.6520  1.0  0.008
B1   B    8 c   0.3860  0.3660  0.0060  1.0  0.012
```

A definitive solution would require profile refinement of the atomic coordinates and testing whether the non-indexed/split features represent a minor phase or a monoclinic distortion of this Pbca cell.
