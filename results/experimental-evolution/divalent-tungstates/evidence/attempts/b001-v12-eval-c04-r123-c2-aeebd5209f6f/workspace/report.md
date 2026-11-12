# PXRD phase analysis

The modeled crystalline product is **wolframite MnWO4 (P2/c), 79.405 wt%**, plus **monoclinic WO3 (P2_1/c), 20.595 wt%**. Fractions are normalized over these two crystalline phases. The final full-range GSAS-II refinement gives Rwp = 7.787%, Rp = 5.210%, and GOF = 3.134.

## Evidence

The precursor chemistry (WO3 and Mn3O4 heated at 700 °C) makes divalent manganese tungstate charge-balanced and plausible. Metadata gives no precursor amounts or ratio, so a fixed mass-balance closure constraint could not be applied. No exact MnWO4 entry was present in the supplied Mn-O-W index; a stoichiometric-analogue search identified wolframite FeWO4 parents. The retained starting model was COD 9008124 with Fe replaced by Mn. Its P2/c topology explains independent MnWO4 families, including 100, 110, 11-1/111, and 020 and the observed splitting near 29.58/30.03° 2theta. Competing P2/c parents (COD 1567215 and 1568792) and a C2/m MnMoO4-derived model were challenged separately; the retained P2/c model was superior, and its atomic coordinates were subsequently refined.

After MnWO4 was fitted, positive residual intensity remained in multiple non-coincident families near 23, 33–34, 40, 49, 53, and 60–65° 2theta. These are jointly explained by monoclinic WO3 from COD 2311041. Alternative WO3 records in P2_1/c, Pnma, and P-1 were refined as competitors; the lower-symmetry P-1 source did not outperform the retained physical P2_1/c source. The exact indexed Mn3WO6 candidate was rejected because its strong calculated reflections near 19.95 and 20.49° are absent, and Mn3O4 did not supply coherent residual families. No additional phase had a replay-stable positive scale with two independent families.

The final cells are a = 4.79911, b = 5.70708, c = 4.97590 Å, beta = 91.1265° for MnWO4 and a = 7.68931, b = 7.55248, c = 10.51595 Å, beta = 136.0347° for the retained setting of WO3. Final and starting retained models passed `learned/cif_health.py`; the final CIFs contain no invalid occupancies or flagged hard contacts.

## Refinement and uncertainty

The refinement used the reported Cu K-alpha doublet and its 0.5 Kalpha2/Kalpha1 ratio over the complete 9.90–100.09° range. Refined terms were phase scales and cells, MnWO4 coordinates, a smooth 10-term background, one specimen-displacement correction, surface roughness, nonnegative common W/X width terms, and symmetry-compatible [010] WO3 size anisotropy. MnWO4 size and strain collapsed or coupled singularly to the common profile and were left neutral; strain and preferred orientation are neutral for both phases. Texture trials were pruned because their gains were axis-ambiguous and traded low-angle improvement for worse high-angle residuals. WO3 coordinates were kept at the source values because the broad, weaker WO3 pattern does not determine a reliable independent atomic model.

The GSAS-II covariance gives a formal fraction uncertainty of about 0.19 wt% for each phase. This is smaller than plausible model systematic error; a conservative interpretation is roughly ±1 wt% absolute. Fractions do not include amorphous material because no internal standard was supplied. Pointwise uncertainties were also absent, so sigma = sqrt(counts) was used as a Poisson proxy; consequently the absolute GOF and formal standard uncertainties should not be overinterpreted.
