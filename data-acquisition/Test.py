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

newscan()
resettime()

a=[1,2,3]

for ii in a:
  print("{0}".format(ii))

simulate('total scan')
#submit('sample3')

estimatetime()




