# Research environment

This project is one continuing research task. Follow PROMPT.md. The user will decide when to stop; there is no total rollout or elapsed-time budget.

Before scientific work, run `python verify_environment.py` directly in this app task. If it fails, report the failing checks and wait for the access setting to be corrected. Do not nest it inside another sandbox, broaden permissions, or proceed under Full access. Select gpt-5.6-sol, Max, and the `pxrd-divalent-tungstates-access` custom permission profile.

Use `lab.py` to request isolated solver experiments. This is the authorized route to additional Sol workers. Do not launch other models, use web/search/connectors, seek historical experiments, or access external answers. The controller handles credentials and EC2 outside your command sandbox. Your own source models, synthetic truth, and returned scientific artifacts are available for investigation; fresh solvers receive only their assigned inputs, database, and frozen package.

Keep case answers, hidden cells, coordinates, fractions, reference files, and case-specific lookup rules out of reusable packages. Oracle-informed diagnostics establish a possible mechanism, not blind recovery. Do not modify the frozen physics, scorer, baseline, or archived experiments. Ask for an infrastructure repair if these are wrong; continue independent work when possible.

Maintain a short STATE.md with a table of all solve scores, the current package, active cases, unfinished hypotheses, pending request IDs, and next action. Update it before long waits and compaction. Read it and controller status when resuming. Requests are durable; never repeat a launch under a new ID merely because a response is slow. Never set `autoResolutionMs` when requesting user input.

A `STOP.md` in this folder, or a controller pause recorded as a user stop, ends the current authorization: do not file recovery or resume requests, remove the marker, or restart work until the user explicitly says to resume. The original task message never re-authorizes work after such a stop.

Process-monitor notices printed by `lab.py` are authorized reminders to reassess priorities; briefly acknowledge the notice and state your next-step decision, using scientific judgment and the original task.
