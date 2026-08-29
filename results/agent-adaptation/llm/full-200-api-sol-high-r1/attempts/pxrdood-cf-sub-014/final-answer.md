The peak positions are best indexed by a **large primitive cubic cell**, with

\[
a = 12.20(2)\ \text{Å}, \qquad V \approx 1816\ \text{Å}^3,
\]

and \(Z=16\) for Zr\(_4\)CoN. Representative indexing is \(210\), \(310\), \(420\), \(430/500\), \(440\), \(620\), \(710\), \(840\), etc. Several observed maxima are unresolved groups of adjacent cubic reflections. The likely symmetry is the chiral cubic pair **\(P4_132\) / \(P4_332\)**; powder diffraction cannot distinguish the two enantiomorphs.

However, the pattern provides only about 20 independent merged peak groups. A cP96 Zr\(_{64}\)Co\(_{16}\)N\(_{16}\) structure has too many positional variables for a unique ab-initio atomic solution from these data alone. Thus the defensible primary result is an indexed superstructure cell, not a uniquely refined coordinate model.

### Primary indexed CIF

```cif
data_Zr4CoN_cubic_superstructure
_audit_creation_method
'Le Bail indexing of supplied Cu Kalpha1 powder pattern; atomic coordinates unresolved'
_chemical_name_common                 'zirconium cobalt nitride'
_chemical_formula_sum                 'Zr64 Co16 N16'
_chemical_formula_structural          'Zr4CoN'
_cell_formula_units_Z                 16

_cell_length_a                        12.205
_cell_length_b                        12.205
_cell_length_c                        12.205
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90
_cell_volume                          1818.3

_space_group_crystal_system           cubic
_space_group_name_H-M_alt             'P 41 3 2'
_space_group_IT_number                213

_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

_exptl_crystal_density_diffrn         6.34

_refine_special_details
;
Peak positions establish a primitive cubic approximately 12.20-A
superstructure. P 41 3 2 and its enantiomorph P 43 3 2 cannot be
distinguished by ordinary powder diffraction. This CIF intentionally
contains no fabricated atomic coordinates.
;
```

### Provisional average-parent alternative

The strongest fundamental reflections are compatible with an approximately \(a/2\) parent cell, \(a_{\rm parent}\approx6.1025\) Å, of the Zr\(_4\)CoN \(I\overline{4}3m\) arrangement. This model does **not** reproduce the low-angle superstructure reflections and should only be used as an average starting model for supercell refinement.

```cif
data_Zr4CoN_average_parent
_audit_creation_method
'Average parent model inferred from the 12.205-A cubic superstructure'
_chemical_name_common                 'Zr4CoN average parent'
_chemical_formula_sum                 'Zr8 Co2 N2'
_chemical_formula_structural          'Zr4CoN'
_cell_formula_units_Z                 2

_cell_length_a                        6.1025
_cell_length_b                        6.1025
_cell_length_c                        6.1025
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90

_space_group_crystal_system           cubic
_space_group_name_H-M_alt             'I -4 3 m'
_space_group_IT_number                217

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Co1  Co  0.00000  0.00000  0.00000  1.0  0.008
N1   N   0.00000  0.00000  0.50000  1.0  0.008
Zr1  Zr  0.25000  0.25000  0.25000  1.0  0.008
```

A complete cP96 coordinate solution would require either a known Zr\(_4\)CoN prototype model, higher-resolution diffraction, or combined neutron/synchrotron data followed by direct-space and Rietveld refinement.
