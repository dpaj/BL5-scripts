#!/usr/bin/python

from epics import caget
from scan import *
import os
import sys
import numpy as np
from operator import __truediv__
sys.path.append('/home/bl-user/Script_Test/')
from CNCS_scanfunction_general_dict import *

print("########################################################################")
print("#                                                                      #")
print("#         Hello from Bl-5, CNCS is ready to collect your data          #")
print("#                                                                      #")
print("########################################################################")


newscan()
resettime()

#set this flag to "1" if you want to submit, otherwise set to "0" if you want to simulate
submit_flag = 1

if submit_flag:
    #for now, put the choppers in Energy Phase Entry Mode
    caput('BL5:Chop:Skf1:PhaseEntryMode', 1)
    caput('BL5:Chop:Skf2:PhaseEntryMode', 1)
    caput('BL5:Chop:Skf3:PhaseEntryMode', 1)
    caput('BL5:Chop:Skf4:PhaseEntryMode', 1)
    caput('BL5:Chop:Skf5:PhaseEntryMode', 1)
    caput('BL5:Chop:Skf1:SpeedReq', 60.0)
    caput('BL5:Chop:Skf2:SpeedReq', 60.0)
    caput('BL5:Chop:Skf3:SpeedReq', 60.0)
    caput('BL5:Chop:Skf4:SpeedReq', 60.0)
    caput('BL5:Chop:Skf5:SpeedReq', 60.0)
    caput('BL5:Chop:Skf45:DblDiskModeReq', 1, wait = True)



title('V-foil white beam, Ei={0} meV  300 K'.format(3.32))
ei(3.32)
start()
waitPC(15.0)
stop()

loadconf('high_flux.sav')

if submit_flag:
    submit('quasi white beam 3.32 meV, 15C, 3hrs')
else:
    simulate('quasi white beam 3.32 meV, 15C, 3hrs')

estimatetime()
