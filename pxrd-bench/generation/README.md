# Benchmark generation

The committed corpora are immutable, hash-bound artifacts. The scripts here are the
scientific builders used to create and audit them:

- `build_pxrd_100.py`: deterministic pXRD-100 selection and audit;
- `index_pxrd_ood_sources.py`, `build_pxrd_ood.py`, and `relax_pxrd_ood.py`:
  novelty indexing, generation, certification, and relaxation for pXRD-ood;
- `build_ab_pxrd_solver_targets.py`: the fixedparams-v1 GSAS-II simulation recipe;
- `make_panel.py`: a small path-independent utility for making runnable subsets of
  the two locked corpora.

The full builders intentionally retain their original source locks and strict audit
requirements. The exact pXRD-ood Python lock is retained as
`runtime/pxrd-ood-uv.lock`. Rebuilding pXRD-ood also requires the large frozen exposure
index and model artifacts named in its source lock; those inputs are not bundled here.
DICVOL is not used to create the benchmark.

The fixedparams-v1 diffraction inputs use a separate, locked GSAS-II runtime from the
one exposed to evaluated agents. Its exact Linux package lock, source revisions, and
replay record are under `pxrd-bench/generation/runtime/`; do not substitute the agent
runtime when auditing pattern bytes.

Audit the committed corpora with `uv run vpbench validate-benchmark`. Create a
deterministic 20-case panel with:

```bash
uv run python pxrd-bench/generation/make_panel.py \
  --size 20 --seed 7 --output pxrd-bench/panels/sample-20.json
```

With the pattern-generation runtime installed, replay either corpus with:

```bash
"$VPBENCH_PATTERN_PYTHON" pxrd-bench/generation/build_ab_pxrd_solver_targets.py \
  audit-fixedparams --corpus-root pxrd-bench/pXRD-100 \
  --dataset-id pXRD-100 --case-prefix pxrd100 --expected-cases 100 \
  --upstream-root "$VPBENCH_AB_PXRD_SOLVER" \
  --gsasii-dir "$VPBENCH_PATTERN_GSASII" --workers 3
```
