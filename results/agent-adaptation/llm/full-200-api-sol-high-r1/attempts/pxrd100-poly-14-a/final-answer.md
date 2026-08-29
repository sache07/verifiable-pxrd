The peak positions index well with an **orthorhombic primitive cell**, approximately

\[
a=6.956\ \text{Å},\quad b=5.662\ \text{Å},\quad c=13.824\ \text{Å},
\]

with the systematic absences of **Pbca, No. 61**. Particularly diagnostic axial reflections are 002 at 12.80°, 020 at 31.58°, 006 at 39.05°, 400 at 52.58°, 008 at 52.95°, and 040 at 65.94°. The cell contains \(Z=8\) PbAuO\(_2\) formula units.

The cell and space group are considerably more secure than the atomic coordinates. Pb and Au differ by only three electrons, so Cu X-ray powder data have weak contrast between their sites; the oxygen coordinates are also relatively insensitive. The following is therefore a direct-space structural model suitable as a starting point for Rietveld refinement, not a publication-grade final refinement.

### Primary CIF

```cif
data_PbAuO2_primary
_audit_creation_method
;Indexed from the supplied Cu Kalpha1 powder pattern.
Atomic coordinates are a provisional direct-space Pbca model and
should be refined against the original profile.
;

_chemical_name_common                  'lead gold dioxide'
_chemical_formula_sum                  'Pb8 Au8 O16'
_chemical_formula_structural           'Pb Au O2'
_cell_formula_units_Z                  8

_cell_length_a                         6.9560
_cell_length_b                         5.6620
_cell_length_c                         13.8240
_cell_angle_alpha                      90
_cell_angle_beta                       90
_cell_angle_gamma                      90
_cell_volume                           544.55

_space_group_name_H-M_alt              'P b c a'
_space_group_IT_number                 61

_diffrn_radiation_type                 'Cu Kalpha1'
_diffrn_radiation_wavelength           1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y+1/2,z'
3  'x,-y,z+1/2'
4  'x+1/2,y,-z'
5  '-x,-y+1/2,z+1/2'
6  '-x+1/2,y+1/2,-z'
7  'x+1/2,-y,-z+1/2'
8  '-x+1/2,-y+1/2,-z+1/2'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Au1  Au  8  c  0.0050  0.0080  0.1240  1.0  0.010
Pb1  Pb  8  c  0.2520  0.0180  0.3740  1.0  0.010
O1   O   8  c  0.1180  0.3500  0.2460  1.0  0.015
O2   O   8  c  0.3860  0.5000  0.2520  1.0  0.015
```

### Surviving cation-site alternative

Because Pb and Au have nearly equal X-ray scattering powers, the cation-swapped model is difficult to reject from this powder pattern alone:

```cif
data_PbAuO2_Pb_Au_swapped
_audit_creation_method
;Cation-site alternative to the primary Pbca model.
Pb and Au are interchanged; neutron, anomalous-dispersion, or
chemical/bond-valence information is needed to discriminate reliably.
;

_chemical_formula_sum                  'Pb8 Au8 O16'
_chemical_formula_structural           'Pb Au O2'
_cell_formula_units_Z                  8

_cell_length_a                         6.9560
_cell_length_b                         5.6620
_cell_length_c                         13.8240
_cell_angle_alpha                      90
_cell_angle_beta                       90
_cell_angle_gamma                      90

_space_group_name_H-M_alt              'P b c a'
_space_group_IT_number                 61

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,y+1/2,z'
3  'x,-y,z+1/2'
4  'x+1/2,y,-z'
5  '-x,-y+1/2,z+1/2'
6  '-x+1/2,y+1/2,-z'
7  'x+1/2,-y,-z+1/2'
8  '-x+1/2,-y+1/2,-z+1/2'

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
Pb1  Pb  8  c  0.0050  0.0080  0.1240  1.0  0.010
Au1  Au  8  c  0.2520  0.0180  0.3740  1.0  0.010
O1   O   8  c  0.1180  0.3500  0.2460  1.0  0.015
O2   O   8  c  0.3860  0.5000  0.2520  1.0  0.015
```

The recommended refinement strategy is therefore: fix **Pbca and the indexed cell**, refine profile/background and zero shift first, then refine the four general-position coordinates with soft Au–O/Pb–O restraints, and finally test the Pb/Au site assignment using bond-valence or anomalous-dispersion data.
