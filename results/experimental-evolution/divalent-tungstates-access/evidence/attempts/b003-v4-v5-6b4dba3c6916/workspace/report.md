# Powder XRD phase analysis

## Result

Three crystalline phases account for every coherent peak family in the measured pattern. Fractions below are normalized over those modeled crystalline phases.

| Phase | Space group | Weight fraction | Formal s.u. | Structural model |
|---|---:|---:|---:|---|
| MnWO4, wolframite | P 2/c | 62.989 wt% | 0.109 wt% | [phase_1_MnWO4.cif](phase_1_MnWO4.cif) |
| Mn3WO6 | R -3 | 18.831 wt% | 0.105 wt% | [phase_2_Mn3WO6.cif](phase_2_Mn3WO6.cif) |
| WO3, monoclinic | P 21/c | 18.180 wt% | 0.078 wt% | [phase_3_WO3.cif](phase_3_WO3.cif) |

The full-grid refinement gives Rwp = 2.9243%, Rp = 2.1307%, Rexp = 1.4263%, and goodness of fit = 2.0544 for 8,301 observations and 33 refined variables. An independent atomic forward replay of `final.gpx` reproduces Rwp = 2.9243% and raises no physical-profile review flags.

## Evidence and model selection

The dominant reflections index as wolframite MnWO4. Two coherent residual families are then explained by trigonal Mn3WO6 and low-symmetry WO3; after adding them, the remaining residuals are intensity/line-shape errors at accepted reflections rather than a new peak family. The phase inventory is also chemically coherent with the laboratory's nominal 1:1 Mn:W dosing context: the refined inventory has Mn:W = 1.019, and its WO3:Mn3WO6 molar ratio is 1.85 versus 2.00 for exact balance with MnWO4.

WO3 topology was screened in the same three-phase state. Triclinic and monoclinic low-symmetry models were the only competitive branches; orthorhombic, tetragonal, and hexagonal models missed resolved splitting and gave substantially worse or boundary-limited fits. The submitted P 21/c neutron parent (COD 2311041) was selected because it preserves complete WO6 coordination and sensible geometry. An older monoclinic record with a slightly better early profile fit contained a 1.57 A O-O contact and was rejected. The P -1 alternative remains a genuine powder-data ambiguity, so the exact WO3 distortion symmetry is less secure than the phase identity.

The submitted geometries pass direct distance screening. MnWO4 has Mn-O = 2.071-2.238 A and W-O = 1.853-2.034 A; Mn3WO6 has Mn-O = 2.101-2.323 A and W-O = 1.903-1.941 A. Both independent W sites in WO3 remain six-coordinate, with W-O = 1.652-2.226 A and no short O-O contact (minimum 2.536 A). Free coordinate refinements that produced bad contacts were rolled back; only bounded, geometry-preserving coordinate updates were retained.

## Refinement details

The Cu K-alpha doublet and reported Kalpha2/Kalpha1 ratio were fixed to the metadata. The accepted model refines phase scales and cells, an eight-term background, crystallite sizes, a common profile term, zero, and polarization. Supported specimen terms are March-Dollase texture for MnWO4 [111] (ratio 1.1448) and WO3 [010] (ratio 1.3094), plus uniaxial MnWO4 microstrain along [010] (848 ppm transverse and 5,398 ppm axial). Phase-common Uiso values of 0.01221(73) A2 for Mn3WO6 and 0.00487(50) A2 for WO3 are physical and supported. Additional Mn3WO6 texture, surface roughness, and further anisotropic broadening were rejected as axis-degenerate, collapsed, boundary-limited, or strongly correlated.

Specimen displacement and angular zero could not be separated reliably. The replay therefore fixes displacement at +800 micrometres for the 200 mm radius and refines zero to +0.207670 degrees; their decomposition should not be interpreted as an independent height measurement.

## Remaining uncertainty

The tabulated standard uncertainties are covariance-only and are much smaller than realistic systematic uncertainty from preferred orientation, profile overlap, and the WO3 topology choice. A practical reading is approximately a few absolute weight percent rather than the sub-0.2 wt% formal values. No internal standard was supplied, so amorphous material cannot be quantified and the reported fractions apply only to the modeled crystalline inventory.

Mn3O4 cannot be determined reliably at trace level. Final-state tests from 0.5, 2, and 5 wt% starts retained 0.74-1.02 wt% but changed Rwp by only 0.004-0.012 percentage points; all useful Mn3O4 reflections overlap accepted peaks, one branch reached the size bound, and there is no unique coherent Mn3O4 family. It is therefore listed in `result.json` as a possible unresolved trace and is not included in the normalized three-phase fractions.
