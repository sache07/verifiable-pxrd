# Public inference contract

The released coding-agent condition is identical to pXRD-100: reduced composition plus
the corresponding fixedparams-v1 CSV. Reference CIFs, generation parents, novelty
metadata, topology labels, space groups, cells, and full-cell compositions remain outside
the agent workspace.

All 100 cases use the shared measurement profile in
`targets/fixedparams-v1/parameters.json`. The target manifest binds every input to the
top-level source manifest and records its SHA-256.

Primary evaluation uses symmetric, scale-disabled StructureMatcher exact recovery;
fixed-profile Rwp is secondary. See `../../docs/METHODS.md`. The generic runner stages
only blind inputs. The larger specialist-baseline target trees from the research
repository are not bundled in this initial public scaffold.
