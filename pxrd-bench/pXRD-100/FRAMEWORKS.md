# Public inference contract

The released coding-agent condition exposes only the reduced composition and the
corresponding CSV in `targets/fixedparams-v1/patterns-fixedparams/`. It does not expose
the reference CIF, source material identifier, category, space group, cell, or full-cell
composition.

All cases use one controlled profile: monochromatic Cu Kalpha1 at 1.5406 Angstrom,
5--90 degrees two-theta on a 0.01-degree grid, with the instrument, sample-broadening,
noise, and seed values recorded in `targets/fixedparams-v1/parameters.json`. The target
manifest binds every input to the top-level source manifest and records its SHA-256.

The generic runner stages only `pattern.csv` in each isolated workspace and supplies the
reduced formula through the frozen prompt. See `../../docs/METHODS.md` for the exact
recovery metric and `../generation/README.md` for deterministic replay.

The original research repository also prepared inputs for several published specialist
baselines. Those larger framework-specific target and result trees are not necessary for
the coding-agent experiments and are not bundled in this initial public scaffold.
