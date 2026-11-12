# Powder XRD phase analysis

The scan is best described by three crystalline phases: **monoclinic WO3
(72.21 wt%)**, **alpha-Mn2O3 (27.07 wt%)**, and trace
**wolframite MnWO4 (0.72 wt%)**. Fractions are normalized over the
modeled crystalline phases. The covariance-only standard uncertainties are
0.18, 0.17, and 0.07 percentage points, respectively;
they do not include model or reference-structure uncertainty.

## Evidence

The metadata gives Mn2O3 and WO3 precursors heated at 500 C and a Cu K-alpha
reflection scan. Monoclinic WO3 accounts for the dominant 23.4--24.7 degree
triplet and its high-angle families. Alpha-Mn2O3 accounts for the coherent
families near 33.27, 38.53, 45.03, 49.6, 55.0, and 66.0 degrees. A physical
monoclinic WO3 model (COD 2311041) was preferred over a marginally closer
legacy intensity model that produced an implausibly short O--O contact.

After both precursor phases were complete, weak residuals at the wolframite
positions (especially the 30.1/30.6 degree pair and the 36.3, 51.5, and 60.9
degree families) gave a positive MnWO4 scale. It remained approximately
0.5--0.8 wt% over tested cell and peak-width checkpoints. The submitted
MnWO4 model uses the COD 1520200 wolframite topology with a bounded
ambient-cell checkpoint. Mn3WO6 was also tested, but its very small apparent
scale was driven by mixed peak overlaps rather than broad family support and
was not retained.

## Refinement and uncertainty

The final GSAS-II fit used the stated Cu K-alpha doublet, a Chebyshev
background, calibrated zero/sample displacement, physical size and strain
broadening, and bounded surface/profile terms. Heavy WO3 coordinates and two
small bounded oxygen-coordinate starts were checked; the 0.05-A start retained
physical W--O and O--O distances. The full-grid fit gives
Rwp = 6.113%, Rp = 4.475%, and
GOF = 2.298.

Because pointwise uncertainties were not supplied, Poisson count weights were
used. The largest remaining residuals track relative-intensity/split-profile
errors of WO3 rather than a new coherent reflection family. A realistic
systematic uncertainty is therefore larger than the covariance values: about
1--2 percentage points for the two major fractions and roughly 0.2--0.3
percentage point for trace MnWO4. The MnWO4 topology is supported, but its
atomic coordinates and exact cell cannot be independently refined reliably at
this abundance; its structure and fraction should be treated as approximate.
