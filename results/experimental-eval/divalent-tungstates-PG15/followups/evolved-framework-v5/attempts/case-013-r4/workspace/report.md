# Powder XRD phase analysis

The 500 °C PbO + WO3 specimen is modeled as five crystalline phases. Fractions below are normalized over the modeled crystalline material; this experiment does not determine an amorphous fraction.

| Phase | Space group | Crystalline wt.% |
|---|---:|---:|
| PbWO4, stolzite | I41/a | 59.79 |
| Pb2WO5 | C2/m | 15.00 |
| PbO, massicot | Pbcm | 9.47 |
| WO3, monoclinic | P21/c | 9.22 |
| PbO, litharge | P4/nmm | 6.51 |

The full-grid Rietveld fit has Rwp = 10.150%, Rp = 6.868%, Rexp = 3.502%, and GOF = 2.905 for 8,282 points and 35 refined variables. The final cycle converged with maximum shift/esd 0.092.

## Evidence and model selection

Stolzite PbWO4 is fixed by the dominant 27.68, 29.89, 33.04, 45.01, 47.28, 51.46, 55.53 and 56.80° families. The starting structure was COD 9009811. A bounded oxygen adjustment of 0.071 Å improved relative intensities while retaining a regular 1.814 Å WO4 tetrahedron.

Pb2WO5 accounts for a broad independent family including 25.89, 29.26, 30.66, 31.04, 39.50, 47.25, 50.19 and 51.93°. No exact Pb2WO5 structure was present in the frozen index, so the model was derived from isostructural C2/m Pb2MoO5 (COD 7220560) by Mo6+ -> W6+ substitution. Pb/W positions were then adjusted by at most 0.192 Å. The resulting W–O distances are 1.69–1.93 Å and the structure passes the geometry screen.

Residual precursor families identify both massicot PbO (notably 29.35, 30.53, 38.09, 49.43, 53.27, 60.51 and 63.25°; COD 2310433) and monoclinic WO3 (23.37/23.85/24.65° triplet plus 33.5–34.4, 48.49 and 50.20°; COD 2311041). The selected WO3 model has six-coordinate W and no short O–O contacts. An older alternative gave a slightly lower preliminary Rwp but contained a 1.58 Å O–O contact and was rejected.

Litharge PbO is required by the 28.86, 32.08, 35.92, 48.77, 54.96, 59.43 and 60.02° family. COD 9012700 was transformed to GSAS-II's standard P4/nmm setting before refinement, preserving Z = 2 and a physical density of 9.33 g cm-3. Coexisting PbO polymorphs are plausible for incompletely reacted material near the PbO transformation region.

Raspite PbWO4, Pb7W8O28.8, and an Mo-to-W-transferred Pb5WO8 model were tested against the complete multiphase checkpoint. Fixed-cell, nonnegative scale trials drove each to zero, so they were not included.

## Remaining uncertainty

The major stolzite assignment is robust, and every submitted minor phase has multiple independent reflections and a stable positive scale. The Pb2WO5 topology is less certain because it is an analogue-derived structure: its oxygen coordinates and its approximately 15 wt.% fraction cannot be regarded as a unique structure solution. Strong overlap, preferred orientation, and phase-specific broadening also correlate the two PbO fractions; litharge refined to the supported 0.04 micrometre size lower bound. Consequently, the minor-phase fractions are semiquantitative even though the crystalline-only vector is internally normalized.

Systematic residual intensity/profile structure remains (Rwp is above Rexp), so trace phases below the detection supported by this pattern cannot be excluded. No additional phase could be assigned with a physical structure and stable positive scale.
