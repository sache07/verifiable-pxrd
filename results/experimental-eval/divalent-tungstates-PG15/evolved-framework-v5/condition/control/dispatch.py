"""Durable 45-slot evaluation queue (evolved framework access v5 on the 15 measured scans); capacity recovery never adds replicates."""
import argparse
from collections import Counter
import fcntl
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import runner

R=runner.ROOT
SETTINGS=json.loads((R/'control/settings.json').read_text())
JOBS=json.loads((R/'jobs/experimental45.json').read_text())
TERMINAL={'finished','failed','timed_out','launcher_error','infrastructure_error','needs_review','cancelled'}
REPLICATE={j['id']:j['replicate'] for j in JOBS}
def released():
    """Replicates the operator has released (control/release.json); all three when the file is absent."""
    r=read(R/'control/release.json')
    return sorted(r['replicates']) if r else [1,2,3]

def read(p,default=None):
    try:return json.loads(p.read_text())
    except (OSError,ValueError):return default

def unit(jid):return SETTINGS['service_prefix']+'-'+jid+'.service'

def unit_active(name):
    prop='ActiveState' if name.endswith('.scope') else 'MainPID'
    p=subprocess.run(['systemctl','--user','show',name,'--property='+prop,'--value'],capture_output=True,text=True)
    return p.stdout.strip() in ['active','activating','deactivating'] if prop=='ActiveState' else p.stdout.strip() not in ['','0']

def execute(jid):
    j=read(R/'jobs/transports'/(jid+'.json'))
    a=R/'attempts'/jid;a.mkdir(parents=True,exist_ok=True)
    with (a/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:runner.run(j)
        except Exception as exc:
            runner.save(a/'dispatch_error.json',{'id':jid,'status':'infrastructure_error','error':repr(exc),'at':runner.now()})

def recover(parent,original,number):
    """Use the established saved-session recovery path, after proving it stopped."""
    a=R/'attempts'/parent;rec=read(a/'run/launch.json',{})
    if unit_active(unit(parent)) or (rec.get('systemd_unit') and unit_active(rec['systemd_unit'])):
        raise RuntimeError('Parent still active; refusing duplicate')
    if not rec.get('inputs_unchanged') or rec.get('infrastructure_failure'):
        raise RuntimeError('Parent failed integrity or service-usage checks')
    events=[]
    for line in (a/'run/codex-events.jsonl').read_text().splitlines():
        try:events.append(json.loads(line))
        except ValueError:pass
    scientific=any(e.get('type','').startswith('item.') for e in events)
    j=dict(original,id=original['id']+'-retry'+str(number),recovery_of=parent)
    if scientific:
        sessions=list((a/'codex-home/sessions').rglob('*'+str(rec.get('session_id'))+'*.jsonl'))
        if len(sessions)!=1:raise RuntimeError('Cannot recover scientific work without its unique saved session')
        j.update(continuation_of=parent,infrastructure_recovery=True,
            continuation_instruction='Resume the interrupted task under the same condition. Preserve your previous work and finish the original scientific task.')
    j['recovery_mode']='saved_session' if scientific else 'no_model_work_transport_retry'
    return j

def launch(jid):
    p=subprocess.run(['systemctl','--user','show',unit(jid),'--property=LoadState','--value'],capture_output=True,text=True)
    if p.stdout.strip() not in ['','not-found']:return
    subprocess.run(['systemd-run','--user','--quiet','--unit='+unit(jid),
        '--property=Type=exec','--property=RemainAfterExit=yes','--property=WorkingDirectory='+str(R),
        '--',str(runner.CORE/'bin/python'),str(Path(__file__)),'--worker',jid],check=True)


def refresh(s):
    for original,row in s['slots'].items():
        if row['status']=='cancelled':continue  # operator-cancelled slot: never refreshed, relaunched or retried
        jid=row['current'];a=R/'attempts'/jid
        rec=read(a/'run/launch.json') or read(a/'dispatch_error.json')
        # The supervisor can remain active/exited after completion; only a live
        # MainPID counts as work. A scientific scope is checked at recovery too.
        p=subprocess.run(['systemctl','--user','show',unit(jid),'--property=MainPID','--value'],capture_output=True,text=True)
        live=p.stdout.strip() not in ['','0']
        if live:
            row['status']='running' if rec else 'starting';continue
        if rec:
            if rec['status']=='running':
                row.update(status='needs_review',error='Supervisor ended without final record; no duplicate launched.');continue
            if (rec['status']=='failed' and rec.get('capacity_limited') and rec.get('inputs_unchanged')
                    and not rec.get('infrastructure_failure') and not row.get('recovery_blocked')):
                if row['status']!='retry_wait':
                    row.update(status='retry_wait',retry_at=time.time()+SETTINGS['capacity_retry_seconds'])
            else:row['status']='needs_review' if row.get('recovery_blocked') else rec['status']
        elif row['status']=='dispatching':
            # The persisted claim and deterministic service name survive a
            # controller restart. No second worker is admitted for this ID.
            launch(jid)


def choose(s,now):
    waiting=[(k,v) for k,v in s['slots'].items() if v['status']=='retry_wait']
    if waiting:
        key,row=max(waiting,key=lambda kv:kv[1]['retry_at'])
        if now<max(row['retry_at'],s.get('retry_after',0)):return None
        return key
    allowed=released()
    return next((k for k,v in s['slots'].items() if v['status']=='queued' and (k not in REPLICATE or REPLICATE[k] in allowed)),None)


def snapshot(s,hold=None):
    rows=[]
    for j in JOBS:
        slot=s['slots'][j['id']];rec=read(R/'attempts'/slot['current']/'run/launch.json',{})
        rows.append({**j,**rec,'id':j['id'],'transport_id':slot['current'],'status':slot['status'],
                     'transport_history':slot['history'],'retry_at':slot.get('retry_at')})
    out={'at':runner.now(),'jobs':rows,'dispatch_hold':hold,'released_replicates':released(),
         'counts':dict(Counter(j['status'] for j in rows)),'maximum_concurrency':SETTINGS['max_concurrent_solvers']}
    runner.save(R/'analysis/status.json',out)
    lines=['# Evolved framework access (v5) evaluation','',out['at'],'',str(out['counts']),'',
        'Dispatch hold: '+str(hold or 'none'),'','Released replicates: '+', '.join(f'r{n}' for n in released()),'',
        '| Case | r1 | r2 | r3 |','|---|---|---|---|']
    for c in range(1,16):
        cells=[]
        for pol in ['fwaccess-v5']:
            for rep in range(1,4):
                row=s['slots'][f'{pol}-exp-case-{c:03d}-r{rep}']
                cells.append(row['status']+(f" ({len(row['history'])-1} retries)" if len(row['history'])>1 else ''))
        lines.append('| '+str(c)+' | '+' | '.join(cells)+' |')
    (R/'report/STATUS.md').write_text('\n'.join(lines)+'\n')
    return out


def main():
    with (R/'control/dispatcher.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        path=R/'control/queue.json'
        s=read(path) or {'slots':{j['id']:{'current':j['id'],'status':'queued','history':[j['id']]} for j in JOBS}}
        originals={j['id']:j for j in JOBS};last_monitor=0
        while True:
            refresh(s)
            busy=sum(v['status'] in ['running','starting','dispatching'] for v in s['slots'].values())
            mem=next(int(l.split()[1])/2**20 for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:'))
            hold=None
            if (R/'control/STOP_DISPATCH.json').exists():hold='Paused by operator or service usage limit'
            elif shutil.disk_usage(R).free/2**30<SETTINGS['minimum_free_disk_gib']:hold='Disk below reserve'
            elif mem<SETTINGS['minimum_available_ram_gib']:hold='RAM below reserve'
            while not hold and busy<SETTINGS['max_concurrent_solvers']:
                key=choose(s,time.time())
                if key is None:break
                row=s['slots'][key];retry=row['status']=='retry_wait'
                if retry:
                    try:
                        job=recover(row['current'],originals[key],len(row['history']))
                        runner.save(R/'jobs/transports'/(job['id']+'.json'),job)
                    except Exception as exc:
                        row.update(status='needs_review',recovery_blocked=str(exc));break
                    row.update(current=job['id']);row['history'].append(job['id']);row.pop('retry_at',None)
                    s['retry_after']=time.time()+SETTINGS['capacity_retry_seconds']
                row['status']='dispatching';runner.save(path,s)
                launch(row['current']);busy+=1
                if retry:break  # one retry admission per interval
            runner.save(path,s)
            out=snapshot(s,hold)
            if time.time()-last_monitor>=SETTINGS['monitor_seconds']:
                with (R/'report/health.jsonl').open('a') as f:
                    f.write(json.dumps({'at':out['at'],'counts':out['counts'],'hold':hold,
                        'available_ram_gib':round(mem,2),'free_disk_gib':round(shutil.disk_usage(R).free/2**30,2)})+'\n')
                print(out['at'],out['counts'],'hold:',hold,flush=True);last_monitor=time.time()
            if all(v['status'] in TERMINAL for v in s['slots'].values()):
                runner.save(R/'analysis/batch_complete.json',out);return
            time.sleep(10)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--worker');args=p.parse_args()
    if args.worker:execute(args.worker)
    else:main()
