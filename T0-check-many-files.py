import scipy.optimize as opt
import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
import matplotlib.pyplot as plt
from mantid import plots
from matplotlib.colors import LogNorm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def gaussian_s_b(x, mu, sig, scale, background):
    return background+scale*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))



#preprocessing V file name
#also this vanadium file is in the local link that gets created for a specific user
processed_vanadium="/SNS/CNCS/IPTS-16211/shared/do_again_Savici_helping_030118/VAN_CNCS_201975.nxs"
van = Load(processed_vanadium)
"""
data_folder = '/SNS/CNCS/IPTS-20360/nexus/' #this is the real thing living in the permission specific data folder

#
Ei_scaling = 1.0

#define the runs and read in the data
#runs_a = range(287950 ,287951 +1, 1) # 1 meV data
runs_a = [274475] # 6.67307102041 meV
runs_a = [274471] # 36.3311644444 meV
runs_a = [274486] #1.00919901235 meV 



file_names_a = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_a]
"""
def monitor_tzero_calc(filename):
    data_a = Load(Filename=filename)
    Ei_scaling = 1.0
    #
    #load the monitors
    monitor_a = LoadNexusMonitors(filename)

    plt.close('all')
    #LoadInstrument(data_a,FileName='/SNS/CNCS/shared/geometry/CNCS_Definition_2018B2.xml', RewriteSpectraMap=False)
    #LoadInstrument(data_a,FileName='/SNS/users/vdp/CNCS/2018B/CNCS_Definition_Pajerowski.xml', RewriteSpectraMap=False)

    #detector_height = 2.06
    detector_height = data_a.getInstrument().getDetector(0).shape().getBoundingBox().width()[1]*128.

    if 1:
        plt.close('all')

    #
    #Get Ei (initial energy through choppers), T0 (delay time of emission from source), vi (initially velocity from source)
    print("Ei",data_a .getRun()['EnergyRequest'].firstValue(), "meV")

    mode = data_a .run()['DoubleDiskMode'].timeAverageValue()
    print("double-disc-mode",mode)

    Ei, _FMP, _FMI, T0 = GetEi(data_a)
    #Ei = 1.00*Ei_scaling
    print(Ei)
    print("T0",T0, 'microseconds')

    if (mode!=1):T0-=5.91
    print("T0",T0, 'microseconds')

    vi = 437.4*np.sqrt(Ei)
    print("vi", vi, "m/s")


    """
    mon_instr = monitor_CNCS_273899_rebin.getInstrument()

    for i in range(mon_instr.nelements()): print(i, mon_instr[i].getName())
    (0, 'moderator')
    (1, 'sample-position')
    (2, 'monitors')
    (3, 'detectors')

    this is giving the indexation of the instrument

    and then monitor has 3 elements...

    for i in range(mon_instr[2].nelements()): print(i, mon_instr[2][i].getName())
    (0, 'monitor1')
    (1, 'monitor2')
    (2, 'monitor3')
    """


    #
    #Get L1 (distance from source to sample), t1 (time from source to sample)
    instr = data_a.getInstrument()

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

    print("source coordinates",source_position)
    print("monitor3 coordinates", monitor3_position)
    print("sample coordinates",sample_position)
    print("L1", L1, "meters")
    print("source_to_monitor3", source_to_monitor3, "meters")
    print("t1", t1, "microseconds")
    print("t_monitor3", t_monitor3, "microseconds")

    #the purported design L2 is 3.5 m
    L2 = 3.5 #m


    #the expected time to get to monitor3
    t_expected_monitor3 = source_to_monitor3/vi * 1e6
    print("t_expected_monitor3", t_expected_monitor3, "microseconds")

    #the time expected for the elastic line, is the time to travel L1 and L2 with a speed of vi, plus the T0 offset
    #T0 ???????? asdf
    t_expected = (L1+L2)/vi * 1e6 + T0
    print("T0 old", T0)
    print("t_expected", t_expected, "microseconds")

    #find the ROI (region of interest)
    tofbin_min = int(t_expected*.95) 
    tofbin_max = int(t_expected*1.05) 
    print("detector elastic line from times of", tofbin_min, "to",tofbin_max,"in microseconds")

    tofbin_monitor3_min = int(t_expected_monitor3*.95) 
    tofbin_monitor3_max = int(t_expected_monitor3*1.05) 
    print("peak at monitor3 from times of", tofbin_monitor3_min, "to",tofbin_monitor3_max,"in microseconds")

    #
    #Time of flight histogram for the detectors
    tofbin_size = 1. #EACH BIN IS 1 microsecond by definition, this is important because later on there is an indexation of array that uses this, do not change it without care!!!
    data_a_near_elastic = Rebin(InputWorkspace=data_a, OutputWorkspace='data_a_near_elastic', Params="%s,%s,%s" % (tofbin_min, tofbin_size, tofbin_max))


    #time of flight for the monitors
    Rebin(InputWorkspace='monitor_a', OutputWorkspace='monitor_a', Params="%s,%s,%s" % (tofbin_monitor3_min, tofbin_size, tofbin_monitor3_max))
    monitor_a = CropWorkspace(monitor_a, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)

    #
    #fit a gaussian to the monitor3 peak, to get the timing_offset

    #extract the arrays associated with the time-of-flight spectrum for the monitor3
    monitor_a_tof = monitor_a.extractX()[0]
    monitor_a_intensity = monitor_a.extractY()[0]
    monitor_a_tof_centered = monitor_a_tof[:-1]-(monitor_a_tof[0]-monitor_a_tof[1])/2.

    #get the center-of-mass
    center_of_mass = np.dot(monitor_a_tof[:-1], monitor_a_intensity) / np.sum(monitor_a_intensity)
    T0_center_of_mass = center_of_mass - t_expected_monitor3

    average_intensity = np.sqrt(np.dot(monitor_a_tof[:-1], monitor_a_intensity**2) / np.sum(monitor_a_tof[:-1]))



    #get an initial guess for the fit by simply taking the maximum value of the peak
    monitor3_height_guess = np.max(monitor_a_intensity)
    print("monitor3_height_guess", monitor3_height_guess)
    monitor3_peakcenter_guess = monitor_a_tof[np.argmax(monitor_a_intensity)]
    print("monitor3_peakcenter_guess", monitor3_peakcenter_guess)
    monitor3_sigma_guess = 50
    print("monitor3_sigma_guess", monitor3_sigma_guess)


    #fit_result = Fit(Function='name=Gaussian,Height='+str(monitor3_height_guess)+',PeakCentre='+str(monitor3_peakcenter_guess)+',Sigma='+str(monitor3_sigma_guess), InputWorkspace=monitor_a, Output=monitor_a, OutputCompositeMembers=True)

    #def gaussian_s_b    mu, sig, scale, background
    initial_guess = (monitor3_peakcenter_guess, monitor3_sigma_guess, monitor3_height_guess, 1.)
    popt, pcov = opt.curve_fit(gaussian_s_b, monitor_a_tof_centered, monitor_a_intensity, p0=initial_guess)
    popt_names = ['mu', 'sig', 'scale', 'background']
    print("****************")
    print("results of gaussian_s_b fit to elastic line in TOF")
    for idx, i in enumerate(popt):
        print(popt_names[idx], i)
        print(initial_guess[idx])


    data_fitted = gaussian_s_b(monitor_a_tof_centered, *popt)

    print('figure of merit is sum(resids)/sum(data)', np.sum(np.abs(data_fitted - monitor_a_intensity)) /np.sum(np.abs(monitor_a_intensity)))


    monitor_3_fit_height = popt[2]
    monitor_3_fit_center = popt[0]
    monitor_3_fit_sigma = popt[1]

    print("monitor_3_fit_height", monitor_3_fit_height)
    print("monitor_3_fit_center", monitor_3_fit_center)
    print("monitor_3_fit_sigma", monitor_3_fit_sigma)

    timing_offset = monitor_3_fit_center - t_expected_monitor3
    print("timing_offset found by peak arrival time at monitor3", timing_offset)
    print("T0 from emission table", T0, "T0 from monitor3 timing gaussian fit", timing_offset, "T0 from monitor3 timing c-o-m", T0_center_of_mass)
    t_expected = (L1+L2)/vi * 1e6 + T0
    print((L1+L2)/vi * 1e6+ T0)


    #
    """
    #plot the detector time of flight in the region of interest
    print('plotting')
    detector_spectrum=SumSpectra(InputWorkspace=data_a_near_elastic)

    fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
    ax.plot(detector_spectrum)
    ax.legend()
    fig.show()
    """


    print(T0, timing_offset, T0_center_of_mass)
    return Ei, timing_offset, T0_center_of_mass


data_folder = '/SNS/CNCS/IPTS-20360/nexus/'
#condition 1
runs_1 = range(274470,274470+20, 1)

#condition 3
runs_3 = range(274470+20,274470+20+20, 1)

#condition 0
runs_0 = range(274470+20+20,274470+20+20+20, 1)

Ei_1_list = []
T0_1_mon_gauss_list = []
T0_1_mon_com_list = []
for this_run in runs_1:
    this_Ei, this_timing_offset, this_T0_center_of_mass = monitor_tzero_calc(data_folder+'CNCS_{0}.nxs.h5'.format(this_run))
    Ei_1_list.append(this_Ei)
    T0_1_mon_gauss_list.append(this_timing_offset)
    T0_1_mon_com_list.append(this_T0_center_of_mass)
    print('HF', this_Ei, this_timing_offset, this_T0_center_of_mass)

Ei_3_list = []
T0_3_mon_gauss_list = []
T0_3_mon_com_list = []
for this_run in runs_3:
    this_Ei, this_timing_offset, this_T0_center_of_mass = monitor_tzero_calc(data_folder+'CNCS_{0}.nxs.h5'.format(this_run))
    Ei_3_list.append(this_Ei)
    T0_3_mon_gauss_list.append(this_timing_offset)
    T0_3_mon_com_list.append(this_T0_center_of_mass)
    print('AI', this_Ei, this_timing_offset, this_T0_center_of_mass)

Ei_0_list = []
T0_0_mon_gauss_list = []
T0_0_mon_com_list = []
for this_run in runs_0:
    this_Ei, this_timing_offset, this_T0_center_of_mass = monitor_tzero_calc(data_folder+'CNCS_{0}.nxs.h5'.format(this_run))
    Ei_0_list.append(this_Ei)
    T0_0_mon_gauss_list.append(this_timing_offset)
    T0_0_mon_com_list.append(this_T0_center_of_mass)
    print('HR', this_Ei, this_timing_offset, this_T0_center_of_mass)

np.savetxt('T0_Ei_1_list_mon.npy', Ei_1_list)
np.savetxt('T0_1_mon_gauss_list.npy', T0_1_mon_gauss_list)
np.savetxt('T0_1_mon_com_list.npy', T0_1_mon_com_list)

np.savetxt('T0_Ei_3_list_mon.npy', Ei_3_list)
np.savetxt('T0_3_mon_gauss_list.npy', T0_3_mon_gauss_list)
np.savetxt('T0_3_mon_com_list.npy', T0_3_mon_com_list)

np.savetxt('T0_Ei_0_list_mon.npy', Ei_0_list)
np.savetxt('T0_0_mon_gauss_list.npy', T0_0_mon_gauss_list)
np.savetxt('T0_0_mon_com_list.npy', T0_0_mon_com_list)

plt.figure()
plt.plot(Ei_1_list, T0_1_mon_gauss_list)
plt.plot(Ei_1_list, T0_1_mon_com_list, 'o', label = 'HF, dd=300Hz')
plt.plot(Ei_3_list, T0_3_mon_com_list, 's', label = 'AI, dd=240Hz')
plt.plot(Ei_0_list, T0_0_mon_com_list, '^', label = 'HR, dd=180Hz')
plt.legend()
plt.show()