# Powder XRD phase analysis

The Cu Kα pattern from the PbO + WO₃ sample fired at 500 °C is best described by eight modeled crystalline phases. Weight fractions are normalized over those crystalline phases only; no amorphous fraction was measured.

| Phase | Space group / structural model | wt% | Formal 1σ (wt%) |
|---|---|---:|---:|
| PbWO₄, scheelite | I4₁/a | 54.94 | 0.24 |
| PbO, massicot | Pbcm | 11.30 | 0.14 |
| PbO, litharge | P4/nmm parent; P1-expanded CIF | 7.35 | 0.12 |
| WO₃, monoclinic | P2₁/n | 8.71 | 0.18 |
| W₃O₈, orthorhombic | P2₁2₁2 | 6.34 | 0.20 |
| PbO₂, cubic | Fm-3m | 2.81 | 0.11 |
| Pb₂O₃, monoclinic | P2₁/c | 5.40 | 0.19 |
| Pb₃O₄, tetragonal | P4₂/mbc | 3.16 | 0.14 |

The final full-range GSAS-II fit has Rwp = 11.45%, Rp = 8.00%, Rexp = 3.50%, and goodness of fit = 3.27 for 8,282 observations. Fractions use the GSAS-II `HAP scale × unit-cell mass` convention and were renormalized to sum to one.

## Evidence

Scheelite PbWO₄ is unambiguous from its dominant series near 27.70, 29.91, 33.05, 45.03, 47.28, 51.49, 55.54, and 56.82° 2θ. Residual precursor phases are supported independently: monoclinic WO₃ gives the low-angle group near 23.4–24.6°, while massicot and litharge account for distinct PbO reflections throughout approximately 29–63°. The litharge model was expanded to P1 solely to avoid a CIF origin-setting incompatibility between GSAS-II and other CIF readers; its exported atomic arrangement is recognized as P4/nmm.

W₃O₈ is supported by features near 25.93, 26.77, 29.2, 35.46, 36.0, 48.37, and 59.38°. Cubic PbO₂ is especially distinguished by the residual groups near 30.2, 50.2, and 59.6°. Pb₂O₃ and Pb₃O₄ retain positive scales in the joint refinement and account for separate parts of the crowded 26.7–34.5° region. Adding tetragonal PbO₂, WO₂, Pb₂O, or raspite PbWO₄ caused their scales to collapse to zero, so they were excluded.

Reference models were taken from COD records 9009811, 2310433, 9012700, 1528915, 2101050, 9005760, 2311012, and 1537983, then refined with bounded cell/profile/specimen parameters. Instrument terms and all ADPs remained in the measurement model's physical ranges; calculated intensity and background are positive across the full scan.

## Remaining uncertainty

The tabulated 1σ values are covariance-based counting-statistical errors and do not include model-selection uncertainty. The three minor oxidized lead phases overlap strongly, so their absolute fractions are less secure than the formal errors suggest. The W₃O₈ fraction is also model-dependent because its preferred-orientation parameter reached the allowed boundary (March–Dollase 0.70 along [010]). Litharge likewise reached bounds in c-axis mismatch and crystallite size. Residual systematic intensity remains near 25.9 and 31.0° and around several strong scheelite peaks, consistent with unresolved texture/reference-coordinate mismatch; no additional tested phase gave a stable physical solution.

Accordingly, the phase identities and approximate fractions are defensible, but detailed atom positions and ADPs—particularly for W₃O₈ and the minor lead oxides—cannot be determined reliably from this crowded powder pattern alone. The submitted CIFs should be treated as refined reference-based structural models, not independent structure solutions.

Atom-level geometry deserves additional caution: the selected WO₃ reference contains 1.58 Å O–O contacts flagged for review by the conservative oxide screen, and the Pb₂O₃ reference contains a very short approximately 1.33 Å Pb–O contact. These do not affect the indexed peak-position evidence, but neither local coordination should be interpreted as a reliably refined bond geometry.
