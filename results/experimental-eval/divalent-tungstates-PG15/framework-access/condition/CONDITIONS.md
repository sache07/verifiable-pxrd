# Framework access on the 15 measured scans with GPT-5.6 Sol Max

This panel prepares 45 fresh solves, three per scan, of a control condition for the evolved package. The solvers are the baseline condition plus read-only access to the starting folder of the November evolution run (`pxrd-evolution/runs/divalent-tungstates`, created 2026-11-02). They are told to do the solve, not the evolution, and that they may use anything in the folder.

The question it answers: how much of the evolved package's gain comes from the evolution itself, and how much from information the framework already held, such as the lab description, the generator's instrument and specimen ranges, the analogue-search tool and the instructions? The evolved package was learned from exactly this folder, so the folder is the information the evolution had before it ran.

Request, from the user on 2026-11-05: "give otherwise baseline condition solvers the evolution framework (I'm thinking pretty much the starting folder that we did the evolution of the november v6 package in) and tell them to do the solve, not the evolution process, but that it can glean any useful information/instructions from the package for it's solves ... get things ready to run the full baseline". **Prepared only.** Launching needs a separate go-ahead.

## Conditions

These match the baseline panel (`pxrd-sol-max-p0-eval15-repeat2-20261019`) and the evolved panel (`pxrd-eval15-v6nov-20261104`) unless the table says otherwise. `control/prepare_panel.py` asserts each match.

| Parameter | Condition |
|---|---|
| Model | `gpt-5.6-sol` at reasoning effort `max` |
| Harness | Pinned Codex CLI 0.154.0. `runner.py` and `probe.py` are byte-identical to both panels'. The condition TOML is `38ae49bb…`. |
| Prompt | The exact P0 bytes (`0c5def00…`) followed by a 120-word note (`policies/framework-access/guidance.md`); prompt SHA-256 `258f27e7…`. The note is appended the same way as the evolved guidance. |
| Folder | The November starting folder, read-only at `learned/divalent-tungstates/`: 45 files, 304 kB (see below) |
| Inputs | Byte-identical to every earlier panel on these scans |
| References | Frozen DARA-filtered COD 2024 index and CIFs, with no masks |
| Resources | 2 CPU cores, 5 GiB memory, no swap, 128 tasks; **no time limit** |
| Dispatch | Up to 16 concurrent solves on `pxrd-tungstate15-ec2`, breadth-first, as for the evolved panel |
| Isolation | As before: a private workspace and session per attempt, no network, and answers that cannot be read. The probe also checks that the November run's later state (STATE.md, investigations, packages including v6, synthetic truths) and the evolved panel's package and results are unreadable. |

**Assessment:** the frozen evaluator, unchanged and byte-identical to the evolved panel's. The live table `report/COMPARISON.md` compares this condition with the evolved panel and the baseline (P0 Max).

## The starting folder

**How it is rebuilt.** `prepare_panel.py` runs `new_run.py`'s own steps from `pxrd-evolution/framework` and `labs/divalent-tungstates/LAB.md`, filling the templates with the November run's paths. The checks:
- The framework's tree digest and LAB.md's hash equal the values recorded in the run's `RUN.json`, so the framework has not changed since the run was created.
- All 112 rebuilt files exist in the run. 108 are byte-identical; the other 4 are files the run itself rewrites (`control/state.json`, `evolve/STATE.md`, `evolve/environment.json`, `scorer/truth_provenance.json`), and the rebuild has their initial content.
- The 25 researcher-immutable files match the hashes the installer recorded before the researcher started.
- `policies/framework-access/reconstruction.json` records all of this.

**What solvers get: exactly what the November researcher could read.** Its Codex profile allowed reading `evolve/`, `runtime/`, `scorer/`, `policies/`, `cases/`, `batches/` and `evidence/`. At the start the last three were empty.
- `evolve/`: PROMPT.md, TOOLS.md, AGENTS.md, LAB.md, P0.md, `lab.py`, `verify_environment.py`, settings, the researcher's Codex profile, the starting STATE.md, and empty working folders.
- `runtime/`: the synthetic-pattern generator, including `library_neighbours.py`, the same-stoichiometry analogue search described in TOOLS.md.
- `scorer/` and `policies/P0/`.

**What is left out.** The researcher could not read these, and they carry no analysis content:
- `control/`: the broker, EC2 runner, settings with the host name, and the isolation canary;
- `RUN.json` and the root README;
- `attempts/` and `resources/`;
- the empty `evolve/.git`.

Install-time records and the worker login are not part of the starting folder and are never copied.

**Audit.** The delivered files name no hidden phase, scan, panel or evaluation set, and contain no credentials, host names or canary text. They do contain the framework's design choices, some made after earlier solves on these scans had been seen (DECISIONS.md 33–34, for example the generator's SH/L range). That is intended: the evolved package also came from these choices, and this control holds them fixed.

## Decisions

1. **The researcher's starting view, not the whole run folder.** It is the information the evolution started from, and it leaves out infrastructure the researcher never saw.
2. **Rebuilt rather than copied from the run.** The live run folder has been written to for two days. The rebuild is byte-identical to the creation state, and the comparisons above show it.
3. **Delivered like the evolved package.** It arrives at `learned/` through the same runner path and with the same read-only sandbox rule. The prompt is P0 followed by the note, as the evolved prompt is P0 followed by its guidance, so the two conditions differ only in what follows P0 and what is in `learned/`.
4. **A neutral note.** It says what the folder is, names its main parts, says not to run the process, and allows using any information, instructions *or code* in it. "Code" is included because the folder's analogue search and generator are information the evolved package drew on. The note gives no procedure.
5. **Same budget and dispatch as the evolved panel.** That means no time limit and 16 concurrent solves.
6. **Same 15 scans × 3 and evaluator,** so the existing tables extend with one more column.
7. **The panel lives at its final place, `verifiable-pxrd-raw/…/divalent-tungstates-PG15/`, on both hosts.** The follower mirrors the same path, so nothing needs moving afterwards.

## Operation

- **`control/stage_ec2.sh`** (starts no solver) does the following:
  1. Creates the folder on EC2 and copies the panel, without the answer references.
  2. Copies the worker login server-side from the evolved panel's `control/auth`.
  3. Prepares all 45 workspaces and runs `prelaunch.py`, which checks prompts, inputs, the delivered folder and the read-only rule, and runs the sandbox probe.
- **`control/launch.sh`** (needs a go-ahead) starts `pxrd-pg15-fwaccess-1105-dispatcher.service` on EC2 and `pxrd-pg15-fwaccess-1105-follow.service` locally. When all 45 are terminal, the follower runs the full assessment.
- **Blocked:** SSH to `pxrd-tungstate15-ec2` fails host-key verification. The config's `UserKnownHostsFile` was `pxrd-tungstate15-baseline-20260919/control/known_hosts`, which was deleted in the 2026-11-05 cleanup. The host key has to be re-trusted before staging.

## Caveats

- **Development evaluation.** These scans shaped earlier research choices.
- **The model alias is noncontemporaneous.** The panels run 2026-10-19/20 (baseline), 2026-11-04 (evolved) and from 2026-11-05 (this one). A fresh P0 panel run alongside this one would separate drift from the condition.
- **The note is itself an intervention.** A difference from the baseline includes the effect of being pointed at the folder, and possibly time spent reading it.
- **Some folder code assumes the evolution host.** For example, `lab.py` needs the broker. It fails harmlessly in the solver sandbox, which has no network.
