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

# Function to Change the phase
def phase_scan_array(center_phase):
    part1 = np.arange(center_phase-700,center_phase-200,100)
    part2 = np.arange(center_phase-200,center_phase+200,20)
    part3 = np.arange(center_phase+200,center_phase+700,100)
    
    all_together = np.concatenate([part1, part2, part3])
    return all_together


#define parameters
# Select range of energies and Proton Charge
energies=[1.0,1.55,3.32,6.59,12.0,25.0,45.0,80.0]
PC_list = [0.32, 0.16, 0.08, 0.12, 0.12, 0.52, 2.5, 4.5]
dd_chopper_mode_file = 'high_flux.sav'
dd_chopper_mode_shorthand = 'HF'

# Select a Chopper Configuration 
if dd_chopper_mode_shorthand == 'AI':
    caput('BL5:Chop:Skf1:SpeedReq', 60.0)
    caput('BL5:Chop:Skf2:SpeedReq', 60.0)
    caput('BL5:Chop:Skf3:SpeedReq', 60.0)
    caput('BL5:Chop:Skf4:SpeedReq', 240.0)
    caput('BL5:Chop:Skf5:SpeedReq', 240.0)
    caput('BL5:Chop:Skf45:DblDiskModeReq', 3, wait = True)
elif dd_chopper_mode_shorthand == 'HF':
    caput('BL5:Chop:Skf1:SpeedReq', 60.0)
    caput('BL5:Chop:Skf2:SpeedReq', 60.0)
    caput('BL5:Chop:Skf3:SpeedReq', 60.0)
    caput('BL5:Chop:Skf4:SpeedReq', 300.0)
    caput('BL5:Chop:Skf5:SpeedReq', 300.0)
    caput('BL5:Chop:Skf45:DblDiskModeReq', 1, wait = True)
elif dd_chopper_mode_shorthand == 'HR':
    caput('BL5:Chop:Skf1:SpeedReq', 60.0)
    caput('BL5:Chop:Skf2:SpeedReq', 60.0)
    caput('BL5:Chop:Skf3:SpeedReq', 60.0)
    caput('BL5:Chop:Skf4:SpeedReq', 180.0)
    caput('BL5:Chop:Skf5:SpeedReq', 180.0)
    caput('BL5:Chop:Skf45:DblDiskModeReq', 0, wait = True)
else:
    exit()

#for now, put the choppers in Energy Phase Entry Mode
caput('BL5:Chop:Skf1:PhaseEntryMode', 1)
caput('BL5:Chop:Skf2:PhaseEntryMode', 1)
caput('BL5:Chop:Skf3:PhaseEntryMode', 1)
caput('BL5:Chop:Skf4:PhaseEntryMode', 1)
caput('BL5:Chop:Skf5:PhaseEntryMode', 1)

##populate the lists that are the centered phases of the choppers at different energies
print("first run some channel access commands to get the approximate phase centers for the choppers at the energies desired")
chp1_phase_us_list = []
chp2_phase_us_list = []
chp3_phase_us_list = []
chp4_phase_us_list = []
chp5_phase_us_list = []
caput('BL5:Chop:Gbl:EnergyReq', 1.137, wait = True) #set to an energy different than 1 meV to avoid inheriting bad phase values
for en_idx, en in enumerate(energies):
    print('requesting energy = ', en)
    caput('BL5:Chop:Gbl:EnergyReq', en, wait = True)
    print('current energy = ', caget('BL5:Chop:Gbl:EnergyReq'))
    print('getting chopper phases...')
    chp1_phase_us = caget('BL5:Chop:Skf1:PhaseTimeDelaySet')
    chp2_phase_us = caget('BL5:Chop:Skf2:PhaseTimeDelaySet')
    chp3_phase_us = caget('BL5:Chop:Skf3:PhaseTimeDelaySet')
    chp4_phase_us = caget('BL5:Chop:Skf4:PhaseTimeDelaySet')
    chp5_phase_us = caget('BL5:Chop:Skf5:PhaseTimeDelaySet')
    print('BL5:Chop:Skf1:PhaseTimeDelaySet', chp1_phase_us)
    print('BL5:Chop:Skf2:PhaseTimeDelaySet', chp2_phase_us)
    print('BL5:Chop:Skf3:PhaseTimeDelaySet', chp3_phase_us)
    print('BL5:Chop:Skf4:PhaseTimeDelaySet', chp4_phase_us)
    print('BL5:Chop:Skf5:PhaseTimeDelaySet', chp5_phase_us)
    chp1_phase_us_list.append(chp1_phase_us)
    chp2_phase_us_list.append(chp2_phase_us)
    chp3_phase_us_list.append(chp3_phase_us)
    chp4_phase_us_list.append(chp4_phase_us)
    chp5_phase_us_list.append(chp5_phase_us)

print(chp1_phase_us_list)
print(chp2_phase_us_list)
print(chp3_phase_us_list)
print(chp4_phase_us_list)
print(chp5_phase_us_list)

### now change back to choppers in TotalDelay Phase Entry Mode
caput('BL5:Chop:Skf1:PhaseEntryMode', 3)
caput('BL5:Chop:Skf2:PhaseEntryMode', 3)
caput('BL5:Chop:Skf3:PhaseEntryMode', 3)
caput('BL5:Chop:Skf4:PhaseEntryMode', 3)
caput('BL5:Chop:Skf5:PhaseEntryMode', 3, wait = True)


newscan()
resettime()

# Select a Chopper Configuration 
loadconf(dd_chopper_mode_file)

for en_idx, en in enumerate(energies):
   Change_phase_entry(1)
   ei(en)
   thisPC = PC_list[en_idx]
   title(dd_chopper_mode_shorthand+" Test for Tzero at E={0} meV".format(en))
   comment(dd_chopper_mode_shorthand+' {} meV, emission table scan'.format(en))
   #print('*************************************************')
   #print("Current Phase for SKF1= {0}".format(chp1_phase_us_list[en_idx]))
   #print("Current Phase for SKF2= {0}".format(chp2_phase_us_list[en_idx]))
   #print("Current Phase for SKF3= {0}".format(chp3_phase_us_list[en_idx]))
   #print("Current Phase for SKF4= {0}".format(chp4_phase_us_list[en_idx]))
   #print("Current Phase for SKF5= {0}".format(chp5_phase_us_list[en_idx]))
   #print('*************************************************')

   ar1 = phase_scan_array(chp1_phase_us_list[en_idx])
   ar2 = phase_scan_array(chp2_phase_us_list[en_idx])
   ar3 = phase_scan_array(chp3_phase_us_list[en_idx])
   ar4 = phase_scan_array(chp4_phase_us_list[en_idx])
   ar5 = phase_scan_array(chp5_phase_us_list[en_idx])
   
   Change_phase_entry(3)
   
   for idx in range(len(ar1)):
      #print(ar1[idx], ar2[idx], ar3[idx], ar4[idx], ar5[idx])
      start()
      New_total_delay(ar1[idx],ar2[idx],ar3[idx],ar4[idx],ar5[idx])
      delay(60)
      waitPC(thisPC)
      stop()

#to be safe, put the choppers back in Energy Phase Entry Mode
caput('BL5:Chop:Skf1:PhaseEntryMode', 1)
caput('BL5:Chop:Skf2:PhaseEntryMode', 1)
caput('BL5:Chop:Skf3:PhaseEntryMode', 1)
caput('BL5:Chop:Skf4:PhaseEntryMode', 1)
caput('BL5:Chop:Skf5:PhaseEntryMode', 1)
ei(12.0)

#simulate('Tzero scan HF')
submit('Tzero scan HF')

estimatetime()
