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





# Simple Scan to count Dark Current for 900s in a for loop
newscan()
resettime()
set_field("fitssm",1.0)
comment("Magnet_Test")
waitS(60.0)
set_field("fitssm",0.0)

simulate('Simulation')
#submit('Simulation')

estimatetime()






#number=-1
#with open("/home/bl-user/Script_Test/command.txt","w") as text_file: 
#   for cm in cmds: 
#     number+=1   
#     text_file.write("{}\n".format(cmds[number]))
