# Full pXRD-Bench, GPT-5.6 Sol high

This normalized bundle contains the completed 200-case `matsci-codex` benchmark run
collected August 4–5, 2026. The agent received the benchmark prompt, ordinary
materials-science Python, and read-only local COD access; it received no GSAS-II,
DICVOL14, or learned pXRD capability.

The exact `scale=False` StructureMatcher score is 104/200 for `selected.cif` and
105/200 including declared alternatives. Three pXRD-ood cases remained
infrastructure-blocked and count as misses in the 200-case denominator.

`attempts/` contains one canonical attempt per benchmark case. The source run contains
214 raw attempt directories because infrastructure failures were retried; canonical
attempts here follow the final per-case entries declared by source `progress.json`.
`source-metadata/` preserves the sanitized run contract and the complete canonical-attempt
mapping. Chronological event traces are compressed reproducibly as
`codex-events.jsonl.gz`.
