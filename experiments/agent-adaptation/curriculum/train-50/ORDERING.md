# Training order provenance

`problem-order.csv` is the authoritative ordering of the frozen 50-problem
selection.

The order was constructed only from metadata fixed before trainee execution:
benchmark category, source dataset, primitive-site count/bin, crystal system,
element count, challenge axis, and polymorph difficulty/family. It balances
cumulative prefixes and the initial eight-case bootstrap, then balances later
four-case waves where feasible. Members of a polymorph family are separated.
No materials-science-agent, workbench, trainee, verifier, Rwp, or other outcome was an input.

Before the 2026-08-18 clean rerun, positions 7 and 10 were deliberately swapped:
`vp-034` moved into the bootstrap and `vp-046` moved into the first rolling
wave. This was a scheduling adjustment informed by the preceding pilot, not a
change to collection membership. The revised bootstrap contains six categories,
all five site-count bins, six crystal systems, five pXRD-100-style cases, and
three OOD cases. Its mean primitive-site count is 11.50, compared with 12.02
for all 50.

For the original outcome-blind order, an independent audit found archived
materials-science-agent outcomes for 41 cases. Matsci-agent success was 4/7 known cases in positions
1-8, 9/13 in positions 1-15, and 8/13 in positions 36-50, versus 26/41 overall.
Those prefix figures describe the archived original order, not the revised
schedule.

The newline-delimited order has SHA-256
`19bc74667063cb2377f20765d9d0a7ff791434435911e2784c6245b8eb52287f`.
