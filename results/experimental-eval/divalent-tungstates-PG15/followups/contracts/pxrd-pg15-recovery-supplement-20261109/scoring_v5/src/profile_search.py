"""Observed-data selection of optional per-phase specimen profile settings.

Structures and submitted mass fractions stay fixed. Specimen settings come only
from the frozen lab grid, never the hidden per-phase realization. Small grids
are enumerated; larger ones use deterministic multiple-start coordinate search.
"""
from itertools import product
import math
import numpy as np
from scipy.optimize import nnls
from common import components, fit_profiles, ROOT
from specimen import profile_options, enabled


class ProfileObjective:
    def __init__(self, x, y, banks, fractions):
        self.banks = banks
        self.fractions = None if fractions is None else np.asarray(fractions, float)
        self.offsets = np.cumsum([0] + [len(b) for b in banks])[:-1]
        profiles = np.concatenate(banks)
        norm = float(np.max(profiles))
        if norm <= 0:
            raise ValueError('Zero profile bank')
        t = (x-x[0])/(x[-1]-x[0])
        background = np.column_stack(((1-t)**2, 2*t*(1-t), t*t))
        A = np.column_stack((profiles.T/norm, background))
        weight = 1/np.maximum(y, 1.)
        self.gram = A.T @ (weight[:, None]*A)
        self.rhs = A.T @ (weight*y)
        self.yy = float(np.sum(weight*y*y))
        self.background_indices = list(range(len(profiles), len(profiles)+3))
        self.memo = {}

    def loss(self, choice):
        choice = tuple(choice)
        if choice in self.memo:
            return self.memo[choice]
        idx = [int(o+c) for o,c in zip(self.offsets, choice)] + self.background_indices
        G, b = self.gram[np.ix_(idx, idx)], self.rhs[idx]
        if self.fractions is not None:
            mapping = np.zeros((len(idx), 4))
            mapping[:-3, 0] = self.fractions
            mapping[-3:, 1:] = np.eye(3)
            G, b = mapping.T @ G @ mapping, mapping.T @ b
        # Solve the same nonnegative least-squares problem using its small Gram
        # matrix. Column equilibration and eigendecomposition tolerate redundant
        # phases without introducing a ridge or changing the objective.
        scale = np.sqrt(np.maximum(np.diag(G), 1e-300))
        gram = G / scale[:, None] / scale[None, :]
        rhs = b/scale
        eigenvalues, vectors = np.linalg.eigh(gram)
        mask = eigenvalues > max(float(eigenvalues[-1]), 1.)*1e-12
        roots = np.sqrt(eigenvalues[mask])
        matrix = roots[:, None]*vectors[:, mask].T
        target = (vectors[:, mask].T @ rhs)/roots
        coef, _ = nnls(matrix, target, maxiter=max(1000, 10*len(rhs)))
        coef = coef/scale
        loss = max(0., float(self.yy - 2*coef@b + coef@G@coef))
        self.memo[choice] = loss
        return loss


def select_profiles(objective, options, policy):
    counts = [len(o) for o in options]
    combinations = math.prod(counts)
    exact_limit = int(policy['exhaustive_max_combinations'])
    if combinations <= exact_limit:
        best = min(product(*(range(n) for n in counts)), key=objective.loss)
        return best, {'method': 'exhaustive finite-grid search', 'combinations': combinations,
                      'evaluated': len(objective.memo), 'converged': True}
    starts = int(policy['coordinate_starts'])
    passes = int(policy['coordinate_max_passes'])
    rng = np.random.default_rng(57219)
    default = tuple(min(range(len(o)), key=lambda j: abs(o[j]['size_um']-.3)
                        + o[j]['microstrain_ppm']/1000 + abs(o[j]['md_ratio']-1)) for o in options)
    initial = [default, tuple(0 for _ in counts)]
    initial += [tuple(int(rng.integers(n)) for n in counts) for _ in range(max(0, starts-2))]
    finalists, convergence = [], []
    for init in initial:
        current = init
        converged = False
        for _ in range(passes):
            before = objective.loss(current)
            for phase, count in enumerate(counts):
                candidates = [current[:phase]+(j,)+current[phase+1:] for j in range(count)]
                candidate = min(candidates, key=objective.loss)
                if objective.loss(candidate) < objective.loss(current)-1e-7:
                    current = candidate
            if objective.loss(current) >= before-1e-7:
                converged = True
                break
        finalists.append(current); convergence.append(converged)
    winner = min(range(len(finalists)), key=lambda j: objective.loss(finalists[j]))
    if not convergence[winner]:
        raise RuntimeError('Independent optional-profile search did not converge; evaluator error, not solver failure')
    return finalists[winner], {'method':'deterministic multiple-start coordinate search',
        'combinations':combinations, 'evaluated':len(objective.memo), 'converged':True,
        'starts':len(initial), 'global_optimum_guaranteed':False,
        'start_final_losses':[objective.loss(c) for c in finalists]}


def calculate_optional_profiles(paths, weights, protocol, x, y, out, eligible):
    policy = protocol['verification']['optional_profile_search']
    common_sizes = [protocol['generation']['domain_size_um'][0]] if enabled(protocol, 'phase_specific_sizes') else protocol['generation']['domain_size_um']
    best = free_best = None
    evidence = []
    for size in common_sizes:
        options = [profile_options(protocol, size) for _ in paths]
        banks = []
        for path, opts in zip(paths, options):
            xx, bank, proof = components([path], protocol, size, out/'cache', profile_variants=[opts])
            if xx.shape != x.shape or not np.allclose(xx, x, atol=1e-7, rtol=0):
                raise ValueError('Optional-profile grid mismatch')
            banks.append(bank)
        results = {}
        for label, fractions in [('fixed', np.asarray(weights))] * int(eligible) + [('free', None)]:
            objective = ProfileObjective(x, y, banks, fractions)
            choice, search = select_profiles(objective, options, policy)
            profiles = np.asarray([bank[j] for bank,j in zip(banks, choice)])
            fit = fit_profiles(x, y, profiles, fixed_fractions=fractions, allow_shift=False)
            if not np.isclose(objective.loss(choice), fit['chi_square'], rtol=1e-6, atol=1e-4):
                raise RuntimeError('Optional-profile objective disagrees with full-grid NNLS')
            fit['domain_size_um'] = None if enabled(protocol, 'phase_specific_sizes') else size
            fit['phase_profile_settings'] = [opts[j] for opts,j in zip(options, choice)]
            fit['profile_search'] = search
            results[label] = fit
        if eligible and (best is None or results['fixed']['chi_square'] < best['chi_square']):
            best = results['fixed']
        if free_best is None or results['free']['chi_square'] < free_best['chi_square']:
            free_best = results['free']
        evidence.append({'common_size_um':None if enabled(protocol, 'phase_specific_sizes') else size,
                         'variants_per_submitted_phase':[len(o) for o in options],
                         'selection':'observed-data weighted least squares only; no true specimen settings used',
                         'searches':{key:value['profile_search'] for key,value in results.items()}})
    return best, free_best, evidence, None
