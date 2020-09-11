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


def powderNxspeToMD(filename=None):
    dgs = Load(Filename=filename, OutputWorkspace='dgs')
    run = dgs.getRun()
    run_keys = run.keys()
    Ei = run['Ei'].value
    Qmax = 1.1*2*np.pi/ (   (  9/np.sqrt(Ei)  ) /2./np.sin(120./2.*np.pi/180.)   ) 

    md = ConvertToMD(InputWorkspace='dgs', QDimensions='|Q|', OutputWorkspace='md')
    md_rebin = BinMD(
                InputWorkspace='md', 
                AlignedDim0='|Q|,0,'+str(Qmax)+',50', 
                AlignedDim1='DeltaE,-'+str(0.1*Ei)+','+str(Ei)+',50', 
                OutputWorkspace='md_rebin')
    return md_rebin


buckyball_1meV_300K = CloneMDWorkspace(powderNxspeToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/CNCS_277504_Ei=1p0.nxspe'))
buckyball_3p32meV_300K = CloneMDWorkspace(powderNxspeToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/CNCS_277505_Ei=3p32.nxspe'))
buckyball_12meV_300K = CloneMDWorkspace(powderNxspeToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/CNCS_277506_Ei=12p0.nxspe'))
buckyball_30meV_300K = CloneMDWorkspace(powderNxspeToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/CNCS_277507_Ei=30p0.nxspe'))
buckyball_80meV_300K = CloneMDWorkspace(powderNxspeToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/CNCS_277508_Ei=80p0.nxspe'))
buckyball_80meV_300K_noTIB = CloneMDWorkspace(powderNxspeToMD('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/CNCS_277508_Ei=80p0.nxspe'))

plotSlice(buckyball_1meV_300K, normalization = 2)
plotSlice(buckyball_3p32meV_300K, normalization = 2)
plotSlice(buckyball_12meV_300K, normalization = 2)
plotSlice(buckyball_30meV_300K, normalization = 2)
plotSlice(buckyball_80meV_300K, normalization = 2)
plotSlice(buckyball_80meV_300K_noTIB, normalization = 2)


#closeAllSliceViewers()