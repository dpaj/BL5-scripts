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

data_folder = '/SNS/CNCS/IPTS-22728/nexus/' #this is the real thing living in the permission specific data folder

#define the runs and read in the data

"""
FIRST SET OF RUNS: (HF)
t-zero scan 1.00 meV = runs from 273278 to 273302, range(273278,273302+1, 1)
t-zero scan 1.55 meV = runs from 273303 to 273327, range(273303,273327+1, 1)
t-zero scan 3.32 meV = runs from 273328 to 273352, range(273328,273352+1, 1)
t-zero scan 6.59 meV = runs from 273353 to 273377, range(273353,273377+1, 1)
t-zero scan 12.0 meV = runs from 273378 to 273402, range(273378,273402+1, 1)
t-zero scan 25.0 meV = runs from 273403 to 273427, range(273403,273427+1, 1)
t-zero scan 80.0 meV = runs from 273428 to 273452, range(273428,273452+1, 1)

SECOND SET OF RUNS: (AI)
t-zero scan 1.00 meV = range(273453,273477+1, 1)
t-zero scan 1.55 meV = range(273478,273502+1, 1)
t-zero scan 3.32 meV = range(273503,273527+1, 1)
t-zero scan 6.59 meV = range(273528,273552+1, 1)
t-zero scan 12.0 meV = range(273553,273577+1, 1)
t-zero scan 25.0 meV = range(273578,273602+1, 1)
t-zero scan 80.0 meV = range(273603,273627+1, 1)

THIRD SET OF RUNS: (HR)
t-zero scan 1.00 meV = range(273628,273652+1, 1)
t-zero scan 1.55 meV = range(273653,273677+1, 1)
t-zero scan 3.32 meV = range(273678,273702+1, 1)
t-zero scan 6.59 meV = range(273703,273727+1, 1)
t-zero scan 12.0 meV = range(273728,273752+1, 1)
t-zero scan 25.0 meV = range(273753,273777+1, 1)
t-zero scan 80.0 meV = range(273778,273802+1, 1)

RERUN OF 3.32 meV:
range(273803,273852+1, 1)

FIFTH SET OF RUNS: (HF) <even further left the phase>
t-zero scan 1.00 meV = range(274178,274210+1, 1)
t-zero scan 1.55 meV = range(274211,274243+1, 1)
t-zero scan 3.32 meV = range(274244,274276+1, 1)
t-zero scan 6.59 meV = range(274277,274309+1, 1)
t-zero scan 12.0 meV = range(274310,274342+1, 1)
t-zero scan 25.0 meV = range(274343,274375+1, 1)
t-zero scan 80.0 meV = range(274376,274394+1, 1)


"""
"""
runs_list_1 = [range(273278,273302+1, 1), range(273303,273327+1, 1), range(273328,273352+1, 1), range(273353,273377+1, 1), range(273378,273402+1, 1), range(273403,273427+1, 1), range(273428,273452+1, 1)]
runs_list_2 = [range(273453,273477+1, 1), range(273478,273502+1, 1), range(273503,273527+1, 1), range(273528,273552+1, 1), range(273553,273577+1, 1), range(273578,273602+1, 1), range(273603,273627+1, 1)]
runs_list_3 = [range(273628,273652+1, 1), range(273653,273677+1, 1), range(273678,273702+1, 1), range(273703,273727+1, 1), range(273728,273752+1, 1), range(273753,273777+1, 1), range(273778,273802+1, 1)]
runs_list_4 = [range(273803,273852+1, 1)]
runs_list_5 = [range(274178,274210+1, 1), range(274211,274243+1, 1), range(274244,274276+1, 1), range(274277,274309+1, 1), range(274310,274342+1, 1), range(274343,274375+1, 1), range(274376,274394+1, 1)]

runs_list = runs_list_1 + runs_list_2 + runs_list_3 + runs_list_4

runs_list = runs_list_5
#                   #1.00 meV                            1.55 meV                              3.32 meV                             6.59 meV                               12 meV INCOMPLETE
#runs_list = [range(298790, 298822+1), range(298823, 298855+1), range(298856, 298888+1), range(298889, 298921+1), range(298922, 298931+1)]
"""

cut_the_run_range = 5
                   #1.00 meV, 1.55 meV, 3.32 meV, 6.59 meV, 12 meV, 25meV, 45meV, 80meVINCOMPLETE
runs_list = [range(299294+cut_the_run_range, 299323+1-cut_the_run_range), 
    range(299324+cut_the_run_range, 299353+1-cut_the_run_range), 
    range(299354+cut_the_run_range, 299383+1-cut_the_run_range), 
    range(299384+cut_the_run_range, 299413+1-cut_the_run_range), 
    range(299414+cut_the_run_range, 299443+1-cut_the_run_range), 
    range(299444+cut_the_run_range, 299473+1-cut_the_run_range),
    range(299474+cut_the_run_range, 299503+1-cut_the_run_range), 
    range(299521+cut_the_run_range, 299551+1-cut_the_run_range-2),]
"""
    range(299474+cut_the_run_range, 299503+1-cut_the_run_range), 
    range(299504+cut_the_run_range, 299518+1-cut_the_run_range*0), ]
"""
#runs_list = [    range(299521+cut_the_run_range, 299511+1-cut_the_run_range*0),]
#plt.close('all')


fitted_tzero_list = []
ei_list = []
fitted_tzero_error_list = []

for runs in runs_list:
    file_names = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs]
    #data = Load('+'.join(file_names))

    #
    #load the monitors


    fig_mon, ax_mon = plt.subplots(subplot_kw={'projection':'mantid'})

    Phase1_list = []
    total_intensity_list = []
    t_zero_list = []

    for this_run in file_names:

        #monitor = LoadNexusMonitors(file_names[0])
        monitor = LoadNexusMonitors(this_run)
        #print(dir(monitor))
        

        #LoadInstrument(data,FileName='/SNS/users/vdp/CNCS/2018B/CNCS_Definition_Pajerowski.xml', RewriteSpectraMap=False)

        Ei, _FMP, _FMI, T0 = GetEi(monitor)

        vi = 437.4*np.sqrt(Ei)
        print("vi", vi, "m/s")

        #
        #Get L1 (distance from source to sample), t1 (time from source to sample)
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

        
        ax_mon.plot(monitor)
        

        ##print(np.shape(monitor_tof[:-1]))
        ##print(np.shape(monitor_intensity))
        
        t_observed_monitor3 = np.sum(np.dot(monitor_tof[:-1]+0.5*tofbin_size, monitor_intensity)) / np.sum(monitor_intensity)
        total_intensity = np.sum(monitor_intensity)
        t_zero = t_observed_monitor3 - t_expected_monitor3
        
        Phase1_list.append(Phase1)
        total_intensity_list.append(total_intensity)
        t_zero_list.append(t_zero)
        
        


        #ax_mon.plot(monitor_tof[:-1]+0.5*tofbin_size,  monitor_intensity)
        #ax_mon.plot(monitor_tof, monitor_3_fit_height*gaussian(monitor_tof, monitor_3_fit_center, monitor_3_fit_sigma) )
        #ax_mon.set_xlim([monitor_3_fit_center-5*monitor_3_fit_sigma, monitor_3_fit_center+5*monitor_3_fit_sigma])
    
    plt.show()
    
    ax_mon.legend()

    print(t_zero)
    print(total_intensity)
    print(Phase1)


    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].scatter(Phase1_list, t_zero_list)
    axarr[0].set_ylabel('T-zero (microseconds)')
    axarr[0].set_title('Ei='+str(Ei)+'meV')
    axarr[1].scatter(Phase1_list, total_intensity_list)
    axarr[1].set_ylabel('Intensity at monitor 3')

    axarr[1].set_xlabel('Phase of chopper 1')



    f.show()

    my_fit_max = 18

    popt, pcov = curve_fit(gaussian, Phase1_list[0:my_fit_max], total_intensity_list[0:my_fit_max], p0 = (Phase1_list[np.argmax(total_intensity_list)], 100., 400.))
    popt_t0, pcov_t0 = curve_fit(linear_func, Phase1_list[0:my_fit_max], t_zero_list[0:my_fit_max], p0 = (1., 10.))


    f_fit, axarr_fit = plt.subplots(2, sharex=True)
    axarr_fit[0].scatter(Phase1_list, t_zero_list)
    axarr_fit[0].plot(Phase1_list,linear_func(Phase1_list, popt_t0[0], popt_t0[1]), linestyle='--')
    axarr_fit[0].plot(Phase1_list[0:my_fit_max],linear_func(Phase1_list[0:my_fit_max], popt_t0[0], popt_t0[1]), linewidth=3)
    axarr_fit[0].set_ylabel('T-zero (microseconds)')
    #axarr_fit[0].set_xlabel('Phase of chopper 1')
    axarr_fit[0].set_title('Ei='+str(Ei)+'meV')
    axarr_fit[0].text(np.min(Phase1_list),np.max(t_zero_list),"x0="+str(popt_t0[0]))
    axarr_fit[0].text(np.min(Phase1_list),0.8*np.max(t_zero_list),"x1="+str(popt_t0[1]))

    axarr_fit[1].scatter(Phase1_list, total_intensity_list)
    axarr_fit[1].plot(Phase1_list,gaussian(Phase1_list, popt[0], popt[1], popt[2]), linestyle='--')
    axarr_fit[1].plot(Phase1_list[0:my_fit_max],gaussian(Phase1_list[0:my_fit_max], popt[0], popt[1], popt[2]), linewidth=3)
    axarr_fit[1].set_ylabel('Intensity at monitor 3')
    axarr_fit[1].set_xlabel('Phase of chopper 1')
    #axarr_fit[1].set_title('Ei='+str(Ei)+'meV')
    axarr_fit[1].text(np.min(Phase1_list),popt[2]*0.0,"center="+str(popt[0]))
    axarr_fit[1].text(np.min(Phase1_list),popt[2]*0.1,"sigma="+str(popt[1]))
    axarr_fit[1].text(np.min(Phase1_list),popt[2]*0.2,"amp="+str(popt[2]))

    f_fit.show()


    #print(pcov_t0[0,0])
    fitted_tzero = popt_t0[0] + popt_t0[1]*popt[0]
    #fitted_tzero_error = pcov_t0[0,0] + pcov_t0[1,1]*popt[0]
    fitted_tzero_error = popt_t0[1]*pcov[0,0]
    print(Ei, fitted_tzero)
    
    ####
    fitted_tzero_list.append(fitted_tzero)
    fitted_tzero_error_list.append(fitted_tzero_error)
    ei_list.append(Ei)

plt.figure()

#ei_list = [1., 1.55, 3.32, 6.59, 12., 25., 80.]

popt_tzerofit, pcov_tzerofit = curve_fit(tzero_function, ei_list, fitted_tzero_list, p0 = (111.67, -28.527, -1.4753, 0.0001) )

dense_ei_list = np.arange(1., 80.5, 0.5)
plt.errorbar(ei_list, fitted_tzero_list, yerr=fitted_tzero_error_list,  label = 'these data', marker = 's')

plt.plot(dense_ei_list, 111.67-28.527*np.log(dense_ei_list)-1.4753*np.log(dense_ei_list)*np.log(dense_ei_list), 'k-', label = 'old t-zero function')

my_fitted_tzero_list = popt_tzerofit[0]-popt_tzerofit[1]*np.log(ei_list)-popt_tzerofit[2]*np.log(ei_list)*np.log(ei_list)-popt_tzerofit[3]*np.log(ei_list)*np.log(ei_list)*np.log(ei_list)

plt.plot(ei_list, np.subtract(my_fitted_tzero_list, fitted_tzero_list), 'gx-', label = 'residual of new data and new fit')

print(popt_tzerofit)

plt.plot(dense_ei_list, popt_tzerofit[0]-popt_tzerofit[1]*np.log(dense_ei_list)-popt_tzerofit[2]*np.log(dense_ei_list)*np.log(dense_ei_list)-popt_tzerofit[3]*np.log(dense_ei_list)*np.log(dense_ei_list)*np.log(dense_ei_list), 'r-', label = 'new t-zero function')

plt.xlabel('Ei meV')
plt.ylabel('fitted t-zero (microseconds)')

#data from 2018 emission table
plt.plot([1,1.55,3.32,6.59,12.0,25.0,80.0], [136.37,101.34,85.21,67.24,38.32,12.08,-62.67], 'mo', label = '2018 HF measurement')

plt.legend()
plt.show()




print(fitted_tzero_list)

print(popt_tzerofit[0]-popt_tzerofit[1]*np.log(ei_list)-popt_tzerofit[2]*np.log(ei_list)*np.log(ei_list)-popt_tzerofit[3]*np.log(ei_list)*np.log(ei_list)*np.log(ei_list))

plt.show()

np.save('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/AI_ei_list', ei_list)
np.save('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/AI_fitted_tzero_list',fitted_tzero_list)
np.save('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/AI_fitted_tzero_error_list',fitted_tzero_error_list)

np.save('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/AI_tzerofit_params', popt_tzerofit)

#plt.close('all')