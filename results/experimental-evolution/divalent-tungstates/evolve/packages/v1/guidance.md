# Evidence-led refinement additions

Apply these additions to P0.

## Candidate and inventory discipline

Before interpreting any trial, inspect the candidate's occupied composition, symmetry, source conditions, disorder, and interatomic geometry. Reject flagged or chemically incompatible records. If a plausible phase fits poorly, test a physically valid alternate record before rejecting the phase. Compare polymorphs under the same modest nuisance model and diagnostic reflections before texture or phase broadening; a candidate that wins only through extreme compensation is not identified.

After every phase addition, removal, source replacement, or analogue substitution, reconverge background, every phase scale, the chosen common angular correction, and cells before judging the residual. A one-pass scale test against a biased base is not decisive. Reinspect residual peak families and precursor/product mass balance; coherent unmatched peaks remain missing-phase evidence even when partly overlapped.

If a chemically plausible formula has no exact entry, search cross-chemistry prototypes rather than only its element-system key. The helper ranks records with the same reduced stoichiometric pattern:

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Optionally add an indexed `--space-group N` and `--cell a b c alpha beta gamma`. Inspect several top parents. Preserve the parent and document a chemically justified site substitution. Physical-screen the adapted model, then refine its scale, cell, and at most one supported width term in stages. Do not transfer case-specific coordinates or force a candidate whose scale, unique peaks, or geometry fail.

## Profile discipline

Establish a low-dimensional physical global profile before atomic, texture, or elaborate phase refinement. Choose zero versus specimen displacement from the angular dependence; avoid refining strongly correlated versions together. Constrain the analytic peak width to remain nonnegative over the full fitted range. Confirm that dominant peak widths are actually described; if not, expand identifiable global width terms one at a time before adding phase broadening.

Print and inspect every phase's saved HAP values and flags. A fixed GSAS-II value such as 1000 ppm microstrain is active broadening, not a neutral placeholder. Start unused strain at zero and size at a large value; after inventory, scales, and cells stabilize, release size or strain one phase at a time according to residual width patterns. Use anisotropic terms only for reproducible hkl-dependent evidence. Check bounds, frozen variables, correlations, geometry, and replayable project consistency after each stage; do not hard-reset all profile terms after a coupled fit.

Export CIFs, fractions, and `fit.csv` only from the final saved project and recheck their exact agreement.
