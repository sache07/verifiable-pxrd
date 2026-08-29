The principal reflections are consistent with a **trirutile-type tetragonal average structure**, approximately \(a=5.049\), \(c=9.573\) Å, space group \(P4_2/mnm\) (No. 136), \(Z=2\). Representative indexing is 110 at 24.92°, 103 at 33.18°, 200 near 35.6°, 004 near 37.6°, 210/202 near 40°, 213 near 49.4°, and 220/105 near 51.1°.

The 26.05° peak and several weak low-angle reflections are forbidden or poorly represented in the ideal parent symmetry, indicating local O/F ordering or an orthorhombic superstructure. Because O and F differ by only one electron, their ordering cannot be determined uniquely from Cu Kα powder data. The most defensible result is therefore the average trirutile framework below.

### Primary CIF: O/F disorder on the 4f anion site

```cif
data_Mn3OF5_average_trirutile
_audit_creation_method
'Indexed and modelled from Cu Kalpha1 powder diffraction; average trirutile structure'
_chemical_name_common                 'manganese oxide fluoride'
_chemical_formula_sum                 'Mn3 O F5'
_chemical_formula_structural          'Mn3OF5'
_cell_formula_units_Z                 2

_cell_length_a                        5.0489
_cell_length_b                        5.0489
_cell_length_c                        9.5730
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90
_cell_volume                          244.03

_symmetry_space_group_name_H-M        'P 42/m n m'
_symmetry_Int_Tables_number           136
_space_group_crystal_system           tetragonal

_exptl_radiation_type                 'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

loop_
_atom_type_symbol
_atom_type_oxidation_number
Mn3+   3
Mn2+   2
O2-   -2
F-    -1

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
Mn1   Mn3+   2   a   0.0000   0.0000   0.0000   1.0000   0.008
Mn2   Mn2+   4   e   0.0000   0.0000   0.3332   1.0000   0.008
O1    O2-    4   f   0.3052   0.3052   0.0000   0.5000   0.012
F1    F-     4   f   0.3052   0.3052   0.0000   0.5000   0.012
F2    F-     8   j   0.3037   0.3037   0.3338   1.0000   0.012
```

This gives the cell contents Mn\(_6\)O\(_2\)F\(_{10}\), or \(Z=2\) Mn\(_3\)OF\(_5\).

### Surviving occupational alternative

Cu Kα diffraction cannot reliably decide whether oxygen is concentrated on 4f or statistically replaces F on 8j. The main alternative has fully fluorinated 4f and 25% O on 8j:

```cif
data_Mn3OF5_average_trirutile_alt_O_on_8j
_audit_creation_method
'Alternative O/F occupational model; same trirutile framework'
_chemical_formula_sum                 'Mn3 O F5'
_cell_formula_units_Z                 2

_cell_length_a                        5.0489
_cell_length_b                        5.0489
_cell_length_c                        9.5730
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90

_symmetry_space_group_name_H-M        'P 42/m n m'
_symmetry_Int_Tables_number           136

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
Mn1   Mn   2   a   0.0000   0.0000   0.0000   1.0000   0.008
Mn2   Mn   4   e   0.0000   0.0000   0.3332   1.0000   0.008
F1    F    4   f   0.3052   0.3052   0.0000   1.0000   0.012
F2    F    8   j   0.3037   0.3037   0.3338   0.7500   0.012
O2    O    8   j   0.3037   0.3037   0.3338   0.2500   0.012
```

The unmodelled superstructure reflections suggest that the true low-temperature/local structure may be a primitive orthorhombic derivative, roughly \(7.4\times7.1\times9.6\) Å. Neutron diffraction or anomalous/scattering-contrast measurements would be required to determine that ordered O/F arrangement uniquely.
