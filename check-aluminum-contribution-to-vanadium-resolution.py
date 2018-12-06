import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


van = Load(Filename='/SNS/CNCS/IPTS-21088/shared/autoreduce/van_273992.nxs', OutputWorkspace='van')

data_folder = '/SNS/CNCS/IPTS-20360/nexus/'

runs_1 = range(274470,274470+7, 1) #vanadium sample

iteration = 0
for this_run in runs_1:
    filename = data_folder+'CNCS_{0}.nxs.h5'.format(this_run)
    raw = Load(Filename=filename, OutputWorkspace=str(runs_1[iteration]))
    iteration = iteration + 1
    #Ei, _FMP, _FMI, T0 = GetEi(raw)




iteration = 0
for this_run in runs_1:
    Ei, _FMP, _FMI, T0 = GetEi(str(runs_1[iteration]))
    DgsReduction(
                OutputWorkspace = str(runs_1[iteration]) + '_dgs',
                SampleInputWorkspace = str(runs_1[iteration]),
                SampleInputMonitorWorkspace = str(runs_1[iteration]),
                EnergyTransferRange = [-0.15*Ei, Ei/200., 0.9*Ei],
                SofPhiEIsDistribution = True, #this will keep the output data as a histogram
                CorrectKiKf = True,
                DetectorVanadiumInputWorkspace = van,
                UseProcessedDetVan = True,
                IncidentBeamNormalisation='ByCurrent',
                )
                
    ConvertToMD(InputWorkspace = str(runs_1[iteration]) + '_dgs', OutputWorkspace = str(runs_1[iteration]) + '_md', QDimensions = '|Q|', dEAnalysisMode = 'Direct')
    iteration = iteration + 1

iteration = 0
for this_run in runs_1:
    Ei, _FMP, _FMI, T0 = GetEi(str(runs_1[iteration]))
    tth_max = 140. * np.pi / 180.
    this_qmax = 4. * np.pi * np.sin(tth_max / 2.)  / (9 / np.sqrt(Ei))
    print(str(runs_1[iteration]), Ei, this_qmax)
    BinMD(
                InputWorkspace = str(runs_1[iteration]) + '_md',
                OutputWorkspace =  str(runs_1[iteration]) + '_slice',
                AxisAligned = True, 
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 100',
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.9*Ei)+', 50', 
                )

    BinMD(
                InputWorkspace = str(runs_1[iteration]) + '_md',
                OutputWorkspace =  str(runs_1[iteration]) + '_lineV',
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', 2.5, 1',
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.1*Ei)+', 30', 
                )
    BinMD(
                InputWorkspace = str(runs_1[iteration]) + '_md',
                OutputWorkspace =  str(runs_1[iteration]) + '_lineAll',
                AlignedDim0 = '|Q|, '+str(0.18+0.027*Ei)+', {0}, 1'.format(this_qmax),
                AlignedDim1 = 'DeltaE, '+str(-0.1*Ei)+', '+str(0.1*Ei)+', 30', 
                )
    iteration = iteration + 1

mtd.importAll()

#make a plot of a slice using the mantid projection
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
Ei, _FMP, _FMI, T0 = GetEi(_274476)
ax.set_title(str(Ei))
ax.plot(_274476_lineV, label = 'up to Q = 2.5 A-1')
ax.plot(_274476_lineAll, label = 'all Q')
ax.legend()
fig.show()

#make a plot of a slice using the mantid projection
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
Ei, _FMP, _FMI, T0 = GetEi(_274475)
ax.set_title(str(Ei))
ax.plot(_274475_lineV, label = 'up to Q = 2.5 A-1')
ax.plot(_274475_lineAll, label = 'all Q')
ax.legend()
fig.show()

#make a plot of a slice using the mantid projection
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
Ei, _FMP, _FMI, T0 = GetEi(_274474)
ax.set_title(str(Ei))
ax.plot(_274474_lineV, label = 'up to Q = 2.5 A-1')
ax.plot(_274474_lineAll, label = 'all Q')
ax.legend()
fig.show()

#make a plot of a slice using the mantid projection
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
Ei, _FMP, _FMI, T0 = GetEi(_274473)
ax.set_title(str(Ei))
ax.plot(_274473_lineV, label = 'up to Q = 2.5 A-1')
ax.plot(_274473_lineAll, label = 'all Q')
ax.legend()
fig.show()

#make a plot of a slice using the mantid projection
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
Ei, _FMP, _FMI, T0 = GetEi(_274472)
ax.set_title(str(Ei))
ax.plot(_274472_lineV, label = 'up to Q = 2.5 A-1')
ax.plot(_274472_lineAll, label = 'all Q')
ax.legend()
fig.show()

#plt.close('all')


E_274476_lineV, I_274476_lineV, dI_274476_lineV = mantid.plots.helperfunctions.get_md_data1d(_274476_lineV,mantid.plots.helperfunctions.get_normalization(_274476_lineV)[0])
E_274476_lineAll, I_274476_lineAll, dI_274476_lineAll = mantid.plots.helperfunctions.get_md_data1d(_274476_lineAll,mantid.plots.helperfunctions.get_normalization(_274476_lineAll)[0])

E_274475_lineV, I_274475_lineV, dI_274475_lineV = mantid.plots.helperfunctions.get_md_data1d(_274475_lineV,mantid.plots.helperfunctions.get_normalization(_274475_lineV)[0])
E_274475_lineAll, I_274475_lineAll, dI_274475_lineAll = mantid.plots.helperfunctions.get_md_data1d(_274475_lineAll,mantid.plots.helperfunctions.get_normalization(_274475_lineAll)[0])

E_274474_lineV, I_274474_lineV, dI_274474_lineV = mantid.plots.helperfunctions.get_md_data1d(_274474_lineV,mantid.plots.helperfunctions.get_normalization(_274474_lineV)[0])
E_274474_lineAll, I_274474_lineAll, dI_274474_lineAll = mantid.plots.helperfunctions.get_md_data1d(_274474_lineAll,mantid.plots.helperfunctions.get_normalization(_274474_lineAll)[0])

E_274473_lineV, I_274473_lineV, dI_274473_lineV = mantid.plots.helperfunctions.get_md_data1d(_274473_lineV,mantid.plots.helperfunctions.get_normalization(_274473_lineV)[0])
E_274473_lineAll, I_274473_lineAll, dI_274473_lineAll = mantid.plots.helperfunctions.get_md_data1d(_274473_lineAll,mantid.plots.helperfunctions.get_normalization(_274473_lineAll)[0])

E_274472_lineV, I_274472_lineV, dI_274472_lineV = mantid.plots.helperfunctions.get_md_data1d(_274472_lineV,mantid.plots.helperfunctions.get_normalization(_274472_lineV)[0])
E_274472_lineAll, I_274472_lineAll, dI_274472_lineAll = mantid.plots.helperfunctions.get_md_data1d(_274472_lineAll,mantid.plots.helperfunctions.get_normalization(_274472_lineAll)[0])

E_274471_lineV, I_274471_lineV, dI_274471_lineV = mantid.plots.helperfunctions.get_md_data1d(_274471_lineV,mantid.plots.helperfunctions.get_normalization(_274471_lineV)[0])
E_274471_lineAll, I_274471_lineAll, dI_274471_lineAll = mantid.plots.helperfunctions.get_md_data1d(_274471_lineAll,mantid.plots.helperfunctions.get_normalization(_274471_lineAll)[0])

E_274470_lineV, I_274470_lineV, dI_274470_lineV = mantid.plots.helperfunctions.get_md_data1d(_274470_lineV,mantid.plots.helperfunctions.get_normalization(_274470_lineV)[0])
E_274470_lineAll, I_274470_lineAll, dI_274470_lineAll = mantid.plots.helperfunctions.get_md_data1d(_274470_lineAll,mantid.plots.helperfunctions.get_normalization(_274470_lineAll)[0])

def gaussian(x, mu, sig, scale):
    return scale*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

popt_274476_lineV, pcov_274476_lineV = curve_fit(gaussian, E_274476_lineV, I_274476_lineV, p0 = (0.00, 0.025*GetEi(_274476)[0], np.max(I_274476_lineV)) )
popt_274475_lineV, pcov_274475_lineV = curve_fit(gaussian, E_274475_lineV, I_274475_lineV, p0 = (0.00, 0.025*GetEi(_274475)[0], np.max(I_274475_lineV)) )
popt_274474_lineV, pcov_274474_lineV = curve_fit(gaussian, E_274474_lineV, I_274474_lineV, p0 = (0.00, 0.025*GetEi(_274474)[0], np.max(I_274474_lineV)) )
popt_274473_lineV, pcov_274473_lineV = curve_fit(gaussian, E_274473_lineV, I_274473_lineV, p0 = (0.00, 0.025*GetEi(_274473)[0], np.max(I_274473_lineV)) )
popt_274472_lineV, pcov_274472_lineV = curve_fit(gaussian, E_274472_lineV, I_274472_lineV, p0 = (0.00, 0.025*GetEi(_274472)[0], np.max(I_274472_lineV)) )
popt_274471_lineV, pcov_274471_lineV = curve_fit(gaussian, E_274471_lineV, I_274471_lineV, p0 = (0.00, 0.025*GetEi(_274471)[0], np.max(I_274471_lineV)) )
popt_274470_lineV, pcov_274470_lineV = curve_fit(gaussian, E_274470_lineV, I_274470_lineV, p0 = (0.00, 0.025*GetEi(_274470)[0], np.max(I_274470_lineV)) )

popt_274476_lineAll, pcov_274476_lineAll = curve_fit(gaussian, E_274476_lineAll, I_274476_lineAll, p0 = (0.00, 0.025*GetEi(_274476)[0], np.max(I_274476_lineAll)) )
popt_274475_lineAll, pcov_274475_lineAll = curve_fit(gaussian, E_274475_lineAll, I_274475_lineAll, p0 = (0.00, 0.025*GetEi(_274475)[0], np.max(I_274475_lineAll)) )
popt_274474_lineAll, pcov_274474_lineAll = curve_fit(gaussian, E_274474_lineAll, I_274474_lineAll, p0 = (0.00, 0.025*GetEi(_274474)[0], np.max(I_274474_lineAll)) )
popt_274473_lineAll, pcov_274473_lineAll = curve_fit(gaussian, E_274473_lineAll, I_274473_lineAll, p0 = (0.00, 0.025*GetEi(_274473)[0], np.max(I_274473_lineAll)) )
popt_274472_lineAll, pcov_274472_lineAll = curve_fit(gaussian, E_274472_lineAll, I_274472_lineAll, p0 = (0.00, 0.025*GetEi(_274472)[0], np.max(I_274472_lineAll)) )
popt_274471_lineAll, pcov_274471_lineAll = curve_fit(gaussian, E_274471_lineAll, I_274471_lineAll, p0 = (0.00, 0.025*GetEi(_274471)[0], np.max(I_274471_lineAll)) )
popt_274470_lineAll, pcov_274470_lineAll = curve_fit(gaussian, E_274470_lineAll, I_274470_lineAll, p0 = (0.00, 0.025*GetEi(_274470)[0], np.max(I_274470_lineAll)) )

print(GetEi(_274476)[0], popt_274476_lineV[1], popt_274476_lineAll[1])
print(GetEi(_274475)[0], popt_274475_lineV[1], popt_274475_lineAll[1])
print(GetEi(_274474)[0], popt_274474_lineV[1], popt_274474_lineAll[1])
print(GetEi(_274473)[0], popt_274473_lineV[1], popt_274473_lineAll[1])
print(GetEi(_274472)[0], popt_274472_lineV[1], popt_274472_lineAll[1])
print(GetEi(_274471)[0], popt_274471_lineV[1], popt_274471_lineAll[1])
print(GetEi(_274470)[0], popt_274470_lineV[1], popt_274470_lineAll[1])

Ei_list = [GetEi(_274476)[0], GetEi(_274475)[0], GetEi(_274474)[0], GetEi(_274473)[0], GetEi(_274472)[0], GetEi(_274471)[0], GetEi(_274470)[0]]
V_list= [popt_274476_lineV[1], popt_274475_lineV[1], popt_274474_lineV[1], popt_274473_lineV[1], popt_274472_lineV[1], popt_274471_lineV[1], popt_274470_lineV[1]]
All_list = [popt_274476_lineAll[1], popt_274475_lineAll[1], popt_274474_lineAll[1], popt_274473_lineAll[1], popt_274472_lineAll[1], popt_274471_lineAll[1], popt_274470_lineAll[1]]

plt.figure()
plt.plot(Ei_list, V_list)
plt.plot(Ei_list, All_list)
plt.show()