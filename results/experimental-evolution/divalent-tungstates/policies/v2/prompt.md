Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Evidence-led refinement additions

Apply these additions to P0.

## Candidate and inventory discipline

Before interpreting any trial, inspect the candidate's occupied composition, symmetry, source conditions, disorder, and interatomic geometry. Reject flagged or chemically incompatible records. If a plausible phase fits poorly, test a physically valid alternate record before rejecting the phase. Compare polymorphs under the same modest nuisance model and diagnostic reflections before texture or phase broadening; a candidate that wins only through extreme compensation is not identified.

After every phase addition, removal, source replacement, or analogue substitution, reconverge background, every phase scale, the chosen common angular correction, and cells before judging the residual. A one-pass scale test against a biased base is not decisive. Reinspect residual peak families and precursor/product mass balance; coherent unmatched peaks remain missing-phase evidence even when partly overlapped.

If a chemically plausible formula has no exact entry, search cross-chemistry prototypes rather than only its element-system key. The helper ranks records with the same reduced stoichiometric pattern:

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Optionally add an indexed `--space-group N` and `--cell a b c alpha beta gamma`. Inspect several top parents. Preserve the parent and document a chemically justified site substitution. Physical-screen the adapted model, then refine its scale, cell, and at most one supported width term in stages. Do not transfer case-specific coordinates or force a candidate whose scale, unique peaks, or geometry fail.

## Profile discipline

Choose zero versus displacement from angular dependence; do not co-refine strongly correlated versions. Neutralize unused HAP defaults: strain zero, size large. Before common-width refinement, inspect isolated peaks assigned to each phase at low, middle, and high angle. Use the lower width envelope from the sharpest well-supported phase as the common instrument baseline, not the dominant phase or an average of broad and narrow peaks. Build a clean branch with nonnegative low-dimensional U/W/X; test bounded SH/L only for reproducible low-angle asymmetry. If necessary, give visibly broader phases provisional isotropic broadening so they cannot force the common baseline wide.

After inventory, scales, cells, and that baseline stabilize, challenge each phase separately with size-only and strain-only branches from neutral values. Reconverge fully after each; combine terms only if their distinct angular signatures remain supported. Add anisotropy only for reproducible hkl-dependent residuals. Prune zero/no-broadening bounds, unstable terms, frozen variables, and strong correlations. Never release every phase term or enumerate anchors simultaneously.

After each accepted profile change, save, reopen, and perform a fresh native atomic replay over the full data range; reject improvements that exist only in stored arrays. Export CIFs, fractions, and `fit.csv` only from that replay-checked project.

Reusable package files are in learned/.
