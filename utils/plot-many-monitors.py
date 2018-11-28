import numpy as np
import matplotlib.pyplot as plt


data_folder = '/SNS/CNCS/IPTS-20360/nexus/'
#condition 1
runs_1 = range(274470,274470+20, 1)
this_run = 274470

fig, ax = plt.subplots()

iteration = 0
for this_run in runs_1:
    iteration = iteration + 1
    filename = data_folder+'CNCS_{0}.nxs.h5'.format(this_run)

    monitor = LoadNexusMonitors(filename)

    print("Ei",monitor .getRun()['EnergyRequest'].firstValue(), "meV")

    mode = monitor .run()['DoubleDiskMode'].timeAverageValue()
    print("double-disc-mode",mode)

    Ei, _FMP, _FMI, T0 = GetEi(monitor)
    print(Ei)


    #time of flight for the monitors
    Rebin(InputWorkspace='monitor', OutputWorkspace='monitor', Params="1" )
    monitor2 = CropWorkspace(monitor, StartWorkspaceIndex = 0, EndWorkspaceIndex = 0)
    monitor3 = CropWorkspace(monitor, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)

    #extract the arrays associated with the time-of-flight spectrum for the monitor3
    monitor3_tof = monitor3.extractX()[0]
    monitor3_intensity = monitor3.extractY()[0]
    monitor3_tof_c = monitor3_tof[:-1]-(monitor3_tof[0]-monitor3_tof[1])/2.

    #extract the arrays associated with the time-of-flight spectrum for the monitor2
    monitor2_tof = monitor2.extractX()[0]
    monitor2_intensity = monitor2.extractY()[0]
    monitor2_tof_c = monitor2_tof[:-1]-(monitor2_tof[0]-monitor2_tof[1])/2.
    
    #ax.plot(monitor3_tof_c, monitor3_intensity+iteration*1e2, label = Ei)
    ax.plot(monitor2_tof_c, monitor2_intensity+iteration*1e3, label = Ei)

ax.set_xlabel('time (micro-seconds)')
ax.set_ylabel('intensity (arb. u.)')
ax.legend()
fig.show()