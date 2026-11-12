# Powder XRD phase analysis

The pattern is best described by six crystalline Pb–W–O phases. Fractions below are normalized over those modeled crystalline phases; an amorphous fraction was not measured.

| Phase | Space group | wt.% | Principal profile evidence |
|---|---:|---:|---|
| PbWO4, scheelite | I41/a | 53.25 | Dominant 112, 204 and 224 peaks near 27.68, 45.00 and 56.80° 2θ |
| PbO, massicot | Pbcm | 5.87 | Independent peaks near 29.4, 30.6, 37.9 and 46.4° |
| WO3, monoclinic | P21/n | 10.73 | Characteristic 23.4–24.7° triplet and 040 peak near 48.5° |
| PbO, long-cell orthorhombic | Pbma | 7.05 | Peaks near 28.87, 32.04/32.11, 36.0, 48.9 and 54.8° |
| Pb2WO5 | C2/m | 13.66 | Distinct 002 and 020 peaks near 26.76 and 31.03°, plus the 43–57° series |
| Pb3WO6 | P21/m | 9.45 | Independent peaks near 27.48, 30.17/30.25 and 44.0°; its inclusion removes a coherent residual series |

The common phases were initialized from COD 9009811 (PbWO4), 2310433 (massicot), 1528915 (WO3), and 1533609 (long-cell PbO). No exact database models were available for the two intermediate lead tungstates: Pb2WO5 was adapted by Mo→W substitution from Pb2MoO5 (COD 7220560), and Pb3WO6 by S→W substitution from Pb3SO6 (COD 8103588). Their cells, symmetry-allowed coordinates, phase scales, bounded crystallite-size/microstrain terms, and supported March–Dollase terms were refined. Element-wise coordinate shifts and isotropic displacement parameters were kept within physically sensible bounds.

Fresh native GSAS-II replay of `final.gpx` gives Rwp = 8.319%, Rp = 6.012%, Rexp = 3.497%, and goodness of fit = 2.379 for 8,282 points. `fit.csv` is this replayed atomic profile, not a cached curve.

## Uncertainty

The inventory and dominant PbWO4 abundance are well supported. Fractions of the common minor phases are likely uncertain by roughly 1–2 wt.% absolute. Pb2WO5 and especially Pb3WO6 carry larger model-dependent uncertainty (about 2–3 wt.% absolute): their framework assignments are supported by multiple peaks, but their detailed oxygen coordinates and refined fractions are correlated with Uiso, texture, and overlapping Pb-rich reflections. Isostructural or closely related off-stoichiometric Pb–W–O variants cannot be excluded from powder data alone.

The historical monoclinic WO3 model retains a short symmetry-generated O···O contact of about 1.60 Å, so its oxygen sublattice should be treated as approximate even though the W lattice and phase identification are secure. Systematic residuals remain around 26–32° and 46–49°; consequently neither the analogue-derived atomic details nor their fractions should be interpreted as uniquely determined. No amorphous content or unmodeled trace phase is included in the reported normalization.
