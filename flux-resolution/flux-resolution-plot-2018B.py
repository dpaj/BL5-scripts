import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from mantid import plots
from matplotlib.colors import LogNorm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from matplotlib.ticker import FormatStrFormatter, FuncFormatter, ScalarFormatter

"""
this file generates plots from the flux-resolution-calc*.py script and saves pdf's
it is set up for a very specific measurement that takes data for the three different chopper openings
These 2018B data were taken on the ~1 mm thickness, 10 mm diameter, 63 mm tall vanadium inside of a aluminum holder
The nominal SNS power during this time is 1.3 MW
"""

"""
def flux_res_load(filename_prefix):
    Ei_list = np.load(filename_prefix+'Ei_list.npy')
    monitor_intensity_list = np.load(filename_prefix+'monitor_intensity_list.npy')
    vi_list = np.load(filename_prefix+'vi_list.npy')
    detector_intensity_list = np.load(filename_prefix+'detector_intensity_list.npy')
    detector_FWHM_list = np.load(filename_prefix+'detector_FWHM_list.npy')
    DD_opening_list = np.load(filename_prefix+'DD_opening_list.npy')
    DD_speed_list = np.load(filename_prefix+'DD_speed_list.npy')
    return Ei_list, monitor_intensity_list, vi_list, detector_intensity_list, detector_FWHM_list, DD_opening_list, DD_speed_list
"""
working_directory = '/SNS/CNCS/shared/BL5-scripts/flux-resolution/'    
os.chdir(working_directory)

wavelength_axis_show = 1

file_prefix = '2018B-'
file_prefix_1 = '2018B-HF-'
file_prefix_3 = '2018B-AI-'
file_prefix_0 = '2018B-HR-'

Ei_list_1 = np.load(file_prefix_1+'Ei_list.npy')
Ei_list_3 = np.load(file_prefix_3+'Ei_list.npy')
Ei_list_0 = np.load(file_prefix_0+'Ei_list.npy')

fwhm_list_1 = np.load(file_prefix_1+'detector_FWHM_list.npy')
fwhm_list_3 = np.load(file_prefix_3+'detector_FWHM_list.npy')
fwhm_list_0 = np.load(file_prefix_0+'detector_FWHM_list.npy')

intensity_list_1 = np.load(file_prefix_1+'monitor_normalized_intensity_perMW_list.npy')
intensity_list_3 = np.load(file_prefix_3+'monitor_normalized_intensity_perMW_list.npy')
intensity_list_0 = np.load(file_prefix_0+'monitor_normalized_intensity_perMW_list.npy')

speed_request_1 = np.mean(np.load(file_prefix_1+'DD_speed_list.npy'))
speed_request_3 = np.mean(np.load(file_prefix_3+'DD_speed_list.npy'))
speed_request_0 = np.mean(np.load(file_prefix_0+'DD_speed_list.npy'))

DD_opening_1 = int(np.mean(np.load(file_prefix_1+'DD_opening_list.npy')))
DD_opening_3 = int(np.mean(np.load(file_prefix_3+'DD_opening_list.npy')))
DD_opening_0 = int(np.mean(np.load(file_prefix_0+'DD_opening_list.npy')))

dd_num_to_opening = {1:'HF', 3: 'AI', 0: 'HR'} #go from numbering system to the well known opening labels

legend_font = font_manager.FontProperties(family='monospace',
                                   weight='normal',
                                   style='normal', size=14)

plt.figure(figsize = [8,10])
ax_resolution = plt.gca()
plt.loglog(Ei_list_1, fwhm_list_1, 's-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_1], speed_request_1) )
plt.loglog(Ei_list_3, fwhm_list_3, '^-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_3], speed_request_3) )
plt.loglog(Ei_list_0, fwhm_list_0, 'o-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_0], speed_request_0) )
plt.xlabel('E (meV)')
plt.ylabel('elastic gaussian FWHM (meV)')
plt.legend(loc = 'upper left', prop = legend_font)
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

plt.xlim([0.5, 100.])
plt.ylim([5e-3, 20])


ax_resolution.axvspan(0.5, 1., facecolor='gray') #color over the lower energy that should not typically be used
ax_resolution.axvspan(20., 100., facecolor='gray') #color over the higher energy that should not typically be used

if wavelength_axis_show ==1:
    ax_wl = ax_resolution.twiny()
    ax_wl.set_xscale('log')
    tick_locations = np.array([0.6, 0.8, 1., 2, 4, 6, 8, 10, 20, 40, 60, 80, 100])
    #tick_locations = np.array([1, 10, 100])

    def tick_function(X):
        V = np.sqrt(81.81/X)
        return ["%.3f" % z for z in V]

    ax_wl.set_xticks(tick_locations)
    ax_wl.set_xlim(ax_resolution.get_xlim())
    ax_wl.set_xticklabels(tick_function(tick_locations))
    ax_wl.set_xlabel(r"wavelength ($\AA$)")
    for label in ax_wl.xaxis.get_ticklabels():
        label.set_rotation(-45)

ax_resolution.tick_params(axis='both', direction = 'inout', length = 20, which = 'major')
ax_resolution.tick_params(axis='both', direction = 'inout', length = 12, which = 'minor')
ax_wl.tick_params(axis='both', direction = 'inout', length = 20, which = 'major')
ax_wl.tick_params(axis='both', direction = 'inout', length = 12, which = 'minor')

plt.savefig(file_prefix+'elastic-resolution.pdf', format = 'pdf')
plt.show()

plt.figure(figsize = [8,10])
ax_flux = plt.gca()
plt.loglog(Ei_list_1, intensity_list_1, 's-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_1], speed_request_1) )
plt.loglog(Ei_list_3, intensity_list_3, '^-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_3], speed_request_3) )
plt.loglog(Ei_list_0, intensity_list_0, 'o-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_0], speed_request_0) )
plt.xlabel('E (meV)')
plt.ylabel('monitor3 flux (n/s/MW)')
plt.legend(loc = 'upper left', prop = legend_font)
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

plt.xlim([0.5, 100.])
plt.ylim([7e3, 3e7])

f = ScalarFormatter(useOffset=False, useMathText=True)
g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
ax_flux.yaxis.set_minor_formatter(FuncFormatter(g))
ax_flux.axvspan(0.5, 1., facecolor='gray') #color over the lower energy that should not typically be used
ax_flux.axvspan(20., 100., facecolor='gray') #color over the higher energy that should not typically be used

if wavelength_axis_show ==1:
    ax_wl = ax_flux.twiny()
    ax_wl.set_xscale('log')
    tick_locations = np.array([0.6, 0.8, 1., 2, 4, 6, 8, 10, 20, 40, 60, 80, 100])
    #tick_locations = np.array([1, 10, 100])

    def tick_function(X):
        V = np.sqrt(81.81/X)
        return ["%.3f" % z for z in V]

    ax_wl.set_xticks(tick_locations)
    ax_wl.set_xlim(ax_flux.get_xlim())
    ax_wl.set_xticklabels(tick_function(tick_locations))
    ax_wl.set_xlabel(r"wavelength ($\AA$)")
    for label in ax_wl.xaxis.get_ticklabels():
        label.set_rotation(-45)
ax_flux.tick_params(axis='both', direction = 'inout', length = 20, which = 'major')
ax_flux.tick_params(axis='both', direction = 'inout', length = 12, which = 'minor')
ax_wl.tick_params(axis='both', direction = 'inout', length = 20, which = 'major')
ax_wl.tick_params(axis='both', direction = 'inout', length = 12, which = 'minor')

plt.savefig(file_prefix+'intensity-monitor3-neutrons.pdf', format = 'pdf')
plt.show()



plt.figure(figsize = [8,10])
ax_flux = plt.gca()
plt.loglog(Ei_list_1, intensity_list_1/np.max(intensity_list_1), 's-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_1], speed_request_1) )
plt.loglog(Ei_list_3, intensity_list_3/np.max(intensity_list_1), '^-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_3], speed_request_3) )
plt.loglog(Ei_list_0, intensity_list_0/np.max(intensity_list_1), 'o-', label = 'dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_0], speed_request_0) )
plt.xlabel('E (meV)')
plt.ylabel('monitor3 intensity normalized to peak flux')
plt.legend(loc = 'upper left', prop= legend_font)
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

plt.xlim([0.5, 100.])
plt.ylim([1e-3, 10e0])

f = ScalarFormatter(useOffset=False, useMathText=True)
g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
ax_flux.yaxis.set_minor_formatter(FuncFormatter(g))
ax_flux.axvspan(0.5, 1., facecolor='gray') #color over the lower energy that should not typically be used
ax_flux.axvspan(20., 100., facecolor='gray') #color over the higher energy that should not typically be used

if wavelength_axis_show ==1:
    ax_wl = ax_flux.twiny()
    ax_wl.set_xscale('log')
    tick_locations = np.array([0.6, 0.8, 1., 2, 4, 6, 8, 10, 20, 40, 60, 80, 100])
    #tick_locations = np.array([1, 10, 100])

    def tick_function(X):
        V = np.sqrt(81.81/X)
        return ["%.3f" % z for z in V]

    ax_wl.set_xticks(tick_locations)
    ax_wl.set_xlim(ax_flux.get_xlim())
    ax_wl.set_xticklabels(tick_function(tick_locations))
    ax_wl.set_xlabel(r"wavelength ($\AA$)")
    for label in ax_wl.xaxis.get_ticklabels():
        label.set_rotation(-45)

ax_flux.tick_params(axis='both', direction = 'inout', length = 20, which = 'major')
ax_flux.tick_params(axis='both', direction = 'inout', length = 12, which = 'minor')
ax_wl.tick_params(axis='both', direction = 'inout', length = 20, which = 'major')
ax_wl.tick_params(axis='both', direction = 'inout', length = 12, which = 'minor')

plt.savefig(file_prefix+'intensity-normed-to-peak.pdf', format = 'pdf')
plt.show()

#for idx,i in enumerate(intensity_list_0): print(i*vi_list_0[idx]/398696139.67)
#plt.close('all')