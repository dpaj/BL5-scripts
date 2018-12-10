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



# Simple Scan for CCR10
newscan()
resettime()


a=np.arange(1,10+1,0.5)
energies=81.74512/(a*a)
energies = np.array([16.5, 52, 100])

for ii in energies:
  title('V-foil HF, T=300 K, Ei={0} meV'.format(ii))
  ei(ii)
  start()
  waitPC(3.0)
  stop()
  
loadconf("intermediate.sav")
for ii in energies:
  title('V-foil AI, T=300 K, Ei={0} meV'.format(ii))
  ei(ii)
  start()
  waitPC(3.0)
  stop() 

loadconf("high_res.sav")
for ii in energies:
  title('V-foil HR, T=300 K, Ei={0} meV'.format(ii))
  ei(ii)
  start()
  waitPC(3.0)
  stop() 

#simulate('CCR10-Flux-Res-2c')
submit('CCR10-Flux-Res-2c')

estimatetime()
