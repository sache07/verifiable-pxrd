"""Offline rescoring of immutable saved attempts. No agent or API calls."""
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
from common import ROOT,read_json,save_json,code_hashes
from score import score_attempt

def main():
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=6);p.add_argument('--ids',nargs='*')
    p.add_argument('--resume',action='store_true');p.add_argument('--manifest',default='attempts.json');args=p.parse_args()
    records=read_json(ROOT/args.manifest)
    if args.ids:records=[r for r in records if r['id'] in args.ids]
    if args.resume:
        def finished(r):
            p=ROOT/'scores'/r['id']/'score.json'
            if not p.exists():return False
            s=read_json(p)
            return s.get('score_status')!='verification_error' and not s.get('registration_errors')
        records=[r for r in records if not finished(r)]
    save_json(ROOT/'implementation_hashes.json',code_hashes())
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for f in as_completed([pool.submit(score_attempt,r) for r in records]):
            r=f.result();print(dict(id=r['id'],score=r['score_100'],status=r['score_status'],error=r.get('error')),flush=True)

if __name__=='__main__':main()
