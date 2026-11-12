# Framework

Shared by every run; never run in place. `new_run.py` copies it into `runs/NAME/` together with one lab's LAB.md.

| Path | Role |
|---|---|
| `evolve/` | What the researcher reads: PROMPT.md, TOOLS.md, P0.md (byte-identical baseline prompt), AGENTS.md, `lab.py` (request client), `verify_environment.py`; the Codex profile template |
| `runtime/` | Generator. `labspec.py` reads LAB.md's settings; `generator_defaults.json` holds the lab-independent audit thresholds; `solver_inputs.py` writes inputs in the lab's experimental format |
| `scorer/` | Profile-primary scorer 7.0.0: verified final.gpx replay against the hidden noise-free pattern (D), gated by physical validity, with a secondary scattering-weighted structural term. Self-contained, frozen by `config_freeze.json` |
| `control/` | Request broker, EC2 runner, isolation probe, process monitor, installer, tests, and `validation/` (oracle-project reward checks) |
| `policies/P0/` | The baseline package |
