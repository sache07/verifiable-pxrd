# Powder XRD phase analysis

The best whole-pattern model contains eight crystalline contributions. Fractions are normalized over these modeled crystalline phases; the data do not determine an amorphous fraction.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| SrWO4, scheelite | I41/a | 57.31% |
| WO3, monoclinic | P21/c | 10.84% |
| Sr3W2O9 | C2/c | 5.74% |
| Sr3WO6, cubic | Pa-3 | 10.48% |
| Sr3WO5 | I4/mcm | 6.70% |
| SrCO3, disordered rhombohedral | R-3m | 1.93% |
| Sr3WO6, monoclinic | P21/c | 3.08% |
| Sr2WO5 | P-1 | 3.92% |

The native, zero-parameter GSAS-II replay gives Rwp = 8.961%, Rp = 6.297%, and GOF = 2.538 on all 8,282 points. `fit.csv` is the replayed total profile, including background, and uses observed minus calculated for the difference column.

## Evidence

Scheelite SrWO4 and residual monoclinic WO3 account for the dominant peak families and are unambiguous. Published Sr3W2O9 gives a coherent set of secondary lines that cannot be represented by those two phases. Residual-profile searches then identified two strong Sr-rich framework families: cubic Pa-3 Sr3WO6 and tetragonal I4/mcm Sr3WO5. Both retain positive, substantial scales after joint refinement and explain multiple separated reflections rather than single peaks.

Three weaker components remain positive after all phases are co-refined. Rhombohedral SrCO3 is chemically consistent with unreacted precursor and improves a coherent low-intensity line set. A second, monoclinic Sr3WO6 polymorph and triclinic Sr2WO5 each improve the full-pattern residual and refine to physically screened cells and contacts. Their contributions are about 3–4 wt%, so they are above a one-peak trace assignment but are still overlap-sensitive.

Published starting models were used for SrWO4 (COD 1546036), WO3 (COD 1528915), Sr3W2O9 (COD 2311977), and SrCO3 (COD 1539128). The remaining structures are analogue-derived: Cu3WO6 COD 1527404 to Pa-3 Sr3WO6; Ba3SiO5 COD 2106454 to I4/mcm Sr3WO5; COD 4031607 to P21/c Sr3WO6; and Al2SiO5 COD 1542089 to P-1 Sr2WO5. Element substitutions, lattice metrics, phase profiles, preferred orientation, and small symmetry-preserving coordinate adjustments were refined only where supported by the pattern.

## Remaining uncertainty

The exact structures and fractions of the three weakest phases are not reliable at the same level as the two major phases. In particular, SrCO3, monoclinic Sr3WO6, and Sr2WO5 overlap other phases; their reported fractions are conditional on the eight-phase model and likely carry systematic uncertainty of roughly 1–2 percentage points absolute.

The selected WO3 reference is strongly preferred by the profile, but its exported model contains 1.64 Å O···O contacts and therefore requires structural adjudication. A conventional P21/c WO3 alternative passes the contact screen but worsens Rwp to about 9.28%; consequently, WO3 phase identity and abundance are secure, while its detailed oxygen coordinates are not. The half-occupied oxygen sites in R-3m SrCO3 represent orientational disorder and likewise trigger close-contact review rather than a unique ordered carbonate structure.

The analogue-derived off-stoichiometric structures are defensible framework models, not unique ab-initio solutions. Peak overlap, preferred orientation, correlated angular-zero/specimen-displacement terms, and the above-noise GOF limit coordinate and fraction precision. No claim is made for amorphous material or for thermodynamic stability of the minor polymorphs after cooling.
