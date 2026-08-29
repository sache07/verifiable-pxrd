The pattern indexes as a primitive orthorhombic, fourfold perovskite cell:

- \(a=5.5116\) Å, \(b=5.6010\) Å, \(c=7.8460\) Å
- \(V=242.21\) Å³, \(Z=1\)
- ordered perovskite formulation  
  \((\mathrm{Na}_{0.75}\mathrm{Nd}_{0.25})(\mathrm{Ti}_{0.5}\mathrm{Nb}_{0.5})\mathrm O_3\)
- best-supported symmetry: polar **Pmm2** (No. 25)
- Ti/Nb are rock-salt ordered; one of the four A sites is Nd and the other three are Na.

The low-angle reflections 001, 010 and 100 at approximately 11.27°, 15.81° and 16.07° require cation ordering and exclude the usual Pnma/Pbnm disordered-perovskite model. The principal structure is:

```cif
data_Na3NdTi2Nb2O12
_audit_creation_method              'Powder indexing and chemically constrained ordered-perovskite model'
_chemical_name_common               'Sodium neodymium titanium niobium oxide'
_chemical_formula_sum               'Na3 Nd Nb2 Ti2 O12'
_chemical_formula_structural        'Na3NdTi2Nb2O12'
_cell_formula_units_Z               1

_symmetry_space_group_name_H-M       'P m m 2'
_symmetry_Int_Tables_number          25
_space_group_crystal_system          orthorhombic
_space_group_name_H-M_alt            'P m m 2'
_space_group_IT_number               25

_cell_length_a                       5.5116
_cell_length_b                       5.6010
_cell_length_c                       7.8460
_cell_angle_alpha                    90
_cell_angle_beta                     90
_cell_angle_gamma                    90
_cell_volume                         242.21

_exptl_crystal_density_diffrn        4.708
_diffrn_radiation_type               'Cu Kalpha1'
_diffrn_radiation_wavelength         1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y,z'
3  'x,-y,z'
4  '-x,-y,z'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Na  1
Nd  3
Ti  4
Nb  5
O  -2

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Nd1  Nd  1  0.50000  0.00000  0.25000  1.000  0.010
Na1  Na  1  0.00000  0.50000  0.25000  1.000  0.010
Na2  Na  1  0.50000  0.00000  0.75000  1.000  0.010
Na3  Na  1  0.00000  0.50000  0.75000  1.000  0.010

Ti1  Ti  1  0.00000  0.00000  0.00000  1.000  0.008
Nb1  Nb  1  0.50000  0.50000  0.00000  1.000  0.008
Nb2  Nb  1  0.00000  0.00000  0.50000  1.000  0.008
Ti2  Ti  1  0.50000  0.50000  0.50000  1.000  0.008

O1   O   4  0.25000  0.25000  0.00000  1.000  0.015
O2   O   4  0.25000  0.25000  0.50000  1.000  0.015
O3   O   1  0.00000  0.00000  0.25000  1.000  0.015
O4   O   1  0.50000  0.50000  0.25000  1.000  0.015
O5   O   1  0.00000  0.00000  0.75000  1.000  0.015
O6   O   1  0.50000  0.50000  0.75000  1.000  0.015
```

Representative indexing is:

| 2θ observed | hkl |
|---:|:---|
| 11.27° | 001 |
| 15.81° | 010 |
| 16.07° | 100 |
| 19.46° | 011 |
| 19.67° | 101 |
| 22.62–22.65° | 110, 002 |
| 27.74° | 012 |
| 27.89° | 102 |
| 31.93° | 020 |
| 32.22° | 112 |
| 32.46° | 200 |

The inversion-related polar ordering domain and axis/order twins are powder-equivalent and do not require separate CIFs. Small oxygen displacements into a Pm or P1 subgroup may survive a full Rietveld refinement, but they are not uniquely determined by this powder pattern alone.
