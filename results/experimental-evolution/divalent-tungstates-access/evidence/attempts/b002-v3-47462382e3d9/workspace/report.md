# Powder XRD phase analysis

The refined crystalline assemblage is 58.51 wt% wolframite MnWO4, 21.48 wt% monoclinic gamma-WO3, and 20.01 wt% monoclinic Mn3WO6. Fractions are normalized over these three modeled crystalline phases. A fresh full-grid replay of `final.gpx`, regenerating reflections and structure factors from the saved atomic models, gives Rwp = 7.359%, Rp = 4.878%, chi-square = 113102.1, and GOF = 3.697 for 8301 observations. The replay raised no negative-width, negative-background, displacement-parameter, or other profile-physics flags.

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| MnWO4 | P 2/c | a=4.79479, b=5.70103, c=4.97026, beta=91.1079 | 0.58507 |
| WO3 | P 21/c | a=7.68182, b=7.53271, c=10.5102, beta=136.063 | 0.21483 |
| Mn3WO6 | C 2/c | a=14.8949, b=8.92047, c=10.8633, beta=91.5043 | 0.20009 |

## Evidence and model selection

MnWO4 (COD 1520200 starting model) accounts for the dominant wolframite reflections, while gamma-WO3 (COD 2311041) accounts for a second sharp family and is chemically expected from the WO3 precursor. Refining only these two phases left a coherent, broad family, notably near 19.85, 20.40, 35.11, and 46.49 degrees 2theta; its independent-replay Rwp was 17.31%.

That family is indexed by a C 2/c Mn3WO6 model transferred from the Zn3TeO6 framework (COD 2211529; Zn to Mn and Te to W), followed by cell and physically constrained profile adaptation. It gives a substantially better comparably relaxed fit than a Pnnm Mn2WO5 alternative (Rwp 10.08%) or a distinct Co3TeO6-derived C 2/c coordinate start (Rwp 12.81%). Common tetragonal and orthorhombic Mn3O4 precursor models refined to about 0.1-0.2 wt%, and Pnma Mn3W2O9 collapsed; they were therefore rejected. No additional coherent residual reflection family remained after accepting the three phases. The resulting Mn:W atomic inventory ratio is 0.992, consistent with an approximately balanced Mn/W reaction inventory.

Heavy-atom coordinates were relaxed for MnWO4 and WO3. Oxygen shifts that produced implausible coordination were rolled back. The accepted Mn3WO6 parent coordinates have a shortest contact of 1.920 angstrom and W-O distances of about 1.92-2.00 angstrom; lower-residual free-coordinate trials created unphysical 1.55 angstrom W-O or 1.48 angstrom Mn-O contacts and were rejected.

## Remaining uncertainty

The MnWO4 and WO3 identifications are strong. The Mn3WO6 composition, C 2/c topology, and approximate fraction are supported by a distinct reflection family, fit improvement, physical geometry, and reaction balance, but its exact polytype and light-atom coordinates are less secure because the phase is broad and the model required cross-chemistry prototype transfer. Its structure therefore cannot be claimed as uniquely determined from this scan alone. The formal GSAS-II fraction standard errors (about 0.08-0.09 absolute wt%) are conditional on the chosen models and underestimate systematic phase/profile uncertainty; especially for WO3 and Mn3WO6, practical abundance uncertainty is at the few-wt% level.
