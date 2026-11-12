# Powder XRD phase analysis

The specimen is modeled as three crystalline phases. Weight fractions are normalized over those modeled crystalline phases only.

| Phase | Structural assignment | Weight fraction |
|---|---|---:|
| MnWO4 | Wolframite, `P 2/c` | 63.43 wt% |
| WO3 | Monoclinic, `P 21/n` | 22.76 wt% |
| Mn2WO5 | Analogue-derived model, `P n n m` | 13.81 wt% |

The dominant reflection set is accounted for by wolframite MnWO4, and a second coherent family is matched by monoclinic WO3, consistent with residual precursor in the Mn3O4/WO3 synthesis heated at 800 C. The remaining coherent peaks index together as orthorhombic Mn2WO5. Two independent `P n n m` starts derived from symmetry-compatible oxide parents converged to essentially the same physical basin after identical composition, cell, and coordinate treatment. A symmetry-diverse `C m c m` pseudobrookite-type start collapsed to zero contribution, and ordinary tetragonal or orthorhombic Mn3O4 models did not provide a physically acceptable match. Every retained phase has a positive contribution supported across a reflection family; no coherent fourth family remains.

The final read-only GSAS-II replay gives Rwp = 12.612%, Rp = 7.888%, and GOF = 6.336 on all 8,301 measured points. The submitted `fit.csv`, CIFs, and fractions were exported from the exact submitted `final.gpx` after the required one-time bounded polish. Formal GSAS-II fraction standard uncertainties are about 0.13–0.15 wt%, but these describe local least-squares precision and not model-selection uncertainty.

The Mn2WO5 assignment is the least certain result. Its peaks require strong size/strain broadening and preferred orientation near the tested laboratory limits, so the detailed atomic coordinates and 13.81 wt% fraction cannot be regarded as equally reliable as the two reference-backed phases; systematic fraction uncertainty is plausibly several weight percent. The monoclinic WO3 source topology contains a short symmetry-related O–O contact of about 1.576 A that was already present in the reference model, so its phase identity is well supported but its detailed oxygen geometry should be treated cautiously. Surface roughness and specimen-displacement refinements were excluded because they were bound-limited or inseparable from correlated alternatives. Amorphous content, if present, cannot be determined from this crystalline-only normalization.
