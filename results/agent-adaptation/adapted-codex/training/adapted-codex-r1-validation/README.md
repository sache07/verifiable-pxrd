# Adapted-codex frozen behavioral validation

This is the complete frozen-capability wave used to decide whether to promote the
public `adapted-codex` package. Its roster was fixed before launch: all 20
`pxrd-codex` baseline misses plus three prior successes selected as regression
controls (`vp-012`, `vp-014`, and `vp-029`).

- Capability commit: `4701bedb466d970174c78c0fc0743ba486e3d99e`
- Capability SHA-256: `a2803fd4807ccea23915e368d3c23455f80b88156df81bb4b744979df3ccd5aa`
- 23/23 attempts completed; two (`vp-015` and `vp-046`) reached the one-hour limit.
- 9/23 were `selected_exact` and `candidates_exact`.
- Six baseline failures were recovered: `vp-002`, `vp-004`, `vp-005`, `vp-006`,
  `vp-034`, and `vp-049`.
- All three prior-success controls remained exact.

The package was not edited during the wave and was frozen afterward. This is targeted
behavioral validation, not a fresh 50-case pass@1 estimate. `bundle.json` indexes the
normalized outcomes and source hashes; `attempts/` contains sanitized prompts, traces,
responses, declared CIFs, launch records, and external-verifier results. The trainer's
predeclared assessment and freeze decision are retained under `trainer-notes/`.
