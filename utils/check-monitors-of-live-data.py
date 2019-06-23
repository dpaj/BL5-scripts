import numpy as np
import matplotlib.pyplot as plt


#live_data = StartLiveData(FromNow=False, FromStartOfRun=True, Instrument='CNCS', Listener='SNSLiveEventDataListener', Address='bl5-daq1.sns.gov:31415', StartTime='1990-01-01T00:00:01', RunTransitionBehavior='Stop', OutputWorkspace='live-data', MonitorLiveData='')

LoadInstrument(mtd['live-data'],FileName='/SNS/CNCS/shared/BL5-scripts/detector-positions/CNCS_Definition-addBM4-pre2019B.xml', RewriteSpectraMap=False)

BM1_pos = mtd['live-data'].getInstrument()[2][0].getPos()
BM2_pos = mtd['live-data'].getInstrument()[2][1].getPos()
BM3_pos = mtd['live-data'].getInstrument()[2][2].getPos()
BM4_pos = mtd['live-data'].getInstrument()[2][3].getPos()

print("BM1 position = {} meters from sample".format(BM1_pos))
print("BM2 position = {} meters from sample".format(BM2_pos))
print("BM3 position = {} meters from sample".format(BM3_pos))
print("BM4 position = {} meters from sample".format(BM4_pos))

Ei = 12#meV

vi = 437.4*np.sqrt(Ei)
print("vi", vi, "m/s")

instr = mtd['live-data'].getInstrument()

monitor1_position = instr[2][0].getPos() #now defunct monitor that is directly in front of chopper 1, the fermi chopper, should be ~6.313 m from the source
monitor2_position = instr[2][1].getPos() #monitor that is directly after chopper 2, the first bandwidth chopper, should be ~7.556 m from the source
monitor3_position = instr[2][2].getPos() #monitor that is directly after choppers 4+5, the double disc choppers, should be ~34.836 m from the source
monitor4_position = instr[2][3].getPos() #monitor that is after the sample position,
#monitor3 is the one that is most useful in this case

source_position = instr.getSource().getPos()
sample_position = instr.getSample().getPos()
L1 = np.linalg.norm(sample_position-source_position)
source_to_monitor3 = np.linalg.norm(monitor3_position-source_position)
source_to_monitor4 = np.linalg.norm(monitor4_position-source_position)
t1 = L1/vi*1e6 #in microseconds
t_monitor3 = source_to_monitor3/vi*1e6
t_monitor4 = source_to_monitor4/vi*1e6

#the expected time to get to monitor3
t_expected_monitor3 = source_to_monitor3/vi * 1e6
print("t_expected_monitor3", t_expected_monitor3, "microseconds")

#the expected time to get to monitor4
t_expected_monitor4 = source_to_monitor4/vi * 1e6
print("t_expected_monitor4", t_expected_monitor4, "microseconds")


tofbin_monitor3_min = int(t_expected_monitor3*.95) 
tofbin_monitor3_max = int(t_expected_monitor3*1.05) 
print("peak at monitor3 from times of", tofbin_monitor3_min, "to",tofbin_monitor3_max,"in microseconds")

tofbin_monitor4_min = int(t_expected_monitor4*.95) 
tofbin_monitor4_max = int(t_expected_monitor4*1.05) 
print("peak at monitor4 from times of", tofbin_monitor4_min, "to",tofbin_monitor4_max,"in microseconds")

detid = mtd['live-data'].getSpectrum(0).getDetectorIDs()[0]
print('Is detector {} a monitor? {}'.format(detid, mtd['live-data'].getInstrument().getDetector(detid).isMonitor()))

detid = mtd['live-data'].getSpectrum(1).getDetectorIDs()[0]
print('Is detector {} a monitor? {}'.format(detid, mtd['live-data'].getInstrument().getDetector(detid).isMonitor()))

detid = mtd['live-data'].getSpectrum(2).getDetectorIDs()[0]
print('Is detector {} a monitor? {}'.format(detid, mtd['live-data'].getInstrument().getDetector(detid).isMonitor()))

detid = mtd['live-data'].getSpectrum(3).getDetectorIDs()[0]
print('Is detector {} a monitor? {}'.format(detid, mtd['live-data'].getInstrument().getDetector(detid).isMonitor()))




mon_spec2 = mtd['live-data'].getSpectrum(2)

print(mon_spec2)

#time of flight for the monitors
tofbin_size = 1.
Rebin(InputWorkspace=mtd['live-data'], OutputWorkspace='asdf', Params="%s,%s,%s" % (tofbin_monitor3_min, tofbin_size, tofbin_monitor3_max))
monitor = CropWorkspace('asdf', StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)

#extract the arrays associated with the time-of-flight spectrum for the monitor3
monitor_tof = monitor.extractX()[0]
monitor_intensity = monitor.extractY()[0]

fig_mon, ax_mon = plt.subplots(subplot_kw={'projection':'mantid'})
ax_mon.plot(monitor)
fig_mon.show()

t_observed_monitor3 = np.sum(np.dot(monitor_tof[:-1]+0.5*tofbin_size, monitor_intensity)) / np.sum(monitor_intensity)
total_intensity = np.sum(monitor_intensity)
t_zero = t_observed_monitor3 - t_expected_monitor3