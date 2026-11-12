# Powder XRD phase analysis

The 900 °C SrCO3 + WO3 pattern is best described by five crystalline components. The reported fractions are normalized over those modeled crystalline phases; this analysis does not quantify amorphous material.

| Phase | Weight fraction | Main evidence | Assessment |
|---|---:|---|---|
| Scheelite SrWO4, I 41/a | 0.6060 | Dominant line set; refined from COD 1546036 | High confidence |
| Monoclinic WO3, P 21/n | 0.1069 | The 23.5–24.7° triplet and its higher-angle line set; COD 1528915 | High confidence |
| Sr3WO6-like phase, P 1 | 0.0832 | Independent residual peaks and a strong profile reduction using a Ba3WO6 framework (COD 1534803) with Ba→Sr substitution | Phase family supported; atomic model tentative |
| Fergusonite SrWO4, I 2/a | 0.0920 | Lines near 29.75, 35.31, 48.57, 50.55, 59.58 and 61.22°; COD 1546037 | Moderate confidence |
| Tetragonal Sr4.26W10O30 bronze, P 4/mbm | 0.1119 | Coherent lines near 22.09, 30.90, 32.62, 44.67, 53.44, 57.0 and 67.04°; Ca4.26W10O30 framework (COD 4030741) with Ca→Sr substitution | Phase family supported; composition/coordinates tentative |

The nested fits improved from Rwp 15.96% for scheelite + WO3 to 14.63% after adding the Sr3WO6-like component, 13.34% after adding fergusonite, and 12.55% after adding the bronze framework. Refinement of cells, bounded profile/specimen terms, selected coordinates and phase fractions gave a final native GSAS-II replay of Rwp = 11.126%, Rp = 7.992%, Rexp = 3.527% and GOF = 3.155 on all 8,282 points. `fit.csv` is generated from that replay, not from cached project arrays.

Important uncertainty remains. The Sr3WO6 and bronze models are analogue-derived rather than unique ab-initio solutions, and their scales correlate with texture, strain and roughness. The P1 Sr3WO6 model contains two pairs of half-occupied split Sr sites (0.68 and 0.80 Å separations); they must be interpreted as mutually exclusive disorder, not simultaneous atoms. The published monoclinic WO3 model also has 1.65 Å O–O contacts that trigger a conservative geometry-review threshold. Neither issue is a fully occupied hard contact, but both warrant caution. The fergusonite assignment is less secure than scheelite/WO3 because it is a minority polymorph with overlap.

Accordingly, the point fractions are suitable as a crystalline-phase estimate, but formal fraction uncertainties cannot be determined reliably from this uncalibrated, strongly correlated multiphase refinement. A practical uncertainty is several weight percent for each analogue-derived minority phase. Residual structured intensity and Rwp well above Rexp show that the submitted atomic models are not unique at the site level. The exact Sr3WO6 split-site structure and exact bronze stoichiometry should therefore be treated as unresolved beyond the submitted best-fit models.
