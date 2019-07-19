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

energies=[3.32,12.0]
temps=[10.0,250.0]

for temp in temps:
    set_temp('ccr10s1',temp)
    set_temp('ccr10s2',temp)
    for ii in energies:
        title('NiCrAl Pressure Cell T={0} K, Ei={1} meV'.format(temp,ii))
        ei(ii)
        start()
        waitPC(16.8)
        stop()

#simulate('Pressure')
submit('Pressure')

estimatetime()



