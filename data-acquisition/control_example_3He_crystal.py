try:
    from scantools.scripting import *
except:
    import sys
    sys.path.insert(0,'/SNS/CNCS/shared/BL5-scripts/data-acquisition/')
    from pajsimtools import *
import numpy as np
import os
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
current_file = path + ' --> ' + filename + "\n"

Tsorb = [5., 7., 8., 9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20.] #empirical list of sorb temperatures
T3He = [0.242, 0.275, 0.300, 0.320, 0.351, 0.369, 0.463, 0.534, 0.604, 0.665, 0.750, 0.887, 0.908, 0.982, 1.20] #empirical list of sample temperatures
Tmapper = interp1d(T3He, Tsorb) #interpolation for the mapping between Tsorb and T3He

Set("BL5:CS:IPTS", -1) #set to the IPTS
this_ITEMS = -1
Set("BL5:CS:ITEMS", this_ITEMS) # change the sample ID

ei_list = [1.55, 3.32] # list of energies to loop over

angles_list = np.arange(-180,180,0.5)

low_temperature_list = [0.25] #list of temperatures to loop over in 3He mode
high_temperature_list = [2.0] #list of temperatures to loop over in one-shot high-temp mode

time_to_wait_between_temp = 1200. #time in seconds to wait after temperature gets within tolerance

wait_pcharge_C = 0.2 #60 minutes, ~5.0 C

#operate in 3He mode
Set("BL5:SE:He3LS:SETP1", 3) #set the range of the loop-1 to be 3
Set("BL5:SE:He3LS:SETP2", 0) #set the range of the loop-2 to be 0
    
for this_temperature in low_temperature_list:
    Set("BL5:SE:He3LS:SETP_S1", Tmapper(this_temperature)) #set sorb temperature
    Delay(time_to_wait_between_temp)
    for idx, this_ei in enumerate(ei_list): # loop over Eis
        Set("Energy", this_ei)           #set Ei
        for this_angle in angles_list:  # corresponding num_repeats to Ei
            Set("BL5:SMS:Marker:NotesComment", "{0} {1} {2}".format(this_ITEMS, this_ei, this_temperature)) #no comment
            Run("Sr2Cu(Te0p5W0p5)O6, Ei={0}meV, T={1}K, w={2}deg".format(this_ei, this_temperature, this_angle), wait_pcharge_C=wait_pcharge_C) #run title, and 0.5 C is ~6 minutes

#change to one-shot high temp mode
Set("BL5:SE:He3LS:SETP1", 0) #set the range of the loop-1 to be 0
Set("BL5:SE:He3LS:SETP2", 3) #set the range of the loop-2 to be 3
Set("BL5:SE:He3LS:SETP_S1", 0) #set sorb temperature

Set("BL5:SE:He3LS:SETP_S2", 1.0) #take an intermediate step in temperature
Delay(time_to_wait_between_temp)

for this_temperature in high_temperature_list:
    Set("BL5:SE:He3LS:SETP_S2", this_temperature-0.5)
    Delay(time_to_wait_between_temp)
    Set("BL5:SE:He3LS:SETP_S2", this_temperature)
    Delay(time_to_wait_between_temp)
    for idx, this_ei in enumerate(ei_list): # loop over Eis
        Set("Energy", this_ei)           #set Ei
        for this_angle in angles_list:  # corresponding num_repeats to Ei
            Set("BL5:SMS:Marker:NotesComment", "{0} {1} {2}".format(this_ITEMS, this_ei, this_temperature)) #no comment
            Run("Sr2Cu(Te0p5W0p5)O6, Ei={0}meV, T={1}K, w={2}deg".format(this_ei, this_temperature, this_angle), wait_pcharge_C=wait_pcharge_C) #run title, and 0.5 C is ~6 minutes


if 1:
    Submit(current_file)
else:
    my_simulate = Simulate()
    for i in my_simulate['simulation'].split('\n'):
        print(i)

