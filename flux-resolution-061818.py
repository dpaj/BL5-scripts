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

redo_all_the_fits = 1

if redo_all_the_fits == 1:

    data_folder = '/SNS/CNCS/IPTS-20360/nexus/'

    #all the runs
    #runs = range(274470,274529+1, 1)

    #condition 1
    runs_1 = range(274470,274470+20, 1)

    #condition 3
    runs_3 = range(274470+20,274470+20+20, 1)

    #condition 0
    runs_0 = range(274470+20+20,274470+20+20+20, 1)


    file_names_1 = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_1]
    Ei_list_1 = []
    intensity_list_1 = []
    vi_list_1 = []
    fig_mon_1, ax_mon_1 = plt.subplots(subplot_kw={'projection':'mantid'})
    for thisfile in file_names_1:
        __raw = LoadEventNexus(Filename = thisfile, MetaDataOnly = True)
        run = __raw.getRun()
        #print(run.keys())
        print(run['DoubleDiskMode'].value[0], run['SpeedRequest4'].value[0], run['EnergyRequest'].value[0])
        speed_request_1 = run['SpeedRequest4'].value[0]


        #write the algorithm for one file then can loop over it
        monitor = LoadNexusMonitors(thisfile)
        Ei, _FMP, _FMI, T0 = GetEi(monitor)
        Ei_list_1.append(Ei)
        print("Ei", Ei, "meV")
        vi = 437.4*np.sqrt(Ei)
        print("vi", vi, "m/s")
        vi_list_1.append(vi)

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

        print("monitor intensity=",np.sum(monitor_intensity))
        intensity_list_1.append(np.sum(monitor_intensity))


        ax_mon_1.plot(monitor, label = "Ei="+str(Ei))

    fig_mon_1.show()


    file_names_3 = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_3]
    Ei_list_3 = []
    intensity_list_3 = []
    vi_list_3 = []
    fig_mon_3, ax_mon_3 = plt.subplots(subplot_kw={'projection':'mantid'})
    for thisfile in file_names_3:
        __raw = LoadEventNexus(Filename = thisfile, MetaDataOnly = True)
        run = __raw.getRun()
        #print(run.keys())
        print(run['DoubleDiskMode'].value[0], run['SpeedRequest4'].value[0], run['EnergyRequest'].value[0])
        speed_request_3 = run['SpeedRequest4'].value[0]


        #write the algorithm for one file then can loop over it
        monitor = LoadNexusMonitors(thisfile)
        Ei, _FMP, _FMI, T0 = GetEi(monitor)
        Ei_list_3.append(Ei)
        print("Ei", Ei, "meV")
        vi = 437.4*np.sqrt(Ei)
        print("vi", vi, "m/s")
        vi_list_3.append(vi)

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

        print("monitor intensity=",np.sum(monitor_intensity))
        intensity_list_3.append(np.sum(monitor_intensity))


        ax_mon_3.plot(monitor, label = "Ei="+str(Ei))

    fig_mon_3.show()


    file_names_0 = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_0]
    Ei_list_0 = []
    intensity_list_0 = []
    vi_list_0 = []
    fig_mon_0, ax_mon_0 = plt.subplots(subplot_kw={'projection':'mantid'})
    for thisfile in file_names_0:
        __raw = LoadEventNexus(Filename = thisfile, MetaDataOnly = True)
        run = __raw.getRun()
        #print(run.keys())
        print(run['DoubleDiskMode'].value[0], run['SpeedRequest4'].value[0], run['EnergyRequest'].value[0])
        speed_request_0 = run['SpeedRequest4'].value[0]


        #write the algorithm for one file then can loop over it
        monitor = LoadNexusMonitors(thisfile)
        Ei, _FMP, _FMI, T0 = GetEi(monitor)
        Ei_list_0.append(Ei)
        print("Ei", Ei, "meV")
        vi = 437.4*np.sqrt(Ei)
        print("vi", vi, "m/s")
        vi_list_0.append(vi)

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

        print("monitor intensity=",np.sum(monitor_intensity))
        intensity_list_0.append(np.sum(monitor_intensity))


        ax_mon_0.plot(monitor, label = "Ei="+str(Ei))

    fig_mon_0.show()




    van = Load(Filename='/SNS/CNCS/IPTS-21088/shared/autoreduce/van_273992.nxs', OutputWorkspace='van')

    fwhm_list_1 = []
    for thisfile in file_names_1:
        __raw = LoadEventNexus(Filename = thisfile)
        run = __raw.getRun()
        print(run['DoubleDiskMode'].value[0], run['SpeedRequest4'].value[0], run['EnergyRequest'].value[0])
        Ei = run['EnergyRequest'].value[0]
        print(Ei)

        my_dgs,_ = DgsReduction(
                SampleInputWorkspace = __raw,
                SampleInputMonitorWorkspace = __raw,
                EnergyTransferRange = [-0.15*Ei, Ei/200., 0.9*Ei],
                SofPhiEIsDistribution = True, #this will keep the output data as a histogram
                CorrectKiKf = True,
                DetectorVanadiumInputWorkspace = van,
                UseProcessedDetVan = True,
                IncidentBeamNormalisation='ByCurrent',
                )
                
        my_md = ConvertToMD(my_dgs, QDimensions = '|Q|', dEAnalysisMode = 'Direct')        

        my_slice = BinMD(
                InputWorkspace = my_md, 
                AxisAligned = True, 
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 100',
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.9*Ei)+', 50', 
                )

        my_line = BinMD(
                InputWorkspace = my_md, 
                AxisAligned = True, 
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 1',
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.1*Ei)+', 30', 
                )
                
        #make a plot of a slice using the mantid projection
        fig_slice, ax = plt.subplots(subplot_kw={'projection':'mantid'})
        c = ax.pcolormesh(my_slice)#, vmin=0, vmax=1.5e-1)
        cbar=fig_slice.colorbar(c)
        cbar.set_label('Intensity (arb. units)') #add text to colorbar
        ax.set_title(str(Ei))
        fig_slice.show()


        #to access and plot line array
        fig, ax = plt.subplots()
        E, I, dI = mantid.plots.helperfunctions.get_md_data1d(my_line,mantid.plots.helperfunctions.get_normalization(my_line)[0])

        #x, mu, sig, scale
        popt, pcov = curve_fit(gaussian, E, I, p0 = (0.01, 0.025*Ei, np.max(I)) )
        E_dense = np.arange(-0.1*Ei, 0.1*Ei, 0.001*Ei)
        print(popt)
        print(0.01, 0.025*Ei, np.max(I)) 

        ax.errorbar(E, I, yerr=dI, fmt='s-', label=str(Ei))
        this_fwhm_1 = 2.355*popt[1]
        fwhm_list_1.append(this_fwhm_1)
        ax.plot(E_dense, gaussian(E_dense, popt[0], popt[1], popt[2]), label = 'gaussian fit\nfwhm='+str(this_fwhm_1))
        ax.legend()
        ax.set_xlabel('E (meV)')
        ax.set_ylabel('Intensity (arb. units)')
        ax.set_ylim([0, np.max(I)*1.5])
        fig.show()


    fwhm_list_3 = []
    for thisfile in file_names_3:
        __raw = LoadEventNexus(Filename = thisfile)
        run = __raw.getRun()
        print(run['DoubleDiskMode'].value[0], run['SpeedRequest4'].value[0], run['EnergyRequest'].value[0])
        Ei = run['EnergyRequest'].value[0]

        my_dgs,_ = DgsReduction(
                SampleInputWorkspace = __raw,
                SampleInputMonitorWorkspace = __raw,
                EnergyTransferRange = [-0.15*Ei, Ei/200., 0.9*Ei],
                SofPhiEIsDistribution = True, #this will keep the output data as a histogram
                CorrectKiKf = True,
                DetectorVanadiumInputWorkspace = van,
                UseProcessedDetVan = True,
                IncidentBeamNormalisation='ByCurrent',
                )
                
        my_md = ConvertToMD(my_dgs, QDimensions = '|Q|', dEAnalysisMode = 'Direct')        

        my_slice = BinMD(
                InputWorkspace = my_md, 
                AxisAligned = True, 
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 100',
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.9*Ei)+', 50', 
                )

        my_line = BinMD(
                InputWorkspace = my_md, 
                AxisAligned = True, 
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 1',
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.1*Ei)+', 30', 
                )
                
        #make a plot of a slice using the mantid projection
        fig_slice, ax = plt.subplots(subplot_kw={'projection':'mantid'})
        c = ax.pcolormesh(my_slice)#, vmin=0, vmax=1.5e-1)
        cbar=fig_slice.colorbar(c)
        cbar.set_label('Intensity (arb. units)') #add text to colorbar
        ax.set_title(str(Ei))
        fig_slice.show()


        #to access and plot line array
        fig, ax = plt.subplots()
        E, I, dI = mantid.plots.helperfunctions.get_md_data1d(my_line,mantid.plots.helperfunctions.get_normalization(my_line)[0])

        #x, mu, sig, scale
        popt, pcov = curve_fit(gaussian, E, I, p0 = (0.01, 0.025*Ei, np.max(I)) )
        E_dense = np.arange(-0.1*Ei, 0.1*Ei, 0.001*Ei)
        print(popt)
        print(0.01, 0.025*Ei, np.max(I)) 

        ax.errorbar(E, I, yerr=dI, fmt='s-', label=str(Ei))
        this_fwhm_3 = 2.355*popt[1]
        fwhm_list_3.append(this_fwhm_3)
        ax.plot(E_dense, gaussian(E_dense, popt[0], popt[1], popt[2]), label = 'gaussian fit\nfwhm='+str(this_fwhm_3))
        ax.legend()
        ax.set_xlabel('E (meV)')
        ax.set_ylabel('Intensity (arb. units)')
        ax.set_ylim([0, np.max(I)*1.5])
        fig.show()



    fwhm_list_0 = []
    for thisfile in file_names_0:
        __raw = LoadEventNexus(Filename = thisfile)
        run = __raw.getRun()
        print(run['DoubleDiskMode'].value[0], run['SpeedRequest4'].value[0], run['EnergyRequest'].value[0])
        Ei = run['EnergyRequest'].value[0]

        my_dgs,_ = DgsReduction(
                SampleInputWorkspace = __raw,
                SampleInputMonitorWorkspace = __raw,
                EnergyTransferRange = [-0.15*Ei, Ei/200., 0.9*Ei],
                SofPhiEIsDistribution = True, #this will keep the output data as a histogram
                CorrectKiKf = True,
                DetectorVanadiumInputWorkspace = van,
                UseProcessedDetVan = True,
                IncidentBeamNormalisation='ByCurrent',
                )
                
        my_md = ConvertToMD(my_dgs, QDimensions = '|Q|', dEAnalysisMode = 'Direct')        

        my_slice = BinMD(
                InputWorkspace = my_md, 
                AxisAligned = True, 
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 100',
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.9*Ei)+', 50', 
                )

        my_line = BinMD(
                InputWorkspace = my_md, 
                AxisAligned = True, 
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 1',
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.1*Ei)+', 30', 
                )
                
        #make a plot of a slice using the mantid projection
        fig_slice, ax = plt.subplots(subplot_kw={'projection':'mantid'})
        c = ax.pcolormesh(my_slice)#, vmin=0, vmax=1.5e-1)
        cbar=fig_slice.colorbar(c)
        cbar.set_label('Intensity (arb. units)') #add text to colorbar
        ax.set_title(str(Ei))
        fig_slice.show()


        #to access and plot line array
        fig, ax = plt.subplots()
        E, I, dI = mantid.plots.helperfunctions.get_md_data1d(my_line,mantid.plots.helperfunctions.get_normalization(my_line)[0])

        #x, mu, sig, scale
        popt, pcov = curve_fit(gaussian, E, I, p0 = (0.01, 0.025*Ei, np.max(I)) )
        E_dense = np.arange(-0.1*Ei, 0.1*Ei, 0.001*Ei)
        print(popt)
        print(0.01, 0.025*Ei, np.max(I)) 

        ax.errorbar(E, I, yerr=dI, fmt='s-', label=str(Ei))
        this_fwhm_0 = 2.355*popt[1]
        fwhm_list_0.append(this_fwhm_0)
        ax.plot(E_dense, gaussian(E_dense, popt[0], popt[1], popt[2]), label = 'gaussian fit\nfwhm='+str(this_fwhm_0))
        ax.legend()
        ax.set_xlabel('E (meV)')
        ax.set_ylabel('Intensity (arb. units)')
        ax.set_ylim([0, np.max(I)*1.5])
        fig.show()

    print(os.getcwd())
    np.save('flux-resolution-Ei_list_1', Ei_list_1)
    np.save('flux-resolution-Ei_list_3', Ei_list_3)
    np.save('flux-resolution-Ei_list_0', Ei_list_0)

    np.save('flux-resolution-fwhm_list_1', fwhm_list_1)
    np.save('flux-resolution-fwhm_list_3', fwhm_list_3)
    np.save('flux-resolution-fwhm_list_0', fwhm_list_0)

    np.save('flux-resolution-vi_list_1', vi_list_1)
    np.save('flux-resolution-vi_list_3', vi_list_3)
    np.save('flux-resolution-vi_list_0', vi_list_0)

    np.save('flux-resolution-intensity_list_1', intensity_list_1)
    np.save('flux-resolution-intensity_list_3', intensity_list_3)
    np.save('flux-resolution-intensity_list_0', intensity_list_0)
else:
    os.chdir('/SNS/users/vdp/CNCS/2018B/')
    Ei_list_1 = np.load('flux-resolution-Ei_list_1.npy', )
    Ei_list_3 = np.load('flux-resolution-Ei_list_3.npy', )
    Ei_list_0 = np.load('flux-resolution-Ei_list_0.npy', )

    fwhm_list_1 = np.load('flux-resolution-fwhm_list_1.npy', )
    fwhm_list_3 = np.load('flux-resolution-fwhm_list_3.npy', )
    fwhm_list_0 = np.load('flux-resolution-fwhm_list_0.npy', )

    vi_list_1 = np.load('flux-resolution-vi_list_1.npy', )
    vi_list_3 = np.load('flux-resolution-vi_list_3.npy', )
    vi_list_0 = np.load('flux-resolution-vi_list_0.npy', )

    intensity_list_1 = np.load('flux-resolution-intensity_list_1.npy', )
    intensity_list_3 = np.load('flux-resolution-intensity_list_3.npy', )
    intensity_list_0 = np.load('flux-resolution-intensity_list_0.npy', )

plt.figure(figsize = [8,10])
ax_resolution = plt.gca()
plt.loglog(Ei_list_1, fwhm_list_1, 's-', label = 'dd=1, speed='+str(speed_request_1)+" Hz")
plt.loglog(Ei_list_3, fwhm_list_3, '^-', label = 'dd=3, speed='+str(speed_request_3)+" Hz")
plt.loglog(Ei_list_0, fwhm_list_0, 'x-', label = 'dd=0, speed='+str(speed_request_0)+" Hz")
plt.xlabel('E (meV)')
plt.ylabel('elastic gaussian FWHM (meV)')
plt.legend(loc = 'upper left')
plt.grid(b=True, which='major', color='y', linestyle='-')
plt.grid(b=True, which='minor', color='k', linestyle='-')

plt.tick_params(axis='y', which='minor')
ax_resolution.yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
for label in ax_resolution.yaxis.get_ticklabels('minor')[1::2]:
    label.set_visible(False)
for label in ax_resolution.yaxis.get_ticklabels('minor')[0::2]:
    label.set_rotation(45)
for label in ax_resolution.yaxis.get_ticklabels():
    label.set_rotation(45)
    
plt.tick_params(axis='x', which='minor')
ax_resolution.xaxis.set_minor_formatter(FormatStrFormatter("%.1f"))
for label in ax_resolution.xaxis.get_ticklabels('minor')[1::2]:
    label.set_visible(False)
for label in ax_resolution.xaxis.get_ticklabels('minor')[0::2]:
    label.set_rotation(-45)
for label in ax_resolution.xaxis.get_ticklabels():
    label.set_rotation(-45)

plt.xlim([0.7, 100.])
plt.ylim([1e-2, 20])
plt.show()

plt.figure(figsize = [8,10])
ax_flux = plt.gca()
plt.loglog(Ei_list_1, np.multiply(intensity_list_1, vi_list_1), 's-', label = 'dd=1, speed='+str(speed_request_1)+" Hz")
plt.loglog(Ei_list_3, np.multiply(intensity_list_3, vi_list_3), '^-', label = 'dd=3, speed='+str(speed_request_3)+" Hz")
plt.loglog(Ei_list_0, np.multiply(intensity_list_0, vi_list_0), 'x-', label = 'dd=0, speed='+str(speed_request_0)+" Hz")
plt.xlabel('E (meV)')
plt.ylabel('monitor counts times velocity')
plt.legend(loc = 'upper left')
plt.grid(b=True, which='major', color='y', linestyle='-')
plt.grid(b=True, which='minor', color='k', linestyle='-')

plt.tick_params(axis='y', which='minor')
ax_flux.yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
for label in ax_flux.yaxis.get_ticklabels('minor')[1::2]:
    label.set_visible(False)
for label in ax_flux.yaxis.get_ticklabels('minor')[0::2]:
    label.set_rotation(45)
for label in ax_flux.yaxis.get_ticklabels():
    label.set_rotation(45)
    
plt.tick_params(axis='x', which='minor')
ax_flux.xaxis.set_minor_formatter(FormatStrFormatter("%.1f"))
for label in ax_flux.xaxis.get_ticklabels('minor')[1::2]:
    label.set_visible(False)
for label in ax_flux.xaxis.get_ticklabels('minor')[0::2]:
    label.set_rotation(-45)
for label in ax_flux.xaxis.get_ticklabels():
    label.set_rotation(-45)

plt.xlim([0.7, 100.])
plt.ylim([1e6, 1e9])

f = ScalarFormatter(useOffset=False, useMathText=True)
g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
ax_flux.yaxis.set_minor_formatter(FuncFormatter(g))

plt.show()



plt.figure(figsize = [8,10])
ax_flux = plt.gca()
plt.loglog(Ei_list_1, np.multiply(intensity_list_1, vi_list_1)/398696139.0, 's-', label = 'dd=1, speed='+str(speed_request_1)+" Hz")
plt.loglog(Ei_list_3, np.multiply(intensity_list_3, vi_list_3)/398696139.0, '^-', label = 'dd=3, speed='+str(speed_request_3)+" Hz")
plt.loglog(Ei_list_0, np.multiply(intensity_list_0, vi_list_0)/398696139.0, 'x-', label = 'dd=0, speed='+str(speed_request_0)+" Hz")
plt.xlabel('E (meV)')
plt.ylabel('monitor counts times velocity')
plt.legend(loc = 'upper left')
plt.grid(b=True, which='major', color='y', linestyle='-')
plt.grid(b=True, which='minor', color='k', linestyle='-')

plt.tick_params(axis='y', which='minor')
ax_flux.yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
for label in ax_flux.yaxis.get_ticklabels('minor')[1::2]:
    label.set_visible(False)
for label in ax_flux.yaxis.get_ticklabels('minor')[0::2]:
    label.set_rotation(15)
for label in ax_flux.yaxis.get_ticklabels():
    label.set_rotation(15)
    
plt.tick_params(axis='x', which='minor')
ax_flux.xaxis.set_minor_formatter(FormatStrFormatter("%.1f"))
for label in ax_flux.xaxis.get_ticklabels('minor')[1::2]:
    label.set_visible(False)
for label in ax_flux.xaxis.get_ticklabels('minor')[0::2]:
    label.set_rotation(-45)
for label in ax_flux.xaxis.get_ticklabels():
    label.set_rotation(-45)

plt.xlim([0.7, 100.])
plt.ylim([1e-3, 10e0])

f = ScalarFormatter(useOffset=False, useMathText=True)
g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
ax_flux.yaxis.set_minor_formatter(FuncFormatter(g))

plt.show()

for idx,i in enumerate(intensity_list_0): print(i*vi_list_0[idx]/398696139.67)
plt.close('all')