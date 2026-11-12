# Powder X-ray diffraction analysis

The pattern is described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO4 | I 41/a | a = b = 5.42558, c = 11.97427 | 64.31% |
| WO3 | P 21/c | a = 7.70264, b = 7.54844, c = 10.54385, beta = 136.07469 | 9.60% |
| Sr2WO5 | P n m a | a = 7.26135, b = 5.55519, c = 10.90892 | 26.09% |

## Evidence

Scheelite SrWO4 is the dominant phase and accounts for the major peak families throughout the measured range; its starting model was COD 1546036. The remaining coherent features require both monoclinic WO3 and an orthorhombic Sr2WO5 phase. The physically sound P21/c WO3 model (COD 2311041) accounts for the characteristic clustered reflections near 23.5–24.7° and additional higher-angle families. Under the same provisional three-phase nuisance model it fitted slightly better than the older WO3 alternative (Rwp 8.376% versus 8.412%), which also contained four implausibly short O–O contacts near 1.58 Å.

No exact Sr2WO5 database entry was available. A stoichiometric-analogue search identified Pnma Ba2ReO5 (COD 1529756); Ba→Sr and Re→W substitutions preserve the A2BO5 stoichiometry and the relevant divalent-A/high-valent-B chemistry. After refinement, this model accounts for coherent families near 15.03, 16.62, 20.68, 22.10, 26.23, 29.75, 30.91, 32.60, and 44.65°. Alternative Pnma rare-earth titanate parents either refined to effectively zero scale or produced contacts as short as 1.19–1.27 Å. The submitted Sr2WO5 model passes the contact/geometry screen, with its shortest W–O separation about 1.77 Å.

The final Rietveld fit has Rwp = 7.5494%, Rp = 5.6338%, and goodness of fit = 2.1384 for 8,282 observations and 22 refined variables. It uses a smooth three-term background, one zero correction (+0.37534°), a common instrumental profile, low-angle roughness, and phase-specific isotropic crystallite sizes. Microstrain, preferred orientation, anisotropic broadening, and polarization variants were tested but were unsupported, singular, or bound-seeking and were pruned. Reopening and replaying `final.gpx` reproduces the profile and fractions; an independent atomic replay gave Rwp = 7.5494% with no profile-review flags.

## Remaining uncertainty

SrWO4 is identified reliably. WO3 is a minor, substantially overlapped component, so its detailed coordinates and fraction are less precise than those of SrWO4 even though the monoclinic assignment is well supported. The Sr2WO5 phase and its nonzero fraction are supported by multiple partly unique families, but its submitted structure is analogue-derived: the cell and heavy-atom positions were refined, whereas the oxygen arrangement remains inherited from the Ba2ReO5 prototype and cannot be determined independently from this powder pattern. Accordingly, the Sr2WO5 CIF is a physically plausible structural model rather than a unique ab-initio structure determination.

The reported fractions are model-dependent Rietveld fractions; no internal standard was present, so amorphous material or an undetected trace phase cannot be quantified. No additional coherent residual family justified another crystalline phase.
