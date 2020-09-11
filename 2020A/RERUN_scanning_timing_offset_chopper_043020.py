import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
import matplotlib.pyplot as plt
from mantid import plots
from matplotlib.colors import LogNorm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit


def tzero_function(x, x0, x1, x2, x3):
    return x0-x1*np.log(ei_list)-x2*np.log(ei_list)*np.log(ei_list)-x3*np.log(ei_list)*np.log(ei_list)*np.log(ei_list)

def gaussian(x, mu, sig, scale):
    return scale*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    
def linear_func(x, x0, x1):
    return np.add(x0,np.multiply(x1,x))

data_folder = '/SNS/CNCS/IPTS-25820/nexus/' #this is the real thing living in the permission specific data folder

#define the runs and read in the data
runs = range(335760, 336075+1)
runs = range(335784, 336115+1)

chp2_delay_list = []
exp_log = np.genfromtxt('/SNS/CNCS/IPTS-25820/shared/autoreduce/experiment_log.csv', skip_header = 1, delimiter = ',', dtype = 'string_')
for idx, val in enumerate(exp_log):
    if int(val[0]) in runs:
        print(val[0], int(val[1].split('=')[1]))
        this_chp2_delay = int(val[1].split('=')[1])
        chp2_delay_list.append(this_chp2_delay)

file_names = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs]


monitor_intensity_list = []
for this_run in file_names:
    print(this_run)
    monitor = LoadNexusMonitors(this_run)
    
    #LoadInstrument(monitor,FileName='/SNS/CNCS/shared/BL5-scripts/2019B/CNCS_Definition-addBM4-pre2019B.xml', RewriteSpectraMap=False)
    
    Ei, _FMP, _FMI, T0 = GetEi(monitor)
    
    vi = 437.4*np.sqrt(Ei)
    print("vi", vi, "m/s")
    
    #monitor_intensity = monitor.extractY()[0]
    
    #monitor = CropWorkspace(monitor, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)
    
    
    #monitor_intensity_list.append(monitor_intensity[0])
    
    instr = monitor.getInstrument()

    monitor1_position = instr[2][0].getPos() #now defunct monitor that is directly in front of chopper 1, the fermi chopper, should be ~6.313 m from the source
    monitor2_position = instr[2][1].getPos() #monitor that is directly after chopper 2, the first bandwidth chopper, should be ~7.556 m from the source
    monitor3_position = instr[2][2].getPos() #monitor that is directly after choppers 4+5, the double disc choppers, should be ~34.836 m from the source
    #monitor3 is the one that is most useful in this case

    source_position = instr.getSource().getPos()
    sample_position = instr.getSample().getPos()
    L1 = np.linalg.norm(sample_position-source_position)
    source_to_monitor3 = np.linalg.norm(monitor3_position-source_position)
    t1 = L1/vi*1e6 #in microseconds
    t_monitor3 = source_to_monitor3/vi*1e6
    #monitormev_log = LoadNexusLogs(
    Phase1 = monitor.getRun()['Phase1'].getStatistics().median

    #the expected time to get to monitor3
    t_expected_monitor3 = source_to_monitor3/vi * 1e6
    print("t_expected_monitor3", t_expected_monitor3, "microseconds")

    tofbin_monitor3_min = int(t_expected_monitor3*.95) 
    tofbin_monitor3_max = int(t_expected_monitor3*1.05) 
    print("peak at monitor3 from times of", tofbin_monitor3_min, "to",tofbin_monitor3_max,"in microseconds")

    #time of flight for the monitors
    tofbin_size = 1.
    Rebin(InputWorkspace='monitor', OutputWorkspace='monitor', Params="%s,%s,%s" % (tofbin_monitor3_min, tofbin_size, tofbin_monitor3_max))
    monitor = CropWorkspace(monitor, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)

    #extract the arrays associated with the time-of-flight spectrum for the monitor3
    monitor_tof = monitor.extractX()[0]
    monitor_intensity = monitor.extractY()[0]
    
    monitor_intensity_list.append(np.sum(monitor_intensity))

plt.figure()
#plt.plot(runs, monitor_intensity_list)
plt.plot(chp2_delay_list, monitor_intensity_list)
plt.show()

sys.exit()