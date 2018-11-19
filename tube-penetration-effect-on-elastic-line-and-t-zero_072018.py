from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
from mantid import plots
from matplotlib.colors import LogNorm
import scipy.optimize as opt


def gaussian(x, mu, sig, scale, background):
    return background+scale*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

van=LoadNexus(Filename='/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/van_277537.nxs')
MaskBTP(Workspace = 'van', Instrument = 'CNCS', Bank = '5-10')

def fittingTzero(filename):
    raw = Load(Filename=filename, OutputWorkspace='raw')
    MaskBTP(Workspace = 'raw', Instrument = 'CNCS', Pixel = '1-63,65-128')
    instr = raw.getInstrument()
    source = instr.getSource()
    sample = instr.getSample()
    source_to_sample_distance_m = sample.getDistance(source)
    source_position = instr.getSource().getPos()
    sample_position = instr.getSample().getPos()
    L1 = np.linalg.norm(sample_position-source_position)
    Ei, _FMP, _FMI, T0 = GetEi(raw)
    vi = 437.4*np.sqrt(Ei)

    two_theta_list = []
    L2_list = []
    bank_indices = range(1,51)
    for idx, chosen_bank in enumerate(bank_indices):
        xs, ys, zs = instr.getComponentByName("bank"+str(chosen_bank))[0].getPos()
        this_two_theta = 180./np.pi * np.arctan2(xs,zs)
        this_two_theta_rad = np.arctan2(xs,zs)
        two_theta_list.append(this_two_theta)
        this_L2 = np.linalg.norm((xs,ys,zs))
        L2_list.append(this_L2)

    L2_ave = np.mean(L2_list)
    L1_plus_L2 = L1 + L2_ave
    D = L1_plus_L2
    D_offset = 2e-2 #2 cm
    D = D - D_offset
    t_elastic_no_offset = D/vi*1e6


    TOF=Rebin(InputWorkspace=raw,Params='10')
    s=SumSpectra(InputWorkspace=TOF)


    TOF = s.readX(0)
    TOF = TOF[:-1] + (TOF[1]-TOF[0])
    I = s.readY(0)

    initial_guess = (t_elastic_no_offset+T0, 5e-4*(t_elastic_no_offset+T0), np.max(I), 0 )
    popt, pcov = opt.curve_fit(gaussian, TOF, I, p0=initial_guess)
    popt_names = ['mu', 'sig', 'scale', 'background']
    print("****************")
    print("results of gaussian fit to elastic line in TOF")
    for idx, i in enumerate(popt):
        print(popt_names[idx], i)

    data_fitted = gaussian(TOF, *popt)

    elastic_position_fitted = popt[0]
    T0_fitted = elastic_position_fitted - t_elastic_no_offset

    fig, ax = plt.subplots()
    ax.plot(TOF, I, 'o', fillstyle='none', label = 'data')
    ax.plot(TOF, data_fitted, 'm-', label = 'gaussian fit')
    ax.axvline(x=t_elastic_no_offset+T0, color = 'red', label = 'chopper T0='+str(T0))
    ax.axvline(x=t_elastic_no_offset, color = 'green', label = 'T0 = 0')
    ax.axvline(x=elastic_position_fitted, color = 'black', label = 'fitted T0='+str(T0_fitted))
    ax.set_xlim(t_elastic_no_offset*0.99, t_elastic_no_offset*1.01)
    ax.set_title(filename)
    ax.set_xlabel('TOF ($\mu$s)')
    ax.set_ylabel('Intensity')
    ax.legend()
    plt.show()

    print("Ei", Ei, "T0",T0, "T0_fitted", T0_fitted)

    dgs,_=DgsReduction(SampleInputWorkspace=raw, 
                                    SampleInputMonitorWorkspace=raw, 
                                    DetectorVanadiumInputWorkspace=van,
                                    UseProcessedDetVan = '1',
                                    IncidentEnergyGuess=Ei, 
                                    UseIncidentEnergyGuess='1', 
                                    TimeZeroGuess=T0_fitted,
                                    IncidentBeamNormalisation='ByCurrent', 
                                    TimeIndepBackgroundSub=False, 
                                    SofPhiEIsDistribution=True) #this means should use normalization # of events

    md = ConvertToMD(InputWorkspace='dgs', QDimensions='|Q|', OutputWorkspace='md')
    Qmax = 1.1*2*np.pi/ (   (  9/np.sqrt(Ei)  ) /2./np.sin(120./2.*np.pi/180.)   ) 
    md_rebin = BinMD(
                InputWorkspace='md', 
                AlignedDim0='|Q|,0,'+str(Qmax)+',1', 
                AlignedDim1='DeltaE,-'+str(0.1*Ei)+','+str(0.1*Ei)+',20', 
                OutputWorkspace='md_rebin')

    dgs_T0,_=DgsReduction(SampleInputWorkspace=raw, 
                                    SampleInputMonitorWorkspace=raw, 
                                    DetectorVanadiumInputWorkspace=van,
                                    UseProcessedDetVan = '1',
                                    IncidentEnergyGuess=Ei, 
                                    UseIncidentEnergyGuess='1', 
                                    TimeZeroGuess=T0,
                                    IncidentBeamNormalisation='ByCurrent', 
                                    TimeIndepBackgroundSub=False, 
                                    SofPhiEIsDistribution=True) #this means should use normalization # of events

    md_T0 = ConvertToMD(InputWorkspace='dgs_T0', QDimensions='|Q|', OutputWorkspace='md_T0')
    Qmax = 1.1*2*np.pi/ (   (  9/np.sqrt(Ei)  ) /2./np.sin(120./2.*np.pi/180.)   ) 
    md_rebin_T0 = BinMD(
                InputWorkspace='md_T0', 
                AlignedDim0='|Q|,0,'+str(Qmax)+',1', 
                AlignedDim1='DeltaE,-'+str(0.1*Ei)+','+str(0.1*Ei)+',20', 
                OutputWorkspace='md_rebin_T0')


    fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
    ax.errorbar(md_rebin_T0,'bo-', label='chopper T0='+str(T0))
    ax.errorbar(md_rebin,'rx-', label='fitted T0='+str(T0_fitted))


    ax.legend()
    ax.set_title(filename)
    ax.tick_params(axis='x', direction='in')
    ax.tick_params(axis='y', direction='out')
    ax.grid(True)

    fig.show()

fittingTzero('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277504.nxs.h5')
fittingTzero('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277505.nxs.h5')
fittingTzero('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277506.nxs.h5')
fittingTzero('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277507.nxs.h5')
fittingTzero('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277508.nxs.h5')
#plt.close('all')


#fittingTzero('/SNS/CNCS/IPTS-21344/nexus/CNCS_277554.nxs.h5')
#fittingTzero('/SNS/CNCS/IPTS-20550/nexus/CNCS_280317.nxs.h5')
#fittingTzero('/SNS/CNCS/IPTS-20550/nexus/CNCS_280523.nxs.h5')
"""
fittingTzero('/SNS/CNCS/IPTS-20550/nexus/CNCS_280729.nxs.h5')
fittingTzero('/SNS/CNCS/IPTS-20550/nexus/CNCS_280874.nxs.h5')
fittingTzero('/SNS/CNCS/IPTS-20550/nexus/CNCS_281142.nxs.h5')
fittingTzero('/SNS/CNCS/IPTS-20550/nexus/CNCS_281345.nxs.h5')
"""