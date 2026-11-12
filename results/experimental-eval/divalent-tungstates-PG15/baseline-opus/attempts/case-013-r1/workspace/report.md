# Phase analysis of the PbO + WO3 (500 °C) powder pattern

**Data**: `inputs/pattern.csv`, Cu Kα1+Kα2 (λ1 = 1.540598 Å, λ2 = 1.544426 Å, I2/I1 = 0.5),
Bragg–Brentano reflection geometry, 10.01–99.99° 2θ, 0.01087° step, raw counts
(background is 62 % of the total counts — strong Pb/W fluorescence with Cu radiation).

**Result**: five crystalline phases. Rietveld refinement of all five simultaneously gives
**Rwp = 10.60 %, Rp = 7.05 %, Rexp = 3.49 %, GOF = 3.03** (8282 points, 43 refined parameters).

| phase | formula | space group | wt % (normalised) | stat. esd | realistic uncertainty |
|---|---|---|---|---|---|
| stolzite (scheelite-type PbWO4) | PbWO4 | I4₁/a | **60.2** | 0.3 | ±3 |
| Pb2WO5 (Pb2MoO5 structure type) | Pb2WO5 | C2/m | **12.8** | 0.2 | ±4 |
| γ-WO3 (unreacted) | WO3 | P2₁/n | **10.1** | 0.2 | ±2 |
| massicot, β-PbO (unreacted) | PbO | Pbcm | **9.2** | 0.2 | ±5 |
| litharge, α-PbO (unreacted) | PbO | P4/nmm | **7.7** | 0.2 | ±5 |

Files (in the working directory, with duplicates in `out/`):
`stolzite.cif`, `Pb2WO5.cif`, `WO3.cif`, `massicot.cif`, `litharge.cif`,
`fit.csv` (2θ, y_obs, y_calc, y_diff, y_background), `result.json`,
`final.gpx` (the GSAS-II project that produced all of the above) and `fit_plot.png`.

Implied bulk cation ratio of the modelled crystalline material: **Pb/W = 1.26**
(≈ 1.26 PbO : 1 WO3), i.e. the product is a partially reacted, slightly Pb-rich mixture:
roughly 60 % of the charge has reacted to PbWO4, ~13 % to the 2:1 intermediate Pb2WO5, and
~17 % PbO + ~10 % WO3 remain unreacted.

## 1. Instrument/sample corrections that had to be established first

* **A systematic 2θ shift of ≈ +0.25°** affects *every* phase in the pattern. It was detected
  by least-squares fitting of eight indexed scheelite PbWO4 lines: without an offset the cell comes
  out ~0.4 % too small, whereas refining cell + offset together gives a = 5.4627, c = 12.0537 Å
  with an offset of +0.30° and a residual rms of 5 × 10⁻³° (the full Rietveld then yields
  a = 5.46117(20), c = 12.05246(33) Å, matching stolzite). Fitting
  Δ2θ ∝ cos θ (specimen displacement) and Δ2θ = const (zero error) are indistinguishable here;
  the displacement model was used (`Shift` = −448 μm at the GSAS-II default goniometer radius of
  200 mm; the value scales with the true radius). This correction is essential — without it the
  lattice parameters of every phase are biased by ~0.4 % and phase identification is misleading.
* **Peak shape**: Gaussian Caglioti terms (U = 116, V = −134, W = 56 centideg²; FWHM ≈ 0.165° at
  27.7° rising to 0.27° at 94°) shared by all phases, plus a Lorentzian crystallite-size term per
  phase. Microstrain was held at a negligible value (500 × 10⁻⁶) because free refinement of both
  size and strain per phase is unstable (it drove strain negative). Apparent sizes:
  PbWO4 106 nm, WO3 124 nm, Pb2WO5 122 nm, massicot 50 nm, litharge 27 nm — these are indicative
  only, since the shared Gaussian term absorbs part of the sample broadening.
* **Suortti surface-roughness correction** (A = 0.30, B = 0.31). Without it the calculated
  intensities of the high-angle PbWO4 reflections (45–57°) fall ~20 % below the observations and
  the refinement drives the displacement parameters to zero; with it the trend disappears
  (ΔRwp = −1.7 %). This is expected for a strongly absorbing (μ ≈ 1000–2000 cm⁻¹) flat-plate
  specimen. Microabsorption (Brindley) was *not* applied: with coherent domain sizes of
  0.03–0.12 μm, far below 1/μ ≈ 5–10 μm, particle-absorption bias is negligible unless the powder
  is strongly agglomerated.
* Polarisation 0.5 (unpolarised, filtered tube), 12-term Chebyshev background, isotropic
  displacement parameters fixed at U_iso = 0.011 Å² (Pb, W) and 0.018 Å² (O).

## 2. Evidence for each phase

**PbWO4, stolzite (60 wt %)** — unambiguous. All 14 strong lines of the pattern (27.70, 29.91,
33.06, 45.03, 47.28, 51.49, 55.54, 56.82, 68.91, 72.27, 75.66, 81.08, 85.98, 94.03° and more)
index on the body-centred tetragonal scheelite cell; the refined cell a = 5.46117(20),
c = 12.05246(33) Å matches stolzite (5.462, 12.046 Å) to 0.08 %. The monoclinic polymorph
raspite was explicitly tested and rejected: its strongest reflections (d = 3.627, 3.597, 2.489 Å)
are absent.

**γ-WO3 (10 wt %)** — unambiguous. The characteristic monoclinic triplet at 23.39/23.89/24.64°
(002/020/200) plus 33.52, 34.43, 41.91, 48.44, 50.22, 51.01, 56.31° are all present and
accounted for. Refined cell 7.29811(106), 7.54121(120), 7.69467(119) Å, β = 90.466(17)°; the
β angle is 0.4° smaller than the standard value (90.88°), which may reflect genuine strain in the
partially reacted precursor or correlation with the heavily overlapped neighbouring phases.
Removing WO3 is not an option — its lines have no other possible owner in a Pb–W–O system.

**α-PbO (litharge, 8 wt %) and β-PbO (massicot, 9 wt %)** — both unreacted PbO polymorphs are
present. Litharge is required by the (101), (110), (112), (211) lines at 28.93, 32.11, 48.86,
54.91°; massicot by (111), (200), (002), (311) at 29.39, 30.62, 38.09,
53.39°. Both are broadened (apparent sizes 27 and 50 nm). Control refinements (identical staged
protocol, coordinates additionally free, which gives Rwp = 10.32 % for the full five-phase model):
dropping massicot raises Rwp to 12.53 %, dropping litharge to 14.13 % — both are required. Their refined cells agree with the literature
(litharge 3.97447(81)/5.03435(157) Å; massicot 5.89464(99)/5.48700(103)/4.75465(75) Å).

**Pb2WO5 (13 wt %)** — identified by indexing the residual after the four phases above.
Twenty-three of 28 residual lines index on a C-centred monoclinic cell
a ≈ 14.1–14.2, b ≈ 5.80, c ≈ 7.30–7.35 Å, β ≈ 113–114° (rms 0.2 % in d), which is within ~1 % of
Pb2MoO5 (C2/m, 14.222/5.785/7.326 Å, 114.17°) — the known 2PbO·MO3 structure type. The observed
intensity ranking also matches the Pb2MoO5 calculation: the strongest residual line (25.91°) is
(310), followed by (11-2) at 29.35°, (020) at 31.05°, (002) at 26.77°, (31-2) at 30.62°.
The structural model is therefore Pb2MoO5 with W on the Mo site; the refined cell
a = 14.2208(118), b = 5.80545(60), c = 7.35127(363) Å, β = 113.878(14)° is slightly larger than
the Mo analogue, as expected for W. Dropping this phase raises Rwp to 13.29 % (same control
protocol as above, full model 10.32 %); keeping only PbWO4 + WO3 + Pb2WO5 gives 15.14 %.
A search of all 3352 Pb- or W-containing entries of the available COD subset (62 098 CIFs) found
no better candidate, and no Pb2WO5 entry exists in that subset.

## 3. What is *not* reliably determined

* **One peak remains unexplained**: the doublet at 30.15/30.24° 2θ (d ≈ 2.986/2.977 Å, corrected
  for the 2θ offset), accounting for **1.7 % of the total Bragg intensity** and the single largest
  residual (1510 counts, 30σ). A Le Bail test (free intensities for Pb2WO5) could not fit it,
  so the refined C2/m Pb2WO5 lattice has no reflection there. With the same cell it would be the
  C-centring-forbidden (1 0 2) reflection, which suggests the real Pb2WO5 is a *primitive*
  (super-structured) variant of the Pb2MoO5 type rather than C2/m; an additional, unidentified
  minor phase cannot be excluded. Attempts to re-index so that both 30.15° and 30.62° are
  explained by one C-centred cell failed, and re-setting the cell to the alternative solution
  (a = 14.10 Å, β = 112.9°) fits 30.15° but loses 30.62° and worsens Rwp (11.9 vs 10.6 %).
  Because of this the **Pb2WO5 structural model should be regarded as a structure *type*
  assignment, not a solved structure**, and its weight fraction carries a systematic uncertainty
  of several wt %.
* **The α-PbO / β-PbO split is poorly conditioned.** Their principal lines overlap each other and
  the Pb2WO5 lines in the 28.5–32° window, and both phases are broadened. In the control
  refinement without massicot, litharge rises to 33 wt % (Rwp 12.5 %); without litharge, massicot
  rises to 22 wt % (Rwp 14.1 %). The *total* PbO content (17 wt % in the accepted model) is
  better determined than the polymorph split (individually ±5 wt %).
* **Oxygen positions cannot be refined** from these Pb/W-dominated X-ray data. Free refinement of
  the PbWO4 oxygen position improved Rwp by only 0.25 % while shortening W–O to 1.68 Å (expected
  1.77–1.79 Å); refining the Pb2WO5 cation positions similarly distorted the WO4 tetrahedron
  (1.71–1.96 Å). All atomic coordinates in the submitted CIFs are therefore held at the
  reference-structure values, which give chemically correct geometry (PbWO4: W–O 1.773 Å ×4,
  Pb–O 2.61/2.65 Å; Pb2WO5: W–O 1.764–1.792 Å; litharge Pb–O 2.322 Å ×4; massicot Pb–O
  2.17–2.50 Å). Only lattice parameters, scale factors, size broadening and the global
  instrument/sample terms were refined.
* **Amorphous/poorly ordered material is not quantified.** No internal standard is available, so
  the five weight fractions are normalised over the modelled crystalline phases only, as
  requested. The broad component that the nanocrystalline PbO phases absorb may partly represent
  a disordered PbO-rich fraction; this is the main reason the PbO fractions (and hence the derived
  Pb/W = 1.26) should be treated as approximate.
* **No Bragg peaks exist below 23°** (the apparent structure there is Poisson noise on a steep
  fluorescence background). A residual excess of only ~25–55 counts persists over 16.5–20°, which
  is at the level of the background model and is not interpreted as a phase.
* GOF = 3.0 (χ² ≈ 9.2) is far above 1 because the data are counting-statistics-limited
  (up to 17 500 counts per point) while the model still has the deficiencies listed above;
  the quoted statistical esds are consequently optimistic. The "realistic uncertainty" column in
  the table reflects the spread seen across model variants (different peak-shape parameterisations,
  background orders, and phase subsets) rather than the least-squares esds.

## 4. Method and tools

Peak search and profile fitting (NumPy/SciPy) → d-spacing list → candidate screening against a
local COD subset with pymatgen's XRD calculator → least-squares cell indexing of the residual →
multi-phase Rietveld refinement with GSAS-II 5.7.8 (scriptable interface), staged as:
background + phase fractions → specimen displacement → crystallite size → lattice parameters →
surface roughness → profile U, V, W → convergence. Parameter limits were used to keep broadening
and displacement parameters physical. Scripts are in `scripts/`, intermediate refinements in
`work/`; the submitted project is `final.gpx`.
