# Phase analysis of `inputs/pattern.csv` (BaCO₃ + WO₃, 400 °C)

## Result

| phase | formula | space group (setting) | *Z* | weight fraction | *R*F² |
|---|---|---|---|---|---|
| witherite | BaCO₃ | *Pmcn* (No. 62, *Pnma* setting) | 4 | **0.503 ± 0.002**(stat) | 6.3 % |
| γ-WO₃ | WO₃ | *P*2₁/*n* (No. 14) | 8 | **0.497 ± 0.002**(stat) | 7.2 % |

Two crystalline phases, normalised over the two modelled phases (no other phase
was modelled and no internal standard is present, so these are
crystalline-only fractions).

Whole-pattern fit (GSAS-II, 9.90–100.09° 2θ, 8301 points, 38 refined
parameters): **R_wp = 7.30 %, R_p = 5.63 %, R_exp = 3.47 %, χ²_red = 4.41,
GOF = 2.10**. Background-subtracted equivalents: R′_wp = 13.7 %, R′_p = 13.0 %.

Files: `BaCO3.cif`, `WO3.cif`, `fit.csv` (2θ, y_obs, y_calc, y_diff,
y_background), `result.json`, `final.gpx`, `fit_overview.png`.

**Chemical reading of the result.** The molar ratio implied by the weight
fractions is BaCO₃ : WO₃ = 1.19 : 1. No barium tungstate or any other ternary
Ba–W–O phase is present: at 400 °C the mixture has not reacted. The "product"
is the unreacted precursor blend, slightly Ba-rich relative to 1 : 1.

## Evidence for the phase identification

Peak search on the raw pattern gives ~95 resolvable maxima above 2 % of the
strongest peak (ignoring the noise-dominated 9.9–11.6° region, where the only
feature is the steep air-scatter background). Every one of them is indexed by
witherite BaCO₃ or monoclinic γ-WO₃ once a +0.3° 2θ offset is allowed (see
below); for example

* 19.78, 20.23, 24.22, 28.03, 34.89, 39.79, 43.25, 44.54, 45.17, 47.08° → BaCO₃
  (110), (020), (111), (002), (130), (220), (041), (202), (132), (113);
* 23.43, 23.91, 24.65, 26.91, 28.97, 33.57, 48.53, 50.22° → WO₃ (002), (020),
  (200), (120), (112̄), (022), (040), (400).

The two phases together generate 621 reflections in range (181 + 440); the
final difference curve shows no unindexed maximum anywhere
(`fit_overview.png`). Both precursors are therefore still present and the
number of phases is 2.

Starting models were taken from the local COD subset:

* **BaCO₃** – COD 9010928 (Antao & Hassan 2007, witherite at 25 °C). The C
  position in that entry gives C–O = 1.275/1.275/1.406 Å, i.e. a
  non-equilateral carbonate; it was reset to the centroid of its three O
  neighbours before use (C–O = 1.311/1.318/1.318 Å). This changes the
  calculated pattern negligibly (C is a weak scatterer next to Ba) but makes
  the deposited CIF chemically coherent.
* **WO₃** – COD 2311041 (Loopstra & Boldrini 1966, neutron diffraction),
  transformed from its published *P*2₁/*c*, β = 136.06° cell into the
  conventional *P*2₁/*n* setting (*a* ≈ 7.30, *b* ≈ 7.54, *c* ≈ 7.69 Å,
  β ≈ 90.9°) with the matrix (1 0 1 / 0 1 0 / −1 0 0); the transformation is
  volume- and pattern-preserving (`scripts/mkwo3n.py`). This model fits
  distinctly better than the older Tanisaki (1960) γ-WO₃ entry, COD 1528915
  (R_wp 7.30 % vs 8.04 % with the same refinement protocol), because its
  oxygen coordinates are better determined.

Refined cells agree with the literature to within ~0.05 %, which is itself
confirmation of the assignment:

| | *a* (Å) | *b* (Å) | *c* (Å) | β (°) | *V* (Å³) |
|---|---|---|---|---|---|
| BaCO₃ refined | 5.30872(31) | 8.91603(53) | 6.43407(38) | 90 | 304.542(47) |
| BaCO₃ reference | 5.3103 | 8.9122 | 6.4365 | 90 | 304.62 |
| WO₃ refined | 7.30882(43) | 7.53809(44) | 7.69444(44) | 90.7455(36) | 423.886(66) |
| WO₃ reference (γ) | 7.306 | 7.540 | 7.692 | 90.88 | 423.7 |

## Refinement model

* **Peak positions.** All reflections sit 0.34° high at 2θ = 24° and 0.27° high
  at 2θ = 56°, i.e. the offset falls off as cos θ. It was modelled as a
  **sample displacement of −582(8) µm**. The alternative, a 2θ zero offset
  (constant shift), fits worse (R_wp 8.22 % vs 8.17 % at the matched stage of
  the protocol, both runs using the earlier Tanisaki WO₃ model) and forces both
  unit cells ~0.08 % too large; the displacement model puts both cells on their
  literature values. The displacement is large
  but physically possible for a loosely pressed powder in reflection.
* **Profile.** Pseudo-Voigt with refined U = 451(30), V = −319(20),
  W = 62.8(3.8), X = 10.34(46), Y = −1.4(7) (centidegree units), axial
  divergence SH/L = 0.0306(20), plus one isotropic microstrain per phase:
  922(138) × 10⁻⁶ for BaCO₃ and 2853(145) × 10⁻⁶ (≈0.29 %) for WO₃. The
  metadata flag `calibrated_instrument_profile: null`, so the instrument
  profile had to be refined together with the sample broadening; the split
  between the two is therefore not unique (Y came out slightly negative, i.e.
  the tan θ Lorentzian broadening is carried entirely by the phase microstrain
  terms). Crystallite-size broadening was held: at these widths it is >88 %
  correlated with microstrain and refines to non-physical values.
* **Radiation.** Cu Kα₁ + Kα₂ with λ = 1.540598/1.544426 Å and I₂/I₁ = 0.5 as
  reported, held fixed; releasing the ratio changes R_wp by <0.04 percentage
  points and nothing else. Polarisation was held at 0.7 — refining it made the fit worse, so the
  `effective_polarization: null` entry cannot be filled from these data.
* **Background.** 8-term shifted Chebyshev. The pattern has a large, smoothly
  decaying background (2400 counts at 10° falling to 210 counts at 100°), about
  26 % of the strongest peak; nothing in it resembles a broad amorphous halo.
* **Structure.** Refined: both cells, both scale factors, Ba(*y*,*z*) and
  W1/W2(*x*,*y*,*z*), and species-grouped U_iso (Ba; C+O of the carbonate;
  W; O of the oxide). Resulting bond lengths are sound — C–O
  1.311–1.318 Å, Ba–O 2.681–2.892 Å (9-coordinate), W–O 1.755, 1.777, 1.872,
  1.925, 2.121, 2.139 Å (the characteristic γ-WO₃ distorted octahedron).
* **Weighting.** No point uncertainties were supplied, so GSAS-II's counting
  statistics weights w = 1/max(y, 1) were used.

## What could *not* be determined

* **Light-atom positions.** Releasing the C and O coordinates lowers R_wp to
  7.05 % but drives them to impossible geometries (WO₃ oxygens with
  U_iso = 2.4 Å² and −0.08 Å², a carbonate with C–O = 1.01 and 1.44 Å). With
  Ba and W in the same pattern, lab Cu-Kα data do not locate C and O: those
  coordinates in the deposited CIFs are **fixed at the published values, not
  refined**, and should not be quoted as a result of this work.
* **Displacement parameters.** U_iso(Ba) = 0.0017(6) Å² is implausibly small
  and U_iso(O, WO₃) = 0.0324(30) Å² implausibly large; U_iso(W) refined
  slightly negative and was held at 0.005 Å². These are the usual sinks for
  un-modelled absorption and profile error and are not physically meaningful
  here.
* **Scheelite BaWO₄ — not detected, ≲3 wt%.** Adding BaWO₄ with its published
  cell held lowers R_wp from 7.30 % to 7.07 % and returns 2.7(2) wt%, which
  looks like a 16σ detection. It is not one. Breaking the χ² gain down by 2θ,
  22 % of it falls in 35–39°, where scheelite has no reflections at all, and
  30 % falls on the flanks of the strong WO₃ 120 line at 26.9° — the extra
  phase is absorbing background curvature and WO₃ peak-shape error. The
  decisive test is BaWO₄ 200 at 32.2°, the only scheelite line in a clear
  region: fitting a peak of the expected width there gives 18–28 counts, the
  same as what a peak fitted at reflection-free control positions
  (31.0, 36.5, 37.5, 39.2, 51.8, 57.8°…) returns (−18 to +21 counts). So the
  pattern neither contains nor excludes BaWO₄ below roughly 3 wt%, and it is
  not reported as a phase.
* **WO₃ polymorph (γ vs δ).** The triclinic δ-WO₃ model (*P*1̄, COD 2106293)
  fits slightly better (R_wp 7.14 %), but it refines to α = 89.89°, γ = 90.05°,
  i.e. 0.05–0.11° from monoclinic, whereas genuine δ-WO₃ has α = 88.8°,
  γ = 90.9°. The triclinic metric is therefore *not* supported; the improvement
  comes from that model's different oxygen positions, not from the symmetry
  lowering. γ-WO₃ (*P*2₁/*n*) is reported. A small δ-WO₃ admixture, or
  stacking/twin disorder, cannot be excluded and is the most likely source of
  the residual misfit at 23.4–24.7° and 26.9°.
* **Preferred orientation.** A one-parameter March–Dollase correction on BaCO₃
  lowers R_wp by ~0.13 percentage points but the axis is not determinable (r = 0.95 along
  [100], r = 1.05 along [001], indistinguishable fits). It was left out of the
  final model; it shifts the weight fractions by <0.5 wt%.

## Uncertainty on the weight fractions

The least-squares esd is ±0.2 wt%, which is far too optimistic. Repeating the
whole refinement with different (but defensible) choices gives:

| variant | BaCO₃ wt% |
|---|---|
| final model (Loopstra WO₃) | 50.3 |
| Tanisaki γ-WO₃ model | 53.0 |
| triclinic δ-WO₃ model | 52.5 |
| + March–Dollase on BaCO₃ | 50.6–50.8 |
| + BaWO₄ as a third phase | 49.0 |

so the realistic uncertainty is **≈ ±3 wt%**: BaCO₃ 50–54 wt%, WO₃ 46–50 wt%.
The spread is dominated by the WO₃ structural model.

No micro-absorption (Brindley) correction was applied. Here that is benign
rather than a gap: from NIST mass attenuation coefficients at 8.048 keV the two
phases have almost the same linear attenuation coefficient
(μ ≈ 1.00 × 10³ cm⁻¹ for BaCO₃ at 4.304 g cm⁻³ and ≈ 1.01 × 10³ cm⁻¹ for WO₃ at
7.266 g cm⁻³), so the Brindley factors of the two phases are nearly equal and
cancel in the fraction ratio, whatever the particle sizes.

The qualitative conclusion — a roughly equal-by-weight, Ba-rich-of-1:1-by-mole
mixture of unreacted BaCO₃ and WO₃, with no ternary product — is robust.

GOF = 2.10 rather than ~1 reflects this residual profile/structure misfit, not
a missing phase: the difference curve is flat except directly under the
strongest reflections.

## Reproducing

All scripts are run with the GSAS-II virtual environment
`~/.local/share/characterizagent/backends/gsas2/venv/bin/python`, from `work/`:

```
work/pattern.xy          # inputs/pattern.csv converted to two-column xy
work/cuka.instprm        # Cu Ka1/Ka2 instrument parameter file (hand written)
work/ref_BaCO3f.cif      # BaCO3 starting model (COD 9010928, C site corrected)
work/ref_WO3n.cif        # WO3 starting model (COD 2311041 -> P2_1/n setting)

python scripts/mkwo3n.py            # derives + checks the WO3 transformation (pymatgen env)
python ../scripts/final3.py final.gpx   # the refinement -> work/final.gpx
python ../scripts/export.py final.gpx   # -> BaCO3.cif, WO3.cif, fit.csv, result.json
python scripts/figure.py                # -> fit_overview.png (pymatgen env)

# supporting tests quoted above
python ../scripts/bawo4_bound.py            # BaWO4 added with its cell held
python ../scripts/bawo4_test2.py A|B        # BaWO4 with 26.4-27.4 excluded / with d-WO3
python ../scripts/tweak.py final.gpx t.gpx md:BaCO3:1,0,0   # one extra feature at a time
python ../scripts/run.py x.gpx BaCO3,WO3t shift,sh,uiso     # alternative starting models
```
