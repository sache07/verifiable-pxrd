# Opus 5 P0 experimental baseline (Claude Code)

Fresh attempts on the same 15 experimental Precursor Genome tungstate scans used by [matched P0](../pxrd-matched-p0-eval15-20261007/CONDITIONS.md). Stage 1 is one attempt per case (`jobs/opus5-r1.json`, `OPUS5-P0-exp-case-NNN-r1`). Replicates r2 and r3 are optional later stages. The intended change is the solver model and harness: **Claude Opus 5 (`claude-opus-5`, effort `high`, its default) in Claude Code 2.1.299** replaces gpt-5.6-sol/high in Codex 0.154. Everything else is the matched P0 condition.

## Held fixed

- P0 prompt bytes (`policies/P0/prompt.md`, sha256 `0c5def00…`, final.gpx requirement included). No learned guidance, helpers, AGENTS.md or CLAUDE.md.
- Raw `pattern.csv`/`metadata.json` byte-identical to matched P0 (`control/input_manifest.json`, checked at copy time).
- Frozen DARA-filtered COD 2024 index (sha256 `03599f54…`) and CIFs, the materials-science environment, GSAS-II, DICVOL14, and the same blocked package data. No web, no ICSD, no references, prior outputs or canonical answers.
- Filesystem view equal to the Codex P0 profile: minimal system, scientific tools and COD read-only, private writable workspace, inputs read-only, no `/tmp` at all (Codex P0 denied it; TMPDIR is `workspace/.tmp`), sandbox root read-only, everything else absent. Same environment variables (HOME = workspace, two numerical threads).
- Per attempt: systemd scope with 2 CPUs, 5 GiB memory, no swap, 128 tasks. No solver time limit, no automatic duplicates or scientific retries. Up to 15 concurrent attempts.
- Primary scoring: frozen final.gpx replay with the fitted calibration preserved, 10.1–99.9°, weights `1/max(counts,1)` (`control/evaluate_attempt.py` and `scoring_v5/`, copied unchanged from the V6R evaluation). The copy reproduces all three matched P0 case-005 replays exactly (`checks/evaluator_reproduction/`).
- Secondary scoring, declared before launch: the same replay with only the 2θ grid-identity tolerance widened from 1e-7° to 1e-6° (`secondary_gridtol/`). It accepts projects whose converted scan rounds 2θ to 6 decimals; counts and point count must still match exactly. It is applied identically to Opus and Sol attempts and reported next to the primary score, never in place of it.

## Harness

- `claude -p --model claude-opus-5 --effort high --tools Bash,Read,Write,Edit,Glob,Grep --permission-mode bypassPermissions --strict-mcp-config --output-format stream-json`. The binary sha256 `2d894a4b…` matches Anthropic's public 2.1.299 linux-x64 release manifest.
- Per-attempt `CLAUDE_CONFIG_DIR`; bundled skills, built-in plugins, auto-memory and CLAUDE.md loading off; no subagents, web tools or MCP. The tool surface the CLI reports at startup is recorded in each `run/launch.json` (`init`).
- Authentication uses the user's Claude subscription (long-lived token from `claude setup-token`), the counterpart of Codex's ChatGPT login. The token stays on the host in `~/.config/pxrd-anthropic/oauth_token`. Inside the sandbox the CLI holds only a per-attempt dummy token.
- Network: the sandbox has its own empty network namespace. The CLI reaches the API through `control/bridge.py` (inside) → Unix socket → `control/auth_proxy.py` (host), which checks the dummy token, injects the subscription token and forwards only to api.anthropic.com. The bridge relays only connections owned by the CLI process itself: tool commands, scripts or a nested CLI are refused. Every API request is logged in `run/proxy.jsonl`, and each launch record flags any non-CLI, foreign-session or rejected request.

## Checks before launch

- The model-free probe (the matched P0 `probe.py` checks plus the Claude binary hash) runs inside each attempt's exact sandbox before the model starts.
- Isolation check (`ISO-haiku-case-005` plus a model-free replay of the probes Haiku declined): answer files, prior attempts, the token file and the private canary are absent; no network or DNS; inputs read-only; the sandbox root is read-only; tool-originated API connections are refused at the bridge, and none reached the host.
- Opus 5.5 smoke attempt `OPUS-P0-smoke-case-005` (a different model; not part of this panel). The frozen scorer rejected its project only for 6-decimal 2θ rounding, which motivated the declared secondary score. Opus 5 model check: `MODELCHECK-opus5-high`. It ran with a private scratch `/tmp`, which the solver used for its working files. `/tmp` was removed afterwards, and `NOTMP-haiku-case-005` confirmed the CLI, mktemp/tempfile, numpy and GSAS-II work without it.

## Known differences from matched P0

- Model and harness change together (system prompt, tool design, context compaction), so this compares Opus + Claude Code with Sol + Codex, not the models alone.
- Not run at the same time as matched P0 (7 Oct vs 19 Oct).
- Subscription usage limits can pause dispatch (`control/STOP_DISPATCH.json`). Running attempts continue and queued attempts wait; nothing is relaunched.
- Both panels are development evaluation: these 15 cases have informed earlier research decisions.
