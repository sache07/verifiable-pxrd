# Texture-axis comparison preregistration

## Claim under test

The independent v1 and v2 c05 solves both retained a dominant-phase [001]
March--Dollase term near 0.894, while width refinements alone left systematic
intensity error. Starting from each physical endpoint, retain every submitted
structure, width, angular, and background choice. For the one already textured
phase, compare no texture with all primitive first-shell directions whose
indices are zero or one. Reset every directional branch to the same submitted
ratio and use an identical reconvergence schedule; select by stored Rwp, then
evaluate that selected project by fresh replay.

## Predictions and decision rule

- Support requires the same crystallographic direction family to beat [001]
  in both endpoints, lower fresh-replay D in both, and preserve physical replay
  and inventory. A tiny stored-Rwp difference without D improvement is not
  support.
- A texture-free selection would instead show that the retained terms were
  nuisance surrogates and should be pruned.
- Different winners, bound-seeking ratios, or degradation in either endpoint
  reject automatic axis enumeration. At most, v3 may then ask solvers to compare
  plausible axes using diagnostic intensity families; this script is not a
  candidate package helper without prospective transfer evidence.

The test is oracle-informed only in identifying texture allocation as a
possible mechanism. It contains no case formula, hidden coordinate, fitted
answer, or generator-specific axis list.
