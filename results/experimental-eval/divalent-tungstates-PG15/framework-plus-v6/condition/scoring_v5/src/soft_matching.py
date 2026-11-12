"""Periodic, occupancy-capacitated atom transport; no all-atom pass/fail gate.

Registration uses a deterministic finite multistart search, not a claim of a
certified global continuous optimum. All lattice mappings and atom-coincidence
origins are screened; the strongest distinct origins are continuously refined.
Resource-limit failures are explicit rather than fabricated nonmatches.
"""
from functools import lru_cache
from pathlib import Path
import hashlib, json, os, tempfile, warnings
import numpy as np
from scipy.optimize import linear_sum_assignment, linprog, minimize
from scipy.sparse import csr_matrix
from pymatgen.util.coord import pbc_shortest_vectors
from common import CONFIG, ROOT, sha

CFG=CONFIG['soft_matching']
SCALES=CFG['length_scale_sensitivity_A']


@lru_cache(maxsize=128)
def _capacity_constraints(n,m):
    k=np.arange(n*m)
    return csr_matrix((np.ones(2*n*m),(np.r_[np.repeat(np.arange(n),m),n+np.tile(np.arange(m),n)],np.r_[k,k])),shape=(n+m,n*m))


def transport(kernel, a, b):
    """Exact nonnegative transport for fixed geometry; unused mass is allowed."""
    a,b=np.asarray(a,float),np.asarray(b,float)
    flow=np.zeros_like(kernel)
    if not len(a) or not len(b):return 0.,flow
    if np.any(a<0) or np.any(b<0):raise ValueError('Negative atomic capacity')
    if np.all(a==a[0]) and np.all(b==a[0]):
        i,j=linear_sum_assignment(kernel,maximize=True)
        flow[i,j]=a[0]
    else:
        # Exact upper-bound shortcuts, particularly useful for dilute sites.
        # If each population can take its highest-valued edge without violating
        # any destination capacity, no linear-program solve is necessary.
        j=np.argmax(kernel,axis=1)
        demand=np.bincount(j,weights=a,minlength=len(b))
        if np.all(demand<=b+1e-12):
            flow[np.arange(len(a)),j]=a
            return float(np.sum(flow*kernel)),flow
        i=np.argmax(kernel,axis=0)
        demand=np.bincount(i,weights=b,minlength=len(a))
        if np.all(demand<=a+1e-12):
            flow[i,np.arange(len(b))]=b
            return float(np.sum(flow*kernel)),flow
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',message='Unrecognized options detected')
            fit=linprog(-kernel.ravel(),A_ub=_capacity_constraints(len(a),len(b)),b_ub=np.r_[a,b],
                        bounds=(0,None),method='highs',options={'threads':1})
        if not fit.success:raise RuntimeError('Atomic transport failed: '+fit.message)
        flow=fit.x.reshape(kernel.shape)
    return float(np.sum(flow*kernel)),flow


def _populations(st):
    out={}
    for i,site in enumerate(st):
        for e,v in site.species.items():
            if v>0:out.setdefault(e.symbol,[]).append((i,float(v)))
    return {e:(np.array([i for i,v in z],int),np.array([v for i,v in z],float)) for e,z in out.items()}


class RegistrationObjective:
    def __init__(self,a,b,scale,lattice):
        self.lattice=lattice;self.scale=scale
        ap,bp=_populations(a),_populations(b)
        af,bf=a.frac_coords,b.frac_coords
        self.elements=[(e,*ap[e],*bp[e],af[ap[e][0]],bf[bp[e][0]]) for e in sorted(set(ap)&set(bp))]
        self.total=float(a.composition.num_atoms+b.composition.num_atoms)

    def origin_upper_bounds(self,origins):
        """Ignore shared capacities to bound fixed-origin transport cheaply.

        Batch periodic geometry in compiled code. Only origins whose bound can
        reach the best exact shortlist need an actual transport optimization.
        """
        output=np.zeros(len(origins))
        for start in range(0,len(origins),32):
            shifts=origins[start:start+32];bound=np.zeros(len(shifts))
            for e,ai,ac,bi,bc,af,bf in self.elements:
                shifted=(bf[None,:,:]+shifts[:,None,:]).reshape(-1,3)
                _,d2=pbc_shortest_vectors(self.lattice,af,shifted,return_d2=True)
                k=np.exp(-d2.reshape(len(af),len(shifts),len(bf)).transpose(1,0,2)/self.scale**2)
                row=np.sum(np.max(k,axis=2)*ac[None,:],axis=1)
                col=np.sum(np.max(k,axis=1)*bc[None,:],axis=1)
                bound+=np.minimum(row,col)
            output[start:start+len(shifts)]=2*bound/self.total
        return output

    def evaluate(self,shift,details=False):
        reward=0.;gradient=np.zeros(3);rows=[]
        for e,ai,ac,bi,bc,af,bf in self.elements:
            vec,d2=pbc_shortest_vectors(self.lattice,af,bf+shift,return_d2=True)
            kernel=np.exp(-d2/self.scale**2)
            val,flow=transport(kernel,ac,bc);reward+=val
            gradient+=np.einsum('ij,ijk->k',flow*kernel,vec)@self.lattice.matrix.T*(-2/self.scale**2)
            if details:
                ii,jj=np.where(flow>1e-10)
                rows.extend(dict(element=e,reference_site=int(ai[i]),submitted_site=int(bi[j]),
                                 population=float(flow[i,j]),distance_A=float(np.sqrt(d2[i,j])),
                                 credit=float(flow[i,j]*kernel[i,j])) for i,j in zip(ii,jj))
        return 2*reward/self.total,2*gradient/self.total,rows


def fixed_registration(a,b,shift,scale,lattice=None,details=False):
    """q and its origin gradient for a fixed common basis and periodic metric."""
    return RegistrationObjective(a,b,scale,a.lattice if lattice is None else lattice).evaluate(shift,details)


def _canonical(st):
    s=st.copy();s.remove_oxidation_states()
    for k in list(s.site_properties):s.remove_site_property(k)
    # Reduce only exact translations, preserving species and occupancies.
    s=s.get_primitive_structure(tolerance=CFG['primitive_tolerance_A'])
    return s.get_reduced_structure('niggli')


def _geometry_signature(st):
    """Same periodic population/metric, regardless of rigid rotation or site order.

    Rounding identifies numerical roundoff from integer cell transformations;
    coordinates used for transport are never rounded or modified.
    """
    gram=np.round(st.lattice.matrix@st.lattice.matrix.T,9)
    gram[gram==0]=0.
    gram=gram.ravel().tolist()
    frac=np.mod(np.round(np.mod(st.frac_coords,1),10),1)
    sites=sorted((tuple(f),tuple(sorted(s.species.get_el_amt_dict().items()))) for f,s in zip(frac,st))
    return hashlib.sha256(json.dumps([gram,sites]).encode()).hexdigest()


def _registrations(a,b,deduplicate=True):
    swap=a.volume<b.volume
    large,small=(b,a) if swap else (a,b)
    seen=set();geometries=set();count=0
    for aligned,rotation,matrix in small.lattice.find_all_mappings(large.lattice,ltol=CFG['lattice_ltol'],
                                                       atol=CFG['lattice_angle_tol_deg'],skip_rotation_matrix=True):
        token=tuple(np.asarray(matrix,int).ravel())
        if token in seen:continue
        seen.add(token)
        expanded=small.copy();expanded.make_supercell(matrix)
        if max(len(expanded),len(large))>CFG['max_registered_atoms']:
            raise RuntimeError('Common-cell atom limit reached')
        aa,bb=(expanded,large) if swap else (large,expanded)
        if deduplicate:
            geometry=_geometry_signature(expanded)
            if geometry in geometries:continue
            geometries.add(geometry)
        count+=1
        if count>CFG['max_lattice_registrations']:raise RuntimeError('Distinct lattice registration search limit reached')
        yield aa,bb,dict(expanded_side='reference' if swap else 'submitted',matrix=np.asarray(matrix,int).tolist())


def _origins(a,b):
    ap,bp=_populations(a),_populations(b)
    shifts=[np.zeros(3)]
    for e in sorted(set(ap)&set(bp)):
        ai,_=ap[e];bi,_=bp[e]
        shifts.extend((a.frac_coords[ai,None,:]-b.frac_coords[None,bi,:]).reshape(-1,3))
    out=np.unique(np.round(np.mod(np.asarray(shifts),1),9),axis=0)
    if len(out)>CFG['max_origin_seeds']:raise RuntimeError('Origin registration search limit reached')
    return out


def _search_metric(a,b,origins,scale,lattice,upper,starts,exhaustive=False):
    problem=RegistrationObjective(a,b,scale,lattice)
    trials=[]
    bounds=problem.origin_upper_bounds(origins) if not exhaustive else np.full(len(origins),upper)
    order=sorted(range(len(origins)),key=lambda i:(-bounds[i],tuple(origins[i])))
    exact_evaluations=0
    for index in order:
        if len(trials)>=max(1,starts) and bounds[index]<trials[min(len(trials),max(1,starts))-1][0]-1e-12:break
        shift=origins[index]
        q,_,_=problem.evaluate(shift)
        exact_evaluations+=1
        trials.append((q,shift));trials.sort(key=lambda x:(-x[0],tuple(x[1])))
        trials=trials[:max(1,starts)]
        if q>=upper-1e-10:
            return q,shift,dict(screened_origins=len(origins),exact_origin_evaluations=exact_evaluations,refined_origins=0,upper_attained=True)
    bestq,bestshift=trials[0];n=0;converged=0
    for q,shift in trials[:starts]:
        def objective(z):
            v,g,_=problem.evaluate(z)
            return -v,-g
        opt=minimize(objective,shift,method='L-BFGS-B',jac=True,
                     options={'maxiter':CFG['origin_maxiter'],'ftol':1e-12,'gtol':1e-8,'maxls':30})
        n+=1;converged+=int(opt.success)
        if -opt.fun>bestq:bestq,bestshift=float(-opt.fun),np.mod(opt.x,1)
        if bestq>=upper-1e-10:break
    return bestq,bestshift,dict(screened_origins=len(origins),exact_origin_evaluations=exact_evaluations,refined_origins=n,
                              converged_origins=converged,upper_attained=bool(bestq>=upper-1e-10))


def pair_quality(reference,predicted,scales=None,starts=None):
    scales=SCALES if scales is None else scales
    starts=CFG['origin_refinement_starts'] if starts is None else starts
    a,b=_canonical(reference),_canonical(predicted)
    best={str(s):[None,None] for s in scales}; n=0
    for aa,bb,transform in _registrations(a,b):
        n+=1;origins=_origins(aa,bb)
        ap,bp=_populations(aa),_populations(bb)
        upper=2*sum(min(ap[e][1].sum(),bp[e][1].sum()) for e in set(ap)&set(bp))/(aa.composition.num_atoms+bb.composition.num_atoms)
        for scale in scales:
            for direction,metric in enumerate([aa.lattice,bb.lattice]):
                prev=best[str(scale)][direction]
                if prev is not None and prev['q']>=upper-1e-10:continue
                q,shift,search=_search_metric(aa,bb,origins,scale,metric,upper,starts)
                if prev is None or q>prev['q']+1e-12:
                    _,_,flow=fixed_registration(aa,bb,shift,scale,metric,details=True)
                    best[str(scale)][direction]=dict(q=float(np.clip(q,0,1)),origin_shift=shift.tolist(),
                        registration=transform,metric='reference' if direction==0 else 'submitted',
                        reference_lattice=aa.lattice.matrix.tolist(),submitted_lattice=bb.lattice.matrix.tolist(),
                        reference_sites=[dict(frac_coords=s.frac_coords.tolist(),species=s.species.as_dict()) for s in aa],
                        submitted_sites=[dict(frac_coords=s.frac_coords.tolist(),species=s.species.as_dict()) for s in bb],
                        transport=flow,search=search,elemental_upper_bound=float(upper))
        if all(all(v is not None and v['q']>=1-1e-10 for v in directions) for directions in best.values()):break
    out={}
    for scale,values in best.items():
        out[scale]=dict(q=0. if not n else float(np.mean([v['q'] for v in values])),
                       directional=values,status='registered' if n else 'no_commensurate_lattice_within_fixed_tolerances')
    return dict(quality_by_scale=out,lattice_registrations=n,
                registration_method='all distinct periodic metrics/populations among admissible lattice maps; all same-element atom-coincidence origins; continuous refinement of leading origins',
                global_continuous_optimum_certified=False,origin_refinement_starts=starts,
                original_atom_counts=[len(reference),len(predicted)])


def _signature(st):
    return dict(lattice=st.lattice.matrix.tolist(),sites=[dict(coords=s.frac_coords.tolist(),species=s.species.as_dict()) for s in st])


def cached_pair(reference,predicted):
    signature=dict(reference=_signature(reference),predicted=_signature(predicted),settings=CFG,
                   implementation=sha(__file__))
    token=hashlib.sha256(json.dumps(signature,sort_keys=True).encode()).hexdigest()
    folder=ROOT/'pair_cache';folder.mkdir(exist_ok=True)
    target=folder/(token+'.json')
    if target.exists():return json.loads(target.read_text()),str(target)
    compatible=ROOT/'cache_equivalent_engines.json'
    if compatible.exists():
        for engine in json.loads(compatible.read_text())['hashes']:
            legacy={**signature,'implementation':engine}
            previous=folder/(hashlib.sha256(json.dumps(legacy,sort_keys=True).encode()).hexdigest()+'.json')
            if previous.exists():return json.loads(previous.read_text()),str(previous)
    value=pair_quality(reference,predicted)
    with tempfile.NamedTemporaryFile(mode='w',dir=folder,prefix=token,suffix='.partial',delete=False) as f:
        json.dump(value,f,sort_keys=True,allow_nan=False);temp=f.name
    os.replace(temp,target)
    return value,str(target)


def assign_quality(matrix,targets,fractions,asserted_count=None):
    """Choose by q only; preserve A bounds over equally optimal assignments."""
    q=np.asarray(matrix,float)
    n,m=q.shape;asserted_count=m if asserted_count is None else asserted_count
    if not n or np.any(~np.isfinite(q)) or np.any(q<0) or np.any(q>1+1e-8):raise ValueError('Invalid quality matrix')
    tol=CFG['tie_tolerance']
    @lru_cache(None)
    def solve(i,used):
        if i==n:return (0.,0.,0.,())
        options=[solve(i+1,used)]
        for j in range(m):
            if used&(1<<j) or q[i,j]<=0:continue
            total,lo,hi,pairs=solve(i+1,used|(1<<j))
            credit=0. if fractions[j] is None else q[i,j]*min(float(targets[i]),float(fractions[j]))
            options.append((total+q[i,j],lo+credit,hi+credit,((i,j),)+pairs))
        maximum=max(z[0] for z in options)
        winners=[z for z in options if maximum-z[0]<=tol]
        selected=min(winners,key=lambda z:z[3])
        return maximum,min(z[1] for z in winners),max(z[2] for z in winners),selected[3]
    total,low,high,pairs=solve(0,0)
    F=2*total/(n+asserted_count)
    return dict(F=float(F),A=float(low) if high-low<=tol else None,A_interval=[float(low),float(high)],
                T=(F+low)/2 if high-low<=tol else None,T_interval=[(F+low)/2,(F+high)/2],
                pairs=[list(p) for p in pairs],assignment_ambiguous=bool(high-low>tol),
                interpretation='Soft occupied-atom/abundance recovery; not proof of phase identity')
