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

van=LoadNexus(Filename='/SNS/CNCS/IPTS-20360/shared/autoreduce/van_273992.nxs')
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
                AlignedDim1='DeltaE,-'+str(0.1*Ei)+','+str(Ei)+',100', 
                OutputWorkspace='md_rebin')
    return md_rebin


v_foil_1meV_300K_2018 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-20360/nexus/CNCS_274486.nxs.h5', van, T0_fitted = 209.414))
v_foil_3p27meV_300K_2018 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-20360/nexus/CNCS_274478.nxs.h5', van, T0_fitted = 122.31))
v_foil_13p08meV_300K_2018 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-20360/nexus/CNCS_274473.nxs.h5', van, tib_min=21451, tib_max=23990, T0_fitted = 72.385))

v_foil_1meV_300K_2020_15p5 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-25820/nexus/CNCS_336705.nxs.h5', van, T0_fitted = 209.414))
v_foil_3p27meV_300K_2020_15p5 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-25820/nexus/CNCS_336706.nxs.h5', van, T0_fitted = 122.31))
v_foil_13p08meV_300K_2020_15p5 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-25820/nexus/CNCS_336707.nxs.h5', van, tib_min=21451, tib_max=23990, T0_fitted = 72.385))

v_foil_1meV_300K_2020_10p0 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-25820/nexus/CNCS_336708.nxs.h5', van, T0_fitted = 209.414))
v_foil_3p27meV_300K_2020_10p0 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-25820/nexus/CNCS_336709.nxs.h5', van, T0_fitted = 122.31))
v_foil_13p08meV_300K_2020_10p0 = CloneMDWorkspace(powderNexusToMD('/SNS/CNCS/IPTS-25820/nexus/CNCS_336710.nxs.h5', van, tib_min=21451, tib_max=23990, T0_fitted = 72.385))


label_1meV = ['v_foil_1meV_300K_2018\n274486', 'v_foil_1meV_300K_2020_15p5\n336705', 'v_foil_1meV_300K_2020_10p0\n336708']
plt.figure()
for idx, val in enumerate([v_foil_1meV_300K_2018, v_foil_1meV_300K_2020_15p5, v_foil_1meV_300K_2020_10p0]):
    #to access and plot the slice arrays directly
    Q_array = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[0]
    E_array = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[1]
    normalized_intensity = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[2]
    Q_mesh, E_mesh = np.meshgrid(Q_array, E_array)
    plt.plot(E_array, np.sum(normalized_intensity[:,10:40], axis = 1), label = label_1meV[idx])
plt.legend()
plt.xlabel('E (meV)')
plt.ylabel('Intensity (arb. units)')
plt.show()


label_3p27meV = ['v_foil_3p27meV_300K_2018\n274478', 'v_foil_3p27meV_300K_2020_15p5\n336706', 'v_foil_3p27meV_300K_2020_10p0\n336709']
plt.figure()
for idx, val in enumerate([v_foil_3p27meV_300K_2018, v_foil_3p27meV_300K_2020_15p5, v_foil_3p27meV_300K_2020_10p0]):
    #to access and plot the slice arrays directly
    Q_array = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[0]
    E_array = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[1]
    normalized_intensity = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[2]
    Q_mesh, E_mesh = np.meshgrid(Q_array, E_array)
    plt.plot(E_array, np.sum(normalized_intensity[:,10:40], axis = 1), label = label_3p27meV[idx])
plt.legend()
plt.xlabel('E (meV)')
plt.ylabel('Intensity (arb. units)')
plt.show()

label_13p08meV = ['v_foil_13p08meV_300K_2018\n274473', 'v_foil_13p08meV_300K_2020_15p5\n336707', 'v_foil_13p08meV_300K_2020_10p0\n336710']
plt.figure()
for idx, val in enumerate([v_foil_13p08meV_300K_2018, v_foil_13p08meV_300K_2020_15p5, v_foil_13p08meV_300K_2020_10p0]):
    #to access and plot the slice arrays directly
    Q_array = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[0]
    E_array = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[1]
    normalized_intensity = mantid.plots.helperfunctions.get_md_data2d_bin_centers(val,mantid.plots.helperfunctions.get_normalization(val)[0])[2]
    Q_mesh, E_mesh = np.meshgrid(Q_array, E_array)
    plt.plot(E_array, np.sum(normalized_intensity[:,10:40], axis = 1), label = label_13p08meV[idx])
plt.legend()
plt.xlabel('E (meV)')
plt.ylabel('Intensity (arb. units)')
plt.show()