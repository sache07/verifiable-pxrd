"""Fixed GSAS-II forward calculation; invoke with the GSAS environment."""
from pathlib import Path
import json
import sys
import numpy as np
from GSASII import GSASIIscriptable as G2
from GSASII import GSASIIpath
from gsas_worker_text import instrument_text

def run(request, output):
    G2.SetPrintLevel('error')
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    root=output.parent
    inst=root/'instrument.instprm'
    inst.write_text(instrument_text(request['instrument']))
    project=G2.G2Project(newgpx=str(root/'forward.gpx'))
    phases=[project.add_phase(str(Path(c).resolve()),phasename=f'phase_{i}',fmthint='CIF') for i,c in enumerate(request['cifs'])]
    masses=np.array([p.data['General']['Mass'] for p in phases],float)
    if not np.all(np.isfinite(masses)) or np.min(masses)<=0:
        raise ValueError('nonpositive GSAS unit-cell mass')
    histograms=[]
    combined=request.get('combined_fractions')
    default_profile={'size_um':float(request['domain_size_um']), 'microstrain_ppm':0., 'md_ratio':1., 'md_axis':[0,0,1]}
    phase_profiles=request.get('phase_profiles',[default_profile for p in phases])
    variants=request.get('profile_variants')
    if variants is not None:
        groups=[([p],[spec]) for p,options in zip(phases,variants) for spec in options]
    elif combined is not None:
        groups=[(phases,phase_profiles)]
    else:
        groups=[([p],[spec]) for p,spec in zip(phases,phase_profiles)]
    for i,(selected,specs) in enumerate(groups):
        hist=project.add_simulated_powder_histogram(
            f'profile_{i}',str(inst),request['grid']['min'],request['grid']['max'],
            Tstep=request['grid']['step'],scale=1.0,phases=selected)
        hist.SampleParameters['Scale']=[1.0,False]
        hist.SampleParameters['Type']='Bragg-Brentano'
        sample=request.get('sample_parameters')
        if sample is not None:
            # Whole-specimen effects in GSAS-II's own Bragg-Brentano convention.
            sp=hist.SampleParameters
            sp['Gonio. radius']=float(sample['goniometer_radius_mm'])
            sp['Shift']=[float(sample['shift_um']),False]
            sp['Transparency']=[float(sample['transparency']),False]
            sp['SurfRoughA']=[float(sample['surf_rough_A']),False]
            sp['SurfRoughB']=[float(sample['surf_rough_B']),False]
        hist.set_refinements({'Background':{'type':'chebyschev-1','no. coeffs':3,'coeffs':[0.,0.,0.],'refine':False}})
        for p,spec in zip(selected,specs):
            index=phases.index(p)
            hap=p.data['Histograms'][hist.name]
            # GSAS-II mass fractions are Scale * unit-cell mass, normalized.
            # 10000 is a common numerical multiplier, removed from the output.
            hap['Scale']=[10000.0*(float(combined[index]) if combined is not None else 1.0)/masses[index],False]
            hap['Size'][0]='isotropic'
            hap['Size'][1][0]=float(spec['size_um'])
            hap['Size'][1][1]=float(spec['size_um'])
            hap['Size'][2]=[False,False,False]
            axial=spec.get('microstrain_axial_ppm')
            if axial is not None and float(axial)!=float(spec['microstrain_ppm']):
                # Uniaxial microstrain: GSAS-II Mustrain;i perpendicular to the axis, Mustrain;a along it.
                hap['Mustrain'][0]='uniaxial'
                hap['Mustrain'][1][0]=float(spec['microstrain_ppm'])
                hap['Mustrain'][1][1]=float(axial)
                hap['Mustrain'][3]=list(spec['microstrain_axis'])
            else:
                hap['Mustrain'][0]='isotropic'
                hap['Mustrain'][1][0]=float(spec['microstrain_ppm'])
                hap['Mustrain'][1][1]=float(spec['microstrain_ppm'])
            hap['Mustrain'][2]=[False,False,False]
            hap['Pref.Ori.'][0]='MD'
            hap['Pref.Ori.'][1]=float(spec['md_ratio'])
            hap['Pref.Ori.'][2]=False
            hap['Pref.Ori.'][3]=list(spec['md_axis'])
            hap['Extinction']=[0.,False]
        histograms.append(hist)
    project.set_Controls('cycles',0)
    project.refine()
    arrays=[np.array(project.histogram(h.name).data['data'][1][3],float)/10000.0 for h in histograms]
    x=np.array(project.histogram(histograms[0].name).data['data'][1][0],float)
    profiles=np.stack(arrays)
    if not np.all(np.isfinite(profiles)) or np.max(profiles)<=0 or np.min(profiles)<-1e-7*np.max(profiles):
        raise ValueError('invalid calculated intensity')
    profiles=np.maximum(profiles,0)
    np.savez_compressed(output,x=x,profiles=profiles,masses=masses)
    info={'GSAS_II_revision':GSASIIpath.GetVersionNumber(),'unit_cell_masses_amu':masses.tolist(),
          'cells':[p.data['General']['Cell'][1:] for p in project.phases()],
          'instrument':request['instrument'],'domain_size_um':request['domain_size_um'],
          'mass_scale_convention':'HAP Scale = 10000 * mass_fraction / unit_cell_mass; output divided by common 10000',
          'varyList':project.data.get('Covariance',{}).get('data',{}).get('varyList',[])}
    if 'phase_profiles' in request:info['phase_profiles']=request['phase_profiles']
    if request.get('sample_parameters') is not None:
        info['sample_parameters']=request['sample_parameters']
        for h in histograms:
            sp=project.histogram(h.name).data['Sample Parameters']
            used={'goniometer_radius_mm':sp['Gonio. radius'],'shift_um':sp['Shift'][0],'transparency':sp['Transparency'][0],
                  'surf_rough_A':sp['SurfRoughA'][0],'surf_rough_B':sp['SurfRoughB'][0]}
            if any(abs(float(used[k])-float(v))>1e-12 for k,v in request['sample_parameters'].items()):
                raise RuntimeError('forward calculation changed a sample parameter')
    if variants is not None:info['profile_variants']=variants
    if info['varyList']:
        raise RuntimeError('forward calculation unexpectedly refined parameters')
    output.with_suffix('.json').write_text(json.dumps(info,indent=2)+'\n')

if __name__=='__main__':
    run(json.loads(Path(sys.argv[1]).read_text()),sys.argv[2])
