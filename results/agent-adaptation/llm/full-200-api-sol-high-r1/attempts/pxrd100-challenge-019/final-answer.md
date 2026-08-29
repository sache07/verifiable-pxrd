The peak positions index well with a **triclinic \(P\bar1\)** cell:

\[
a=6.4152,\quad b=6.3677,\quad c=6.3489\ \text{Å}
\]
\[
\alpha=87.839^\circ,\quad \beta=93.740^\circ,\quad \gamma=92.009^\circ,\quad Z=2.
\]

For example, the first five strong lines are indexed as \(10\bar1\), 101, 200, 020 and 002. The corresponding calculated positions are approximately 19.06, 20.34, 27.87, 28.04 and 28.17° 2θ.

The lattice and Nb substructure are well constrained. Li positions and especially O/F ordering are less secure because Li scatters very weakly and O and F differ by only one electron. The primary CIF below therefore represents a chemically restrained ordered model, with O assigned to the shortest Nb–anion bond.

### Primary CIF

```cif
data_Li2NbOF5_primary
_audit_creation_method
'Indexed from Cu Kalpha1 powder data; chemically restrained light-atom model'
_chemical_name_common                 'dilithium niobium oxide pentafluoride'
_chemical_formula_structural          'Li2NbOF5'
_chemical_formula_sum                 'Li2 Nb O F5'
_cell_formula_units_Z                 2

_cell_length_a                        6.4152
_cell_length_b                        6.3677
_cell_length_c                        6.3489
_cell_angle_alpha                     87.839
_cell_angle_beta                      93.740
_cell_angle_gamma                     92.009
_cell_volume                          258.48

_space_group_crystal_system           triclinic
_space_group_name_H-M_alt             'P -1'
_space_group_IT_number                2

_exptl_crystal_density_diffrn         2.798
_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Nb1  Nb  0.2500  0.0000  0.2500  1.0  0.008
Li1  Li  0.5500  0.3000  0.3500  1.0  0.020
Li2  Li  0.5500  0.7000  0.1500  1.0  0.020
O1   O   0.5200  0.0200  0.2600  1.0  0.014
F1   F   0.9490  0.9790  0.2430  1.0  0.014
F2   F   0.2650  0.3010  0.2700  1.0  0.014
F3   F   0.2300  0.6990  0.2280  1.0  0.014
F4   F   0.2600  0.0180  0.5570  1.0  0.014
F5   F   0.2400  0.9820  0.9430  1.0  0.014
```

### Surviving O/F-disordered alternative

The powder pattern alone cannot reliably distinguish an ordered terminal O atom from distributed O/F disorder. The principal alternative has the same framework and cell, with \(1/6\) O and \(5/6\) F on each anion site:

```cif
data_Li2NbOF5_OF_disordered
_audit_creation_method
'Alternative average O/F-disordered model from Cu Kalpha1 powder data'
_chemical_formula_structural          'Li2NbOF5'
_chemical_formula_sum                 'Li2 Nb O F5'
_cell_formula_units_Z                 2

_cell_length_a                        6.4152
_cell_length_b                        6.3677
_cell_length_c                        6.3489
_cell_angle_alpha                     87.839
_cell_angle_beta                      93.740
_cell_angle_gamma                     92.009
_cell_volume                          258.48

_space_group_crystal_system           triclinic
_space_group_name_H-M_alt             'P -1'
_space_group_IT_number                2

_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Nb1   Nb  0.2500  0.0000  0.2500  1.000000  0.008
Li1   Li  0.5500  0.3000  0.3500  1.000000  0.020
Li2   Li  0.5500  0.7000  0.1500  1.000000  0.020
X1O   O   0.5200  0.0200  0.2600  0.166667  0.014
X1F   F   0.5200  0.0200  0.2600  0.833333  0.014
X2O   O   0.9490  0.9790  0.2430  0.166667  0.014
X2F   F   0.9490  0.9790  0.2430  0.833333  0.014
X3O   O   0.2650  0.3010  0.2700  0.166667  0.014
X3F   F   0.2650  0.3010  0.2700  0.833333  0.014
X4O   O   0.2300  0.6990  0.2280  0.166667  0.014
X4F   F   0.2300  0.6990  0.2280  0.833333  0.014
X5O   O   0.2600  0.0180  0.5570  0.166667  0.014
X5F   F   0.2600  0.0180  0.5570  0.833333  0.014
X6O   O   0.2400  0.9820  0.9430  0.166667  0.014
X6F   F   0.2400  0.9820  0.9430  0.833333  0.014
```

The ordered versus disordered anion model would require neutron diffraction, solid-state NMR, or a chemically constrained joint refinement to distinguish reliably.
