# Method-specific refinement checks

## Start here

- **Completed results:** [CPU sweep](../../../results/appendix/native-refinement/released-export-20261109/README.md), including original/refined CIFs, per-candidate scores, failure logs, and exact runner snapshots.
- **Crystalyze / StructSnap:** [completed stage-one sweep](../../../results/appendix/native-refinement/crystalyze-stage1-20261110/README.md), with 1,600 saved first-stage outputs and a separately reported second-stage subset.
- **Rwp distributions:** [separate analysis](../profile-residuals/README.md) and [saved figures/data](../../../results/appendix/profile-residuals/README.md). These remain as-submitted distributions.

The key reporting choice is **original-candidate fallback on execution/export failure**. A completed but structurally incorrect refinement remains a miss. The CPU report separates matching refined outputs from matches retained through fallback; pass@8/20 uses the original candidate order, not Rwp ranking.

Rerun method-specific refinement on the **existing sampled CIFs**, without regenerating candidates or using reference structures during refinement. The September 2026 aggregate reports survived, but their complete runners and intermediate CIFs did not. This reconstruction is versioned separately; its outputs must not be presented as a bit-for-bit reproduction of those reports.

## Methods

| Method | Implementation | Limit per candidate |
| --- | --- | ---: |
| Crystalyze | Initial StructSnap schedule: cell lengths and peak width, then coordinates as well; stage-1-only continuation retains only the first stage. Up to 30,001 iterations per stage, native early stopping | 3,600 s, CUDA GPU |
| PXRDGen | Released two-pass GSAS-II example, with conventional-cell standardization between passes; 100 cycles per stage | 1,800 s |
| Ab-PXRD-Solver | Released staged GSAS-II routine; 20 cycles, native early-exit threshold 50 | 60 s |
| RealPXRD-Solver | Our implementation of the paper's refinement sequence: background, scale, profile, cell, zero, coordinates, joint fit | 900 s |

RealPXRD's adapter is not author-released refinement code. It uses a 0.1-degree Gaussian broadening of the native peak list, unit weights, fixed Uiso=0.01, and one fixed highest-Z atom to remove translational freedom. Steps are rejected if they worsen the freshly recalculated residual or violate the recorded geometric/profile bounds. See `gsas.py` for all bounds.

Inputs retain each framework's original measurement representation and conditioning. Crystalyze uses the unmasked 8,500-point target for StructSnap; its encoder-masked representation in the historical Rwp plots is different. StructSnap optimizes negative cosine similarity, not Rwp. No reference-derived cell, symmetry, profile parameters, match labels, or structures enter a worker.

### StructSnap stage-1 handoff (9 November 2026)

The initial GPU campaign ran only the first two stages of the released code,
not its full search over four alternative schedules (up to twelve stages).
Its second stage optimizes coordinates, whereas the paper describes lattice-only
optimization. Preserve these two-stage results as a separate diagnostic, not a
paper-faithful reproduction.

The continuation uses `structsnap_mode="lattice-stage1"`. It keeps the original
first-stage calculations and parameters, changing only the scheduler's
`finished` flag so that this intermediate is returned as the final output.
Cell lengths and W are optimized; fractional coordinates and lattice angles
are fixed during gradient updates. The preceding native symmetry operation is
unchanged. It is a single-schedule cell-length refinement, not the paper's
multi-schedule procedure or its Findsym-based symmetry treatment.

The saved handoff partitions the frozen original inputs into reserved old calls
and unreserved stage-1-only calls. The continuation shared the original budget
ledger, preserved account assignments and candidate ranks, and used separate
immutable runner snapshots.
Implementation controls rerun a saved first-stage result across the two accounts;
they are excluded from benchmark recovery counts. `verify_stage1_control.py`
checks structure, profile, and cosine agreement before the continuation is
released. `continue_sweep.py --validation PATH/passed.json` enforces this gate.
To pause a subsequent continuation safely, create `DRAIN_REQUESTED` in its
shard directory; the dispatcher stops reserving new work and collects all
submitted calls before exiting. This avoids interrupting the reserve/submit
transaction. Reconcile any reservation without a call ID against the remote
outputs before retrying it.

Evaluate `stage-1.cif` for every candidate, whether it came from the original
two-stage run or the continuation. Retain the original candidate-level outputs
and record the handoff. The old run's `paired_profile.after` describes stage 2,
so it must **not** be reused as a stage-1 Rwp value; stage-1 profiles must be
scored separately. StructSnap's native stage-1 cosine and profile arrays are
saved in `stages.json` and `stage-1-profile.npz`.

All 1,600 candidates have returned. `summarize_structsnap_stage1.py` combines the
disjoint campaigns, verifies input/output hashes, checks the original exact
labels, and scores `stage-1.cif`. It recalculates independent GSAS-II diagnostics
for all 200 first candidates in fresh CPU processes. Four stage-1-only controls
check agreement with the saved inline diagnostic. No refinement is rerun.

```bash
GSASII_PATH="$PWD/.runs/native-refinement/GSAS-II/GSASII" \
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MPLBACKEND=Agg \
.runs/native-refinement/scoring-env/bin/python \
  experiments/appendix/native-refinement/summarize_structsnap_stage1.py \
  --inputs .runs/native-refinement/full-20261109/input \
  --runs .runs/native-refinement/full-20261109/primary \
         .runs/native-refinement/full-20261109/secondary \
         .runs/native-refinement/structsnap-stage1-20261109/primary \
         .runs/native-refinement/structsnap-stage1-20261109/secondary \
  --output results/appendix/native-refinement/crystalyze-stage1-20261110 \
  --workers 4
```

The summary separates first-candidate profile statistics from all-candidate
native cosine statistics. Pass@8 retains the original eight-candidate grouping
and uses oracle structural coverage, not profile-based reranking. The tested
two-stage subset is recorded separately; it is never substituted for stage 1.

The published bundle can be checked locally without Modal or GSAS-II:

```bash
uv run python experiments/appendix/native-refinement/audit_bundle.py \
  results/appendix/native-refinement/crystalyze-stage1-20261110
uv run python experiments/appendix/native-refinement/summarize_structsnap_stage1.py \
  --inputs results/appendix/native-refinement/crystalyze-stage1-20261110/inputs \
  --runs results/appendix/native-refinement/crystalyze-stage1-20261110 \
  --output .runs/native-refinement/structsnap-structural-check \
  --structural-only --workers 4
```

The second command checks every saved input/stage CIF against its hash and
recomputes the before/after recovery counts. The raw-campaign command above
additionally regenerates the independent paired-profile diagnostics.

### Released-export CPU run (9 November 2026)

The primary CPU rerun uses `specialist-native-refinement-v3-released-export`.
PXRDGen executes its released refinement functions with unmodified GSAS-II
uncertainty-based CIF formatting. Ab uses the same formatting when saving the
fitted phase. Unreadable exports and symmetry-conversion failures are retained,
not repaired. The earlier precision-patched pilot remains a separate diagnostic.
RealPXRD is still our paper-guided adapter, not an author-code reproduction.
Crystalyze continues with the original frozen v2 GPU runner; no GPU settings or
calls were changed for this CPU rerun.

`refinement-stage.json`, exception records, and compressed worker/Ab logs identify
the failure point. `failure_report.py` separates full failures, rejected RealPXRD
stages, structural regressions, and failures of the independent Rwp diagnostic.
An exported structure that fails the matcher is a completed refinement, not an
execution failure. Recovery retains the original candidate on a full failure;
paired Rwp summaries include only successfully exported first candidates.

### Explicit adaptations

- Crystalyze: update an obsolete pymatgen import; save the best UVW values with the best structure. The released routine otherwise returns an unsaved width tensor. Preserve the native differentiable forward operations and effective symmetry tolerance; no `torch.compile` or CPU substitution. Use one candidate per batch to avoid cross-case optimizer coupling.
- Ab: export the fitted phase, rather than returning the input CIF path.
- PXRDGen: fix the second-pass file location. Extract only the released refinement functions, so the example's reference-CIF analysis never executes.
- PXRDGen and Ab: retain default GSAS CIF formatting in the primary v3 run. The v2 pilot used a 12-significant-digit export patch; those results must not be pooled with v3. Our RealPXRD implementation and independent Rwp diagnostic still use high-precision exports.

Upstream commits, file hashes, and instrument files are in `sources.lock.json` and `protocol.json`. The image checks the compiled GSAS-II binary hashes. Every result records the runtime packages, source hash, input/output hashes, stage diagnostics, and failures.

## Run

Each worker requests two physical CPU cores and 8 GiB RAM. CUDA workers prefer T4 and may fall back to L4. The pilot initially used two concurrent GPU workers; the remaining already-reserved jobs were allowed up to six to shorten queueing. Per-candidate resources and time limits were unchanged.

The released-export CPU sweep uses two account shards, initially 16 concurrent
workers per account, increased to 32 through the CPU function autoscaler. The
coordinators retain at most 32 outstanding CPU calls per account. Per-candidate
resources, timeouts, optimizer settings, and the shared $300 budget are unchanged.
The GPU functions were not changed by that autoscaler update.

From the repository root, using Python 3.11:

```bash
python experiments/appendix/native-refinement/fetch_sources.py
python experiments/appendix/native-refinement/prepare.py --pilot --output .runs/native-refinement/pilot
python -m modal run experiments/appendix/native-refinement/remote.py \
  --tasks .runs/native-refinement/pilot/tasks.json \
  --output .runs/native-refinement/pilot-results --campaign pilot-new
```

Install `modal==1.5.2` and configure your own Modal account. The image supplies the scientific dependencies. The PXRDGen Code Ocean download currently returns HTTP 403; if that persists, pass `--capsule-source /path/to/unpacked/PXRDGen` to `fetch_sources.py`. The fallback must match the published source hashes; arbitrary replacement code is rejected.

For a CPU-only full run, prepare with `--methods pxrdgen ab-pxrd-solver
realpxrd-solver` and omit `--pilot`. Run the sweep from a frozen copy of this
directory and set `NATIVE_REFINEMENT_SOURCES` to the absolute source-download
directory. This prevents subsequent report/documentation edits from changing
the worker image or its identity. The per-shard `runner/` snapshots and source
hashes are the authoritative implementation record.

The pilot selects four first-available parseable candidates per method and corpus, spaced across candidate site-count ranks. It does not use exact-match or fit scores. It is an implementation check, not an estimate of benchmark performance. The existing pilot excludes two unparsable PXRDGen first candidates (`pxrd100-challenge-012`, `pxrdood-tn-css-024`) before rank selection; a full run retains such failures.

For a cheap CUDA smoke test, add `--methods crystalyze --limit 1 --diagnostic-iterations 10`. For a synthetic self-target control, add `--self-target` and use a separate output directory. The native background subtraction also acts on synthetic targets, so processed self-target cosine similarity need not equal one. These diagnostic runs are not benchmark results.

The pilot's shared local budget ledger conservatively reserves resource cost before dispatch and records call IDs immediately. A fresh pilot ledger includes $5 for build overhead; reservations are estimates, not billing receipts. Failed jobs are not automatically retried. T4 is preferred, with L4 as an availability fallback. Full tasks additionally require `--allow-full` and prior spending approval. The ledger cannot constrain unrelated Modal applications.

To retrieve calls after a client interruption, without launching new computation:

```bash
python experiments/appendix/native-refinement/collect.py .runs/native-refinement/budget-ledger.json
```

### Full sweep across two Modal workspaces

Authenticate each account into a separate profile. `--no-activate` preserves the existing default; each sweep process selects its own profile explicitly. Never publish the credential file.

```bash
python -m modal token new --profile secondary --no-activate
python experiments/appendix/native-refinement/prepare.py --output .runs/native-refinement/full/input
python experiments/appendix/native-refinement/sweep.py \
  --tasks .runs/native-refinement/full/input/tasks.json \
  --output .runs/native-refinement/full/primary \
  --ledger .runs/native-refinement/full/budget-ledger.json \
  --profile PRIMARY_PROFILE --campaign native-full \
  --shard 0 --shards 2 --gpus 10 --cpus 4 --budget 300 --allow-full
```

Run a second process with `--profile secondary --shard 1` and a separate `--output`, retaining the **same input file, ledger, campaign, budget, and shard count**. These commands divide the frozen candidate order into disjoint shards. Each process runs CPU and GPU work concurrently. The 7,360 available inputs comprise 1,600 Crystalyze, 1,600 PXRDGen, 160 Ab-PXRD-Solver, and 4,000 RealPXRD-Solver candidates; 40 missing Ab originals remain recorded for evaluation.

`sweep.py` uses a separate version-2 ledger with $10 shared startup allowance. Before dispatch, it reserves the full candidate timeout at L4/CPU/RAM rates plus startup allowance and 25% margin. After collecting a result, it retains the observed runtime charge plus 20 seconds and 25% margin, releasing the unused hold. Both account processes take the same file lock, so they cannot independently spend the entire budget. Unresolved calls retain their full reservations. This is a resource-based spending guard, not a guaranteed invoice cap; account-level spending limits remain the billing safeguard.

Keep both local coordinator processes running. They launch detached Modal apps, preserve call IDs and per-shard source snapshots, and write `progress.json`. If a coordinator is interrupted, rerun **the identical command with unchanged source files** to reconnect to its submitted calls. Do not use the pilot's `collect.py` with the version-2 ledger. A reservation without a call ID is ambiguous and requires checking Modal before retrying. No failed candidate is automatically resubmitted. A budget pause leaves all collected results intact.

The November full sweep was authorized after a $50-capped pilot, with a $300 shared resource-budget target. The pilot's runtime projection was approximately 265 GPU-hours for Crystalyze, or 13.3 hours at 20 continuously occupied GPUs; this is not a guaranteed completion time. Account limits, GPU availability, and the long-runtime tail affect elapsed time.

To continue only selected methods of an existing campaign, stop its local
coordinator first, then use `continue_sweep.py --plan PATH/plan.json --tasks
PATH/input/tasks.json --sources PATH/sources --methods crystalyze`. This loads
the immutable runner snapshot, reconnects submitted calls (including other
methods), and submits new calls only for the named methods. It never cancels a
remote call. Its progress is recorded in `continued-progress.json`. Do not run
the original coordinator simultaneously. This handoff was used to drain the
superseded CPU queue while leaving Crystalyze running.

### Supervised continuation

A detached Modal app preserves submitted calls, **not the local dispatch loop**.
If the local coordinator exits, queued calls can finish while the rest of the
sweep remains unsubmitted. This occurred in the November run: 180 GPU results
were collected before the coordinators exited, and 40 more completed remotely.
All 220 outputs were retained for recovery; the remaining 1,380 had not started.

Use a process supervisor for unattended sweeps. `continue_sweep.py` supports
systemd readiness and watchdog notifications and holds a per-shard file lock
to prevent duplicate coordinators. Freeze this controller separately from the
already-frozen scientific runner. For example, run one user service per shard:

```bash
systemd-run --user --no-block --unit=pxrd-structsnap-primary \
  --property=Type=notify --property=NotifyAccess=main \
  --property=WatchdogSec=300 --property=TimeoutStartSec=600 \
  --property=Restart=on-failure --property=RestartSec=30 \
  --property='RestartPreventExitStatus=75 78' \
  --property=StartLimitIntervalSec=900 --property=StartLimitBurst=5 \
  /ABS/PYTHON -u /ABS/FROZEN/continue_sweep.py \
  --plan /ABS/primary/plan.json --tasks /ABS/input/tasks.json \
  --sources /ABS/sources --methods crystalyze --interleave-panels
systemctl --user status pxrd-structsnap-primary
```

Ensure the user service manager persists after logout (user lingering), or use
an equivalent system-level supervisor. A heartbeat is emitted every dispatch
loop iteration; systemd restarts crashed or unresponsive controllers. Exit 75
means the budget guard paused dispatch, and exit 78 means manual reconciliation
is needed; neither is automatically retried. Read `continued-progress.json` for
current counts, not the original coordinator's stale `progress.json`. Do not
edit the per-shard scientific runner snapshots.

`--interleave-panels` round-robins unsubmitted tasks across panels, ordering each
panel by original candidate slot and case identifier. It changes scheduling only;
input hashes, refinement settings, candidate ranks, account assignments, and
scoring remain unchanged. The supervised restart enabled this option so partial
coverage would no longer be confined to the challenge panel. Already submitted
calls are recovered by ID rather than resubmitted. Interleaving does not make
completion-conditioned interim results a random sample.

## Score and audit

Use the pinned scoring environment (pymatgen 2023.8.10, NumPy 1.26.4, SciPy 1.11.4, spglib 2.7.0):

```bash
python experiments/appendix/native-refinement/report.py \
  --inputs .runs/native-refinement/pilot --results .runs/native-refinement/pilot-results
python experiments/appendix/native-refinement/failure_report.py --results PATH/TO/SCORED/RESULTS
python -m pytest experiments/appendix/native-refinement/test_protocol.py
```

Only this local scoring step opens the reference CIFs. It reuses the repository's composition, validity, and bounded symmetric StructureMatcher evaluator. Candidate order is unchanged. Execution failures retain the original candidate; pending work is never counted as completed. Original missing submissions remain in the denominator. The full-run report aggregates the first 1, 8, and 20 original slots where available; the pilot contains only one candidate per selected case.

The paired Rwp diagnostic re-simulates both exported structures under the same observation-derived profile, fitting a nonnegative scale and four Chebyshev background coefficients. It is separate from the method's optimizer residual and from the **clean-reference fixedparams-v1** distributions in `experiments/appendix/profile-residuals`. Never combine these metrics in one unlabeled column. Structural refinement can improve profile fit while losing an exact match; report both outcomes and the paired sample count.

If an inline diagnostic fails after a GSAS numerical error, `recheck_profiles.py
--tasks PATH/input/tasks.json --runs PATH/primary PATH/secondary --workers 4`
recalculates the residual in a fresh local process using the pinned GSAS/Python
environment. Set `GSASII_PATH` to the pinned checkout's `GSASII` directory.
This never reruns refinement or changes a CIF. Original result/error records are
preserved; `profile-recheck.json`, `rechecked-profiles.npz`, and its log record
the separate calculation. The scorer uses a successful recheck only when the
inline residual is absent, and records `profile_source` in `scores.csv`.
Metadata-selected successful controls must agree within 1e-6 percentage points.

Keep compact CIFs, result/stage JSON, paired profile arrays, and compressed worker logs in the public result bundle. GSAS project/checkpoint files and downloaded third-party source trees remain in `.runs/` or the Modal Volume. Retain the original as-submitted distributions separately from any later post-refinement analysis.
