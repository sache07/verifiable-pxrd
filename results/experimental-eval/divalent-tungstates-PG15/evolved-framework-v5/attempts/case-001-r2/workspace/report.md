# Powder XRD phase analysis

The pattern is described by two crystalline phases: orthorhombic witherite-type BaCO3 and monoclinic WO3. This is chemically consistent with the BaCO3 + WO3 precursor mixture after the reported 400 °C treatment. The accepted structures were initialized from COD 9010928 (BaCO3) and COD 2311041 (WO3), then refined in GSAS-II against all 8,301 measured points using the reported Cu Kalpha1/Kalpha2 wavelengths and intensity ratio.

The refined crystalline-phase fractions are 0.5472 BaCO3 and 0.4528 WO3 by weight (54.72 and 45.28 wt%, normalized to the modeled crystalline material). GSAS-II's counting-statistical standard uncertainty is 0.00138 for each fraction, but a more realistic uncertainty is about 1–2 wt% because displacement parameters, preferred orientation, surface roughness, and peak broadening are correlated with phase scale. No amorphous fraction can be obtained without an internal standard.

The final cells are:

- BaCO3, Pmcn (Pnma-equivalent): a = 5.308760, b = 8.915854, c = 6.433585 Å.
- WO3, P21/c in the submitted nonstandard setting: a = 7.693561, b = 7.538345, c = 10.541209 Å, beta = 136.11168°.

All strong and coherent reflection families are indexed by these two phases. The largest residual features occur at modeled peaks or overlapping peak shoulders, indicating remaining line-shape/intensity mismatch rather than a repeatable third-phase d-spacing family. A physically constrained BaWO4 trial refined to only about 0.4 wt% and reduced Rwp by roughly 0.04 percentage point without broad unique-family support. Allowing it unrestricted profile freedom produced nonphysical nanometre-scale size and extreme microstrain, so BaWO4 was rejected; an unquantified trace amount cannot be excluded. A triclinic WO3 reference gave only a small Rwp gain while its metric collapsed toward monoclinic symmetry, so the lower-parameter physical P21/c model was retained.

The final full-grid fit has Rwp = 5.8159%, Rp = 4.4184%, and GOF = 1.6741 (Rwp,min = 3.4807%). An independent replay of `final.gpx` converged with no singular values and maximum shift/esd = 0.024. The WO3 W–O coordination is physically credible (six W–O distances per W, about 1.74–2.19 Å). Light-atom positions are less certain: WO3 oxygen coordinates and the BaCO3 carbonate group were retained near their reference values after free/bounded light-atom refinements became unstable or hit bounds. In particular, the BaCO3 reference has one elongated apparent C–O distance (~1.407 Å), so its detailed carbonate geometry should not be interpreted as independently determined by this powder pattern.
