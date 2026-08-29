# Verifier-gated scaling

One ordinary adapted-Codex solve per problem was followed by blind verifier
decisions and only the authorized solver calls. The schedule was
`S0 -> J0 -> C1 -> J1 -> S2 -> J2 -> S3`; `C1` received the initial trace,
CIFs, and review reason, while `S2` and `S3` were fresh ordinary solves.
Candidates were retained cumulatively and declared alternatives counted as
exact recoveries.

## Result

| Checkpoint | Cumulative exact candidates | Recovery | Cumulative agent calls | Token cost |
| --- | ---: | ---: | ---: | ---: |
| S0 | 13/20 | 65% | 20 | $62.9920 |
| C1 | 17/20 | 85% | 52 | $140.5061 |
| S2 | 18/20 | 90% | 73 | $184.1190 |
| S3 | 18/20 | 90% | 88 | $216.5979 |

Token costs use each stage's recorded token mix under the frozen price schedule,
then apply the campaign-wide calibration to the $446.15 source bill. In
particular, S0 is the measured cost of replicate 1, not one eighth of that bill.

## Case-level execution matrix

`E` means the primary CIF was exact, `A` means an alternative was exact, `M`
means no submitted CIF was exact, and `--` means the gate ended that case.
For reviews, `S`/`C` mean stop/continue; `+` marks a retrospectively correct
decision and `!` an incorrect decision.

```text
CASE 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20
S0    E  E  M  E  M  M  E  E  E  E  M  E  M  M  E  E  E  E  M  E
J0   C! C! C+ S+ C+ C+ S+ S+ S+ S+ C+ S+ C+ C+ C! S+ S+ C! C+ C!
C1    E  E  E --  A  M -- -- -- --  M --  E  M  A -- --  M  E  E
J1   C! C! C! -- S+ C+ -- -- -- -- C+ -- S+ C+ S+ -- -- C+ C! C!
S2    E  E  E -- --  M -- -- -- --  E -- --  M -- -- --  M  M  E
J2   C! S+ C! -- -- C+ -- -- -- -- C! -- -- S! -- -- -- C+ C+ S+
S3    A --  M -- --  M -- -- -- --  M -- -- -- -- -- --  M  M --
status complete=20 running=0 failed=0; finalized cumulative exact=18/20
```

## Artifact layout

- `scaling-curve.csv` contains the plotted recovery/cost points.
- `outcomes.csv` and `stage-matrix.csv` contain the per-case outcomes.
- `attempts/vh-*/` contains every applicable prompt, decision, compressed
  chronological trace, response, submitted CIF, verifier result, and launch.
- `candidate-pool/` under each case preserves all structures cumulatively.
- `source-metadata/` freezes the panel, conditions, prompts, policy, and hashes.
- `cost-method.json` records token counts, prices, calibration, and imputation.
- `SHA256SUMS` authenticates every normalized artifact.

The hidden references are not included. Agents never received a reference CIF
or verifier result; those were applied only after each solver stage for
retrospective evaluation.
