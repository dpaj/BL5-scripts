import numpy as np
import matplotlib.pyplot as plt


#monitor = LoadNexusMonitors('	/SNS/CNCS/IPTS-22728/nexus/CNCS_308320.nxs.h5')#No sample 	Bottom Loading CCR 	12 meV first day of startup 	beam ramping 	05:37:26 	2019/06/21 12:17:04 EDT 	2019/06/21 17:54:30 EDT 	0.13 
monitor = LoadNexusMonitors('	/SNS/CNCS/IPTS-22728/nexus/CNCS_299743.nxs.h5')#No sample 	Bottom Loading CCR 	HF many energies for det tzero 	V-foil, HF, Ei=12.0 meV 	00:04:02 	2019/01/23 05:17:52 EST 	2019/01/23 05:21:54 EST 	0.33

#monitor = LoadNexusMonitors('	/SNS/CNCS/IPTS-22728/nexus/CNCS_308331.nxs.h5') #
#monitor = LoadNexusMonitors('	/SNS/CNCS/IPTS-22728/nexus/CNCS_308347.nxs.h5') #

LoadInstrument(monitor,FileName='/SNS/CNCS/shared/BL5-scripts/detector-positions/CNCS_Definition-addBM4-pre2019B.xml', RewriteSpectraMap=False)

run_was_with_bm4 = 0
divide_by_this_pC = 0.13

BM1_pos = monitor.getInstrument()[2][0].getPos()
BM2_pos = monitor.getInstrument()[2][1].getPos()
BM3_pos = monitor.getInstrument()[2][2].getPos()
BM4_pos = monitor.getInstrument()[2][3].getPos()

print("BM1 position = {} meters from sample".format(BM1_pos))
print("BM2 position = {} meters from sample".format(BM2_pos))
print("BM3 position = {} meters from sample".format(BM3_pos))
print("BM4 position = {} meters from sample".format(BM4_pos))

Ei = 12#meV

vi = 437.4*np.sqrt(Ei)
print("vi", vi, "m/s")

instr = monitor.getInstrument()

monitor1_position = instr[2][0].getPos() #now defunct monitor that is directly in front of chopper 1, the fermi chopper, should be ~6.313 m from the source
monitor2_position = instr[2][1].getPos() #monitor that is directly after chopper 2, the first bandwidth chopper, should be ~7.556 m from the source
monitor3_position = instr[2][2].getPos() #monitor that is directly after choppers 4+5, the double disc choppers, should be ~34.836 m from the source
monitor4_position = instr[2][3].getPos() #monitor that is after the sample position,
#monitor3 is the one that is most useful in this case

source_position = instr.getSource().getPos()
sample_position = instr.getSample().getPos()
L1 = np.linalg.norm(sample_position-source_position)
source_to_monitor2 = np.linalg.norm(monitor2_position-source_position)
source_to_monitor3 = np.linalg.norm(monitor3_position-source_position)
source_to_monitor4 = np.linalg.norm(monitor4_position-source_position)
t1 = L1/vi*1e6 #in microseconds
t_monitor2 = source_to_monitor2/vi*1e6
t_monitor3 = source_to_monitor3/vi*1e6
t_monitor4 = source_to_monitor4/vi*1e6

#the expected time to get to monitor2
t_expected_monitor2 = source_to_monitor2/vi * 1e6
print("t_expected_monitor2", t_expected_monitor2, "microseconds")

#the expected time to get to monitor3
t_expected_monitor3 = source_to_monitor3/vi * 1e6
print("t_expected_monitor3", t_expected_monitor3, "microseconds")

#the expected time to get to monitor4
t_expected_monitor4 = source_to_monitor4/vi * 1e6
print("t_expected_monitor4", t_expected_monitor4, "microseconds")

tofbin_monitor2_min = int(t_expected_monitor2*.85) 
tofbin_monitor2_max = int(t_expected_monitor2*1.15) 
print("peak at monitor2 from times of", tofbin_monitor2_min, "to",tofbin_monitor2_max,"in microseconds")

tofbin_monitor3_min = int(t_expected_monitor3*.95) 
tofbin_monitor3_max = int(t_expected_monitor3*1.05) 
print("peak at monitor3 from times of", tofbin_monitor3_min, "to",tofbin_monitor3_max,"in microseconds")

tofbin_monitor4_min = int(t_expected_monitor4*.95) 
tofbin_monitor4_max = int(t_expected_monitor4*1.05) 
print("peak at monitor4 from times of", tofbin_monitor4_min, "to",tofbin_monitor4_max,"in microseconds")

detid = monitor.getSpectrum(0).getDetectorIDs()[0]
print('Is detector {} a monitor? {}'.format(detid, monitor.getInstrument().getDetector(detid).isMonitor()))

detid = monitor.getSpectrum(1).getDetectorIDs()[0]
print('Is detector {} a monitor? {}'.format(detid, monitor.getInstrument().getDetector(detid).isMonitor()))

if run_was_with_bm4:
    detid = monitor.getSpectrum(2).getDetectorIDs()[0]
    print('Is detector {} a monitor? {}'.format(detid, monitor.getInstrument().getDetector(detid).isMonitor()))

#why doesn't this work as expected?  set if statement to run to test it
if 0:
    detid = monitor.getSpectrum(3).getDetectorIDs()[0]
    print('Is detector {} a monitor? {}'.format(detid, monitor.getInstrument().getDetector(detid).isMonitor()))

#time of flight for the monitors
tofbin_size = 1.
monitor2 = Rebin(InputWorkspace=monitor, OutputWorkspace='monitor2', Params="%s,%s,%s" % (tofbin_monitor2_min, tofbin_size, tofbin_monitor2_max))
monitor3 = Rebin(InputWorkspace=monitor, OutputWorkspace='monitor3', Params="%s,%s,%s" % (tofbin_monitor3_min, tofbin_size, tofbin_monitor3_max))
monitor4 = Rebin(InputWorkspace=monitor, OutputWorkspace='monitor4', Params="%s,%s,%s" % (tofbin_monitor4_min, tofbin_size, tofbin_monitor4_max))

monitor2 = CropWorkspace(monitor2, StartWorkspaceIndex = 0, EndWorkspaceIndex = 0)
monitor3 = CropWorkspace(monitor3, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)
if run_was_with_bm4:
    monitor4 = CropWorkspace(monitor4, StartWorkspaceIndex = 2, EndWorkspaceIndex = 2)




fig_mon, ax_mon = plt.subplots(subplot_kw={'projection':'mantid'})
ax_mon.plot(monitor2)
ax_mon.set_title('monitor2')
fig_mon.show()


fig_mon, ax_mon = plt.subplots(subplot_kw={'projection':'mantid'})
ax_mon.plot(monitor3)
ax_mon.set_title('monitor3')
fig_mon.show()

if run_was_with_bm4:
    fig_mon, ax_mon = plt.subplots(subplot_kw={'projection':'mantid'})
    ax_mon.plot(monitor4)
    ax_mon.set_title('monitor4')
    fig_mon.show()

#plt.close('all')

"""

#extract the arrays associated with the time-of-flight spectrum for the monitor3
monitor_tof = monitor.extractX()[0]
monitor_intensity = monitor.extractY()[0]

t_observed_monitor3 = np.sum(np.dot(monitor_tof[:-1]+0.5*tofbin_size, monitor_intensity)) / np.sum(monitor_intensity)
total_intensity = np.sum(monitor_intensity)
t_zero = t_observed_monitor3 - t_expected_monitor3

"""