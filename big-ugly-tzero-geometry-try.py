from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
from mantid import plots
from matplotlib.colors import LogNorm
import scipy.optimize as opt


def gaussian_s_b(x, mu, sig, scale, background):
    return background+scale*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def gaussian_s(x, mu, sig, scale):
    return scale*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def pulser(x, start, amplitude):
    stop = start + 200
    stretch = 0.02
    return amplitude*(x > start)*(x < stop)*np.exp(-stretch*(x-start))

van=LoadNexus(Filename='/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/van_277537.nxs')
MaskBTP(Workspace = 'van', Instrument = 'CNCS', Bank = '5-10')

#filename = '/SNS/CNCS/IPTS-20360/nexus/CNCS_274475.nxs.h5'

data_folder = '/SNS/CNCS/IPTS-20360/nexus/'
#condition 1
runs_1 = range(274470,274470+20, 1) #vanadium sample
#runs_1 = range(291503,291503+20, 1) #bismuth sample
#runs_1 = range(274470,274470+6, 1)

#condition 3
runs_3 = range(274470+20,274470+20+20, 1)

#condition 0
runs_0 = range(274470+20+20,274470+20+20+20, 1)


Ei_1_list = []
T0_1_chopper_list = []
T0_1_fitted_list = []
elastic_line_expected_list = []
prompt_pulse_1_list = []
T0_monitor_list = []
t_expected_monitor3_list = []
iteration = 0
fig, ax = plt.subplots()
for this_run in runs_1:
    iteration = iteration + 1
    filename = data_folder+'CNCS_{0}.nxs.h5'.format(this_run)

    raw = Load(Filename=filename, OutputWorkspace='raw')
    #LoadInstrument(raw,FileName='/SNS/CNCS/shared/geometry/CNCS_Definition_2018B2.xml', RewriteSpectraMap=False)
    raw_equator = CloneWorkspace('raw')
    MaskBTP(Workspace = 'raw_equator', Instrument = 'CNCS', Pixel = '1-63,65-128')
    
    instr = raw.getInstrument()
    source = instr.getSource()
    sample = instr.getSample()
    source_to_sample_distance_m = sample.getDistance(source)
    source_position = instr.getSource().getPos()
    sample_position = instr.getSample().getPos()
    L1 = np.linalg.norm(sample_position-source_position)
    print('L1', L1, 'source to sample', source_to_sample_distance_m)
    Ei, _FMP, _FMI, T0 = GetEi(raw)
    print('Ei', Ei)
    vi = 437.4*np.sqrt(Ei)

    L2_list = []
    bank_indices = range(1,51)
    for idx, chosen_bank in enumerate(bank_indices):
        bank=instr.getComponentByName("bank"+str(chosen_bank))[0]
        L2_list.append(bank.getDistance(sample))

    L2_ave = np.mean(L2_list)
    L1_plus_L2 = L1 + L2_ave
    D = L1_plus_L2
    print('source to detector', D)
    t_elastic_no_offset = D/vi*1e6

    microseconds_per_bin = 1
    TOF=Rebin(InputWorkspace=raw,Params=str(microseconds_per_bin))
    TOF_equator =Rebin(InputWorkspace=raw_equator,Params=str(microseconds_per_bin))
    s=SumSpectra(InputWorkspace=TOF)
    s_equator=SumSpectra(InputWorkspace=TOF_equator)

    TOF = s.readX(0)
    TOF = TOF[:-1] + (TOF[1]-TOF[0])/2.0
    I = s.readY(0)
    
    TOF_equator = s_equator.readX(0)
    TOF_equator = TOF_equator[:-1] + (TOF_equator[1]-TOF_equator[0])/2.0
    I_equator = s_equator.readY(0)

    #fit the elastic line in the detector in the equator
    initial_guess = (t_elastic_no_offset+T0, 5e-4*(t_elastic_no_offset+T0), np.max(I), 0 )
    popt, pcov = opt.curve_fit(gaussian_s_b, TOF_equator, I_equator, p0=initial_guess)
    popt_names = ['mu', 'sig', 'scale', 'background']
    print("****************")
    print("results of gaussian_s_b fit to elastic line in TOF")
    for idx, i in enumerate(popt):
        print(popt_names[idx], i)
    data_fitted = gaussian_s_b(TOF_equator, *popt)
    elastic_position_fitted = popt[0]
    T0_fitted = elastic_position_fitted - t_elastic_no_offset


    #fit the prompt pulse position
    sns_period = 1/60.*1e6
    if t_elastic_no_offset < sns_period*1.5:
        prompt_pulse_no_offset = sns_period*1
        print('***one', Ei, sns_period*1)
    elif t_elastic_no_offset < sns_period*2.5:
        prompt_pulse_no_offset = sns_period*2
        print('***two', Ei, sns_period*2)
    elif t_elastic_no_offset < sns_period*3.5:
        prompt_pulse_no_offset = sns_period*3
        print('***three', Ei, sns_period*3)
    elif t_elastic_no_offset < sns_period*4.5:
        prompt_pulse_no_offset = sns_period*4
        print('***four', Ei, sns_period*4)
    elif t_elastic_no_offset < sns_period*5.5:
        prompt_pulse_no_offset = sns_period*5
        print('***five', Ei, sns_period*5)
    elif t_elastic_no_offset < sns_period*6.5:
        prompt_pulse_no_offset = sns_period*6
        print('***six', Ei, sns_period*6)

    prompt_pulse_no_offset_index = int((prompt_pulse_no_offset - np.min(TOF)) / float(microseconds_per_bin))
    I_d = np.gradient(I)
    TOF_near_prompt_pulse = (TOF[prompt_pulse_no_offset_index-int(100./microseconds_per_bin):prompt_pulse_no_offset_index+100./microseconds_per_bin])
    I_d_near_prompt_pulse = (I_d[prompt_pulse_no_offset_index-int(100./microseconds_per_bin):prompt_pulse_no_offset_index+100./microseconds_per_bin])

    #fit the derivative of the prompt pulse
    #gaussian_s(x, mu, sig, scale)
    initial_guess = (TOF_near_prompt_pulse[np.argmax(I_d_near_prompt_pulse)], 2., 300.)
    popt, pcov = opt.curve_fit(gaussian_s, TOF_near_prompt_pulse, I_d_near_prompt_pulse, p0=initial_guess)
    popt_names = ['mu', 'sig', 'scale']
    print("****************")
    print("results of gaussian_s fit to prompt pulse derivative in TOF")
    for idx, i in enumerate(popt):
        print(popt_names[idx], i)

    prompt_pulse_in_frame = popt[0]
    prompt_pulse = prompt_pulse_in_frame - prompt_pulse_no_offset
    prompt_pulse_fitted = gaussian_s(TOF_near_prompt_pulse, *popt)

    #calculate the timing at monitor3
    monitor = LoadNexusMonitors(filename)
    monitor1_position = instr[2][0].getPos() #now defunct monitor that is directly in front of chopper 1, the fermi chopper, should be ~6.313 m from the source
    monitor2_position = instr[2][1].getPos() #monitor that is directly after chopper 2, the first bandwidth chopper, should be ~7.556 m from the source
    monitor3_position = instr[2][2].getPos() #monitor that is directly after choppers 4+5, the double disc choppers, should be ~34.836 m from the source
    
    source_to_monitor3 = np.linalg.norm(monitor3_position-source_position)
    t_expected_monitor3 = source_to_monitor3/vi * 1e6

    #time of flight for the monitors
    tofbin_monitor3_min = int(t_expected_monitor3*.95) 
    tofbin_monitor3_max = int(t_expected_monitor3*1.05)
    Rebin(InputWorkspace='monitor', OutputWorkspace='monitor', Params="%s,%s,%s" % (tofbin_monitor3_min, microseconds_per_bin, tofbin_monitor3_max))
    monitor = CropWorkspace(monitor, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)

    #extract the arrays associated with the time-of-flight spectrum for the monitor3
    monitor_tof = monitor.extractX()[0]
    monitor_intensity = monitor.extractY()[0]
    monitor_tof_centered = monitor_tof[:-1]-(monitor_tof[0]-monitor_tof[1])/2.

    #get the center-of-mass
    center_of_mass = np.dot(monitor_tof[:-1], monitor_intensity) / np.sum(monitor_intensity)
    T0_center_of_mass = center_of_mass - t_expected_monitor3

    average_intensity = np.sqrt(np.dot(monitor_tof[:-1], monitor_intensity**2) / np.sum(monitor_tof[:-1]))

    #get an initial guess for the fit by simply taking the maximum value of the peak
    monitor3_height_guess = np.max(monitor_intensity)
    print("monitor3_height_guess", monitor3_height_guess)
    monitor3_peakcenter_guess = monitor_tof[np.argmax(monitor_intensity)]
    print("monitor3_peakcenter_guess", monitor3_peakcenter_guess)
    monitor3_sigma_guess = 50
    print("monitor3_sigma_guess", monitor3_sigma_guess)


    #fit_result = Fit(Function='name=Gaussian,Height='+str(monitor3_height_guess)+',PeakCentre='+str(monitor3_peakcenter_guess)+',Sigma='+str(monitor3_sigma_guess), InputWorkspace=monitor, Output=monitor, OutputCompositeMembers=True)

    #def gaussian_s_b    mu, sig, scale, background
    initial_guess = (monitor3_peakcenter_guess, monitor3_sigma_guess, monitor3_height_guess, 1.)
    popt, pcov = opt.curve_fit(gaussian_s_b, monitor_tof_centered, monitor_intensity, p0=initial_guess)
    popt_names = ['mu', 'sig', 'scale', 'background']
    print("****************")
    print("results of gaussian_s_b fit to elastic line in TOF")
    for idx, i in enumerate(popt):
        print(popt_names[idx], i)
        print(initial_guess[idx])


    data_fitted = gaussian_s_b(monitor_tof_centered, *popt)

    print('figure of merit is sum(resids)/sum(data)', np.sum(np.abs(data_fitted - monitor_intensity)) /np.sum(np.abs(monitor_intensity)))


    monitor_3_fit_height = popt[2]
    monitor_3_fit_center = popt[0]
    monitor_3_fit_sigma = popt[1]

    print("monitor_3_fit_height", monitor_3_fit_height)
    print("monitor_3_fit_center", monitor_3_fit_center)
    print("monitor_3_fit_sigma", monitor_3_fit_sigma)

    T0_monitor = monitor_3_fit_center - t_expected_monitor3

    ###
            
    ax.set_xlabel('TOF ($\mu$s)')
    ax.set_ylabel('Intensity')
    ax.legend()
    Ei_1_list.append(Ei)
    T0_1_chopper_list.append(T0)
    T0_1_fitted_list.append(T0_fitted)
    elastic_line_expected_list.append(t_elastic_no_offset)
    prompt_pulse_1_list.append(prompt_pulse)
    T0_monitor_list.append(T0_monitor)
    t_expected_monitor3_list.append(t_expected_monitor3)
plt.show()

plt.figure()
Ei_1_list
T0_1_chopper_list
T0_1_fitted_list
plt.semilogx(Ei_1_list, prompt_pulse_1_list, 's-')
plt.xlabel('Ei (meV)')
plt.ylabel('prompt pulse timing offset from n*16666 micro-s (microseconds)')
plt.show()

### compare with the 
print(1000./106.25)
print(9.4)
for i in elastic_line_expected_list:
    print(i- i*9.4/9.41167)
plt.figure()
Ei_1_list
T0_1_chopper_list
T0_1_fitted_list
plt.plot(elastic_line_expected_list, prompt_pulse_1_list, 's-')
#plt.plot(elastic_line_expected_list, elastic_line_expected_list, 's-')
plt.xlabel('expected elastic line (microseconds)')
plt.ylabel('prompt pulse timing offset from n*16666 micro-s (microseconds)')
plt.show()

plt.figure()
plt.plot(Ei_1_list, np.subtract(T0_1_fitted_list, prompt_pulse_1_list), 's', label = 'detector elastic line T0')
plt.plot(Ei_1_list, T0_1_chopper_list, 'x', label = 'chopper-phase-peak-emission T0')
plt.plot(Ei_1_list, T0_monitor_list, 'x', label = 'monitor3 T0')
plt.xlabel('Ei (meV)')
plt.ylabel('T0 (microseconds)')
plt.legend()
plt.show()

plt.figure()
plt.plot(Ei_1_list, np.subtract(T0_1_chopper_list , T0_monitor_list), 'x', label = 'monitor3 T0 minus chopper T0')
plt.xlabel('Ei (meV)')
plt.ylabel('T0 (microseconds)')
plt.legend()
plt.show()

plt.figure()
plt.plot(Ei_1_list, np.subtract(T0_1_fitted_list, prompt_pulse_1_list)-T0_monitor_list, 's', label = 'detector elastic line T0 minus monitor T0')
plt.xlabel('Ei (meV)')
plt.ylabel('T0 (microseconds)')
plt.legend()
plt.show()

plt.figure()
plt.plot(Ei_1_list, np.divide(np.subtract(T0_1_fitted_list, prompt_pulse_1_list), T0_monitor_list), 's', label = 'detector elastic line T0 divided by monitor T0')
plt.xlabel('Ei (meV)')
plt.ylabel('T0 (microseconds)')
plt.legend()
plt.show()

Ei_ = 1.00
Ei_mod = Ei_*1.001
D_ = 39.7627958745+1.e-3
print(D)
vi_ = 437.4*np.sqrt(Ei_)
vi_mod = 437.4*np.sqrt(Ei_mod)
print(D_/vi_*1e6)
print(D/vi_*1e6)
print(D_/vi_*1e6-D/vi_*1e6)
print(D/vi_mod*1e6-D/vi_*1e6)


Ei_1_list
T0_1_chopper_list
T0_1_fitted_list
elastic_line_expected_list
prompt_pulse_1_list
T0_monitor_list
t_expected_monitor3_list
tmon = np.add(T0_monitor_list, t_expected_monitor3_list)
tdet = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list)+elastic_line_expected_list)

plt.figure()
plt.plot(Ei_1_list, np.divide(tdet, tmon), 's-')
plt.plot(Ei_1_list, np.ones(20)*D/source_to_monitor3)
plt.show()

plt.figure()
plt.plot(np.sqrt(Ei_1_list), tdet, 's-')
plt.plot(np.sqrt(Ei_1_list), tmon, 's-')
plt.show()

print(np.sqrt(2. * 1.6021766208e-22 / 1.674928e-27))
def avg_pen_calc(E):
    #for a given energy, return the length in meters that the neutrons penetrate to the detector
    L = 25.4 #mm
    wavelength = np.sqrt(81.81 / E)
    att = 20.921 /wavelength
    return np.array((att * np.exp(L/att) - L - att ) / (np.exp(L/att) - 1) *1e-3)

print(avg_pen_calc(1.0))

my_index = 4
E = Ei_1_list[my_index]
Dmon = source_to_monitor3
Ddet = D
#E = 0.75
v = 437.393295261 * np.sqrt(E)
tzero = T0_monitor_list[my_index]*1e-6
tzero = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))[my_index]*1e-6
print(tzero*1e6)
Tmon = Dmon/v + tzero
Tdet = (Ddet + 1.*avg_pen_calc(E))/v + tzero
print(E)
print(Tmon*1e6, Tdet*1e6)
print(tmon[my_index], tdet[my_index])


###oh boy, start trying to fit here
v = 437.393295261 * np.sqrt(np.array(Ei_1_list)*1.)
def attempt_to_fit_tzeros(x):
    Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19 = x
    E = np.array(Ei_1_list)*1.
    Dmon = Dmon_offset + source_to_monitor3*np.ones(20)
    Ddet = Ddet_offset + D*np.ones(20)+ 1.*avg_pen_calc(E)
    v = 437.393295261 * np.sqrt(E)
    #tzero = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6+5.0e-6
    tzero = np.array([t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19])
    Tmon = Dmon/v + tzero
    Tdet = (Ddet )/v + tzero
    mon_resids = Tmon*1e6-tmon
    det_resids = Tdet*1e6-tdet
    resids2 = np.sum(   mon_resids**2 + det_resids**2   )
    return resids2

t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19 = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6
Dmon_offset, Ddet_offset = 0.,0.
#print(attempt_to_fit_tzeros(Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19))

my_guess = [Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19]

my_fit = opt.fmin(attempt_to_fit_tzeros, x0 = my_guess, maxfun = 50000, maxiter = 50000)

print('Dmon_offset', my_fit[0])
print('Ddet_offset', my_fit[1])

print(1e6*my_fit[2:])

plt.figure()
print(np.shape((np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6))
plt.plot(v, 1e6*(np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6)
plt.plot(v, 1e6*my_fit[2:])
plt.xlabel('v (m/s)')
plt.ylabel('tzero (microseconds)')
plt.show()


plt.figure()
Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19 = my_fit
E = np.array(Ei_1_list)*1.
Dmon = Dmon_offset + source_to_monitor3*np.ones(20)
Ddet = Ddet_offset + D*np.ones(20)+ 1.*avg_pen_calc(E)
v = 437.393295261 * np.sqrt(E)
#tzero = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6+5.0e-6
tzero = np.array([t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19])
Tmon = Dmon/v + tzero
Tdet = (Ddet )/v + tzero

plt.plot(v, Tmon*1e6-tmon, '.-', label = 'residual of monitor timing')
plt.plot(v, Tdet*1e6-tdet, 'x-', label = 'residual of detector timing')
plt.ylabel('microseconds')
plt.xlabel('v$_i$ [m/s]')
plt.legend()
plt.show()

###oh boy, start trying to fit here INCLUDING ENERGY FITTING
def attempt_to_fit_tzeros_and_energy(x):
    Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, e00, e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19 = x
    E = np.array(Ei_1_list)*1. + np.array([e00, e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19])
    Dmon = Dmon_offset + source_to_monitor3*np.ones(20)
    Ddet = Ddet_offset + D*np.ones(20)+ 1.*avg_pen_calc(E)
    v = 437.393295261 * np.sqrt(E)
    #tzero = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6+5.0e-6
    tzero = np.array([t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19])
    Tmon = Dmon/v + tzero
    Tdet = (Ddet )/v + tzero
    mon_resids = Tmon*1e6-tmon
    det_resids = Tdet*1e6-tdet
    resids2 = np.sum(   mon_resids**2 + det_resids**2   ) #+ np.sum(np.gradient(E))
    print('resids2=',resids2)
    return resids2

t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19 = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6
e00, e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19 = np.zeros(20)
Dmon_offset, Ddet_offset = 0.,0.

my_guess = [Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, e00, e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19]

my_fit = opt.fmin(attempt_to_fit_tzeros_and_energy, x0 = my_guess, maxfun = 50000, maxiter = 50000)

print('Dmon_offset', my_fit[0])
print('Ddet_offset', my_fit[1])

actual_T0_from_chopper_emission = np.array([136.37, 101.34, 85.21, 67.24, 38.32, 12.08, -62.67])
actual_E_from_chopper_emission = np.array([1.00, 1.55, 3.32, 6.59, 12.0, 25.0, 80.0])

plt.figure()
plt.plot(E, (np.subtract(T0_1_fitted_list, prompt_pulse_1_list)), '.-', label = 'fit from only refining t0 detector elastic line')
plt.plot(E, my_fit[2:22]*1e6, '.-', label = "full fit of E, t0's, detector position, monitor position")
plt.plot(actual_E_from_chopper_emission, actual_T0_from_chopper_emission, '.-', label = 't0 from chopper phasing peak intensity')
plt.xlabel('E (meV)')
plt.ylabel('t0 (microseconds)')
plt.legend()
plt.show()

plt.figure()
plt.plot(E, my_fit[22:], '.-')
plt.title('')
plt.xlabel('E (meV)')
plt.ylabel('refined dE (meV)')
plt.show()

plt.figure()
Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, e00, e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19 = my_fit
E = np.array(Ei_1_list)*1. + np.array([e00, e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19])
Dmon = Dmon_offset + source_to_monitor3*np.ones(20)
Ddet = Ddet_offset + D*np.ones(20)+ 1.*avg_pen_calc(E)
v = 437.393295261 * np.sqrt(E)
#tzero = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6+5.0e-6
tzero = np.array([t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19])
Tmon = Dmon/v + tzero
Tdet = (Ddet )/v + tzero

plt.plot(v, Tmon*1e6-tmon, '.-', label = 'residual of monitor timing')
plt.plot(v, Tdet*1e6-tdet, 'x-', label = 'residual of detector timing')
plt.ylabel('microseconds')
plt.xlabel('v$_i$ [m/s]')
plt.legend()
plt.show()

###




###oh boy, start trying to fit here, weighting the detector to be more important than the monitor for fitting
def attempt_to_fit_tzeros(x):
    Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19 = x
    relative_weighting_factor = 10.
    E = np.array(Ei_1_list)*1.
    Dmon = Dmon_offset + source_to_monitor3*np.ones(20)
    Ddet = Ddet_offset + D*np.ones(20)+ 1.*avg_pen_calc(E)
    v = 437.393295261 * np.sqrt(E)
    #tzero = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6+5.0e-6
    tzero = np.array([t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19])
    Tmon = Dmon/v + tzero
    Tdet = (Ddet )/v + tzero
    mon_resids = Tmon*1e6-tmon
    det_resids = relative_weighting_factor*(Tdet*1e6-tdet)
    resids2 = np.sum(   mon_resids**2 + det_resids**2   )
    return resids2

t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19 = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6
Dmon_offset, Ddet_offset = 0.,0.
#print(attempt_to_fit_tzeros(Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19))

my_guess = [Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19]

my_fit = opt.fmin(attempt_to_fit_tzeros, x0 = my_guess)

print('Dmon_offset', my_fit[0])
print('Ddet_offset', my_fit[1])

plt.figure()
plt.plot(v, (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6)
plt.plot(v, my_fit[2:])
plt.show()


plt.figure()
Dmon_offset, Ddet_offset, t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19 = my_fit
E = np.array(Ei_1_list)*1.
Dmon = Dmon_offset + source_to_monitor3*np.ones(20)
Ddet = Ddet_offset + D*np.ones(20)+ 1.*avg_pen_calc(E)
v = 437.393295261 * np.sqrt(E)
#tzero = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6+5.0e-6
tzero = np.array([t00, t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19])
Tmon = Dmon/v + tzero
Tdet = (Ddet )/v + tzero

plt.plot(v, Tmon*1e6-tmon, '.-', label = 'residual of monitor timing')
plt.plot(v, Tdet*1e6-tdet, 'x-', label = 'residual of detector timing')
plt.ylabel('microseconds')
plt.xlabel('v$_i$ [m/s]')
plt.legend()
plt.show()

#how does error in timing affect the energy
time_from_v = np.divide(Ddet, v)*1e6
time_from_v_offset = time_from_v + 10.

v_from_time = np.divide(Ddet , (time_from_v*1e-6))
v_from_time_offset  = np.divide(Ddet , (time_from_v_offset *1e-6))

e_from_v = v_from_time**2 / (437.393295261)**2
e_from_v_offset = v_from_time_offset**2 / (437.393295261)**2

e_diffs = e_from_v-e_from_v_offset

plt.figure()
plt.loglog(e_from_v, e_diffs)
plt.xlabel('E (meV)')
plt.ylabel('dE (meV)')
plt.title('effect of 10 microseconds offset on elastic position')
plt.xlim([0.7, 80.])
plt.show()

"""
plt.figure()
for dmon_scaler in [1.0001, 1., .9999, .9998]:
    E = np.array(Ei_1_list)*1.
    Dmon = 15e-3 + dmon_scaler*source_to_monitor3*np.ones(20)
    Ddet = 20e-3 + D*np.ones(20)+ 1.*avg_pen_calc(E)
    print(Ddet)
    #E = 0.75
    v = 437.393295261 * np.sqrt(E)
    tzero = np.array(T0_monitor_list)*1e-6
    tzero = (np.subtract(T0_1_fitted_list, prompt_pulse_1_list))*1e-6+5.0e-6
    print(tzero*1e6)
    Tmon = Dmon/v + tzero
    Tdet = (Ddet )/v + tzero
    print(E)
    print(Tmon*1e6, Tdet*1e6)
    print(tmon, tdet)


    plt.plot(v, Tmon*1e6-tmon, '.-', label = 'residual of monitor timing')
    plt.plot(v, Tdet*1e6-tdet, 'x-', label = 'residual of detector timing')
plt.ylabel('microseconds')
plt.xlabel('v$_i$ [m/s]')
plt.legend()
plt.show()
"""