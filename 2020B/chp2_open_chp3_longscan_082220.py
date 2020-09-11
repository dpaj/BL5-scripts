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
        E, I, dI = mantid.plots.datafunctions.get_md_data1d(line,mantid.plots.datafunctions.get_normalization(line)[0]) #extract the energy, intensity, and error arrays

        #fit a gaussian to the elastic line at the detector
        #[x, mu, sig, scale] are the arguments of the gaussian function defined above
        try:
            popt, pcov = curve_fit(gaussian, E, I, p0 = (0.01, 0.025*Ei, np.max(I)) )
            detector_intensity = popt[2] #arbitrary units
            detector_FWHM = popt[1]*2.355 #units of meV
        except:
            detector_intensity = -1
            detector_FWHM = -1

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

data_folder = '/SNS/CNCS/IPTS-25821/nexus/'
results_folder = '/SNS/CNCS/shared/BL5-scripts/2020B/'

runs = range(346779, 346857+1)

initial_phase_delay = 3820.74 #microseconds # want to get this from BL5:Chop:Skf3:PhaseTimeDelaySet, as it is energy dependent etc.
initial_phase_delay_integer = int(initial_phase_delay)

scan_range = 1000
#scan_range = 120
scan_step = 20
#scan_step = 5

chp3_delay_list = range(initial_phase_delay_integer-scan_range, initial_phase_delay_integer+scan_range, scan_step)

"""
exp_log = np.genfromtxt('/SNS/CNCS/IPTS-25821/shared/autoreduce/experiment_log.csv', skip_header = 1, delimiter = ',', dtype = 'string_')
for idx, val in enumerate(exp_log):
    if int(val[0]) in runs:
        print(val[0], int(val[1].split('=')[1]))
        this_chp3_delay = int(val[1].split('=')[1])
        chp3_delay_list.append(this_chp3_delay)
"""
Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list = flux_res_calc(runs)
flux_res_save(results_folder+'2020A-chp3-test-FINE-', Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list)

np.save(results_folder+'2020A-chp3-test-FINE-chp3_delay_list.npy', chp3_delay_list)

#plt.figure()
#plt.title('detector elastic intensity')
#plt.plot(chp3_delay_list, detector_intensity_list)
#plt.show()


plt.figure()
plt.title('IPTS-25820, detector elastic FWHM, runs = ({0}, {1})'.format(np.min(runs), np.max(runs)))
plt.plot(chp3_delay_list, detector_FWHM_list, '.-',label = 'fit FWHM')
plt.ylim([0,1.])
plt.hlines(0.72, np.min(chp3_delay_list), np.max(chp3_delay_list) , colors = 'red', label = '2019 fit FWHM')
plt.vlines(3820.71, -1,1, colors = 'green', label = '2019 chp3 delay')
plt.xlabel('chop3 delay (microseconds)')
plt.ylabel('FWHM (meV)')
plt.legend()
plt.show()

#plt.figure()
#plt.title('bm3 intensity')
#plt.plot(chp3_delay_list, monitor_normalized_intensity_list)
#plt.show()


plt.figure()
plt.title('IPTS-25820, Ei = 12 meV, runs = ({0}, {1})'.format(np.min(runs), np.max(runs)))
plt.plot(chp3_delay_list, monitor_normalized_intensity_list/ np.max(monitor_normalized_intensity_list), label = 'normalized bm3')
plt.plot(chp3_delay_list, detector_intensity_list/ np.max(detector_intensity_list), label = 'normalized detector')
plt.vlines(3820.74, -1,1, colors = 'red', label = '2019 chp3 delay')
chp3_period = 1.e6/60./60.
for i in range(-5,20):
    plt.vlines(3820.74 + i*chp3_period, -1,1, colors = 'red', linestyles = 'dashed')
plt.ylabel('intensity (arb. units)')
plt.xlabel('chop3 delay (microseconds)')
plt.ylim([0,1.])
plt.legend()
plt.show()

