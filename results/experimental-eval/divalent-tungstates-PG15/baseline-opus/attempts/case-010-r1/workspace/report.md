# Phase analysis of `inputs/pattern.csv` (Mn2O3 + WO3, 500 °C)

## Summary

Three crystalline phases were identified and refined by the Rietveld method in GSAS-II.
The sample is essentially an **unreacted mixture of the two precursors** with a trace of the
target tungstate:

| Phase | Formula | Space group | Weight fraction* | CIF |
|---|---|---|---|---|
| γ-WO3, monoclinic tungsten trioxide | WO3 | P2₁/n (14) | **73.8 % ± 0.2 %** | `WO3.cif` |
| α-Mn2O3, bixbyite | Mn2O3 | Ia-3 (206) | **25.4 % ± 0.2 %** | `Mn2O3.cif` |
| MnWO4, wolframite-type (hübnerite) | MnWO4 | P2/c (13) | **0.74 % ± 0.09 %** | `MnWO4.cif` |

\* normalised over the three modelled crystalline phases. The quoted ± values are the
least-squares esds; the *realistic* uncertainties are several times larger (see
"Remaining uncertainty").

Fit statistics (whole pattern, 9.90–100.09° 2θ, 8301 points, 39 refined variables):
**Rwp = 6.66 %, Rp = 4.81 %, Rexp = 2.66 %, GOF = 2.51**; per-phase
R_F = 2.19 % (WO3), 1.97 % (Mn2O3), 4.46 % (MnWO4).
Observed/calculated/difference profile: `fit.csv`. GSAS-II project: `final.gpx`.

**Chemical consistency.** The refined fractions correspond to an overall **Mn : W = 1.01 : 1**
atomic ratio (Mn2O3 : WO3 = 1 : 1.98 molar). This is exactly the stoichiometry of a 1:1
Mn:W charge intended to make MnWO4, so the quantification is self-consistent with the
stated precursors. Only ~0.8 mol % of the available W has been converted to MnWO4 —
at 500 °C the solid-state reaction has barely started.

## Evidence

**Candidate generation.** The local COD subset (62 098 CIFs) was screened for every entry
whose formula contains only Mn, W and/or O (73 hits: WO3 polymorphs, sub-stoichiometric
tungsten oxides, MnO/MnO2/Mn2O3/Mn3O4/Mn5O8, MnWO4, Mn3WO6, metals). Each was simulated
and cross-correlated with the background-stripped data over a ±0.6° 2θ shift window.

**γ-WO3 (dominant).** The three strongest reflections of the pattern form the classic
monoclinic WO3 triplet — d = 3.793 / 3.719 / 3.604 Å (002/020/200) — and the best-matching
candidate by a wide margin was COD 1528915, P2₁/n WO3 (match 0.80 vs 0.42 for the next
non-WO3 candidate). The refined cell, a = 7.3074, b = 7.5397, c = 7.6957 Å, β = 90.683°,
V = 423.97 Å3, agrees with literature γ-WO3 (7.3008/7.5389/7.6896 Å, β = 90.89°) to within
0.1 % in the axial lengths. R_F = 2.2 % on 440 reflections.

**α-Mn2O3 bixbyite.** After WO3 alone the largest residual peak (23 % of the strongest
observed peak) sat at d = 2.692 Å, with companions at 2.352, 1.656 and 1.414 Å. Corrected
for the refined specimen displacement these index as the 222/400/440/622 reflections of a
body-centred cubic cell with **a = 9.4166 Å**, i.e. bixbyite Mn2O3 (literature a = 9.4146 Å)
— the expected precursor. Refinement gives R_F = 2.0 % on 74 reflections. Adding it drops
Rwp from ~25 % to ~7 %. The cubic Ia-3 model is sufficient; no peak splitting indicating
the orthorhombic (Pbca) bixbyite distortion is resolvable here.

**MnWO4 (trace, but real).** After the two-phase fit a weak, isolated residual peak remained
at 18.71° 2θ, which is not indexable on either WO3 or Mn2O3 but is exactly the MnWO4 (100)
reflection. Consistent residual excesses also remain at 30.15/30.58° (the MnWO4 1-11/111
doublet, its two strongest lines), 36.27° (021) and 48.50° (022). Including wolframite-type
MnWO4 reduces Rwp by 0.13–0.25 percentage points and returns a phase fraction at 8–13 σ.
As a control, the same test with phases that are *not* present (Mn3O4, β-MnO2, Mn3WO6)
gave ~half the Rwp improvement, fractions of ≤0.7 % at ≤3 σ, and, for Mn3WO6, a fraction
indistinguishable from zero. Letting the MnWO4 cell refine freely from the ambient
literature values returns a = 4.809, b = 5.764, c = 4.991 Å, β = 91.07°, i.e. it stays at
hübnerite values rather than wandering — a further (if weak) consistency check.

**Phases excluded.** No evidence was found for Mn3O4 (hausmannite), MnO, MnO2 polymorphs,
Mn5O8, Mn3WO6, hexagonal WO3, WO2, or the reduced tungsten oxides W18O49/W17O47/W3O8: in
each case the characteristic strong reflections are absent from the data and from the
two/three-phase residual, and trial refinement returns insignificant or zero fractions.

## Model details

* Background: 16-term Chebyshev polynomial (1st kind), refined.
* Peak positions: specimen-displacement correction only (Zero fixed at 0). The refined
  displacement, −619 μm, is large but it is what brings all three phases simultaneously
  onto literature cell parameters; a pure zero-point offset of ≈ +0.30° gives an equally
  good profile fit but forces all cells ~1 % too small, so displacement is the physically
  correct interpretation.
* Peak shape: pseudo-Voigt with Gaussian U = V = 0 (fixed) and W = 13.78; Lorentzian
  X = 7.32, Y = 12.13; axial-divergence asymmetry SH/L = 0.040. The peaks here are narrow
  (FWHM 0.13–0.29°) and predominantly Lorentzian; an unrestricted Caglioti refinement runs
  into unphysical negative U and W, so the Gaussian part was restricted to its constant
  term. The broadening is not deconvolved into instrument and sample components (no
  calibration standard was supplied); taken at face value it corresponds to ~110 nm
  apparent domain size and ~5 × 10⁻⁴ microstrain, i.e. well-crystallised powders.
* Cu Kα1/Kα2 doublet with I(α2)/I(α1) = 0.5, as given in the metadata. The doublet is
  resolved in the data (e.g. the 83.64/83.90° pair, Δ = 0.26°, matches the predicted
  0.255° splitting), confirming that a two-wavelength model is required.
* Polarisation was not supplied; 0.7 was used (0.5 was tested and gave a slightly worse
  fit, Rwp 6.97 vs 6.87 in a comparison run).
* Structural parameters: cell parameters of WO3 and Mn2O3 and the W1/W2 (WO3) and
  Mn2/O1 (Mn2O3) coordinates were refined. The WO3 oxygen coordinates and all Uiso values
  were held fixed (W 0.006, Mn 0.008, O 0.010 Å2) — see below. For MnWO4 only the scale
  factor was refined, with cell and coordinates fixed at literature hübnerite values.
* Preferred orientation was tested (March-Dollase along [100], [010], [001]) and is
  negligible (r = 0.97–1.01); it is not included in the final model.

## Remaining uncertainty

* **Weight fractions.** Across the model variants explored (background 12 vs 16 terms,
  old vs modern WO3 starting structure, free vs fixed oxygen positions, with and without
  preferred orientation, MnWO4 cell free or fixed) the fractions spanned
  WO3 73.8–76.4 %, Mn2O3 23.5–25.5 %, MnWO4 0.7–1.3 %. **Those ranges, not the esds, are
  the honest uncertainty.** I would quote WO3 ≈ 75 ± 1.5 %, Mn2O3 ≈ 24.5 ± 1.5 %,
  MnWO4 ≈ 1.0 ± 0.4 %. No microabsorption (Brindley) correction was applied; with the
  strongly contrasting absorption of WO3 and Mn2O3 this can bias the WO3:Mn2O3 split by a
  few percent in either direction.
* **The MnWO4 fraction is at the quantification limit.** Its presence is well supported
  (unique 18.71° line plus three further matching residual features, 8–13 σ), but a value
  of 0.7 % vs 1.3 % cannot be distinguished by these data. Its structure is *not*
  determined here — it is adopted from the literature and only scaled.
* **WO3 structure.** The oxygen positions of γ-WO3 are not determined by this measurement:
  released, they drift to chemically implausible values and the refined Uiso go negative,
  which is overfitting of residual profile/intensity systematics by a weakly scattering
  sublattice. They are therefore fixed at published values, and only the W positions
  (which barely move, ≤0.004 fractional) were refined. The CIF should be read as
  "literature γ-WO3 with a refined cell", not as an independent structure determination.
* **The refined β = 90.683° for WO3 is ~0.21° below the accepted 90.89°.** The axial
  lengths and volume are in excellent agreement, so this is unlikely to be a different
  polymorph; it more plausibly reflects a correlation between β, the large specimen
  displacement and the peak-shape model, or genuine strain in this powder. Treat β as the
  least reliable of the refined lattice parameters.
* **Residual misfit.** Durbin–Watson = 0.36 and GOF = 2.5 show significant serial
  correlation in the residuals: the remaining misfit (up to ~12 % of the strongest peak,
  concentrated on the strong WO3 lines at 33.6/34.1/34.5° and 23–25°) is systematic peak
  shape/intensity error of the WO3 phase, not a missing phase — every residual feature
  above ~2 % of the maximum coincides with an already-indexed reflection. Anisotropic
  microstrain broadening was tried and made the refinement unstable without improving the
  fit, so it was not retained. An amorphous component, if present, cannot be quantified
  because no internal standard was measured; all fractions are normalised over the
  crystalline phases only.

## Files

| File | Contents |
|---|---|
| `WO3.cif`, `Mn2O3.cif`, `MnWO4.cif` | refined structural model for each phase |
| `fit.csv` | 2θ, y_obs, y_calc, y_diff, y_background |
| `result.json` | phases, CIF paths, normalised weight fractions, fit statistics |
| `final.gpx` | GSAS-II project that produced all of the above |
| `scripts/` | analysis and refinement scripts (`pipeline5.py` builds the final model, `export.py` writes the deliverables) |
