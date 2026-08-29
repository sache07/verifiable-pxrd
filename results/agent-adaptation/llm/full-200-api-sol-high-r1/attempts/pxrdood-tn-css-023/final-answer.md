The pattern indexes convincingly as a **primitive orthorhombic** phase. The lowest-angle reflections are consistent with

- 11.59°: 001  
- 17.10°: 101  
- 22.805°: 020  
- 23.31°: 002  
- 25.22°: 200  
- 27.7–27.85°: overlapping 210/201  
- 35.28°: 202  
- 46.58°: 040  
- 47.81°: 004  

giving approximately:

\[
a=7.058\ \text{Å},\quad b=7.793\ \text{Å},\quad c=7.627\ \text{Å}.
\]

The missing 100 and 010 reflections, together with an observed 001, point to **P2₁2₁2 (No. 18)** as the leading space group. With \(Z=4\), the calculated density is about 15.14 g cm⁻³, chemically reasonable for NdIr₄B₄.

## Primary CIF — indexed phase

The supplied powder profile determines the lattice and likely extinction group, but it does **not uniquely determine the 27 independent positional parameters** required for the nine general sites in P2₁2₁2. Consequently, the following is an indexing/space-group CIF rather than a fabricated atomistic model.

```cif
data_NdIr4B4_indexed
_audit_creation_method
;
Powder indexing from the supplied Cu Kalpha1 pattern.
This CIF contains the defensible unit cell and probable space group.
Atomic coordinates have not been inserted because they are not uniquely
determined by the supplied one-dimensional profile alone.
;

_chemical_name_common                 'neodymium iridium boride'
_chemical_formula_structural          'NdIr4B4'
_chemical_formula_sum                 'Nd1 Ir4 B4'
_chemical_formula_weight              956.35
_cell_formula_units_Z                 4

_cell_length_a                        7.058
_cell_length_b                        7.793
_cell_length_c                        7.627
_cell_angle_alpha                     90
_cell_angle_beta                      90
_cell_angle_gamma                     90
_cell_volume                          419.51

_exptl_crystal_density_diffrn         15.14
_diffrn_radiation_type                'Cu Kalpha1'
_diffrn_radiation_wavelength          1.5406

_space_group_crystal_system           orthorhombic
_space_group_name_H-M_alt             'P 21 21 2'
_space_group_IT_number                18

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1  'x,y,z'
2  '-x,-y,z'
3  'x+1/2,-y+1/2,-z'
4  '-x+1/2,y+1/2,-z'

loop_
_pd_index_h
_pd_index_k
_pd_index_l
_pd_index_2theta
_pd_index_d_spacing
0 0 1  11.590  7.627
1 0 1  17.100  5.181
0 2 0  22.805  3.8965
0 0 2  23.310  3.8135
2 0 0  25.220  3.5290
2 1 0  27.7    3.22
2 0 1  27.8    3.20
2 0 2  35.280  2.542
2 2 1  36.25   2.476
3 0 1  40.05   2.250
3 1 0  39.95   2.254
3 2 0  45.0    2.014
0 4 0  46.580  1.9483
0 0 4  47.810  1.9068
4 0 0  51.98   1.7645
```

### Remaining ambiguity

The principal surviving alternative is a lower-symmetry **P222/P2₁-type subgroup** with the same metric, if the missing 100 and 010 peaks are accidental structure-factor cancellations rather than screw-axis extinctions. It is less likely than P2₁2₁2. A complete atomistic CIF would require direct-space structure solution or database/prototype matching followed by Rietveld refinement; assigning coordinates without that step would not be defensible.
