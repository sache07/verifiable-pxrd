# Agent adaptation

This directory contains full-benchmark results for four evaluation conditions. Each
condition uses the 100-case pXRD-100 and 100-case pXRD-ood corpora and the same
StructureMatcher evaluator:

1. `llm/`: direct language-model inference without a coding harness;
2. `matsci-codex/`: Codex with ordinary scientific Python and local COD;
3. `pxrd-codex/`: the same Codex agent plus native GSAS-II and DICVOL14;
4. `adapted-codex/`: `pxrd-codex` plus the frozen learned capability package.

Archived source metadata retains the original run and condition identifiers. The
directory and condition-file names above are used in the reported analyses.
