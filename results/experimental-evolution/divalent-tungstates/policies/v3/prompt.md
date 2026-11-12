Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Evidence-led refinement additions

Apply these additions to P0.

## Candidate and inventory discipline

Before interpreting any trial, inspect the candidate's occupied composition, symmetry, source conditions, disorder, and interatomic geometry. Reject flagged or chemically incompatible records. If a plausible phase fits poorly, test a physically valid alternate record before rejecting the phase. Compare polymorphs only after each candidate has an adequate common profile, using the same restrained phase nuisance schedule and diagnostic reflections; a candidate that wins only through compensation is not identified.

After every phase addition, removal, source replacement, or analogue substitution, reconverge background, every phase scale, the chosen common angular correction, and cells before judging the residual. A one-pass scale test against a biased base is not decisive. Reinspect residual peak families and precursor/product mass balance; coherent unmatched peaks remain missing-phase evidence even when partly overlapped.

If a chemically plausible formula has no exact entry, search cross-chemistry prototypes rather than only its element-system key. The helper ranks records with the same reduced stoichiometric pattern:

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Optionally add an indexed `--space-group N` and `--cell a b c alpha beta gamma`. Inspect several top parents. Preserve the parent and document a chemically justified site substitution. Physical-screen the adapted model, then refine its scale, cell, and at most one supported width term in stages. Do not transfer case-specific coordinates or force a candidate whose scale, unique peaks, or geometry fail.

## Refinement discipline

Neutralize unused HAP defaults: strain zero and size large. Choose zero versus specimen displacement from angular dependence; do not co-refine unidentifiable versions. Before phase broadening, establish a nonnegative low-dimensional common profile. Check resolved sharp peaks from the same phase at low, middle, and high angle: U/W/X must reproduce their angular width trend. A sharp lower envelope guards against averaging broad phases; it is not a target to fix. Test bounded SH/L early when low-angle asymmetry repeats across peaks. Covariance alone does not reject a term, but bounds, instability, or failure on fresh replay do. If later phase terms hit bounds, return to common-profile adequacy.

Only then challenge size-only and strain-only branches one phase at a time from neutral values; combine or add anisotropy only for distinct reproducible angular or hkl-dependent residuals. Before phase texture, test whether background, polarization, or sample roughness explains a coherent angle-dependent intensity trend shared across phases; reject bound-seeking surrogates. Compare no texture and plausible symmetry-distinct axes against multiple diagnostic reflection families rather than defaulting to one axis.

After each accepted profile or intensity change, save, reopen, and perform a fresh native atomic replay over the full range. Prune unsupported terms and recheck bounds, frozen variables, correlations, geometry, fractions, and project/export agreement.

Reusable package files are in learned/.
