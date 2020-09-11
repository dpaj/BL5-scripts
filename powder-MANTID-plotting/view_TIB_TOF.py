import sys
sys.path.append('/opt/mantidnightly/bin')
from mantid.simpleapi import *
import matplotlib.pyplot as plt
from mantid import plots
import numpy as np

def plotTOFwithTIB(filename, T0_fitted = None):
    data=Load(Filename=filename)
    data=Rebin(InputWorkspace=data,Params='10')
    s=SumSpectra(InputWorkspace=data)

    Ei,_,_,T0=GetEi(InputWorkspace=data)
    if Ei <= 50:
        tib_min,tib_max=SuggestTibCNCS(Ei)
    else:
        tib_min, tib_max = 0,0

    TOF = s.readX(0)
    TOF = TOF[:-1] + (TOF[1]-TOF[0])
    I = s.readY(0)
    
    if T0_fitted == None:
        TOF = TOF + T0_fitted
    else:
        TOF = TOF + T0

    fig, ax = plt.subplots()
    ax.plot(TOF, I)
    ax.axvline(x=tib_min, color = 'red', label = 'suggested TIB min')
    ax.axvline(x=tib_max, color = 'red', label = 'suggested TIB max')
    ax.set_ylim([0,np.max(I)*1e-3])
    ax.set_title('Ei='+str(Ei)+', \n'+filename)
    ax.set_xlabel('TOF ($\mu$s)')
    ax.set_ylabel('Intensity')
    ax.legend()
    fig.show()

"""
plotTOFwithTIB('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277504.nxs.h5', T0_fitted = 209.414)
plotTOFwithTIB('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277505.nxs.h5', T0_fitted = 122.31)
plotTOFwithTIB('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277506.nxs.h5', T0_fitted = 72.385)
plotTOFwithTIB('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277507.nxs.h5', T0_fitted = 22.921)
"""
plotTOFwithTIB('/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/nexus/CNCS_277508.nxs.h5', T0_fitted = -44.971)

plotTOFwithTIB('/SNS/CNCS/IPTS-21441/nexus/CNCS_277990.nxs.h5', T0_fitted = -16.618688377213402)


#print(s.readY(0))

#plt.close('all')