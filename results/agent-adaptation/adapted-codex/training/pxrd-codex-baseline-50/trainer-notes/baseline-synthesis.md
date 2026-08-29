# Baseline synthesis for the first capability revision

## Evidence reviewed

The declared baseline is complete: 50/50 closed attempts, 30 `selected_exact`, 30
`candidates_exact`, and 20 misses. I reviewed the common solve prompt, every episode and
verifier result, chronological trainee messages and command traces, final responses,
retained workspaces, all declared CIFs, all other retained CIFs, and the now-visible
references. I also compared candidate/reference structures with the verifier matcher,
a scale-enabled element matcher, and a species-agnostic framework matcher. No undeclared
or held-out material was used.

## Failure layers and motivating problems

Five misses crossed the lattice/topology gap but failed at the concrete element-specific
periodic realization:

- `vp-004`: the submitted ZnSnBiAs cell and unlabeled framework match the reference, but
  three of four element assignments differ. The trainee explicitly collapsed numerical
  orderings as origin/axis copies and declared only one CIF.
- `vp-002`: the framework matches, but the submission represents Si/C as a 50:50 average
  site while the reference has a periodic Si/C ordering.
- `vp-018`: the framework matches, but one As/Se pair is interchanged; no alternative was
  materialized.
- `vp-045`: the framework matches, but the submission interchanges In/Sb and several
  Cl/F sites; it declared one apparently unique ordering.
- `vp-049`: the perovskite framework matches, but Ti/Fe are represented by a 75:25
  average site rather than the ordered periodic realization.

These are distinct from the remaining structural misses. `vp-006`, `vp-017`, `vp-034`,
`vp-039`, `vp-043`, `vp-046`, and `vp-048` instantiate a different cell, symmetry, site
count, or framework. `vp-005`, `vp-026`, `vp-028`, `vp-031`, `vp-041`, and `vp-047`
recover useful metric or family information but not reference-matching coordinates and
topology. Their detailed scientific diagnoses do not justify trainee-facing workflow or
branch advice.

Two misses fail at the artifact layer despite meaningful progress. `vp-015` timed out
after reporting a chemically valid C2 hypothesis with profile correlation about 0.914,
but declared no CIF. `vp-037` stopped after decisive tetragonal indexing and also declared
no CIF. `vp-006` timed out but did at least leave parseable selected and alternative CIFs.
No undeclared retained CIF in any miss matched the reference, so there is no broader
"copy every intermediate" lesson.

Successful controls show the behavior to preserve. `vp-001`, `vp-010`, `vp-012`,
`vp-020`, and `vp-036` explicitly discriminate element-to-site assignments and select the
correct ordered realization. `vp-014` preserves a genuinely competitive light-anion
ordering as an alternative while keeping the exact ordering selected. `vp-013` and
`vp-029` safely materialize homometric representations. These successes argue for a
narrow representation/output reminder, not a prescribed solve workflow.

## Repeated backend-interface mechanism

DICVOL14 is present but its executable exposes no usable `--help`; it prompts for a native
input filename, returns success even for malformed input, and uses an undocumented
five-line header. Thirty-five of 50 trainees contacted this direct interface. The traces
contain 50 prompt encounters and 25 explicit open/header errors, including repeated
line-2 failures in `vp-006`, `vp-015`, `vp-034`, and `vp-043`; no baseline trace reached an
actual DICVOL search. Both successful and failed solvers lost commands probing the binary,
GSAS-II source, or guessed input layouts.

A controlled probe of the declared binary reconstructed and validated the native contract:

1. title;
2. number of lines, input kind (0 Q, 1 theta, 2 two-theta, 3 d), then flags for cubic,
   tetragonal, hexagonal, orthorhombic, monoclinic, and triclinic;
3. a/b/c maxima, volume minimum/maximum, beta minimum/maximum;
4. wavelength;
5. experimental error, minimum FOM, tolerated unindexed lines, zero shift, and its refine
   flag; followed by the chosen peak values.

On a sealed mechanical probe generated from closed `vp-010`, this format invoked a real
cubic search and returned a = 5.7085 A, matching the known closed-case cell. This validates
the tool contract only; it is not a substitute for a fresh blind wave.

## Proposed coherent intervention

Keep `SKILL.md` below 200 words and limit it to the declared artifact contract:

- only named CIFs are graded;
- candidates are element-specific, periodic, occupancy-specific, and scale-sensitive;
- average disorder, an uninstantiated site permutation, or an indexed cell is not the same
  candidate;
- keep a parseable `selected.cif` current once a concrete model exists;
- materialize only a few genuinely surviving orderings/realizations as alternatives;
- round-trip the formula, occupancies, cell, and coordinates.

Add one neutral executable, `bin/dicvol14-adapter`. It will accept an explicit peak list,
input kind, wavelength, selected crystal systems, search bounds, and native control values;
generate the native file; invoke the existing `dicvol14`; retain the `.dat`, `.ind`, `.ucp`,
console logs, summary files, and JSON provenance; expose every backend result without
ranking; refuse implicit peak picking; and return nonzero on interface/backend errors.
The skill may neutrally name the adapter but must not recommend when to use it.

## Behavioral prediction and transfer

- On `vp-004`, `vp-002`, `vp-018`, `vp-045`, and `vp-049`, trainees should be less likely
  to collapse unresolved element order into one average/disordered CIF. At least some
  should improve `candidates_exact`; better-supported ordering may also improve
  `selected_exact`.
- On `vp-015` and `vp-037`, a concrete model should be declared before a long final search,
  avoiding a zero-artifact verifier result.
- Across indexing-heavy failures, especially `vp-006`, `vp-015`, `vp-034`, and `vp-043`,
  DICVOL engagement should become an actual native search rather than help/format probing.
- The interface adapter should transfer to any composition because it contains no case
  diagnosis, reference data, scientific ranking, or workflow routing.
- Prior successes should retain their unconstrained scientific behavior because the
  revision adds no crystallographic gates, search order, prototype policy, or solver route.

## Regression risks and controls

The representation reminder could encourage combinatorial alternatives or demote a strong
primary. Wording will limit alternatives to a few surviving periodic models and keep
`selected.cif` as the best-supported model. Early declaration could preserve a weak
provisional file; wording will require keeping it current, not freezing it. The adapter
could invite indiscriminate or long indexing runs; its CLI will require explicit systems
and chosen peaks, preserve backend no-solution results, offer a user-selected timeout, and
perform no peak selection or scientific ranking. A prior-success regression case will be
included in the blind wave.
