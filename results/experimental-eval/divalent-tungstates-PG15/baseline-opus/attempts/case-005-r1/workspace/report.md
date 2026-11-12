# Phase analysis of the Co3O4 + WO3 (500 °C) product

## Summary

The pattern contains **two crystalline phases, both of them the starting materials**:

| Phase | Formula | Space group | CIF | Weight fraction (normalised over modelled crystalline phases) |
|---|---|---|---|---|
| γ-WO3 (monoclinic tungsten trioxide) | WO3 | *P* 2₁/*n* (#14) | `WO3.cif` | **0.752 ± 0.002** (75.2 wt%) |
| Co3O4 (normal spinel) | Co3O4 | *Fd*-3*m* (#227, origin 2) | `Co3O4.cif` | **0.248 ± 0.002** (24.8 wt%) |

No cobalt tungstate (or any other new phase) is detectable. Within the resolution of this
measurement the 500 °C treatment produced **no reaction**: the refined WO3 : Co3O4 molar ratio is
3.15 : 1 (Co : W = 0.95 : 1), i.e. the batch is still the 3 WO3 + 1 Co3O4 (Co : W = 1 : 1) mixture
that a CoWO4 synthesis would start from.

Final two-phase Rietveld fit (GSAS-II 5.7.8, project `final.gpx`, profile `fit.csv`, figure `fit.png`):

* R<sub>wp</sub> = 2.78 %, R<sub>p</sub> = 2.13 %, GOF = 1.62 (χ²<sub>red</sub> = 2.63), 8301 points, 33 refined parameters
* background-subtracted R'<sub>wp</sub> = 11.8 %, R'<sub>p</sub> = 14.3 % (the background is ~2900 counts, i.e. ~17 % of the tallest peak, so the plain R<sub>wp</sub> is flattered by it)
* per-phase Bragg residuals: WO3 R<sub>F</sub> = 2.9 % (440 reflections); Co3O4 R<sub>F</sub> = 3.4 % (22 reflections)

## Evidence for the phase assignment

**γ-WO3.** The three strongest lines of the pattern form the classic monoclinic-WO3 triplet,
observed at 23.47/23.95/24.71° 2θ. After correction for the sample-displacement offset (below)
these are 23.14/23.62/24.38°, i.e. d = 3.845/3.767/3.652 Å = (002)/(020)/(200) of a cell with
a = 7.305, b = 7.536, c = 7.693 Å, β ≈ 90.7° — γ-WO3 to within 0.1 %. Every medium and strong
line up to 100° 2θ is indexed by this cell (440 reflections), including the characteristic
33.6/34.2/34.5° and 50.25/50.66° groups (as observed, i.e. including the displacement shift).

**Co3O4.** The remaining lines (19.37, 31.63, 37.21, 38.91, 45.14, 56.24, 59.66, 65.54° observed)
index on a face-centred cubic cell with a = 8.0838 Å and the *Fd*-3*m* reflection conditions and
intensity pattern of the normal spinel; the refined lattice parameter matches stoichiometric
Co3O4 (8.084 Å at 296 K) to 0.005 %. No rocksalt CoO lines are present: the difference curve at
its two strongest positions (36.83° and 42.72° in the displaced frame) is flat to within ±30 counts.

**Instrumental note — large sample displacement.** All peaks are shifted to *higher* 2θ by
≈ +0.35° at 20° 2θ, decreasing as cos θ. This is a specimen-displacement error, not a lattice
effect: it is identical for both phases and follows the cos θ law rather than the tan θ law of a
wavelength error. The refinement gives a displacement of −669 µm on the 200 mm goniometer circle.
If this geometric term is ignored, both phases appear ~1 % compressed and the cell constants are
badly wrong; with it refined, both match literature values. (A 2θ-zero offset cannot be
distinguished from this with certainty, but the angular dependence clearly favours displacement.)

## Structural models

Published structures were used as starting models and only lattice parameters, scale factors and
profile terms were refined:

* **WO3** — neutron refinement of Loopstra & Boldrini, *Acta Cryst.* **21** (1966) 158 (COD 2311041).
  The COD entry describes γ-WO3 in the *P* 2₁/*c*, β = 136.06° setting; it was transformed
  (a′ = a + c, b′ = b, c′ = −a) to the conventional *P* 2₁/*n* cell before use, which is what the
  delivered CIF contains. Using instead the older *P* 2₁/*n* coordinates of Tanisaki (COD 1528915)
  with the identical protocol gave a clearly worse fit (R<sub>wp</sub> 4.25 % vs 3.2–3.4 % at the
  same refinement stage), so the neutron coordinates were kept.
* **Co3O4** — Liu & Prewitt, *Phys. Chem. Minerals* **17** (1990) 168, 296 K (COD 9005896).

Refined quantities: 12 background terms (Chebyshev), histogram scale, Co3O4 phase fraction,
sample displacement, both unit cells, instrument profile (Gaussian W, Lorentzian X, axial
asymmetry SH/L; U, V held at small fixed values and Y at 0), Co3O4 isotropic Lorentzian
microstrain, and anisotropic (generalised, 9-term) microstrain for WO3. Crystallite size was
held at 1 µm (negligible broadening; it is >90 % correlated with the instrumental X term here)
and displacement parameters were held fixed at chemically sensible values
(U<sub>iso</sub> = 0.005 Å² for W and Co, 0.010 Å² for O).

Refined cells: WO3 a = 7.30472(15), b = 7.53623(14), c = 7.69332(18) Å, β = 90.654(3)°,
V = 423.49(2) Å³; Co3O4 a = 8.08378(20) Å, V = 528.26(4) Å³.

The WO3 line broadening is strongly anisotropic — in the final model *h0l* reflections
(e.g. 303, 313, 323) are roughly three times broader than *hk*0/0*kl* reflections such as 110 and
002. This is the expected signature of the twin/domain structure of γ-WO3 (and of any residual
triclinic ε/δ-WO3 domains, which would appear as *h0l*-selective broadening rather than as
resolvable extra peaks). Including this anisotropy lowered R<sub>wp</sub> from 3.24 % to 2.78 % and
removed the systematic misfit of the 34.5° and 50.25° peaks; it did not move the weight fractions
(75.4 → 75.2 wt% WO3).

## Quantitative phase analysis and its uncertainty

Weight fractions come from the refined Rietveld scale factors (GSAS-II's standard
Z·M·V formulation) and are normalised over the two modelled phases. The quoted ±0.2 wt% is the
refinement esd only. The honest uncertainty is larger:

* Across every physically acceptable model variant tried (isotropic vs anisotropic microstrain;
  fixed vs element-grouped U<sub>iso</sub>; both WO3 starting structures; size refined or held) the
  WO3 fraction stayed within **74.4–75.4 wt%**. One further variant, adding a Bragg–Brentano
  surface-roughness correction, reached 76.5 wt% but refined to a negative roughness coefficient
  (A = −0.79) and was rejected as unphysical. We therefore quote **75 ± 1 wt% WO3 /
  25 ± 1 wt% Co3O4** as the defensible result, with the tabulated values as the best estimate.
* Microabsorption is a genuine systematic risk here: WO3 and Co3O4 have very different linear
  absorption coefficients for Cu Kα, and no Brindley correction was applied (particle sizes are
  unknown). This typically biases the fraction of the more absorbing phase (WO3) downward by a
  few relative percent and is not covered by the esd.
* **Amorphous or very poorly diffracting material is not quantified** — there is no internal
  standard and no spiking experiment, so the fractions are relative to the crystalline content only.
  The smooth, high background (~2900 counts, partly Co fluorescence under Cu radiation) means an
  amorphous component cannot be excluded or measured from these data.

## Phases tested and rejected

* **CoWO4 (wolframite, *P* 2/*c*, COD 5910316)** — the expected reaction product. Added as a third
  phase with its literature cell, its fraction refines to zero, and the difference curve shows no
  intensity at its strongest reflection (−111, 30.9° in the displaced frame: mean residual −29 ± 11
  counts). From the noise level and the Co3O4 (311) peak height, the upper bound is **≲1.5 wt%**.
  This is consistent with the literature: CoWO4 formation from Co3O4 + WO3 normally requires
  ≳600–700 °C, so 500 °C leaving the precursors intact is chemically expected.
* **Triclinic ε/δ-WO3 (*P*-1, COD 2106293)** — much worse fit than monoclinic γ-WO3 (R<sub>wp</sub>
  8.3 % vs 3.2 % with the identical protocol). A *minor* admixture of a second WO3 polymorph cannot
  be excluded (see below), but it is not required and cannot be quantified.
* **CoO, WO2, W metal** — no distinct unmodelled peaks at their principal lines (CoO 36.8/42.7°,
  W 40.6/53.1°, WO2 26.2/37.3° in the displaced frame); the difference curve there is flat to
  within a few tens of counts, and the small positive residual spread over 25.4–27.6° has no peak
  shape (it is a slight background underestimate on the flank of the WO3 120 line).
* **Preferred orientation** — March–Dollase tests on WO3 along [100], [010] and [001] all refined
  to 1.00 ± 0.00 (no texture); the term was dropped.

## What remains uncertain / cannot be determined

1. **Atomic coordinates and displacement parameters** of either phase are *not* determined by these
   data. Free refinement of individual U<sub>iso</sub> values drove them to unphysical values
   (negative for W, +0.09 Å² for one O) while lowering R<sub>wp</sub>, i.e. they were absorbing
   systematic errors (absorption/roughness contrast), not structural information. They were
   therefore fixed; the delivered CIFs carry literature coordinates with refined lattice parameters.
   No structural conclusion should be drawn from them.
2. **Residual misfit.** The largest remaining difference features (≈10σ at 34.16°, ≈7σ at 34.45°
   and 50.26°, ≈6σ at 42.33°) all sit on existing WO3 reflections, not at new positions. They are
   intensity/line-shape discrepancies of the WO3 model — most plausibly residual anisotropic
   strain/stacking disorder or a small ε/δ-WO3 domain contribution — and they are the main reason
   the background-subtracted R'<sub>wp</sub> is ~12 % rather than ~7 %.
3. **β = 90.654(3)°** for WO3 is slightly smaller than the usual 90.88–90.92° of well-crystallised
   γ-WO3. Combined with the anisotropic broadening this hints at a partially disordered/twinned
   WO3, but with lab data and a displacement correction of this size the absolute accuracy of β is
   limited, so this is a flag rather than a finding.
4. **Separation of instrumental and sample broadening** is not unique here (no instrument
   calibration standard was supplied; `calibrated_instrument_profile` is null in the metadata).
   The values of W, X and the microstrain terms should be read as an empirical profile
   description, not as physical microstructure parameters. Crystallite sizes were not determinable
   independently and are not reported.
5. The **polarization factor** (0.7 assumed, metadata reports it as unknown) and the Kα2/Kα1 ratio
   (0.5, as reported) slightly affect calculated intensities and hence the fractions; this is part
   of the ±1 wt% band quoted above.

## Files

| File | Contents |
|---|---|
| `WO3.cif`, `Co3O4.cif` | refined structural models (one per phase) |
| `fit.csv` | 2θ, y_obs, y_calc, y_diff, y_background for all 8301 points |
| `fit.png` | plot of the same |
| `result.json` | phases, CIF paths, normalised weight fractions, fit statistics, rejected phases, caveats |
| `final.gpx` | the GSAS-II project that produced all of the above (`final.lst` is its printed report) |
| `scripts/` | the scripts used (`final_refine.py` builds `final.gpx`; `export_results.py`, `polish_cif.py` write the deliverables) |
