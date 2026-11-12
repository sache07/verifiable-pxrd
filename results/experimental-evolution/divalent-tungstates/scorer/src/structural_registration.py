"""Bounded, cached raw-structure registration for the structural precision score.

Cell/origin search is deterministic finite multistart, not a certified global
continuous optimum. Phase pairing and registration both maximize credited
agreement. Atomic populations use capacity transport with scattering (Z-weighted)
element weights; reference models and submitted diffraction models are never modified.
"""
from pathlib import Path
from contextlib import contextmanager
import hashlib,json,signal,time,tempfile
import numpy as np
from scipy.optimize import minimize
from pymatgen.core import Lattice
from pymatgen.util.coord import pbc_shortest_vectors
from common import ROOT,CONFIG,sha
from soft_matching import _canonical,_populations,_origins,_registrations,_geometry_signature,transport
from atomic_weighting import weighted_populations,factors,NAME

CFG=CONFIG['structural_registration']
PREC=CONFIG['structural_precision']


class SearchLimit(RuntimeError):pass

@contextmanager
def deadline(seconds):
    def stop(*_):raise SearchLimit('Structural registration time budget reached')
    previous=signal.signal(signal.SIGALRM,stop)
    signal.setitimer(signal.ITIMER_REAL,max(.001,seconds))
    try:yield
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous)


def hermite_cells(n):
    for a in range(1,n+1):
        if n%a:continue
        for d in range(1,n//a+1):
            if n%(a*d):continue
            f=n//(a*d)
            for b in range(d):
                for c in range(f):
                    for e in range(f):yield np.array([[a,b,c],[0,d,e],[0,0,f]],int)


def common_cells(a,b):
    found=False
    for item in _registrations(a,b):found=True;yield item
    if found:return
    # Preserve the previously audited 2x/3x commensurate-cell fallback.
    swap=a.volume>b.volume;small,large=(b,a) if swap else(a,b);seen=set()
    for h in hermite_cells(3):
        expanded=Lattice(h@small.lattice.matrix)
        if expanded.volume<large.volume:continue
        for _,_,mat in large.lattice.find_all_mappings(expanded,
                ltol=CONFIG['soft_matching']['lattice_ltol'],
                atol=CONFIG['soft_matching']['lattice_angle_tol_deg'],skip_rotation_matrix=True):
            if abs(round(np.linalg.det(mat)))!=2:continue
            ra,rb=(mat,h)if swap else(h,mat)
            aa=a.copy();bb=b.copy();aa.make_supercell(ra);bb.make_supercell(rb)
            if max(len(aa),len(bb))>CONFIG['soft_matching']['max_registered_atoms']:
                raise SearchLimit('Common-cell atom limit reached')
            key=(_geometry_signature(aa),_geometry_signature(bb))
            if key in seen:continue
            seen.add(key)
            if len(seen)>CONFIG['soft_matching']['max_lattice_registrations']:
                raise SearchLimit('Common-cell mapping limit reached')
            yield aa,bb,dict(kind='mutual_commensurate_2_3',reference_matrix=ra.tolist(),submitted_matrix=rb.tolist())


class Objective:
    def __init__(self,a,b):
        self.a=a;self.b=b
        A=a.lattice.matrix;B=b.lattice.matrix
        self.strain=float(np.sqrt(np.mean(np.log(np.linalg.svd(np.linalg.solve(A,B),compute_uv=False))**2)))
        self.lattice=Lattice(np.linalg.cholesky((A@A.T+B@B.T)/2))
        self.acount=a.composition.get_el_amt_dict();self.bcount=b.composition.get_el_amt_dict()
        maximum={e:max(self.acount.get(e,0),self.bcount.get(e,0)) for e in set(self.acount)|set(self.bcount)}
        self.factor=factors({e:v for e,v in maximum.items() if v>0})
        ap,bp=_populations(a),_populations(b)
        self.elements=[(e,*ap[e],*bp[e],a.frac_coords[ap[e][0]],b.frac_coords[bp[e][0]])for e in sorted(set(ap)&set(bp))]
        self.pop_upper=sum(min(ac.sum(),bc.sum())*self.factor[e] for e,ai,ac,bi,bc,af,bf in self.elements)
        self.cell_broad=1/(1+(self.strain/CFG['broad_cell_scale'])**2)
        self.cell=1/(1+(self.strain/PREC['cell_scale'])**2)
        self.cell_factor=1-PREC['cell_cap']*(1-self.cell)
        self.site_cap=PREC['position_cap']
        self.upper=self.unit(self.pop_upper,self.pop_upper)

    def unit(self,g,x):return self.cell_broad*self.cell_factor*g*(1-self.site_cap+self.site_cap*x)

    def geometry(self,shift):
        out=[]
        for e,ai,ac,bi,bc,af,bf in self.elements:
            vec,d2=pbc_shortest_vectors(self.lattice,af,bf+shift,return_d2=True)
            kb=1/(1+d2/CFG['broad_position_scale_A']**2)
            kf=1/(1+d2/PREC['position_scale_A']**2)
            out.append((e,ai,ac,bi,bc,vec,d2,kb,kf))
        return out

    def evaluate(self,shift,details=False):
        geo=self.geometry(shift)
        if not geo:return 0.,np.zeros(3),None
        flows=[transport(kb,ac,bc)[1] for e,ai,ac,bi,bc,vec,d2,kb,kf in geo]
        def values(fs):
            return tuple(sum(self.factor[g[0]]*float(np.sum(f*g[k])) for f,g in zip(fs,geo)) for k in [7,8])
        g,x=values(flows);gap=0.
        # Maximize log(G)+log(1-c+cX), a concave objective on the capacity
        # polytope. Exact linear transport oracles and exact line searches avoid
        # selecting atoms with one objective and grading with another.
        for iteration in range(64):
            if g<=0:break
            sf=1-self.site_cap+self.site_cap*x
            targets=[transport(kb/g+self.site_cap*kf/sf,ac,bc)[1]
                     for e,ai,ac,bi,bc,vec,d2,kb,kf in geo]
            tg,tx=values(targets);dg,dx=tg-g,tx-x
            gap=dg/g+self.site_cap*dx/sf
            if gap<1e-10:break
            candidates=[0.,1.]
            if abs(dg*dx*self.site_cap)>1e-24:
                t=-(dg*sf+self.site_cap*dx*g)/(2*self.site_cap*dg*dx)
                if 0<t<1:candidates.append(t)
            t=max(candidates,key=lambda t:(g+t*dg)*(sf+self.site_cap*t*dx))
            if t<1e-14:break
            flows=[f+t*(target-f) for f,target in zip(flows,targets)];g,x=values(flows)
        gradient=np.zeros(3);rows=[]
        for flow,(e,ai,ac,bi,bc,vec,d2,kb,kf) in zip(flows,geo):
            db=-kb*kb/CFG['broad_position_scale_A']**2
            df=-kf*kf/PREC['position_scale_A']**2
            derivative=self.cell_broad*self.cell_factor*((1-self.site_cap+self.site_cap*x)*db+self.site_cap*g*df)
            gradient+=2*self.factor[e]*np.einsum('ij,ijk->k',flow*derivative,vec)@self.lattice.matrix.T
            if details:
                ii,jj=np.where(flow>1e-10)
                rows.extend(dict(element=e,reference_site=int(ai[i]),submitted_site=int(bi[j]),population=float(flow[i,j]),distance_A=float(np.sqrt(d2[i,j])))for i,j in zip(ii,jj))
        detail=None
        if details:
            pops,counts=weighted_populations(self.acount,self.bcount,rows)
            detail=dict(cell_error=self.strain,populations=pops,element_populations=counts,
                        atomic_weighting=NAME,population_overlap=sum(p['coefficient']for p in pops),
                        transport=rows,transport_log_duality_gap=max(0.,float(gap)),
                        reference_lattice=self.a.lattice.matrix.tolist(),submitted_lattice=self.b.lattice.matrix.tolist(),
                        reference_sites=[dict(frac_coords=s.frac_coords.tolist(),species=s.species.get_el_amt_dict())for s in self.a],
                        submitted_sites=[dict(frac_coords=s.frac_coords.tolist(),species=s.species.get_el_amt_dict())for s in self.b],
                        origin_shift=np.mod(shift,1).tolist(),q=self.cell_broad*g,site_accuracy=x)
        return self.unit(g,x),gradient,detail

    def origin_bounds(self,origins):
        result=np.zeros(len(origins))
        for start in range(0,len(origins),32):
            shifts=origins[start:start+32];bounds=[np.zeros(len(shifts)),np.zeros(len(shifts))]
            for e,ai,ac,bi,bc,af,bf in self.elements:
                _,d2=pbc_shortest_vectors(self.lattice,af,(bf[None,:,:]+shifts[:,None,:]).reshape(-1,3),return_d2=True)
                d2=d2.reshape(len(af),len(shifts),len(bf)).transpose(1,0,2)
                for k,scale in enumerate([CFG['broad_position_scale_A'],PREC['position_scale_A']]):
                    ker=1/(1+d2/scale**2)
                    bounds[k]+=self.factor[e]*np.minimum(np.sum(ker.max(axis=2)*ac,axis=1),np.sum(ker.max(axis=1)*bc,axis=1))
            result[start:start+len(shifts)]=self.unit(*bounds)
        return result


def pair_quality(a,b,seconds=None):
    started=time.monotonic();best=0.;winner=None;count=0;searched=0;status='registered';error=None
    upper=1.;q_upper=1.
    try:
        with deadline(seconds or CFG['pair_deadline_seconds']):
            a=_canonical(a);b=_canonical(b)
            maps=[]
            for aa,bb,reg in common_cells(a,b):
                obj=Objective(aa,bb);maps.append((obj,reg))
            count=len(maps)
            upper=max((obj.upper for obj,_ in maps),default=0.)
            q_upper=max((obj.cell_broad*obj.pop_upper for obj,_ in maps),default=0.)
            for obj,reg in sorted(maps,key=lambda v:-v[0].upper):
                if obj.upper<=best+1e-10:continue
                searched+=1;origins=_origins(obj.a,obj.b);bounds=obj.origin_bounds(origins)
                ix=np.argsort(-bounds,kind='stable')[:CFG['shortlist_size']]
                trials=[]
                for i in ix:
                    val,_,_=obj.evaluate(origins[i]);trials.append((val,origins[i]))
                trials.sort(key=lambda v:(-v[0],tuple(v[1])))
                value,shift=trials[0]
                if value<obj.upper-1e-10:
                    for v,s in trials[:CFG['origin_refinement_starts']]:
                        def fun(t):
                            z,g,_=obj.evaluate(t);return -z,-g
                        fit=minimize(fun,s,jac=True,method='L-BFGS-B',options=dict(maxiter=CFG['origin_maxiter'],ftol=1e-12,gtol=1e-8,maxls=25))
                        if -fit.fun>value:value,shift=float(-fit.fun),fit.x%1
                if value>best+1e-12:
                    best=value;_,_,winner=obj.evaluate(shift,True);winner['registration']=reg
            if not maps:status='no_commensurate_lattice_within_fixed_tolerances'
    except (SearchLimit,RuntimeError) as exc:
        status='incomplete_search';error=str(exc)
    return dict(q=0. if winner is None else float(winner['q']),feature=winner,
                unit_credit=float(best),unit_upper=float(upper),q_upper=float(q_upper),
                status=status,error=error,lattice_registrations=count,searched_registrations=searched,
                seconds=time.monotonic()-started,global_continuous_optimum_certified=False)


def signature(st):
    return dict(lattice=np.round(st.lattice.matrix,10).tolist(),sites=sorted((tuple(np.round(site.frac_coords%1,10)),tuple(sorted(site.species.get_el_amt_dict().items())))for site in st))


def cached_pair(a,b,seconds=None):
    payload=dict(a=signature(a),b=signature(b),registration=CFG,precision=PREC,
                 config_sha256=sha(ROOT/'config.json'),
                 code={p:sha(Path(__file__).parent/p)for p in ['structural_registration.py','atomic_weighting.py','soft_matching.py']})
    token=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    path=ROOT/'pair_cache'/(token+'.json')
    if path.exists():return json.loads(path.read_text()),str(path)
    result=pair_quality(a,b,seconds)
    if result['status']!='incomplete_search':
        # Independent solver evaluations can discover the same pair at once.
        # Each writer needs its own temporary file before the atomic replace.
        path.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,
                prefix=path.name+'.',suffix='.partial',delete=False) as f:
            temp=Path(f.name)
            try:
                json.dump(result,f,indent=2,sort_keys=True,allow_nan=False)
                f.write('\n');f.flush();temp.replace(path)
            finally:temp.unlink(missing_ok=True)
    return result,str(path)
