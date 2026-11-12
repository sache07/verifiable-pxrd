# Working commands

Run commands from this folder (`evolve/`) with `python` (the configured materials-science environment). `python lab.py --help` lists the controller requests. It works through a file queue, so your command network remains blocked. Requests return immediately. `python lab.py wait ID --seconds N` waits up to N seconds (at most 1800) for a worker, run group, or request to finish; a run request waits on its workers, not just acceptance. Each check costs a model turn, so when nothing else is worth doing, wait in one long call rather than many short polls. `python lab.py response REQUEST_ID` reads only the acknowledgement. Unknown IDs return an error rather than a misleading pending status. Read `../evidence/STATUS.md` and `../evidence/status.json` for experiment progress. Reuse IDs when checking progress; do not invent a replacement launch.

A separate Sol process monitor checks recent training progress every 30 minutes and normally stays silent. An occasional advisory is printed once by `lab.py`, separately from its JSON output; review decisions are in `../evidence/monitor/`. It checks the scheduled development-cycle checkpoint as well as scientific drift. It cannot change packages, scores, or jobs, and does not run while dispatch is paused.

Scientific tools: pymatgen, scipy, numpy, spglib, ASE, pyxtal, matplotlib; `dicvol14`; and GSAS-II through `$GSAS2_PYTHON`. Resource paths and the frozen index hash are in resources.json. CIF 1234567 is under `1/23/45/1234567.cif`. No DARA solver or hidden structure libraries are supplied.

## Rules

- Use the frozen filtered COD 2024 in resources.json and select sources yourself. ICSD, live COD, historical packages, prior diagnoses and experimental evaluation data are unavailable. Construct chemical-system keys with `"-".join(sorted(set(elements)))`.
- Published structures, justified repairs, analogue substitutions and modest physical perturbations are allowed. Record provenance and transformations; inspect symmetry, occupied composition, geometry and relevant source conditions. Keep the parent available for reference-adjustment cases. Repair flagged sources with evidence or mark them diagnostic-only; synthetic validity does not establish experimental stability.
- Use the supplied generator with LAB.md's settings. Do not treat simulator settings as known properties of future samples or change physics to improve scores.
- The score is profile-primary: 60% profile agreement, 1/(1+D) with D the deviation of the verified `final.gpx` replay from the hidden noise-free pattern, plus 40% structural agreement (phase recovery, fractions and scattering-weighted site precision), gated by physical validity. A solution is good when its predicted pattern matches the data to the noise floor and every structure is physically valid. Interpret both components alongside the independent Rwp from the same replay, without refinement or calibration substitution.
- Preserve every case and result. Freeze new batches and the incumbent before their transfer runs; learning from those results makes them training data. Report any outcome-selected supplementary cases separately from the original prospective comparison. Experimental evaluation remains outside this task.

## Curate and freeze

Create `drafts/b001/sources.json`: `{"schema_version":1,"records":[...]}`. Each source record needs `id`, `cif_path`, `provenance`, `model_basis` (`published`, `repaired`, `analogue_derived`, or `perturbed`), and `lineage_group`. Nonpublished models also require `parent_ids` and `transformation`. Paths resolve relative to sources.json; source COD paths may be absolute. Inspect the source code for additional fields and exact validation.

```
python ../runtime/register_models.py drafts/b001/sources.json --out drafts/b001/pool
```

Create `drafts/b001/manifest.json` with `schema_version: 1`, `source_pool_sha256` (pool/catalog.json), `lab_sha256` (LAB.md), and `cases`. A recipe has:
- an opaque globally unique `id` (e.g. b001-c01) and a `rationale`;
- `phases: [{"id":"pool-model-id","weight_fraction":0.6}, ...]`, with fractions summing to one;
- `availability`: `"full"`; `"withhold_principal_composition"` with `principal_id` (hides every library entry with that phase's exact composition, so all its polymorphs); or `"withhold_ids"` with `withhold_ids: ["1520641", ...]`, an explicit list of COD record IDs to hide (the product's own entry plus whichever analogues you choose);
- `sample`: the solver-visible sample description, with exactly the fields LAB.md's `solver_inputs.sample_fields` defines;
- `peak_counts` (one of LAB.md's `measurement.peak_counts`), `domain_size_um` (one of LAB.md's `specimen.control_size_um`), integer `seed`, and a private `measurement_session` string shared by scans from the same simulated session;
- optional `background_family: "auto"|"simple"|"exponential"|"power_law"` (omit for automatic sampling), `angular_offset_control: true` and `specimen_control: true`.

The stated sample is what the solver is told, so choose an inventory plausible for it. Every element in a phase must come from the sample fields LAB.md names as element sources, or be one of its ambient elements; if LAB.md asks, every source element must also appear in some phase. Do not state conditions the lab's metadata does not report. Withholding removes entries from the solver's copy of the library; the solver is never told what is missing. Its difficulty is set by the nearest entry that remains, not by what was removed. List a model's analogues with

```
python ../runtime/library_neighbours.py drafts/b001/pool/models/MODEL.cif [--withhold ID,ID] --out drafts/b001/neighbours-MODEL.json
```

It compares every library entry with the same number of atoms and the same anion count per formula to the model with pymatgen's structure matcher, lattice scaled and element identities ignored, so relatives are found by atomic arrangement rather than formula pattern (an ordered A2BB'O6 perovskite is a relative of A3BO6; a tellurate or sulfate is a relative of the corresponding tungstate). For each matching framework it maps sites onto the model's and reports the distinct element `substitutions`, a `tier` (0 same composition, a polymorph or other setting; 1 one substitution; 2 two substitutions), the normalized `framework_rms`, and `cell_mismatch_percent`, the lattice difference a solver adapting that relative must refine across. Entries that match only after more than two substitutions, or whose framework does not match, are reported as counts, not tiers. Run it with `--withhold` listing the IDs the recipe hides: `surviving_tier` and `nearest_survivor` are then the case's actual difficulty, and that is the tier to record in the case rationale and the batch review. Withholding more than the hidden phase's own records raises the surviving tier; a panel that uses this for a harder adaptation case keeps an easier one beside it. Never list an entry that another phase of the case was registered from; the generator refuses it. Constructed models may also be naturally absent.

Every property of the simulated laboratory comes from the settings block in LAB.md, which is frozen. The hidden instrument profile is drawn once per `measurement_session`; case seeds drive the specimen, angular offset, background and noise. Each specimen may receive a displacement (sample height; GSAS-II Bragg-Brentano `Shift` at LAB.md's goniometer radius) and a low-angle intensity deficit (GSAS-II `SurfRoughA`/`SurfRoughB`); each phase may receive its own crystallite size, isotropic or uniaxial microstrain, March-Dollase texture and Uiso. Each is drawn privately from a seeded stream with LAB.md's distribution and probability. Each phase's true structure also differs from its registered model by LAB.md's `reference_mismatch`, a symmetry-preserving cell strain and coordinate displacement, as a sample's phases differ from their published refinements; the solver's database keeps the registered parent. `angular_offset_control: true` gives a zero-offset control and `specimen_control: true` removes every specimen effect (common recipe size, registration Uiso) but keeps the reference mismatch, with identical public information. The recipe's `domain_size_um` is the common size used by a specimen control or when phase-specific sizing is off. Background shape and counts are sampled automatically; do not supply `background_counts`, and use a family override only when a diagnostic needs it. Realizations stay private: generation audits use them, solver scoring never does. Do not expose session IDs or realizations in public metadata. Registered source CIFs remain unchanged.

Solver inputs have the same form as the lab's experimental scans: `pattern.csv` with LAB.md's column names and `metadata.json` built from LAB.md's template, holding the stated sample and the reported instrument header. There is no instrument file, and nothing beyond what that template contains.

For a larger deliberate reference-adjustment problem, prepare a candidate source with:

```
python ../runtime/perturb_model.py PARENT.cif drafts/b001/variant.cif --seed 123 --cell-strain 0.003 --position-rms 0.02
```

The helper preserves detected symmetry, occupied composition, and special positions, and requires a passing physical screen. Its adjacent provenance JSON records the operation. Review chemical plausibility yourself; this is parameter-recovery data, not evidence of a stable new compound. Register it as `model_basis: "perturbed"` with parent IDs and the transformation. Keep the original database parent available when the intended challenge is refinement.

```
python ../runtime/generate.py drafts/b001/manifest.json --pool drafts/b001/pool --lab LAB.md --out drafts/b001/preview --cache .cache/forward
python lab.py freeze-batch --id freeze-b001 --batch b001 --manifest drafts/b001/manifest.json --pool drafts/b001/pool --notes drafts/b001/review.md
python lab.py wait freeze-b001
python lab.py run --id b001-p0 --batch b001 --policies P0 --repeats 3 --purpose baseline
```

The controller regenerates the cases and checks them independently. Frozen cases are in `../cases/`, batch notes and audits in `../batches/`. Flagged source models may be frozen with `--kind diagnostic`; their results must remain diagnostic. Do not hide these flags. Use new IDs for changed recipes or packages. Small diagnostic variants use this same generation interface; no separate investigator is needed.

Supplement an already frozen batch under a new batch ID containing only the additional cases, then include both batches in subsequent learning comparisons. Existing cases stay frozen. The optional generator `--finalize` check accepts six or more cases; omit it for a smaller supplement or diagnostic batch.

## Package and test

Create `packages/v1/guidance.md`, optional `helpers/` (delivered to workers as `learned/`), and, only if part of the learned change, TOOLS.md, AGENTS.md or OUTPUT_SCHEMA.md. Put development notes outside that directory. P0 and its output requirements remain fixed; no checker or extra scientific guidance is automatically added to P0. Helpers must be reusable from solver-available inputs; do not bundle reference CIFs, fitted answers, private paths, or case lookup rules. When the baseline includes a folder of its own (`../policies/P0/helpers/`, described in P0.md), every solver receives it read-only under `learned/` and the package's helpers are laid on top; a package helper cannot reuse one of its top-level names.

The controller enforces 600 additional guidance words across `guidance.md`, `TOOLS.md`, `AGENTS.md`, and `OUTPUT_SCHEMA.md`, counted as whitespace-separated words including headings and examples. P0 and executable helpers are excluded. Optional on-demand helper documentation may live under `helpers/`; do not move required instructions there to evade the cap. The frozen package records its word counts. Keep research notes and exploratory code outside the shipped package.

Every solver condition must save its final GSAS-II project as `final.gpx`, consistent with its submitted CIFs, fractions and `fit.csv`. This is a shared P0 output requirement, inherited by packages.

```
python lab.py freeze-package --id freeze-v1 --package v1 --path packages/v1 --notes investigations/v1-review.md
python lab.py run --id b001-v1 --batch b001 --policies v1 --repeats 1 --purpose development
python lab.py status
python lab.py promote --id choose-v1 --package v1 --notes investigations/v1-decision.md
```

The full score, independently replayed curve, launch record, event trajectory, scientific workspace (including `.tmp`), and artifact hashes appear under `../evidence/attempts/ATTEMPT_ID/`. Solver IDs and conditions are listed in status.json. Read the actual scorer at `../scorer/src/score.py`, `structural_precision.py`, `structural_registration.py`, `structural_inventory.py`, `replay.py`, `predictive.py`, and `../scorer/runtime/replay_worker.py`. All source/configuration is read-only. Profile diagnostics use the saved `final.gpx` model, verified against the submitted CIFs and fractions, with no evaluator fitting or calibration substitution. The original observed grid and common weights determine Rwp; the frozen prediction then determines D against the hidden expected signal (smaller is better). `fit.csv` and reported scalar Rwp are separate diagnostics. A project containing multiple matching histograms can identify the final one with `refinement_histogram` in result.json. An evaluator failure is null, not a solver zero; provisional scores are marked.

Scorer 7.0.1 is profile-primary: score = 100 × (0.6 × 1/(1+D) + 0.4 × structural/100), zero on a hard physical failure. D is the mean Poisson deviance per bin of the verified `final.gpx` replay against the hidden noise-free pattern (D = 1 is about one noise standard deviation per point and earns half profile credit); fitting noise cannot lower it. Without a verified, consistent project the profile term is zero. A provisional score (†) flags a physical or profile review that nothing adjudicates; STATUS.md means include provisional scores, with the mean without them beside it. The structural term credits phase recovery, abundance, fraction accuracy and site agreement weighted by scattering power (Z × count), so atoms the pattern barely sees carry little credit; cell error is reported but not credited, because the profile term already measures it. Phase assignment maximizes total credited agreement. Unfinished registration returns bounds and a review status; it is not a scientific failure. Ordinary CIF rounding is handled by the replay verifier. Compare results evaluated under the same frozen version.

## Investigate

For direct numerical investigations, copy the relevant workspace into investigations/, perform calculations with permitted tools, and optionally request independent scoring:

```
python lab.py score-investigation --id direct-check-01 --case b001-c01 --path investigations/direct-check-01
```

These scores are labelled researcher diagnostics with oracle access, excluded from fresh-rollout comparisons. Use this controller request for verified scoring; directly invoking the replay sandbox inside the research sandbox is unsupported. Never execute copied scripts blindly: rebase old paths into your investigation directory and inspect what they do.

To test a procedure across saved solver projects, write it as a script `SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR` (a copy of the attempt's final.gpx, where to save the result, and the case's public inputs). It runs under GSAS-II's own Python, which has numpy, scipy and GSAS-II but not pymatgen; in a solver's workspace that interpreter is `$GSAS2_PYTHON`. Request:

```
python lab.py procedure-test --id ptest-01 --script investigations/ptest-01/procedure.py
```

By default the newest completed attempts with verified projects are used, up to the cap in settings.json, except cases whose prospective comparison is unfinished; `--cases` or `--attempts` narrows the set. The controller runs the script on each copy in parallel in the evaluator's sandbox (GSAS-II, sibling `.py` files importable, no network), replays every output with the frozen scorer, and writes D, independent Rwp, phase fractions, physical screens and logs before and after under `../evidence/procedure-tests/ID/`. `lab.py wait ID` follows it and `lab.py cancel-test --test ID` stops it. One test runs at a time; settings.json gives the workers, the per-project time limit and the attempt cap. Like `score-investigation`, these are diagnostics scored against hidden truth: they rank and screen procedures and do not validate a rule. The same script can ship in a package as a helper that solvers run with `$GSAS2_PYTHON learned/SCRIPT final.gpx refined.gpx inputs`; the solver must then re-export its CIFs, fractions and fit.csv from the refined project, because scoring requires them to agree with final.gpx.

## New batches and persistence

Freeze a new batch with `--kind transfer --incumbent v1`. Its first solve request must contain all cases and at least three fresh attempts under each of P0 and that frozen incumbent:

```
python lab.py run --id b002-transfer --batch b002 --policies P0 v1 --repeats 3 --purpose transfer
```

After the full recorded comparison finishes, use the results for learning. The controller blocks new-case development runs and scored investigations until every comparison slot is complete and collected; earlier-case investigations may continue. If the selected incumbent remains P0, freeze with `--kind transfer --incumbent P0` and run `--policies P0 --repeats 3 --purpose transfer`; this produces a baseline-only new-batch assessment, not a learned-transfer claim. Additional package tests on those cases are development tests. Include older cases through separate explicit run requests; the controller does not choose the regression sample for you.

Each development cycle, from one completed next-batch comparison to the next, has 30 package solves (`development_solves_per_cycle`). Every non-P0 solve counts when it is queued, except in the prospective comparison and the 2nd and 3rd solve of a package on a case under `--purpose evaluation`, the 3-rollout evaluation:

```
python lab.py run --id b001-v3-eval --batch b001 --policies v3 --repeats 2 --purpose evaluation
```

Once the budget is spent, development solves wait for the next-batch comparison. One package may then be completed to three solves on each case run in this cycle with `--purpose evaluation`, uncounted, including cases it has not yet run on. P0 runs and investigations remain available. `status.json` exposes `development_cycle` to you and the monitor. A comparison closes the cycle only when every scheduled slot has completed and its evidence has been collected; interruption recovery retains the original slots. There is no total budget across cycles.

There are at most sixteen concurrent EC2 solver jobs, each Sol/max, two CPU cores and 5 GiB RAM; this is scheduling capacity, not a rollout budget. Jobs launch one at a time in each run group's schedule order: every case and condition once before any repeat. A launch the service rejects for capacity is retried automatically at the head of the queue every minute, replacing its slot. A worker is stopped after four hours (`solver_timeout_seconds`) and scored on what it saved. The app researcher is Sol/max. The same model family is used throughout.

`python lab.py pause` stops new dispatch while running jobs finish. `python lab.py resume` clears a dispatch pause after the cause is resolved; it does not rerun interrupted work. For an interrupted worker, use `python lab.py recover --id recover-01 --parent ATTEMPT_ID`. The controller first checks that its scientific process ended. It resumes preserved history, or permits a fresh transport retry only if no scientific action occurred. The recovered run replaces that interrupted slot, not a new independent replicate. If scoring itself failed (`evaluator_error`), `python lab.py rescore --id rescore-01 --attempt ATTEMPT_ID` scores the unchanged attempt again. Missing history or an integrity failure requires infrastructure repair. Keep STATE.md current; app/session interruption is not an experiment reset. The broker never autonomously selects a research idea or calls another reflector.

Capacity-limited workers remain queued: the controller retries the rejected launch at the head of the queue once per minute, preserving its replicate and saved history; wait on the original run-group ID rather than submitting replacements.
