import os,json,errno,socket,gzip,hashlib,importlib,shutil,subprocess
from pathlib import Path
S=__SETTINGS__;w=Path.cwd();checks={};details={}
checks['input_readable']=(w/'inputs').is_dir()
required=['pattern.csv','metadata.json'] if S['role']=='solver' else ['SUMMARY.json']
if S['role']=='solver' and (w/'inputs/instrument.instprm').is_file():required.append('instrument.instprm')
for f in required:
 try:
  with (w/'inputs'/f).open('r+'):checks['readonly_'+f]=False
 except OSError as e:checks['readonly_'+f]=e.errno in [errno.EPERM,errno.EACCES,errno.EROFS]
for root in [w/'learned',w/'submission_check',w/'scorer_v5']:
 for f in root.rglob('*'):
  if f.is_file():
   try:
    with f.open('r+'):checks['readonly_helper_'+str(f.relative_to(w))]=False
   except OSError as e:checks['readonly_helper_'+str(f.relative_to(w))]=e.errno in [errno.EPERM,errno.EACCES,errno.EROFS]
p=w/'.tmp/probe';p.write_text('ok');checks['workspace_writable']=p.read_text()=='ok';p.unlink()
for i,path in enumerate(S['blocked']):
 try:
  with open(path,'rb'):checks['blocked_'+str(i)]=False
 except OSError as e:checks['blocked_'+str(i)]=e.errno in [errno.EPERM,errno.EACCES,errno.ENOENT]
try:
 s=socket.create_connection(('1.1.1.1',443),2);s.close();checks['network_blocked']=False
except OSError as e:checks['network_blocked']=e.errno in [errno.EPERM,errno.EACCES,errno.ENETUNREACH];details['network']=str(e)
for pkg in ['numpy','scipy','pymatgen','spglib','ase','pyxtal','matplotlib','pandas']:
 try:importlib.import_module(pkg);checks[pkg]=True
 except Exception as e:checks[pkg]=False;details[pkg]=str(e)
checks['no_dara']=importlib.util.find_spec('dara') is None and shutil.which('dara') is None
checks['no_secret_env']=not any(k in os.environ for k in ['OPENAI_API_KEY','CODEX_API_KEY','AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY','AWS_SESSION_TOKEN'])
p=Path(S['index']);checks['index_hash']=hashlib.sha256(p.read_bytes()).hexdigest()==S['index_sha256'];d=json.load(gzip.open(p,'rt'));ids={str(r[1]) for v in d.values() for r in v}
checks['excluded_not_indexed']=not set(S['excluded']) & ids
checks['excluded_files_absent']=not any((Path(S['cifs'])/i[0]/i[1:3]/i[3:5]/(i+'.cif')).exists() for i in S['excluded'])
i=next(iter(ids));checks['allowed_cif_readable']=(Path(S['cifs'])/i[0]/i[1:3]/i[3:5]/(i+'.cif')).read_text().strip()!=''
checks['original_resource_env']=os.environ.get('COD_METADATA') is None and os.environ.get('COD_CIFS') is None
if S.get('baseline'):
 checks['no_added_solver_guidance']=not any((w/name).exists() for name in ['TOOLS.md','AGENTS.md','OUTPUT_SCHEMA.md','submission_check'])
dic=shutil.which('dicvol14');checks['dicvol']=bool(dic) and hashlib.sha256(Path(dic).read_bytes()).hexdigest()=='317430d2806ec8e4ed8f87b70940d9315092cab0869f84e479ec1c6e3bb5e586'
r=subprocess.run([os.environ['GSAS2_PYTHON'],'-c','from GSASII import GSASIIscriptable'],capture_output=True,text=True,timeout=30);checks['gsas']=r.returncode==0
print(json.dumps({'passed':all(checks.values()),'checks':checks,'details':details}))
