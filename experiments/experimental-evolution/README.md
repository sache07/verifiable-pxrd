# Experimental evolution

In a reflexive evolution process, a GPT-5.6 Sol evolver (Max effort, Codex) improves its own powder-XRD quantitative phase analysis. It works through four steps:
1. It curates synthetic, verifiable training problems for one sample family.
2. It launches solver attempts by the same model and studies them.
3. It drafts learned packages, each a short guidance text plus optional read-only helpers.
4. It screens, evaluates and promotes packages under a fixed budget and fixed rules.

No stronger model contributes. The measured scans in [`pxrd-bench/divalent-tungstates-PG15`](../../pxrd-bench/divalent-tungstates-PG15/README.md) are never shown to the researcher or used in its scorer.

## Layout

This folder holds what is needed to start a run:

| Path | What |
|---|---|
| [`framework/`](framework/README.md) | Shared by every run and never run in place. `evolve/` holds what the researcher reads (PROMPT.md, TOOLS.md, P0.md, AGENTS.md, the `lab.py` request client). `runtime/` is the synthetic-problem generator, `scorer/` the profile-primary scorer, and `control/` the request broker, EC2 runner, isolation probe, installer and tests. `policies/P0/` is the baseline package, and `new_run.py` creates a run. |
| [`labs/`](labs/TEMPLATE.md) | One LAB.md per sample family: the sample family, measurement, generator settings and solver-input format. It is written from prior lab knowledge, never from evaluation results. [`labs/divalent-tungstates/LAB.md`](labs/divalent-tungstates/LAB.md) is the lab used here, and `labs/TEMPLATE.md` explains how to write one. |
| [`AGENTS.md`](AGENTS.md) | Operator rules: change the framework only deliberately and record why, never edit a run after its researcher has started, and keep evaluation data out of run folders. |
| [`DECISIONS.md`](DECISIONS.md) | Every framework change with its reason, including decisions informed by earlier panels on the measured scans (for example 33–34). It calls `divalent-tungstates-PG15` "eval15". |

A run is a frozen copy of `framework/` plus one LAB.md, and everything it produces, packages included, is an output. The November run is kept with the results:
- [`results/experimental-evolution/divalent-tungstates/`](../../results/experimental-evolution/README.md) is the complete record: the researcher's session, its synthetic cases, every solve, and packages P0 and v1–v15. The package evaluated as `evolved` is its `policies/v6/`.
- The same result index includes `divalent-tungstates-fw/` and
  `divalent-tungstates-access/`, the two framework-access evolution campaigns that
  promoted no package. Their frozen protocols and all available attempts are retained.
- [`results/experimental-eval/divalent-tungstates-PG15/`](../../results/experimental-eval/divalent-tungstates-PG15/RELEASE.md)
  contains all five main measured conditions, follow-ups and model comparisons.
- [`analysis/`](analysis/README.md) rebuilds tables and figures without launching
  new solver attempts. The [release guide](../../docs/MULTIPHASE.md) distinguishes
  this from configuring a new paid campaign.

## Start a run

From this folder:

```bash
python framework/new_run.py --lab labs/NAME/LAB.md --name NAME --canary LABEL=/path/to/an/evaluation/label
```

`--canary` takes files the researcher must not be able to read (evaluation labels, analyses); the environment check verifies each one. Then, inside `runs/NAME` (ignored by git):
1. `python control/install.py` freezes P0, the environment manifest and infrastructure hashes, and copies the run to the EC2 solver host.
2. `python control/start_controller.py` starts the controller and the 30-minute process monitor.
3. Open `runs/NAME/evolve/` in the Codex app and trust the folder. Codex reads the run's `.codex/config.toml` only for a trusted folder, so start a new thread after trusting. Check that it shows GPT-5.6 Sol, Max and the profile named in its AGENTS.md, and send:

   > Read PROMPT.md and carry out the autonomous PXRD evolution process.

The original runs used `<HOME>/.local/share/pxrd-baseline/core/bin/python` for these operator commands.

## Relation to the measured scans

The framework was developed over several earlier runs, and some generator ranges and case types were chosen after solves on the measured scans had been seen. DECISIONS.md records each such change. Decision 34, for example, widened the simulated peak-asymmetry range. The November run's researcher saw only its synthetic cases, LAB.md and the framework documents. The measured-scan comparison is therefore a development evaluation of the process, not a sealed test.
