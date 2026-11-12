"""Claude Code P0 runner. Same scientific condition as matched P0; only the solver model and harness differ.

Isolation: systemd scope (2 CPU, 5 GiB, 128 tasks) -> bubblewrap with the Codex P0 filesystem
view (minimal system, scientific tools and COD read-only, private workspace writable, inputs
read-only, no /tmp at all, as Codex P0 denied it) and no network namespace access. The CLI reaches the API
only through bridge.py -> Unix socket -> auth_proxy.py on the host, which holds the key.
"""
from pathlib import Path
import argparse, concurrent.futures, datetime, fcntl, hashlib, json, os, secrets, shutil, subprocess, sys, threading, time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'control'))
import auth_proxy
CORE=Path('<HOME>/.local/share/pxrd-baseline/core')
BACK=Path('<HOME>/.local/share/characterizagent/backends')
UV=Path('<HOME>/.local/share/uv/python')
INDEX=BACK/'dara/venv/lib/python3.11/site-packages/dara/data/cod_filtered_info_2024.json.gz'
CIFS=BACK/'dara/cod-filtered-2024/cif'
CLAUDE_DIR=Path('<HOME>/.local/share/pxrd-claude/2.1.299')
CLAUDE=CLAUDE_DIR/'claude'
CLAUDE_SHA256='2d894a4b1bfaaa9aab72aeff7803e3c73bc2510f279a171f6b8f59f72d17d077'
INDEX_SHA256='03599f54f03f04420523dca36cc06927b74ce0070a4a80e6d859faa38a6c5aed'
# Same read-only paths as the matched P0 Codex profile (Codex binary replaced by the Claude binary).
READ_PATHS=[CORE,BACK/'gsas2/venv',BACK/'dicvol',INDEX,CIFS,UV,CLAUDE_DIR]
DENY_PATHS=[CORE/'lib/python3.11/site-packages'/p for p in ['ase/test','pyocse/data','pyxtal/database/cifs','pyxtal/database/bug.json','pyxtal/database/mech.db','pyxtal/database/test.db']]
TOOLS='Bash,Read,Write,Edit,Glob,Grep'
PORT=8787
LOCK=threading.Lock()
FINAL_PROJECT_REQUIREMENT='Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.'
STOP_MARKERS=['session limit','hit your limit','hit your session','rate_limit','rate limit','overloaded','credit balance','usage limit','limit reached','extra usage','quota','invalid x-api-key','authentication_error','permission_error','oauth','token has expired','revoked']
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
 a=ROOT/'attempts'/j['id']
 return a,a/'workspace',a/'claude-home',a/'run'
def solver_prompt(j):
 if j.get('prompt_file'):return Path(j['prompt_file']).read_text()
 text=(ROOT/'policies'/j['policy']/'prompt.md').read_text()
 if FINAL_PROJECT_REQUIREMENT not in text:text=text.rstrip()+'\n\n'+FINAL_PROJECT_REQUIREMENT+'\n'
 return text
def variables(j,w,h,token):
 """Codex shell_environment_policy values for P0, plus what the CLI itself needs."""
 return {'PATH':os.pathsep.join([str(BACK/'dicvol/bin'),str(CORE/'bin'),'/usr/local/bin','/usr/bin','/bin']),
  'HOME':str(w),'TMPDIR':str(w/'.tmp'),'XDG_CACHE_HOME':str(w/'.cache'),'MPLCONFIGDIR':str(w/'.cache/matplotlib'),
  'PYTHONNOUSERSITE':'1','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','SHELL':'/bin/bash','TERM':'dumb',
  'OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2','MKL_NUM_THREADS':'2','NUMEXPR_NUM_THREADS':'2',
  'GSAS2_PYTHON':str(BACK/'gsas2/venv/bin/python'),
  'CLAUDE_CONFIG_DIR':str(h),'ANTHROPIC_BASE_URL':'http://127.0.0.1:%d'%PORT,'CLAUDE_CODE_OAUTH_TOKEN':token,
  'DISABLE_AUTOUPDATER':'1','CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC':'1','DISABLE_TELEMETRY':'1',
  'DISABLE_ERROR_REPORTING':'1','CLAUDE_CODE_SUBPROCESS_ENV_SCRUB':'0','CLAUDE_CODE_DISABLE_BUNDLED_SKILLS':'1',
  'CLAUDE_CODE_DISABLE_AUTO_MEMORY':'1','CLAUDE_CODE_DISABLE_CLAUDE_MDS':'1','CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY':'1',
  'CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS':'1'}
def bwrap(j,inner,token='none',network_bridge=True):
 a,w,h,r=paths(j)
 cmd=['bwrap','--die-with-parent','--new-session','--unshare-all','--clearenv',
  '--proc','/proc','--dev','/dev','--ro-bind','/usr','/usr','--ro-bind','/etc','/etc',
  '--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64']
 for p in READ_PATHS:
  if p.exists():cmd+=['--ro-bind',str(p),str(p)]
 for p in DENY_PATHS:
  if p.is_dir():cmd+=['--tmpfs',str(p),'--remount-ro',str(p)]
  elif p.exists():cmd+=['--ro-bind','/dev/null',str(p)]
 cmd+=['--bind',str(w),str(w),'--ro-bind',str(w/'inputs'),str(w/'inputs'),'--bind',str(h),str(h),
  '--ro-bind',str(h/'settings.json'),str(h/'settings.json')]
 if network_bridge:cmd+=['--ro-bind',str(ROOT/'control/bridge.py'),str(ROOT/'control/bridge.py'),'--bind',str(a/'sock'),str(a/'sock')]
 for k,v in variables(j,w,h,token).items():cmd+=['--setenv',k,v]
 # Sandbox root (mount-point parents) read-only: writes outside the workspace and CLI home fail; there is no /tmp.
 return cmd+['--remount-ro','/','--chdir',str(w),'--',*inner]
def claude_argv(j):
 a,w,h,r=paths(j)
 return [str(CLAUDE),'-p','--model',j['model'],'--effort',j['effort'],'--tools',TOOLS,
  '--permission-mode','bypassPermissions','--strict-mcp-config','--settings',str(h/'settings.json'),
  '--output-format','stream-json','--verbose']
def prepare(j):
 a,w,h,r=paths(j)
 if (r/'launch.json').exists():raise RuntimeError('Refusing duplicate '+j['id'])
 for p in [w/'.tmp',w/'.cache/matplotlib',h,r,a/'sock']:p.mkdir(parents=True,exist_ok=True)
 shutil.copytree(Path(j['case_path'])/'inputs',w/'inputs',dirs_exist_ok=True)
 for p in (w/'inputs').rglob('*'):
  if p.is_file():p.chmod(0o444)
 (a/'prompt.txt').write_text(solver_prompt(j))
 save(h/'settings.json',{'cleanupPeriodDays':100000,'includeCoAuthoredBy':False,'permissions':{'deny':['WebFetch','WebSearch','Agent','Task','Skill']},
  'enabledPlugins':{'cc-plugin-agents-md@builtin':False,'cc-plugin-plugin-authoring@builtin':False}})
 (w/'sibling-canary.txt').write_text('private to this attempt\n')
 save(a/'job.json',j)
 hashes={str(p.relative_to(w)):sha(p) for p in (w/'inputs').rglob('*') if p.is_file()}
 save(r/'frozen.json',{'prompt':sha(a/'prompt.txt'),'settings':sha(h/'settings.json'),'claude_sha256':CLAUDE_SHA256,
  'argv':claude_argv(j),'tools':TOOLS,'inputs':hashes})
def scope(j,inner,suffix):
 unit=json.loads((ROOT/'control/settings.json').read_text())['service_prefix']+'-'+j['id']+'-'+suffix+'-'+str(time.time_ns())+'.scope'
 return ['systemd-run','--user','--scope','--quiet','--unit='+unit,'--property=CPUQuota=200%','--property=MemoryMax=5G','--property=MemorySwapMax=0','--property=TasksMax=128','--',*inner],unit
def blocked_paths(j):
 a,w,h,r=paths(j)
 out=[ROOT/'control/private-canary.txt',ROOT/'references',ROOT/'scoring_v5',auth_proxy.KEY_FILE,Path('<HOME>/.codex/auth.json'),
  Path('<HOME>/.ssh'),Path('<HOME>/.aws'),ROOT.parent/('pxrd-matched-p0-eval15-20261007/attempts/P0-exp-%s-r1/workspace/result.json'%j['case_id']),
  ROOT.parent/'pxrd-autonomous-v6-refinement-eval15-20261015/references',ROOT.parent/('pxrd-tungstate15-baseline-20260919/references/%s.json'%j['case_id'])]
 out+=[Path(p) for p in j.get('extra_forbidden',[])]
 return [str(p) for p in out if p.exists()]
def preflight(j):
 """Model-free probe run inside the exact attempt sandbox (same checks as matched P0)."""
 a,w,h,r=paths(j)
 settings={'blocked':blocked_paths(j),'index':str(INDEX),'index_sha256':INDEX_SHA256,'cifs':str(CIFS),'excluded':[],'role':'solver','baseline':j.get('policy')=='P0'}
 src=(ROOT/'control/probe.py').read_text().replace('__SETTINGS__',repr(settings))
 src=src.replace("['OPENAI_API_KEY','CODEX_API_KEY',","['OPENAI_API_KEY','CODEX_API_KEY','ANTHROPIC_AUTH_TOKEN',")
 cmd,_=scope(j,bwrap(j,[str(CORE/'bin/python'),'-c',src],network_bridge=False),'probe')
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
 (r/'preflight.stdout').write_text(p.stdout);(r/'preflight.stderr').write_text(p.stderr)
 try:d=json.loads(p.stdout)
 except Exception:d={'passed':False,'error':(p.stdout+p.stderr)[-2500:]}
 d['checks']=d.get('checks',{});d['checks']['claude_binary_hash']=sha(CLAUDE)==CLAUDE_SHA256
 d['passed']=bool(d.get('passed')) and d['checks']['claude_binary_hash']
 d.update(returncode=p.returncode,checked_at=now());save(r/'preflight.json',d)
 if p.returncode or not d['passed']:raise RuntimeError(j['id']+' preflight '+json.dumps(d))
 return d
def run(j):
 a,w,h,r=paths(j)
 if (r/'launch.json').exists():return json.loads((r/'launch.json').read_text())
 if (ROOT/'control/STOP_DISPATCH.json').exists():raise RuntimeError('Dispatch stopped; no model launched')
 if not (r/'frozen.json').exists():prepare(j)
 else:j=json.loads((a/'job.json').read_text())
 preflight(j)
 return _launch(j,claude_argv(j),(a/'prompt.txt').read_text(),{'prompt_sha256':sha(a/'prompt.txt')},'START')
def _launch(j,argv,prompt,extra,label):
 a,w,h,r=paths(j)
 token='sk-ant-oat01-attempt-'+secrets.token_urlsafe(32)
 proxy=auth_proxy.start(a/'sock/proxy.sock',token,r/'proxy.jsonl')
 inner=['/usr/bin/python3',str(ROOT/'control/bridge.py'),str(PORT),str(a/'sock/proxy.sock'),'--',*argv]
 cmd,unit=scope(j,bwrap(j,inner,token),'run')
 rec={**j,**extra,'status':'running','started_at':now(),'systemd_unit':unit,'argv':argv,'host':os.uname().nodename,'harness':'claude-code-2.1.299'}
 save(r/'launch.json',rec);log(j['id']+' '+label)
 def consume(pipe,path,events):
  with path.open('w',buffering=1) as f:
   for line in pipe:
    f.write(line)
    if not events:continue
    try:e=json.loads(line)
    except ValueError:continue
    t=e.get('type')
    if t=='system' and e.get('subtype')=='init':
     rec['session_id']=e.get('session_id')
     rec['init']={k:e.get(k) for k in ['model','tools','mcp_servers','permissionMode','cwd','claude_code_version','apiKeySource']}
    elif t=='assistant':
     for c in e.get('message',{}).get('content',[]):
      if c.get('type')=='text' and c.get('text','').strip():
       with (r/'messages.log').open('a') as m:m.write(c['text']+'\n\n')
       log(j['id']+' '+c['text'][:1800])
    elif t=='result':
     rec['result']={k:e.get(k) for k in ['subtype','is_error','num_turns','duration_ms','duration_api_ms','total_cost_usd','usage','modelUsage','permission_denials','stop_reason']}
     rec['usage']=e.get('usage',{})
     (r/'final-answer.md').write_text(str(e.get('result') or ''))
     log(j['id']+' RESULT '+json.dumps({k:rec['result'].get(k) for k in ['subtype','is_error','num_turns','total_cost_usd']}))
     text=json.dumps(e).lower()
     if e.get('is_error') and any(s in text for s in STOP_MARKERS):
      save(ROOT/'control/STOP_DISPATCH.json',{'at':now(),'job':j['id'],'reason':'API service/auth error; preserve unfinished jobs and stop new launches.','result':str(e.get('result'))[:2000]})
      rec['infrastructure_failure']='service_error'
 try:
  p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
  threads=[threading.Thread(target=consume,args=(p.stdout,r/'claude-events.jsonl',True)),threading.Thread(target=consume,args=(p.stderr,r/'claude-stderr.log',False))]
  for t in threads:t.start()
  p.stdin.write(prompt);p.stdin.close();timeout=False
  try:p.wait(timeout=j.get('timeout_seconds'))
  except subprocess.TimeoutExpired:
   timeout=True;subprocess.run(['systemctl','--user','stop',unit],capture_output=True);p.wait(timeout=30)
  for t in threads:t.join(timeout=30)
  ok=p.returncode==0 and rec.get('result',{}).get('subtype')=='success' and not rec.get('result',{}).get('is_error')
  rec.update(status='timed_out' if timeout else 'finished' if ok else 'failed',returncode=p.returncode,timed_out=timeout)
 except BaseException as exc:
  subprocess.run(['systemctl','--user','stop',unit],capture_output=True);rec.update(status='launcher_error',error=repr(exc))
 finally:
  # End every process in the attempt scope before freezing the outcome.
  subprocess.run(['systemctl','--user','stop',unit],capture_output=True)
  proxy.shutdown();proxy.server_close();(a/'sock/proxy.sock').unlink(missing_ok=True)
  rec['ended_at']=now()
  rec['elapsed_seconds']=(datetime.datetime.fromisoformat(rec['ended_at'])-datetime.datetime.fromisoformat(rec['started_at'])).total_seconds()
  frozen=json.loads((r/'frozen.json').read_text())
  rec['inputs_unchanged']=all((w/f).is_file() and sha(w/f)==v for f,v in frozen['inputs'].items())
  rec['outputs_present']={f:(w/f).exists() for f in ['result.json','fit.csv','report.md','final.gpx']}
  rec['proxy']=auth_proxy.summarize(r/'proxy.jsonl')
  if not rec['inputs_unchanged']:rec['infrastructure_failure']='immutable_inputs_modified'
  if rec['proxy']['non_cli_user_agents'] or rec['proxy']['rejected'] or rec['proxy']['sessions'] not in ([],[rec.get('session_id')]):
   rec['proxy_flag']='non-CLI, foreign-session or rejected API requests; review proxy.jsonl'
  save(r/'launch.json',rec)
 log(j['id']+' '+rec['status'].upper());return rec
CONTINUE_TEXT=('Your previous session ended early because the Claude service usage limit was reached. Your conversation history and every file '
 'in the working directory are intact; processes that were still running when the session ended were stopped. Continue the original task '
 'from where you left off. The original instructions and output requirements are unchanged.\n')
def segments(a):
 """Launch records of every segment of an attempt, oldest first (run-seg1, run-seg2, ..., run)."""
 a=Path(a);out=[]
 for d in sorted(a.glob('run-seg*'),key=lambda p:int(p.name[7:]))+[a/'run']:
  if (d/'launch.json').exists():out.append({**json.loads((d/'launch.json').read_text()),'_dir':d.name})
 return out
def interruption(a):
 """Why the latest segment ended, if it was the service rather than the solver. None means not eligible."""
 a,w,h,r=paths({'id':Path(a).name}) if not isinstance(a,tuple) else a
 L=json.loads((r/'launch.json').read_text())
 if L.get('status') not in ('failed','launcher_error'):return None
 if L.get('infrastructure_failure')=='service_error':return 'service_error flagged'
 res=L.get('result') or {}
 text=(str((r/'final-answer.md').read_text()) if (r/'final-answer.md').exists() else '').lower()
 px=[json.loads(l) for l in (r/'proxy.jsonl').read_text().splitlines() if l.strip()] if (r/'proxy.jsonl').exists() else []
 tail=[x.get('status') for x in px[-5:]]
 if res.get('is_error') and any(k in text for k in ['limit','api error','overloaded','rate']):return 'error result: '+text[:200]
 if tail and all(t in (429,529) for t in tail[-2:]):return 'proxy shows %s at end'%tail
 return None
def resume(j,allow=False,instruction=CONTINUE_TEXT):
 """Resume an interrupted attempt in place: same sandbox, workspace and Claude session (claude -p --resume)."""
 a,w,h,r=paths(j)
 if (ROOT/'control/STOP_DISPATCH.json').exists():raise RuntimeError('STOP_DISPATCH present; clear it after the usage limit resets')
 j=json.loads((a/'job.json').read_text())
 parent=json.loads((r/'launch.json').read_text())
 why=interruption((a,w,h,r))
 if not why and not allow:raise RuntimeError(j['id']+' is not a service interruption (status %s); pass --allow to override'%parent.get('status'))
 unit=parent.get('systemd_unit')
 if unit and subprocess.run(['systemctl','--user','show',unit,'--property=ActiveState','--value'],capture_output=True,text=True).stdout.strip() in ('active','activating'):
  raise RuntimeError(j['id']+' scope still active')
 sid=parent.get('session_id')
 if not sid:
  for line in (r/'claude-events.jsonl').read_text().splitlines():
   try:e=json.loads(line)
   except ValueError:continue
   if e.get('type')=='system' and e.get('subtype')=='init':sid=e.get('session_id');break
 found=list(h.glob('projects/*/%s.jsonl'%sid)) if sid else []
 if len(found)!=1:raise RuntimeError(j['id']+' needs exactly one session transcript for %s, found %d'%(sid,len(found)))
 frozen=json.loads((r/'frozen.json').read_text())
 if not all((w/f).is_file() and sha(w/f)==v for f,v in frozen['inputs'].items()):raise RuntimeError(j['id']+' inputs changed; not resumable')
 n=len(list(a.glob('run-seg*')))+1
 r.rename(a/('run-seg%d'%n));r.mkdir()
 shutil.copy2(a/('run-seg%d'%n)/'frozen.json',r/'frozen.json')
 info={'segment':n+1,'previous_segment':'run-seg%d'%n,'resumed_session_id':sid,'session_transcript':str(found[0]),
       'session_transcript_sha256_at_resume':sha(found[0]),'interruption':why or 'manual override','continuation_prompt_sha256':hashlib.sha256(instruction.encode()).hexdigest(),'at':now()}
 save(r/'segment.json',info);(r/'continuation_prompt.txt').write_text(instruction)
 preflight(j)
 return _launch(j,claude_argv(j)+['--resume',sid],instruction,info,'RESUME segment %d'%(n+1))
def main():
 p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('--ids',nargs='*');p.add_argument('--workers',type=int,default=1)
 p.add_argument('--prepare-only',action='store_true');p.add_argument('--probe-only',action='store_true')
 p.add_argument('--resume',action='store_true',help='resume service-interrupted attempts in place');p.add_argument('--allow',action='store_true',help='with --resume and --ids: resume even if not detected as a service interruption')
 p.add_argument('--dry-run',action='store_true',help='with --resume: only report eligibility');args=p.parse_args()
 jobs=[j for j in json.loads(Path(args.manifest).read_text()) if not args.ids or j['id'] in args.ids]
 if args.prepare_only:
  for j in jobs:prepare(j)
  return
 if args.probe_only:
  for j in jobs:
   if not (paths(j)[3]/'frozen.json').exists():prepare(j)
   print(json.dumps(preflight(j)),flush=True)
  return
 if args.resume:
  todo=[]
  for j in jobs:
   a,w,h,r=paths(j)
   if not (r/'launch.json').exists():print(j['id'],'never launched');continue
   why=interruption((a,w,h,r));st=json.loads((r/'launch.json').read_text())['status']
   print(j['id'],st,'->','RESUME ('+why+')' if why else ('RESUME (manual)' if args.allow and args.ids else 'skip'),flush=True)
   if why or (args.allow and args.ids):todo.append(j)
  if args.dry_run:return
  target=lambda j:resume(j,allow=args.allow)
 else:todo,target=jobs,run
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
  fs={ex.submit(target,j):j for j in todo}
  for f in concurrent.futures.as_completed(fs):
   try:f.result()
   except Exception as exc:log(fs[f]['id']+' LAUNCH ERROR '+repr(exc))
if __name__=='__main__':main()
