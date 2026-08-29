The chemistry-constrained identification is the usual monoclinic \(\eta\)-Ni\(_3\)Sn\(_4\) structure, Pearson symbol **mC14**, space group **C2/m** (No. 12), with \(Z=2\). The atomic coordinates below are an appropriate literature-derived starting model for Rietveld refinement.

There is, however, a notable inconsistency: if the first column is strictly \(2\theta\), the first several peaks index almost exactly on an orthorhombic primitive metric of approximately \(a=5.805\), \(b=4.050\), \(c=7.89\) Å—for example 001, 100, 101, 010, 002 at 11.21, 15.25, 18.97, 21.93 and 22.52°. That metric is not the established ambient-pressure Ni\(_3\)Sn\(_4\) cell. Thus the CIF below should be treated as the primary chemistry-constrained model, but the angle metadata or the presence of an unusual polymorph should be checked before final refinement.

```cif
data_Ni3Sn4_eta_primary
_audit_creation_method              'chemistry-constrained identification from powder pattern'
_chemical_name_common               'eta-Ni3Sn4'
_chemical_formula_sum               'Ni6 Sn8'
_chemical_formula_structural        'Ni3Sn4'
_cell_formula_units_Z               2

_symmetry_space_group_name_H-M       'C 1 2/m 1'
_symmetry_Int_Tables_number          12
_space_group_crystal_system          monoclinic
_space_group_IT_number               12
_space_group_name_H-M_alt            'C 2/m'

_cell_length_a                       12.2140
_cell_length_b                        4.0600
_cell_length_c                        5.2180
_cell_angle_alpha                    90
_cell_angle_beta                    103.91
_cell_angle_gamma                    90

_exptl_crystal_density_diffrn         8.61

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y,-z'
3  '-x,-y,-z'
4  'x,-y,z'
5  'x+1/2,y+1/2,z'
6  '-x+1/2,y+1/2,-z'
7  '-x+1/2,-y+1/2,-z'
8  'x+1/2,-y+1/2,z'

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
Ni1  Ni  2  a  0.0000  0.0000  0.0000  1.0  0.50
Ni2  Ni  4  i  0.3050  0.0000  0.6810  1.0  0.50
Sn1  Sn  4  i  0.1510  0.0000  0.3330  1.0  0.50
Sn2  Sn  4  i  0.3910  0.0000  0.1340  1.0  0.50
```

For reference, the directly indexed metric implied by the supplied angle column is:

```cif
data_Ni3Sn4_unresolved_orthorhombic_metric
_audit_creation_method
;Pawley-type metric obtained directly from the supplied peak positions.
Atomic coordinates and space group are not determined.
;
_chemical_formula_structural        'Ni3Sn4'
_cell_length_a                       5.805
_cell_length_b                       4.050
_cell_length_c                       7.89
_cell_angle_alpha                    90
_cell_angle_beta                     90
_cell_angle_gamma                    90
_space_group_crystal_system          orthorhombic
_space_group_name_H-M_alt            'P 1'
```

The second block is intentionally lattice-only rather than an invented atomic solution. A final choice between it and conventional monoclinic Ni\(_3\)Sn\(_4\) requires confirmation that the supplied angles are true \(2\theta\) values and, ideally, an independent density or diffraction dataset.
