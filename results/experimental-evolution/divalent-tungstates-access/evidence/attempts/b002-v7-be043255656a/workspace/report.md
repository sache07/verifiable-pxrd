# Powder X-ray diffraction phase analysis

The specimen was modeled as five crystalline Mn-W-O phases. Weight fractions are normalized only over those modeled crystalline phases:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| MnWO4 (wolframite) | P 2/c | 64.29% |
| WO3 | P 21/c | 24.68% |
| MnO, cubic | F m -3 m | 1.63% |
| MnO, hexagonal | P 63 m c | 3.50% |
| Mn2WO6 | P b c n | 5.90% |

## Evidence and model selection

The data are an unsmoothed reflection scan collected with Cu K-alpha radiation from a WO3/Mn3O4 mixture heated at 800 degrees C. Ordinary reference models account for the principal wolframite MnWO4 and residual monoclinic WO3 families. Two smaller, distinct MnO reflection families require rock-salt cubic and wurtzite-like hexagonal models; both retain positive scales across their families. In a controlled pre-polish remove test, deleting cubic MnO worsened Rwp from 15.736% to 15.827%, supporting retention despite its small abundance.

One coherent family remained after fitting the common phases. Composition-balanced, symmetry-diverse substituted parents were converted identically to Mn2WO6 and compared at equally developed checkpoints. An ordered Pbcn topology gave the best physical basin; alternative polar standard-setting and disordered small-cell models fit less well, while an apparently better nonstandard polar trial was rejected because its multiplicities produced Mn2WO3 and 0.81 A cation contacts. The accepted Pbcn model has Mn-O distances of about 1.95-2.26 A, W-O distances of about 1.94-2.07 A, and a minimum O-O distance of 2.57 A. No coherent unassigned Bragg family remained after this phase was included.

The final bounded polish was run once and selected a converged physical branch with no frozen variables. A replay over all 8,301 measured points gives Rwp = 15.58385%, Rp = 9.60474%, goodness of fit = 7.8321, and maximum shift/esd = 0.409. The refined zero shift is -0.06512 degrees. `fit.csv`, all CIFs, and the fractions above were exported from the byte-identical accepted `final.gpx`/`polished.gpx` model.

## Remaining uncertainty

MnWO4 and WO3 identities are strong, but the detailed WO3 oxygen geometry is not fully reliable: the exported model contains a 1.576 A O-O contact. The starting published WO3 reference contains the same 1.575 A feature, so it is not a polish-induced collapse, but it still requires crystallographic adjudication and should not be treated as a precise oxygen substructure.

The 1.63% cubic MnO contribution is near the practical minor-phase limit and its fraction is correspondingly uncertain. The Mn2WO6 family is supported by multiple reflections and physical geometry, but no exact-composition reference was available; its CIF is an analogue-derived ordered topology, and the individual coordinates and 5.90% fraction are lower-confidence than the MnWO4/WO3 results. The relatively high goodness of fit and remaining peak-shape residuals also make all reported fractions semi-quantitative. No amorphous content was measured, and the absence of supplied pointwise uncertainties prevents defensible standard uncertainties for the fractions.
