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

energies=[3.32,1.55]

for ii in energies:
   title('V-foil white beam, Ei={0} meV  100 K'.format(ii))
   ei(ii)
   start()
   waitPC(15.0)
   stop()


energies2=[1.55,3.32,12.0,60]

loadconf('high_flux.sav')

for ii in energies2:
   title('V-foil HF, Ei={0} meV  100 K'.format(ii))
   ei(ii)
   start()
   waitPC(2.5)
   stop()
   
loadconf('killingleak.sav')

for ii in energies2:
   title('V-foil KL, Ei={0} meV  100 K'.format(ii))
   ei(ii)
   start()
   waitPC(2.5)
   stop()

#simulate('whitebeam')
submit('whitebeam')

estimatetime()