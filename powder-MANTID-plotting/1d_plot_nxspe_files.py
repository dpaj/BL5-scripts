from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
from mantid import plots
from matplotlib.colors import LogNorm


def change_permissions(filename,permission):
    try:
        os.chmod(filename,permission)
    except OSError:
        pass


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



    


data_directory = '/SNS/CNCS/IPTS-22122/shared/autoreduce/inelastic/'
data_directory = '/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/'

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
buckyball_80meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277508_Ei=80p0.nxspe',
    qmin = 1,
    qmax = 10,
    num_q_points = 1,
    Emin = -10,
    Emax = 75,
    num_E_points = 100,
    ))

#make a plot of some lines
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
ax.errorbar(buckyball_1meV_300K/0.105,'o-', label='T = 300 K, Ei = 1 meV')
ax.errorbar(buckyball_3p32meV_300K/0.788,'o-', label='T = 300 K, Ei = 3.32 meV')
ax.errorbar(buckyball_12meV_300K/0.980,'o-', label='T = 300 K, Ei = 12 meV')
ax.errorbar(buckyball_30meV_300K/0.240,'o-', label='T = 300 K, Ei = 30 meV')
ax.errorbar(buckyball_80meV_300K/0.057,'o-', label='T = 300 K, Ei = 80 meV')
ax.legend()
#ax.set_ylim(0,1e-2)
ax.set_title("C60: overplot energy scans of different Ei's")
ax.tick_params(axis='x', direction='in')
ax.tick_params(axis='y', direction='out')
ax.grid(True)
ax.set_yscale('log')

fig.show()

#plt.close('all')
