import numpy as np
import matplotlib.pyplot as plt

thisfile = '/SNS/CNCS/IPTS-20360/nexus/CNCS_274474.nxs.h5'
raw = LoadEventNexus(Filename = thisfile, MetaDataOnly = True)
run = raw.getRun()
instr = raw.getInstrument()
monitor = LoadNexusMonitors(thisfile)

pc = run['proton_charge'].value
nonzero_pc = pc[np.nonzero(run['proton_charge'].value)]
number_of_pulses = np.shape(nonzero_pc)[0]
pulse_spacing = 1/60. # seconds
total_uptime = number_of_pulses * pulse_spacing
average_power_during_uptime = np.mean(nonzero_pc) * 60. * 1e-9




Ei, _FMP, _FMI, T0 = GetEi(raw)
vi = 437.4*np.sqrt(Ei)
monitor3_position = instr[2][2].getPos() #monitor that is directly after choppers 4+5, the double disc choppers, should be ~34.836 m from the source
source_position = instr.getSource().getPos() #position of the moderator source
source_to_monitor3 = np.linalg.norm(monitor3_position-source_position) #distance between the source and the monitor3
t_expected_monitor3 = source_to_monitor3/vi * 1e6 + T0 #expected arrival time at monitor3

tofbin_monitor3_min = int(t_expected_monitor3*.95) #the minimum TOF value to use for summing up the monitor counts
tofbin_monitor3_max = int(t_expected_monitor3*1.05) #the maximum TOF value to use for summing up the monitor counts
tofbin_size = 100. #binning for the monitor, units of microseconds
Rebin(InputWorkspace='monitor', OutputWorkspace='monitor', Params="%s,%s,%s" % (tofbin_monitor3_min, tofbin_size, tofbin_monitor3_max)) #default is one bin, rebin to tofbin_size
monitor = CropWorkspace(monitor, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)

monitor_tof = monitor.extractX()[0] #extract the monitor3 TOF array
monitor_intensity = monitor.extractY()[0] #extract the monitor3 intensity array

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
ax.plot(monitor)
fig.show()

monitor_pulse_total_counts = np.sum(monitor_intensity)# * 1e-6 * tofbin_size #the flux in counts/second at monitor3 for a given pulse, rectangular integration with the fixed time-width (tofbin_size) outside of the summation      
monitor_absolute_intensity = monitor_pulse_total_counts / 8.8e-6 * vi/2197.763809 / total_uptime # the counts per pulse, divided by the efficiency at 1.8 angstroms (~25 meV), times the velocity correction, times 60 pulses per second
monitor_absolute_intensity_perMW = monitor_absolute_intensity / average_power_during_uptime


print(Ei, monitor_pulse_total_counts , monitor_absolute_intensity, monitor_absolute_intensity_perMW)