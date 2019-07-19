#!/usr/bin/python

from epics import caget
from scan import *
import os
import sys
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

energies=[0.54,1.55,3.32,5.1,6.59,12.0,25.0,50.0,80.0]
resettime()
loadconf("high_flux.sav")
for ii in energies:
    title('TiZr in Air High Flux Ei={0} meV'.format(ii))
    ei(ii)
    start()
    waitPC(1.0)
    stop()

loadconf("intermediate.sav")
for ii in energies:
    title('TiZr in Air Intermediate Ei={0} meV'.format(ii))
    ei(ii)
    start()
    waitPC(1.0)
    stop()

loadconf("high_res.sav")
for ii in energies:
    title('TiZr in Air High Resolution Ei={0} meV'.format(ii))
    ei(ii)
    start()
    waitPC(1.0)
    stop()

#simulate('Air')
submit('Air')

estimatetime()



