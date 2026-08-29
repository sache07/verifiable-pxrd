# Verifiable pXRD problems

This is a locked collection of 50 single-phase pXRD structure-determination
problems for verifiable training. It proportionally mirrors the declared
categories of the held-out 200-case `pXRD-100 + pXRD-ood` benchmark while using
the disjoint development-v2 source panels. Selection never used solver results.

## Standard collection layout

```text
verifiable-pxrd-problems/
  README.md
  manifest.json                 authoritative collection manifest
  problem-order.csv             prefix-balanced training order plus provenance
  problem-order.txt             problem IDs only, one per line
  SOURCE.lock.json              source/exclusion manifest hashes
  selection-report.json         requested and realized marginals
  verifier/
    verifier.json               verifier contract and metric settings
    verify.py                   shared executable verifier
    requirements.txt
  problems/
    vp-001/
      problem.json              paths, hashes, verifier, metadata
      problem_input/            the only trainee-visible problem payload
        prompt.md
        pattern.csv
      solution/                 private oracle material
        reference.cif
```

Every problem is self-describing through `problem.json`. Paths in that file are
relative to the problem directory, and all public inputs and solutions are
SHA-256-bound. A harness should stage only `problem_input/` for a blind attempt;
`solution/`, collection metadata, and source provenance stay outside the trainee
sandbox. `problem-order.csv` is the authoritative training sequence; see
`ORDERING.md` for the original outcome-blind construction and the documented
later scheduling adjustment. The neutral IDs intentionally reveal neither
chemistry nor category.

## pXRD verifier

The shared verifier grades root-level `selected.cif` and `alternative-<n>.cif` only. It
reports `selected_exact` for the primary file and `candidates_exact` when either the
primary or a declared alternative matches. This preserves the distinction between
selecting the reference-like answer and merely covering it in a candidate set. It uses the
benchmark-report predicate:

```python
StructureMatcher(
    ltol=0.2,
    stol=0.3,
    angle_tol=5,
    primitive_cell=True,
    scale=False,
    attempt_supercell=True,
    allow_subset=False,
    comparator=ElementComparator(),
).fit(reference, candidate, symmetric=True)
```

Run it directly with:

```bash
python verifier/verify.py \
  --problem problems/vp-001 \
  --workspace /path/to/attempt-workspace \
  --output /path/to/result.json
```

The verifier also accepts problem paths supplied through the training harness
environment.

Synthetic-generation profile parameters are excluded from trainee inputs. Their
source-record hashes are stored in `SOURCE.lock.json`, and the generation artifacts
are retained with the corpus builders.

## Roster design

The 50 cases contain 25 pXRD-100-style and 25 OOD problems. Integer rounding is
assigned toward harder strata: 7 representative, 8 challenge, 10 polymorph;
6 substitutions, 6 ordered decorations, 6 topology-novel Wyckoff cases, and 7
topology-novel crystal-search cases. The polymorph subset contains five complete
two-member families (1 easy, 2 medium, 2 hard). See `SELECTION.md` for the full
outcome-blind protocol and `selection-report.json` for realized marginals.
