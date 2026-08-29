# Adapted-codex full-200 evaluation

This is the blind, one-attempt-per-case evaluation of the frozen `adapted-codex`
capability on all 200 released pXRD-Bench cases.

## Results

| Score | Adapted-codex | Frozen pXRD-codex control |
| --- | ---: | ---: |
| Primary `selected_exact` | **138/200 (69.0%)** | 114/200 (57.0%) |
| Declared `candidates_exact` | **141/200 (70.5%)** | 117/200 (58.5%) |

For primary selection, 98 cases were solved by both conditions, 40 only by
adapted-codex, 16 only by pXRD-codex, and 46 by neither. Their union is 154/200. The
two-sided exact paired binomial test on the 40:16 discordant outcomes gives
`p = 0.00184155478849`.

| Category | Cases | `selected_exact` | `candidates_exact` |
| --- | ---: | ---: | ---: |
| Challenge | 30 | 22 | 22 |
| Polymorph | 40 | 28 | 28 |
| Representative | 30 | 27 | 27 |
| Ordered decoration | 25 | 21 | 21 |
| Familiar substitution | 25 | 19 | 19 |
| Novel crystal search | 25 | 11 | 12 |
| Novel Wyckoff | 25 | 10 | 12 |

## Protocol

- Model: `gpt-5.6-sol`, high reasoning effort.
- Harness: Codex standalone `0.149.0-x86_64-unknown-linux-musl`.
- Authentication: ChatGPT subscription.
- Resources: 2 vCPU, 5 GiB, 128 tasks, and a one-hour limit per case.
- Parallelism: 16 continuously refilled workers.
- Prompt: the released short structure-solution prompt.
- Scientific environment: the released pXRD environment plus the frozen learned
  capability whose package SHA-256 is
  `a2803fd4807ccea23915e368d3c23455f80b88156df81bb4b744979df3ccd5aa`.

All 200 attempts completed archival; three reached the one-hour limit, no workers failed,
and 198 attempts produced a primary CIF. The normalized bundle retains verifier output,
submitted primary and alternative CIFs, final answers, launch metadata, sanitized source
metadata, content hashes, and compressed chronological traces.

The frozen pXRD-codex control used the same model family, prompt, scientific environment,
and per-case limits but API authentication. This difference is explicit in the directory
names and `paired-pxrd-codex.json`, so the comparison is not a strict single-variable
ablation.

## Files

- `bundle.json`: normalized case-level outcomes, hashes, and provenance.
- `category-summary.csv`: exact recovery by benchmark category.
- `paired-pxrd-codex.csv` and `.json`: matched-case comparison with pXRD-codex.
- `attempts/`: public per-case evidence, including compressed traces.
- `source-metadata/`: sanitized run, condition, prompt, panel, and capability manifests.
