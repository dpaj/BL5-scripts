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


def powderNxspeToMD(filename=None, qmin = None, qmax = None, Emin = None, Emax = None, num_q_points = 50, num_E_points = 50):
    dgs = Load(Filename=filename, OutputWorkspace='dgs')
    run = dgs.getRun()
    run_keys = run.keys()
    Ei = run['Ei'].value
    Qmax = 1.1*2*np.pi/ (   (  9/np.sqrt(Ei)  ) /2./np.sin(120./2.*np.pi/180.)   ) 
    if qmin == None:
        qmin = 0
    if qmax == None:
        qmax = Qmax
    if Emin == None:
        Emin = -0.1*Ei
    if Emax == None:
        Emax = 0.9*Ei

    md = ConvertToMD(InputWorkspace='dgs', QDimensions='|Q|', OutputWorkspace='md')
    md_rebin = BinMD(
                InputWorkspace='md', 
                AlignedDim0='|Q|,'+str(qmin)+','+str(qmax)+','+str(num_q_points), 
                AlignedDim1='DeltaE,'+str(Emin)+','+str(Emax)+','+str(num_E_points), 
                OutputWorkspace='md_rebin')
    return md_rebin



    


data_directory = '/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/'
"""
buckyball_1meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277504_Ei=1p0.nxspe',
    qmin = 0.4,
    qmax = 1.0,
    num_q_points = 1,
    Emin = -0.5,
    Emax = 0.5,
    num_E_points = 100,
    ))
buckyball_3p32meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277505_Ei=3p32.nxspe',
    qmin = 0.5,
    qmax = 1.7,
    num_q_points = 1,
    Emin = -2,
    Emax = 2.5,
    num_E_points = 100,
    ))
buckyball_12meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277506_Ei=12p0.nxspe',
    qmin = 0.5,
    qmax = 3,
    num_q_points = 1,
    Emin = -10,
    Emax = 10,
    num_E_points = 100,
    ))
buckyball_30meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277507_Ei=30p0.nxspe',
    qmin = 0.5,
    qmax = 6,
    num_q_points = 1,
    Emin = -5,
    Emax = 25,
    num_E_points = 100,
    ))
"""
buckyball_80meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277508_Ei=80p0.nxspe',
    qmin = 1,
    qmax = 10,
    num_q_points = 1,
    Emin = -10,
    Emax = 75,
    num_E_points = 100,
    ))

#to access and plot the line arrays directly
E, I, dI = mantid.plots.helperfunctions.get_md_data1d(buckyball_80meV_300K,mantid.plots.helperfunctions.get_normalization(buckyball_80meV_300K)[0])
E = E[0:75]
I =I[0:75]
dI = dI[0:75]



def gaussian(x, mu1, sig1, scale1, mu2, scale2, mu3, scale3):
    return 0.00016+scale1*np.exp(-np.power(x - mu1, 2.) / (2 * np.power(sig1, 2.)))+np.abs(scale2)*np.exp(-np.power(x - mu2, 2.) / (2 * np.power(4, 2.)))+np.abs(scale3)*np.exp(-np.power(x - mu3, 2.) / (2 * np.power(4, 2.)))

initial_guess = (0.001, 4, 10,          12, 1e-2,              42, 1e-3, )
popt, pcov = opt.curve_fit(gaussian, E, I, sigma=dI, p0=initial_guess)
popt_names = ['mu1', 'sig1', 'scale1', 'mu2', 'scale2', 'mu3', 'scale3']
for idx, i in enumerate(popt):
    print(popt_names[idx], i)

data_fitted = gaussian(E, *popt)

fig, ax = plt.subplots()
ax.errorbar(E, I, yerr=dI, fmt='rs-', label='T = 0.3 K, Ei = 1.55 meV')
ax.plot(E, data_fitted)
ax.set_ylim(1e-5,1e-2)
ax.legend()
ax.set_yscale('log')
fig.show()
#plt.close('all')
