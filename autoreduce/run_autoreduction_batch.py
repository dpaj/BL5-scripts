import sys
sys.path.append("/opt/Mantid/bin")
import mantid, subprocess
from mantid import simpleapi as api

runs=range(166769,166775)
arscript="/SNS/CNCS/shared/autoreduce/reduce_CNCS.py" #replace with the one in the IPTS folder
outputdir="/tmp/" #Use the full path (/SNS/CNCS/IPTS-....). Needs the final /

alg = api.AlgorithmManager.createUnmanaged("Load")
alg.initialize()

for r in runs:
    alg.setPropertyValue('Filename',"CNCS_"+str(r))
    filename=alg.getProperty('Filename').value[0]
    print "Processing "+str(filename)
    cmd="python "+arscript+" "+filename+" "+outputdir
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
