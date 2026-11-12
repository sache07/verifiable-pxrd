# PXRD phase analysis

The modeled crystalline fraction contains **55.3 wt% witherite BaCO3** and **44.7 wt% monoclinic WO3**, normalized to the two modeled crystalline phases. The corresponding refined structures are in `phase_BaCO3.cif` and `phase_WO3.cif`; the exact final refinement is saved as `final.gpx`.

## Evidence and model

The four-feature group at 23.4–24.7 degrees requires both phases: the monoclinic WO3 triplet accounts for peaks near 23.43, 23.91, and 24.65 degrees, while the strong BaCO3 reflections account for the 24.21-degree peak and overlap the high-angle side of the group. Independent BaCO3 peaks near 19.78, 28.03, 39.79, 43.26, and 45.17 degrees and the WO3 multiplets around 33–35, 42, and 50 degrees support the assignments throughout the measured range.

Starting structures were COD 9010928 (witherite) and COD 2311041 (room-temperature monoclinic WO3). Refined cells are:

- BaCO3, Pmcn (No. 62): a = 5.31088 A, b = 8.92033 A, c = 6.43680 A.
- WO3, P21/n (No. 14): a = 7.31154 A, b = 7.54183 A, c = 7.69816 A, beta = 90.7524 degrees.

The refinement used the reported Cu K-alpha doublet and intensity ratio, a 15-term smooth background, phase scales and cells, a zero offset, profile coefficients, and a small [001] March-Dollase correction for BaCO3 (1.065). Atomic coordinates and displacement parameters were held at the reference-model values because this broad, overlapping two-phase pattern does not determine them reliably. The refined zero offset is +0.3126 degrees; because no calibrated instrument profile was supplied, it should not be interpreted as a sample property.

The final fit has Rwp = 7.13%, Rp = 5.41%, and goodness of fit = 2.05. `fit.csv` contains the observed, calculated, observed-minus-calculated, and background profiles from this exact saved project.

## Remaining uncertainty

BaWO4 was explicitly tested because it is the expected reaction product. Its strongest candidate contribution overlaps a WO3 reflection, while isolated BaWO4 reflections expected near 17.6 and 32.2 degrees are not compelling. Trial three-phase refinements returned only about 0.4–0.9 wt% BaWO4 and the value was unstable against the peak-broadening model, so neither its presence nor fraction can be determined reliably; it is excluded from the reported phase set. A high-temperature orthorhombic WO3 model fit substantially worse. A triclinic model gave a small numerical improvement but refined toward nearly monoclinic metrics, so the chemically appropriate monoclinic model was retained.

No pointwise uncertainties were supplied. Poisson counting weights were therefore used; the formal fraction standard uncertainty is only 0.12 wt% for each phase and is optimistic. Profile/background/model variations shift the fractions by roughly 1–1.5 wt%, which is the more realistic absolute uncertainty. Any amorphous content is unconstrained by this normalization.
