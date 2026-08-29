The pattern indexes as a triclinic, centrosymmetric, ReS₂-type superstructure. A consistent indexing is:

- Space group: \(P\overline{1}\) (No. 2)
- \(a \approx 6.290\), \(b \approx 7.454\), \(c \approx 6.865\) Å
- \(\alpha \approx 123.52^\circ\), \(\beta \approx 88.50^\circ\), \(\gamma \approx 88.08^\circ\)
- \(Z=2\), \(V\approx267.8\) Å³
- Calculated density: approximately 8.57 g cm⁻³

Representative indexing includes 100 at 14.10°, 010 at 14.25°, 001 at 15.50°, 110 at 19.51°, 101 at 20.43°, 02−1 at 23.87°, 011 at 26.40°, 12−1 at 27.40°, 200 at 28.42°, 020 at 28.76°, and 002 at 31.28°.

The positional model below is a prototype-constrained powder solution. Sb and Te have almost identical Cu-Kα scattering factors, so their detailed ordering is not uniquely determined by this pattern.

### Primary CIF

```cif
data_FeOsSb2Te2_primary
_audit_creation_method              'Powder indexing and ReS2-type direct-space model'
_chemical_name_common               'iron osmium diantimonide ditelluride'
_chemical_formula_structural        'FeOsSb2Te2'
_chemical_formula_sum               'Fe1 Os1 Sb2 Te2'
_cell_formula_units_Z               2

_space_group_name_H-M_alt           'P -1'
_space_group_IT_number              2

_cell_length_a                      6.2898
_cell_length_b                      7.4540
_cell_length_c                      6.8648
_cell_angle_alpha                   123.520
_cell_angle_beta                    88.504
_cell_angle_gamma                   88.078
_cell_volume                        267.77

_exptl_crystal_density_diffrn       8.57
_diffrn_radiation_probe             x-ray
_diffrn_radiation_wavelength        1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,-z'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_B_iso_or_equiv
Os1  Os  2  0.4903  0.0564  0.2508  1.0  0.60
Fe1  Fe  2  0.5045  0.5116  0.2982  1.0  0.60
Sb1  Sb  2  0.2174  0.2508  0.1175  1.0  0.70
Sb2  Sb  2  0.2769  0.7581  0.1193  1.0  0.70
Te1  Te  2  0.7562  0.2662  0.3891  1.0  0.70
Te2  Te  2  0.6961  0.7368  0.3948  1.0  0.70
```

### Surviving ordering alternatives

The strongest unresolved ambiguity is Sb/Te ordering. A nearly diffraction-equivalent alternative is obtained by making the following substitutions in the atom loop:

```text
Sb1 ↔ Te1
Sb2 ↔ Te2
```

A weaker alternative, owing to the much larger Fe/Os scattering contrast, swaps the two transition-metal sublattices:

```text
Os1 at 0.5045 0.5116 0.2982
Fe1 at 0.4903 0.0564 0.2508
```

The primary assignment above is preferred, but anomalous diffraction or neutron data would be needed to establish the Sb/Te ordering reliably.
