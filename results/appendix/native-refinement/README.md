# Method-specific refinement results

[`released-export-20261109`](released-export-20261109/README.md) contains the full
PXRDGen, Ab-PXRD-Solver, and RealPXRD-adapter CPU sweep, with default GSAS export
formatting for the released PXRDGen/Ab routines. Its tables separate execution
failures, successful refined matches, and matches retained through the original
candidate fallback. [Crystalyze's completed stage-one sweep](crystalyze-stage1-20261110/README.md)
contains all 1,600 candidates, original/stage CIFs, scores, and both frozen runners.
Its 1,067-candidate second-stage diagnostic remains separate from the stage-one result.

The [Rwp distributions](../profile-residuals/README.md) remain a
separate as-submitted analysis.

## Earlier pilot

The `pilot-20261109` bundle contains four candidate-size-spaced cases per corpus for each method (eight per method). Selection used candidate site counts, not success labels or residuals. These are implementation checks, not full-benchmark results.

The pilot used a high-precision GSAS export patch. It is preserved as a separate
diagnostic and must not be pooled with the released-export CPU sweep.

Reproduction instructions: `experiments/appendix/native-refinement/README.md`.

The bundle retains original/refined CIFs, stage diagnostics, paired profile arrays, compressed logs, runtime/source hashes, local scoring inputs, and the exact worker source snapshots. Large GSAS project files remain outside the repository. No case is omitted because refinement failed or lost an exact match.

`code_sha256` identifies the actual worker source. Some early pilot records have a different launcher-side `source_code_sha256`: the launcher was edited while its image was building. The actual image source was recovered and hash-verified into `runners/`. The current launcher freezes its source fingerprint before building and rejects any worker/image mismatch. This preserves the pilot's provenance without pretending it ran a later revision.

Rwp columns in this experiment use freshly simulated exported CIFs against the native observation, with an identical fixed profile and fitted scale/background before and after. The appendix's clean-reference fixedparams-v1 distributions remain separately archived in `results/appendix/profile-residuals`.

RealPXRD-Solver uses our paper-guided adapter, not a released author implementation. See the protocol and runner documentation for its additional bounds and rollback rules.
