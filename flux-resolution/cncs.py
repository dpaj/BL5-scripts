import sys
#sys.path.append('/opt/mantidnightly/bin/')
#from mantid.simpleapi import *
import matplotlib.pyplot as plt
#from mantid import plots
from matplotlib.colors import LogNorm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from matplotlib.ticker import FormatStrFormatter, FuncFormatter, ScalarFormatter
import scipy as sp
import scipy.interpolate


def log_interp1d(x, y, kind='linear'):
    log_x = np.log10(x)
    log_y = np.log10(y)
    lin_int = scipy.interpolate.interp1d(log_x, log_y, kind=kind)
    log_int = lambda z: np.power(10.0, lin_int(np.log10(z)))
    return log_int


#plt.close('all')

#os.chdir('/SNS/users/vdp/CNCS/2018B/')

speed_request_1, speed_request_3, speed_request_0 = 300, 240, 180

#Ei_list_1 = np.load('flux-resolution-Ei_list_1.npy', )
#Ei_list_3 = np.load('flux-resolution-Ei_list_3.npy', )
#Ei_list_0 = np.load('flux-resolution-Ei_list_0.npy', )

Ei_list_1 = np.array([ 81.74512   ,  36.33116444,  20.43628   ,  13.0792192 ,
         9.08279111,   6.67307102,   5.10907   ,   4.03679605,
         3.2698048 ,   2.70231802,   2.27069778,   1.93479574,
         1.66826776,   1.45324658,   1.2772675 ,   1.13142035,
         1.00919901,   0.9057631 ,   0.8174512 ,   0.74145234])
Ei_list_3 = np.array([ 81.74512   ,  36.33116444,  20.43628   ,  13.0792192 ,
         9.08279111,   6.67307102,   5.10907   ,   4.03679605,
         3.2698048 ,   2.70231802,   2.27069778,   1.93479574,
         1.66826776,   1.45324658,   1.2772675 ,   1.13142035,
         1.00919901,   0.9057631 ,   0.8174512 ,   0.74145234])
Ei_list_0 = np.array([ 81.74512   ,  36.33116444,  20.43628   ,  13.0792192 ,
         9.08279111,   6.67307102,   5.10907   ,   4.03679605,
         3.2698048 ,   2.70231802,   2.27069778,   1.93479574,
         1.66826776,   1.45324658,   1.2772675 ,   1.13142035,
         1.00919901,   0.9057631 ,   0.8174512 ,   0.74145234])

#fwhm_list_1 = np.load('flux-resolution-fwhm_list_1.npy', )
#fwhm_list_3 = np.load('flux-resolution-fwhm_list_3.npy', )
#fwhm_list_0 = np.load('flux-resolution-fwhm_list_0.npy', )

fwhm_list_1 = np.array([ 11.6298568 ,   3.30391352,   1.49875251,   0.7750223 ,
         0.45939386,   0.29392047,   0.20135992,   0.13999083,
         0.10482014,   0.08052093,   0.06166183,   0.05043774,
         0.04118733,   0.03293292,   0.02811838,   0.02386944,
         0.02017329,   0.01731349,   0.01504153,   0.01309776])
fwhm_list_3 = np.array([ 5.72237633,  1.82027035,  0.93902208,  0.51761669,  0.31507266,
        0.20998066,  0.14349269,  0.10568444,  0.0802249 ,  0.06010263,
        0.04858085,  0.03928043,  0.03171963,  0.02641805,  0.02209539,
        0.01881818,  0.01631665,  0.0136715 ,  0.01202215,  0.01098126])
fwhm_list_0 = np.array([ 3.583287  ,  1.19663914,  0.68370586,  0.43022958,  0.26476339,
        0.16828534,  0.11971238,  0.09284073,  0.06841243,  0.05204582,
        0.04349954,  0.03500421,  0.0287296 ,  0.02376795,  0.02031884,
        0.01786536,  0.01550203,  0.01265805,  0.01176094,  0.01081881])

#vi_list_1 = np.load('flux-resolution-vi_list_1.npy', )
#vi_list_3 = np.load('flux-resolution-vi_list_3.npy', )
#vi_list_0 = np.load('flux-resolution-vi_list_0.npy', )

vi_list_1 = np.array([ 3954.66496614,  2636.44331076,  1977.33248307,  1581.86598646,
        1318.22165538,  1129.90427604,   988.66624154,   878.81443692,
         790.93299323,   719.02999384,   659.11082769,   608.40999479,
         564.95213802,   527.28866215,   494.33312077,   465.2547019 ,
         439.40721846,   416.28052275,   395.46649661,   376.63475868])
vi_list_3 = np.array([ 3954.66496614,  2636.44331076,  1977.33248307,  1581.86598646,
        1318.22165538,  1129.90427604,   988.66624154,   878.81443692,
         790.93299323,   719.02999384,   659.11082769,   608.40999479,
         564.95213802,   527.28866215,   494.33312077,   465.2547019 ,
         439.40721846,   416.28052275,   395.46649661,   376.63475868])
vi_list_0 = np.array([ 3954.66496614,  2636.44331076,  1977.33248307,  1581.86598646,
        1318.22165538,  1129.90427604,   988.66624154,   878.81443692,
         790.93299323,   719.02999384,   659.11082769,   608.40999479,
         564.95213802,   527.28866215,   494.33312077,   465.2547019 ,
         439.40721846,   416.28052275,   395.46649661,   376.63475868])


#intensity_list_1 = np.load('flux-resolution-intensity_list_1.npy', )
#intensity_list_3 = np.load('flux-resolution-intensity_list_3.npy', )
#intensity_list_0 = np.load('flux-resolution-intensity_list_0.npy', )

intensity_list_1 = np.array([   5618.,   25693.,   96386.,  245578.,  302450.,  255444.,
        196420.,  376644.,  395523.,  347737.,  298550.,  254526.,
        213368.,  176994.,  144776.,  118833.,   97263.,   79196.,
         63504.,   51822.])
intensity_list_3 = np.array([   1944.,    8555.,   30784.,   78157.,   94749.,   78555.,
         61276.,  118000.,  123615.,  107914.,   93246.,   78355.,
         65694.,   54981.,   44856.,   37721.,   31388.,   25906.,
         21097.,   17313.])
intensity_list_0 = np.array([   445.,   1946.,   7337.,  17263.,  20555.,  16776.,  13262.,
        24892.,  25695.,  22437.,  19552.,  17188.,  14233.,  12138.,
         9723.,   8016.,   6585.,   5374.,   4544.,   3635.])
#print(repr(intensity_list_0))

my_interp_fwhm_1 = log_interp1d(list(reversed(Ei_list_1)), list(reversed(fwhm_list_1)))
my_interp_fwhm_3 = log_interp1d(list(reversed(Ei_list_3)), list(reversed(fwhm_list_3)))
my_interp_fwhm_0 = log_interp1d(list(reversed(Ei_list_0)), list(reversed(fwhm_list_0)))

my_interp_flux_1 = log_interp1d(list(reversed(Ei_list_1)), list(reversed(np.multiply(intensity_list_1, vi_list_1)/398696139.0)))
my_interp_flux_3 = log_interp1d(list(reversed(Ei_list_3)), list(reversed(np.multiply(intensity_list_3, vi_list_3)/398696139.0)))
my_interp_flux_0 = log_interp1d(list(reversed(Ei_list_0)), list(reversed(np.multiply(intensity_list_0, vi_list_0)/398696139.0)))

def displayFluxResPlots():
    plt.figure(figsize = [8,10])
    ax_resolution = plt.gca()
    plt.loglog(Ei_list_1, fwhm_list_1, 's', label = 'dd=1, speed='+str(speed_request_1)+" Hz")
    plt.loglog(Ei_list_3, fwhm_list_3, '^', label = 'dd=3, speed='+str(speed_request_3)+" Hz")
    plt.loglog(Ei_list_0, fwhm_list_0, 'x', label = 'dd=0, speed='+str(speed_request_0)+" Hz")

    plt.loglog(Ei_list_1, my_interp_fwhm_1(Ei_list_1), 'b-')
    plt.loglog(Ei_list_3, my_interp_fwhm_3(Ei_list_3), 'g-')
    plt.loglog(Ei_list_0, my_interp_fwhm_0(Ei_list_0), 'r-')

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
    #plt.show()


    #plt.figure(figsize = [8,10])
    #ax_flux = plt.gca()
    #plt.loglog(Ei_list_1, np.multiply(intensity_list_1, vi_list_1), 's-', label = 'dd=1, speed='+str(speed_request_1)+" Hz")
    #plt.loglog(Ei_list_3, np.multiply(intensity_list_3, vi_list_3), '^-', label = 'dd=3, speed='+str(speed_request_3)+" Hz")
    #plt.loglog(Ei_list_0, np.multiply(intensity_list_0, vi_list_0), 'x-', label = 'dd=0, speed='+str(speed_request_0)+" Hz")
    #plt.xlabel('E (meV)')
    #plt.ylabel('monitor counts times velocity')
    #plt.legend(loc = 'upper left')
    #plt.grid(b=True, which='major', color='y', linestyle='-')
    #plt.grid(b=True, which='minor', color='k', linestyle='-')

    #plt.tick_params(axis='y', which='minor')
    #ax_flux.yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
    #for label in ax_flux.yaxis.get_ticklabels('minor')[1::2]:
    #    label.set_visible(False)
    #for label in ax_flux.yaxis.get_ticklabels('minor')[0::2]:
    #    label.set_rotation(45)
    #for label in ax_flux.yaxis.get_ticklabels():
    #    label.set_rotation(45)
        
    #plt.tick_params(axis='x', which='minor')
    #ax_flux.xaxis.set_minor_formatter(FormatStrFormatter("%.1f"))
    #for label in ax_flux.xaxis.get_ticklabels('minor')[1::2]:
    #    label.set_visible(False)
    #for label in ax_flux.xaxis.get_ticklabels('minor')[0::2]:
    #    label.set_rotation(-45)
    #for label in ax_flux.xaxis.get_ticklabels():
    #    label.set_rotation(-45)

    #plt.xlim([0.7, 100.])
    #plt.ylim([1e6, 1e9])

    #f = ScalarFormatter(useOffset=False, useMathText=True)
    #g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
    #ax_flux.yaxis.set_minor_formatter(FuncFormatter(g))

    #plt.show()



    plt.figure(figsize = [8,10])
    ax_flux = plt.gca()
    plt.loglog(Ei_list_1, np.multiply(intensity_list_1, vi_list_1)/398696139.0, 's', label = 'dd=1, speed='+str(speed_request_1)+" Hz")
    plt.loglog(Ei_list_3, np.multiply(intensity_list_3, vi_list_3)/398696139.0, '^', label = 'dd=3, speed='+str(speed_request_3)+" Hz")
    plt.loglog(Ei_list_0, np.multiply(intensity_list_0, vi_list_0)/398696139.0, 'x', label = 'dd=0, speed='+str(speed_request_0)+" Hz")

    plt.loglog(Ei_list_1, my_interp_flux_1(Ei_list_1), 'b-')
    plt.loglog(Ei_list_3, my_interp_flux_3(Ei_list_3), 'g-')
    plt.loglog(Ei_list_0, my_interp_flux_0(Ei_list_0), 'r-')

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

def calcFluxRes(condition, Ei):
    if condition == 'HF':
        print(condition,'Ei='+str(Ei)+'meV','fwhm@E=0:',my_interp_fwhm_1(Ei), 'rel. flux:', my_interp_flux_1(Ei))
    if condition == 'AI':
        print(condition,'Ei='+str(Ei)+'meV','fwhm@E=0:',my_interp_fwhm_3(Ei), 'rel. flux:', my_interp_flux_3(Ei))
    if condition == 'HR':
        print(condition,'Ei='+str(Ei)+'meV','fwhm@E=0:',my_interp_fwhm_0(Ei), 'rel. flux:', my_interp_flux_0(Ei))



