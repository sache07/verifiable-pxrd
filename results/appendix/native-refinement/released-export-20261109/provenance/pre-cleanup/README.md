# Released-export CPU refinement results

The three CPU experiments refine existing generated candidates; no candidate generation is rerun. PXRDGen uses the released two-pass functions and default GSAS-II CIF formatting. Ab uses its released optimizer, with a fitted-phase export added using default GSAS formatting. RealPXRD-Solver uses our paper-guided GSAS-II adapter, not author-released refinement code. Reference structures are available only to the local scorer.

Crystalyze is a separate GPU campaign and is not included here. The precision-patched pilot and superseded partial CPU campaign are preserved separately and are not pooled into these results.

## Structural recovery

Entries are before → after refinement, out of 100 problems per corpus. Candidate order is unchanged. A full execution/export failure retains the original candidate; a completed refinement is retained even when it loses a structural match. Missing original submissions remain misses. Pass@8/20 denotes any matching candidate among those original slots, not Rwp-ranked selection.

| Method | Corpus | Pass@1 | Pass@8 | Pass@20 | Completed / available candidates | Missing originals |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| PXRDGen | pxrd-100 | 47 → 32 | 84 → 67 | — | 646 / 800 | 0 |
| PXRDGen | pxrd-ood | 17 → 6 | 26 → 17 | — | 579 / 800 | 0 |
| Ab-PXRD-Solver | pxrd-100 | 42 → 41 | — | — | 76 / 77 | 23 |
| Ab-PXRD-Solver | pxrd-ood | 20 → 23 | — | — | 83 / 83 | 17 |
| RealPXRD-Solver adapter | pxrd-100 | 41 → 29 | 62 → 62 | 65 → 64 | 1997 / 2000 | 0 |
| RealPXRD-Solver adapter | pxrd-ood | 20 → 18 | 28 → 27 | 35 → 33 | 1978 / 2000 | 0 |

### Matches from refined outputs versus failure fallback

These counts also use all 100 problems per corpus as the denominator. They distinguish a matching refined first candidate from a match retained only because refinement failed.

| Method | Corpus | Matching refined first candidates | Additional matches from original fallback |
| --- | --- | ---: | ---: |
| PXRDGen | pxrd-100 | 23 | 9 |
| PXRDGen | pxrd-ood | 4 | 2 |
| Ab-PXRD-Solver | pxrd-100 | 41 | 0 |
| Ab-PXRD-Solver | pxrd-ood | 23 | 0 |
| RealPXRD-Solver adapter | pxrd-100 | 29 | 0 |
| RealPXRD-Solver adapter | pxrd-ood | 18 | 0 |

## Execution failures

Failure types below are candidate-level counts. `failures.csv` preserves the exact candidate ID, pipeline stage, and exception; the compressed logs retain the underlying messages. Unreadable exported CIFs are reported as failures rather than repaired by changing export precision.

| Method | Corpus | Failure type | Candidates |
| --- | --- | --- | ---: |
| Ab-PXRD-Solver | pxrd-100 | unreadable-refined-cif | 1 |
| PXRDGen | pxrd-100 | cif-import-error | 11 |
| PXRDGen | pxrd-100 | export-composition-change | 1 |
| PXRDGen | pxrd-100 | inter-pass-symmetry-conversion | 42 |
| PXRDGen | pxrd-100 | unreadable-refined-cif | 100 |
| PXRDGen | pxrd-ood | cif-import-error | 2 |
| PXRDGen | pxrd-ood | inter-pass-symmetry-conversion | 45 |
| PXRDGen | pxrd-ood | numerical-refinement-error | 1 |
| PXRDGen | pxrd-ood | unreadable-refined-cif | 173 |
| RealPXRD-Solver adapter | pxrd-100 | cif-import-error | 3 |
| RealPXRD-Solver adapter | pxrd-ood | cif-import-error | 21 |
| RealPXRD-Solver adapter | pxrd-ood | no-reflections-in-observation-range | 1 |

RealPXRD stage rejections are different from full failures: the adapter restores the last accepted state and attempts later stages. Their counts and exception messages are in `failure-summary.json`. Failure of the independent profile diagnostic also does not erase an otherwise completed refinement.

## Paired profile agreement

The same successfully refined first candidates contribute before and after. Here n is the number of such candidates with both residuals available. Each exported CIF is simulated against its method-specific observation under an identical fixed profile, fitting only nonnegative scale and four Chebyshev background coefficients with unit weights. This independently recomputed Rwp is not the optimizer-reported residual or the clean-reference fixedparams-v1 metric. Absolute values are not comparable across methods.

| Method | Corpus | n | Mean Rwp (%) | Median Rwp (%) |
| --- | --- | ---: | ---: | ---: |
| Ab-PXRD-Solver | pxrd-100 | 76 | 41.47 → 30.50 | 36.54 → 17.70 |
| Ab-PXRD-Solver | pxrd-ood | 83 | 54.66 → 46.12 | 53.08 → 30.67 |
| PXRDGen | pxrd-100 | 76 | 89.47 → 51.10 | 93.79 → 51.60 |
| PXRDGen | pxrd-ood | 71 | 93.10 → 82.10 | 96.17 → 92.09 |
| RealPXRD-Solver adapter | pxrd-100 | 100 | 94.71 → 85.52 | 97.68 → 96.34 |
| RealPXRD-Solver adapter | pxrd-ood | 99 | 96.98 → 94.02 | 98.06 → 98.04 |

Some inline profile diagnostics failed after numerical errors during refinement. Their residuals were recalculated from the unchanged input/output CIFs in fresh processes. The original errors remain in `result.json`; separate `profile-recheck.json` records identify the recalculations and their code/package versions. Successful-diagnostic controls check agreement with the inline calculation. No optimizer or structural output was changed.


## Export-related examples

PXRDGen `pxrd100-poly-02-a`, candidate 1: the first-pass exporter rounds the poorly determined fractional coordinates to integers. The next CIF read fails, so the correct original is retained. The separate precision-patched pilot completed this case but produced a nonmatch. This illustrates why fallback matches are counted separately.

Ab `pxrd100-challenge-013`: default CIF formatting rounds symmetry-related coordinates inconsistently; reading the export expands nine sites into 18 nearly overlapping sites. The file is readable and retains elemental proportions, so this is a completed export that fails structural validity, rather than a full execution failure. The historical precision-corrected analysis restored this one match. The released-export run intentionally retains the uncorrected outcome.


## Reproduction and provenance

All available original candidates reproduce their released benchmark match labels. Original/refined/intermediate CIFs, metric records, compressed logs, source snapshots, and pinned package/source/binary hashes accompany this report. Dense profile arrays remain in the raw run folders; they can be regenerated from the retained CIFs, original observation manifests, and pinned runner. The raw arrays were checked before the compact bundle was made.

Run `report.py --inputs BUNDLE/inputs --results BUNDLE --workers 4`, then `failure_report.py --results BUNDLE` and `write_report.py BUNDLE`. Run `audit_bundle.py BUNDLE` to check artifact and runner hashes. See `experiments/native-refinement/README.md` for the remote execution procedure.
