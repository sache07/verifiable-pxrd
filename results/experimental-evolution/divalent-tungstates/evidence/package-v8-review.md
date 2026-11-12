# v8 design

v8 is a replacement for v7, not an additive expansion. It preserves the
prospectively successful precursor/charge-balance and non-1:1 formula route,
the unchanged stoichiometric-analogue helper, watch-list reconvergence, and the
exact output-schema guard. It removes the requirement to construct exhaustive
per-phase audit tables.

One reusable executable is added: `cif_health.py` reports invalid, partial or
mixed occupancies; impossible contacts; and close O--O sites. It is read-only,
accepts arbitrary CIF paths, discloses overrideable distance defaults, and
labels warnings for chemical review rather than claiming stability or making
repairs. Retrospectively it separates every v7 source regression from 18
directly relevant physical v6 structures, but only the prospective v8 screen
can test adherence and scientific effect.

The guidance makes the replicated GSAS-II state error concrete: inactive size
is set to at least 10 micrometres, strain to zero, March ratio to one and
roughness to zero; refine flags alone are not neutralization. A concise numeric
spot check now has a stopping consequence: material structured mismatch or
excess goodness-of-fit requires a targeted correction and repeated check.
Finally, alternate records and polymorphs are competitors unless independent
unique families support coexistence, preventing c06's duplicate-WO3 surrogate.

No case identities, source IDs, hidden values, coordinates, fractions or
lookup rules are included. The analogue helper is copied byte-for-byte from
v7. The six-case initial screen will test all carried and transfer cases because
v7 has no 80+ set-aside success to protect.

Pre-freeze validation: guidance is 345 words with SHA-256
`3e8a25da91c998bdc2595878acc06336477338d4e8cc5f9c2745c1834c0b0935`;
`cif_health.py` is
`2e2d8abc4d563ba2011772b21714716557ead17663556eb2db2d1c0c4ca2da7f`;
the analogue helper remains
`0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`.
Both helpers pass their CLI smoke tests; the new report reproduces the expected
review/pass contrast on one flagged and one physical retained source.
