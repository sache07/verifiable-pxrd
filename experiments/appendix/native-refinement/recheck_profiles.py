"""Re-evaluate failed independent residual diagnostics in fresh processes.

Never refine, modify a candidate, or open a reference structure. Preserve the
original result and its diagnostic error; write a separately identified record.
Small metadata-selected successful controls check agreement with the inline fit.
"""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from common import digest, read_json, verify_task, write_json


def one(task, directory, control=False):
    result = read_json(directory/'result.json')
    record = dict(id=task['id'], status='failed', input_sha256=task['candidate_sha256'],
        output_sha256=result['output_sha256'], original_diagnostic_error=result.get('paired_profile_error'),
        control=control, script_sha256=digest(Path(__file__).read_bytes()),
        diagnostic_code_sha256=digest((Path(__file__).parent/'gsas.py').read_bytes()))
    try:
        verify_task(task)
        for name, sha in [('input.cif', record['input_sha256']), ('refined.cif', record['output_sha256'])]:
            if digest((directory/name).read_bytes()) != sha:
                raise ValueError('Candidate changed before independent recheck')
        from gsas import diagnostic, observation
        with tempfile.TemporaryDirectory(prefix='pxrd-profile-recheck-') as temporary:
            root=Path(temporary)
            for name in ('input.cif','refined.cif'):
                shutil.copy2(directory/name,root/name)
            profile=diagnostic(task,root,*observation(task))
            if control:
                delta=max(abs(profile[side]['rwp_percent']-result['paired_profile'][side]['rwp_percent'])
                          for side in ('before','after'))
                record['max_control_delta_pp']=delta
                if delta>1e-6:
                    raise ValueError(f'Fresh diagnostic control differs by {delta} pp')
            shutil.copy2(root/'paired-profiles.npz',directory/'rechecked-profiles.npz')
            record.update(status='completed', paired_profile=profile)
    except Exception as error:
        record['error']=f'{type(error).__name__}: {error}'
    record['packages']={n: importlib.metadata.version(n) for n in ('numpy','scipy','pymatgen','spglib')}
    write_json(directory/'profile-recheck.json',record)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tasks',type=Path,required=True)
    parser.add_argument('--runs',type=Path,nargs='+',required=True)
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--controls-per-group',type=int,default=2)
    parser.add_argument('--one-task',type=Path,help=argparse.SUPPRESS)
    parser.add_argument('--one-directory',type=Path,help=argparse.SUPPRESS)
    parser.add_argument('--control',action='store_true',help=argparse.SUPPRESS)
    args=parser.parse_args()
    if args.one_task:
        one(read_json(args.one_task),args.one_directory,args.control)
        return
    tasks={t['id']:t for t in read_json(args.tasks)}
    jobs,controls,seen=[],defaultdict(int),set()
    for path in sorted(p for run in args.runs for p in (run/'candidates').rglob('result.json')):
        r=read_json(path)
        if r['id'] in seen:
            raise ValueError('Duplicate result: '+r['id'])
        seen.add(r['id'])
        if r['status']!='completed':continue
        group=tuple(r['id'].split('/')[:2])
        control=not r.get('paired_profile_error') and 'paired_profile' in r and controls[group]<args.controls_per_group
        if control:controls[group]+=1
        if not r.get('paired_profile_error') and not control:continue
        target=path.parent/'profile-recheck.json'
        if target.exists():
            old=read_json(target)
            if old['input_sha256']!=r['input_sha256'] or old['output_sha256']!=r['output_sha256']:
                raise ValueError('Recheck belongs to another candidate')
            continue
        jobs.append((tasks[r['id']],path.parent,control))
    def run(job):
        task,directory,control=job
        with tempfile.TemporaryDirectory(prefix='pxrd-recheck-request-') as temporary:
            path=Path(temporary)/'task.json'
            write_json(path,task)
            command=[sys.executable,str(Path(__file__).resolve()),'--tasks',str(args.tasks),
                '--runs',str(directory),'--one-task',str(path),'--one-directory',str(directory)]
            if control:command.append('--control')
            with (directory/'profile-recheck.log').open('w') as log:
                subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=120,check=True)
        return read_json(directory/'profile-recheck.json')['status']
    print(f'Rechecking {len(jobs)} profiles (fresh subprocess per candidate)',flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        statuses=list(pool.map(run,jobs))
    print({s:statuses.count(s) for s in set(statuses)},flush=True)


if __name__=='__main__':main()
