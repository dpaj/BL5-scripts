from epics import caget, caput, PV, camonitor, cainfo
from scan import *
from math import *
import numpy as np
from numpy import array
import Tkinter as tk
import os
import re
import sys
import shutil
import datetime
import smtplib
# import savevalue
sys.path.append('/home/controls/share/master/python/Util')
from Autosave import Autosave
from Spell_Checker import *
from Tkinter import *
from tkMessageBox import *

# Declare the Variables
cmds = []                                       # List of commands to execute, Order Matters !!!!
hystory = []                                    # Append the History of the commands to save a .txt file
client = ScanClient('bl5-dassrv1.sns.gov')      # Make sure it is the right address
pctotal = 0.0
timetotal = 0
this_name= os.path.basename(sys.argv[0])        

# Color List from https://gist.github.com/vratiu/9780109

class bcolors:
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[0;31m'
   FAIL = '\033[91m'
   ENDC = '\033[0m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'

#######################################################################################
##################### List of Common Functions to Manipulate CNCS #####################
#######################################################################################

def ei(Energy):
    '''
    This Function sets the Incident Energy of the beam (meV).
    param   Energy: Incident energy value.
    '''
    cmds.append(Set('BL5:Chop:Gbl:EnergyReq', Energy, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Set Incident Energy to {0} meV".format(Energy)))
    print(str(datetime.datetime.now()) + " ...Set Incident Energy to {0} meV".format(Energy))

def cmdei(Energy):
    '''
    This Function sets the Incident Energy of the beam (meV).
    param   Energy: Incident energy value.
    '''
    caput('BL5:Chop:Gbl:EnergyReq', Energy)
    caput('BL5:CS:LineLog:Add',"Set Incident Energy to {0} meV".format(Energy))
    print(str(datetime.datetime.now()) + " ...Set Incident Energy to {0} meV".format(Energy))

##

def title(title):
    '''
    This Function sets the title of the scan. Users have the possibility to add PV values such as Energy, Motor Position,
    Temperature and Field. Any other note can be added using the command comment.
    param   title: Title of the scan.
    '''
    cmds.append(Set('BL5:SMS:RunInfo:RunTitle', title))
    cmds.append(Set('BL5:CS:LineLog:Add',"Set Title: {0} ".format(title)))
    print(str(datetime.datetime.now()) + " ...Set Title: {0} ".format(title))

def cmdtitle(title):
    '''
    This Function sets the title of the scan. Users have the possibility to add PV values such as Energy, Motor Position,
    Temperature and Field. Any other note can be added using the command cmdcomment.
    param   title: Title of the scan.
    '''
    caput('BL5:SMS:RunInfo:RunTitle', title)
    caput('BL5:CS:LineLog:Add',"Set Title: {0} ".format(title))
    print(str(datetime.datetime.now()) + " ...Set Title: {0} ".format(title))

########## Choppers ##########

def Fermifreq(hz):
    '''
    This Function sets the Frequency of the Fermi Chopper (Hz).
    param   hz: Frequency of the Fermi Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf1:SpeedReq', hz, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Setting Fermi Chopper frequency to {0} Hz".format(hz)))
    print(str(datetime.datetime.now()) + " ...Setting Fermi Chopper frequency to {0} Hz, and wait for completion".format(hz))

def cmdFermifreq(hz):
    '''
    This Function sets the Frequency of the Fermi Chopper (Hz).
    param   hz: Frequency of the Fermi Chopper (Hz).
    '''
    caput('BL5:Chop:Skf1:SpeedReq', hz, wait=True)
    caput('BL5:CS:LineLog:Add',"Setting Fermi Chopper frequency to {0} Hz".format(hz))
    print(str(datetime.datetime.now()) + " ...Setting Fermi Chopper frequency to {0} Hz, and wait for completion".format(hz))

##

def Chop2freq(hz):
    '''
    This Function sets the Frequency of the second Chopper (Hz).
    param   hz: Frequency of the second Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf2:SpeedReq', hz, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Setting Chopper 2 frequency to {0} Hz".format(hz)))
    print(str(datetime.datetime.now()) + " ...Setting Chopper 2 frequency to {0} Hz, and wait for completion".format(hz))

def cmdChop2freq(hz):
    '''
    This Function sets the Frequency of the second Chopper (Hz).
    param   hz: Frequency of the second Chopper (Hz).
    '''
    caput('BL5:Chop:Skf2:SpeedReq', hz, wait=True)
    caput('BL5:CS:LineLog:Add',"Setting Chopper 2 frequency to {0} Hz".format(hz))
    print(str(datetime.datetime.now()) + " ...Setting Chopper 2 frequency to {0} Hz, and wait for completion".format(hz))

##

def Chop3freq(hz):
    '''
    This Function sets the Frequency of the third Chopper (Hz).
    param   hz: Frequency of the third Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf3:SpeedReq', hz, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Setting Chopper 3 frequency to {0} Hz".format(hz)))
    print(str(datetime.datetime.now()) + " ...Setting Chopper 3 frequency to {0} Hz, and wait for completion".format(hz))

def cmdChop3freq(hz):
    '''
    This Function sets the Frequency of the third Chopper (Hz).
    param   hz: Frequency of the third Chopper (Hz).
    '''
    caput('BL5:Chop:Skf3:SpeedReq', hz, wait=True)
    caput('BL5:CS:LineLog:Add',"Setting Chopper 3 frequency to {0} Hz".format(hz))
    print(str(datetime.datetime.now()) + " ...Setting Chopper 3 frequency to {0} Hz, and wait for completion".format(hz))

##

def Chop4freq(hz):
    '''
    This Function sets the Frequency of the first disk of the Double Disk Chopper (Hz).
    param   hz: Frequency of the first disk of the Double Disk Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf4:SpeedReq', hz, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Setting Chopper 4 frequency to {0} Hz".format(hz)))
    print(str(datetime.datetime.now()) + " ...Setting Chopper 4 frequency to {0} Hz, and wait for completion".format(hz))

def cmdChop4freq(hz):
    '''
    This Function sets the Frequency of the first disk of the Double Disk Chopper (Hz).
    param   hz: Frequency of the first disk of the Double Disk Chopper (Hz).
    '''
    caput('BL5:Chop:Skf4:SpeedReq', hz, wait=True)
    caput('BL5:CS:LineLog:Add',"Setting Chopper 4 frequency to {0} Hz".format(hz))
    print(str(datetime.datetime.now()) + " ...Setting Chopper 4 frequency to {0} Hz, and wait for completion".format(hz))

##

def Chop5freq(hz):
    '''
    This Function sets the Frequency of the second disk of the Double Disk Chopper (Hz).
    param   hz: Frequency of the second disk of the Double Disk Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf5:SpeedReq', hz, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Setting Chopper 5 frequency to {0} Hz".format(hz)))
    print(str(datetime.datetime.now()) + " ...Setting Chopper 5 frequency to {0} Hz, and wait for completion".format(hz))

def cmdChop5freq(hz):
    '''
    This Function sets the Frequency of the second disk of the Double Disk Chopper (Hz).
    param   hz: Frequency of the second disk of the Double Disk Chopper (Hz).
    '''
    caput('BL5:Chop:Skf5:SpeedReq', hz, wait=True)
    caput('BL5:CS:LineLog:Add',"Setting Chopper 5 frequency to {0} Hz".format(hz))
    print(str(datetime.datetime.now()) + " ...Setting Chopper 5 frequency to {0} Hz, and wait for completion".format(hz))

# Need to check this command for adding delays
def delay(time):
    '''
    This function sets a delay (s) in the script. It can be used e.g. to
    thermalise the system or, more in general, to wait before executing a command.
    param   time: Value of the time-delay in seconds.
    '''
    global timetotal
    timetotal = timetotal + time
    print("...Delay {0} seconds".format(time))
    return cmds.append(Delay(time))

# Need to check this command to Reset the command line
def newscan():
    '''
    This function creates/splits the number of scan in the script. E.g.
    newscan()
    # command 1
    # command 2
    # command 3
    It will create a single scan containing 3 commands.
    newscan()
    # command 1
    newscan()
    # command 2
    newscan()
    # command 3
    It will create 3 scans containg 1 command.
    '''
    global cmds
    print("...Resetting cmds and history for a new scan.")
    cmds = []
    hystory = []

#######################################################################################
##################################### Motors Stage ####################################
#######################################################################################

def Vstick(value):
    '''
    This function drives the Vstick connected with Axis1. Please refer to local contact
    for more information.
    param   value:  Value of the position in mm.
    '''
    cmds.append(Set('BL5:Mot:Sample:Axis1', value, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Drive V-stick to {0} mm".format(value)))
    print(str(datetime.datetime.now()) + " ...Drive V-stick to {0} mm".format(value))

def cmdVstick(value):
    '''
    This function drives the Vstick connected with Axis1. Please refer to local contact
    for more information.
    param   value:  Value of the position in mm.
    '''
    print(str(datetime.datetime.now()) + " ...Drive V-stick to {0} mm".format(value))
    caput('BL5:Mot:Sample:Axis1', value, wait=True)
    caput('BL5:CS:LineLog:Add',"Drive V-stick to {0} mm".format(value))

##

def Axis1(value):
    '''
    This function drives the motor connected with Axis1. Please refer to local contact
    for more information.
    param   value:  Value of the angle in degree.
    '''
    cmds.append(Set('BL5:Mot:Sample:Axis1', value, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Drive Axis1 to {0} Degree".format(value)))
    print(str(datetime.datetime.now()) + " ...Drive Axis1 to {0} Degree".format(value))

def cmdAxis1(value):
    '''
    This function drives the motor connected with Axis1. Please refer to local contact
    for more information.
    param   value:  Value of the angle in degree.
    '''
    print(str(datetime.datetime.now()) + " ...Drive Axis1 to {0} Degree".format(value))
    caput('BL5:Mot:Sample:Axis1', value, wait=True)
    caput('BL5:CS:LineLog:Add',"Drive Axis1 to {0} Degree".format(value))

##

def Axis2(value):
    '''
    This function drives the motor connected with Axis2. Please refer to local contact
    for more information.
    param   value:  Value of the angle in degree.
    '''
    cmds.append(Set('BL5:Mot:Sample:Axis2', value, completion = True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Drive Axis2 to {0} Degree".format(value)))
    print(str(datetime.datetime.now()) + " ...Drive Axis2 to {0} Degree".format(value))

def cmdAxis2(value):
    '''
    This function drives the motor connected with Axis2. Please refer to local contact
    for more information.
    param   value:  Value of the angle in degree.
    '''
    print(str(datetime.datetime.now()) + " ...Drive Axis2 to {0} Degree".format(value))
    caput('BL5:Mot:Sample:Axis2', value, wait=True)
    caput('BL5:CS:LineLog:Add',"Drive Axis2 to {0} Degree".format(value))

##

def movesampleZ(value):
    '''
    This function lifts the sample Z axis in the laboratory coordinate system. Please refer to local contact
    for more information. Limits are from 150 mm to 310 mm
    param   value:  Value of the position of Sample Z (mm).
    '''
    cmds.append(Set('BL5:Mot:sampleZ', value, completion = True))
    hystory.append('BL5:Mot:sampleZ')
    print(str(datetime.datetime.now()) + " ...Move Sample Z to {0} mm".format(value))

def cmdmovesampleZ(value):
    '''
    This function lifts the sample Z axis in the laboratory coordinate system. Please refer to local contact
    for more information. Limits are from 150 mm to 310 mm
    param   value:  Value of the position of Sample Z (mm).
    '''
    print(str(datetime.datetime.now()) + " ...Move Sample Z to {0} mm".format(value))
    caput('BL5:Mot:sampleZ', value, wait=True)
    caput('BL5:CS:LineLog:Add',"Move Sample Z to {0} mm".format(value))

##

def movehuber(value):
    '''
    This function moves the huber rotation of the sample. Please refer to local contact
    for more information. 
    param   value:  Value of the angle in degree.
    '''
    cmds.append(Set('BL5:Mot:huber', value, completion = True))
    hystory.append('BL5:Mot:huber')
    print(str(datetime.datetime.now()) + " ...Move huber to {0} Degree".format(value))

def cmdmovehuber(value):
    '''
    This function moves the huber rotation of the sample. Please refer to local contact
    for more information. 
    param   value:  Value of the angle in degree.
    '''
    print(str(datetime.datetime.now()) + " ...Move huber to {0} Degree".format(value))
    caput('BL5:Mot:huber', value, wait=True)
    caput('BL5:CS:LineLog:Add',"Move huber to {0} Degree".format(value))

##

def beamstopL(pos):    
    '''
    This function moves the Left Beam Stop. Limits are -10 to +10 mm.
    param   pos:  Position of the Left beam stop in mm.
    '''
    cmds.append(Set('BL5:Mot:beamstopL', pos, completion = True))
    hystory.append('BL5:Mot:beamstopL')
    print(str(datetime.datetime.now()) + " ...Set Beamstop Left : {0} mm".format(pos))

def cmdbeamstopL(pos):
    '''
    This function moves the Left Beam Stop. Limits are -10 to +10 mm.
    param   pos:  Position of the Left beam stop in mm.
    '''
    print(str(datetime.datetime.now()) + " ...Set Beamstop Left : {0} mm".format(pos))
    caput('BL5:Mot:beamstopL', pos, wait=True)
    caput('BL5:CS:LineLog:Add',"Set Beamstop Left : {0} mm".format(pos))

##

def beamstopR(pos):
    '''
    This function moves the Right Beam Stop. Limits are -10 to +10 mm.
    param   pos:  Position of the Right beam stop in mm.
    '''
    cmds.append(Set('BL5:Mot:beamstopR', pos, completion = True))
    hystory.append('BL5:Mot:beamstopR')
    print(str(datetime.datetime.now()) + " ...Set Beamstop Right : {0} mm".format(pos))

def cmdbeamstopR(pos):
    '''
    This function moves the Right Beam Stop. Limits are -10 to +10 mm.
    param   pos:  Position of the Right beam stop in mm.
    '''
    print(str(datetime.datetime.now()) + " ...Set Beamstop Right : {0} mm".format(pos))
    caput('BL5:Mot:beamstopR', pos, wait=True)
    caput('BL5:CS:LineLog:Add',"Set Beamstop Right : {0} mm".format(pos))

##############

def collimator(args):
    '''
    This function rotates or stop the radial collimator. 
    param   args: Type 'on' or 'start' to start the rotation of the collimator.
                  Type ''off' or 'stop' to stop the rotation of the collimator.
                  Any other argument will generate an error message.
    '''
    if args.lower() == 'on' or args.lower() == 'start' :
        caput('BL5:Mot:Colli:MotionMenu', 1)
        print("Rotate Radial Collimator")
    elif args.lower() == 'off' or args.lower() =='stop':
        caput('BL5:Mot:Colli:MotionMenu', 0)
        print("Stop Radial Collimator")
    else:
        raise Exception("Unknown arguments. (start, stop, on, off)")

#######################################################################################
############################## Sample Environment Stage ###############################
#######################################################################################

def set_temp(args, value, args2='none', value2=0.0, waitime=5):
    '''
    This function sets the Temperature (K) of a device. IT WAITS FOR THE TEMPERATURE
    TO REACH THE VALUE within tolerance, with a default timeout time of 5 hours.
    param   args:     Name of the device (cryo6, vticryo6, ccr10s1, ccr10s2, vtifitssm, fitssm)
    param   args2:    Name of the device (cryo6, vticryo6, ccr10s1, ccr10s2, vtifitssm, fitssm)
    param   value:    Value of the temperature in Kelvin.
    param   value2:   Value of the temperature in Kelvin.
    param   waitime:  Timeout for the current command (hours) i.e. once the timeout is reached the scan fails.
                      The default time is set to 5 hours, users can increase or decrease it according to their will.
    '''
    waitsecond=waitime*3600
    print("Waiting time to reach the desired temperature: {0} hours or {1} seconds".format(waitime,waitsecond))
    if args not in __Aliases_PVs.keys() or ((args2.lower() != 'none') and (args2 not in __Aliases_PVs.keys())):
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(args) + bcolors.ENDC)
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(args2) + bcolors.ENDC)
       SpellChk(args)
       SpellChk(args2)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    elif args2.lower() == 'none' and value2 == 0.0:
       temptol=caget(__Max_PVs[args])
       print(str(datetime.datetime.now()) + " ...Set {0} Temperature : {1} K".format(args,value))
       print("Tolerance for PV: +/-{0} K".format(temptol))
       cmds.append(Set(__Aliases_PVs[args], value, completion = True, readback=True, tolerance=temptol, timeout=waitsecond))
       cmds.append(Set('BL5:CS:LineLog:Add',"Setting {0} Temperature : {1} K".format(args,value)))
    else:
       temptol=caget(__Max_PVs[args])
       temptol2=caget(__Max_PVs[args2])
       print(str(datetime.datetime.now()) + " ...Set {0} Temperature : {1} K".format(args,value))
       print("Tolerance for PV: +/-{0} K".format(temptol))
       print(str(datetime.datetime.now()) + " ...Set {0} Temperature : {1} K".format(args2,value2))
       print("Tolerance for PV: +/-{0} K".format(temptol2))
       cmds.append(Set(__Aliases_PVs[args2], value2, completion = False, readback=True, tolerance=temptol2))
       cmds.append(Set(__Aliases_PVs[args], value, completion = True, readback=True, tolerance=temptol, timeout=waitsecond))
       cmds.append(Set('BL5:CS:LineLog:Add',"Setting {0} Temperature : {1} K".format(args,value)))
       cmds.append(Set('BL5:CS:LineLog:Add',"Setting {0} Temperature : {1} K".format(args2,value2)))


def cmdset_temp(args, value):
    '''
    This function sets the Temperature (K) of a device. IT DOES NOT WAIT FOR THE TEMPERATURE
    TO REACH THE VALUE.
    param   args:   Name of the device (cryo6, vticryo6, ccr10s1, ccr10s2, vtifitssm, fitssm)
    param   value:  Value of the temperature in Kelvin.
    '''
    if args not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(args) + bcolors.ENDC)
       SpellChk(args)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    else:
       caput(__Aliases_PVs[args], value)
       caput('BL5:CS:LineLog:Add',"Set {0} Temperature : {1} K".format(args,value))
       print(str(datetime.datetime.now()) + " ...Set {0} Temperature : {1} K".format(args,value))


def set_field(args,value,ramping='True'):
    '''
    This function the Magnetic Field (Tesla) of a device.
    param   args:        Name of the device (slimssm, fitssm, fatssm)
    param   value:       Value of the field in Tesla.
    param   ramping:     Set the mode for collecting data: True waits for the persistent field, 
                         False skip to the next command after 30.0 seconds. Default is True !!!
    '''
    currentfield=caget('BL5:SE:FitSam:PersistentField')
    finalfield=np.abs(currentfield - value)
    cmds.append(Set('BL5:SE:FitSam:FieldSP',value))
    cmds.append(Set('BL5:CS:LineLog:Add',"Setting the magnetic field at {0} Tesla".format(value)))
    cmds.append(Delay(8.0))
    cmds.append(Set('BL5:SE:FitSam:FieldSPExe',1, completion = True, readback=True))
    print("...Ramping from {0} Tesla, to {1} Tesla".format(currentfield,value))
    if ramping == 'True':
       if value <= 5.5:
          timefield= (value/0.1)*(value*0.8) + 270.0 + (currentfield/0.1)
          delay(timefield)
       elif value > 5.5 and value <= 7.0:
          timefield= (value/0.025)*(value*0.8) + 300.0 + (currentfield/0.025)
          delay(timefield)
       elif value > 7.0:
          timefield= (value/0.01)*(value*0.55)  
          delay(timefield)
    else:
       timefield= 30.0
       delay(timefield)
       print("Collecting data while ramping the current.")
    print("Waiting time = {0} seconds, or {1} minutes".format(timefield,timefield/60.0))   


#######################################################################################
############################### General Commands Stage ################################
#######################################################################################

#def submit(scantitle=os.path.basename(sys.argv[0])):
#    '''
#    This function submits a scan or an ensamble of scans in the script.
#    It does not require any parameters.
#    '''
#    print("...Submitting the scan : " + scantitle)
#    id = client.submit(cmds, scantitle)
#    print("...scan id = " + str(id))
#    newscan()  # after submission, reset the cmds list every time
    
def submit(scantitle=os.path.basename(sys.argv[0])):
    '''
    This function submits a scan or an ensamble of scans in the script.
    It does not require any parameters.
    '''
    if caget('PPS_BMLN:BL05:ShtrOpen') == 1.0:
       print("...Submitting the scan : " + scantitle)
       id = client.submit(cmds, scantitle)
       print("...scan id = " + str(id))
       newscan()  # after submission, reset the cmds list every time
    else:
       root=tk.Tk()
       root.withdraw()
       ckbeam=askokcancel("Warning","One or more Shutters are closed. Is it ok to continue ?")
       if ckbeam == True:
           print("...Submitting the scan : " + scantitle)
           id = client.submit(cmds, scantitle)
           print("...scan id = " + str(id))
           root.update()
           newscan()  # after submission, reset the cmds list every time
       else:
           print(bcolors.WARNING + bcolors.BOLD + "...Scan not submitted, check the Shutter status." + bcolors.ENDC)
           root.update()

def simulate(scantitle=os.path.basename(sys.argv[0])):
    '''
    This function simulates a scan or an ensamble of scans in the script.
    It does not require any parameters.
    '''
    print("\n")
    print("...Simulating the scan : " + scantitle)
    print("\n")
    number=-1
    simulation = client.simulate(cmds)
    for cmd in cmds:
       number+=1
       print("{}".format(cmds[number]))

# Need to check this PV
def start():
    '''
    This function starts a run and collects data that will be saved in the neXus folder.
    It does not require any parameters.
    '''
    return cmds.append(Set('BL5:CS:RunControl:Start', 1, completion = True))

# Need to check this PV
def stop():
    '''
    This function stops a run and saves data in the neXus folder.
    It does not require any parameters.
    '''
    return cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion = True))

# Need to check this PV
def startdiag():
    '''
    This function starts a diagnostic run without saving data.
    It does not require any parameters.
    '''
    return cmds.append(Set('BL5:Det:ADnED:Start', 1, completion = True))

# Need to check this PV
def stopdiag():
    '''
    This function stops a diagnostic run without saving data.
    It does not require any parameters.
    '''
    return cmds.append(Set('BL5:Det:ADnED:Stop', 1, completion = True))

def waitPC(value):
    '''
    This function waits for the proton charge (C) to increase to the desired value.
    param   value:  Value of the proton charge in Coulomb.
    '''
    global pctotal
    pctotal = pctotal + value
    return cmds.append(Wait('BL5:Det:PCharge:C', value, comparison='increase by'))

def waitS(value):
    '''
    This function waits for the time (s) to increase to the desired value.
    param   value:  Value of the waiting time in seconds.
    '''
    global timetotal
    timetotal = timetotal + value
    return cmds.append(Wait('BL5:CS:RunControl:RunTimer', value, comparison='increase by'))

def estimatetime():
    '''
    This function estimates the amount of time a scan takes to be completed.
    Based on the power of the beam users can check the estimated time converted in hours
    for their measurement. At present this function calculates the time for a beam power
    of 0.85 MW, 1.0 MW, 1.2 MW, 1.3 MW and 1.4 MW.
    It does not require any parameters.
    '''
    print ".Total PC = %.2f C" %(pctotal)
    print "..........= %.2f hours (%.1f min) at 1.4 MW \n..........= %.2f hours (%.1f min) at 1.3 MW \n..........= %.2f hours (%.1f min) at 1.2 MW \n..........= %.2f hours (%.1f min) at 1.0 MW \n..........= %.2f hours (%.1f min) at 0.85 MW"  % (pctotal/5.4, pctotal/5.4*60,pctotal/4.8, pctotal/4.8*60,pctotal/4.2, pctotal/4.2*60,pctotal/3.6, pctotal/3.6*60,pctotal/3.0,pctotal/3.0*60)
    print ".Other time = %.1f s = %.2f hours" %(timetotal, timetotal/3600)
    print "The total time for your experiment is the sum of the two quantities above." 

def resettime(): # reset time counter
    '''
    This function reset the time of the estimated time of the measurement to zero.
    It can be used e.g. to check the estimated time for single scans in the script.
    It does not require any parameters.
    '''
    global pctotal
    global timetotal
    pctotal = 0.0
    timetotal = 0

#############################################################################################################
#					   	                                                                                    #
#			                      Translation of the old HFIR command in SPICE	                		    #
#							                                                                                #
#############################################################################################################

# It should also save a .log file before changing the IPTS
def begin(ipts):
    '''
    This command begins a New Experiment by typing the specified IPTS.
    param   ipts:  New IPTS number of the current experiment.
    '''
    curripts=caget('BL5:CS:IPTS')
    #shutil.copy("/home/controls/var/log/dassrv1/linelog.log","/home/controls/var/tmp/scan/IPTS-{0}/LogBook_{0}_{1}.txt".format(curripts,str(datetime.date.today())))
    shutil.copy("/home/controls/var/log/dassrv1/linelog.log","/home/bl-user/Script_Test/DAS_Logs/LogBook_IPTS-{0}_{1}.txt".format(curripts,str(datetime.date.today())))
    print("Previous Log Book Saved in IPTS-{0}".format(curripts))
    caput('BL5:CS:IPTS',ipts)
    caput('BL5:CS:CrystalAlign:ResetAllButton', 1)
    caput('BL5:CS:LineLog:Clear',1) 
    caput('BL5:CS:LineLog:Add',"Starting IPTS-{0} on {1}".format(ipts,str(datetime.date.today()))) 
    print(str(datetime.datetime.now()) + " Begin IPTS-{0} ".format(ipts))

##

def savelog():
    '''
    This command save the current User Line Log in text format in the DAS_Logs folder.
    Notice that if the file already exists in the folder, it will be over-written.
    It does not require any parameters. 
    '''
    curripts=caget('BL5:CS:IPTS')
    shutil.copy("/home/controls/var/log/dassrv1/linelog.log","/home/bl-user/Script_Test/DAS_Logs/LogBook_IPTS-{0}_{1}.txt".format(curripts,str(datetime.date.today())))
    print("Current Log Book Saved.")

##

def comment(note):
    '''
    This command adds a note to the Experiment.
    param   note:  Comment to add in quotes.
    '''
    cmds.append(Set('BL5:SMS:Marker:NotesComment',note))
    hystory.append('BL5:SMS:Marker:NotesComment')
    print(str(datetime.datetime.now()) + " Comment: {0}".format(note))

def cmdcomment(note):
    '''
    This command adds a note to the Experiment.
    param   note:  Comment to add in quotes.
    '''
    caput('BL5:SMS:Marker:NotesComment',note)
    caput('BL5:CS:LineLog:Add',"Comment: {0}".format(note))
    print(str(datetime.datetime.now()) + " Comment: {0}".format(note))

##

def mode(args):
    '''
    This function changes the Chopeer Mode in: high_flux, high_res, intermediate.
    param  args: Chopper mode selected (e.g. 'high_flux', 'high_res', 'intermediate').
    '''
    if args not in __Mode_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n Chopper mode '{0}' not found !!!".format(args) + bcolors.ENDC)
       SpellChk(args)
       print("\n")
       raise RuntimeError("Not a valid Chopper Mode.")
    cmds.append(Set('BL5:Chop:Skf45:DblDiskModeReq', __Mode_PVs[args], completion=True))
    cmds.append(Set('BL5:CS:LineLog:Add',"Setting Chopper mode in: {0}".format(args)))
    print(str(datetime.datetime.now()) + " Setting Chopper mode in: {0}".format(args))

def cmdmode(args):
    '''
    This function changes the Chopeer Mode in: high_flux, high_res, intermediate.
    param  args: Chopper mode selected (e.g. 'high_flux', 'high_res', 'intermediate').
    '''
    if args not in __Mode_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n Chopper mode '{0}' not found !!!".format(args) + bcolors.ENDC)
       SpellChk(args)
       print("\n")
       raise RuntimeError("Not a valid Chopper Mode.")
    caput('BL5:Chop:Skf45:DblDiskModeReq',__Mode_PVs[args])
    caput('BL5:CS:LineLog:Add',"Setting Chopper mode in: {0}".format(args))
    print(str(datetime.datetime.now()) + " Setting Chopper mode in: {0}".format(args))

##

def lattice(a,b,c,alpha,beta,gamma):
    '''
    This command sets the Lattice Parameters of the Crystal.
    param   a,b,c:  		Lattice Size of the Unit Cell in Angstrom.
    param   alpha,beta,gamma:	Lattice Angles of the Unit Cell in Degree.
    '''
    caput('BL5:CS:CrystalAlign:a',a)
    caput('BL5:CS:CrystalAlign:b',b)
    caput('BL5:CS:CrystalAlign:c',c)
    caput('BL5:CS:CrystalAlign:alpha',alpha)
    caput('BL5:CS:CrystalAlign:beta',beta)
    caput('BL5:CS:CrystalAlign:gamma',gamma)
    caput('BL5:CS:LineLog:Add',"Setting: a={0} b={1} c={2} alpha={3} beta={4} gamma={5}".format(a,b,c,alpha,beta,gamma))
    print(str(datetime.datetime.now()) + " Setting: a={0} b={1} c={2} alpha={3} beta={4} gamma={5}".format(a,b,c,alpha,beta,gamma))

##

def Uvec(h,k,l):
    '''
    This command sets the Nominal u Vector of the Scattering Plane.
    param   h,k,l:   Value of the Reciprocal Lattice Indices.
    '''
    caput('BL5:CS:CrystalAlign:u0:h',h)
    caput('BL5:CS:CrystalAlign:u0:k',k)
    caput('BL5:CS:CrystalAlign:u0:l',l)
    caput('BL5:CS:LineLog:Add',"Setting U vec: h={0} k={1} l={2}".format(h,k,l))
    print(str(datetime.datetime.now()) + " Setting U vec: h={0} k={1} l={2}".format(h,k,l))

def Vvec(h,k,l):
    '''
    This command sets the Nominal v Vector of the Scattering Plane.
    param   h,k,l:   Value of the Reciprocal Lattice Indices.
    '''
    caput('BL5:CS:CrystalAlign:v0:h',h)
    caput('BL5:CS:CrystalAlign:v0:k',k)
    caput('BL5:CS:CrystalAlign:v0:l',l)
    caput('BL5:CS:LineLog:Add',"Setting V vec: h={0} k={1} l={2}".format(h,k,l))
    print(str(datetime.datetime.now()) + " Setting V vec: h={0} k={1} l={2}".format(h,k,l))
    
def SAngle(omega,chi=0.0,phi=0.0):
    '''
    This command sets the Sample Angles (Degree) in the Crystal Alignment tool. The
    convention used is the same as in most triple axis, and it can be viewed by 
    clicking on "Convention of Angles" button (Notice tha beam is along Z).
    param   omega:   Value of the omega angle along Y.
    param   chi:     Value of the chi angle along X (default is 0.0, no Tilt).
    param   phi:     Value of the phi angle along Z (default is 0.0, no Tilt).
    '''
    caput('BL5:CS:CrystalAlign:Sample:omega',omega)
    caput('BL5:CS:CrystalAlign:Sample:chi',chi)
    caput('BL5:CS:CrystalAlign:Sample:phi',phi)
    caput('BL5:CS:LineLog:Add',"Setting: Omega={0} Chi={1} Phi={2}".format(omega,chi,phi))
    print(str(datetime.datetime.now()) + " Setting: Omega={0} Chi={1} Phi={2}".format(omega,chi,phi))   
    

## Check that the value is connected to the right PV (It is Pos)

def com(pv, wait=True):
    '''
    This function drives a motor to the Center of Mass calculated from a scan, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more
                    general pv must be verified with the local contact.
    '''
    value=caget('BL5:CS:Fitting:Fit:Pos')
    if pv not in __Aliases_cmddict.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(pv) + bcolors.ENDC)
       SpellChk(pv)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    else:
       __Aliases_cmddict[pv](value)

## Find a way to get this peak from the Calculated Bragg peak list

def calc(h,k,l,En=0.0):
    '''
    This function calculates the position of a Bragg peak based on the current UB matrix, 
    and it provides the 3 rotational angles (Omega, Chi, Delta).
    param   h,k,l:   H,K,L values of the Bragg peak.
    param   En:      Incident energy used for the calculation. If nothing is specified, 
                     this function assumes the current energy as the requested one.
    '''
    HKL=np.array([h,k,l])
    UBv=caget('BL5:CS:CrystalAlign:UBMatrix',as_string=True)
    UBmatrix=eval(UBv)
    if En == 0.0:
       Ei=caget('BL5:Chop:Gbl:EnergyReq')
    elif En != 0.0:
       Ei=En
    ki=np.sqrt(Ei/2.0717)
    Q0=2.0*pi*np.dot(UBmatrix,HKL)
    ### Angle Calculation
    theta=np.arccos(1.0-(Q0.dot(Q0))/(2.0*ki**2))
    phi1=np.arcsin(-Q0[1]/(ki*np.sin(theta)))
    phi2=pi-phi1
    Qlab1=ki*np.array([-np.cos(phi1)*np.sin(theta),-np.sin(phi1)*np.sin(theta),1.0-np.cos(theta)])
    Qlab2=ki*np.array([-np.cos(phi2)*np.sin(theta),-np.sin(phi2)*np.sin(theta),1.0-np.cos(theta)])
    omega1=np.arctan2((Q0[2]*Qlab1[0]-Q0[0]*Qlab1[2]),(Q0[0]*Qlab1[0]+Q0[2]*Qlab1[2]))
    omega1=np.rad2deg(omega1)
    omega2=np.arctan2((Q0[2]*Qlab2[0]-Q0[0]*Qlab2[2]),(Q0[0]*Qlab2[0]+Q0[2]*Qlab2[2]))
    omega2=np.rad2deg(omega2)
    print("Bragg Peak Left:      Omega = {0}    2Theta = {1}     Phi = {2}".format(omega1,np.rad2deg(theta),np.rad2deg(phi1)))
    print("Bragg Peak Right:     Omega = {0}    2Theta = {1}     Phi = {2}".format(omega2,np.rad2deg(theta),np.rad2deg(phi2)))

##
    
def cmdbr(h,k,l,pv,scattering='left',wait=True):
    '''
    This function drives a motor to the (h,k,l) peak specified, the peak can be observed.
    either on the 'left' or 'right' side of the detector array.
    param   h,k,l:         Selected Miller Indices of the peak.
    param   pv:            Choose 'axis1' or 'axis2'.
    param   scattering:    Choose if you want the peak on left or right side of the detector bank (default is left).
    '''
    HKL=np.array([h,k,l])
    UBv=caget('BL5:CS:CrystalAlign:UBMatrix',as_string=True)
    UBmatrix=eval(UBv)
    Ei=caget('BL5:Chop:Gbl:EnergyReq')
    ki=np.sqrt(Ei/2.0717)
    Q0=2.0*pi*np.dot(UBmatrix,HKL)
    ### Angle Calculation
    theta=np.arccos(1.0-(Q0.dot(Q0))/(2.0*ki**2))
    phi1=np.arcsin(-Q0[1]/(ki*np.sin(theta)))
    phi2=pi-phi1
    Qlab1=ki*np.array([-np.cos(phi1)*np.sin(theta),-np.sin(phi1)*np.sin(theta),1.0-np.cos(theta)])
    Qlab2=ki*np.array([-np.cos(phi2)*np.sin(theta),-np.sin(phi2)*np.sin(theta),1.0-np.cos(theta)])
    omega1=np.arctan2((Q0[2]*Qlab1[0]-Q0[0]*Qlab1[2]),(Q0[0]*Qlab1[0]+Q0[2]*Qlab1[2]))
    omega1=np.rad2deg(omega1)
    omega2=np.arctan2((Q0[2]*Qlab2[0]-Q0[0]*Qlab2[2]),(Q0[0]*Qlab2[0]+Q0[2]*Qlab2[2]))
    omega2=np.rad2deg(omega2)
    if scattering.lower() == 'left':
       omega=omega1
       phi=np.rad2deg(phi1)
    else:
       omega=omega2
       phi=np.rad2deg(phi2)
    if pv not in __Aliases_cmddict.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(pv) + bcolors.ENDC)
       SpellChk(pv)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    elif omega < caget(__Min_PVs[pv]) or omega > caget(__Max_PVs[pv]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(pv,caget(__Min_PVs[pv]),caget(__Max_PVs[pv])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    else:
       __Aliases_cmddict[pv](omega)
       SROIxy(np.rad2deg(theta)-2.5,np.rad2deg(theta)+2.5,phi-5.0,phi+5.0)
       caput('BL5:CS:LineLog:Add',"Driving to: ({0},{1},{2}) at Omega={3}".format(h,k,l,omega))
       print("Bragg to h={0} k={1} l={2}".format(h,k,l))

############################# Drive Commands #############################

def drive(pv, value, completion=True):
    '''
    This function is a general command to drive a motor, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more
                    general pv must be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv not in __Aliases_dict.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(pv) + bcolors.ENDC)
       SpellChk(pv)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    elif value < caget(__Min_PVs[pv]) or value > caget(__Max_PVs[pv]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(pv,caget(__Min_PVs[pv]),caget(__Max_PVs[pv])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    else:
       __Aliases_dict[pv](value)

##

def cmddrive(pv, value):
    '''
    This function is a general command to drive a motor, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more 
                    general pv must be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv not in __Aliases_cmddict.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(pv) + bcolors.ENDC)
       SpellChk(pv)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    elif value < caget(__Min_PVs[pv]) or value > caget(__Max_PVs[pv]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(pv,caget(__Min_PVs[pv]),caget(__Max_PVs[pv])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    else:
       __Aliases_cmddict[pv](value)

##

def driverel(pv, value, completion=True):
    '''
    This function drives a motor from current position to the specified value, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more
                    general pv must be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv not in __Aliases_dict.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(pv) + bcolors.ENDC)
       SpellChk(pv)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    currentpos=caget(__Aliases_PVs[pv])
    if (currentpos+value) < caget(__Min_PVs[pv]) or (currentpos+value) > caget(__Max_PVs[pv]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(pv,caget(__Min_PVs[pv]),caget(__Max_PVs[pv])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    else:
       __Aliases_dict[pv](currentpos+value)

##

def cmddriverel(pv, value):
    '''
    This function drives a motor from current position to the specified value, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more
                    general pv must be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv not in __Aliases_cmddict.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(pv) + bcolors.ENDC)
       SpellChk(pv)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    currentpos=caget(__Aliases_PVs[pv])
    if (currentpos+value) < caget(__Min_PVs[pv]) or (currentpos+value) > caget(__Max_PVs[pv]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(pv,caget(__Min_PVs[pv]),caget(__Max_PVs[pv])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    else:
       __Aliases_cmddict[pv](currentpos+value)

############ These ones Need to Be Tested with Beam On ############

def scan(name, minvalue, maxvalue, step, args, value, mode='step'):
    '''
    This function generate a single scan on a specified PV in the range selected by the user.
    param   name:   		Select the name of the PV to scan (axis1, axis2, 3sample, samplez, beaml, beamr, huber).
    param   min/maxvalue:	Minimum and Maximum range of the scan.
    param   step:    		Step size of the scan.
    param   args:   		'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:  		Value of the counting time (either C or s).
    param   mode:           Select the way the data are recorded ('single', 'step' default is 'step').
    '''
    if name not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(name) + bcolors.ENDC)
       SpellChk(name)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    elif args not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(args) + bcolors.ENDC)
       SpellChk(args)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    else:
       pv=__Aliases_PVs[name]
    if minvalue < caget(__Min_PVs[name]) or maxvalue > caget(__Max_PVs[name]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(name,caget(__Min_PVs[name]),caget(__Max_PVs[name])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    runs=np.arange(minvalue,maxvalue+step,step)
    currun=caget('BL5:CS:RunControl:LastRunNumber')+1
    cmds.append(Set('BL5:CS:LineLog:Add',"Scanning {0}, run {1}".format(name,currun)))
    if args.lower() == 'pc' and mode.lower() == 'step':
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Scanning " + name + " at " + str(r))
          #cmds.append(Set('BL5:SMS:RunInfo:RunTitle',"Scan_" + name + "_" + str(r)))
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
          waitPC(value)
          cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
    elif args.lower() == 'time' and mode.lower() == 'step':
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Scanning " + name + " at " + str(r))
          #cmds.append(Set('BL5:SMS:RunInfo:RunTitle',"Scan_" + name + "_" + str(r)))
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
          waitS(value)
          cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
    elif args.lower() == 'pc' and mode.lower() == 'single':
       cmds.append(Set('BL5:CS:Scan:Step:Control',1.0,completion=True))
       cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
       cmds.append(Wait('BL5:CS:RunControl:StateEnum',3.0,comparison='=',tolerance=0.1,timeout=60.0))
       cmds.append(Set('BL5:CS:RunControl:Pause',1.0,completion=True))
       for r in runs:
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:Det:ADnED:ResetCounters',1.0,completion=True))
          cmds.append(Set('BL5:CS:RunControl:Pause',0.0,completion=True))
          cmds.append(Set('BL5:CS:Scan:Step:Control',2.0,completion=True))
          waitPC(value)
          cmds.append(Set('BL5:CS:Scan:Step:Control',3.0,completion=True))
          cmds.append(Set('BL5:CS:RunControl:Pause',1.0,completion=True))
       cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
       cmds.append(Wait('BL5:CS:RunControl:StateEnum',1.0,comparison='=',tolerance=0.1,timeout=60.0))
    elif args.lower() == 'time' and mode.lower() == 'single':
       cmds.append(Set('BL5:CS:Scan:Step:Control',1.0,completion=True))
       cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
       cmds.append(Wait('BL5:CS:RunControl:StateEnum',3.0,comparison='=',tolerance=0.1,timeout=60.0))
       cmds.append(Set('BL5:CS:RunControl:Pause',1.0,completion=True))
       for r in runs:
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:Det:ADnED:ResetCounters',1.0,completion=True))
          cmds.append(Set('BL5:CS:RunControl:Pause',0.0,completion=True))
          cmds.append(Set('BL5:CS:Scan:Step:Control',2.0,completion=True))
          waitS(value)
          cmds.append(Set('BL5:CS:Scan:Step:Control',3.0,completion=True))
          cmds.append(Set('BL5:CS:RunControl:Pause',1.0,completion=True))
       cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
       cmds.append(Wait('BL5:CS:RunControl:StateEnum',1.0,comparison='=',tolerance=0.1,timeout=60.0))

##

def cmdscan(name, minvalue, maxvalue, step, args, value, mode='norun',wait=True):
    '''
    This function generate a single scan on a specified PV in the range selected by the user.
    param   name:   		Select the name of the PV to scan (axis1, axis2, 3sample, samplez, beaml, beamr, huber).
    param   min/maxvalue:	Minimum and Maximum range of the scan.

    param   step:    		Step size of the scan.
    param   args:   		'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:  		Value of the counting time (either C or s).
    param   mode:           Select the way the data are recorded ('single', 'step' default is 'norun').
    '''
    if name not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(name) + bcolors.ENDC)
       SpellChk(name)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    elif args not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(args) + bcolors.ENDC)

       SpellChk(args)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    else:
       pv=__Aliases_PVs[name]
    if minvalue < caget(__Min_PVs[name]) or maxvalue > caget(__Max_PVs[name]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(name,caget(__Min_PVs[name]),caget(__Max_PVs[name])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    currun=caget('BL5:CS:RunControl:LastRunNumber')+1
    caput('BL5:CS:LineLog:Add',"Scanning {0}, run {1}".format(name,currun))
    caput('BL5:CS:Align:Motor',pv)
    caput('BL5:CS:Align:Start',minvalue)
    caput('BL5:CS:Align:End',maxvalue)
    caput('BL5:CS:Align:Step',step)
    if args.lower() == 'pc':
       caput('BL5:CS:Align:Counter','BL5:Det:PCharge:C')
    elif args.lower() == 'time':
       caput('BL5:CS:Align:Counter','seconds')
    caput('BL5:CS:Align:Counts',value)
    if mode.lower() == 'norun':
       caput('BL5:CS:Align:Runs',0)
    elif mode.lower() == 'single':
       caput('BL5:CS:Align:Runs',1)
    elif mode.lower() == 'step':
       caput('BL5:CS:Align:Runs',2)
    caput('BL5:CS:Align:Run',1,wait=True)

##

def scanrel(name, minvalue, maxvalue, step, args, value, mode='step'):
    '''
    This function generate a single scan on a specified PV in the relative range selected by the user.
    param   name:   		Select the name of the PV to scan (axis1, axis2, 3sample, samplez, beaml, beamr, huber).
    param   min/maxvalue:	Minimum and Maximum range of the scan considering as central position the current location of the PV.
    param   step:    		Step size of the scan.
    param   args:   		'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:  		Value of the counting time (either C or s).
    param   mode:           Select the way the data are recorded ('single', 'step' default is 'step').
    '''
    if name not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(name) + bcolors.ENDC)
       SpellChk(name)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    elif args not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(args) + bcolors.ENDC)
       SpellChk(args)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    else:
       pv=__Aliases_PVs[name]
    center=caget(pv)
    if (center+minvalue) < caget(__Min_PVs[name]) or (center+maxvalue) > caget(__Max_PVs[name]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(name,caget(__Min_PVs[name]),caget(__Max_PVs[name])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    runs=np.arange((center+minvalue),(center+maxvalue+step), step)
    currun=caget('BL5:CS:RunControl:LastRunNumber')+1
    cmds.append(Set('BL5:CS:LineLog:Add',"Relative Scan {0}, run {1}".format(name,currun)))
    if args.lower() == 'pc' and mode.lower() == 'step':
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Relative Scan " + name + " at " + str(r))
          #cmds.append(Set('BL5:SMS:RunInfo:RunTitle',"Rel_Scan_" + name + "_" + str(r)))
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
          waitPC(value)
          cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
    elif args.lower() == 'time' and mode.lower() == 'step':
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Relative Scan " + name + " at " + str(r))
          #cmds.append(Set('BL5:SMS:RunInfo:RunTitle',"Rel_Scan_" + name + "_" + str(r)))
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
          waitS(value)
          cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
    elif args.lower() == 'pc' and mode.lower() == 'single':
       cmds.append(Set('BL5:CS:Scan:Step:Control',1.0,completion=True))
       cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
       cmds.append(Wait('BL5:CS:RunControl:StateEnum',3.0,comparison='=',tolerance=0.1,timeout=60.0))
       cmds.append(Set('BL5:CS:RunControl:Pause',1.0,completion=True))
       for r in runs:
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:Det:ADnED:ResetCounters',1.0,completion=True))
          cmds.append(Set('BL5:CS:RunControl:Pause',0.0,completion=True))
          cmds.append(Set('BL5:CS:Scan:Step:Control',2.0,completion=True))
          waitPC(value)
          cmds.append(Set('BL5:CS:Scan:Step:Control',3.0,completion=True))
          cmds.append(Set('BL5:CS:RunControl:Pause',1.0,completion=True))
       cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
       cmds.append(Wait('BL5:CS:RunControl:StateEnum',1.0,comparison='=',tolerance=0.1,timeout=60.0))
    elif args.lower() == 'time' and mode.lower() == 'single':
       cmds.append(Set('BL5:CS:Scan:Step:Control',1.0,completion=True))
       cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
       cmds.append(Wait('BL5:CS:RunControl:StateEnum',3.0,comparison='=',tolerance=0.1,timeout=60.0))
       cmds.append(Set('BL5:CS:RunControl:Pause',1.0,completion=True))
       for r in runs:
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:Det:ADnED:ResetCounters',1.0,completion=True))
          cmds.append(Set('BL5:CS:RunControl:Pause',0.0,completion=True))
          cmds.append(Set('BL5:CS:Scan:Step:Control',2.0,completion=True))
          waitS(value)
          cmds.append(Set('BL5:CS:Scan:Step:Control',3.0,completion=True))
          cmds.append(Set('BL5:CS:RunControl:Pause',1.0,completion=True))
       cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
       cmds.append(Wait('BL5:CS:RunControl:StateEnum',1.0,comparison='=',tolerance=0.1,timeout=60.0)) 
    
##

def cmdscanrel(name, minvalue, maxvalue, step, args, value, mode='norun',wait=True):
    '''
    This function generate a single scan on a specified PV in the range selected by the user.

    param   name:   		Select the name of the PV to scan (axis1, axis2, 3sample, samplez, beaml, beamr, huber).
    param   min/maxvalue:	Minimum and Maximum range of the scan.
    param   step:    		Step size of the scan.
    param   args:   		'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:  		Value of the counting time (either C or s).
    param   mode:           Select the way the data are recorded ('single', 'step' default is 'norun').
    '''
    if name not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(name) + bcolors.ENDC)
       SpellChk(name)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    elif args not in __Aliases_PVs.keys():
       print(bcolors.WARNING + bcolors.BOLD + "\n PV '{0}' not found !!!".format(args) + bcolors.ENDC)
       SpellChk(args)
       print("\n")
       raise RuntimeError("Not a valid PV, Check Spelling.")
    else:
       pv=__Aliases_PVs[name]
    center=caget(pv)
    if (center+minvalue) < caget(__Min_PVs[name]) or (center+maxvalue) > caget(__Max_PVs[name]):
       print(bcolors.WARNING + bcolors.BOLD + "\n Range for PV '{0}' = [{1},{2}] !!!".format(name,caget(__Min_PVs[name]),caget(__Max_PVs[name])) + bcolors.ENDC)
       raise RuntimeError("PV outside the Imposed Limits, Check the value.")
    currun=caget('BL5:CS:RunControl:LastRunNumber')+1
    caput('BL5:CS:LineLog:Add',"Relative Scan {0}, run {1}".format(name,currun))
    caput('BL5:CS:Align:Motor',pv)
    caput('BL5:CS:Align:Start',center+minvalue)
    caput('BL5:CS:Align:End',center+maxvalue)
    caput('BL5:CS:Align:Step',step)
    if args.lower() == 'pc':
       caput('BL5:CS:Align:Counter','BL5:Det:PCharge:C')
    elif args.lower() == 'time':
       caput('BL5:CS:Align:Counter','seconds')
    caput('BL5:CS:Align:Counts',value)
    if mode.lower() == 'norun':
       caput('BL5:CS:Align:Runs',0)
    elif mode.lower() == 'single':
       caput('BL5:CS:Align:Runs',1)
    elif mode.lower() == 'step':
       caput('BL5:CS:Align:Runs',2)
    caput('BL5:CS:Align:Run',1,wait=True)

######################## Loading and Saving a Chopper Configuration ########################

# CNCS checked on 12th Feb 2018
def loadconf(file_name):
    '''
    This function Loads a predefined Chopper configuration for CNCS in the CNCS_config folder. 
    param   file_name:  Name of the saved Chopper configuration (e.g. 'high_flux.sav', 'high_res.sav', 'intermediate.sav', 
                        'killingleak.sav', 'quasiwhitebeam.sav', 'max_flux.sav').
                        Refer to local contact for more information.
    '''
    config_path = "/home/bl-user/Script_Test/CNCS_config/" + file_name
    print("...Use Configuration file " + config_path)
    with open(config_path,'r') as filec:
	for line in filec:
	    data=line.split(' ')
	    #caput(data[0],data[1])
            cmds.append(Set(data[0],data[1], completion=True))
	    print("{0} {1}".format(data[0],data[1]))			
			
# CNCS checked on 12th Feb 2018
def saveconf(file_name):
    '''
    This function Saves a predefined Chopper configuration for CNCS in the CNCS_config folder. 
    param   file_name:  Name of the Chopper configuration users want to save.
                        THE FILE MUST BE SAVED WITH THE EXTENSION ".sav"
    '''
    config_path = "/home/bl-user/Script_Test/CNCS_config/" + file_name
    print("...Save Configuration file " + config_path)
    filec = open(config_path,'w')
    filec.write("BL5:Chop:Skf1:SpeedReq {0} \n".format(caget('BL5:Chop:Skf1:SpeedReq')))
    filec.write("BL5:Chop:Skf2:SpeedReq {0} \n".format(caget('BL5:Chop:Skf2:SpeedReq')))
    filec.write("BL5:Chop:Skf3:SpeedReq {0} \n".format(caget('BL5:Chop:Skf3:SpeedReq')))
    filec.write("BL5:Chop:Skf4:SpeedReq {0} \n".format(caget('BL5:Chop:Skf4:SpeedReq')))
    filec.write("BL5:Chop:Skf5:SpeedReq {0} \n".format(caget('BL5:Chop:Skf5:SpeedReq')))
    filec.write("BL5:Chop:Skf45:DblDiskModeReq {0} \n".format(caget('BL5:Chop:Skf45:DblDiskModeReq')))
    filec.close()

########################################################################################################################

def SROIqe(qmin,qmax,emin,emax):
    '''
    This function changes the limits of the Signal ROI on the Q/E plot.
    param   qmin/qmax:  Minimum and Maximum range of Q (1/A)
    param   emin/emax:  Minimum and Maximum range of Energy (meV)
    '''
    print(str(datetime.datetime.now()) + " New Q/E Signal ROI at Q=[{0},{1}] E=[{2},{3}]".format(qmin,qmax,emin,emax))
    caput('BL5:CS:LineLog:Add',"New Q/E Signal ROI at Q=[{0},{1}] E=[{2},{3}]".format(qmin,qmax,emin,emax))
    qsize=abs(qmax-qmin)
    esize=abs(emax-emin)
    caput('BL5:Det:N1:Det2:XY:ROI:1:P1Min',qmin)
    caput('BL5:Det:N1:Det2:XY:ROI:1:P1Size',qsize)
    caput('BL5:Det:N1:Det2:XY:ROI:1:P2Min',emin)
    caput('BL5:Det:N1:Det2:XY:ROI:1:P2Size',esize)

def BROIqe(qmin,qmax,emin,emax):
    '''
    This function changes the limits of the Background ROI on the Q/E plot.
    param   qmin/qmax:  Minimum and Maximum range of Q (1/A)
    param   emin/emax:  Minimum and Maximum range of Energy (meV)
    '''
    print(str(datetime.datetime.now()) + " New Q/E Background ROI at Q=[{0},{1}] E=[{2},{3}]".format(qmin,qmax,emin,emax))
    caput('BL5:CS:LineLog:Add',"New Q/E Background ROI at Q=[{0},{1}] E=[{2},{3}]".format(qmin,qmax,emin,emax))
    qsize=abs(qmax-qmin)
    esize=abs(emax-emin)
    caput('BL5:Det:N1:Det2:XY:ROI:2:P1Min',qmin)
    caput('BL5:Det:N1:Det2:XY:ROI:2:P1Size',qsize)
    caput('BL5:Det:N1:Det2:XY:ROI:2:P2Min',emin)
    caput('BL5:Det:N1:Det2:XY:ROI:2:P2Size',esize)

##

def SROIxy(tthmin,tthmax,phimin,phimax):
    '''
    This function changes the limits of the Signal ROI on the X/Y plot.
    param   tthmin/tthmax:  Minimum and Maximum range of 2 Theta (Degree)
    param   phimin/phimax:  Minimum and Maximum range of Phi (Degree)
    '''
    print(str(datetime.datetime.now()) + " New X/Y Signal ROI at 2Theta=[{0},{1}] Phi=[{2},{3}]".format(tthmin,tthmax,phimin,phimax))
    caput('BL5:CS:LineLog:Add',"New X/Y Signal ROI at 2Theta=[{0},{1}] Phi=[{2},{3}]".format(tthmin,tthmax,phimin,phimax))
    center2theta=(tthmin+tthmax)/2.0
    centerphi=(phimin+phimax)/2.0
    min2thl=3.8
    max2thl=132.6
    min2thr=3.8
    max2thr=53.6
    xpixelsize=(max2thl-min2thl)/(36*8)
    ypixelsize=(1.0/64.0)
    # Left Side bank (64.5 is half bank pixel)
    if ((phimin >= -90.0) and (phimin <= 90.0)) and ((phimax >= -90.0) and (phimax <= 90.0)):
        tthpixel=1.5+(max2thl+xpixelsize-tthmax)/xpixelsize
        tthpixelf=1.5+(max2thl+xpixelsize-tthmin)/xpixelsize
        tthsize=np.abs(tthpixelf-tthpixel)
        phipixel=3.0+64.5-(3.5*np.tan(phimax*pi/180.0)*np.sin(center2theta*pi/180.0))/ypixelsize
        phipixelf=3.0+64.5-(3.5*np.tan(phimin*pi/180.0)*np.sin(center2theta*pi/180.0))/ypixelsize
        phisize=np.abs(phipixelf-phipixel)        
    # Right Side bank (16.0 is the size of beamstop + 288 is pixel in 36 banks)
    elif ((phimin < -90.0) or (phimin > 90.0)) and ((phimax < -90.0) or (phimax > 90.0)):
        tthpixel=3.0+16.0+288.0+(-min2thr+xpixelsize+tthmin)/xpixelsize
        tthpixelf=3.0+16.0+288.0+(-min2thr+xpixelsize+tthmax)/xpixelsize
        tthsize=np.abs(tthpixelf-tthpixel)
        phipixel=3.0+64.5-(3.5*np.tan(phimin*pi/180.0)*np.sin(-center2theta*pi/180.0))/ypixelsize
        phipixelf=3.0+64.5-(3.5*np.tan(phimax*pi/180.0)*np.sin(-center2theta*pi/180.0))/ypixelsize
        phisize=np.abs(phipixelf-phipixel)
    if tthpixel < 0:
       tthpixel = 0
    elif tthpixel > 422:
       tthpixel = 422
    elif phipixel < 0:
       phipixel = 0
    elif phipixel > 134:
       phipixel = 134  
    caput('BL5:Det:N1:Det1:XY:ROI:1:MinX',int(np.round(tthpixel)))
    caput('BL5:Det:N1:Det1:XY:ROI:1:SizeX',int(np.round(tthsize)))
    caput('BL5:Det:N1:Det1:XY:ROI:1:MinY',int(np.round(phipixel)))
    caput('BL5:Det:N1:Det1:XY:ROI:1:SizeY',int(np.round(phisize)))

def BROIxy(tthmin,tthmax,phimin,phimax):
    '''
    This function changes the limits of the Background ROI on the X/Y plot.
    param   tthmin/tthmax:  Minimum and Maximum range of 2 Theta (Degree)
    param   phimin/phimax:  Minimum and Maximum range of Phi (Degree)
    '''
    print(str(datetime.datetime.now()) + " New X/Y Background ROI at 2Theta=[{0},{1}] Phi=[{2},{3}]".format(tthmin,tthmax,phimin,phimax))
    caput('BL5:CS:LineLog:Add',"New X/Y Background ROI at 2Theta=[{0},{1}] Phi=[{2},{3}]".format(tthmin,tthmax,phimin,phimax))
    center2theta=(tthmin+tthmax)/2.0
    centerphi=(phimin+phimax)/2.0
    min2thl=3.8
    max2thl=132.6
    min2thr=3.8
    max2thr=53.6
    xpixelsize=(max2thl-min2thl)/(36*8)
    ypixelsize=(1.0/64.0)
    # Left Side bank (64.5 is half bank pixel)
    if ((phimin >= -90.0) and (phimin <= 90.0)) and ((phimax >= -90.0) and (phimax <= 90.0)):
        tthpixel=1.5+(max2thl+xpixelsize-tthmax)/xpixelsize
        tthpixelf=1.5+(max2thl+xpixelsize-tthmin)/xpixelsize
        tthsize=np.abs(tthpixelf-tthpixel)
        phipixel=3.0+64.5-(3.5*np.tan(phimax*pi/180.0)*np.sin(center2theta*pi/180.0))/ypixelsize
        phipixelf=3.0+64.5-(3.5*np.tan(phimin*pi/180.0)*np.sin(center2theta*pi/180.0))/ypixelsize
        phisize=np.abs(phipixelf-phipixel)        
    # Right Side bank (16.0 is the size of beamstop + 288 is pixel in 36 banks)
    elif ((phimin < -90.0) or (phimin > 90.0)) and ((phimax < -90.0) or (phimax > 90.0)):
        tthpixel=3.0+16.0+288.0+(-min2thr+xpixelsize+tthmin)/xpixelsize
        tthpixelf=3.0+16.0+288.0+(-min2thr+xpixelsize+tthmax)/xpixelsize
        tthsize=np.abs(tthpixelf-tthpixel)
        phipixel=3.0+64.5-(3.5*np.tan(phimin*pi/180.0)*np.sin(-center2theta*pi/180.0))/ypixelsize
        phipixelf=3.0+64.5-(3.5*np.tan(phimax*pi/180.0)*np.sin(-center2theta*pi/180.0))/ypixelsize
        phisize=np.abs(phipixelf-phipixel)
    if tthpixel < 0:
       tthpixel = 0
    elif tthpixel > 422:
       tthpixel = 422
    elif phipixel < 0:
       phipixel = 0
    elif phipixel > 134:
       phipixel = 134
    caput('BL5:Det:N1:Det1:XY:ROI:2:MinX',int(np.round(tthpixel)))
    caput('BL5:Det:N1:Det1:XY:ROI:2:SizeX',int(np.round(tthsize)))
    caput('BL5:Det:N1:Det1:XY:ROI:2:MinY',int(np.round(phipixel)))
    caput('BL5:Det:N1:Det1:XY:ROI:2:SizeY',int(np.round(phisize)))


############### Dictionary to map the PVs to functions ###############

__Aliases_dict={'samplez':movesampleZ,'beaml':beamstopL,'beamr':beamstopR,'huber':movehuber,'ei':ei,
    'chop1':Fermifreq,'freq1':Fermifreq,'chop2':Chop2freq,'freq2':Chop2freq,'chop3':Chop3freq,'freq3':Chop3freq,'chop4':Chop4freq,'freq4':Chop4freq,
    'chop5':Chop5freq,'freq5':Chop5freq,'axis1':Axis1,'3sample':Axis1,'axis2':Axis2,'title':title,'comment':comment,'vstick':Vstick}

__Aliases_cmddict={'samplez':cmdmovesampleZ,'beaml':cmdbeamstopL,'beamr':cmdbeamstopR,'huber':cmdmovehuber,'collimator':collimator,'ei':cmdei,
    'chop1':cmdFermifreq,'freq1':cmdFermifreq,'chop2':cmdChop2freq,'freq2':cmdChop2freq,'chop3':cmdChop3freq,'freq3':cmdChop3freq,'chop4':cmdChop4freq,'freq4':cmdChop4freq,
    'chop5':cmdChop5freq,'freq5':cmdChop5freq,'axis1':cmdAxis1,'3sample':cmdAxis1,'axis2':cmdAxis2,'title':cmdtitle,'comment':cmdcomment,'vstick':cmdVstick}

__Min_PVs={'samplez':'BL5:Mot:sampleZ.LLM','beaml':'BL5:Mot:beamstopL.LLM','beamr':'BL5:Mot:beamstopR.LLM','huber':'BL5:Mot:huber.LLM','axis1':'BL5:Mot:Sample:Axis1.LLM','vstick':'BL5:Mot:Sample:Axis1.LLM','3sample':'BL5:Mot:Sample:Axis1.LLM',
    'axis2':'BL5:Mot:Sample:Axis2.LLM','ccr10s1':'BL5:SE:Lakeshore:CALC_IN_WINDOW1.A','ccr10s2':'BL5:SE:Lakeshore:CALC_IN_WINDOW2.A','vti':'BL5:SE:Cryo:Temp:TOLERANCE','cryo6':'BL5:SE:Cryo:Temp:TOLERANCE',
    'vtifitssm':'BL5:SE:Lakeshore:CALC_IN_WINDOW1.A','fitssm':'BL5:SE:Lakeshore:CALC_IN_WINDOW2.A'}

__Max_PVs={'samplez':'BL5:Mot:sampleZ.HLM','beaml':'BL5:Mot:beamstopL.HLM','beamr':'BL5:Mot:beamstopR.HLM','huber':'BL5:Mot:huber.HLM','axis1':'BL5:Mot:Sample:Axis1.HLM','vstick':'BL5:Mot:Sample:Axis1.HLM','3sample':'BL5:Mot:Sample:Axis1.HLM',
    'axis2':'BL5:Mot:Sample:Axis2.HLM','ccr10s1':'BL5:SE:Lakeshore:CALC_IN_WINDOW1.A','ccr10s2':'BL5:SE:Lakeshore:CALC_IN_WINDOW2.A','vticryo6':'BL5:SE:Cryo:Temp:TOLERANCE','cryo6':'BL5:SE:Cryo:Temp:TOLERANCE',
    'vtifitssm':'BL5:SE:Lakeshore:CALC_IN_WINDOW1.A','fitssm':'BL5:SE:Lakeshore:CALC_IN_WINDOW2.A'}

## Add New PVs here
__Aliases_PVs={'samplez':'BL5:Mot:sampleZ','beaml':'BL5:Mot:beamstopL','beamr':'BL5:Mot:beamstopR','huber':'BL5:Mot:huber','ei':'BL5:Chop:Gbl:EnergyReq','wl':'BL5:Chop:Skf1:WavelengthUserReq',
    'chop1':'BL5:Chop:Skf1:SpeedReq','freq1':'BL5:Chop:Skf1:SpeedReq','chop2':'BL5:Chop:Skf2:SpeedReq','freq2':'BL5:Chop:Skf2:SpeedReq','chop3':'BL5:Chop:Skf3:SpeedReq','freq3':'BL5:Chop:Skf3:SpeedReq',
    'chop4':'BL5:Chop:Skf4:SpeedReq','freq4':'BL5:Chop:Skf4:SpeedReq','chop5':'BL5:Chop:Skf5:SpeedReq','freq5':'BL5:Chop:Skf5:SpeedReq','axis1':'BL5:Mot:Sample:Axis1','3sample':'BL5:Mot:Sample:Axis1',
    'axis2':'BL5:Mot:Sample:Axis2','title':'BL5:SMS:RunInfo:RunTitle','comment':'BL5:SMS:Marker:NotesComment','pc':'BL5:Det:PCharge:C','time':'BL5:CS:RunControl:RunTimer','ccr10s1':'BL5:SE:Lakeshore:SETP_S1',
    'ccr10s2':'BL5:SE:Lakeshore:SETP_S2','vticryo6':'BL5:SE:Cryo:Temp:SETP_S1','cryo6':'BL5:SE:Cryo:Temp:SETP_S2','vtifitssm':'BL5:SE:FitSam:OP1SP','fitssm':'BL5:SE:FitSam:SampleTempSP'}

__Mode_PVs={'high_res':0,'high_flux':1,'intermediate':3}

########### Email Instrument Scientists for Alarm ###########


# Use the following table for popular carriers:
# T-Mobile: phonenumber@tmomail.net
# Virgin Mobile: phonenumber@vmobl.com
# Cingular: phonenumber@cingularme.com
# Sprint: phonenumber@messaging.sprintpcs.com
# Verizon: phonenumber@vtext.com
# Nextel: phonenumber@messaging.nextel.com
# AT&T: phonenumber@txt.att.net
# SPRINT NEXTEL pagenumber@page.nextel.com
# where phonenumber = your 10 digit phone number
# For ORNL accounts it is sufficient the 3-digit letters


def EmailAlert(email=""):
    '''
    This function sends an alert message (e.g. email or SMS message) to alert users and BL staff about the
    status of the instrument.
    # Use the following table for popular carriers:
    # T-Mobile: phonenumber@tmomail.net
    # Virgin Mobile: phonenumber@vmobl.com
    # Cingular: phonenumber@cingularme.com
    # Sprint: phonenumber@messaging.sprintpcs.com
    # Verizon: phonenumber@vtext.com
    # Nextel: phonenumber@messaging.nextel.com
    # AT&T: phonenumber@txt.att.net
    # SPRINT NEXTEL pagenumber@page.nextel.com
    # where phonenumber = your 10 digit phone number
    # For ORNL accounts it is sufficient the 3-digit letters
    param   email:   Email or phone number of the users.
    '''
    camonitor('BL5:CS:Scan:Alarm')
    SERVER = "160.91.4.26"
    FROM = "CNCS@ornl.gov"
    #TO = ["gqs@ornl.gov","ewf@ornl.gov","podlesnyakaa@ornl.gov"]# must be a list
    TO = ["gqs@ornl.gov","ewf@ornl.gov"]# must be a list
    TO.append(email) 
     
    SUBJECT = "Alarm from CNCS BL-5"
    TIME = str(datetime.datetime.now())
    TEXT = "This is CNCS, BL-5 at ORNL.\n Your scan finished at: {0}\n Please make sure you collected all data you need.".format(TIME)

    # Prepare actual message
    message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\n
    
    %s
    """ % (FROM, ",".join(TO), SUBJECT, TEXT)

    # Send the mail
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()

    print("Humans notified at: {0}".format(TIME))


