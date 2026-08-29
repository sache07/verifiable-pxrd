The peak positions index on a body-centered tetragonal metric with approximately \(a=6.0853\) Å and \(c=5.4774\) Å. The sequence 110, 200, 002, 211, 112, 220, 202 and 310 identifies a CuAl\(_2\)-type framework. The clear 101 and 301 reflections, extinct in ideal \(I4/mcm\), indicate Zr/Ti ordering on the CuAl\(_2\) 8h sublattice.

The primary model below is therefore an ordered CuAl\(_2\)-type derivative. It is written explicitly in \(P1\) to avoid imposing an uncertain orthorhombic subgroup; the coordinates retain the body-centering translation. The Fe/Co ordering shown is one representative domain because Cu X-rays have very little Fe/Co contrast.

### Primary structure: ordered CuAl\(_2\)-type derivative

```cif
data_Zr2Ti2FeCo_ordered_CuAl2_derivative
_audit_creation_method              'Powder indexing and CuAl2-type structure solution'
_chemical_name_common               'ordered Zr2Ti2FeCo'
_chemical_formula_structural        'Zr2Ti2FeCo'
_chemical_formula_sum               'Co Fe Ti2 Zr2'
_cell_formula_units_Z               2

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_cell_length_a                      6.0853
_cell_length_b                      6.0853
_cell_length_c                      5.4774
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90
_cell_volume                        202.84

_space_group_name_H-M_alt           'P 1'
_space_group_IT_number              1

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x,y,z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Zr1 Zr  0.1730  0.6730  0.0000  1.0
Zr2 Zr  0.8270  0.3270  0.0000  1.0
Zr3 Zr  0.6730  0.1730  0.5000  1.0
Zr4 Zr  0.3270  0.8270  0.5000  1.0

Ti1 Ti  0.3270  0.1730  0.0000  1.0
Ti2 Ti  0.6730  0.8270  0.0000  1.0
Ti3 Ti  0.8270  0.6730  0.5000  1.0
Ti4 Ti  0.1730  0.3270  0.5000  1.0

Fe1 Fe  0.0000  0.0000  0.2500  1.0
Fe2 Fe  0.5000  0.5000  0.7500  1.0
Co1 Co  0.0000  0.0000  0.7500  1.0
Co2 Co  0.5000  0.5000  0.2500  1.0
```

Representative indexing:

| \(2\theta_{\rm obs}\) | Reflection |
|---:|:---|
| 20.63° | 110 |
| 21.82° | 101, ordering reflection |
| 29.33° | 200 |
| 32.67° | 002 |
| 36.85° | 211 |
| 38.95° | 112 |
| 41.96° | 220 |
| 44.47° | 202 |
| 47.19° | 310 |
| 47.78° | 301, ordering reflection |
| 54.15° | 222 |
| 61.06° | 400 |
| 64.95° | 330 |
| 65.44° | 411 |
| 68.45° | 004 |
| 70.78° | 402 |
| 74.63° | 332 |

### Surviving average-structure alternative

If the 101 and 301 peaks belong to a weak secondary phase, or if occupational order is only short-range, the average structure is the disordered \(I4/mcm\) CuAl\(_2\) parent:

```cif
data_Zr2Ti2FeCo_average_I4mcm
_audit_creation_method              'Average CuAl2-type model'
_chemical_name_common               'Zr2Ti2FeCo, disordered CuAl2 type'
_chemical_formula_structural        'Zr2Ti2FeCo'
_chemical_formula_sum               'Co Fe Ti2 Zr2'
_cell_formula_units_Z               2

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

_cell_length_a                      6.0853
_cell_length_b                      6.0853
_cell_length_c                      5.4774
_cell_angle_alpha                   90
_cell_angle_beta                    90
_cell_angle_gamma                   90

_space_group_name_H-M_alt           'I 4/m c m'
_space_group_IT_number              140

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Zr1 Zr  8  0.1730  0.6730  0.0000  0.5
Ti1 Ti  8  0.1730  0.6730  0.0000  0.5
Fe1 Fe  4  0.0000  0.0000  0.2500  0.5
Co1 Co  4  0.0000  0.0000  0.2500  0.5
```

The ordered model is preferred because it naturally generates the observed 101 and 301 superstructure reflections. The positional parameter is approximately \(x=0.173\), with an estimated powder-only uncertainty of roughly 0.003–0.005. Fe/Co order versus disorder cannot be established reliably from Cu \(K\alpha\) X-ray data alone.
