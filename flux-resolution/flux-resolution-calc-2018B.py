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

def flux_res_save(filename, Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list):
    """
    save numpy arrays for the specified values
    """
    np.save(filename+'Ei_list.npy', Ei_list)
    np.save(filename+'monitor_normalized_intensity_list.npy', monitor_normalized_intensity_list)
    np.save(filename+'monitor_normalized_intensity_perMW_list.npy', monitor_normalized_intensity_perMW_list)
    np.save(filename+'vi_list.npy', vi_list)
    np.save(filename+'detector_intensity_list.npy', detector_intensity_list)
    np.save(filename+'detector_FWHM_list.npy', detector_FWHM_list)
    np.save(filename+'DD_opening_list.npy', DD_opening_list)
    np.save(filename+'DD_speed_list.npy', DD_speed_list)

def flux_res_calc(runs_list):
    """
    for the runs passed, calculate the flux and resolution and output the resulting lists
    """
    
    van = Load(Filename='/SNS/CNCS/IPTS-21088/shared/autoreduce/van_273992.nxs', OutputWorkspace='van') #the vanadium normalization file
    
    file_names = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_list]
    
    Ei_list = []
    monitor_normalized_intensity_list = []
    monitor_normalized_intensity_perMW_list = []
    vi_list = []
    detector_intensity_list = []
    detector_FWHM_list = []
    DD_opening_list = []
    DD_speed_list = []
    
    file_names = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_list]
    
    for thisfile in file_names:
        print(thisfile)
        raw = LoadEventNexus(Filename = thisfile) #the raw data file
        run = raw.getRun() #run information
        monitor = LoadNexusMonitors(thisfile) #the monitor data
        instr = raw.getInstrument() #the instrument geometry object
        Ei, _FMP, _FMI, T0 = GetEi(raw) #get Ei in meV
        vi = 437.4*np.sqrt(Ei) #calculate the velocity in m/s
        
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
        
        pc = run['proton_charge'].value #array of proton charge for every pulse
        nonzero_pc = pc[np.nonzero(run['proton_charge'].value)] #the nonzero pulses in the array
        number_of_pulses = np.shape(nonzero_pc)[0] #the total number of nonzero pulses
        pulse_spacing = 1/60. # seconds, the pulse spacing
        total_uptime = number_of_pulses * pulse_spacing #the total amount of time when neutrons are being delivered to the sample
        average_power_during_uptime = np.mean(nonzero_pc) * 60. * 1e-9 #MegaWatts
        
        monitor_pulse_total_counts = np.sum(monitor_intensity)#counts, all of the counts in the monitor during the integration range
        monitor3_efficiency_at_1p8_angs = 8.8e-6 #counts/neutron, this value was measured in 2007 by the detector group by using a calibrated standard monitor at the HFIR
        v_1p8_angs = 2197.763809 #m/s
        monitor_normalized_intensity = monitor_pulse_total_counts / monitor3_efficiency_at_1p8_angs * vi/v_1p8_angs / total_uptime # neutrons/s, the counts per pulse, divided by the efficiency at 1.8 angstroms (~25 meV), times the velocity correction, divided by total_uptime
        monitor_normalized_intensity_perMW = monitor_normalized_intensity / average_power_during_uptime #neutrons/s/MW

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
        monitor_normalized_intensity_list.append(monitor_normalized_intensity)
        monitor_normalized_intensity_perMW_list.append(monitor_normalized_intensity_perMW)
        vi_list.append(vi)
        detector_intensity_list.append(detector_intensity)
        detector_FWHM_list.append(detector_FWHM)
        DD_opening_list.append(run['DoubleDiskMode'].value[0])
        DD_speed_list.append(run['SpeedRequest4'].value[0])
    return Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list

data_folder = '/SNS/CNCS/IPTS-20360/nexus/'
results_folder = '/SNS/CNCS/shared/BL5-scripts/flux-resolution/'

#runs = range(274470,274529+1, 1) #all the runs
runs_1 = range(274470,274470+20, 1) #condition 1, HF
[ 81.74512, 36.33116444, 20.43628, 13.0792192, 9.08279111, 6.67307102, 5.10907, 4.03679605, 3.2698048, 2.70231802, 2.27069778, 1.93479574, 1.66826776, 1.45324658, 1.2772675, 1.13142035, 1.00919901, 0.9057631, 0.8174512, 0.74145234]
#first run energies [ 81.745, 36.331, 20.436, 13.079, 9.082, 6.673, 5.109, 4.036, 3.269, 2.702, 2.270, 1.934, 1.668, 1.453, 1.277, 1.131, 1.009, 0.905, 0.817, 0.741]
#additional run energies 11, 10, 7.9, 6.0, 4.5, 0.54
#[277528, 277525, 277514, 277513, 277512, 277511]
#put together by hand [ 81.745, 36.331, 20.436, 13.079, ***11, ***10, 9.082, ***7.9, 6.673, ***6, 5.109, ***4.5, 4.036, 3.269, 2.702, 2.270, 1.934, 1.668, 1.453, 1.277, 1.131, 1.009, 0.905, 0.817, 0.741, ***0.54]
runs_1 = [274470, 274471, 274472, 274473, 277528, 277525, 274474, 277514, 274475, 277513, 274476, 277512, 274477, 274478, 274479, 274480, 274481, 274482, 274483, 274484, 274485, 274486, 274487, 274488, 274489, 277511]

runs_3 = range(274470+20,274470+20+20, 1) #condition 3, AI
#[277529, 277526, 277519, 277518, 277517, 277516]
#put together by hand [ 81.745, 36.331, 20.436, 13.079, ***11, ***10, 9.082, ***7.9, 6.673, ***6, 5.109, ***4.5, 4.036, 3.269, 2.702, 2.270, 1.934, 1.668, 1.453, 1.277, 1.131, 1.009, 0.905, 0.817, 0.741, ***0.54]
runs_3 = [274490, 274491, 274492, 274493, 277529, 277526, 274494, 277519, 274495, 277518, 274496, 277517, 274497, 274498, 274499, 274500, 274501, 274502, 274503, 274504, 274505, 274506, 274507, 274508, 274509, 277516]

runs_0 = range(274470+20+20,274470+20+20+20, 1) #condition 0, HR
#[277530, 277527, 277524, 277523, 277522, 277521]
#put together by hand [ 81.745, 36.331, 20.436, 13.079, ***11, ***10, 9.082, ***7.9, 6.673, ***6, 5.109, ***4.5, 4.036, 3.269, 2.702, 2.270, 1.934, 1.668, 1.453, 1.277, 1.131, 1.009, 0.905, 0.817, 0.741, ***0.54]
runs_0 = [274510, 274511, 274512, 274513, 277530, 277527, 274514, 277524, 274515, 277523, 274516, 277522, 274517, 274518, 274519, 274520, 274521, 274522, 274523, 274524, 274525, 274526, 274527, 274528, 274529, 277521]

Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list = flux_res_calc(runs_1)
flux_res_save(results_folder+'2018B-HF-', Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list)

Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list = flux_res_calc(runs_3)
flux_res_save(results_folder+'2018B-AI-', Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list)

Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list = flux_res_calc(runs_0)
flux_res_save(results_folder+'2018B-HR-', Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list)