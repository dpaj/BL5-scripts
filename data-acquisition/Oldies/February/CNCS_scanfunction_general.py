from epics import caget, caput, PV, cainfo
from scan import *
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

def setWL(wl):
    cmds.append(Set('BL5:Chop:Skf1:WavelengthUserReq', wl, completion = True)) # Is it implemented ???
    hystory.append('BL5:Chop:Skf1:WavelengthUserReq')
    print(str(datetime.datetime.now()) + " ...Set Wavelength to " + str(wl) + " A")

def cmdsetWL(wl):
    caput('BL5:Chop:Skf1:WavelengthUserReq', wl) # Is it implemented ???
    print(str(datetime.datetime.now()) + " ...Set Wavelength to " + str(wl) + " A")

##

def setEnergy(Energy):
    cmds.append(Set('BL5:Chop:Gbl:EnergyReq', Energy, completion = True))
    hystory.append('BL5:Chop:Gbl:EnergyReq')
    print(str(datetime.datetime.now()) + " ...Set Incident Energy to " + str(Energy) + " meV")

def cmdsetEnergy(Energy):
    caput('BL5:Chop:Gbl:EnergyReq', Energy)
    print(str(datetime.datetime.now()) + " ...Set Incident Energy to " + str(Energy) + " meV")

##

def setTitle(title):
    cmds.append(Set('BL5:SMS:RunInfo:RunTitle', title))
    hystory.append('BL5:SMS:RunInfo:RunTitle')
    print(str(datetime.datetime.now()) + " ...Set Title: {0} ".format(title))

def cmdsetTitle(title):
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
    cmds.append(Set('BL5:Chop:Skf1:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf1:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Fermi Chopper frequency to " + str(hz) + " Hz, and wait for completion")

def cmdFermifreq(hz):
    caput('BL5:Chop:Skf1:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Fermi Chopper frequency to " + str(hz) + " Hz, and wait for completion")

##

def Chop2freq(hz):
    cmds.append(Set('BL5:Chop:Skf2:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf2:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Chopper 2 frequency to " + str(hz) + " Hz, and wait for completion")

def cmdChop2freq(hz):
    caput('BL5:Chop:Skf2:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Chopper 2 frequency to " + str(hz) + " Hz, and wait for completion")

##

def Chop3freq(hz):
    cmds.append(Set('BL5:Chop:Skf3:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf3:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Chopper 3 frequency to " + str(hz) + " Hz, and wait for completion")

def cmdChop3freq(hz):
    caput('BL5:Chop:Skf3:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Chopper 3 frequency to " + str(hz) + " Hz, and wait for completion")

##

def Chop4freq(hz):
    cmds.append(Set('BL5:Chop:Skf4:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf4:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Chopper 4 frequency to " + str(hz) + " Hz, and wait for completion")

def cmdChop4freq(hz):
    caput('BL5:Chop:Skf4:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Chopper 4 frequency to " + str(hz) + " Hz, and wait for completion")

##

def Chop5freq(hz):
    cmds.append(Set('BL5:Chop:Skf5:SpeedReq', hz, completion = True))
    hystory.append('BL5:Chop:Skf5:SpeedReq')
    print(str(datetime.datetime.now()) + " ...Setting Chopper 5 frequency to " + str(hz) + " Hz, and wait for completion")

def cmdChop5freq(hz):
    caput('BL5:Chop:Skf5:SpeedReq', hz)
    print(str(datetime.datetime.now()) + " ...Setting Chopper 5 frequency to " + str(hz) + " Hz, and wait for completion")

##

# Need to check this command
def GChopfreq(hz1,hz2,hz3,hz4,hz5):
    cmds.append(Set('+p BL5:Chop:Skf1:SpeedReq', hz1, completion = True))
    cmds.append(Set('+p BL5:Chop:Skf2:SpeedReq', hz2, completion = True))
    cmds.append(Set('+p BL5:Chop:Skf3:SpeedReq', hz3, completion = True))
    cmds.append(Set('+p BL5:Chop:Skf4:SpeedReq', hz4, completion = True))
    cmds.append(Set('+p BL5:Chop:Skf5:SpeedReq', hz5, completion = True))
    hystory.append('Changed:Global:Chopper:Frequqncies')
    print(str(datetime.datetime.now()) + " ...Setting Chopper frequencis to " + str(hz1,hz2,hz3,hz4,hz5) + " Hz, and wait for completion")

# Need to check this command
def cmdGChopfreq(hz1,hz2,hz3,hz4,hz5):
    caput('+p BL5:Chop:Skf1:SpeedReq', hz1)
    caput('+p BL5:Chop:Skf2:SpeedReq', hz2)
    caput('+p BL5:Chop:Skf3:SpeedReq', hz3)
    caput('+p BL5:Chop:Skf4:SpeedReq', hz4)
    caput('+p BL5:Chop:Skf5:SpeedReq', hz5)
    print(str(datetime.datetime.now()) + " ...Setting Chopper frequencis to " + str(hz1,hz2,hz3,hz4,hz5) + " Hz, and wait for completion")

# Need to check this command for adding delays
def delay(time):
    global timetotal
    timetotal = timetotal + time
    print("...Delay " + str(time) + " seconds")
    return cmds.append(Delay(time))

# Need to check this command to Reset the command line
def newscan():
    global cmds
    print("...Resetting cmds and history for a new scan.")
    cmds = []
    hystory = []

#######################################################################################
##################################### Motors Stage ####################################
#######################################################################################

def driveOmega(value):
    cmds.append(Set('BL5:Mot:Sample:Axis1', value, completion = True))
    hystory.append('BL5:Mot:Sample:Axis1')
    print(str(datetime.datetime.now()) + " ...Drive Omega to " + str(value) + " Degree")

def cmddriveOmega(value):
    caput('BL5:Mot:Sample:Axis1', value)
    print(str(datetime.datetime.now()) + " ...Drive Omega to " + str(value) + " Degree")

##

def driveOC(value):
    cmds.append(Set('BL5:Mot:Sample:Axis2', value, completion = True))
    hystory.append('BL5:Mot:Sample:Axis2')
    print(str(datetime.datetime.now()) + " ...Drive Orange Cryo to " + str(value) + " Degree")

def cmddriveOC(value):
    caput('BL5:Mot:Sample:Axis2', value)
    print(str(datetime.datetime.now()) + " ...Drive Orange Cryo to " + str(value) + " Degree")

##

def move3sample(value):
    cmds.append(Set('BL5:Mot:Sample:Axis1', value, completion = True))
    hystory.append('BL5:Mot:Sample:Axis1')
    print(str(datetime.datetime.now()) + " ...Move 3-Sample Stick to " + str(value) + " Degree")

def cmdmove3sample(value):
    caput('BL5:Mot:Sample:Axis1', value)
    print(str(datetime.datetime.now()) + " ...Move 3-Sample Stick to " + str(value) + " Degree")

##

def movesampleZ(value):
    cmds.append(Set('BL5:Mot:sampleZ', value, completion = True))
    hystory.append('BL5:Mot:sampleZ')
    print(str(datetime.datetime.now()) + " ...Move Sample Z to " + str(value) + " mm")

def cmdmovesampleZ(value):
    caput('BL5:Mot:sampleZ', value)
    print(str(datetime.datetime.now()) + " ...Move Sample Z to " + str(value) + " mm")

##

def movehuber(value):
    cmds.append(Set('BL5:Mot:huber', value, completion = True))
    hystory.append('BL5:Mot:huber')
    print(str(datetime.datetime.now()) + " ...Move huber to " + str(value) + " Degree")

def cmdmovehuber(value):
    caput('BL5:Mot:huber', value)
    print(str(datetime.datetime.now()) + " ...Move huber to " + str(value) + " Degree")

##

def beamstopL(pos):
    cmds.append(Set('BL5:Mot:beamstopL', pos, completion = True))
    hystory.append('BL5:Mot:beamstopL')
    print(str(datetime.datetime.now()) + " ...Set Beamstop Left : "+str(pos)+" mm")

def cmdbeamstopL(pos):
    caput('BL5:Mot:beamstopL', pos)
    print(str(datetime.datetime.now()) + " ...Set Beamstop Left : "+str(pos)+" mm")

##

def beamstopR(pos):
    cmds.append(Set('BL5:Mot:beamstopR', pos, completion = True))
    hystory.append('BL5:Mot:beamstopR')
    print(str(datetime.datetime.now()) + " ...Set Beamstop Right : "+str(pos)+" mm")

def cmdbeamstopR(pos):
    caput('BL5:Mot:beamstopR', pos)
    print(str(datetime.datetime.now()) + " ...Set Beamstop Right : "+str(pos)+" mm")

##############
def collimator(args):
    if args.lower() == 'on' or args.lower() == 'start' :
        print("Rotate Radial Collimator")
        cmds.append(Set('BL5:Mot:Colli:MotionMenu', 1, completion = False))
    elif args.lower() == 'off' or args.lower() =='stop':
        print("Stop Radial Collimator")
        cmds.append(Set('BL5:Mot:Colli:MotionMenu', 0, completion = False))
    else:
        raise Exception("Unknown arguments. (start, stop, on, off)")

def cmdcollimator(args):
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
    print "...Submitting the scan : " + scantitle
    id = client.submit(cmds, scantitle)
    print "...scan id = " + str(id)
    newscan()  # after submission, reset the cmds list every time

def simulate(scantitle=os.path.basename(sys.argv[0])):
    print "...Simulating the scan : " + scantitle
    simulation = client.simulate(cmds)
    print simulation

# Need to check this PV
def start():
    return cmds.append(Set('BL5:CS:RunControl:Start', 1, completion = True))

# Need to check this PV
def stop():
    return cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion = True))

# Need to check this PV
def startdiag():
    return cmds.append(Set('BL5:Det:ADnED:Start', 1, completion = True))

# Need to check this PV
def stopdiag():
    return cmds.append(Set('BL5:Det:ADnED:Stop', 1, completion = True))

def waitPC(value):
    global pctotal
    pctotal = pctotal + value
    return cmds.append(Wait('BL5:Det:PCharge:C', value, comparison='increase by'))

def waitS(value):
    global timetotal
    timetotal = timetotal + value
    return cmds.append(Wait('BL5:CS:RunControl:RunTimer', value, comparison='increase by'))

def estimatetime():
    print ".Total PC = %.2f C \n..........= %.2f hours (%.1f min) at 1.2 MW \n..........= %.2f hours (%.1f min) at 1.0 MW \n..........= %.2f hours (%.1f min) at 0.85 MW"  % (pctotal , 	pctotal/4.32, pctotal/4.32*60 , pctotal/3.6, pctotal/3.6*60, pctotal/3.0, pctotal/3.0*60)
    print ".Other time = %.1f s = %.2f hours" %(timetotal, timetotal/3600)

def resettime(): # reset time counter
    global pctotal
    global timetotal
    pctotal = 0.0
    timetotal = 0

#############################################################################################################


def drive(pv, value , wait=True):
	if pv.lower() == 'omega' or pv.lower() == 'axis1' :
		driveOmega(value)
	elif pv.lower() == '3sample' :
		move3sample(value)
	elif pv.lower() == 'omegaoc' or pv.lower() == 'axis2' or pv.lower() == 'oc' :
		driveOC(value)
	else:
		print("...Not a predefined PV. Check PV spelling.")

##

def cmddrive(pv, value):
    if pv.lower() == 'omega' or pv.lower() == 'axis1' :
        driveOmegacmd(value)
    elif pv.lower() == '3sample' :
        move3samplecmd(value)
    elif pv.lower() == 'omegaoc' or pv.lower() == 'axis2' or pv.lower() == 'oc' :
        driveOCcmd(value)
    else:
        print("...Not a predefined PV. Check PV spelling.")

#############

def set(pv, value, wait=True):
    """
    generalized command to set PVs
    """
    if pv.lower() == 'samplez' :
        movesampleZ(value)
    elif pv.lower() == 'beamstopl' :
        beamstopL(value)
    elif pv.lower() == 'beamstopr':
        beamstopR(value)
    elif pv.lower() == 'huberrot':
        movehuber(value)
    elif pv.lower() == 'collimator':
        collimator(value)
    elif pv.lower() == 'energy':
        setEnergy(value)
    elif pv.lower() == 'wl':
        setWL(value)
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
    elif pv.lower() == 'axis1' or pv.lower()=='omega' :
        driveOmega(value)
    elif pv.lower() == 'axis2' or pv.lower()=='omegaoc' or pv.lower()=='oc':
        driveOC(value)
    elif pv.lower() == '3sample' :
        move3sample(value)
    elif pv.lower() == 'title' :
        setTitle(value)
    else:
        print("...Not a predefined PV. Processing as a raw command.")
        cmds.append(Set(pv, value, completion = wait))

##

def cmdset(pv, value):
    """
        generalized command to set PVs
        """
    if pv.lower() == 'samplez' :
        cmdmovesampleZ(value)
    elif pv.lower() == 'beamstopl' :
        cmdbeamstopL(value)
    elif pv.lower() == 'beamstopr':
        cmdbeamstopR(value)
    elif pv.lower() == 'huberrot':
        cmdmovehuber(value)
    elif pv.lower() == 'collimator':
        cmdcollimator(value)
    elif pv.lower() == 'energy':
        cmdsetEnergy(value)
    elif pv.lower() == 'wl':
        cmdsetWL(value)
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
    elif pv.lower() == 'axis1' or pv.lower()=='omega' :
        cmddriveOmega(value)
    elif pv.lower() == 'axis2' or pv.lower()=='omegaoc' or pv.lower()=='oc':
        cmddriveOC(value)
    elif pv.lower() == '3sample' :
        cmdmove3sample(value)
    elif pv.lower() == 'title' :
        cmdsetTitle(value)
    else:
        print("...Not a predefined PV. Processing as a raw command.")
        caput(pv, value)

############ A for loop has been tested on 12 Feb 2018 ##############

def runexp(title, energy, pos, args, value): 
    if args.lower() == 'pc' :
        global pctotal
        pctotal = pctotal + value
        cmds.append(Set('BL5:SMS:RunInfo:RunTitle', title + "_" + str(energy) + "meV_" + str(pos)))
        cmds.append(Set('BL5:Chop:Gbl:EnergyReq', energy))
        cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
        cmds.append(Wait('BL5:Det:PCharge:C', value, comparison='increase by'))
        cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
        print(str(datetime.datetime.now()) + " ...Set measurement for " + title + " at position " + str(pos))
    elif args.lower() == 'time' :
        global timetotal
        timetotal = timetotal + value
        cmds.append(Set('BL5:SMS:RunInfo:RunTitle', title + "_" + str(energy) + "meV_" + str(pos)))
        cmds.append(Set('BL5:Chop:Gbl:EnergyReq', energy))
        cmds.append(Set('BL5:CS:RunControl:Start', 1, completion=True))
        cmds.append(Wait('BL5:CS:RunControl:RunTimer', value, comparison='increase by'))
        cmds.append(Set('BL5:CS:RunControl:Stop', 1, completion=True))
        print(str(datetime.datetime.now()) + " ...Set measurement for " + title + " at position " + str(pos))

############ These ones Need to Be Tested with Beam On ############

def cmdscan(pv, min, max, step, value):
    runs=loop(min,max,step)
    for r in runs:
        print(str(datetime.datetime.now()) + " ...Scanning " + pv + " at " + str(r))
        caput('BL5:SMS:RunInfo:RunTitle',"Scan_" + pv + "_" + str(r))
        caput(pv,r)
        caput('BL5:CS:RunControl:Start', 1)
        Wait('BL5:Det:PCharge:C', value, comparison='increase by')
        caput('BL5:CS:RunControl:Stop', 1)

def cmdscanrel(pv, min, max, step, value):
    center=caget(pv)
    runs=loop((center-min),(center+max), step)
    for r in runs:
        print(str(datetime.datetime.now()) + " ...Rel Scanning " + pv + " at " + str(r))
        caput('BL5:SMS:RunInfo:RunTitle',"Scanrel_" + pv + "_" + str(r))
        caput(pv,r)
        caput('BL5:CS:RunControl:Start', 1)
        Wait('BL5:Det:PCharge:C', value, comparison='increase by')
        caput('BL5:CS:RunControl:Stop', 1)

#def Braggcmd():

############

# CNCS checked on 12th Feb 2018
def loadconf(file_name):
	config_path = "/home/bl-user/Script_Test/CNCS_config/" + file_name
	print("...Use Configuration file " + config_path)
	with open(config_path,'r') as filec:
		for line in filec:
			data=line.split(' ')
			caput(data[0],data[1])
			print("{0} {1}".format(data[0],data[1]))			
			

# CNCS checked on 12th Feb 2018
def saveconf(file_name):
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

############





