#!/usr/bin/env python

import sys,os
sys.path.append("/opt/Mantid/bin")
from mantid.simpleapi import *
#from mantid import apiVersion
#apiVersion()

config['default.facility']="SNS"
nexus_file=sys.argv[1]
output_directory=sys.argv[2]

print nexus_file
print output_directory 

DgsReduction(
             SampleInputFile=nexus_file,
             OutputWorkspace="reduce",
             HardMaskFile="/SNS/CNCS/shared/autoreduce/mask8bothsides.xml",
             IncidentBeamNormalisation="ByCurrent",
#             IncidentEnergyGuess=3.316,
#             UseIncidentEnergyGuess=True,
#             TimeZeroGuess=76.0,
             TimeIndepBackgroundSub=True,
             TibTofRangeStart=42000.0,
             TibTofRangeEnd=45000.0,
#             DetectorVanadiumInputFile="/SNS/CNCS/IPTS-6343/0/57514/NeXus/CNCS_57514_event.nxs",
             DetectorVanadiumInputFile="/SNS/CNCS/shared/autoreduce/CNCS_57514_event.nxs",
             UseBoundsForDetVan=True,
             DetVanIntRangeLow=52000.0,
             DetVanIntRangeHigh=53000.0,
             DetVanIntRangeUnits="TOF"
            )

filename = os.path.split(nexus_file)[-1]
#run_number = filename.split('_')[1]
run_number = os.path.splitext(os.path.splitext(filename.split('_')[1])[0])[0]
processed_filename = os.path.join(output_directory, "CNCS_" + run_number + "_spe.nxs")
nxspe_filename=os.path.join(output_directory, "CNCS_" + run_number + ".nxspe")
# Get Angle
s1=mtd["reduce"].getRun()['SERotator2'].value[0]
# Save a file
SaveNexus(Filename=processed_filename, InputWorkspace="reduce")
SaveNXSPE(Filename=nxspe_filename, InputWorkspace="reduce", Psi=str(s1), KiOverKfScaling='1')
