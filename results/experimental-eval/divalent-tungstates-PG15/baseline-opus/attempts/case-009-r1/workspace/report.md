# Phase analysis of `inputs/pattern.csv`

**Result: a single crystalline phase — MnWO₄ (hübnerite, wolframite type, monoclinic *P*2/*c*), 100 wt % of the modelled crystalline content.**

| quantity | value |
|---|---|
| Phase | MnWO₄, *P*2/*c* (No. 13), Z = 2 |
| CIF | `MnWO4.cif` |
| Weight fraction (normalised over modelled crystalline phases) | 1.000 |
| *a*, *b*, *c* | 4.83056(11), 5.75677(14), 4.99611(12) Å |
| *β* | 91.2172(10)° |
| *V* | 138.903(9) Å³ |
| R<sub>wp</sub> / R<sub>p</sub> | 4.94 % / 3.74 % |
| GOF (= √χ²<sub>red</sub>) | 1.43 |
| R<sub>wp</sub> (statistical minimum) | 3.46 % |
| R<sub>F</sub> / R<sub>F²</sub> (145 reflections) | 1.66 % / 3.30 % |
| N<sub>obs</sub> / N<sub>var</sub> | 8284 / 34 |

Project: `final.gpx` (GSAS-II 5.7.8). Profile: `fit.csv` (2θ, y_obs, y_calc, y_bkg, y_obs−y_calc), 10–100° 2θ.

## Evidence for the phase assignment

**Chemistry.** The precursors are Mn₃O₄ + WO₃ heated to 900 °C, so the accessible crystalline
products are MnWO₄, Mn₃WO₆, and unreacted/partly reduced binaries (WO₃, Mn₂O₃, Mn₃O₄, MnO).

**Search–match.** All 62 Mn–W–O entries in the local COD subset were simulated and ranked
against the extracted peak list (47 peaks above 0.8 % relative intensity, 2θ = 15.7–98.3°).
MnWO₄ (COD 1520200) was the only strong match: it accounted for 89 % of the simulated
intensity falling on observed peaks and 84 % of the observed intensity. The next-best
candidates scored below 0.55 and were accidental coincidences. Every observed peak above the
0.8 % threshold indexes on the MnWO₄ cell; the few that initially looked unassigned (64.08,
71.09, 73.22, 74.22, 77.50, 89.12°) are MnWO₄ reflections displaced by the sample-displacement
error (see below).

**Le Bail check.** A Le Bail fit with MnWO₄ alone reached R<sub>wp</sub> = 5.77 % against a
statistical floor of 3.46 %. The difference curve over the whole 10–100° range contains no
positive feature at any reflection position of WO₃, Mn₂O₃, Mn₃O₄, MnO or Mn₃WO₆ — the regions
that are free of MnWO₄ peaks (26–27.5°, 32.5–35°, 37.8–39°, 58–59.5°) are pure counting noise.

**Rietveld.** The full Rietveld refinement converges at R<sub>wp</sub> = 4.94 %, GOF = 1.43,
R<sub>F</sub> = 1.66 %. The refined oxygen positions, O1 (0.2148, 0.0974, 0.9476) and
O2 (0.2513, 0.3689, 0.3948), reproduce the published hübnerite values (≈ 0.211, 0.102, 0.946 and
0.252, 0.375, 0.393) to within 0.004 in fractional coordinates, which is an independent
confirmation that the structural model — not just the cell — is correct.

## How the model was built

1. **Instrument/sample corrections.** Peak positions are shifted by ≈ +0.25° cos θ relative to
   literature MnWO₄. This is a specimen-displacement error; it refines to −425 µm on the quoted
   200 mm goniometer radius. Zero-point and displacement are 99.99 % correlated, so the zero was
   held at 0 and only the displacement refined.
2. **Peak shape.** Direct Rietveld refinement from default profile values fell into a local
   minimum with far-too-broad peaks (R<sub>wp</sub> ≈ 10 %). The profile was therefore first
   determined by Le Bail refinement and then transferred to the Rietveld model, which removed
   the problem entirely.
3. **Surface roughness.** This was the decisive correction. Without it the refinement drove all
   displacement parameters negative (U<sub>iso</sub> ≈ −0.018 Å²) and distorted the oxygen
   positions, because the observed low-angle intensities are suppressed relative to the
   high-angle ones. Adding the Suortti roughness model (A = 0.135, B = 0.369) dropped
   R<sub>wp</sub> from 9.7 % to 5.4 % and restored both physical ADPs and literature-consistent
   oxygen coordinates. MnWO₄ is strongly absorbing for Cu Kα, so a roughness effect of this size
   on a packed powder is expected.
4. **Preferred orientation** was tested (March–Dollase along [010], the wolframite cleavage
   direction). It improved R<sub>wp</sub> by only 0.02 % absolute and was not retained.

## Uncertainty and what cannot be determined reliably

- **Weight fraction.** With a single detected phase the normalised fraction is 1.000 by
  construction; it carries no refinement uncertainty. The meaningful statement is the detection
  limit, below.
- **Detection limit for minor phases (≈ 1 wt %).** Each candidate impurity was added to the
  converged model and its scale alone refined: WO₃ 0.29 wt % (ΔR<sub>wp</sub> −0.004), Mn₂O₃
  0.65 wt % (−0.009), Mn₃O₄ 0.27 wt % (−0.001), MnO 0.24 wt % (−0.002), Mn₃WO₆ 0.00 wt % (0.000).
  None of these improvements is meaningful — they absorb residual profile misfit rather than
  real peaks — so **no second phase can be claimed**. An amorphous or poorly crystalline
  fraction cannot be quantified at all from this data set, since no internal standard was
  measured; the reported fraction refers only to the crystalline, modelled content.
- **Lattice parameters.** The quoted e.s.d.s (~0.0001 Å) are statistical only. Because the cell
  correlates with the large specimen displacement, the realistic accuracy is nearer ±0.002 Å; the
  refined cell is ~0.15 % larger than the literature hübnerite cell, which is within that
  systematic margin and should not be read as a composition effect.
- **Displacement parameters are not determined.** All U<sub>iso</sub> values were held fixed
  (W 0.004, Mn 0.006, O 0.010 Å²). When refined, W and Mn go to ≈ 0 or slightly negative because
  they are strongly correlated with the roughness correction, for a gain of only 0.016 % in
  R<sub>wp</sub>. The fixed-ADP model is reported instead; the CIF should not be used as a source
  of thermal parameters.
- **Oxygen coordinates** are refined but weakly determined: with Cu Kα radiation, W (Z = 74)
  dominates the scattering, so the O e.s.d.s (~0.001 in fractional coordinates, i.e. ~0.005 Å)
  are optimistic and the real accuracy is a few hundredths of an Å.
- **Site occupancies were not refined.** Stoichiometric MnWO₄ was assumed. Lab PXRD with a
  dominant W scatterer cannot usefully distinguish small Mn/W non-stoichiometry or Mn vacancies,
  and the Mn₃O₄ precursor could in principle leave slight Mn excess.
- **Residual misfit.** The remaining structure in the difference curve is confined to the
  low-2θ flanks of the five strongest reflections (18.4, 23.6, 29.9, 30.6°) and is an incompletely
  modelled axial-divergence asymmetry/peak-shape effect, not an unindexed phase. The
  Durbin–Watson statistic of 1.01 reflects this residual serial correlation, so the quoted
  e.s.d.s are underestimated by roughly a factor of √2.
- **Instrument profile caveat.** No calibrated instrument profile was supplied, so the profile
  terms are purely empirical. The refined Lorentzian term Y is negative, meaning the Lorentzian
  width is clamped to zero above ~57° 2θ and the high-angle peaks are modelled as essentially
  Gaussian. This describes the data well but should not be interpreted as microstructural
  information (crystallite size / microstrain were therefore not extracted).

## Files

| file | content |
|---|---|
| `MnWO4.cif` | refined MnWO₄ structure |
| `fit.csv` | 2θ, y_obs, y_calc, y_bkg, y_diff over 10–100° |
| `result.json` | phase list, weight fraction, cell, fit statistics, minor-phase screening |
| `final.gpx` | GSAS-II project that produced all of the above |
