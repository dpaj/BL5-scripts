import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
import matplotlib.pyplot as plt
from mantid import plots
from matplotlib.colors import LogNorm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from matplotlib.ticker import FormatStrFormatter, FuncFormatter, ScalarFormatter


def gaussian(x, mu, sig, scale):
    return scale*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def flux_res_save(filename, Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list):
    np.save(filename+'Ei_list.npy', Ei_list)
    np.save(filename+'monitor_intensity_list.npy', monitor_intensity_list)
    np.save(filename+'vi_list.npy', vi_list)
    np.save(filename+'detector_intensity_list.npy', detector_intensity_list)
    np.save(filename+'detector_FWHM_list.npy', detector_FWHM_list)
    np.save(filename+'DD_opening_list.npy', DD_opening_list)
    np.save(filename+'DD_speed_list.npy', DD_speed_list)

def flux_res_calc(runs_list):
    
    van = Load(Filename='/SNS/CNCS/IPTS-21088/shared/autoreduce/van_273992.nxs', OutputWorkspace='van') #the vanadium normalization file
    
    file_names = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_list]
    
    Ei_list = []
    monitor_intensity_list = []
    vi_list = []
    detector_intensity_list = []
    detector_FWHM_list = []
    DD_opening_list = []
    DD_speed_list = []
    
    file_names = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_list]
    
    for thisfile in file_names:
        print(thisfile)
        raw = LoadEventNexus(Filename = thisfile)
        run = raw.getRun()
        monitor = LoadNexusMonitors(thisfile)
        instr = raw.getInstrument()
        Ei, _FMP, _FMI, T0 = GetEi(raw)
        vi = 437.4*np.sqrt(Ei)
        
        monitor3_position = instr[2][2].getPos() #monitor that is directly after choppers 4+5, the double disc choppers, should be ~34.836 m from the source
        source_position = instr.getSource().getPos() #position of the moderator source
        source_to_monitor3 = np.linalg.norm(monitor3_position-source_position) #distance between the source and the monitor3
        t_expected_monitor3 = source_to_monitor3/vi * 1e6 + T0 #expected arrival time at monitor3
        
        tofbin_monitor3_min = int(t_expected_monitor3*.95) #the minimum TOF value to use for summing up the monitor counts
        tofbin_monitor3_max = int(t_expected_monitor3*1.05) #the maximum TOF value to use for summing up the monitor counts
        tofbin_size = 1. #binning for the monitor, units of microseconds
        Rebin(InputWorkspace='monitor', OutputWorkspace='monitor', Params="%s,%s,%s" % (tofbin_monitor3_min, tofbin_size, tofbin_monitor3_max)) #default is one bin, rebin to tofbin_size
        monitor = CropWorkspace(monitor, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)
        
        monitor_tof = monitor.extractX()[0] #extract the monitor3 TOF array
        monitor_intensity = monitor.extractY()[0] #extract the monitor3 intensity array
        
        monitor_pulse_flux = np.sum(monitor_intensity) * 1e-6 * tofbin_size #the flux in counts/second at monitor3 for a given pulse, rectangular integration with the fixed time-width (tofbin_size) outside of the summation      
        monitor_intensity = monitor_pulse_flux / 8.8e-6 * vi/2197.763809 * 60. # the counts per pulse, divided by the efficiency at 1.8 angstroms (~25 meV), times the velocity correction, times 60 pulses per second

        dgs,_ = DgsReduction(
            SampleInputWorkspace = raw,
            SampleInputMonitorWorkspace = raw,
            EnergyTransferRange = [-0.15*Ei, Ei/200., 0.25*Ei],
            SofPhiEIsDistribution = True, #this will keep the output data as a histogram
            CorrectKiKf = True,
            DetectorVanadiumInputWorkspace = van,
            UseProcessedDetVan = True,
            IncidentBeamNormalisation='ByCurrent',
            ) #convert to E and angle distribution
        md = ConvertToMD(dgs, QDimensions = '|Q|', dEAnalysisMode = 'Direct') # change units from angle and E to |Q| and E
        line = BinMD(
            InputWorkspace = md, 
            AxisAligned = True, 
            AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 1',
            AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.1*Ei)+', 30', 
            ) #sum over Q, get I vs E
        E, I, dI = mantid.plots.helperfunctions.get_md_data1d(line,mantid.plots.helperfunctions.get_normalization(line)[0]) #extract the energy, intensity, and error arrays

        #fit a gaussian to the elastic line at the detector
        #[x, mu, sig, scale] are the arguments of the gaussian function defined above
        popt, pcov = curve_fit(gaussian, E, I, p0 = (0.01, 0.025*Ei, np.max(I)) )
        detector_intensity = popt[2] #arbitrary units
        detector_FWHM = popt[1]*2.355 #units of meV

        #append the results for this run to the various lists
        Ei_list.append(Ei)
        monitor_intensity_list.append(monitor_intensity)
        vi_list.append(vi)
        detector_intensity_list.append(detector_intensity)
        detector_FWHM_list.append(detector_FWHM)
        DD_opening_list.append(run['DoubleDiskMode'].value[0])
        DD_speed_list.append(run['SpeedRequest4'].value[0])
    return Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list

data_folder = '/SNS/CNCS/IPTS-20360/nexus/'
results_folder = '/SNS/CNCS/shared/BL5-scripts/flux-resolution/'

#runs = range(274470,274529+1, 1) #all the runs
runs_1 = range(274470,274470+20, 1) #condition 1, HF
runs_3 = range(274470+20,274470+20+20, 1) #condition 3, AI
runs_0 = range(274470+20+20,274470+20+20+20, 1) #condition 0, HR

Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list = flux_res_calc(runs_1)
flux_res_save(results_folder+'2018B-HF-', Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list)

Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list = flux_res_calc(runs_3)
flux_res_save(results_folder+'2018B-AI-', Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list)

Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list = flux_res_calc(runs_0)
flux_res_save(results_folder+'2018B-HR-', Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list)