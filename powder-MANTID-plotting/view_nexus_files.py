from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
from mantid import plots
from matplotlib.colors import LogNorm


def change_permissions(filename,permission):
    try:
        os.chmod(filename,permission)
    except OSError:
        pass

van=LoadNexus(Filename='/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/van_277537.nxs')
MaskBTP(Workspace = 'van', Instrument = 'CNCS', Bank = '5-10')
def powderNexusToMD(filename=None, van='van', tib_min = None, tib_max = None, apply_TIB = '1', T0_fitted = None):
    raw = Load(Filename=filename, OutputWorkspace='raw')
    MaskDetectors(Workspace=raw,MaskedWorkspace=van)
    Ei,_,_,T0=GetEi(InputWorkspace=raw)
    Qmax = 1.1*2*np.pi/ (   (  9/np.sqrt(Ei)  ) /2./np.sin(120./2.*np.pi/180.)   ) 

    
    if (tib_min == None) or (tib_max==None):
        if Ei < 50:
            apply_TIB = '1'
            tib_min,tib_max=SuggestTibCNCS(Ei)
        else:
            apply_TIB = '0'
            tib_min,tib_max = 0,0
 
    if T0_fitted == None:
        T0 = T0
    else:
        T0 = T0_fitted

 
    dgs,_=DgsReduction(SampleInputWorkspace=raw, 
                                    SampleInputMonitorWorkspace=raw, 
                                    DetectorVanadiumInputWorkspace=van,
                                    UseProcessedDetVan = '1',
                                    IncidentEnergyGuess=Ei, 
                                    UseIncidentEnergyGuess='1', 
                                    TimeZeroGuess=T0,
                                    IncidentBeamNormalisation='ByCurrent', 
                                    TimeIndepBackgroundSub=apply_TIB, 
                                    TibTofRangeStart=tib_min,
                                    TibTofRangeEnd=tib_max,
                                    SofPhiEIsDistribution=True) #this means should use normalization # of events

    md = ConvertToMD(InputWorkspace='dgs', QDimensions='|Q|', OutputWorkspace='md')
    md_rebin = BinMD(
                InputWorkspace='md', 
                AlignedDim0='|Q|,0,'+str(Qmax)+',50', 
                AlignedDim1='DeltaE,-'+str(0.1*Ei)+','+str(Ei)+',50', 
                OutputWorkspace='md_rebin')
    return md_rebin


buckyball_1meV_300K = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277504.nxs.h5', van, T0_fitted = 209.414))
buckyball_3p32meV_300K = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277505.nxs.h5', van, T0_fitted = 122.31))
buckyball_12meV_300K = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277506.nxs.h5', van, tib_min=21451, tib_max=23990, T0_fitted = 72.385))
buckyball_30meV_300K = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277507.nxs.h5', van, T0_fitted = 22.921))
buckyball_80meV_300K = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277508.nxs.h5', van, tib_min=6733, tib_max=9274, T0_fitted = -44.971))
buckyball_80meV_300K_noTIB = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277508.nxs.h5', van, T0_fitted = -44.971))

plotSlice(buckyball_1meV_300K, normalization = 2)
plotSlice(buckyball_3p32meV_300K, normalization = 2)
plotSlice(buckyball_12meV_300K, normalization = 2)
plotSlice(buckyball_30meV_300K, normalization = 2)
plotSlice(buckyball_80meV_300K, normalization = 2)
plotSlice(buckyball_80meV_300K_noTIB, normalization = 2)


#closeAllSliceViewers()