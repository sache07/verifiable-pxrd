"""Score attempts with the primary (frozen) and secondary (grid-tolerant) evaluators.
Usage: score_attempts.py ROOT ID [ID ...]   (ROOT holds attempts/, cases/ and jobs/)"""
import concurrent.futures, json, os, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SCORERS={'primary':R/'control/evaluate_attempt.py','secondary_gridtol':R/'secondary_gridtol/control/evaluate_attempt.py'}
def one(args):
    root,jid,kind=args
    env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
    p=subprocess.run([sys.executable,str(SCORERS[kind]),root,jid],env=env,capture_output=True,text=True,timeout=900)
    out=SCORERS[kind].parents[1]/'analysis/attempts'/jid
    out.mkdir(parents=True,exist_ok=True);(out/'assessment.log').write_text(p.stdout+'\n'+p.stderr)
    return jid,kind,p.returncode,p.stdout.strip()[-300:]
if __name__=='__main__':
    root,ids=sys.argv[1],sys.argv[2:]
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get('SCORE_WORKERS','4'))) as ex:
        for jid,kind,rc,msg in ex.map(one,[(root,i,k) for i in ids for k in SCORERS]):
            print(kind,jid,'rc=%d'%rc,msg,flush=True)
