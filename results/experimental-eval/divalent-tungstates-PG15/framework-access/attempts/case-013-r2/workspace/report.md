# Powder XRD phase analysis

The pattern is best represented by seven crystalline components. Weight fractions below are normalized over those modeled crystalline phases; the data do not determine an amorphous fraction or absolute crystalline yield.

| Phase | wt.% | Structural model | Assessment |
|---|---:|---|---|
| scheelite PbWO4 | 53.67 | COD 9009811; I41/a | high |
| monoclinic WO3 | 9.02 | COD 2311041; P21/c | high |
| massicot beta-PbO | 7.40 | COD 2310433; Pbcm | high |
| long-period alpha-PbO approximant | 6.68 | COD 1533609; Pbma long-period approximant | moderate |
| Pb2WO5 intermediate | 11.88 | C2/m Pb2MoO5 analogue (COD 7220560), Mo replaced by W | moderate; analogue-derived atomic model |
| monoclinic Pb2O3-like phase | 8.15 | COD 2311012; P21/c | tentative |
| minium Pb3O4 | 3.21 | COD 1537983; P42/mbc | tentative minor phase |

## Evidence and refinement

The GSAS-II fit uses the complete 10.009–99.994° 2theta scan, the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 doublet ratio, and counting-statistical weights of `1/max(I,1)`. Refined unit cells, bounded atomic-coordinate adjustments, phase scales, phase-specific size/strain, selected March-Dollase terms, a smooth background, and the common instrumental profile are stored in `final.gpx`. The independently computed profile statistics are Rwp = 8.004%, Rp = 5.731%, Rexp = 3.502%, and goodness of fit = 2.290 (chi-square = 43270.1; 8282 points).

Scheelite PbWO4 accounts for the dominant 27–33° and corresponding high-angle reflection families. Monoclinic WO3 is required by its split low-angle 23–24° family and numerous higher-angle lines. The two PbO models are independently supported: massicot accounts for its orthorhombic 29–33° family, while the long-period alpha-PbO approximant supplies additional broadened/superstructure intensity that simple litharge does not. The C2/m Pb2WO5 model accounts for distinct intensity near 25.9°, 29–31°, 43°, and 47°. Pb2O3-like and Pb3O4 models account for weaker remaining peak families; omitting any of the first six phases raised Rwp to 10–36%, while omitting Pb3O4 raised it to about 8.46%. PbO2, Pb7W8O28.8, raspite/WO2-type alternatives, and tested Pb3WO6 analogues refined to negligible scale or gave inferior fits.

## Remaining uncertainty

The Pb2WO5 CIF is an analogue-derived Pb2MoO5 framework with Mo replaced by W because no direct Pb2WO5 reference was available; its phase family and approximate amount are supported, but its detailed oxygen coordinates are not uniquely determined. The monoclinic Pb2O3-like component required a comparatively large cell adjustment and strong anisotropic broadening, so the exact structure and its 8.1 wt.% fraction cannot be considered reliable independently of this model. Minor Pb3O4 (3.2 wt.%) is also strongly overlapped and model-dependent. Geometry screening flags short O-O contacts in the published Pb2O3 and Pb3O4 model families (about 1.72 and 1.80 A after refinement), reinforcing that those CIFs are tentative profile models rather than definitive local structures. The split between the two PbO forms and the Pb2WO5/Pb2O3-like components is correlated; realistic systematic fraction uncertainty is several percentage points for those phases and exceeds the least-squares standard errors. Structured residuals remain (Rwp well above Rexp), so these tentative assignments should not be treated as unique structure solutions.
