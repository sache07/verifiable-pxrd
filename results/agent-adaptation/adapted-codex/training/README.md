# Training evidence

This directory contains compact, normalized evidence for the public `adapted-codex`
capability and later judge-training experiments. The frozen capability itself lives under
`experiments/agent-adaptation/artifacts/adapted-codex/`.

- `pxrd-codex-baseline-50/`: one blind baseline attempt for every training problem,
  including complete chronological traces and submitted CIFs.
- `adapted-codex-r1-validation/`: one frozen-capability wave over all 20 baseline misses
  plus three prior successes selected before the wave.
- `adapted-codex-first-pass-50/`: one later adapted-Codex first pass for all 50 problems;
  these traces and submitted CIFs are the evidence used by the GEPA judge experiment.

Each bundle is indexed by `bundle.json`; per-problem evidence is under `attempts/<id>/`.
The bundles are compact public copies, not live runner directories, and intentionally omit
credentials, Codex state databases, and hidden references. Trainer analyses are retained in
`trainer-notes/`.
