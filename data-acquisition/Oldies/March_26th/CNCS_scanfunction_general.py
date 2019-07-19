from epics import caget, caput, PV, cainfo
from scan import *
import numpy as np
import os
import sys
import datetime
# import savevalue
sys.path.append('/home/controls/share/master/python/Util')
from Autosave import Autosave

# Declare the Variables
cmds = []                                       # List of commands to execute, Order Matters !!!!
hystory = []                                    # Append the History of the commands to save a .txt file
client = ScanClient('bl5-dassrv1.sns.gov')      # Make sure it is the right address
pctotal = 0.0
timetotal = 0
this_name= os.path.basename(sys.argv[0])        # What is this ??


#######################################################################################
##################### List of Common Functions to Manipulate CNCS #####################
#######################################################################################

def WL(wl):
    '''
    This Function sets the Incident Wavelength (A).
    param   wl: Incident wavelength value.
                E = (81.7452)/wl^2
    '''
    cmds.append(Set('BL5:Chop:Skf1:WavelengthUserReq', wl, completion = True)) # Is it implemented ???
    hystory.append('BL5:Chop:Skf1:WavelengthUserReq')
    print(str(datetime.datetime.now()) + " ...Set Wavelength to " + str(wl) + " A")

def cmdWL(wl):
    '''
    This Function sets the Incident Wavelength (A).
    param   wl: Incident wavelength value.
                E = (81.7452)/wl^2
    '''
    caput('BL5:Chop:Skf1:WavelengthUserReq', wl) # Is it implemented ???
    print(str(datetime.datetime.now()) + " ...Set Wavelength to " + str(wl) + " A")

##

def ei(Energy):
    '''
    This Function sets the Incident Energy of the beam (meV).
    param   Energy: Incident energy value.
    '''
    cmds.append(Set('BL5:Chop:Gbl:EnergyReq', Energy, completion = True))
    hystory.append('BL5:Chop:Gbl:EnergyReq')
    print(str(datetime.datetime.now()) + " ...Set Incident Energy to " + str(Energy) + " meV")

def cmdei(Energy):
    '''
    This Function sets the Incident Energy of the beam (meV).
    param   Energy: Incident energy value.
    '''
    caput('BL5:Chop:Gbl:EnergyReq', Energy)
    print(str(datetime.datetime.now()) + " ...Set Incident Energy to " + str(Energy) + " meV")

##

def title(title):
    '''
    This Function sets the title of the scan. Users have the possibility to add PV values such as Energy, Motor Position,
    Temperature and Field. Any other note can be added using the command comment.
    param   title: Title of the scan.
    '''
    cmds.append(Set('BL5:SMS:RunInfo:RunTitle', title))
    hystory.append('BL5:SMS:RunInfo:RunTitle')
    print(str(datetime.datetime.now()) + " ...Set Title: {0} ".format(title))

def cmdtitle(title):
    '''
    This Function sets the title of the scan. Users have the possibility to add PV values such as Energy, Motor Position,
    Temperature and Field. Any other note can be added using the command cmdcomment.
    param   title: Title of the scan.
    '''
    caput('BL5:SMS:RunInfo:RunTitle', title)
    print(str(datetime.datetime.now()) + " ...Set Title: {0} ".format(title))

##

#def closeShutter():
#    cmds.append(Set('BL5:Mot:', 'Closed', completion=True))
#    print("...Close secondary shutter")

#def openShutter():
#    cmds.append(Set('BL5:Mot:', 'Open', completion=True))
#    print("...Open secondary shutter")

def Fermifreq(hz):
    '''
    This Function sets the Frequency of the Fermi Chopper (Hz).
    param   hz: Frequency of the Fermi Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf1:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf1:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Fermi Chopper frequency to " + str(hz) + " Hz, and wait for completion")

def cmdFermifreq(hz):
    '''
    This Function sets the Frequency of the Fermi Chopper (Hz).
    param   hz: Frequency of the Fermi Chopper (Hz).
    '''
    caput('BL5:Chop:Skf1:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Fermi Chopper frequency to " + str(hz) + " Hz, and wait for completion")

##

def Chop2freq(hz):
    '''
    This Function sets the Frequency of the second Chopper (Hz).
    param   hz: Frequency of the second Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf2:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf2:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Chopper 2 frequency to " + str(hz) + " Hz, and wait for completion")

def cmdChop2freq(hz):
    '''
    This Function sets the Frequency of the second Chopper (Hz).
    param   hz: Frequency of the second Chopper (Hz).
    '''
    caput('BL5:Chop:Skf2:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Chopper 2 frequency to " + str(hz) + " Hz, and wait for completion")

##

def Chop3freq(hz):
    '''
    This Function sets the Frequency of the third Chopper (Hz).
    param   hz: Frequency of the third Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf3:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf3:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Chopper 3 frequency to " + str(hz) + " Hz, and wait for completion")

def cmdChop3freq(hz):
    '''
    This Function sets the Frequency of the third Chopper (Hz).
    param   hz: Frequency of the third Chopper (Hz).
    '''
    caput('BL5:Chop:Skf3:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Chopper 3 frequency to " + str(hz) + " Hz, and wait for completion")

##

def Chop4freq(hz):
    '''
    This Function sets the Frequency of the first disk of the Double Disk Chopper (Hz).
    param   hz: Frequency of the first disk of the Double Disk Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf4:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf4:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Chopper 4 frequency to " + str(hz) + " Hz, and wait for completion")

def cmdChop4freq(hz):
    '''
    This Function sets the Frequency of the first disk of the Double Disk Chopper (Hz).
    param   hz: Frequency of the first disk of the Double Disk Chopper (Hz).
    '''
    caput('BL5:Chop:Skf4:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Chopper 4 frequency to " + str(hz) + " Hz, and wait for completion")

##

def Chop5freq(hz):
    '''
    This Function sets the Frequency of the second disk of the Double Disk Chopper (Hz).
    param   hz: Frequency of the second disk of the Double Disk Chopper (Hz).
    '''
    cmds.append(Set('BL5:Chop:Skf5:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf5:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Chopper 5 frequency to " + str(hz) + " Hz, and wait for completion")

def cmdChop5freq(hz):
    '''
    This Function sets the Frequency of the second disk of the Double Disk Chopper (Hz).
    param   hz: Frequency of the second disk of the Double Disk Chopper (Hz).
    '''
    caput('BL5:Chop:Skf5:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Chopper 5 frequency to " + str(hz) + " Hz, and wait for completion")

##

# Need to check this command
def GChopfreq(hz1,hz2,hz3,hz4,hz5):
    '''
    This Function sets the Frequency of all the Choppers at CNCS in parallel.
    param   hz1: Frequency of the Fermi Chopper (Hz).
    param   hz2: Frequency of the second Chopper (Hz).
    param   hz3: Frequency of the third Chopper (Hz).
    param   hz4: Frequency of the first disk of the Double Disk Chopper (Hz).
    param   hz5: Frequency of the second disk of the Double Disk Chopper (Hz).
    '''
    cmds.append(Set('+p BL5:Chop:Skf1:SpeedReq', hz1, completion = True))
    cmds.append(Set('+p BL5:Chop:Skf2:SpeedReq', hz2, completion = True))
    cmds.append(Set('+p BL5:Chop:Skf3:SpeedReq', hz3, completion = True))
    cmds.append(Set('+p BL5:Chop:Skf4:SpeedReq', hz4, completion = True))
    cmds.append(Set('+p BL5:Chop:Skf5:SpeedReq', hz5, completion = True))
    hystory.append('Changed:Global:Chopper:Frequqncies')
    print(str(datetime.datetime.now()) + " ...Setting Chopper frequencis to " + str(hz1,hz2,hz3,hz4,hz5) + " Hz, and wait for completion")

# Need to check this command
def cmdGChopfreq(hz1,hz2,hz3,hz4,hz5):
    '''
    This Function sets the Frequency of all the Choppers at CNCS in parallel.
    param   hz1: Frequency of the Fermi Chopper (Hz).
    param   hz2: Frequency of the second Chopper (Hz).
    param   hz3: Frequency of the third Chopper (Hz).
    param   hz4: Frequency of the first disk of the Double Disk Chopper (Hz).
    param   hz5: Frequency of the second disk of the Double Disk Chopper (Hz).
    '''
    caput('+p BL5:Chop:Skf1:SpeedReq', hz1)
    caput('+p BL5:Chop:Skf2:SpeedReq', hz2)
    caput('+p BL5:Chop:Skf3:SpeedReq', hz3)
    caput('+p BL5:Chop:Skf4:SpeedReq', hz4)
    caput('+p BL5:Chop:Skf5:SpeedReq', hz5)
    print(str(datetime.datetime.now()) + " ...Setting Chopper frequencis to " + str(hz1,hz2,hz3,hz4,hz5) + " Hz, and wait for completion")

# Need to check this command for adding delays
def delay(time):
    '''
    This function sets a delay (s) in the script. It can be used e.g. to
    thermalise the system or, more in general, to wait before executing a command.
    param   time: Value of the time-delay in seconds.
    '''
    global timetotal
    timetotal = timetotal + time
    print("...Delay " + str(time) + " seconds")
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

def Axis1(value):
    '''
    This function drives the motor connected with Axis1. Please refer to local contact
    for more information.
    param   value:  Value of the angle in degree.
    '''
    cmds.append(Set('BL5:Mot:Sample:Axis1', value, completion = True))
    hystory.append('BL5:Mot:Sample:Axis1')
    print(str(datetime.datetime.now()) + " ...Drive Axis1 to " + str(value) + " Degree")

def cmdAxis1(value):
    '''
    This function drives the motor connected with Axis1. Please refer to local contact
    for more information.
    param   value:  Value of the angle in degree.
    '''
    caput('BL5:Mot:Sample:Axis1', value)
    print(str(datetime.datetime.now()) + " ...Drive Axis1 to " + str(value) + " Degree")

##

def Axis2(value):
    '''
    This function drives the motor connected with Axis2. Please refer to local contact
    for more information.
    param   value:  Value of the angle in degree.
    '''
    cmds.append(Set('BL5:Mot:Sample:Axis2', value, completion = True))
    hystory.append('BL5:Mot:Sample:Axis2')
    print(str(datetime.datetime.now()) + " ...Drive Axis2 to " + str(value) + " Degree")

def cmdAxis2(value):
    '''
    This function drives the motor connected with Axis2. Please refer to local contact
    for more information.
    param   value:  Value of the angle in degree.
    '''
    caput('BL5:Mot:Sample:Axis2', value)
    print(str(datetime.datetime.now()) + " ...Drive Axis2 to " + str(value) + " Degree")

##

def movesampleZ(value):
    '''
    This function Lifts the sample Z axis in the laboratory coordinate system. Please refer to local contact
    for more information. Limits are from 150 mm to 210 mm
    param   value:  Value of the position of Sample Z (mm).
    '''
    cmds.append(Set('BL5:Mot:sampleZ', value, completion = True))
    hystory.append('BL5:Mot:sampleZ')
    print(str(datetime.datetime.now()) + " ...Move Sample Z to " + str(value) + " mm")

def cmdmovesampleZ(value):
    '''
    This function Lifts the sample Z axis in the laboratory coordinate system. Please refer to local contact
    for more information. Limits are from 150 mm to 210 mm
    param   value:  Value of the position of Sample Z (mm).
    '''
    caput('BL5:Mot:sampleZ', value)
    print(str(datetime.datetime.now()) + " ...Move Sample Z to " + str(value) + " mm")

##

def movehuber(value):
    '''
    This function moves the huber rotation of the sample. Please refer to local contact
    for more information. 
    param   value:  Value of the angle in degree.
    '''
    cmds.append(Set('BL5:Mot:huber', value, completion = True))
    hystory.append('BL5:Mot:huber')
    print(str(datetime.datetime.now()) + " ...Move huber to " + str(value) + " Degree")

def cmdmovehuber(value):
    '''
    This function moves the huber rotation of the sample. Please refer to local contact
    for more information. 
    param   value:  Value of the angle in degree.
    '''
    caput('BL5:Mot:huber', value)
    print(str(datetime.datetime.now()) + " ...Move huber to " + str(value) + " Degree")

##

def beamstopL(pos):    
    '''
    This function moves the Left Beam Stop. Limits are -10 to +10 mm.
    param   value:  Position of the Left beam stop in mm.
    '''
    cmds.append(Set('BL5:Mot:beamstopL', pos, completion = True))
    hystory.append('BL5:Mot:beamstopL')
    print(str(datetime.datetime.now()) + " ...Set Beamstop Left : "+str(pos)+" mm")

def cmdbeamstopL(pos):
    '''
    This function moves the Left Beam Stop. Limits are -10 to +10 mm.
    param   value:  Position of the Left beam stop in mm.
    '''
    caput('BL5:Mot:beamstopL', pos)
    print(str(datetime.datetime.now()) + " ...Set Beamstop Left : "+str(pos)+" mm")

##

def beamstopR(pos):
    '''
    This function moves the Right Beam Stop. Limits are -10 to +10 mm.
    param   value:  Position of the Right beam stop in mm.
    '''
    cmds.append(Set('BL5:Mot:beamstopR', pos, completion = True))
    hystory.append('BL5:Mot:beamstopR')
    print(str(datetime.datetime.now()) + " ...Set Beamstop Right : "+str(pos)+" mm")

def cmdbeamstopR(pos):
    '''
    This function moves the Right Beam Stop. Limits are -10 to +10 mm.
    param   value:  Position of the Right beam stop in mm.
    '''
    caput('BL5:Mot:beamstopR', pos)
    print(str(datetime.datetime.now()) + " ...Set Beamstop Right : "+str(pos)+" mm")

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

#def sethaaketemp(value):
#    print "...Set HAAKE temperature to " + str(value)
#    cmds.append(Set('BL6:SE:HAAKE:WriteSetPointTemp', value, completion = True))

#def setfurnacetemp(value):
#    print "...Set furnace temperature to " + str(value)
#    cmds.append(Set('BL6:SE:FURNACE:SP', value, completion = True))

#def movemask(value):
#    print "...Move mask to " + str(value)
#   cmds.append(Set('BL6:Mot:mask', value, completion = True))

#######################################################################################
############################### General Commands Stage ################################
#######################################################################################

def submit(scantitle=os.path.basename(sys.argv[0])):
    '''
    This function submits a scan or an ensamble of scans in the script.
    It does not require any parameters.
    '''
    print("...Submitting the scan : " + scantitle)
    id = client.submit(cmds, scantitle)
    print("...scan id = " + str(id))
    newscan()  # after submission, reset the cmds list every time

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
    of 0.85 MW, 1.0 MW and 1.2 MW.
    It does not require any parameters.
    '''
    print ".Total PC = %.2f C \n..........= %.2f hours (%.1f min) at 1.2 MW \n..........= %.2f hours (%.1f min) at 1.0 MW \n..........= %.2f hours (%.1f min) at 0.85 MW"  % (pctotal , 	pctotal/4.32, pctotal/4.32*60 , pctotal/3.6, pctotal/3.6*60, pctotal/3.0, pctotal/3.0*60)
    print ".Other time = %.1f s = %.2f hours" %(timetotal, timetotal/3600)

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
#													    #
#				Translation of the old HFIR command in SPICE				    #
#													    #
#############################################################################################################

def begin(ipts):
    '''
    This command begins a New Experiment by typing the specified IPTS.
    param   ipts:  New IPTS number of the current experiment.
    '''
    caput('BL5:CS:IPTS',ipts)
    print(str(datetime.datetime.now()) + " Begin IPTS-{0} ".format(ipts))

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
    print(str(datetime.datetime.now()) + " Comment: {0}".format(note))

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
    print(str(datetime.datetime.now()) + " Setting: h={0} k={1} l={2}".format(h,k,l))

def Vvec(h,k,l):
    '''
    This command sets the Nominal v Vector of the Scattering Plane.
    param   h,k,l:   Value of the Reciprocal Lattice Indices.
    '''
    caput('BL5:CS:CrystalAlign:v0:h',h)
    caput('BL5:CS:CrystalAlign:v0:k',k)
    caput('BL5:CS:CrystalAlign:v0:l',l)
    print(str(datetime.datetime.now()) + " Setting: h={0} k={1} l={2}".format(h,k,l))

## Check that the value is connected to the right PV (Is it Pos or Base ?)

def com(pv, wait=True):
    '''
    This function drives a motor to the Center of Mass calculated from a scan, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more
                    general pv must be verified with the local contact.
    '''
    value=caget('BL5:CS:Fitting:Fit:Pos')
    if pv.lower() == 'axis1' or pv.lower() == '3sample' :
	cmdAxis1(value)
    elif pv.lower() == 'axis2' :
	cmdAxis2(value)
    elif pv.lower() == 'samplez' :
	cmdmovesampleZ(value)
    elif pv.lower() == 'huber' :
	cmdmovehuber(value)
    elif pv.lower() == 'beaml' :
	cmdbeamstopL(value)
    elif pv.lower() == 'beamr' :
	cmdbeamstopR(value)
    else:
	print("...Not a predefined PV. Check PV spelling.")

## Find a way to get this peak from the Calculated Bragg peak list

def br(h,k,l,args, wait=True):
    '''
    This function drives a motor to the (h,k,l) peak specified, the peak can be observed.
    either on the 'left' or 'right' side of the detector array.
    param   h,k,l:   Selected Miller Indices of the peak.
    param   args:    Choose if you want to see the peak on the 'left' or 'right' side of the detector array.
    '''
    if args.lower() == 'left' :
       #caput('BL5:CS:CrystalAlign:SelectedPeak',str("({0},{1},{2})".format(h,k,l)))
       Omega=caget('BL5:CS:CrystalAlign:SelectedOmega')
       #caput('BL5:CS:CrystalAlign:OmegaMotor',Omega)
       print(str(datetime.datetime.now()) + " Driving to: ({0},{1},{2}) at Omega={3}".format(h,k,l,Omega))
    elif args.lower() == 'right':
       #caput('BL5:CS:CrystalAlign:SelectedPeak',str("({0},{1},{2})".format(h,k,l)))
       Omega=caget('BL5:CS:CrystalAlign:SelectedOmega')
       #caput('BL5:CS:CrystalAlign:OmegaMotor',Omega)
       print(str(datetime.datetime.now()) + " Driving to: ({0},{1},{2}) at Omega={3}".format(h,k,l,Omega))

############################# Drive Commands #############################

def drive(pv, value, wait=True):
    '''
    This function is a general command to drive a motor, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more
                    general pv must be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv.lower() == 'axis1' or pv.lower() == '3sample' :
	Axis1(value)
    elif pv.lower() == 'axis2' :
	Axis2(value)
    elif pv.lower() == 'samplez' :
	movesampleZ(value)
    elif pv.lower() == 'huber' :
	movehuber(value)
    elif pv.lower() == 'beaml' :
	beamstopL(value)
    elif pv.lower() == 'beamr' :
	beamstopR(value)
    else:
	print("...Not a predefined PV. Check PV spelling.")

##

def cmddrive(pv, value, wait=True):
    '''
    This function is a general command to drive a motor, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more 
                    general pv must be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv.lower() == 'axis1' or pv.lower() == '3sample' :
        cmdAxis1(value)
    elif pv.lower() == 'axis2' :
        cmdAxis2(value)
    elif pv.lower() == 'samplez' :
	cmdmovesampleZ(value)
    elif pv.lower() == 'huber' :
	cmdmovehuber(value)
    elif pv.lower() == 'beaml' :
	cmdbeamstopL(value)
    elif pv.lower() == 'beamr' :
	cmdbeamstopR(value)
    else:
        print("...Not a predefined PV. Check PV spelling.")

##

def driverel(pv, value, wait=True):
    '''
    This function drives a motor from current position to the specified value, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more
                    general pv must be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv.lower() == 'axis1' or pv.lower() == '3sample' :
        currentpos=caget('BL5:Mot:Sample:Axis1')
	Axis1(currentpos+value)
    elif pv.lower() == 'axis2' :
        currentpos=caget('BL5:Mot:Sample:Axis2')
	Axis2(currentpos+value)
    elif pv.lower() == 'samplez' :
        currentpos=caget('BL5:Mot:sampleZ')
	movesampleZ(currentpos+value)
    elif pv.lower() == 'huber' :
        currentpos=caget('BL5:Mot:huber')
	movehuber(currentpos+value)
    elif pv.lower() == 'beaml' :
        currentpos=caget('BL5:Mot:beamstopL')
	beamstopL(currentpos+value)
    elif pv.lower() == 'beamr' :
        currentpos=caget('BL5:Mot:beamstopR')
	beamstopR(currentpos+value)
    else:
	print("...Not a predefined PV. Check PV spelling.")

##

def cmddriverel(pv, value, wait=True):
    '''
    This function drives a motor from current position to the specified value, and it waits till the command is completed.
    param   pv:     Name of the alias pv (axis1, axis2, 3sample, samplez, huber, beaml, beamr). A more
                    general pv must be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv.lower() == 'axis1' or pv.lower() == '3sample' :
        currentpos=caget('BL5:Mot:Sample:Axis1')
	cmdAxis1(currentpos+value)
    elif pv.lower() == 'axis2' :
        currentpos=caget('BL5:Mot:Sample:Axis2')
	cmdAxis2(currentpos+value)
    elif pv.lower() == 'samplez' :
        currentpos=caget('BL5:Mot:sampleZ')
	cmdmovesampleZ(currentpos+value)
    elif pv.lower() == 'huber' :
        currentpos=caget('BL5:Mot:huber')
	cmdmovehuber(currentpos+value)
    elif pv.lower() == 'beaml' :
        currentpos=caget('BL5:Mot:beamstopL')
	cmdbeamstopL(currentpos+value)
    elif pv.lower() == 'beamr' :
        currentpos=caget('BL5:Mot:beamstopR')
	cmdbeamstopR(currentpos+value)
    else:
	print("...Not a predefined PV. Check PV spelling.")



#############

def set(pv, value, wait=True):
    '''
    This function is a general command to set the value of a PV, and it waits till the command is completed.
    param   pv:     Name of the alias pv (samplez, beaml, beamr, huber, collimator, ei, wl, title). A more general pv must
                    be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv.lower() == 'samplez' :
        movesampleZ(value)
    elif pv.lower() == 'beaml' :
        beamstopL(value)
    elif pv.lower() == 'beamr':
        beamstopR(value)
    elif pv.lower() == 'huber':
        movehuber(value)
    elif pv.lower() == 'collimator':
        collimator(value)
    elif pv.lower() == 'ei':
        ei(value)
    elif pv.lower() == 'wl':
        WL(value)
    elif pv.lower() =='chop1' or pv.lower()=='freq1' :
        Fermifreq(value)
    elif pv.lower() =='chop2' or pv.lower()=='freq2' :
        Chop2freq(value)
    elif pv.lower() =='chop3' or pv.lower()=='freq3' :
        Chop3freq(value)
    elif pv.lower() =='chop4' or pv.lower()=='freq4' :
        Chop4freq(value)
    elif pv.lower() =='chop5' or pv.lower()=='freq5' :
        Chop5freq(value)
    elif pv.lower() == 'axis1' or pv.lower() == '3sample' :
        Axis1(value)
    elif pv.lower() == 'axis2' :
        Axis2(value)
    elif pv.lower() == 'title' :
        title(value)
    else:
        print("...Not a predefined PV. Processing as a raw command.")
        cmds.append(Set(pv, value, completion = wait))

##

def cmdset(pv, value, wait=True):
    '''
    This function is a general command to set the value of a PV, and it waits till the command is completed.
    param   pv:     Name of the alias pv (samplez, beaml, beamr, huber, collimator, ei, wl, title). A more general pv must
                    be verified with the local contact.
    param   value:  New value of the pv.
    '''
    if pv.lower() == 'samplez' :
        cmdmovesampleZ(value)
    elif pv.lower() == 'beaml' :
        cmdbeamstopL(value)
    elif pv.lower() == 'beamr':
        cmdbeamstopR(value)
    elif pv.lower() == 'huber':
        cmdmovehuber(value)
    elif pv.lower() == 'collimator':
        cmdcollimator(value)
    elif pv.lower() == 'ei':
        cmdei(value)
    elif pv.lower() == 'wl':
        cmdWL(value)
    elif pv.lower() =='chop1' or pv.lower()=='freq1' :
        cmdFermifreq(value)
    elif pv.lower() =='chop2' or pv.lower()=='freq2' :
        cmdChop2freq(value)
    elif pv.lower() =='chop3' or pv.lower()=='freq3' :
        cmdChop3freq(value)
    elif pv.lower() =='chop4' or pv.lower()=='freq4' :
        cmdChop4freq(value)
    elif pv.lower() =='chop5' or pv.lower()=='freq5' :
        cmdChop5freq(value)
    elif pv.lower() == 'axis1' or pv.lower() == '3sample' :
        cmdAxis1(value)
    elif pv.lower() == 'axis2' :
        cmdAxis2(value)
    elif pv.lower() == 'title' :
        cmdtitle(value)
    else:
        print("...Not a predefined PV. Processing as a raw command.")
        caput(pv, value)

############ A for loop has been tested on 12 Feb 2018 ##############

def runexp(title, energy, name, pos, args, value): 
    '''
    This function automatically generates a scan that can be submitted in the scan server.
    param   title:   Set a title for the scan. The Incident Energy and Sample position will be automatically recorded.
    param   energy:  Incident Energy (meV).
    param   name:    Name of the PV to scan (axis1, axis2).
    param   pos:     Set a position of the sample (an array of angle can be given).
    param   args:    'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:   Value of the counting time (either C or s).
    '''
    if name.lower() == 'axis1' :
       pv='BL5:Mot:Sample:Axis1'
    elif name.lower() == 'axis2' :
       pv='BL5:Mot:Sample:Axis2'
    if args.lower() == 'pc' :
        global pctotal
        pctotal = pctotal + value
        cmds.append(Set('BL5:SMS:RunInfo:RunTitle', title + "_" + str(energy) + "meV_" + str(pos)))
        cmds.append(Set('BL5:Chop:Gbl:EnergyReq', energy))
        cmds.append(Set(pv, pos, completion=True))
        cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
        cmds.append(Wait('BL5:Det:PCharge:C', value, comparison='increase by'))
        cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
        print(str(datetime.datetime.now()) + " ...Set measurement for " + title + " at position " + str(pos))
    elif args.lower() == 'time' :
        global timetotal
        timetotal = timetotal + value
        cmds.append(Set('BL5:SMS:RunInfo:RunTitle', title + "_" + str(energy) + "meV_" + str(pos)))
        cmds.append(Set('BL5:Chop:Gbl:EnergyReq', energy))
        cmds.append(Set(pv, pos, completion=True))
        cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
        cmds.append(Wait('BL5:CS:RunControl:RunTimer', value, comparison='increase by'))
        cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
        print(str(datetime.datetime.now()) + " ...Set measurement for " + title + " at position " + str(pos))

############ These ones Need to Be Tested with Beam On ############

def scan(name, minvalue, maxvalue, step, args, value):
    '''
    This function generate a single scan on a specified PV in the range selected by the user.
    param   name:   		Select the name of the PV to scan (axis1, axis2, 3sample, samplez, beaml, beamr, huber).
    param   minvalue,maxvalue:	Minimum and Maximum range of the scan.
    param   step:    		Step size of the scan.
    param   args:   		'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:  		Value of the counting time (either C or s).
    '''
    if name.lower() == 'axis1' or name.lower() == '3sample' :
       pv='BL5:Mot:Sample:Axis1'
    elif name.lower() == 'axis2' :
       pv='BL5:Mot:Sample:Axis2'
    elif name.lower() == 'samplez' :
       pv='BL5:Mot:sampleZ'
    elif name.lower() == 'huber' :
       pv='BL5:Mot:huber'
    elif name.lower() == 'beaml' :
       pv='BL5:Mot:beamstopL'
    elif name.lower() == 'beamr' :
       pv='BL5:Mot:beamstopR'
    runs=np.arange(minvalue,maxvalue+step,step)
    if args.lower() == 'pc' :
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Scanning " + pv + " at " + str(r))
          cmds.append(Set('BL5:SMS:RunInfo:RunTitle',"Scan_" + name + "_" + str(r)))
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
          cmds.append(Wait('BL5:Det:PCharge:C', value, comparison='increase by'))
          cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
    elif args.lower() == 'time' :
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Scanning " + pv + " at " + str(r))
          cmds.append(Set('BL5:SMS:RunInfo:RunTitle',"Scan_" + name + "_" + str(r)))
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
          cmds.append(Wait('BL5:CS:RunControl:RunTimer', value, comparison='increase by'))
          cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))

##

def cmdscan(name, minvalue, maxvalue, step, args, value):
    '''
    This function generate a single scan on a specified PV in the range selected by the user.
    param   name:   		Select the name of the PV to scan (axis1, axis2, 3sample, samplez, beaml, beamr, huber).
    param   minvalue,maxvalue:	Minimum and Maximum range of the scan.
    param   step:    		Step size of the scan.
    param   args:   		'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:  		Value of the counting time (either C or s).
    '''
    if name.lower() == 'axis1' or name.lower() == '3sample' :
       pv='BL5:Mot:Sample:Axis1'
    elif name.lower() == 'axis2' :
       pv='BL5:Mot:Sample:Axis2'
    elif name.lower() == 'samplez' :
       pv='BL5:Mot:sampleZ'
    elif name.lower() == 'huber' :
       pv='BL5:Mot:huber'
    elif name.lower() == 'beaml' :
       pv='BL5:Mot:beamstopL'
    elif name.lower() == 'beamr' :
       pv='BL5:Mot:beamstopR'
    runs=np.arange(minvalue,maxvalue+step,step)
    if args.lower() == 'pc' :
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Scanning " + pv + " at " + str(r))
          caput('BL5:SMS:RunInfo:RunTitle',"Scan_" + name + "_" + str(r))
          caput(pv,r, completion=True)
          caput('BL5:CS:RunControl:Start', 1, completion=True)
          Wait('BL5:Det:PCharge:C', value, comparison='increase by')
          caput('BL5:CS:RunControl:Stop', 1, completion=True)
    elif args.lower() == 'time' :
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Scanning " + pv + " at " + str(r))
          caput('BL5:SMS:RunInfo:RunTitle',"Scan_" + name + "_" + str(r))
          caput(pv,r, completion=True)
          caput('BL5:CS:RunControl:Start', 1, completion=True)
          Wait('BL5:CS:RunControl:RunTimer', value, comparison='increase by')
          caput('BL5:CS:RunControl:Stop', 1, completion=True)

##

def scanrel(name, minvalue, maxvalue, step, args, value):
    '''
    This function generate a single scan on a specified PV in the relative range selected by the user.
    param   name:   		Select the name of the PV to scan (axis1, axis2, 3sample, samplez, beaml, beamr, huber).
    param   minvalue,maxvalue:	Minimum and Maximum range of the scan considering as central position the current location of the PV.
    param   step:    		Step size of the scan.
    param   args:   		'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:  		Value of the counting time (either C or s).
    '''
    if name.lower() == 'axis1' or name.lower() == '3sample' :
       pv='BL5:Mot:Sample:Axis1'
    elif name.lower() == 'axis2' :
       pv='BL5:Mot:Sample:Axis2'
    elif name.lower() == 'samplez' :
       pv='BL5:Mot:sampleZ'
    elif name.lower() == 'huber' :
       pv='BL5:Mot:huber'
    elif name.lower() == 'beaml' :
       pv='BL5:Mot:beamstopL'
    elif name.lower() == 'beamr' :
       pv='BL5:Mot:beamstopR'
    center=caget(pv)
    runs=np.arange((center-minvalue),(center+maxvalue+step), step)
    if args.lower() == 'pc' :
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Relative Scan " + pv + " at " + str(r))
          cmds.append(Set('BL5:SMS:RunInfo:RunTitle',"Rel_Scan_" + name + "_" + str(r)))
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
          cmds.append(Wait('BL5:Det:PCharge:C', value, comparison='increase by'))
          cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
    elif args.lower() == 'time' :
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Relative Scan " + pv + " at " + str(r))
          cmds.append(Set('BL5:SMS:RunInfo:RunTitle',"Rel_Scan_" + name + "_" + str(r)))
          cmds.append(Set(pv,r, completion=True))
          cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
          cmds.append(Wait('BL5:CS:RunControl:RunTimer', value, comparison='increase by'))
          cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))

##

def cmdscanrel(name, minvalue, maxvalue, step, args, value):
    '''
    This function generate a single scan on a specified PV in the relative range selected by the user.
    param   name:   		Select the name of the PV to scan (axis1, axis2, 3sample, samplez, beaml, beamr, huber).
    param   minvalue,maxvalue:	Minimum and Maximum range of the scan considering as central position the current location of the PV.
    param   step:    		Step size of the scan.
    param   args:   		'pc' to count in Coulomb, or 'time' to count in seconds.
    param   value:  		Value of the counting time (either C or s).
    '''
    if name.lower() == 'axis1' or name.lower() == '3sample' :
       pv='BL5:Mot:Sample:Axis1'
    elif name.lower() == 'axis2' :
       pv='BL5:Mot:Sample:Axis2'
    elif name.lower() == 'samplez' :
       pv='BL5:Mot:sampleZ'
    elif name.lower() == 'huber' :
       pv='BL5:Mot:huber'
    elif name.lower() == 'beaml' :
       pv='BL5:Mot:beamstopL'
    elif name.lower() == 'beamr' :
       pv='BL5:Mot:beamstopR'
    center=caget(pv)
    runs=np.arange((center-minvalue),(center+maxvalue+step), step)
    if args.lower() == 'pc' :
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Relative Scan " + pv + " at " + str(r))
          caput('BL5:SMS:RunInfo:RunTitle',"Rel_Scan_" + name + "_" + str(r))
          caput(pv,r, completion=True)
          caput('BL5:CS:RunControl:Start', 1, completion=True)
          Wait('BL5:Det:PCharge:C', value, comparison='increase by')
          caput('BL5:CS:RunControl:Stop', 1, completion=True)
    elif args.lower() == 'time' :
       for r in runs:
          print(str(datetime.datetime.now()) + " ...Relative Scan " + pv + " at " + str(r))
          caput('BL5:SMS:RunInfo:RunTitle',"Rel_Scan_" + name + "_" + str(r))
          caput(pv,r, completion=True)
          caput('BL5:CS:RunControl:Start', 1, completion=True)
          Wait('BL5:CS:RunControl:RunTimer', value, comparison='increase by')
          caput('BL5:CS:RunControl:Stop', 1, completion=True)


######################## Loading and Saving a Chopper Configuration ########################

# CNCS checked on 12th Feb 2018
def loadconf(file_name):
    '''
    This function Loads a predefined Chopper configuration for CNCS in the CNCS_config folder. 
    param   file_name:  Name of the saved Chopper configuration.
                        Refer to local contact for more information.
    '''
    config_path = "/home/bl-user/Script_Test/CNCS_config/" + file_name
    print("...Use Configuration file " + config_path)
    with open(config_path,'r') as filec:
	for line in filec:
		data=line.split(' ')
		caput(data[0],data[1])
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
    filec.write("BL5:Chop:Skf1:SpeedUserReq {0} \n".format(caget('BL5:Chop:Skf1:SpeedUserReq')))
    filec.write("BL5:Chop:Skf2:SpeedUserReq {0} \n".format(caget('BL5:Chop:Skf2:SpeedUserReq')))
    filec.write("BL5:Chop:Skf3:SpeedUserReq {0} \n".format(caget('BL5:Chop:Skf3:SpeedUserReq')))
    filec.write("BL5:Chop:Skf4:SpeedUserReq {0} \n".format(caget('BL5:Chop:Skf4:SpeedUserReq')))
    filec.write("BL5:Chop:Skf5:SpeedUserReq {0} \n".format(caget('BL5:Chop:Skf5:SpeedUserReq')))
    filec.write("BL5:Chop:Skf45:DblDiskModeReq {0} \n".format(caget('BL5:Chop:Skf45:DblDiskModeReq')))
    filec.close()

########################################################################################################################

def SROIqe(qmin,qmax,emin,emax):
    '''
    This function changes the limits of the Signal ROI on the Q/E plot.
    param   qmin/qmax:  Minimum and Maximum range of Q (1/A)
    param   emin/emax:  Minimum and Maximum range of Energy (meV)
    '''
    print(str(datetime.datetime.now()) + "New Q/E Signal ROI at Q=[{0},{1}] E=[{2},{3}]".format(qmin,qmax,emin,emax))
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
    print(str(datetime.datetime.now()) + "New Q/E Background ROI at Q=[{0},{1}] E=[{2},{3}]".format(qmin,qmax,emin,emax))
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
    print(str(datetime.datetime.now()) + "New X/Y Signal ROI at 2Theta=[{0},{1}] Phi=[{2},{3}]".format(tthmin,tthmax,phimin,phimax))
    tthpixel=[291-(2.236*abs(3.8-tthmin)),291-(2.236*abs(3.8-tthmax))]
    tthsize=2.236*abs(tthmax-tthmin)
    phipixel=[67.0-(4.267*phimin),67.0-(4.267*phimax)]
    phisize=4.267*abs(phimax-phimin)    
    caput('BL5:Det:N1:Det1:XY:ROI:1:MinX',int(np.amin(tthpixel)))
    caput('BL5:Det:N1:Det1:XY:ROI:1:SizeX',int(tthsize))
    caput('BL5:Det:N1:Det1:XY:ROI:1:MinY',int(np.amin(phipixel)))
    caput('BL5:Det:N1:Det1:XY:ROI:1:SizeY',int(phisize))

def BROIxy(tthmin,tthmax,phimin,phimax):
    '''
    This function changes the limits of the Background ROI on the X/Y plot.
    param   tthmin/tthmax:  Minimum and Maximum range of 2 Theta (Degree)
    param   phimin/phimax:  Minimum and Maximum range of Phi (Degree)
    '''
    print(str(datetime.datetime.now()) + "New X/Y Background ROI at 2Theta=[{0},{1}] Phi=[{2},{3}]".format(tthmin,tthmax,phimin,phimax))
    tthpixel=[291-(2.236*abs(3.8-tthmin)),291-(2.236*abs(3.8-tthmax))]
    tthsize=2.236*abs(tthmax-tthmin)
    phipixel=[67.0-(4.267*phimin),67.0-(4.267*phimax)]
    phisize=4.267*abs(phimax-phimin)    
    caput('BL5:Det:N1:Det1:XY:ROI:2:MinX',int(np.amin(tthpixel)))
    caput('BL5:Det:N1:Det1:XY:ROI:2:SizeX',int(tthsize))
    caput('BL5:Det:N1:Det1:XY:ROI:2:MinY',int(np.amin(phipixel)))
    caput('BL5:Det:N1:Det1:XY:ROI:2:SizeY',int(phisize))











