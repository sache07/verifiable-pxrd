# Phase analysis and Rietveld refinement

## Result

Three crystalline phases are required. Weight fractions are normalized over these modeled crystalline phases.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| SrWO4 | scheelite, `I 41/a` | 61.16(15) wt% |
| SrCO3 | strontianite, `P n m a` | 14.39(15) wt% |
| WO3 | triclinic, `P -1` | 24.45(13) wt% |

The final fit has Rwp = 3.8364%, Rp = 2.9340%, Rexp = 2.8612%, and GOF = 1.3433 for 8301 unchanged observations and 30 variables. The quoted fraction uncertainties are GSAS-II covariance e.s.d.s, not expanded systematic uncertainties.

## Evidence and model selection

The inventory is chemically coherent with the reported 650 °C reaction of WO3 and SrCO3: scheelite SrWO4 is the major product and both starting materials remain. The residual SrCO3:WO3 mole ratio calculated from the refined fractions is 0.92, consistent with incomplete reaction at approximately matched precursor stoichiometry.

The intense scheelite families at approximately 27.18, 29.43, 32.62, and 44.80° 2theta establish SrWO4. Partly isolated SrCO3 families at 24.62, 25.26, 34.61, 36.04, and 43.61°, and WO3 multiplets near 22.5–23.8, 32.6–33.6, and 47–56°, are reproduced coherently. Under the same preliminary common profile, deleting SrCO3 worsened Rwp from 7.322% to 8.246%, while deleting WO3 worsened it to 11.833%.

No exact SrWO4 record was present in the supplied index, so the stoichiometric-analogue search was used. SrMoO4 (COD 2300460), EuWO4 (COD 1561850), and CaWO4 (COD 7219229) scheelite parents were screened. The submitted model uses EuWO4 with Eu2+ replaced by similarly sized Sr2+; it preserves the W–O tetrahedron and gives W–O = 1.769 Å and Sr–O = 2.569–2.599 Å. The Mo parent fitted worse and inherited an unsuitable tetrahedron; the Ca parent gave a slightly lower intermediate Rwp but less credible substitution geometry. The analogue-derived oxygen coordinate was therefore retained rather than over-refined.

Ambient orthorhombic SrCO3 (COD 9008198) was retained. Its high-temperature rhombohedral alternative refined to zero/frozen scale and was rejected. The carbonate geometry remains physical (C–O = 1.291–1.304 Å). High-pressure Sr3W2O9 was also rejected: its scale collapsed and its characteristic low-angle families were absent, in addition to its source conditions being inconsistent with the synthesis metadata.

WO3 polymorphs were compared under the same restrained nuisance model. The final triclinic model (COD 2106293) gives Rwp = 3.836% with 30 variables; the best room-temperature monoclinic `P 21/c` control (COD 2311041) gives 4.144% with 32 variables. The triclinic model also has the better contact geometry, with six-coordinate W–O ranges of 1.669–2.235 Å and no flagged short contact. Orthorhombic WO3 was substantially poorer. Thus `P -1` is the diffraction-selected submission, although the missing measurement temperature leaves some physical polymorph uncertainty.

## Refinement controls

The baseline uses a smooth six-coefficient Chebyshev background, one specimen-displacement correction, and nonnegative W/X profile terms; U, V, Y, Z, zero, roughness, and unused size/strain terms are fixed at neutral values. The refined displacement is +1.057 mm, so absolute cell metrics retain some displacement correlation. SH/L did not remain supported. Polarization refined to 0.7028; roughness trials hit a bound or correlated strongly with scale and were rejected.

Only an isotropic WO3 coherent-domain size is retained (0.160 µm). SrWO4 size/strain trials collapsed or hit bounds. A carbonate size term was re-challenged in the final triclinic model and improved Rwp by only 0.0005 percentage point, so it was neutralized. No isotropic strain or symmetry-appropriate anisotropic broadening was replay-stable. Isolated low-, middle-, and high-angle families showed no remaining systematic width or asymmetry trend that justified more profile terms.

March–Dollase texture was retained only after axis comparisons across multiple families: SrWO4 [110], r = 0.7391, and WO3 [001], r = 1.2670. Competing low-index WO3 axes gave Rwp values from 4.278% to 5.241% before coordinate completion, versus 3.904% for [001].

The prescribed staged heavy-atom test accepted only triclinic WO3 W3: the gain was 0.067 Rwp percentage point, the displacement was 0.148 Å (below the 0.15 Å guard), no variable froze, and contact checks passed. Other heavy sites either failed the gain threshold or produced unacceptable contacts. Two subsequent save/reopen replays preserved the result (final maximum shift/e.s.d. = 0.0022).

## Remaining uncertainty

The strongest residual remains in the WO3-rich 23.8° multiplet, and triclinic WO3 is normally associated with lower measurement temperatures than the common monoclinic form. Because measurement temperature was not supplied, the WO3 phase identity is secure but its exact polymorph and local coordinates are not completely definitive. Only one W site was safely refined; most WO3 oxygen and heavy-atom coordinates remain source-derived. Likewise, the detailed SrWO4 oxygen position is analogue-derived.

No external standard or calibrated instrumental profile was supplied, and counting uncertainties were absent; sqrt(counts) uncertainties were used. Preferred orientation and source-coordinate choices therefore make the real fraction uncertainty larger than the formal e.s.d.s. The reported fractions exclude any amorphous material and any crystalline phase below detection.
