The pattern indexes convincingly as an **orthorhombically distorted, Ti/Mo-ordered spinel**. The refined metric is approximately:

\[
a=7.5941\ \text{Å},\quad b=7.7939\ \text{Å},\quad c=10.8600\ \text{Å},\quad Z=4.
\]

Diagnostic indexing includes 011 at 13.98°, 101 at 14.22°, overlapping 002/110 near 16.3°, 112 at 23.13°, 200 at 23.42°, 022 at 28.16°, 202 at 28.67°, 004/220 near 32.9°, 040 at 46.56°, 224 at 47.27°, and 400 at 47.89°.

The CIF below uses an explicit P1 description of the I-centered ordered cell, avoiding imposition of uncertain higher symmetry. The atomic coordinates are an ordered-spinel prototype model rather than a full Rietveld refinement; the lattice and topology are considerably more certain than the small internal displacements.

```cif
data_TiCuMoSe4_ordered_orthorhombic_spinel
_audit_creation_method
'Powder indexing and ordered-spinel prototype model; atomic coordinates not fully Rietveld refined'

_chemical_name_common                 'titanium copper molybdenum selenide'
_chemical_formula_structural          'TiCuMoSe4'
_chemical_formula_sum                 'Cu1 Mo1 Se4 Ti1'
_cell_formula_units_Z                 4

_cell_length_a                        7.5941
_cell_length_b                        7.7939
_cell_length_c                        10.8600
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90
_cell_volume                          642.78

_exptl_crystal_density_diffrn         5.407
_diffrn_radiation_wavelength          1.5406

_space_group_crystal_system           orthorhombic
_space_group_name_H-M_alt             'P 1'
_space_group_IT_number                1

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x,y,z'

# Explicit nonprimitive I-centered orthorhombic cell.
# Cu occupies tetrahedral spinel sites.
# Ti and Mo occupy alternating octahedral sublattices.

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Cu1  Cu  0.25000  0.00000  0.12500  1.0
Cu2  Cu  0.75000  0.50000  0.62500  1.0
Cu3  Cu  0.75000  0.00000  0.87500  1.0
Cu4  Cu  0.25000  0.50000  0.37500  1.0

Ti1  Ti  0.00000  0.00000  0.50000  1.0
Ti2  Ti  0.50000  0.50000  0.00000  1.0
Ti3  Ti  0.50000  0.00000  0.50000  1.0
Ti4  Ti  0.00000  0.50000  0.00000  1.0

Mo1  Mo  0.25000  0.25000  0.75000  1.0
Mo2  Mo  0.75000  0.75000  0.25000  1.0
Mo3  Mo  0.25000  0.75000  0.75000  1.0
Mo4  Mo  0.75000  0.25000  0.25000  1.0

Se1  Se  0.51000  0.00000  0.25500  1.0
Se2  Se  0.01000  0.50000  0.75500  1.0
Se3  Se  0.25000  0.74000  0.99500  1.0
Se4  Se  0.75000  0.24000  0.49500  1.0
Se5  Se  0.25000  0.26000  0.99500  1.0
Se6  Se  0.75000  0.76000  0.49500  1.0
Se7  Se  0.99000  0.00000  0.25500  1.0
Se8  Se  0.49000  0.50000  0.75500  1.0
Se9  Se  0.49000  0.00000  0.74500  1.0
Se10 Se  0.99000  0.50000  0.24500  1.0
Se11 Se  0.75000  0.26000  0.00500  1.0
Se12 Se  0.25000  0.76000  0.50500  1.0
Se13 Se  0.75000  0.74000  0.00500  1.0
Se14 Se  0.25000  0.24000  0.50500  1.0
Se15 Se  0.01000  0.00000  0.74500  1.0
Se16 Se  0.51000  0.50000  0.24500  1.0
```

A global interchange of Ti and Mo gives the principal surviving ordering-domain alternative. The average higher symmetry is likely an **Imma-type orthorhombic spinel subgroup**, but the explicit-cell CIF is preferable until the internal coordinates and extinction conditions are refined against the complete profile.
