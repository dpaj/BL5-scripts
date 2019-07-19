#!/usr/bin/python

from epics import caget
from scan import *
import os
import sys
from operator import __truediv__
sys.path.append('/home/bl-user/Script_Test/')
from CNCS_scanfunction import *

print("##############################################################")
print("#                                                            #")
print("# Hello users from BL-5, CNCS is ready to collect your data. #")
print("#                                                            #")
print("##############################################################")

####################################################################################


# User scripting example below
newscan()
resettime()
print("Starting a new Scan.")
loadconf('Conf_BL5_HighRes.sav')
runexp('Prova Script', 12, 90, 'pc', 4.2)

estimatetime()

newscan()
#resettime()
print("Starting a new Scan.")
loadconf('Conf_BL5_AI.sav')
runexp('Prova Script', 12, 190, 'time', 3600)

estimatetime()

newscan()
#resettime()
print("Starting a new Scan.")
loadconf('Conf_BL5_HighRes.sav')
runexp('Prova Script', 12, 90, 'pc', 4.2)
loadconf('Conf_BL5_AI.sav')
runexp('Prova Script', 12, 190, 'time', 3600)

#submit('run test')
estimatetime()







