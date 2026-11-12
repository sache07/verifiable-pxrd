# Powder XRD phase analysis

## Result

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| MnWO4 | wolframite, P 2/c (No. 13) | 63.10 wt% |
| Mn3WO6 | rhombohedral, R -3 (No. 148) | 18.50 wt% |
| WO3 | monoclinic, P 21/c (No. 14) | 18.40 wt% |

The fractions are normalized over these three modeled crystalline phases. The final full-grid refinement has Rwp = 2.7029%, Rp = 1.9590%, Rexp = 1.4263%, and GSAS-II goodness of fit = 1.8993 for 8,301 points and 37 refined parameters.

## Evidence and model selection

The Cu K-alpha pattern requires all three phases. Diagnostic calculated families include MnWO4 at 15.248, 18.224, 29.750/30.210, and 37.234 degrees 2-theta; Mn3WO6 at 19.699, 20.225, 28.502, 35.007, and 46.379 degrees; and the characteristic monoclinic WO3 split group at 22.868, 23.359, and 24.155 degrees plus its 33.0-34.0 degree multiplet. The strongest remaining difference-profile lobes coincide with reflections of these accepted phases; no coherent fourth peak family remains.

Starting structures were COD 1520200 (MnWO4), COD 2002703 (Mn3WO6), and COD 2311041 (WO3). Comparable three-phase WO3 screens gave Rwp about 6.76% for the selected physical monoclinic parent, 6.77% for a triclinic parent, and 8.15% for an orthorhombic parent before the later common coordinate/specimen refinements. Another nominal P21/c record reached about 6.64% but was rejected because it produced a 1.575 A O-O contact. The selected refined models retain physical octahedra: minimum O-O distances are 2.445, 2.531, and 2.516 A for MnWO4, Mn3WO6, and WO3, respectively; metal-oxygen distances are also chemically reasonable.

The refined phase inventory gives an Mn:W molar ratio of 1.012:1, independently closing the laboratory's 1:1 metal feed. Cell, bounded heavy- and oxygen-coordinate, crystallite-size, microstrain, and profile terms were staged. Only supported specimen corrections were retained: MnWO4 [010] uniaxial microstrain, MnWO4 [111] March-Dollase texture, and WO3 [010] texture. Trial phase-wide displacement-parameter refinements changed Rwp by less than 0.001 percentage point and were rejected.

## Remaining uncertainty

Phase identities and coordination topologies are reliable, but individual oxygen coordinates from laboratory XRD are less well determined than the phase assignments. The covariance-only fraction errors are 0.05-0.07 wt%, which are unrealistically small as total errors: MnWO4 scale and the surface-roughness term are 95.9% correlated, and preferred orientation overlaps scale. A realistic reading is therefore about +/-1-2 absolute wt% for the reported fractions. These values do not quantify amorphous material because no internal standard was supplied. Crystallite-size and microstrain values should likewise be treated as profile-model parameters rather than unique microstructural measurements.

The submitted CIFs, `fit.csv`, and phase fractions were exported from the replayed, converged project `final.gpx`; three consecutive final passes remained at Rwp = 2.70293% with no frozen variables.
