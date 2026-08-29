# Learn a minimal pXRD capability

Use `$train-pxrd-capability` with `experiments/agent-adaptation/harness.toml`.

The goal is building a portable capability pack through access to training problems and their
solution verifier that improves performance over `pxrd-codex` on held-out problems. selected_exact is the
primary metric of success, with candidates_exact as secondary coverage evidence.

First obtain one blind `pxrd-codex` baseline attempt for every ordered training problem. Reuse
complete, valid imported attempts and run only the missing problems. Meticulously analyze the complete set of
successes and failures considering the below specifications before changing the active package.

The full baseline review is the package-design phase. Implement the complete minimal package supported by
that evidence in the first committed revision. Its allowed trainee-facing surface is:

- one `SKILL.md` containing only a few task/output-contract notes that repeatedly help behavior line up
  better with the declared verifier, less than 100-200 words; and
- optional executables under `bin/` that address load-bearing interface issues with software already present
  in the scientific environment. Agents should be able to effectively use and produce valid native inputs
  for every supplied program. Minor, consistently overcome-able friction does not warrant a tool.

The skill must not prescribe a solve workflow, crystallographic gates, hypothesis ledgers, search order,
or branch-selection policy. The skill may neutrally name available executables, but must not recommend,
route to, or prescribe when to use them, as that may imply an expected workflow. Detailed case diagnoses remain trainer-only.

For each miss, distinguish three layers: what structural family the trainee inferred,
which concrete element-specific periodic realizations it actually instantiated, and which artifacts
it declared for verification. Synthesize recurring gaps across chemically distinct problems—especially
where the scientific interpretation was reasonable but submitted structure did not pass the verifier—and
contrast them with successes that crossed the same gap. Use selective trainee reflection only when the trace
does not explain the representation choice.

Each executable must be a neutral adapter with a clear `--help` contract: accept explicit user
choices, invoke an existing backend reliably, retain provenance and native outputs, expose all
results without scientific ranking, and fail transparently. Do not add a tool merely because the
backend has the feature. When repeated attempts fail at a supplied backend’s interface, treat the
missing translation as a candidate adapter. When that need is supported, investigate the installed
backend and retained attempts, use controlled probes to reconstruct, reverse-engineer, and validate
its interface. Keep tests and trainer notes outside the trainee-facing capability directory.

After the first shape-defining revision, use 1-3 blind rerun waves on the motivating failures and some prior
successes needed to probe regression. The first rerun wave should include all the failures. These waves test whether
the package is usable and changes behavior as predicted; they are not a campaign to force every training case to pass.
Repair or remove broken or intrusive additions, then freeze one clean final revision for held-out evaluation. Do not
add further scientific advice in response to isolated hard misses. Cut off long-running reruns if they are no longer
informative and holding up your development progress.
