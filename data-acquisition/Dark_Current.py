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





# Simple Scan to count Dark Current for 3600s in a for loop
newscan()
runs=range(1,30,1)
resettime()
for ii in runs:
    title('Dark Current 03 May 2018 run_{0}'.format(ii))
    #drive('axis1',ii)
    start()
    waitS(3600)
    stop()

#simulate('Dark Current')
submit('Dark Current')

estimatetime()






#number=-1
#with open("/home/bl-user/Script_Test/command.txt","w") as text_file: 
#   for cm in cmds: 
#     number+=1   
#     text_file.write("{}\n".format(cmds[number]))
