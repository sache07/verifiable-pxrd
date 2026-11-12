"""Small isolated job runner; scientific conditions reused from the frozen harness."""
from pathlib import Path
from dataclasses import replace
import argparse, concurrent.futures, datetime, fcntl, hashlib, json, os, shutil, subprocess, sys, threading, time

ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'control/harness'
CORE=Path('<HOME>/.local/share/pxrd-baseline/core')
BACK=Path('<HOME>/.local/share/characterizagent/backends')
STANDALONE=Path('<HOME>/.codex/packages/standalone/releases/0.154.0-x86_64-unknown-linux-musl')
INDEX=BACK/'dara/venv/lib/python3.11/site-packages/dara/data/cod_filtered_info_2024.json.gz'
CIFS=BACK/'dara/cod-filtered-2024/cif'
AUTH=ROOT/'control/auth'
os.environ.update(VPBENCH_AUTH_HOME=str(AUTH),VPBENCH_CODEX=str(STANDALONE/'bin/codex'),VPBENCH_MATSCI_ENV=str(CORE),VPBENCH_GSAS_ENV=str(BACK/'gsas2/venv'),VPBENCH_DICVOL_ROOT=str(BACK/'dicvol'),VPBENCH_COD_METADATA=str(INDEX),VPBENCH_COD_CIFS=str(CIFS),VPBENCH_UV_PYTHON='<HOME>/.local/share/uv/python',VPBENCH_CODEX_STANDALONE=str(STANDALONE))
sys.path.insert(0,str(H/'src'))
from verifiable_pxrd.condition import load_condition
from verifiable_pxrd.run import _config_text, _clean_environment, _remove_auth_links
LOCK=threading.Lock()
FINAL_PROJECT_REQUIREMENT='Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 q=p.with_suffix(p.suffix+'.new');q.write_text(json.dumps(x,indent=2)+'\n');q.replace(p)
def log(s):
 with LOCK:
  s='['+now()+'] '+s;print(s,flush=True)
  with (ROOT/'monitor.log').open('a') as f:f.write(s+'\n')
def paths(j):
 if j.get('persistent_id'):
  b=ROOT/'reflectors'/j['persistent_id'];a=b/'turns'/j['id']
  return a,b/'workspace',b/'codex-home',a/'run'
 a=ROOT/('reflectors' if j['role']=='reflector' else 'attempts')/j['id']
 return a,a/'workspace',a/'codex-home',a/'run'
def resources(j):
 r=j.get('resource','full')
 return (INDEX,CIFS) if r=='full' else (ROOT/'resources'/r/'index.json.gz',ROOT/'resources'/r/'cif')
def clone_continuation(j,w,h):
 """Independent files and raw session history; never resume in the parent home."""
 parent=ROOT/'attempts'/j['continuation_of'];launch=json.loads((parent/'run/launch.json').read_text())
 if not j.get('infrastructure_recovery') and launch['status'] not in ['finished','timed_out']:raise ValueError('Parent is not a completed scientific attempt')
 if j.get('infrastructure_recovery'):
  frozen=json.loads((parent/'run/frozen.json').read_text())
  if not all((parent/'workspace'/f).is_file() and sha(parent/'workspace'/f)==v for f,v in frozen['inputs'].items()):raise ValueError('Recovery input integrity failure')
  if not launch.get('session_id'):
   for line in (parent/'run/codex-events.jsonl').read_text().splitlines():
    try:event=json.loads(line)
    except ValueError:continue
    if event.get('type')=='thread.started':launch['session_id']=event['thread_id'];break
 elif launch.get('infrastructure_failure') or not launch.get('inputs_unchanged'):raise ValueError('Parent failed integrity checks')
 sid=launch['session_id'];matches=list((parent/'codex-home/sessions').rglob('*'+sid+'*.jsonl'))
 if len(matches)!=1:raise ValueError('Need exactly one archived session for '+sid)
 source=parent/'workspace'
 # Only copy scientific working files. In particular, .tmp is retained.
 for p in source.rglob('*'):
  rel=p.relative_to(source)
  if any(x in ['__pycache__','.git','.codex','.agents'] for x in rel.parts):continue
  if p.is_symlink():raise ValueError('Continuation needs symlink review: '+str(p))
  if p.is_file():
   dest=w/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 session=matches[0];dest=h/session.relative_to(parent/'codex-home')
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(session,dest)
 j['resume_session_id']=sid
 j['extra_forbidden']=list(dict.fromkeys(j.get('extra_forbidden',[])+[str(source/'result.json')]))
 files={str(p.relative_to(w)):sha(p) for p in w.rglob('*') if p.is_file()}
 save(w.parent/'branch_provenance.json',dict(parent=j['continuation_of'],parent_workspace=str(source),
  session_id=sid,source_session=str(session),session_sha256=sha(session),copied_workspace_hashes=files,
  note='Raw history retained; workspace location changes. Original absolute paths may require rebasing.'))
def config(j,w):
 base=load_condition(H/'experiments/agent-adaptation/conditions/pxrd-codex.toml')
 index,cifs=resources(j)
 cond=replace(base,auth_method='chatgpt',auth_home=AUTH,model=j.get('model','gpt-5.6-sol'),reasoning_effort=j.get('effort','high'),read_paths=tuple(p for p in base.read_paths if p not in (INDEX,CIFS))+(index,cifs))
 text=_config_text(cond,w).replace('\":slash_tmp\" = \"write\"','\":slash_tmp\" = \"deny\"')
 marker=json.dumps(str(w))+' = "write"'
 text=text.replace(marker,marker+'\n'+json.dumps(str(w/'inputs'))+' = "read"')
 if (w/'learned').is_dir():text=text.replace(marker,marker+'\n'+json.dumps(str(w/'learned'))+' = "read"')
 for p in ['submission_check','OUTPUT_SCHEMA.md','AGENTS.md','CONTEXT.md','TOOLS.md']:
  if (w/p).exists():text=text.replace(marker,marker+'\n'+json.dumps(str(w/p))+' = "read"')
 if j['role']=='reflector':
  for p in ['scorer_v5','REFLECTOR.md','P0.md']:
   if (w/p).exists():text=text.replace(marker,marker+'\n'+json.dumps(str(w/p))+' = "read"')
 return text
def solver_prompt(j):
 text=(ROOT/'policies'/j['policy']/'prompt.md').read_text()
 if j.get('continuation_of'):
  condition_text=('\n\nCurrent condition instructions:\n'+text) if j['policy']!='P0' else ''
  text=('This is an independent continuation of your archived analysis. Your conversation and scientific files are retained in the current working directory. Earlier absolute workspace paths refer to the archive and are inaccessible; use the corresponding files here. Keep the original task and output requirements.'+condition_text+'\n\n'+j['continuation_instruction'])
 # Common output requirement also reaches older frozen packages and P0
 # continuations. Their archived prompts and completed attempts stay intact.
 if FINAL_PROJECT_REQUIREMENT not in text:
  text=text.rstrip()+'\n\n'+FINAL_PROJECT_REQUIREMENT+'\n'
 return text

def prepare(j):
 a,w,h,r=paths(j)
 if (r/'launch.json').exists():raise RuntimeError('Refusing duplicate '+j['id'])
 for p in [w/'.tmp',w/'.cache/matplotlib',h,r]:p.mkdir(parents=True,exist_ok=True)
 if j['role']=='solver':
  if j.get('continuation_of'):clone_continuation(j,w,h)
  # A new condition replaces its delivery, while the prior scientific workspace
  # and conversation remain archived in the parent attempt.
  if j.get('continuation_of'):
   shutil.rmtree(w/'learned',ignore_errors=True)
   for name in ['TOOLS.md','AGENTS.md','OUTPUT_SCHEMA.md']:(w/name).unlink(missing_ok=True)
  shutil.copytree(Path(j['case_path'])/'inputs',w/'inputs',dirs_exist_ok=True)
  if j.get('seed_workspace') and not (w/'prior').exists():
   shutil.copytree(j['seed_workspace'],w/'prior',ignore=shutil.ignore_patterns('.cache','.tmp','__pycache__','.git','.codex','.agents','inputs'))
  text=solver_prompt(j)
  helpers=ROOT/'policies'/j['policy']/'helpers'
  if helpers.is_dir():
   proposal=ROOT/'policies'/j['policy']/'proposal.json'
   delivery=json.loads(proposal.read_text()).get('delivery',{}).get('helpers/','learned/') if proposal.exists() else 'learned/'
   if delivery not in ['learned/','learned/helpers/']:raise ValueError('Unsupported helper deployment path '+delivery)
   shutil.copytree(helpers,w/delivery,ignore=shutil.ignore_patterns('__pycache__'),dirs_exist_ok=True)
  for name in ['TOOLS.md','AGENTS.md','OUTPUT_SCHEMA.md']:
   p=ROOT/'policies'/j['policy']/name
   if p.is_file():shutil.copy2(p,w/name)
 else:text=(a/'prompt.md').read_text()
 (a/'prompt.txt').write_text(text)
 index,cifs=resources(j)
 (h/'config.toml').write_text(config(j,w));(w/'sibling-canary.txt').write_text('private to this attempt\n')
 save(a/'job.json',j)
 immutable=[w/'inputs',w/'learned',w/'submission_check']
 if j['role']=='reflector':immutable.append(w/'scorer_v5')
 hashes={str(p.relative_to(w)):sha(p) for folder in immutable for p in folder.rglob('*') if p.is_file()}
 hashes.update({name:sha(w/name) for name in ['OUTPUT_SCHEMA.md','AGENTS.md','CONTEXT.md','TOOLS.md','REFLECTOR.md','P0.md'] if (w/name).exists()})
 save(r/'frozen.json',{'prompt':sha(a/'prompt.txt'),'config':sha(h/'config.toml'),'inputs':hashes})
def scope(j,inner,suffix):
 unit=json.loads((ROOT/'control/settings.json').read_text())['service_prefix']+'-'+j['id']+'-'+suffix+'-'+str(time.time_ns())+'.scope'
 return ['systemd-run','--user','--scope','--quiet','--unit='+unit,'--property=CPUQuota=200%','--property=MemoryMax=5G','--property=MemorySwapMax=0','--property=TasksMax=128','--',*inner],unit
def preflight(j):
 a,w,h,r=paths(j);index,cifs=resources(j)
 forbidden=[ROOT/'PLAN.md',ROOT/'control/private-canary.txt',AUTH/'auth.json',Path('<HOME>/.codex/auth.json'),h/'config.toml']
 if j['role']=='solver':forbidden.append(Path(j['case_path'])/'private/truth.json')
 forbidden.extend([ROOT/'cases/validation-001/private/truth.json',ROOT.parent/'pxrd-rollout-evidence-sol-20260925/policies/repeat1/guidance.md'])
 forbidden.extend(Path(p) for p in j.get('extra_forbidden',[]))
 forbidden=[str(p) for p in forbidden if p.exists()]
 settings={'blocked':forbidden,'index':str(index),'index_sha256':sha(index),'cifs':str(cifs),'excluded':j.get('excluded_ids',[]),'role':j['role'],'baseline':j.get('policy')=='P0'}
 src=(ROOT/'control/probe.py').read_text().replace('__SETTINGS__',repr(settings))
 cmd,_=scope(j,[str(STANDALONE/'bin/codex'),'sandbox','-C',str(w),'-P','vpbench','--',str(CORE/'bin/python'),'-c',src],'probe')
 env=_clean_environment(h);env['TMPDIR']=str(w/'.tmp')
 p=subprocess.run(cmd,cwd=w,env=env,capture_output=True,text=True,timeout=90)
 (r/'preflight.stdout').write_text(p.stdout);(r/'preflight.stderr').write_text(p.stderr)
 try:d=json.loads(p.stdout)
 except Exception:d={'passed':False,'error':(p.stdout+p.stderr)[-2500:]}
 d.update(returncode=p.returncode,checked_at=now());save(r/'preflight.json',d)
 if p.returncode or not d['passed']:raise RuntimeError(j['id']+' preflight '+json.dumps(d))
 return d
def run(j):
 a,w,h,r=paths(j)
 if (r/'launch.json').exists():return json.loads((r/'launch.json').read_text())
 if j.get('approval_required') and not (ROOT/'control/REFLECTION_APPROVED.json').is_file():raise RuntimeError('Experiment awaits user approval; no model launched')
 if not (r/'frozen.json').exists():prepare(j)
 else:j=json.loads((a/'job.json').read_text())
 preflight(j);assert (AUTH/'auth.json').is_file()
 for name in ['auth.json','models_cache.json']:
  p=h/name
  if p.is_symlink():p.unlink()
  if (AUTH/name).exists():p.symlink_to(AUTH/name)
 inner=[str(STANDALONE/'bin/codex'),'exec','-C',str(w),'--skip-git-repo-check','--strict-config','--color','never','-m',j.get('model','gpt-5.6-sol'),'-c','model_reasoning_effort="'+j.get('effort','high')+'"','--json','-o',str(r/'final-answer.md'),'-']
 if j.get('resume_session_id'):
  inner=[str(STANDALONE/'bin/codex'),'exec','-C',str(w),'--color','never','resume','--skip-git-repo-check','--strict-config','-m',j.get('model','gpt-5.6-sol'),'-c','model_reasoning_effort="'+j.get('effort','high')+'"','--json','-o',str(r/'final-answer.md'),j['resume_session_id'],'-']
 cmd,unit=scope(j,inner,'run');env=_clean_environment(h);env['TMPDIR']=str(w/'.tmp')
 rec={**j,'status':'running','started_at':now(),'systemd_unit':unit,'prompt_sha256':sha(a/'prompt.txt'),'host':os.uname().nodename}
 save(r/'launch.json',rec);log(j['id']+' START')
 def consume(pipe,path,events):
  with path.open('w',buffering=1) as f:
   for line in pipe:
    f.write(line)
    if not events:continue
    try:e=json.loads(line)
    except ValueError:continue
    item=e.get('item',{})
    if e.get('type')=='thread.started':
     rec['session_id']=e['thread_id']
     if j.get('resume_session_id') and rec['session_id']!=j['resume_session_id']:
      rec['infrastructure_failure']='resumed_wrong_session'
    if e.get('type')=='turn.completed':rec['usage']=e.get('usage',{})
    if e.get('type')=='item.completed' and item.get('type')=='agent_message':
     with (r/'messages.log').open('a') as m:m.write(item.get('text','')+'\n\n')
     log(j['id']+' '+item.get('text','')[:1800])
    if e.get('type') in ['turn.completed','turn.failed','error']:
     log(j['id']+' '+json.dumps(e))
     if e.get('type')!='turn.completed' and any(s in json.dumps(e).lower() for s in ['429','too many requests','at capacity','server_overloaded','server_is_overloaded']):
      rec['capacity_limited']=True
     if e.get('type')!='turn.completed' and any(s in json.dumps(e).lower() for s in ['usage limit','usage_limit','quota exceeded','insufficient_quota']):
      save(ROOT/'control/STOP_DISPATCH.json',{'at':now(),'job':j['id'],'reason':'Service usage limit; preserve unfinished jobs and stop new launches.'})
      rec['infrastructure_failure']='service_usage_limit'
 try:
  p=subprocess.Popen(cmd,cwd=w,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
  threads=[threading.Thread(target=consume,args=(p.stdout,r/'codex-events.jsonl',True)),threading.Thread(target=consume,args=(p.stderr,r/'codex-stderr.log',False))]
  for t in threads:t.start()
  p.stdin.write((a/'prompt.txt').read_text());p.stdin.close();timeout=False
  try:p.wait(timeout=j.get('timeout_seconds'))
  except subprocess.TimeoutExpired:
   timeout=True;subprocess.run(['systemctl','--user','stop',unit],capture_output=True);p.wait(timeout=30)
  for t in threads:t.join(timeout=30)
  rec.update(status='timed_out' if timeout else 'finished' if p.returncode==0 else 'failed',returncode=p.returncode,timed_out=timeout)
 except BaseException as exc:
  subprocess.run(['systemctl','--user','stop',unit],capture_output=True);rec.update(status='launcher_error',error=repr(exc))
 finally:
  # A completed CLI can leave an abandoned scientific subprocess in its scope.
  # End all work at the recorded attempt boundary before freezing its outcome.
  subprocess.run(['systemctl','--user','stop',unit],capture_output=True)
  _remove_auth_links(h);rec['ended_at']=now()
  rec['elapsed_seconds']=(datetime.datetime.fromisoformat(rec['ended_at'])-datetime.datetime.fromisoformat(rec['started_at'])).total_seconds()
  frozen=json.loads((r/'frozen.json').read_text())
  rec['inputs_unchanged']=all((w/f).is_file() and sha(w/f)==v for f,v in frozen['inputs'].items())
  rec['outputs_present']={f:(w/f).exists() for f in (['adaptation','report.md','requests'] if j['role']=='reflector' else ['result.json','fit.csv','report.md','final.gpx'])}
  if not rec['inputs_unchanged']:rec['infrastructure_failure']='immutable_inputs_modified'
  save(r/'launch.json',rec)
 log(j['id']+' '+rec['status'].upper());return rec
def bounded_run(j,limit):
 slots=ROOT/'control/reservations';slots.mkdir(exist_ok=True)
 reservation=slots/(j['id']+'.json')
 while True:
  if (ROOT/'control/STOP_DISPATCH.json').exists():
   log(j['id']+' NOT LAUNCHED: service usage limit');return {'id':j['id'],'status':'not_launched'}
  with (ROOT/'control/scheduler.lock').open('a') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX)
   busy=set()
   for kind in ['attempts','reflectors']:
    for f in (ROOT/kind).rglob('run/launch.json'):
     try:
      d=json.loads(f.read_text())
      if d['status']=='running' and d.get('host',os.uname().nodename)==os.uname().nodename:busy.add(d['id'])
     except (ValueError,FileNotFoundError):pass
   for f in slots.glob('*.json'):
    d=json.loads(f.read_text())
    try:os.kill(d['pid'],0);busy.add(d['id'])
    except ProcessLookupError:f.unlink()
   if len(busy)<limit:
    save(reservation,{'id':j['id'],'pid':os.getpid(),'at':now()});break
  time.sleep(3)
 try:return run(j)
 finally:reservation.unlink(missing_ok=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('--workers',type=int,default=4);p.add_argument('--cluster-limit',type=int,default=12);p.add_argument('--prepare-only',action='store_true');p.add_argument('--probe-only',action='store_true');args=p.parse_args()
 jobs=json.loads(Path(args.manifest).read_text())
 if args.prepare_only:
  for j in jobs:prepare(j)
  return
 if args.probe_only:
  for j in jobs:print(json.dumps(preflight(j)),flush=True)
  return
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
  fs={ex.submit(bounded_run,j,args.cluster_limit):j for j in jobs}
  for f in concurrent.futures.as_completed(fs):
   try:f.result()
   except Exception as exc:log(fs[f]['id']+' LAUNCH ERROR '+repr(exc))
if __name__=='__main__':main()
