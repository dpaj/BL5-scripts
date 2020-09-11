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
    DD_opening_list = []
    DD_speed_list = []
    average_power_during_uptime_list = []
    pc_list = []
    duration_list = []
    monitor_raw_intensity_list = []
    
    file_names = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_list]
    
    for thisfile in file_names:
        print(thisfile)

        #run = raw.getRun() #run information
        monitor = LoadNexusMonitors(thisfile) #the monitor data
        run = monitor.getRun() 
        instr = monitor.getInstrument() #the instrument geometry object
        
        duration = run['duration'].value
        
        Ei, _FMP, _FMI, T0 = GetEi(monitor) #get Ei in meV
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
        average_power_during_uptime_list.append(average_power_during_uptime)
        pc_list.append(np.sum(pc))
        
        monitor_pulse_total_counts = np.sum(monitor_intensity)#counts, all of the counts in the monitor during the integration range
        monitor3_efficiency_at_1p8_angs = 8.8e-6 #counts/neutron, this value was measured in 2007 by the detector group by using a calibrated standard monitor at the HFIR
        v_1p8_angs = 2197.763809 #m/s
        monitor_normalized_intensity = monitor_pulse_total_counts / monitor3_efficiency_at_1p8_angs * vi/v_1p8_angs / total_uptime # neutrons/s, the counts per pulse, divided by the efficiency at 1.8 angstroms (~25 meV), times the velocity correction, divided by total_uptime
        monitor_normalized_intensity_perMW = monitor_normalized_intensity / average_power_during_uptime #neutrons/s/MW

        monitor_raw_intensity = monitor_pulse_total_counts



        #append the results for this run to the various lists
        Ei_list.append(Ei)
        monitor_normalized_intensity_list.append(monitor_normalized_intensity)
        monitor_normalized_intensity_perMW_list.append(monitor_normalized_intensity_perMW)
        vi_list.append(vi)
        duration_list.append(duration)
        DD_opening_list.append(run['DoubleDiskMode'].value[0])
        DD_speed_list.append(run['SpeedRequest4'].value[0])
        monitor_raw_intensity_list.append(monitor_raw_intensity)
    return Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, DD_opening_list, DD_speed_list, pc_list, average_power_during_uptime_list, duration_list, monitor_raw_intensity_list

data_folder = '/SNS/CNCS/IPTS-23272/nexus/'
results_folder = '/SNS/CNCS/IPTS-23272/shared/testing_source_power/'

runs_1 = range(309853, 310000, 1) #condition 1, HF

Ei_list, monitor_normalized_intensity_list, monitor_normalized_intensity_perMW_list, vi_list, DD_opening_list, DD_speed_list, pc_list, average_power_during_uptime_list, duration_list, monitor_raw_intensity_list = flux_res_calc(runs_1)

plt.figure()
#plt.plot(monitor_normalized_intensity_list)
plt.plot(monitor_normalized_intensity_perMW_list/np.max(monitor_normalized_intensity_perMW_list), label = 'I per MW up to scale factor')
#plt.plot(np.divide(monitor_raw_intensity_list, duration_list)/np.max(np.divide(monitor_raw_intensity_list, duration_list)), label = 'I per duration')
plt.plot(np.divide(monitor_raw_intensity_list, pc_list)/np.max(np.divide(monitor_raw_intensity_list, pc_list)), label = 'I per pc up to scale factor')
plt.ylabel('arb. u.')
plt.xlabel('relative run index; proportional to wall clock run starting time')
plt.title('monitor after chopper system before sample\nEi = 2.5meV')
plt.legend(loc = 'best')
plt.show()

plt.figure()
plt.plot(np.divide(average_power_during_uptime_list, np.max(average_power_during_uptime_list)), label = 'average power up to scale factor')
plt.plot(np.divide(duration_list, np.max(duration_list)), label = 'run duration up to scale factor')
plt.ylabel('arb. u.')
plt.xlabel('relative run index; proportional to wall clock run starting time')
#plt.title('monitor after chopper system before sample\nEi = 2.5meV')
plt.legend(loc = 'best')
plt.show()

plt.figure()
power_time_runtime = np.divide(average_power_during_uptime_list, np.max(average_power_during_uptime_list)) * np.divide(duration_list, np.max(duration_list))
plt.plot(power_time_runtime/power_time_runtime[0], label = 'power times runtime up to scale factor')
#plt.plot(, label = 'run duration up to scale factor')
plt.ylabel('arb. u.')
plt.xlabel('relative run index; proportional to wall clock run starting time')
#plt.title('monitor after chopper system before sample\nEi = 2.5meV')
plt.legend(loc = 'best')
plt.show()

#plt.close('all')

"""
plt.figure()
#plt.plot(monitor_normalized_intensity_list)
plt.plot(np.divide(monitor_raw_intensity_list, duration_list)/np.max(np.divide(monitor_raw_intensity_list, duration_list)))
plt.show()
"""