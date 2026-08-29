# Frozen 30/10/10 GEPA split audit

This split freezes the 50 completed adapted-Codex first-pass trajectories into 30 training, 10 validation, and 10 development-test problems before any GEPA optimization. It is an internal prompt-development split, not the final system benchmark. The inference-scaling held-out panel remains untouched.

## Selection protocol

- Split selection used only the completed frozen first-pass outcomes and declared problem metadata. It did not use any GEPA judge decisions.
- Each validation-sized set contains one representative, two challenge, two polymorph, one substitution, one ordered-decoration, one Wyckoff-enumeration, and two crystal-search problems. This gives each exactly five pXRD-100-v2 and five pXRD-ood-v2 sources.
- Validation and development each contain seven candidate-set-exact `stop` cases and three nonexact `continue` cases. Training contains 22 stops and eight continues.
- The five two-member polymorph families are indivisible: no formula/polymorph family crosses a split.
- The six held-out misses contain one case from each category that exhibited a miss. Training independently retains at least one miss from every such category.
- Each 10-case holdout contains all seven crystal systems. One alternative-only exact submission is retained in training and one in validation. The two timeout cases are divided between training and development.
- A seeded constrained search first minimized deviation from the full-set distributions of crystal system, primitive-site bin, element count, space-group-number band, runtime band, original-order quintile, and declared challenge/polymorph subtype. Two outcome-preserving, within-category swaps then filled the single missing crystal system in each holdout while improving development runtime and site-count balance.

Frozen source hashes:

- Problem manifest: `724ce82b75c08bd4a85f78df11b88b6c7f7d203302c97015dd3525ba91b9e38e`
- First-pass summary: `ee6316a8adb640f1eca9899579ad68ebe6a08c2b03b971030ae2a5c91f022bd7`

## Frozen membership

### Training (30)

`vp-012`, `vp-004`, `vp-034`, `vp-029`, `vp-046`, `vp-010`, `vp-021`, `vp-039`, `vp-018`, `vp-027`, `vp-035`, `vp-031`, `vp-014`, `vp-006`, `vp-024`, `vp-007`, `vp-025`, `vp-028`, `vp-005`, `vp-045`, `vp-041`, `vp-020`, `vp-008`, `vp-001`, `vp-049`, `vp-036`, `vp-026`, `vp-040`, `vp-050`, `vp-009`

### Validation (10)

`vp-023`, `vp-017`, `vp-032`, `vp-016`, `vp-019`, `vp-044`, `vp-022`, `vp-043`, `vp-011`, `vp-037`

### Development test (10)

`vp-038`, `vp-033`, `vp-042`, `vp-002`, `vp-048`, `vp-013`, `vp-047`, `vp-030`, `vp-003`, `vp-015`

## Marginal audit

### Benchmark category

| Value | Train | Validation | Development | Total |
| --- | ---: | ---: | ---: | ---: |
| representative | 5 | 1 | 1 | 7 |
| challenge | 4 | 2 | 2 | 8 |
| polymorph | 6 | 2 | 2 | 10 |
| substitution | 4 | 1 | 1 | 6 |
| ordered-decoration | 4 | 1 | 1 | 6 |
| wyckoff-enumeration | 4 | 1 | 1 | 6 |
| crystal-search | 3 | 2 | 2 | 7 |

### Oracle reviewer action

| Value | Train | Validation | Development | Total |
| --- | ---: | ---: | ---: | ---: |
| stop | 21 | 6 | 7 | 34 |
| stop-alt | 1 | 1 | 0 | 2 |
| continue | 8 | 3 | 3 | 14 |

### Source dataset

| Value | Train | Validation | Development | Total |
| --- | ---: | ---: | ---: | ---: |
| pXRD-100-v2 | 15 | 5 | 5 | 25 |
| pXRD-ood-v2 | 15 | 5 | 5 | 25 |

### Crystal system

| Value | Train | Validation | Development | Total |
| --- | ---: | ---: | ---: | ---: |
| triclinic | 4 | 1 | 1 | 6 |
| monoclinic | 7 | 3 | 2 | 12 |
| orthorhombic | 6 | 1 | 1 | 8 |
| tetragonal | 3 | 2 | 3 | 8 |
| trigonal | 5 | 1 | 1 | 7 |
| hexagonal | 2 | 1 | 1 | 4 |
| cubic | 3 | 1 | 1 | 5 |

### Primitive-site bin

| Value | Train | Validation | Development | Total |
| --- | ---: | ---: | ---: | ---: |
| 1-4 | 5 | 1 | 1 | 7 |
| 5-8 | 4 | 3 | 2 | 9 |
| 9-12 | 8 | 1 | 2 | 11 |
| 13-16 | 6 | 2 | 2 | 10 |
| 17-20 | 7 | 3 | 3 | 13 |

### Element count

| Value | Train | Validation | Development | Total |
| --- | ---: | ---: | ---: | ---: |
| 1 | 1 | 1 | 0 | 2 |
| 2 | 3 | 1 | 2 | 6 |
| 3 | 13 | 3 | 4 | 20 |
| 4 | 9 | 5 | 2 | 16 |
| 5 | 4 | 0 | 2 | 6 |

### First-pass runtime band

| Value | Train | Validation | Development | Total |
| --- | ---: | ---: | ---: | ---: |
| short (<12m) | 9 | 5 | 3 | 17 |
| medium (12-25m) | 11 | 3 | 4 | 18 |
| long (>25m) | 10 | 2 | 3 | 15 |

## Outcome-bearing cases

- **Training:** continues `vp-046`, `vp-039`, `vp-018`, `vp-031`, `vp-024`, `vp-028`, `vp-045`, `vp-026`; alternative-only stops `vp-014`; timeouts `vp-046`.
- **Validation:** continues `vp-023`, `vp-017`, `vp-037`; alternative-only stops `vp-032`; timeouts none.
- **Development:** continues `vp-048`, `vp-047`, `vp-015`; alternative-only stops none; timeouts `vp-015`.

The split should now remain frozen. Development-test outcomes must not influence GEPA mutation, validation selection, stopping, or finalist nomination.
