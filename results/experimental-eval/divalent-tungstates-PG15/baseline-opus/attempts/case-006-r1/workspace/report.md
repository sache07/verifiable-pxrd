# Phase analysis of the CuO + WO3 (800 °C) product

## Result

| Phase | Formula | Space group | Weight fraction | CIF |
|---|---|---|---|---|
| Cuprotungstite-type copper tungstate | CuWO4 | P-1 (#2), triclinic | **97.5 wt%** | `CuWO4.cif` |
| γ-tungsten trioxide (unreacted precursor) | WO3 | P2₁/n (#14), monoclinic | **2.5 wt%** | `WO3.cif` |

Fractions are normalized over these two crystalline phases (no internal standard was
measured, so amorphous content cannot be quantified).

Final Rietveld statistics (GSAS-II, 9.90–100.09° 2θ, 8301 points, 66 refined variables):
**Rwp = 3.78 %, Rp = 2.98 %, Rexp = 2.42 %, GOF = 1.56 (χ²_red = 2.43)**;
Bragg residuals R(F) = 1.34 % (CuWO4, 273 reflections) and 2.62 % (WO3, 439 reflections).
Observed/calculated/difference profile: `fit.csv` (plot: `fit.png`); project: `final.gpx`.

## Evidence

**Identification.** The precursors (CuO + WO3) restrict the chemistry to Cu–W–O. All
Cu–W–O, Cu–O and W–O entries of the bundled COD-filtered structure database were screened
by simulating their powder patterns and comparing with the observed peak list:

* Every strong observed line, and their relative intensities, match triclinic CuWO4:
  the 100 %/87 %/64 %/58 % quartet at 28.97/30.44/31.94/32.43° is the CuWO4
  (11-1)/(111)/(1-1-1)/(1-11) group, with (100) at 19.31° (57 %) and (1-10) at 26.27° (53 %).
* All observed positions sit ≈ +0.25–0.30° above the ideal CuWO4 positions, with the offset
  decreasing as cos θ. This is a sample-displacement error, not a cell effect, and it refines
  to a single Bragg–Brentano displacement parameter. Zeroing it raises χ² by two orders of
  magnitude, confirming the interpretation.
* A weak residual triplet at 23.44/23.91/24.68° plus lines at 26.9, 33.56 and 33.90° is left
  over by a CuWO4-only model; these are the γ-WO3 (002)/(020)/(200), (120), (022) and (20-2)
  reflections. Its refined cell, 7.3035(5)/7.5385(7)/7.6900(6) Å, β = 90.884(10)°, agrees with
  literature γ-WO3 (7.306/7.540/7.692 Å, 90.88°) to <0.01 Å.
* Control refinement: CuWO4 alone, same protocol, gives Rwp = 8.58 % / GOF = 3.54 versus
  3.78 % / 1.56 for the two-phase model — the minor phase is required by the data.

**Rejected candidates.** CuO (tenorite) and Cu2O (cuprite) were each added as a third phase
and refined to 0.00 wt% (adding CuO degrades Rwp to 3.87 %). Cu3WO6 and Cu2WO4 are excluded
directly: their strongest calculated lines (Cu3WO6 320 near 33.2° and 210 near 20.5°;
Cu2WO4 at 11.6, 13.4, 18.3°) have no counterpart in the data — the observed net intensity at
those positions is ≤0.6 % of the strongest peak, and 10–15° 2θ contains only background. The
high-pressure CuWO4-II polymorph refines to 0.2 wt% with no meaningful change in Rwp
(3.7788 → 3.7731) and is not distinguishable from the main phase. The practical detection
limit here is about 0.5 wt% for a well-crystallized heavy-metal oxide.

**Structure refinement.** Starting model for CuWO4: ambient-pressure Forsyth/Kihlborg-type
P-1 structure (COD 4000806 coordinates with the ambient cell). Refined: cell, all six atomic
coordinates, Uiso (one common value for the four O sites), anisotropic (generalized)
microstrain, phase fraction. Refined cell a = 4.70858(6), b = 5.84317(8), c = 4.88196(4) Å,
α = 91.654(1)°, β = 92.532(1)°, γ = 82.753(1)°, V = 133.078(2) Å³ — within 0.15 % of published
CuWO4. The refined coordination is chemically sound: a Jahn–Teller 4+2 Cu–O octahedron
(1.86, 1.93, 1.94, 1.99 + 2.31, 2.39 Å) and a distorted WO6 octahedron (1.82–2.26 Å).
Uiso values are positive and reasonable (Cu 0.0074(4), W 0.00547(20), O 0.0051(8) Å²).
Instrument/sample model: Cu Kα1/Kα2 (0.5 ratio) as supplied, Chebyshev background
(12 terms), U/V/W + X, axial-divergence asymmetry SH/L = 0.071, sample displacement.

## Uncertainty and limitations

* **CuWO4 fraction (97.5 wt%) is reliable**; **WO3 is 2.5 ± 0.2 wt%**. The statistical esd on
  the fractions is only ±0.03 wt%, which is optimistic. The ±0.2 wt% range is the spread seen
  over defensible model variants (WO3 Uiso from 0.003–0.020 Å², Kα2 ratio 0.48–0.50,
  polarization 0.5–0.7, zero-point versus displacement, isotropic WO3 microstrain).
* **No microabsorption (Brindley) correction was applied.** Both phases are strongly absorbing
  and of similar μ, so the effect on a 2.5 wt% minor phase should be small, but if the WO3 is
  present as coarse unreacted grains its fraction could be underestimated.
* **The WO3 structure is not refined, only scaled.** At 2.5 wt% its atomic coordinates and
  displacement parameters cannot be determined (unconstrained refinement of its Uiso diverges
  to nonphysical values); coordinates were held at the literature γ-WO3 values and Uiso fixed
  at typical room-temperature values. The assignment to the γ (P2₁/n) polymorph rests on cell
  metrics and peak positions; the closely related δ/ε-WO3 distortions cannot be ruled out from
  2.5 wt% of overlapped reflections.
* **Oxygen positions in CuWO4 carry the usual lab-XRD caveat**: with W dominating the
  scattering, O coordinates have esds of ~0.001 in fractional units and the shortest refined
  Cu–O distance (1.861 Å) is ~0.09 Å shorter than the single-crystal value. The cation
  positions and the cell are well determined; the O sublattice should be treated as
  approximately, not definitively, refined.
* Remaining misfit is concentrated at the tops of the strongest CuWO4 reflections (≤2 % of the
  maximum intensity) and is plausibly residual profile/anisotropic-broadening and mild
  preferred-orientation error; adding 4th-order spherical-harmonic texture changed Rwp by only
  0.004 % absolute and the fractions by <0.01 wt%, so it was not retained.
* The implied cation ratio of the modeled mixture is Cu:W = 0.967:1 (3.4 mol% W excess),
  consistent with a slightly W-rich starting mixture or incomplete reaction; no Cu-bearing
  second phase is present to balance it, which is itself consistent with the absence of CuO.

## Files

* `CuWO4.cif`, `WO3.cif` — refined structures (GSAS-II export from `final.gpx`)
* `fit.csv` — `two_theta_deg, y_obs, y_calc, y_diff, y_background`
* `result.json` — phases, CIF paths, weight fractions, fit statistics, notes
* `final.gpx` — GSAS-II project behind every number above
* `scripts/` — the scripts used (`ref_final.py` builds the final model, `finalize.py` exports)
