The pattern indexes as a body-centered tetragonal K₂NiF₄-type cell:

- \(a \approx 4.2784\) Å
- \(c \approx 13.4557\) Å
- \(Z=2\)
- reflection condition \(h+k+l=2n\)

Representative indexing is 13.15° (002), 21.78° (101), 26.48° (004), 28.82° (103), 29.50° (110), 32.42° (112), and 42.21° (200). The composition favors ordered Ca/La and O/S sites in polar \(I4mm\). The absolute polar direction is not determined by ordinary powder diffraction; inverting every \(z\) coordinate gives an equivalent domain.

### Primary structure: ordered polar \(I4mm\)

```cif
data_CaLaFeO3S_I4mm
_audit_creation_method            'Powder-XRD indexing and chemically constrained structure solution'
_chemical_name_common             'calcium lanthanum iron oxysulfide'
_chemical_formula_structural      'CaLaFeO3S'
_chemical_formula_sum             'Ca1 Fe1 La1 O3 S1'
_cell_formula_units_Z             2

_cell_length_a                    4.2784
_cell_length_b                    4.2784
_cell_length_c                    13.4557
_cell_angle_alpha                 90
_cell_angle_beta                  90
_cell_angle_gamma                 90
_cell_volume                      246.35

_space_group_crystal_system       tetragonal
_space_group_name_H-M_alt         'I 4 m m'
_space_group_IT_number            107

_diffrn_radiation_type            'Cu Kalpha1'
_diffrn_radiation_wavelength      1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1   'x,y,z'
2   '-y,x,z'
3   '-x,-y,z'
4   'y,-x,z'
5   '-x,y,z'
6   'x,-y,z'
7   'y,x,z'
8   '-y,-x,z'
9   'x+1/2,y+1/2,z+1/2'
10  '-y+1/2,x+1/2,z+1/2'
11  '-x+1/2,-y+1/2,z+1/2'
12  'y+1/2,-x+1/2,z+1/2'
13  '-x+1/2,y+1/2,z+1/2'
14  'x+1/2,-y+1/2,z+1/2'
15  'y+1/2,x+1/2,z+1/2'
16  '-y+1/2,-x+1/2,z+1/2'

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
Fe1   Fe   2  a   0.000000   0.000000   0.000000   1.000   0.005
Oeq1  O    4  b   0.000000   0.500000   0.001000   1.000   0.007
Oap1  O    2  a   0.000000   0.000000   0.148000   1.000   0.007
S1    S    2  a   0.000000   0.000000   0.819000   1.000   0.007
La1   La   2  a   0.000000   0.000000   0.356000   1.000   0.005
Ca1   Ca   2  a   0.000000   0.000000   0.640000   1.000   0.006
```

This model contains FeO₅S octahedra with approximate Fe–O(apical), Fe–S, and Fe–O(equatorial) distances of 1.99, 2.44, and 2.14 Å, respectively.

### Surviving average-structure alternative: disordered \(I4/mmm\)

A centrosymmetric average model, in which Ca/La and apical O/S are each statistically disordered, has the same lattice and systematic absences. It is lower-ranked because the low-angle intensity distribution favors the ordered polar model.

```cif
data_CaLaFeO3S_I4mmm_average
_audit_creation_method            'Centrosymmetric occupationally disordered alternative'
_chemical_name_common             'calcium lanthanum iron oxysulfide, average structure'
_chemical_formula_structural      'CaLaFeO3S'
_chemical_formula_sum             'Ca1 Fe1 La1 O3 S1'
_cell_formula_units_Z             2

_cell_length_a                    4.2784
_cell_length_b                    4.2784
_cell_length_c                    13.4557
_cell_angle_alpha                 90
_cell_angle_beta                  90
_cell_angle_gamma                 90
_cell_volume                      246.35

_space_group_crystal_system       tetragonal
_space_group_name_H-M_alt         'I 4/m m m'
_space_group_IT_number            139

_diffrn_radiation_type            'Cu Kalpha1'
_diffrn_radiation_wavelength      1.5406

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
Fe1   Fe   2  a   0.000000   0.000000   0.000000   1.000   0.005
Oeq1  O    4  c   0.000000   0.500000   0.000000   1.000   0.007
Ca1   Ca   4  e   0.000000   0.000000   0.358000   0.500   0.006
La1   La   4  e   0.000000   0.000000   0.358000   0.500   0.005
Oap1  O    4  e   0.000000   0.000000   0.164500   0.500   0.007
S1    S    4  e   0.000000   0.000000   0.164500   0.500   0.007
```

The primary \(I4mm\) coordinates are a powder-derived starting model; the five independent \(z\) coordinates should be finalized by full-profile Rietveld refinement.
