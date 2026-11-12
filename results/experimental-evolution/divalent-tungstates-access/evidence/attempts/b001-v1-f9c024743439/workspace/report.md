# Powder XRD phase analysis

The accepted crystalline model contains **scheelite CaWO4 (84.99 wt%)** and **monoclinic WO3 (15.01 wt%)**, normalized over the modeled crystalline phases. The final replayed fit has Rwp = 4.031%, Rp = 3.073%, and Rexp = 3.138% for 8301 points.

## Evidence

The dominant broad family (including the strong features near 18.27, 28.42, 33.85, 38.91, 46.88, 54.16 and 57.65 degrees 2theta) is indexed by I41/a scheelite CaWO4. The narrower family near 22.76, 23.18, 23.98, 26.19, 28.77, 32.9–33.2 and 49.47 degrees is accounted for by P21/c WO3. The CaWO4 structure is physically conventional after refinement (W–O 1.797 A; Ca–O 2.413–2.455 A). The WO3 model retains distorted WO6 octahedra with W–O 1.735–2.152 A; all occupancies are 1 and no short-contact or negative-ADP issue was found.

All available same-formula CaWO4 and WO3 entries were enumerated before nomination. Under the same stable nuisance model, the shortlisted WO3 alternatives gave Rwp 4.518% (P-1, COD 2106293), 4.681% (alternative P21/c, COD 1528915), and 7.267% (Pnma, COD 2107312), versus 4.064% for COD 2311041 before its limited W-coordinate stage. The P21/m and small-cell P21/c trials failed to produce valid replayable refinements and remain unknown rather than rejected. The complete screen is in `analysis/candidate_screen.csv`, with the branch decisions in `analysis/candidate_ledger.json`.

Phase-closure trials covered calcite/aragonite/vaterite CaCO3, CaO, Ca3WO6, Ca4.26W10O30 and the high-pressure CaWO4 polymorph. Their scales collapsed or their gain was unsupported. Calcite gave only a 0.0047 percentage-point Rwp decrease with a fixed profile; attempting to broaden it drove size to the 0.04 um boundary and worsened the replay, so it was omitted. The remaining positive residuals are concentrated on flanks of existing CaWO4/WO3 peaks, not a separate coherent peak family. Trace material below roughly 0.5–1 wt% cannot be excluded.

## Refinement and uncertainty

The refinement was staged through scale/background, displacement and cells, isotropic instrument/phase profiles, then limited symmetry-allowed coordinates. One-at-a-time uniaxial-strain and March–Dollase trials were unsupported (largest Rwp gain 0.0044 percentage points); roughness was singular and boundary-hitting, so all were rolled back. Exported CIF geometry was screened after replay.

The CaWO4 coherent-domain size is only a lower-limit estimate: the diagnostic optimum was 0.0392 um, just below the allowed 0.04 um range, so 0.04 um was fixed. This peak-width limit and correlations with background/profile terms make the formal fraction errors optimistic; a practical uncertainty is about ±1.5 wt% absolute for each phase. CaWO4 oxygen and WO3 tungsten coordinates are supported by limited refinement, while WO3 oxygen coordinates were unstable and were retained from the nominated reference. Thus the phase identities and approximate fractions are reliable, but crystallite size and fine WO3 oxygen geometry are not determined reliably from this pattern alone.
