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
runs_1 = range(274470,274470+20, 1)
#runs_1 = range(274470,274470+6, 1)

#condition 3
runs_3 = range(274470+20,274470+20+20, 1)

#condition 0
runs_0 = range(274470+20+20,274470+20+20+20, 1)


Ei_1_list = []
T0_1_chopper_list = []
T0_1_fitted_list = []
prompt_pulse_1_list = []
iteration = 0
fig, ax = plt.subplots()
for this_run in runs_1:
    iteration = iteration + 1
    filename = data_folder+'CNCS_{0}.nxs.h5'.format(this_run) # 36.3311644444 meV

    raw = Load(Filename=filename, OutputWorkspace='raw')
    #LoadInstrument(raw,FileName='/SNS/CNCS/shared/geometry/CNCS_Definition_2018B2.xml', RewriteSpectraMap=False)
    #MaskBTP(Workspace = 'raw', Instrument = 'CNCS', Pixel = '1-63,65-128')
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
    s=SumSpectra(InputWorkspace=TOF)


    TOF = s.readX(0)
    TOF = TOF[:-1] + (TOF[1]-TOF[0])/2.0
    I = s.readY(0)

    for this_I in I:
        if np.abs(400. - this_I) < 5:
            print(this_I)

    #fit the elastic line in the detector
    initial_guess = (t_elastic_no_offset+T0, 5e-4*(t_elastic_no_offset+T0), np.max(I), 0 )
    popt, pcov = opt.curve_fit(gaussian_s_b, TOF, I, p0=initial_guess)
    popt_names = ['mu', 'sig', 'scale', 'background']
    print("****************")
    print("results of gaussian_s_b fit to elastic line in TOF")
    for idx, i in enumerate(popt):
        print(popt_names[idx], i)

    data_fitted = gaussian_s_b(TOF, *popt)

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
        
    #pulser(x, start, amplitude, stretch)    
    initial_guess = (prompt_pulse_no_offset, 400.)
    popt, pcov = opt.curve_fit(pulser, TOF, I, p0=initial_guess)
    popt_names = ['start', 'amplitude']#, 'stretch']
    print("****************")
    print("results of prompt pulse fit")
    for idx, i in enumerate(popt):
        print(popt_names[idx], i) 
    
    prompt_data_fitted = pulser(TOF, *popt)
    
    prompt_pulse = popt[0]
    ax.plot(TOF, I+iteration*0, '.-', fillstyle='none', label = 'data '+str(Ei) +' meV')
    ax.plot(TOF, prompt_data_fitted)
    ax.axhline(y=400, color = 'black')
    #ax.plot(TOF, data_fitted, 'm-', label = 'gaussian_s_b fit')
    #ax.axvline(x=t_elastic_no_offset+T0, color = 'red', label = 'chopper T0='+str(T0))
    #ax.axvline(x=t_elastic_no_offset, color = 'green', label = 'T0 = 0')
    #ax.axvline(x=elastic_position_fitted, color = 'black', label = 'fitted T0='+str(T0_fitted))
    ##ax.set_xlim(t_elastic_no_offset*0.99, t_elastic_no_offset*1.01)
    #ax.set_title(filename)
    ax.set_xlabel('TOF ($\mu$s)')
    ax.set_ylabel('Intensity')
    ax.legend()
    Ei_1_list.append(Ei)
    T0_1_chopper_list.append(T0)
    T0_1_fitted_list.append(T0_fitted)
    prompt_pulse_1_list.append(prompt_pulse)
plt.show()

plt.figure()
Ei_1_list
T0_1_chopper_list
T0_1_fitted_list
leading_edge_list = [16665.-sns_period,
16658.8-sns_period,
16652.8-sns_period,
33333.6-sns_period*2,
33327.3-sns_period*2,
33320.1-sns_period*2,
33314.8-sns_period*2,
49995.4-sns_period*3,
49988.6-sns_period*3,
49983.0-sns_period*3,
66663.7-sns_period*4,
66657.5-sns_period*4,
66650.7-sns_period*4,
83332.2-sns_period*5,
83326.1-sns_period*5,
83319.6-sns_period*5,
83313.5-sns_period*5,
99993.9-sns_period*6,
99987.7-sns_period*6,
99981.6-sns_period*6]
plt.plot(Ei_1_list, leading_edge_list, '.-')
plt.xlabel('Ei (meV)')
plt.ylabel('prompt pulse timing offset from n*16666 micro-s (microseconds)')
plt.show()

print(np.shape(T0_1_fitted_list))
print(np.shape(leading_edge_list))

plt.figure()
plt.plot(Ei_1_list, np.subtract(T0_1_fitted_list, leading_edge_list), 's')
plt.show()

plt.figure()
I_d = np.gradient(I)
plt.plot(TOF, I)
plt.plot(TOF, I_d, '.-')
plt.show()

print(np.min(TOF))
print(prompt_pulse_no_offset)
print(float(microseconds_per_bin))
print(prompt_pulse_no_offset)
prompt_pulse_no_offset_index = int((prompt_pulse_no_offset - np.min(TOF)) / float(microseconds_per_bin))
print(np.max(TOF))
TOF_near_prompt_pulse = (TOF[prompt_pulse_no_offset_index-int(100./microseconds_per_bin):prompt_pulse_no_offset_index+100./microseconds_per_bin])
I_d_near_prompt_pulse = (I_d[prompt_pulse_no_offset_index-int(100./microseconds_per_bin):prompt_pulse_no_offset_index+100./microseconds_per_bin])

#fit the derivative of the prompt pulse
#gaussian_s(x, mu, sig, scale)
initial_guess = (TOF_near_prompt_pulse[np.argmax(I_d_near_prompt_pulse)], 2., 300.)
#print(np.max(I_d_near_prompt_pulse))
popt, pcov = opt.curve_fit(gaussian_s, TOF_near_prompt_pulse, I_d_near_prompt_pulse, p0=initial_guess)
popt_names = ['mu', 'sig', 'scale']
print("****************")
print("results of gaussian_s fit to prompt pulse derivative in TOF")
for idx, i in enumerate(popt):
    print(popt_names[idx], i)

data_fitted = gaussian_s(TOF_near_prompt_pulse, *popt)
plt.figure()
plt.plot(TOF_near_prompt_pulse, I_d_near_prompt_pulse, '.-')
plt.plot(TOF_near_prompt_pulse, data_fitted)
plt.show()
