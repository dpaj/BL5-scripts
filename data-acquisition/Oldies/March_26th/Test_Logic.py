#!/usr/bin/python

from epics import caget
from scan import *
import os
import sys
from operator import __truediv__
sys.path.append('/home/bl-user/Script_Test/')
from CNCS_scanfunction_general import *

print("########################################################################")
print("#                                                                      #")
print("#         Hello from Bl-5, CNCS is ready to collect your data          #")
print("#                                                                      #")
print("########################################################################")

# Simple Scan to count one angle for 1 h in pc
newscan()
resettime()
loadconf('Conf_BL5_HighRes.sav')
runexp('Prova Script', 12, 90, 'pc', 4.2)

estimatetime()

# Simple Scan to count one angle for 1 h in s
newscan()
resettime()
loadconf('Conf_BL5_AI.sav')
runexp('Prova Script', 12, 190, 'time', 3600)

estimatetime()

# Two Different Scans total is 2 h
newscan()
resettime()
loadconf('Conf_BL5_HighRes.sav')
runexp('Prova Script', 12, 90, 'pc', 4.2)
loadconf('Conf_BL5_AI.sav')
runexp('Prova Script', 12, 190, 'time', 3600)

#submit('run test')
estimatetime()


#########################################################################


# Scan to rotate the sample and save info in the title
runs=range(0,90+1,2)
resettime()
#loadconf('Conf_BL5_HighRes.sav')
for ii in runs:
    newscan()
    runexp('Prova Script', 12, ii, 'pc', 0.5)

simulate('run test')
#submit('run test')
estimatetime()

