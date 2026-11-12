"""Run a manifest of Claude Code P0 attempts with no elapsed solver deadline. Never relaunches an existing attempt.
Usage: dispatch.py [jobs/manifest.json]  (default jobs/opus5-r1.json)"""
import concurrent.futures
import fcntl
import json
import shutil
import time
from pathlib import Path
import runner

R=runner.ROOT
import sys
MANIFEST=Path(sys.argv[1]) if len(sys.argv)>1 else R/'jobs/opus5-r1.json'
JOBS=json.loads(MANIFEST.read_text())
SETTINGS=json.loads((R/'control/settings.json').read_text())
TERMINAL={'finished','failed','timed_out','launcher_error','infrastructure_error'}

def read(p,default=None):
    try:return json.loads(p.read_text())
    except (OSError,ValueError):return default

def state(job):
    a=R/'attempts'/job['id']
    return read(a/'run/launch.json') or read(a/'dispatch_error.json') or {'status':'queued'}

def snapshot(hold=None):
    rows=[{'id':j['id'],**{k:v for k,v in state(j).items() if k in ['status','started_at','ended_at','elapsed_seconds','infrastructure_failure','proxy_flag']}} for j in JOBS]
    out={'at':runner.now(),'jobs':rows,'dispatch_hold':hold}
    runner.save(R/'analysis'/('status-'+MANIFEST.stem+'.json'),out)
    return out

def execute(j):
    (R/'attempts'/j['id']).mkdir(parents=True,exist_ok=True)
    with (R/'attempts'/j['id']/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:return runner.run(j)
        except Exception as exc:
            result={'id':j['id'],'status':'infrastructure_error','error':repr(exc),'at':runner.now()}
            runner.save(R/'attempts'/j['id']/'dispatch_error.json',result)
            return result

def main():
    limit=SETTINGS['max_concurrent_solvers']
    with (R/'control/dispatcher.lock').open('a') as singleton:
        fcntl.flock(singleton,fcntl.LOCK_EX|fcntl.LOCK_NB)
        runner.save(R/'control/dispatcher.json',{'status':'running','at':runner.now()})
        pending=[j for j in JOBS if state(j)['status']=='queued']
        active={}
        with concurrent.futures.ThreadPoolExecutor(max_workers=limit) as pool:
            while active or (pending and not (R/'control/STOP_DISPATCH.json').exists()):
                for f in list(active):
                    if f.done():
                        job=active.pop(f)
                        try:runner.log(job['id']+' returned '+f.result()['status'])
                        except Exception as exc:
                            runner.save(R/'attempts'/job['id']/'dispatch_error.json',{'id':job['id'],'status':'infrastructure_error','error':repr(exc)})
                mem=next(int(l.split()[1])/2**20 for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:'))
                hold=None
                if (R/'control/STOP_DISPATCH.json').exists():hold='Service/usage limit; new dispatch paused, running attempts continue.'
                elif shutil.disk_usage(R).free/2**30<SETTINGS['minimum_free_disk_gib']:hold='Free disk low; new dispatch paused.'
                elif mem<SETTINGS['minimum_available_ram_gib']:hold='Available RAM low; new dispatch paused.'
                if not hold:
                    while pending and len(active)<limit:
                        job=pending.pop(0);active[pool.submit(execute,job)]=job
                snapshot(hold)
                time.sleep(10)
        result=snapshot()
        done=all(j['status'] in TERMINAL for j in result['jobs'])
        if done:runner.save(R/'analysis'/('batch_complete-'+MANIFEST.stem+'.json'),result)
        runner.save(R/'control/dispatcher.json',{'status':'complete' if done else 'paused','at':runner.now(),
                    'reason':None if done else 'Queued attempts remain (usage limit or hold). Restart dispatch after the limit resets; existing attempts are never relaunched.'})

if __name__=='__main__':main()
