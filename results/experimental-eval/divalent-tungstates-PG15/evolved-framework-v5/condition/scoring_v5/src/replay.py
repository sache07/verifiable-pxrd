"""Verify and replay a submitted final.gpx, without fitting or hidden inputs."""
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import time
import warnings
import numpy as np
from pymatgen.analysis.structure_matcher import StructureMatcher, ElementComparator
from pymatgen.io.cif import CifParser, str2float
from scipy.optimize import linear_sum_assignment
from common import ROOT, CONFIG, load_structure, read_json, save_json, sha
from export_precision import half_last_digit, tensor_bound, occupancy_tolerance, adps_agree, position_bound, cell_tolerances

BACKEND=Path('<HOME>/.local/share/characterizagent/backends/gsas2')
UV=Path('<HOME>/.local/share/uv/python')


def annotated_structure(path):
    """Attach declared element-specific displacement tensors to expanded sites.

    CIFs may omit ADPs; the saved project supplies them in that case. When
    supplied, U/B and isotropic/anisotropic declarations must agree with GPX.
    """
    st=load_structure(path)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore'); parser=CifParser(path,frac_tolerance=0)
    block=next(b for b in parser._cif.data.values() if '_atom_site_fract_x' in b.data)
    d=block.data; ops=parser.get_symops(block)
    n=len(d['_atom_site_fract_x']); values=[[] for _ in st]; adp_errors=[[] for _ in st]
    position_errors=[np.zeros(3) for _ in st]; occupancy_errors=[{} for _ in st]
    cell_keys=['_cell_length_'+axis for axis in 'abc']+['_cell_angle_'+axis for axis in ['alpha','beta','gamma']]
    st.properties['cell_rounding']=[half_last_digit(d[key]) for key in cell_keys]
    st.properties['cell_declared']=[str2float(d[key]) for key in cell_keys]
    labels=d.get('_atom_site_label',['']*n)
    aniso_labels=d.get('_atom_site_aniso_label',[])
    lattice=np.asarray(st.lattice.matrix)
    rec=np.diag(np.linalg.norm(np.linalg.inv(lattice),axis=0))
    for i in range(n):
        symbol=d.get('_atom_site_type_symbol',labels)[i]
        element=re.match(r'[A-Z][a-z]?',symbol).group()
        occ_token=d.get('_atom_site_occupancy',['1']*n)[i]
        occupancy=str2float(occ_token)
        if occupancy<=0: continue
        u=None; u_error=None
        for field,scale in [('_atom_site_U_iso_or_equiv',1.),('_atom_site_B_iso_or_equiv',1/(8*np.pi**2))]:
            if field in d and d[field][i] not in ['.','?']:
                u=np.eye(3)*str2float(d[field][i])*scale
                u_error=np.eye(3)*half_last_digit(d[field][i])*scale;break
        tensor=None; tensor_error=None
        if labels[i] in aniso_labels:
            k=aniso_labels.index(labels[i]);keys=['11','22','33','12','13','23']
            for prefix,scale in [('_atom_site_aniso_U_',1.),('_atom_site_aniso_B_',1/(8*np.pi**2))]:
                if all(prefix+key in d for key in keys):
                    v=[str2float(d[prefix+key][k])*scale for key in keys]
                    e=[half_last_digit(d[prefix+key][k])*scale for key in keys]
                    tensor=rec@np.array([[v[0],v[3],v[4]],[v[3],v[1],v[5]],[v[4],v[5],v[2]]])@rec
                    tensor_error=tensor_bound(rec,[[e[0],e[3],e[4]],[e[3],e[1],e[5]],[e[4],e[5],e[2]]])
                    break
        tokens=[d['_atom_site_fract_'+axis][i] for axis in 'xyz']
        xyz=np.array([str2float(token) for token in tokens])
        xyz_error=np.array([half_last_digit(token) for token in tokens])
        positions=[]
        for op in ops:
            pos=op.operate(xyz)%1
            if positions and np.min(st.lattice.get_all_distances([pos],positions))<1e-4:continue
            positions.append(pos)
            distances=st.lattice.get_all_distances([pos],st.frac_coords)[0]
            j=int(np.argmin(distances))
            if distances[j]>.01:raise RuntimeError('Could not associate a declared CIF atom with its expanded site')
            position_errors[j]=np.maximum(position_errors[j],np.abs(lattice.T@op.rotation_matrix)@xyz_error)
            occupancy_errors[j][element]=occupancy_errors[j].get(element,0.)+half_last_digit(occ_token)
            if tensor is not None:
                transform=lattice.T@op.rotation_matrix
                cart=transform@tensor@transform.T
                error=tensor_bound(transform,tensor_error)
            elif u is not None:cart=u;error=u_error
            else:continue
            values[j].append((element,float(occupancy),cart.tolist()))
            adp_errors[j].append(error.tolist())
    st.add_site_property('declared_adps',values)
    st.add_site_property('adp_rounding_A2',adp_errors)
    st.add_site_property('position_rounding_A',[e.tolist() for e in position_errors])
    st.add_site_property('occupancy_rounding',occupancy_errors)
    return st


def model_agrees(project_structure, submitted_structure):
    """Numerical export-consistency check, not the ground-truth recovery matcher."""
    settings=CONFIG['project_replay']['consistency']
    relative_tolerance,angle_tolerance=cell_tolerances(project_structure,submitted_structure,settings)
    def compatible(a,b):
        ca=a.species.get_el_amt_dict();cb=b.species.get_el_amt_dict()
        if any(abs(ca.get(e,0)-cb.get(e,0))>occupancy_tolerance(a,b,e,settings['occupancy_tolerance']) for e in set(ca)|set(cb)):return False
        return adps_agree(a,b,settings['adp_tolerance_A2'],settings['occupancy_tolerance'])
    # Prefer the unrotated correspondence when exported cells have the same
    # basis. A matcher may otherwise choose a symmetry-equivalent rotation
    # that amplifies harmless rounding of anisotropic displacement tensors.
    if len(project_structure)==len(submitted_structure) and np.allclose(
            project_structure.lattice.matrix,submitted_structure.lattice.matrix,
            rtol=relative_tolerance,atol=1e-7):
        good=np.array([[compatible(a,b) for b in submitted_structure] for a in project_structure])
        for j in np.flatnonzero(good[0]):
            shift=project_structure[0].frac_coords-submitted_structure[j].frac_coords
            distances=project_structure.lattice.get_all_distances(project_structure.frac_coords,submitted_structure.frac_coords+shift)
            anchor=position_bound(project_structure[0])+position_bound(submitted_structure[j])
            allowances=np.array([[max(settings['position_tolerance_A'],np.linalg.norm(position_bound(a)+position_bound(b)+anchor))
                                  for b in submitted_structure] for a in project_structure])
            allowed=good & (distances<=allowances+1e-12)
            ii,jj=linear_sum_assignment(~allowed)
            if np.all(allowed[ii,jj]):return True
    position_limit=max(settings['position_tolerance_A'],2*max(np.linalg.norm(position_bound(a)) for a in project_structure)+
                       2*max(np.linalg.norm(position_bound(b)) for b in submitted_structure))
    free_length=min((s.volume/len(s))**(1/3) for s in [project_structure,submitted_structure])
    match=StructureMatcher(ltol=relative_tolerance,stol=max(.002,position_limit/free_length),
        angle_tol=angle_tolerance,primitive_cell=False,scale=False,
        attempt_supercell=True,allow_subset=False,comparator=ElementComparator())
    if set(project_structure.composition.get_el_amt_dict())!=set(submitted_structure.composition.get_el_amt_dict()):return False
    def geometry(s):
        s=s.copy()
        for i,site in enumerate(s):
            occupied=site.species.get_el_amt_dict()
            properties=dict(site.properties,occupied_elements=occupied)
            s.replace(i,{e:1/len(occupied) for e in occupied},properties=properties)
        return s
    a0,b0=geometry(project_structure),geometry(submitted_structure)
    # The larger cell must be the target for pymatgen's correspondence routine.
    swapped=len(a0)<len(b0)
    target,moving=(b0,a0) if swapped else (a0,b0)
    aligned=match.get_s2_like_s1(target,moving)
    if aligned is None or len(aligned)!=len(target):return False
    rotation=np.linalg.solve(aligned.lattice.matrix,target.lattice.matrix)
    u,_,vh=np.linalg.svd(rotation);rotation=u@vh
    for site in aligned:
        site.properties['declared_adps']=[(e,pop,(rotation.T@np.asarray(tensor)@rotation).tolist())
                                          for e,pop,tensor in site.properties['declared_adps']]
        site.properties['adp_rounding_A2']=[tensor_bound(rotation.T,error).tolist() for error in site.properties.get('adp_rounding_A2',[])]
        site.properties['position_rounding_A']=(np.abs(rotation.T)@position_bound(site)).tolist()
    native,submitted=(aligned,target) if swapped else (target,aligned)
    anchor_error=np.max([position_bound(a)+position_bound(b) for a,b in zip(native,submitted)],axis=0)
    for a,b in zip(native,submitted):
        distance=target.lattice.get_distance_and_image(a.frac_coords,b.frac_coords)[0]
        allowance=max(settings['position_tolerance_A'],np.linalg.norm(position_bound(a)+position_bound(b)+anchor_error))
        if distance>allowance+1e-12:return False
        ca=a.properties['occupied_elements'];cb=b.properties['occupied_elements']
        if any(abs(ca.get(e,0)-cb.get(e,0))>occupancy_tolerance(a,b,e,settings['occupancy_tolerance']) for e in set(ca)|set(cb)):return False
        if not adps_agree(a,b,settings['adp_tolerance_A2'],settings['occupancy_tolerance']):return False
    return True


def isolated_replay(project, observed, dest, histogram=None):
    """The GPX loader cannot read truth, other submissions, credentials, or network."""
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    for p in dest.iterdir():
        if p.is_symlink():raise ValueError('Unsafe replay output symlink')
    save_json(dest/'request.json',{'project':'/input/final.gpx','observed':'/input/pattern.csv','histogram':histogram})
    cmd=['bwrap','--unshare-all','--die-with-parent','--new-session',
         '--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/lib','/lib',
         '--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp',
         '--ro-bind','/etc/ld.so.cache','/etc/ld.so.cache',
         '--ro-bind',str(BACKEND),str(BACKEND),'--ro-bind',str(UV),str(UV),
         '--ro-bind',str(ROOT/'runtime'),'/code','--ro-bind',str(project),'/input/final.gpx',
         '--ro-bind',str(observed),'/input/pattern.csv','--bind',str(dest),'/output','--chdir','/output',
         str(BACKEND/'venv/bin/python'),'/code/replay_worker.py','/output/request.json']
    env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
    (dest/'replay.json').unlink(missing_ok=True)
    started=time.monotonic()
    p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=120)
    (dest/'stdout.log').write_text(p.stdout);(dest/'stderr.log').write_text(p.stderr)
    if not (dest/'replay.json').exists():raise RuntimeError('Replay worker failed: '+p.stderr[-1500:])
    report=read_json(dest/'replay.json');report['wall_seconds']=time.monotonic()-started
    if report['status']=='verification_error':raise RuntimeError(report.get('error','Replay failed'))
    return report


def replay_prediction(record, rows, submission, out, eligible):
    work,case=Path(record['workspace']),Path(record['case_path'])
    x,y=np.loadtxt(case/'inputs/pattern.csv',delimiter=',',skiprows=1).T
    meta={'mode':'verified submitted-project replay','parameters_optimized':0,
          'hidden_calibration_used':False,'reference_rwp':None,'profile_review_flags':[],
          'export_consistency':'Printed-digit rounding intervals plus numerical floors; parenthesized uncertainties never widen allowances.'}
    if not eligible:return x,y,None,{**meta,'status':'incomplete_or_invalid_quantified_model'}
    project=work/'final.gpx'
    if not project.is_file():return x,y,None,{**meta,'status':'missing_final_project'}
    if project.is_symlink() or project.stat().st_size>100_000_000:
        return x,y,None,{**meta,'status':'invalid_project','error':'Unsafe or excessive project file'}
    digest=sha(project);folder=out/'project_replay'
    report=isolated_replay(project.resolve(),(case/'inputs/pattern.csv').resolve(),folder,
                           submission.get('refinement_histogram'))
    meta.update(report,source_project=str(project),project_sha256=digest)
    if sha(project)!=digest:raise RuntimeError('Project changed during evaluation')
    if report['status']!='replayed':return x,y,None,meta
    submitted=[[annotated_structure(e['path']) for e in r.get('equivalent_exports',[r])] for r in rows]
    totals=np.zeros(len(rows));assignment=[]
    for phase in report['phases']:
        native=annotated_structure(folder/phase['cif'])
        matches=[j for j,group in enumerate(submitted) if any(model_agrees(native,s) for s in group)]
        if len(matches)!=1:
            return x,y,None,{**meta,'status':'project_submission_mismatch',
                'error':'A project phase must correspond unambiguously to a submitted CIF, including declared occupancies/ADPs',
                'unmatched_project_phase':phase['name'],'matching_submission_indices':matches}
        j=matches[0];totals[j]+=phase['weight_fraction'];assignment.append({'project_phase':phase['name'],'submitted_index':j})
    declared=np.asarray([r['fraction'] for r in rows])
    errors=np.abs(totals-declared)
    if len({a['submitted_index'] for a in assignment})!=len(rows) or np.max(errors)>CONFIG['project_replay']['consistency']['fraction_absolute_tolerance']:
        return x,y,None,{**meta,'status':'project_submission_mismatch','error':'Project phase inventory or fractions differ from the submitted answer',
                         'project_fractions_in_submission_order':totals.tolist(),'fraction_absolute_errors':errors.tolist()}
    with np.load(folder/'prediction.npz',allow_pickle=False) as z:
        if not np.array_equal(z['x'],x) or not np.array_equal(z['observed'],y):raise RuntimeError('Replay grid/observations changed')
        predicted=z['predicted'].copy()
    weights=1/np.maximum(y,1.);loss=float(np.sum(weights*(y-predicted)**2));denominator=float(np.sum(weights*y*y))
    if denominator<=0:raise ValueError('Zero observed-data Rwp denominator')
    best={'calculated':predicted,'rwp_percent':float(100*np.sqrt(loss/denominator)),'chi_square':loss}
    meta.update(status='verified',phase_correspondence=assignment,project_fractions_in_submission_order=totals.tolist(),
                fraction_absolute_errors=errors.tolist(),prediction_sha256=sha(folder/'prediction.npz'))
    return x,y,best,meta
