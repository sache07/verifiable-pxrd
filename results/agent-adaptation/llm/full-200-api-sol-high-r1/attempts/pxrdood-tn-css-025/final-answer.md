The pattern contains a very clear hexagonal sub-pattern with approximately

\[
a=6.692\ \text{Å},\qquad c=5.494\ \text{Å}.
\]

For example, the reflections 100, 001, 101, 110, 200 and 002 occur at about 15.28°, 16.13°, 22.29°, 26.63°, 30.84° and 32.59°, respectively. Together with the composition and cell volume, this points to the **hexagonal Cr\(_{12}\)P\(_5\)-type Fe\(_{12}\)As\(_5\)** structure, Pearson symbol hP17, most plausibly \(P\bar6\) (No. 174), \(Z=1\).

However, this model does **not** index several strong peaks, particularly those near 27.14°, 41.54°, 42.57°, 44.24° and 47.32°. The supplied pattern therefore appears multiphase or contains a lower-symmetry/superstructure contribution. Consequently, the atomic coordinates below should be treated as a prototype-constrained starting model rather than a uniquely powder-refined solution.

### Primary candidate CIF

```cif
data_Fe12As5_Cr12P5_type_candidate
_audit_creation_method
'Prototype-constrained solution from supplied Cu Kalpha1 powder pattern'
_audit_creation_date              2025-01-01
_audit_update_record
'Cell well constrained; fractional coordinates are an unrefined starting model'

_chemical_name_systematic         'Iron arsenide, Fe12As5'
_chemical_formula_sum             'Fe12 As5'
_chemical_formula_structural      'Fe12As5'
_cell_formula_units_Z             1

_symmetry_space_group_name_H-M    'P -6'
_symmetry_space_group_name_Hall   'P -6'
_symmetry_Int_Tables_number       174

_cell_length_a                    6.692
_cell_length_b                    6.692
_cell_length_c                    5.494
_cell_angle_alpha                 90
_cell_angle_beta                  90
_cell_angle_gamma                 120
_cell_volume                      212.99

_exptl_crystal_density_diffrn     8.14

loop_
_symmetry_equiv_pos_as_xyz
'x,y,z'
'-y,x-y,z'
'-x+y,-x,z'
'-x,-y,-z'
'y,-x+y,-z'
'x-y,x,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Fe1  Fe  0.1860  0.3710  0.1450  1.0  0.010
Fe2  Fe  0.4490  0.1190  0.3520  1.0  0.010
As1  As  0.0000  0.0000  0.0000  1.0  0.008
As2  As  0.333333  0.666667  0.2520  1.0  0.008
As3  As  0.333333  0.666667  0.5000  1.0  0.008
```

The multiplicities are \(6+6\) for Fe and \(1+2+2\) for As, giving exactly Fe\(_{12}\)As\(_5\).

A definitive CIF cannot be extracted reliably without separating the additional diffraction contribution and performing whole-pattern refinement. In particular, the strong 42.57° peak is incompatible with the stated hexagonal cell and should not be ignored when deciding whether this is the majority phase.
