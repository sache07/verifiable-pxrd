"""Immutable atomic models, native GSAS profiles, no GPX I/O in the fit loop.

The preparation follows GSASIIstrMain's powder-profile setup. Only isotropic
size, isotropic microstrain and March-Dollase ratio/axis may change afterwards.
Each histogram contains one phase, so numerical derivatives only recompute
the phase whose specimen parameters changed.
"""
from collections import OrderedDict
import numpy as np
from GSASII import GSASIIstrIO as IO
from GSASII import GSASIIstrMath as M
from GSASII import GSASIIpwd as PW
from GSASII import GSASIIlattice as LAT


class MemoryProfiles:
    def __init__(self, native, folder):
        self.project = native.project
        self.names, self.histograms, self.masses = native.names, native.histograms, native.masses
        self.project.save()
        gpx = str(folder/'continuous.gpx')
        self.hist, self.phases = IO.GetUsedHistogramsAndPhases(gpx)
        self.controls = dict(IO.GetControls(gpx))
        rigid = IO.GetRigidBodies(gpx)
        ids = rigid.get('RBIds', {'Vector':[], 'Residue':[]})
        _, rb = IO.GetRigidBodyModels(rigid, Print=False)
        (natoms, atomidx, _, phase, pawley, ff, ef, orb, bl, mf, maxss) = IO.GetPhaseData(
            self.phases, {}, ids, Print=False)
        self.controls.update(atomIndx=atomidx, Natoms=natoms, FFtables=ff,
                             EFtables=ef, ORBtables=orb, BLtables=bl,
                             MFtables=mf, maxSSwave=maxss)
        _, hap, c = IO.GetHistogramPhaseData(self.phases, self.hist, Controls=self.controls, Print=False)
        self.controls.update(c)
        _, hist, self.hist1, c = IO.GetHistogramData(self.hist, Print=False)
        self.controls.update(c)
        self.parms = {**rb, **phase, **hap, **hist}
        IO.GetFprime(self.controls, self.hist)
        self.pawley = pawley
        self.prefix = [f"{self.phases[name]['pId']}:{self.hist[h]['hId']}:"
                       for name,h in zip(self.names,self.histograms)]
        self.x = np.asarray(self.hist[self.histograms[0]]['Data'][0])
        self.cache = [OrderedDict() for _ in self.names]
        self.calls = 0
        self.phase_calls = [0 for _ in self.names]
        self.cache_hits = 0
        self.immutable_parameters = dict(self.parms)
        self.allowed_parameters = {p+k for p in self.prefix for k in ['Size;i','Mustrain;i','MD']}
        self.banks = [self._prepare_bank(i) for i in range(len(self.names))]

    def _prepare_bank(self, i):
        """Cache native reflection positions, |F|², and all fixed corrections.

        For isotropic CW broadening, sigma is quadratic and gamma linear in
        reciprocal size and strain. Obtain their coefficients from GSAS itself.
        FCJ peak evaluation and truncation still call GSAS's native routines.
        """
        name,h,p=self.names[i],self.histograms[i],self.prefix[i]
        hf=f":{self.hist[h]['hId']}:"
        pf=f"{self.phases[name]['pId']}::"
        phase=self.phases[name]
        if self.controls[hf+'histType']!='PXC' or phase['General'].get('Modulated',False):
            raise ValueError('Fast evaluator supports non-modulated constant-wavelength X-ray profiles')
        if self.controls[p+'SizeType']!='isotropic' or self.controls[p+'MustrainType']!='isotropic':
            raise ValueError('Fast evaluator requires isotropic size and strain')
        self.parms[p+'MD']=1.
        self.parms[p+'Size;i']=1.
        self.parms[p+'Mustrain;i']=0.
        M.getPowderProfile(self.parms,self.hist1,self.x,[],self.hist[h],self.phases,self.controls,self.pawley)
        sg=phase['General']['SGData']
        ops=np.array([op[0].T for op in sg['SGOps']])
        dij=M.GetDij(p,sg,self.parms)
        avec=[self.parms[pf+f'A{j}']+dij[j] for j in range(6)]
        G,g=LAT.A2Gmat(avec)
        _,GB=LAT.Gmat2AB(G)
        vst=np.sqrt(np.linalg.det(G))
        wave=self.parms.get(hf+'Lam1',self.parms.get(hf+'Lam'))
        shl=max(self.parms[hf+'SH/L'],.002)
        ka2=hf+'Lam1' in self.parms
        lr=360*(self.parms[hf+'Lam2']-wave)/(np.pi*wave) if ka2 else 0.
        kr=self.parms[hf+'I(L2)/I(L1)'] if ka2 else 0.
        peaks=[]
        for refl in self.hist[h]['Reflection Lists'][name]['RefList']:
            pos=M.GetReflPos(refl,0,wave,avec,pf,hf,p,self.controls,self.parms)
            refl[5]=pos
            c=M.cosd(pos/2);tan=M.tand(pos/2)
            lorenz=1/(2*M.sind(pos/2)**2*c)
            uniq=np.inner(refl[:3],ops)
            intensity=M.GetIntensityCorr(refl,0,uniq,G,g,pf,p,hf,sg,self.controls,self.parms)[0]
            intensity *= vst*lorenz*refl[9]/10000.
            sig0=self.parms[hf+'U']*tan**2+self.parms[hf+'V']*tan+self.parms[hf+'W']
            gam0=self.parms[hf+'X']/c+self.parms[hf+'Y']*tan+self.parms[hf+'Z']
            self.parms[p+'Mustrain;i']=0.
            ss,gs=M.GetSampleSigGam(refl,0,wave,G,GB,sg,hf,p,self.controls,self.parms)
            self.parms[p+'Mustrain;i']=1.
            sm,gm=M.GetSampleSigGam(refl,0,wave,G,GB,sg,hf,p,self.controls,self.parms)
            self.parms[p+'Mustrain;i']=0.
            peaks.append(dict(pos=pos,pos2=pos+lr*tan,intensity=intensity,
                              sig0=sig0,gam0=gam0,ss=ss,gs=gs,sm=sm-ss,gm=gm-gs,
                              uniq=uniq))
        return dict(peaks=peaks,shl=shl,ka2=ka2,kr=kr,G=G,angle_cache={},kernels=OrderedDict())

    def _profile(self,i,s):
        bank=self.banks[i]
        axis=tuple(s['md_axis'])
        if axis not in bank['angle_cache']:
            bank['angle_cache'][axis]=[np.array([LAT.CosSinAngle(h,axis,bank['G'])[0]**2
                                               for h in p['uniq']]) for p in bank['peaks']]
        size,strain,md=s['size_um'],s['microstrain_ppm'],s['md_ratio']
        key=(size,strain)
        kernels=bank['kernels']
        if key not in kernels:
            matrix=np.zeros((len(bank['peaks']),len(self.x)))
            for j,p in enumerate(bank['peaks']):
                sig=max(.001,p['sig0']+p['ss']/size**2+p['sm']*strain**2)
                gam=max(.001,p['gam0']+p['gs']/size+p['gm']*strain)
                stop=False
                for pos,mult in ([(p['pos'],1.),(p['pos2'],bank['kr'])] if bank['ka2'] else [(p['pos'],1.)]):
                    _,left,right=PW.getWidthsCW(pos,sig,gam,bank['shl'])
                    start,end=np.searchsorted(self.x,[pos-left,pos+right])
                    if not start+end:continue
                    if start==end:
                        stop=True
                        break
                    if start>end:continue
                    fp=PW.getFCJVoigt3(pos,sig,gam,bank['shl'],self.x[start:end])[0]
                    matrix[j,start:end] += p['intensity']*mult*fp
                if stop:break
            kernels[key]=matrix
            while len(kernels)>1 and (len(kernels)>4 or sum(v.nbytes for v in kernels.values())>64*1024**2):
                kernels.popitem(last=False)
        kernels.move_to_end(key)
        orientation=[]
        for cos2 in bank['angle_cache'][axis]:
            ori=1. if md==1. else np.mean((md**2*cos2+(1-cos2)/md)**-1.5)
            orientation.append(ori)
        return np.asarray(orientation)@kernels[key]

    def calculate(self, specs):
        values=[]
        self.calls += 1
        for i,(h,p,s) in enumerate(zip(self.histograms,self.prefix,specs)):
            key=(s['size_um'],s['microstrain_ppm'],s['md_ratio'],*s['md_axis'])
            cache=self.cache[i]
            if key in cache:
                cache.move_to_end(key)
                self.cache_hits += 1
                values.append(cache[key])
                continue
            self.parms[p+'Size;i']=float(s['size_um'])
            self.parms[p+'Mustrain;i']=float(s['microstrain_ppm'])
            self.parms[p+'MD']=float(s['md_ratio'])
            self.controls[p+'MDAxis']=list(s['md_axis'])
            profile=self._profile(i,s)
            if not np.isfinite(profile).all() or profile.max()<=0 or profile.min() < -1e-7*profile.max():
                raise ValueError('Invalid in-memory native profile')
            profile=np.maximum(profile,0)
            cache[key]=profile
            if len(cache)>256:cache.popitem(last=False)
            self.phase_calls[i] += 1
            values.append(profile)
        return np.asarray(values)

    def assert_fixed_model(self):
        for key,value in self.immutable_parameters.items():
            if key in self.allowed_parameters:continue
            if not np.array_equal(np.asarray(value),np.asarray(self.parms[key])):
                raise ValueError('Native fit changed a fixed parameter: '+key)
