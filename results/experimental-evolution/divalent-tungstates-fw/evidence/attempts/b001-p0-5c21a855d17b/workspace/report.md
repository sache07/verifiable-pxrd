# Powder XRD phase analysis

## Result

Four crystalline phases were required. Weight fractions are normalized over the modeled crystalline material; they do not measure any amorphous fraction.

| Phase | wt% | formal 1σ (wt%) | Space group | Structural model |
|---|---:|---:|---|---|
| CaWO4 (scheelite) | 63.53 | 0.09 | I 41/a | phase_CaWO4_scheelite.cif |
| WO3 (monoclinic) | 27.14 | 0.06 | P 21/c | phase_WO3_monoclinic.cif |
| CaCO3 (calcite) | 6.48 | 0.10 | R -3 c | phase_CaCO3_calcite.cif |
| CaO (rocksalt) | 2.85 | 0.05 | F m -3 m | phase_CaO_rocksalt.cif |

The independently regenerated GSAS-II profile gives **Rwp = 3.125%**, **Rp = 2.422%**, and goodness of fit **1.128** over all 8301 measured points. The difference column in `fit.csv` is observed minus calculated.

## Evidence

The precursor chemistry and 650 °C treatment support partial formation of scheelite CaWO4 with residual WO3 and Ca-bearing precursor/decomposition products. The whole-pattern assignments are anchored by the CaWO4 reflections near 18.7° and 28.8° 2θ, the characteristic monoclinic WO3 multiplet from about 23.2–24.5°, the calcite line near 29.5°, and the CaO series near 32.3°, 37.4°, 53.9°, and 91.4°. Candidate monoclinic, triclinic, and orthorhombic WO3 reference structures were screened; the COD 2311041 monoclinic model gave the best stable whole-pattern refinement.

Phase-deletion controls increased Rwp from 3.125% to 49.68% without CaWO4, 25.05% without WO3, 4.55% without calcite, and 4.60% without CaO. Thus even the two minor phases are supported by reproducible multi-line residuals, not solely by a single overlapped peak.

The Rietveld model uses the supplied Cu Kα doublet, refined unit cells, phase scales, isotropic size broadening, microstrain (uniaxial for WO3), a modest [111] March–Dollase correction for WO3, specimen displacement, polarization, and a smooth Chebyshev background. Atomic coordinates were allowed only small symmetry-preserving departures from the published reference structures.

## Remaining uncertainty

The tabulated 1σ values are conditional least-squares errors and are smaller than the likely systematic uncertainty from peak overlap, absorption, preferred orientation, and model choice. In particular, the 2.85 wt% CaO fraction and the exact oxygen coordinates in low-symmetry WO3 are less secure than the phase identities. Thermal displacement and polarization terms are strongly correlated, so their individual values should not be interpreted independently. No crystalline phase is left unidentified in the fitted pattern, but trace phases below the detection limit and amorphous material cannot be excluded; consequently, absolute bulk phase fractions cannot be determined reliably without an internal standard. The submitted fractions are reliable as normalized crystalline-phase estimates, with the minor-phase values carrying the greatest practical uncertainty.
