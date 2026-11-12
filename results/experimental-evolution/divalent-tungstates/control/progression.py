"""Mechanical checkpoint accounting; no scientific selection or score threshold."""

FRESH_PURPOSES = {'baseline', 'development', 'evaluation', 'diagnostic', 'transfer'}


def _walk(state, limit, proposed=(), purpose=None):
    """Classify every package solve in schedule order as counted, free or refused.

    A solve's cost depends on how many fresh solves its package already has on that
    case: under evaluation the 2nd and 3rd are free and the 1st counts. Once the
    budget is spent, one package may be completed to three solves per case run in
    this cycle, uncounted; everything else waits for the next comparison.
    """
    groups = sorted(state.get('groups', {}).values(),
                    key=lambda g: (g.get('created_at', ''), g['id']))
    jobs = state.get('jobs', {})
    completed, pending = [], []
    for index, group in enumerate(groups):
        if group.get('purpose') != 'transfer':
            continue
        ids = group.get('jobs', [])
        # A queued comparison, interruption or scoring error cannot close
        # the cycle. Recovery replaces the original slots in group.jobs.
        if ids and all(jobs.get(j, {}).get('status') == 'complete'
                       and jobs[j].get('collected') for j in ids):
            completed.append((index, group['id']))
        else:
            pending.append(group['id'])
    boundary = completed[-1][0] if completed else -1
    rows = [(index, group['purpose'], jobs.get(j, {}), False)
            for index, group in enumerate(groups) if group.get('purpose') in FRESH_PURPOSES
            for j in group.get('jobs', [])]
    rows += [(len(groups), purpose, job, True) for job in proposed]
    runs, cycle_cases, used, free, chosen, verdicts = {}, set(), 0, 0, None, []
    for index, kind, job, new in rows:
        policy, case = job.get('policy', 'P0'), job.get('case_id')
        n = runs.get((policy, case), 0)
        runs[(policy, case)] = n + 1
        verdict = None
        if index > boundary and kind != 'transfer' and policy != 'P0':
            if kind == 'evaluation' and n >= 3:
                verdict = 'repeat'
            elif kind == 'evaluation' and used >= limit:
                verdict = ('case' if case not in cycle_cases else
                           'package' if chosen not in (None, policy) else 'free')
                chosen = policy if verdict == 'free' else chosen
            elif kind == 'evaluation' and n:
                verdict = 'free'
            elif used >= limit:
                verdict = 'budget'
            else:
                verdict = 'counted'
                used += 1
            free += verdict == 'free'
        if index >= boundary and not new:
            cycle_cases.add(case)
        if new:
            verdicts.append((verdict, job))
    summary = {
        'cycle': len(completed) + 1,
        'development_solve_budget': limit,
        'development_solves_used': used,
        'evaluation_solves_free': free,
        'budget_reached': used >= limit,
        'package_completed_after_budget': chosen,
        'last_completed_comparison': completed[-1][1] if completed else None,
        'comparisons_pending': pending,
        'counting': 'Package solves since the last completed new-batch comparison count when queued; '
                    'recoveries replace their slot. Free: P0, the comparison, and a package\'s 2nd and '
                    '3rd solve on a case under evaluation. Once the budget is spent, one package may be '
                    'completed to three solves per case run this cycle under evaluation, uncounted.'
    }
    return summary, verdicts


def development_cycle(state, limit=30):
    return _walk(state, limit)[0]


def check_candidate_capacity(state, jobs, purpose, limit=30):
    if purpose == 'transfer':
        return
    used = development_cycle(state, limit)['development_solves_used']
    summary, verdicts = _walk(state, limit, jobs, purpose)
    needed = sum(v in ('counted', 'budget') for v, _ in verdicts)
    for verdict, job in verdicts:
        policy, case = job['policy'], job['case_id']
        if verdict == 'repeat':
            raise ValueError(f'{policy} already has three fresh solves on {case}; '
                             'further solves of it there are development runs.')
        if verdict == 'case':
            raise ValueError(f'{case} has not been run in this cycle. Once the budget is spent, '
                             'evaluation completes a package only on cases run in this cycle.')
        if verdict == 'package':
            raise ValueError(f"The budget is spent and {summary['package_completed_after_budget']} "
                             'is the package being completed by evaluation this cycle; other '
                             'packages wait for the next-batch P0/incumbent comparison.')
        if verdict == 'budget':
            raise ValueError(
                f'Development budget: {used} of {limit} package solves used this cycle; this '
                f'request needs {needed}. Once the budget is spent, one package may be completed '
                'to three solves per case run this cycle with --purpose evaluation, uncounted, '
                'before the next-batch P0/incumbent comparison. P0 runs and investigations remain '
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
