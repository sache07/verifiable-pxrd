# v11 design

## Evidence target

v10 achieved physical, strict formula inventory on all three unresolved cases but scored only 53.39 on average. Its saved-boundary, chemistry, weak-phase and coexistence clauses worked. The common failure was irreversible temporal ordering: common widths, phase size/strain, geometry, shared-intensity terms, texture and source ranking were each challenged once, then treated as final despite later changes to coupled terms.

## Minimal replacement

v11 keeps the two v10 helpers byte-identical and preserves its inventory, fixed-balance, constructed-analogue, weak-phase, coexistence and output-schema gates. It replaces the profile/source section with one reversible coordinate-descent loop:

- reopen common profile and angular correction;
- compare neutral, size, strain and combined size-plus-strain from the same checkpoint, followed by symmetry-compatible anisotropy;
- compare background/polarization/roughness before low-index March texture;
- repeat after every accepted chemistry, geometry, intensity, texture or broadening change until terms, fractions and source ranking are stable.

Every serious source/polymorph receives its own neutral-to-converged symmetry-appropriate loop. Lower symmetry additionally needs observed diagnostic splitting/families and a stable equal-loop advantage, preventing profile error from being purchased with lattice flexibility. Bound branches still reload saved values and receive a physically meaningful boundary retest.

This is a procedural replacement rather than added tooling. The guidance is 472 words, versus 506 in v10.

## Integrity

- guidance SHA-256: `9f687f264e8a12d82952f18a2332c942e9210b3efe214d058cf9df8ba6756ab5`
- CIF-health helper: `2e2d8abc4d563ba2011772b21714716557ead17663556eb2db2d1c0c4ca2da7f`
- analogue helper: `0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`
- both helpers are byte-identical to v10; CLI smoke tests pass
- no case identity, source identifier, fitted value or hidden answer appears in the package

## Prospective test

Run one development solve on unresolved c03/c05/c06. Hold c04 and both b002 controls until the new mechanism improves the unresolved screen; otherwise preserve rollout budget for another diagnosis.
