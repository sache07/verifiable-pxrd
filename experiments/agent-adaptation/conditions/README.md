# Agent-adaptation conditions

A condition specifies a harness and model, scientific environment, prompt, optional
capability, compute limit, and network policy. Four evaluation conditions are
included:

- `llm-chat-sol-high-api-v2.toml`: one Responses API user message containing the
  rendered `chat-solve.md` prompt and complete 8,501-row CSV, with no tools, developer
  message, code execution, or persistent workspace;
- `matsci-codex.toml`: Codex with the general materials-science substrate and no task-specific
  capability;
- `pxrd-codex.toml`: the same Codex model and prompt with GSAS-II and bare DICVOL14,
  API authentication, and a one-hour limit per problem;
- `adapted-codex.toml`: the pXRD environment plus the immutable learned capability frozen
  before held-out evaluation, launched through machine-local ChatGPT subscription
  authentication.

Training uses a separate mutable condition under `experiments/agent-adaptation/`.

Each Codex condition contains its environment policy and installation specification.
The materials-science conditions record the input requirements, package lock, Python
version, and installer. The pXRD conditions additionally record the GSAS-II revision,
dependency lock, installer, and DICVOL14 binary checksum and installer.

Run metadata includes the condition file, prompt hash, model and reasoning level,
and resource contract. Run-specific variants are recorded in their result bundles.

`portable/gsas-codex.toml` is a macOS/Linux setup example for the runtime created by
`vpbench setup-runtime`. It excludes DICVOL and is not used in the four reported
evaluation conditions.

The LLM chat condition is launched by `scripts/run_llm_only.py`, not by the Codex harness.
The runner archives the literal template and rendered prompt, complete serialized API
request, pattern and request hashes, condition and panel hashes, and its own source and
commit. The model receives no local Python, scientific libraries, or workspace.
