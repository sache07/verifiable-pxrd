# Powder XRD phase analysis

The modeled crystalline inventory is **52.17 wt% monoclinic WO3** and **47.83 wt% orthorhombic BaCO3 (witherite)**, normalized over the modeled crystalline phases. This is consistent with a largely unreacted BaCO3/WO3 precursor mixture after the reported 250 degrees C heating, but chemistry was not used to constrain or round the fractions. The formal GSAS-II scale-derived standard uncertainty is 0.16 wt% for each fraction, while a more realistic uncertainty is about 1 wt% because closely related WO3 symmetry/source models shift the result.

## Evidence and model selection

The three strong lines at about 23.42, 23.86, and 24.64 degrees and their split higher-angle families at 33--35, 42, 47--56, and 60--63 degrees identify low-symmetry WO3. Independent lines at about 19.62, 24.09, 28.01, 39.57, 43.10, 44.35, 45.06, and 47.03 degrees require witherite BaCO3. Deleting WO3 raises Rwp to 7.53%; deleting BaCO3 raises it to 5.60%.

Public COD candidates were round-tripped through GSAS-II into compatible settings, reloaded, and screened with the supplied occupancy/contact test before fitting. The submitted parents are COD 2311041 (WO3, P 21/c) and COD 9010928 (room-temperature synthetic witherite, Pmcn; equivalent standard type Pnma); both final CIFs pass with no flagged contacts. Under the same fixed-coordinate model, orthorhombic WO3 was clearly inferior (Rwp 4.00%). Monoclinic and triclinic WO3 were much closer: the monoclinic source gave Rwp 2.4435% versus 2.4489% for triclinic with the initial common profile, while a simpler profile restart slightly favored triclinic (2.3868% versus 2.4006%). The monoclinic ambient-phase model was retained as the more parsimonious structure; P-1 WO3 remains a credible symmetry alternative and is the main structural uncertainty.

A physically repaired scheelite BaWO4 diagnostic model refined to only 0.27(8) wt% and changed Rwp by just 0.0016 percentage points. Its diagnostic line near 31.9 degrees is not independently visible, so overlapping lines do not establish this trace phase; it was removed from the final inventory. No other multi-line residual family supports an additional crystalline phase.

Cells, scales, a six-term smooth background, angular zero, and the minimal positive common profile terms W and X were refined; atomic coordinates were kept at the published parents. Four-, six-, and eight-term backgrounds and zero-versus-specimen-displacement branches changed the WO3 fraction by only about 0.14 wt%. Size and strain terms changed fractions materially or became nonphysical, texture was negligible, polarization attempted to exceed its physical range, and selective W-coordinate refinement was more than 99.6% correlated. Those terms were rejected.

## Final refinement and uncertainty

The final full-grid fit has Rwp = 2.3999%, Rp = 1.8726%, Rexp = 1.8383%, and goodness of fit = 1.3069. Refined cells are:

- WO3 (P 21/c): a = 7.67960 A, b = 7.53817 A, c = 10.53204 A, beta = 136.15297 degrees.
- BaCO3 (Pmcn): a = 5.34055 A, b = 8.93177 A, c = 6.42583 A.

The fractions describe only the modeled crystalline material; this scan does not independently quantify amorphous content. Atomic coordinates, especially oxygen positions, are not determined reliably enough by these data to justify moving them away from the published parents. The exact WO3 monoclinic-versus-triclinic symmetry is likewise not uniquely resolved.

An independent no-refinement replay regenerated fresh reflections and structure factors from `final.gpx`. It returned Rwp = 2.3999004%, exactly the submitted fractions, no project review flags, and one-to-one agreement between the project phases and submitted CIFs.
