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
These 2020B data were taken on the ~1 mm thickness, 10 mm diameter, 63 mm tall vanadium inside of a aluminum holder
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

file_prefix = 'compare-2020B-2018B-'
file_prefix_1 = '2020B-HF-'
file_prefix_3 = '2018B-HF-'

Ei_list_1 = np.load(file_prefix_1+'Ei_list.npy')
Ei_list_3 = np.load(file_prefix_3+'Ei_list.npy')

fwhm_list_1 = np.load(file_prefix_1+'detector_FWHM_list.npy')
fwhm_list_3 = np.load(file_prefix_3+'detector_FWHM_list.npy')

intensity_list_1 = np.load(file_prefix_1+'monitor_normalized_intensity_perMW_list.npy')
intensity_list_3 = np.load(file_prefix_3+'monitor_normalized_intensity_perMW_list.npy')

speed_request_1 = np.mean(np.load(file_prefix_1+'DD_speed_list.npy'))
speed_request_3 = np.mean(np.load(file_prefix_3+'DD_speed_list.npy'))

DD_opening_1 = int(np.mean(np.load(file_prefix_1+'DD_opening_list.npy')))
DD_opening_3 = int(np.mean(np.load(file_prefix_3+'DD_opening_list.npy')))

dd_num_to_opening = {1:'HF', 3: 'AI', 0: 'HR'} #go from numbering system to the well known opening labels

legend_font = font_manager.FontProperties(family='monospace',
                                   weight='normal',
                                   style='normal', size=14)

plt.figure(figsize = [8,10])
ax_resolution = plt.gca()
plt.loglog(Ei_list_1, fwhm_list_1, 's-', label = '2020-B:dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_1], speed_request_1) )
plt.loglog(Ei_list_3, fwhm_list_3, '^-', label = '2018-B:dd-opening={0}, dd-freq={1} Hz'.format(dd_num_to_opening[DD_opening_3], speed_request_3) )
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
plt.savefig(file_prefix+'elastic-resolution.png', format = 'png')
plt.show()