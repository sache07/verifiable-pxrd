# Baseline results

These are normalized, auditable bundles for the non-agent comparison methods in
the paper. Every reported run provides a common `run.json`, case index, candidate
index, and checksum manifest. Each condition exposes generated CIFs and verifier
outcomes under `candidates/<case-id>/`; compressed archives retain the untouched
execution shards as secondary provenance.

| Framework | Corpus | Condition | Exact@1 | Exact@reported-k | CIFs | Raw archive |
| --- | --- | --- | ---: | ---: | ---: | --- |
| [Crystalyze](crystalyze/pxrd-100/element-set-k8/) | pXRD-100 | element-set conditioning | 11/100 | 19/100 | 800 | included |
| [Crystalyze](crystalyze/pxrd-ood/element-set-k8/) | pXRD-ood | element-set conditioning | 2/100 | 6/100 | 800 | included |
| [deCIFer](decifer/pxrd-100/reduced-composition-k8/) | pXRD-100 | reduced-composition conditioning | 0/100 | 2/100 | 624 | included |
| [deCIFer](decifer/pxrd-ood/reduced-composition-k8/) | pXRD-ood | reduced-composition conditioning | 0/100 | 1/100 | 595 | included |
| [deCIFer](decifer/pxrd-100/known-conventional-z-k8/) | pXRD-100 | known conventional-cell Z | 18/100 | 32/100 | 788 | included |
| [deCIFer](decifer/pxrd-ood/known-conventional-z-k8/) | pXRD-ood | known conventional-cell Z | 9/100 | 12/100 | 771 | included |
| [PXRDGen](pxrdgen/pxrd-100/known-primitive-z-k8/) | pXRD-100 | known primitive-cell Z | 47/100 | 84/100 | 800 | included |
| [PXRDGen](pxrdgen/pxrd-ood/known-primitive-z-k8/) | pXRD-ood | known primitive-cell Z | 17/100 | 26/100 | 800 | included |
| [DiffractGPT](diffractgpt/pxrd-100/reduced-composition-greedy-k1/) | pXRD-100 | single greedy decode | 9/100 | 9/100 | 0 | withheld |
| [DiffractGPT](diffractgpt/pxrd-ood/reduced-composition-greedy-k1/) | pXRD-ood | single greedy decode | 6/100 | 6/100 | 0 | withheld |
| [Ab-PXRD-Solver](ab-pxrd-solver/pxrd-100/reduced-composition-k1/) | pXRD-100 | reduced-composition solver | 42/100 | 42/100 | 77 | included |
| [Ab-PXRD-Solver](ab-pxrd-solver/pxrd-ood/reduced-composition-k1/) | pXRD-ood | reduced-composition solver | 20/100 | 20/100 | 83 | included |
| [RealPXRD-Solver](realpxrd-solver/pxrd-100/known-primitive-z-k20/) | pXRD-100 | known primitive-cell Z | 41/100 | 62/100 | 2000 | included |
| [RealPXRD-Solver](realpxrd-solver/pxrd-ood/known-primitive-z-k20/) | pXRD-ood | known primitive-cell Z | 20/100 | 28/100 | 2000 | included |
RealPXRD-Solver retains 20 generated candidates per case, while the paper reports
the common first/best-eight cutoff. Both values are explicit in its `cases.csv` and
`run.json`. DiffractGPT candidate files are withheld pending redistribution-license
clarification; their identities and evaluation outcomes remain indexed.

This directory is the canonical framework-by-framework evidence surface.
