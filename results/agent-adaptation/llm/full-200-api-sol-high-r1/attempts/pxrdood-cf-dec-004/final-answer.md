The peak positions are best indexed by an **orthorhombic supercell** with approximately

\[
a=9.886\ \text{Å},\quad b=4.720\ \text{Å},\quad c=4.134\ \text{Å}.
\]

The axial series \(200/400/600/800\) occurs at 17.93, 36.32, 55.74 and 77.12°, while 020 and 040 occur at 38.11 and 81.54°. The extinction pattern favors **Pnma (No. 62)**. The weak component at 36.59° is not accounted for exactly and may represent a slightly contracted domain or minor secondary polymorph.

The cell and space group are substantially better determined than the atomic coordinates. The following is therefore an ordered, chemically reasonable **starting model** for subsequent Rietveld refinement, with two independent CrMoN formula units on Pnma 4c sites.

```cif
data_CrMoN_primary
_audit_creation_method
'Indexed from Cu Kalpha1 powder diffraction; atomic coordinates are a provisional ordered Pnma starting model'

_chemical_name_common                 'chromium molybdenum nitride'
_chemical_formula_sum                 'Cr8 Mo8 N8'
_chemical_formula_structural          'CrMoN'
_cell_formula_units_Z                 8

_symmetry_space_group_name_H-M        'P n m a'
_symmetry_Int_Tables_number           62
_space_group_name_H-M_alt             'P n m a'
_space_group_IT_number                62

_cell_length_a                        9.8860
_cell_length_b                        4.7200
_cell_length_c                        4.1340
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90
_cell_volume                          192.88

_exptl_crystal_density_diffrn         11.15
_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '1/2-x,3/4,1/2+z'
3  '-x,3/4,-z'
4  '1/2+x,1/4,1/2-z'
5  '-x,-y,-z'
6  '1/2+x,1/4,1/2-z'
7  'x,1/4,z'
8  '1/2-x,3/4,1/2+z'

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
Cr1  Cr  4  c  0.0500  0.2500  0.1000  1.0  0.006
Cr2  Cr  4  c  0.1500  0.2500  0.8500  1.0  0.006
Mo1  Mo  4  c  0.0500  0.2500  0.6000  1.0  0.005
Mo2  Mo  4  c  0.4000  0.2500  0.1500  1.0  0.005
N1   N   4  c  0.2500  0.2500  0.3500  1.0  0.008
N2   N   4  c  0.3500  0.2500  0.7800  1.0  0.008
```

Representative indexing is:

| 2θ observed | Proposed hkl |
|---:|:---|
| 17.93° | 200 |
| 36.32° | 400 |
| 38.11° | 020 |
| 43.78° | 002 |
| 47.66° | 202 |
| 55.74° | 600 |
| 57.04° | 312 |
| 62.42° | 412 |
| 64.84° | 611 |
| 67.88° | 512 |
| 74.40° | 711 |
| 76.65° | 612 |
| 77.12° | 800 |
| 77.76° | 313 |
| 81.54° | 040 |
| 84.33° | 630/721 region |

A non-centrosymmetric subgroup such as **Pna2₁** remains a positional alternative, but the powder data do not justify a separate fully refined CIF for it. The coordinates above should not be treated as publication-quality without Rietveld refinement against the full profile.
