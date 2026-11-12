# Experiment status

Current package: P0

Development cycle 1: 18/30 package solves counted; 0 free evaluation solves. The comparison may be taken earlier.
Pending prospective comparisons: none.

Evaluator: 7.0.1. Frozen configuration: ../scorer/config_freeze.json; compare scores from the same evaluator.

Dispatch paused: False

| Group | Case | Condition | Individual scores | Mean | Mean without † | D (lower is better) | Independent Rwp % | Scored / slots | Pending or failed infrastructure |
|---|---|---|---|---:|---:|---|---|---:|---:|
| b001-p0 | b001-c03 | P0 | 58.9, 96.5, 80.0 | 78.5 | 78.5 | 1.367, 0.030, 0.279 | 4.19, 2.79, 3.12 | 3/3 | 0 |
| b001-p0 | b001-c05 | P0 | 39.4†, 63.1, 66.7 | 56.4 | 64.9 | 3.001, 0.781, 0.905 | 5.26, 3.47, 3.60 | 3/3 | 0 |
| b001-p0 | b001-c02 | P0 | 88.7, 89.3, 68.6† | 82.2 | 89.0 | 0.042, 0.057, 0.350 | 1.89, 1.92, 2.15 | 3/3 | 0 |
| b001-p0 | b001-c04 | P0 | 61.6, 84.3, 94.6 | 80.2 | 80.2 | 0.933, 0.225, 0.048 | 3.71, 2.92, 2.69 | 3/3 | 0 |
| b001-p0 | b001-c01 | P0 | 99.7, 98.0, 99.6 | 99.1 | 99.1 | 0.003, 0.024, 0.003 | 3.55, 3.57, 3.55 | 3/3 | 0 |
| b001-p0 | b001-c06 | P0 | 93.8, 88.3, 83.7† | 88.6 | 91.1 | 0.009, 0.075, 0.102 | 3.37, 3.51, 3.52 | 3/3 | 0 |
| b001-v1-screen | b001-c01 | v1 | 98.1 | 98.1 | 98.1 | 0.019 | 3.56 | 1/1 | 0 |
| b001-v1-screen | b001-c03 | v1 | 57.9 | 57.9 | 57.9 | 1.086 | 3.98 | 1/1 | 0 |
| b001-v1-screen | b001-c04 | v1 | 66.1 | 66.1 | 66.1 | 0.919 | 3.67 | 1/1 | 0 |
| b001-v1-screen | b001-c02 | v1 | 66.2 | 66.2 | 66.2 | 0.684 | 2.40 | 1/1 | 0 |
| b001-v1-screen | b001-c05 | v1 | 49.8 | 49.8 | 49.8 | 2.310 | 4.76 | 1/1 | 0 |
| b001-v1-screen | b001-c06 | v1 | 84.6 | 84.6 | 84.6 | 0.162 | 3.64 | 1/1 | 0 |
| b001-v2-unresolved | b001-c05 | v2 | 50.6 | 50.6 | 50.6 | 2.361 | 4.80 | 1/1 | 0 |
| b001-v2-unresolved | b001-c03 | v2 | 85.9 | 85.9 | 85.9 | 0.189 | 3.00 | 1/1 | 0 |
| b001-v2-unresolved | b001-c02 | v2 | 83.6 | 83.6 | 83.6 | 0.083 | 1.93 | 1/1 | 0 |
| b001-v2-unresolved | b001-c04 | v2 | 39.1 | 39.1 | 39.1 | 4.244 | 6.05 | 1/1 | 0 |
| b001-v3-analogue | b001-c04 | v3 | 96.4 | 96.4 | 96.4 | 0.023 | 2.67 | 1/1 | 0 |
| b001-v3-analogue | b001-c05 | v3 | 33.4 | 33.4 | 33.4 | 5.398 | 6.38 | 1/1 | 0 |
| b001-v4-coordinate | b001-c05 | v4 | 23.5 | 23.5 | 23.5 | 20.046 | 10.64 | 1/1 | 0 |
| b001-v5-inventory-coordinate | b001-c05 | v5 | 70.1 | 70.1 | 70.1 | 0.641 | 3.32 | 1/1 | 0 |
| b001-v6-structure-recovery | b001-c05 | v6 | 35.1 | 35.1 | 35.1 | 24.283 | 12.74 | 1/1 | 0 |
| b001-v7-connected-ledger | b001-c05 | v7 | 0.0 | 0.0 | 0.0 | — | — | 1/1 | 0 |
| b001-v8-bounded-retry | b001-c05 | v8 | 59.6 | 59.6 | 59.6 | 1.164 | 3.82 | 1/1 | 0 |
| b001-v9-profile-closure | b001-c05 | v9 | running | — | — | — | — | 0/1 | 1 |

Means include provisional (†) scores; nothing adjudicates them, and most belong to failed attempts, so leaving them out would flatter the condition that failed. Mean without † is shown beside it. Both exclude evaluator errors and show denominators. Scientific failures and invalid submissions remain in both. † Provisional physical/registration review.

Last update: 2026-11-07T05:06:23.310002+00:00

## All fresh attempts by case and frozen package

This includes every recorded fresh attempt, not just the best round. Consult the group table to distinguish training, evaluation and prospective transfer.

| Case | Package | Scored / slots | Mean | Mean without † | Minimum |
|---|---|---:|---:|---:|---:|
| b001-c03 | P0 | 3/3 | 78.5 | 78.5 | 58.9 |
| b001-c05 | P0 | 3/3 | 56.4 | 64.9 | 39.4 |
| b001-c02 | P0 | 3/3 | 82.2 | 89.0 | 68.6 |
| b001-c04 | P0 | 3/3 | 80.2 | 80.2 | 61.6 |
| b001-c01 | P0 | 3/3 | 99.1 | 99.1 | 98.0 |
| b001-c06 | P0 | 3/3 | 88.6 | 91.1 | 83.7 |
| b001-c01 | v1 | 1/1 | 98.1 | 98.1 | 98.1 |
| b001-c03 | v1 | 1/1 | 57.9 | 57.9 | 57.9 |
| b001-c04 | v1 | 1/1 | 66.1 | 66.1 | 66.1 |
| b001-c02 | v1 | 1/1 | 66.2 | 66.2 | 66.2 |
| b001-c05 | v1 | 1/1 | 49.8 | 49.8 | 49.8 |
| b001-c06 | v1 | 1/1 | 84.6 | 84.6 | 84.6 |
| b001-c05 | v2 | 1/1 | 50.6 | 50.6 | 50.6 |
| b001-c03 | v2 | 1/1 | 85.9 | 85.9 | 85.9 |
| b001-c02 | v2 | 1/1 | 83.6 | 83.6 | 83.6 |
| b001-c04 | v2 | 1/1 | 39.1 | 39.1 | 39.1 |
| b001-c04 | v3 | 1/1 | 96.4 | 96.4 | 96.4 |
| b001-c05 | v3 | 1/1 | 33.4 | 33.4 | 33.4 |
| b001-c05 | v4 | 1/1 | 23.5 | 23.5 | 23.5 |
| b001-c05 | v5 | 1/1 | 70.1 | 70.1 | 70.1 |
| b001-c05 | v6 | 1/1 | 35.1 | 35.1 | 35.1 |
| b001-c05 | v7 | 1/1 | 0.0 | 0.0 | 0.0 |
| b001-c05 | v8 | 1/1 | 59.6 | 59.6 | 59.6 |
| b001-c05 | v9 | 0/1 | — | — | — |
