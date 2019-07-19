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

title('Dummy run waiting for beam to Warm up')
ei(0.54)
start()
waitPC(6.0)
stop()

energies=[0.54,1.55,3.32,6.59,12.0,25.0,80.0]
resettime()
for ii in energies:
    title('Get Lost Tube in Ar, V-foil with BeamStop Ei={0} meV'.format(ii))
    #title('YIG with BeamStop Ei={0} meV'.format(ii))
    ei(ii)
    start()
    waitPC(1.0)
    stop()

#simulate('CCR10')
submit('CCR10')

estimatetime()



