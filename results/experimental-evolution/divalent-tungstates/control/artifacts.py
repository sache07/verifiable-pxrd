"""Freeze and audit cases and packages; reproduce forward data before dispatch."""
from pathlib import Path
import ast
import hashlib
import json
import shutil
import sys
import warnings

import numpy as np

from common import ROOT, WORK, read, save, sha, ident, under, copy_science, hashes, register_truth


def guidance_budget(folder, limit=2000):
    """All worker-level documents share the cap; helper code/help are optional.

    Whitespace-delimited words, including headings and examples. Semantic
    attempts to hide mandatory instructions in code/help remain audit concerns.
    """
    names = ['guidance.md', 'TOOLS.md', 'AGENTS.md', 'OUTPUT_SCHEMA.md']
    counts = {name: len((folder / name).read_text().split())
              for name in names if (folder / name).is_file()}
    total = sum(counts.values())
    if total > limit:
        raise ValueError(f'Additional worker guidance is {total} words; the limit is {limit} '
                         f'across worker documents: {counts}. Consolidate before freezing. '
                         'Do not move required instructions into helpers or optional help.')
    return {'limit': limit, 'total_words': total, 'words_by_file': counts,
            'excludes': 'Fixed P0, executable helpers, optional on-demand helper documentation.'}


def structure_mixture(truth):
    """Registered models and mass fractions, independent of measurement effects.

    Thermal variants retain their original registered model hash. This is an
    exact model-reuse check, not a claim to detect all equivalent structures.
    """
    weights = {}
    for phase, fraction in zip(truth['phases'], truth['true_fractions']):
        model = phase.get('parent_model_sha256', phase['model_sha256'])
        weights[model] = weights.get(model, 0.) + float(fraction)
    return tuple(sorted((model, round(weight, 12)) for model, weight in weights.items()))


def freeze_batch(request):
    bid = ident(request['batch'])
    source_manifest = under(WORK, request['manifest'])
    source_pool = under(WORK, request['pool'])
    notes = under(WORK, request['notes'])
    if not notes.read_text().strip():
        raise ValueError('Batch scientific rationale and source review are required')
    manifest = read(source_manifest)
    sys.path.insert(0, str(ROOT / 'runtime'))
    from labspec import protocol as lab_protocol
    protocol = lab_protocol(WORK / 'LAB.md')
    if manifest.get('lab_sha256') != sha(WORK / 'LAB.md'):
        raise ValueError('The manifest lab_sha256 must match the frozen LAB.md')
    if manifest.get('source_pool_sha256') != sha(source_pool / 'catalog.json'):
        raise ValueError('Pool manifest checksum mismatch')
    if not manifest.get('cases') or len({r['id'] for r in manifest['cases']}) != len(manifest['cases']):
        raise ValueError('Empty batch or duplicate case IDs')
    base = ROOT / 'batches' / bid
    if base.exists():
        raise ValueError('Batch ID already exists; inspect it rather than overwriting it')
    for row in manifest['cases']:
        ident(row['id'])
        if (ROOT / 'cases' / row['id']).exists():
            raise ValueError('Case ID already frozen: ' + row['id'])
    stage = ROOT / 'control/staging' / bid
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    copy_science(source_pool, stage / 'pool')
    catalog = read(stage / 'pool/catalog.json')
    for row in catalog['records']:
        for key, hkey in [('model_path', 'model_sha256'), ('source_path', 'source_sha256')]:
            p = under(stage / 'pool', row[key])
            if sha(p) != row[hkey]:
                raise ValueError('Source/model hash changed: ' + row['id'])
        if not row.get('provenance') or not row.get('lineage_group'):
            raise ValueError('Missing source provenance')
    shutil.copy2(source_manifest, stage / 'manifest.json')
    shutil.copy2(notes, stage / 'review.md')
    sys.path.insert(0, str(ROOT / 'runtime'))
    from generate import generate_one
    # The frozen scorer has a module named common too: audit in a separate process.
    summaries = []
    prior = []
    for tp in (ROOT / 'cases').glob('*/private/truth.json'):
        t = read(tp)
        fp = np.load(tp.parent / 'forward.npz')
        signature = hashlib.sha256(np.round(fp['x'], 8).tobytes() + np.round(fp['mean'], 8).tobytes()).hexdigest()
        prior.append({'case': tp.parent.parent.name, 'expected_signal': signature,
                      'structure_mixture': structure_mixture(t),
                      'compositions': sorted(ph['composition_key'] for ph in t['phases'])})
    for recipe in manifest['cases']:
        check = generate_one(recipe, stage / 'pool', protocol, stage / 'cases', ROOT / 'control/forward_cache')
        case = stage / 'cases' / recipe['id']
        truth = read(case / 'private/truth.json')
        fwd = np.load(case / 'private/forward.npz')
        y = np.loadtxt(case / 'inputs/pattern.csv', delimiter=',', skiprows=1)
        if not (np.isfinite(fwd['mean']).all() and (fwd['mean'] > 0).all()):
            raise ValueError('Invalid expected counts')
        assert np.allclose(fwd['mean'], np.array(truth['true_fractions']) @ fwd['profiles'] * fwd['normalization'] + fwd['background'])
        assert np.array_equal(np.random.default_rng(recipe['seed']).poisson(fwd['mean']), y[:, 1])
        assert np.allclose(y[:, 0], fwd['x'], atol=1e-8)
        signature = hashlib.sha256(np.round(fwd['x'], 8).tobytes() + np.round(fwd['mean'], 8).tobytes()).hexdigest()
        same_signal = [p['case'] for p in prior if p['expected_signal'] == signature]
        mixture = structure_mixture(truth)
        same_mixture = [p['case'] for p in prior if p['structure_mixture'] == mixture]
        overlap = [p['case'] for p in prior if p['compositions'] == sorted(ph['composition_key'] for ph in truth['phases'])]
        if request.get('kind') == 'transfer' and same_signal:
            raise ValueError('A noise replica of an existing signal is not a new transfer case: ' + recipe['id'])
        if request.get('kind') == 'transfer' and same_mixture:
            raise ValueError('Transfer case reuses the same registered structures and fractions as ' + ', '.join(same_mixture)
                             + ': ' + recipe['id'] + '. Use a learning or diagnostic batch for measurement/resource variants.')
        summaries.append({'case': recipe['id'], 'checks': check, 'truth_sha256': sha(case / 'private/truth.json'),
                          'novelty': {'same_expected_signal': same_signal, 'same_structures_and_fractions': same_mixture,
                                      'same_composition_assemblage': overlap,
                                      'note': 'Composition overlap can still involve new structures or a new question; explain it in the review.'}})
        prior.append({'case': recipe['id'], 'expected_signal': signature, 'structure_mixture': mixture,
                      'compositions': sorted(ph['composition_key'] for ph in truth['phases'])})
    import subprocess
    from common import CORE
    p = subprocess.run([CORE, str(ROOT / 'control/scoring.py'), 'audit', str(stage / 'cases')], capture_output=True, text=True, check=True)
    physical = json.loads(p.stdout)
    flagged = [cid for cid, rows in physical.items() if any(x['status'] != 'pass' for x in rows)]
    if flagged and request.get('kind', 'learning') != 'diagnostic':
        save(stage / 'physical_review.json', physical)
        raise ValueError('Reference physical review required. Repair with evidence or freeze as diagnostic-only: ' + ', '.join(flagged))
    diagnostic = request.get('kind', 'learning') == 'diagnostic'
    save(stage / 'audit.json', {'cases': summaries, 'physical': physical, 'diagnostic_only': diagnostic,
                              'limitations': 'Omission and known-phase checks do not establish unique solutions or difficulty.'})
    base.parent.mkdir(parents=True, exist_ok=True)
    stage.rename(base)
    for row in manifest['cases']:
        cid = row['id']
        (base / 'cases' / cid).rename(ROOT / 'cases' / cid)
        register_truth(ROOT / 'cases' / cid)
    (base / 'cases').rmdir()
    record = {'id': bid, 'kind': request.get('kind', 'learning'), 'cases': [x['id'] for x in manifest['cases']],
              'incumbent': request.get('incumbent', 'P0'), 'manifest_sha256': sha(base / 'manifest.json'),
              'audit': str(base / 'audit.json'), 'diagnostic_only': diagnostic, 'transfer_group': None}
    save(base / 'record.json', record)
    save(base / 'frozen.json', {'files': hashes(base), 'cases': {cid: hashes(ROOT / 'cases' / cid) for cid in record['cases']}})
    return record


def freeze_package(request):
    pid = ident(request['package'])
    if pid == 'P0' or (ROOT / 'policies' / pid).exists():
        raise ValueError('Package IDs are immutable; use a new version')
    source = under(WORK, request['path'])
    guidance = source / 'guidance.md'
    if not guidance.is_file():
        raise ValueError('Package requires guidance.md (may be empty for a tools-only change)')
    notes = under(WORK, request['notes'])
    if not notes.read_text().strip():
        raise ValueError('Provide mechanism, validation evidence, limitations and information audit')
    stage = ROOT / 'control/staging' / ('package-' + pid)
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    copy_science(source, stage)
    allowed_docs = {'guidance.md', 'TOOLS.md', 'AGENTS.md', 'OUTPUT_SCHEMA.md'}
    for p in stage.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(stage)
        if rel.parts[0] != 'helpers' and str(rel) not in allowed_docs:
            raise ValueError('Deliver only guidance.md, optional worker documents and helpers/: ' + str(rel))
        if p.suffix.lower() in {'.cif', '.gpx', '.npz', '.npy', '.pkl', '.pickle'}:
            raise ValueError('Reference/project/data artifacts do not belong in reusable packages')
        if p.suffix == '.py':
            ast.parse(p.read_text(), filename=str(rel))
        text = p.read_text()
        if any(s in text for s in ['private/truth.json', 'private/references', 'forward.npz', str(ROOT / 'cases'), str(WORK)]):
            raise ValueError('Package includes experiment-private paths/data: ' + str(rel))
    budget = guidance_budget(stage, read(ROOT / 'control/settings.json')['max_guidance_words'])
    dest = ROOT / 'policies' / pid
    stage.rename(dest)
    p0 = (ROOT / 'policies/P0/prompt.md').read_text()
    (dest / 'prompt.md').write_text(p0 + '\n\n' + (dest / 'guidance.md').read_text())
    if (dest / 'helpers').exists():
        with (dest / 'prompt.md').open('a') as f:
            f.write('\nReusable package files are in learned/.\n')
    save(dest / 'proposal.json', {'delivery': {'helpers/': 'learned/'}, 'author': 'persistent Sol/max research agent'})
    shutil.copy2(notes, ROOT / 'evidence' / ('package-' + pid + '-review.md'))
    record = {'id': pid, 'files': hashes(dest), 'prompt_sha256': sha(dest / 'prompt.md'),
              'guidance_budget': budget,
              'review': str(ROOT / 'evidence' / ('package-' + pid + '-review.md')),
              'information_check': 'Mechanical path/file screen; semantic leakage still requires research audit and fresh transfer.'}
    save(dest / 'frozen.json', record)
    return record
