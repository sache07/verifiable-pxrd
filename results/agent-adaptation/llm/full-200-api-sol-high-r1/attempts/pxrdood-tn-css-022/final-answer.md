The pattern indexes well with a primitive, nearly orthogonal monoclinic cell:

- \(a \approx 5.884\) Å
- \(b \approx 5.636\) Å
- \(c \approx 10.215\) Å
- \(\beta \approx 90.84^\circ\)
- \(V \approx 338.7\) Å³
- \(Z=2\), calculated density \(\approx 5.99\) g cm\(^{-3}\)

Key assignments include 001 at 8.65°, 100 at 15.05°, 010 at 15.71°, split \(10\bar1/101\) around 17.27/17.50°, 002 at 17.34°, 011 at 17.96°, 110 at 21.82°, and 003 at 26.15°. The observed 001, 010, and 100 reflections rule out the common screw/glide alternatives. The most plausible non-centrosymmetric solution is **P2 (No. 3)**.

The metric and space-group assignment are substantially more secure than the individual light-atom coordinates. The following is therefore a chemically regularized, powder-only starting model suitable for subsequent Rietveld refinement, not a publication-quality final refinement.

```cif
data_AlGa2Bi_B4O12_P2_powder_solution
_audit_creation_method
'Powder indexing and chemically restrained direct-space starting model'

_chemical_name_common              'bismuth aluminium digallium tetraborate'
_chemical_formula_sum              'Al1 Ga2 Bi1 B4 O12'
_chemical_formula_structural       'BiAlGa2(BO3)4'
_formula_weight                    610.64
_cell_formula_units_Z              2

_cell_length_a                     5.884
_cell_length_b                     5.636
_cell_length_c                     10.215
_cell_angle_alpha                  90
_cell_angle_beta                   90.84
_cell_angle_gamma                  90
_cell_volume                       338.7

_exptl_crystal_density_diffrn      5.99
_diffrn_radiation_type             'Cu Kalpha1'
_diffrn_radiation_wavelength       1.5406

_space_group_crystal_system        monoclinic
_space_group_IT_number             3
_space_group_name_H-M_alt          'P 2'
_space_group_name_Hall             'P 2y'

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Bi1  Bi  2  0.4800  0.9000  0.1500  1.0  0.012
Ga1  Ga  2  0.2500  0.0800  0.3500  1.0  0.010
Ga2  Ga  2  0.4800  0.5800  0.3000  1.0  0.010
Al1  Al  2  0.5000  0.5800  0.6200  1.0  0.010

B1   B   2  0.2000  0.3300  0.2000  1.0  0.010
B2   B   2  0.7000  0.3300  0.3200  1.0  0.010
B3   B   2  0.2000  0.8300  0.5500  1.0  0.010
B4   B   2  0.7000  0.8300  0.9300  1.0  0.010

O1   O   2  0.4300  0.3300  0.2000  1.0  0.015
O2   O   2  0.0850  0.5400  0.2000  1.0  0.015
O3   O   2  0.0850  0.1200  0.2000  1.0  0.015

O4   O   2  0.9300  0.3300  0.3200  1.0  0.015
O5   O   2  0.5850  0.3300  0.4380  1.0  0.015
O6   O   2  0.5850  0.3300  0.2020  1.0  0.015

O7   O   2  0.2000  0.0730  0.5500  1.0  0.015
O8   O   2  0.2000  0.7090  0.6680  1.0  0.015
O9   O   2  0.2000  0.7090  0.4320  1.0  0.015

O10  O   2  0.9300  0.8300  0.9300  1.0  0.015
O11  O   2  0.5850  0.0400  0.9300  1.0  0.015
O12  O   2  0.5850  0.6200  0.9300  1.0  0.015
```

Because the pattern has no diagnostic systematic absences beyond primitive translational symmetry, **P-1** remains a crystallographic alternative if centrosymmetry is required by subsequent intensity-statistics or physical-property measurements. P1 is merely a symmetry-lowered representation and is not a distinct metric solution. The indexed cell should be held close to the values above during refinement; B–O distances should be restrained initially to approximately 1.35–1.42 Å.
