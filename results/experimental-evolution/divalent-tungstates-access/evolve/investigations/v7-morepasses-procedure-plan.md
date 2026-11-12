# Prospective five-pass procedure-test plan

Status: complete and passed as `ptest-v7-morepasses-04`. See
`investigations/v7-morepasses-procedure-result.md`.

## Change under test

Use `investigations/v7-prototype/staged_polish_morepasses.py`, SHA-256
`954ecebf0bbb6445cdac938860abb83f8c0c55ba4789fcdd9c87af0a8349d6fe`.
It is byte-for-byte equivalent to frozen v6 helper `c022d606...` except that
the fixed maximum coordinate-stabilization passes is five rather than three.
All convergence, rollback, fraction, geometry and minimum-gain gates remain
unchanged.

## Core panel

Repeat the prior eight-project no-harm panel so every endpoint can be compared
both with its source and with `ptest-v6-staged-covfix-02`:

- `b003-v4-v5-a02e30914a71`
- `b003-v4-v5-92b88601b429`
- `b003-v4-v5-856dde72f4da`
- `b003-v4-v5-ad16ddf37d6f`
- `b002-v4-v5-99637c5841ce`
- `b002-v4-v5-8bda9314cb4f`
- `b001-v4-v5-b9e3a697c8a5`
- `b001-v4-v5-a49a4302f681`

Add fresh v6 endpoints that separate the observed mechanisms:

- c03: `b001-v6-c1622f1955d4`, `b001-v6-1862b20be476`,
  `b001-v6-a8e159045358` (the known three-pass false rejection);
- harder Zn: recovered `b002-v6-efdf82b5144b` and poor-registry
  `b002-v6-4231c2299c73`, `b002-v6-57d5c04ba22f`;
- floor c02: `b001-v6-242b3796d085`;
- tier-1 c06: recovered/post-polish `b001-v6-72423d721f82` and exact-helper
  `b001-v6-d0efe3967c0b`;
- exact-inventory b003: `b003-v6-e01220925a6c`.

Add later v6 b003 endpoints only if their completed audits expose a distinct
coordinate-convergence state. Do not outcome-select additional cases merely
because they would improve the aggregate diagnostic.

## Prospective criteria

1. Every selected project executes and every output passes the physical screen.
2. No previously recovered control worsens hidden D by more than 0.10, and no
   source project worsens by more than 0.10.
3. The six improvements and two baseline returns from the prior eight-project
   test are retained within 0.05 D; an extra pass must not sacrifice the v6
   helper's established benefit/no-harm behavior.
4. Fresh c03 rep3 must reproduce the direct diagnostic's material gain and
   recovery (D <= 1); this is the causal target.
5. Improvements on other fresh failures are welcome but not required. In
   particular, unchanged poor-registry harder-Zn outputs count as confirmation
   that a larger local budget does not replace parent multistart.

Passing this test licenses only the constant change for a prospective package.
It does not validate source-residue closure, parent multistart, or terminal
helper ordering; those remain separate behavioral interventions.
