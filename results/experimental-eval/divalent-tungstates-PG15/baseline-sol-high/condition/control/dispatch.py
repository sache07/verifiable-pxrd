"""Run the matched P0 panel after v6, with no elapsed solver deadline."""
import concurrent.futures
import fcntl
import json
import shutil
import time
from pathlib import Path
import runner

R=runner.ROOT
JOBS=json.loads((R/'jobs/experimental45.json').read_text())
SETTINGS=json.loads((R/'control/settings.json').read_text())
TERMINAL={'finished','failed','timed_out','launcher_error','infrastructure_error'}

def read(p,default=None):
    try:return json.loads(p.read_text())
    except (OSError,ValueError):return default

def state(root,job):
    a=root/'attempts'/job['id']
    return read(a/'run/launch.json') or read(a/'dispatch_error.json') or {'status':'queued'}

def snapshot(hold=None):
    rows=[{**j,**state(R,j)} for j in JOBS]
    out={'at':runner.now(),'jobs':rows,'dispatch_hold':hold}
    runner.save(R/'analysis/status.json',out)
    return out

def execute(j):
    with (R/'attempts'/j['id']/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:return runner.run(j)
        except Exception as exc:
            result={'id':j['id'],'status':'infrastructure_error','error':repr(exc),'at':runner.now()}
            runner.save(R/'attempts'/j['id']/'dispatch_error.json',result)
            return result

def main():
    with (R/'control/dispatcher.lock').open('a') as singleton:
        fcntl.flock(singleton,fcntl.LOCK_EX|fcntl.LOCK_NB)
        previous=Path(SETTINGS['wait_for_panel'])
        earlier=read(previous/'jobs/experimental45.json')
        assert len(earlier)==45
        while any(state(previous,j)['status']=='queued' for j in earlier):
            snapshot('Waiting for all v6 jobs to launch, then filling its released slots (16 workers total).')
            time.sleep(30)
        runner.save(R/'control/dispatcher.json',{'status':'running','at':runner.now()})
        pending=[j for j in JOBS if state(R,j)['status']=='queued']
        active={}
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
            while pending or active:
                for f in list(active):
                    if f.done():
                        job=active.pop(f)
                        try:runner.log(job['id']+' returned '+f.result()['status'])
                        except Exception as exc:
                            runner.save(R/'attempts'/job['id']/'dispatch_error.json',
                                        {'id':job['id'],'status':'infrastructure_error','error':repr(exc)})
                mem=next(int(l.split()[1])/2**20 for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:'))
                hold=None
                if (R/'control/STOP_DISPATCH.json').exists():hold='Service limit; new dispatch paused.'
                elif shutil.disk_usage(R).free/2**30<6:hold='Free disk below 6 GiB; new dispatch paused.'
                elif mem<8:hold='Available RAM below 8 GiB; new dispatch paused.'
                remaining_v6=sum(state(previous,j)['status']=='running' for j in earlier)
                limit=max(0,16-remaining_v6)
                if not hold:
                    while pending and len(active)<limit:
                        job=pending.pop(0);active[pool.submit(execute,job)]=job
                snapshot(hold)
                if pending or active:time.sleep(10)
        result=snapshot()
        if all(j['status'] in TERMINAL for j in result['jobs']):
            runner.save(R/'analysis/batch_complete.json',result)
            runner.save(R/'control/dispatcher.json',{'status':'complete','at':runner.now()})
        else:
            runner.save(R/'control/dispatcher.json',{'status':'needs_review','at':runner.now(),
                        'reason':'Existing nonterminal records preserved; attempts were not relaunched.'})

if __name__=='__main__':main()
