"""Mechanical cycle accounting: package versions per cycle and three solves per package and case."""

FRESH_PURPOSES = {'baseline', 'development', 'evaluation', 'diagnostic', 'transfer'}
SOLVES = 3


def _walk(state, limit, proposed=(), purpose=None):
    """Classify every package solve in schedule order.

    A cycle runs from one completed next-batch comparison to the next. Each non-P0 package
    run in it counts once, when its first solve is queued, except a package that was the
    frozen incumbent of a comparison; at most `limit` count. A package has at most three
    fresh solves on a case, and a request brings a package to three on each case it names.
    """
    groups = sorted(state.get('groups', {}).values(),
                    key=lambda g: (g.get('created_at', ''), g['id']))
    jobs = state.get('jobs', {})
    completed, pending, incumbent_from = [], [], {}
    for index, group in enumerate(groups):
        if group.get('purpose') != 'transfer':
            continue
        for policy in set(group.get('policies', [])) - {'P0'}:
            incumbent_from.setdefault(policy, index)
        ids = group.get('jobs', [])
        # A queued comparison, interruption or scoring error cannot close
        # the cycle. Recovery replaces the original slots in group.jobs.
        if ids and all(jobs.get(j, {}).get('status') == 'complete'
                       and jobs[j].get('collected') for j in ids):
            completed.append((index, group))
        else:
            pending.append(group['id'])
    boundary = completed[-1][0] if completed else -1
    rows = [(index, group['purpose'], jobs.get(j, {}), False)
            for index, group in enumerate(groups) if group.get('purpose') in FRESH_PURPOSES
            for j in group.get('jobs', [])]
    rows += [(len(groups), purpose, job, True) for job in proposed]
    runs, used, cycle_cases, verdicts = {}, [], {}, []
    for index, kind, job, new in rows:
        policy, case = job.get('policy', 'P0'), job.get('case_id')
        n = runs.get((policy, case), 0)
        runs[(policy, case)] = n + 1
        verdict = None
        if kind != 'transfer' and policy != 'P0':
            if n >= SOLVES:
                verdict = 'repeat'
            elif (index > boundary and policy not in used
                  and not index > incumbent_from.get(policy, len(groups) + 1)):
                verdict = 'budget' if len(used) >= limit else 'counted'
                if verdict == 'counted':
                    used.append(policy)
        if index > boundary and kind != 'transfer' and not new:
            cycle_cases.setdefault(policy, set()).add(case)
        if new:
            verdicts.append((verdict, job))
    last = completed[-1][1] if completed else None
    summary = {
        'cycle': len(completed) + 1,
        'candidates_allowed': limit,
        'candidates_used': len(used),
        'candidates': used,
        'candidates_spent': len(used) >= limit,
        'cycle_cases': {p: sorted(c) for p, c in sorted(cycle_cases.items())},
        'last_completed_comparison': last['id'] if last else None,
        'comparison_cases': sorted(last.get('cases', [])) if last else [],
        'comparisons_pending': pending,
        'counting': 'Each package run since the last completed new-batch comparison counts once, when its '
                    'first solve is queued; P0, the comparison and packages that were a comparison\'s '
                    'incumbent do not count. Each package is solved three times on each case, in one request.'
    }
    return summary, verdicts


def development_cycle(state, limit=3):
    return _walk(state, limit)[0]


def check_candidate_capacity(state, jobs, purpose, limit=3):
    if purpose == 'transfer':
        return
    summary, verdicts = _walk(state, limit, jobs, purpose)
    requested = {}
    for job in jobs:
        if job['policy'] != 'P0':
            key = (job['policy'], job['case_id'])
            requested[key] = requested.get(key, 0) + 1
    for (policy, case), n in requested.items():
        if n < SOLVES:
            raise ValueError(f'Each package is evaluated with three solves per case in one request; '
                             f'this request has {n} of {policy} on {case}. Use --repeats 3.')
    for verdict, job in verdicts:
        policy, case = job['policy'], job['case_id']
        if verdict == 'repeat':
            raise ValueError(f'{policy} already has three fresh solves on {case}; its evaluation there is complete.')
        if verdict == 'budget':
            raise ValueError(
                f"{limit} package versions have been evaluated this cycle ({', '.join(summary['candidates'])}). "
                'The next-batch P0/incumbent comparison comes next; P0 runs and investigations remain '
                'available. See evidence/status.json development_cycle.'
            )


def require_transfer_complete(state, batch_id):
    """Old-case investigations may run while a new comparison is pending."""
    batch = state['batches'][batch_id]
    if batch['kind'] != 'transfer':
        return
    group = state.get('groups', {}).get(batch.get('transfer_group'), {})
    ids = group.get('jobs', [])
    if not ids or not all(state['jobs'].get(j, {}).get('status') == 'complete'
                          and state['jobs'][j].get('collected') for j in ids):
        raise ValueError('Complete and collect the frozen P0/incumbent comparison on this '
                         'new batch before development runs or scored investigations on '
                         'its cases. Earlier-case work remains available.')
