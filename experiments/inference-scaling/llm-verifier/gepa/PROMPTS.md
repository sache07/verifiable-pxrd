# Prompt inventory

Every agent-facing prompt owned by this experiment is a Markdown file under
[`prompts/`](prompts/). GEPA's built-in candidate merging is disabled so that it
cannot introduce a hidden, package-defined merge prompt.

| File | Called by | Mutable during optimization? | Purpose |
| --- | --- | --- | --- |
| `reviewer-wrapper.md` | Blind reviewer | No | Evidence paths, task framing, and the `decision.json` contract. |
| `seed-judge-policy.md` | Blind reviewer | Yes, as the initial `judge_policy` | Scientific stop/continue policy optimized by GEPA. |
| `reflection.md` | Policy-proposal agent | No | Directs training-time inspection of the blind evidence, both traces, submitted and reference CIFs, and verifier outcome before proposing a replacement policy. |
| `evaluator-feedback.md` | External evaluator | No | Provides the decision label and a compact index into the complete reflection artifacts. |
| `continuation-policy.md` | Later second-pass solver | No during judge optimization | Defines the downstream continuation used only after the judge is frozen. |

The rendered reviewer prompt is:

```text
reviewer-wrapper.md(
  case evidence,
  judge_policy = current GEPA candidate
)
```

Only the current policy is changed. The reviewer never receives a reference CIF,
an exact-match result, another attempt, or post-hoc structural diagnostics. After
the blind decision is archived, the reflection agent receives read-only access to
the complete training-case evidence, including the reference and verifier result.

Before any run, edit these files directly and use `pxrd-gepa render` on a staged
example to inspect the exact reviewer prompt.
