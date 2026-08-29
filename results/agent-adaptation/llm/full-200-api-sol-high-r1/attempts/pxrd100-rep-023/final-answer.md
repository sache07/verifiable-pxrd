The pattern indexes as a primitive, pseudo-orthorhombic perovskite supercell:

- \(a \approx 5.824\) Å
- \(b \approx 8.216\) Å
- \(c \approx 5.794\) Å
- \(\alpha=\beta=\gamma\approx90^\circ\)

The weak reflections at approximately 10.76°, 15.2°, and 18.7° correspond to 010, 100/001, and 110/011. They exclude the usual disordered **Pnma** average structure because those first reflections are systematically absent in Pnma. A 1:3 ordered Ti:Zr arrangement in the four-B-site perovskite cell reduces the parent Pnma symmetry most naturally to **P-1**. The strong peak splitting is reproduced by the orthorhombic metrics.

The heavy-atom ordering and lattice are well constrained; oxygen and Sr coordinates below are chemically regularized starting coordinates suitable for final Rietveld refinement.

```cif
data_Sr4Zr3TiO12_ordered
_audit_creation_method              'Powder XRD indexing and chemically constrained structure solution'
_chemical_name_common               '1:3 B-site ordered perovskite Sr4Zr3TiO12'
_chemical_formula_sum               'Sr4 Zr3 Ti O12'
_chemical_formula_structural        'Sr4Zr3TiO12'
_cell_formula_units_Z               1

_cell_length_a                       5.824(2)
_cell_length_b                       8.216(2)
_cell_length_c                       5.794(2)
_cell_angle_alpha                    90
_cell_angle_beta                     90
_cell_angle_gamma                    90
_cell_volume                         277.24
_exptl_crystal_density_diffrn       5.18

_space_group_crystal_system         triclinic
_space_group_name_H-M_alt           'P -1'
_space_group_IT_number              2

_diffrn_radiation_type              'Cu Kalpha1'
_diffrn_radiation_wavelength        1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,-z'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Sr  2
Zr  4
Ti  4
O  -2

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
Ti1  Ti  1  a  0.0000  0.0000  0.0000  1.000  0.45
Zr1  Zr  1  f  0.5000  0.0000  0.5000  1.000  0.45
Zr2  Zr  1  c  0.0000  0.5000  0.0000  1.000  0.45
Zr3  Zr  1  h  0.5000  0.5000  0.5000  1.000  0.45

Sr1  Sr  2  i  0.0200  0.2500  0.5000  1.000  0.70
Sr2  Sr  2  i  0.4800  0.7500  0.0000  1.000  0.70

O1   O   2  i  0.4890  0.2500  0.5580  1.000  0.90
O2   O   2  i  0.0110  0.7650  0.0580  1.000  0.90
O3   O   2  i  0.2650  0.0350  0.2000  1.000  0.90
O4   O   2  i  0.2050  0.9650  0.7300  1.000  0.90
O5   O   2  i  0.7200  0.5350  0.7850  1.000  0.90
O6   O   2  i  0.7800  0.4650  0.2850  1.000  0.90
```

Representative indexing checks are:

| 2θ observed | Principal indices |
|---:|---|
| 10.76° | 010 |
| 15.2–15.3° | 100, 001 |
| 18.7° | 110, 011 |
| 21.63° | 020, 101 |
| 24.20° | 111 |
| 26.56° | 120, 021 |
| 30.68–30.85° | 200, 121, 002 |
| 37.85–37.99° | 220, 022 |
| 44.05° | 040, 202 |

The disordered Pnma model is not retained as a primary alternative because it cannot generate the first two low-angle superstructure groups.
