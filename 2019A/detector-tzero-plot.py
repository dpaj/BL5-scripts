import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interp


run_cycle = '2019A'

HF_m3_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-m3-tzero-{1}.npy'.format('HF' ,run_cycle))
HF_ei_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-ei-tzero-{1}.npy'.format('HF',run_cycle))

AI_m3_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-m3-tzero-{1}.npy'.format('AI' ,run_cycle))
AI_ei_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-ei-tzero-{1}.npy'.format('AI',run_cycle))

HR_m3_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-m3-tzero-{1}.npy'.format('HR' ,run_cycle))
HR_ei_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-ei-tzero-{1}.npy'.format('HR',run_cycle))

HF_interp = interp.interp1d(HF_ei_tzero[::-1], HF_m3_tzero[::-1])
AI_interp = interp.interp1d(AI_ei_tzero[::-1], AI_m3_tzero[::-1])
HR_interp = interp.interp1d(HR_ei_tzero[::-1], HR_m3_tzero[::-1])

print(HF_ei_tzero)
print(HF_interp(1.5))

#exit()

plt.figure()
plt.plot(HF_ei_tzero  , HF_m3_tzero , '.-', label = 'HF')
plt.plot(AI_ei_tzero  , AI_m3_tzero , '.-', label = 'AI')
plt.plot(HR_ei_tzero  , HR_m3_tzero , '.-', label = 'HR')
plt.legend()
plt.xlabel('Ei (meV)')
plt.ylabel('t-zero from m3 (micro-seconds)')
plt.title(run_cycle)
plt.show()

