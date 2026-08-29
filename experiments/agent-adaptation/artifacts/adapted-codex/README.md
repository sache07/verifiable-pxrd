# adapted-codex

This is the frozen pXRD capability used by the `adapted-codex`
condition. It was produced by the isolated 50-problem agent-adaptation experiment
and frozen at trainer commit `4701bedb466d970174c78c0fc0743ba486e3d99e`.

The package contains:

- `package/SKILL.md`: a short exact-periodic-CIF and submission contract;
- `package/bin/dicvol14-adapter`: a neutral peak-list interface to the installed
  DICVOL14 backend that preserves native inputs, outputs, logs, and provenance.

The package tree SHA-256 is
`a2803fd4807ccea23915e368d3c23455f80b88156df81bb4b744979df3ccd5aa`.
The frozen behavioral wave recovered 6/20 baseline misses and preserved all three
preselected prior-success controls. This targeted training validation is not a
held-out accuracy estimate.

Machine-readable provenance is in `manifest.json`.
