The pattern indexes as an ordered, doubled-\(c\) clinopyroxene superstructure. The strongest low-angle reflections are consistent with approximately:

- 13.33°: 110  
- 17.12°: \(10\bar2\)  
- 18.53°: 200  
- 19.27°: 020  
- 19.44°: 012  
- 21.19°: 102  
- 26.85°: 220  
- 29.61°: 310  
- 30.57°: 130  

This gives \(a\approx9.874\), \(b\approx9.205\), \(c\approx10.841\) Å, \(\beta\approx104.285^\circ\). The most plausible symmetry is \(P2_1/c\), with ordered Sc and In and \(Z=4\) for Na₂ScInSi₄O₁₂. The CIF below is a chemically constrained ordered-pyroxene model; the oxygen coordinates should be regarded as a Rietveld starting model rather than publication-precision single-crystal coordinates.

```cif
data_Na2ScInSi4O12_ordered_clinopyroxene
_audit_creation_method
'Powder indexing and ordered-clinopyroxene constrained structure model'

_chemical_name_systematic
'Disodium scandium indium tetrasilicate'
_chemical_formula_sum              'Na2 Sc In Si4 O12'
_chemical_formula_structural       'Na2ScIn(SiO3)4'
_chemical_formula_weight           510.08
_cell_formula_units_Z              4

_cell_length_a                     9.8744
_cell_length_b                     9.2047
_cell_length_c                     10.8412
_cell_angle_alpha                  90
_cell_angle_beta                   104.285
_cell_angle_gamma                  90
_cell_volume                       954.7

_space_group_crystal_system        monoclinic
_space_group_name_H-M_alt          'P 21/c'
_space_group_IT_number             14

_diffrn_radiation_type             'Cu Kalpha1'
_diffrn_radiation_wavelength       1.5406

loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x,y,z'
2 '-x,y+1/2,-z+1/2'
3 '-x,-y,-z'
4 'x,-y+1/2,z+1/2'

loop_
_atom_type_symbol
_atom_type_oxidation_number
Na  1
Sc  3
In  3
Si  4
O  -2

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_B_iso_or_equiv
Na1  Na  4  0.0000  0.3000  0.1250  1.0  1.00
Na2  Na  4  0.5000  0.8000  0.1250  1.0  1.00

Sc1  Sc  4  0.0000  0.9060  0.1250  1.0  0.50
In1  In  4  0.5000  0.4060  0.1250  1.0  0.50

Si1  Si  4  0.2872  0.0932  0.1147  1.0  0.40
Si2  Si  4  0.7128  0.0932  0.1353  1.0  0.40
Si3  Si  4  0.2872  0.0932  0.6147  1.0  0.40
Si4  Si  4  0.7128  0.0932  0.6353  1.0  0.40

O11  O   4  0.1155  0.0879  0.0707  1.0  0.70
O12  O   4  0.8845  0.0879  0.1793  1.0  0.70
O13  O   4  0.1155  0.0879  0.5707  1.0  0.70
O14  O   4  0.8845  0.0879  0.6793  1.0  0.70

O21  O   4  0.3610  0.2508  0.1592  1.0  0.70
O22  O   4  0.6390  0.2508  0.0908  1.0  0.70
O23  O   4  0.3610  0.2508  0.6592  1.0  0.70
O24  O   4  0.6390  0.2508  0.5908  1.0  0.70

O31  O   4  0.3501  0.0188  0.4977  1.0  0.70
O32  O   4  0.6499  0.0188  0.2523  1.0  0.70
O33  O   4  0.3501  0.0188  0.9977  1.0  0.70
O34  O   4  0.6499  0.0188  0.7523  1.0  0.70
```

The principal alternative is the Sc/In-interchanged ordering domain; it has the same powder pattern and is obtained simply by exchanging `Sc1` and `In1`. A disordered \(C2/c\) half-\(c\) pyroxene model is not favored because it does not account for the observed superstructure reflections and the \(10\bar2/102\) splitting.
