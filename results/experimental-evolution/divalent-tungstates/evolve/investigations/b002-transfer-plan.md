# b002 transfer analysis plan (written before outcomes)

The frozen comparison is `b002-transfer-p0-v6-r3`: three fresh P0 and three
fresh v6 solves on each of b002-c01 and b002-c02. Do not inspect or diagnose
individual attempts until all 12 slots terminate.

Report the new-case comparison separately from the learned b001 cases. For each
case and policy, compute the three-score mean, population standard deviation,
range, count above 80, physical-validity count, complete-framework-inventory
count, maximum fraction errors, profile D/Rwp relative to the frozen floor, and
source/framework choices. Use all scientifically failed attempts in the means;
do not discard provisional failures merely because exclusion improves a
condition.

Transfer is strong only if v6's intended behavior is visible in execution and
not merely in a favorable aggregate score:

- c01: complete MgWO4/MgO/WO3 inventory, physical sources, and phase-specific
  profile handling should replicate across rollouts.
- c02: complete four-phase inventory, rejection of the disordered exact BaWO4
  record, ordered-scheelite analogue adaptation, and physical replay should
  replicate across rollouts.
- For both cases, compare v6 directly with the same-case P0 distribution. Mark
  any inventory/source gain separately from remaining profile or quantitative
  error. A case mean above P0 is necessary evidence of positive transfer;
  mostly 80+ rollouts and a mean above 80 are the stronger success criterion.

After comparison, the six-case active panel is b001-c03--c06 plus b002-c01--c02.
The four b001 cases retain their existing v6 evaluation evidence and are not
relabelled as transfer cases. Design the next package from mechanisms that are
replicated across this full panel, preserving v6 behavior that transfers and
replacing rather than appending interventions that fail. Use new explicit
requests for carried b001 cases during development; never regenerate them in
b002.
