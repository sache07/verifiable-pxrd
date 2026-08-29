The pattern indexes on a face-centred cubic cell with \(a \approx 12.418\) Å. The strong reflections define a \(6.209\) Å pseudocubic subcell, while the weaker 111, 311, 331, 511/333, etc. reflections require doubling the cell. A plausible composition-compatible model is therefore an ordered \(Fd\bar 3m\) structure with Sr on 16c, Zn on 16d, and S on 32e. The sulfur positional parameter is only weakly constrained by this powder pattern and should be regarded as provisional.

Representative indexing:

| 2θ (°) | hkl |
|---:|:---|
| 12.32 | 111 |
| 23.77 | 311 |
| 24.83 | 222 |
| 28.73 | 400 |
| 31.37 | 331 |
| 37.55 | 511/333 |
| 41.1 | 440 |
| 43.1 | 531 |
| 48.6 | 622 |
| 50.9 | 444 |
| 52.5 | 711/551 |
| 56.9 | 731/553 |
| 59.5 | 800 |
| 67.4 | 840 |
| 74.8 | 844-family |
| 80.3 | 10 2 2 / 666 |
| 89.1 | 880 |

### Primary CIF

```cif
data_SrZnS2_ordered_cubic
_audit_creation_method            'indexed from Cu Kalpha1 powder pattern'
_chemical_name_common             'strontium zinc sulfide'
_chemical_formula_sum             'Sr Zn S2'
_chemical_formula_structural      'SrZnS2'
_cell_formula_units_Z             16

_symmetry_space_group_name_H-M     'F d -3 m'
_symmetry_Int_Tables_number        227
_space_group_name_H-M_alt          'F d -3 m'
_space_group_IT_number             227

_cell_length_a                     12.418
_cell_length_b                     12.418
_cell_length_c                     12.418
_cell_angle_alpha                  90
_cell_angle_beta                   90
_cell_angle_gamma                  90
_cell_volume                       1915.0

_exptl_crystal_density_diffrn      2.997

_diffrn_radiation_type             'Cu Kalpha1'
_diffrn_radiation_wavelength       1.5406

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
Sr1  Sr  16  c  0.0000  0.0000  0.0000  1.0  1.0
Zn1  Zn  16  d  0.5000  0.5000  0.5000  1.0  1.0
S1   S   32  e  0.2000  0.2000  0.2000  1.0  1.2
```

The cell and cubic symmetry are substantially better determined than the sulfur coordinate. A Rietveld refinement should allow the 32e parameter to vary, approximately over \(x_{\rm S}=0.18\)–0.23.

### Surviving average-subcell alternative

If the weak doubled-cell reflections are interpreted as ordering satellites or a minor ordered domain, the dominant peaks can be represented by an ordered \(F\bar 43m\), \(a\approx6.209\) Å average cell:

```cif
data_SrZnS2_average_subcell
_audit_creation_method            'average pseudocubic model'
_chemical_formula_sum             'Sr Zn S2'
_chemical_formula_structural      'SrZnS2'
_cell_formula_units_Z             4

_symmetry_space_group_name_H-M     'F -4 3 m'
_symmetry_Int_Tables_number        216
_space_group_name_H-M_alt          'F -4 3 m'
_space_group_IT_number             216

_cell_length_a                     6.2090
_cell_length_b                     6.2090
_cell_length_c                     6.2090
_cell_angle_alpha                  90
_cell_angle_beta                   90
_cell_angle_gamma                  90
_cell_volume                       239.36

_diffrn_radiation_type             'Cu Kalpha1'
_diffrn_radiation_wavelength       1.5406

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
Sr1  Sr  4  a  0.0000  0.0000  0.0000  1.0  1.0
S1   S   4  b  0.5000  0.5000  0.5000  1.0  1.2
Zn1  Zn  4  c  0.2500  0.2500  0.2500  1.0  1.0
S2   S   4  d  0.7500  0.7500  0.7500  1.0  1.2
```

The doubled \(Fd\bar 3m\) model is preferred because it accounts for the low-angle 12.32° and 23.77° superstructure reflections; the \(F\bar 43m\) model accounts only for the dominant pseudocubic subset.
