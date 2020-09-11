from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
from mantid import plots
from matplotlib.colors import LogNorm
from matplotlib.mlab import griddata

import scipy.optimize as opt


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

def plotNxspe(sqw=None, title = '', log_scale = True, vmin = 1e-5, vmax = 1):
    #2D plot
    fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
    if log_scale == True:
        c = ax.pcolormesh(sqw, norm=LogNorm(vmin = vmin, vmax = vmax))
    else:
        c = ax.pcolormesh(sqw, vmin = vmin, vmax = vmax)
    cbar=fig.colorbar(c)
    cbar.set_label('Intensity (arb. units)') #add text to colorbar
    ax.set_title(title)
    fig.show()

data_directory = '/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/'

buckyball_1meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277504_Ei=1p0.nxspe',
    qmin = 0.4,
    qmax = 1.0,
    num_q_points = 100,
    Emin = -0.5,
    Emax = 0.5,
    num_E_points = 100,
    ))
"""
buckyball_3p32meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277505_Ei=3p32.nxspe',
    qmin = 0.5,
    qmax = 1.7,
    num_q_points = 100,
    Emin = -2,
    Emax = 2.5,
    num_E_points = 100,
    ))
buckyball_12meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277506_Ei=12p0.nxspe',
    qmin = 0.5,
    qmax = 3,
    num_q_points = 100,
    Emin = -10,
    Emax = 10,
    num_E_points = 100,
    ))
buckyball_30meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277507_Ei=30p0.nxspe',
    qmin = 0.5,
    qmax = 6,
    num_q_points = 100,
    Emin = -5,
    Emax = 25,
    num_E_points = 100,
    ))
buckyball_80meV_300K = CloneMDWorkspace(powderNxspeToMD(data_directory+'CNCS_277508_Ei=80p0.nxspe',
    qmin = 1,
    qmax = 10,
    num_q_points = 100,
    Emin = -10,
    Emax = 75,
    num_E_points = 100,
    ))
"""


#to access and plot the slice arrays directly
Q_array = mantid.plots.helperfunctions.get_md_data2d_bin_centers(buckyball_1meV_300K,mantid.plots.helperfunctions.get_normalization(buckyball_1meV_300K)[0])[0]
E_array = mantid.plots.helperfunctions.get_md_data2d_bin_centers(buckyball_1meV_300K,mantid.plots.helperfunctions.get_normalization(buckyball_1meV_300K)[0])[1]
normalized_intensity = mantid.plots.helperfunctions.get_md_data2d_bin_centers(buckyball_1meV_300K,mantid.plots.helperfunctions.get_normalization(buckyball_1meV_300K)[0])[2]
Q_mesh, E_mesh = np.meshgrid(Q_array, E_array)

extent = (np.min(Q_array), np.max(Q_array), np.min(E_array), np.max(E_array))
fig, ax = plt.subplots()
cax = ax.imshow(normalized_intensity, origin = "lower", extent = extent, aspect='auto', interpolation='nearest', vmin=0.0, vmax=10)
cbar=fig.colorbar(cax)
ax.set_xlabel('|Q| ($\AA^{-1}$)')
ax.set_ylabel('$\Delta$E (meV)')
ax.set_title('Ei = 1 meV, data')
fig.show()

def twoD_Gaussian((x, y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    xo = float(xo)
    yo = float(yo)    
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                            + c*((y-yo)**2)))
    return g.ravel()
    
initial_guess = (3,0.74,0,0.1,0.1,0,1e-9)
popt, pcov = opt.curve_fit(twoD_Gaussian, (Q_mesh, E_mesh), normalized_intensity.ravel(), p0=initial_guess)
popt_names = ['amplitude', 'xo', 'yo', 'sigma_x', 'sigma_y', 'theta', 'offset']
for idx, i in enumerate(popt):
    print(popt_names[idx], i)

data_fitted = twoD_Gaussian((Q_mesh, E_mesh), *popt)

extent = (np.min(Q_array), np.max(Q_array), np.min(E_array), np.max(E_array))
fig, ax = plt.subplots()
cax = ax.imshow(data_fitted.reshape(np.shape(normalized_intensity)), origin = "lower", extent = extent, aspect='auto', interpolation='nearest', vmin=0.0, vmax=10)
cbar=fig.colorbar(cax)
ax.set_xlabel('|Q| ($\AA^{-1}$)')
ax.set_ylabel('$\Delta$E (meV)')
ax.set_title('Ei = 1 meV, fit Bragg peak')
fig.show()


#plt.close('all')