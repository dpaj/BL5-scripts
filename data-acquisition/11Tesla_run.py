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

title('11 Tesla Empty sample with BeamStop Ei=0.54 meV')
#mode('high_flux')
ei(0.54)
start()
waitPC(0.5)
stop()

energies=[1.55,3.32,6.59,12.0,25.0]
resettime()
for ii in energies:
    title('11 Tesla Empty sample with BeamStop Ei={0} meV'.format(ii))
    ei(ii)
    start()
    waitPC(0.5)
    stop()

#simulate('11 Tesla')
submit('11 Tesla')

estimatetime()



