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
#EmailAlert()


# Simple Scan to count 11 Tesla for loop
newscan()
resettime()

energies=[1.2,1.55,3.32,5.0,12.0,20.0,30.0,50.0,1.2,1.55,3.32]
resettime()
for ii in energies:
    title('YIG in Teflon NiCrAl-cell, Room Temp Ei={0} meV'.format(ii))
    ei(ii)
    start()
    waitPC(12.4)
    stop()

#simulate('Pressure')
submit('Pressure')

estimatetime()



