# Standard Python support
import atexit
import code
import logging
import time
import datetime
import sys
import os
import threading
import cPickle as pickle
import re
import math
import shelve
        
# EPICS support
from sns.ca_client import cainit, caget, caput, CAThread
from pcaspy import Driver
from Util.RingLogHandler import RingLogHandler
from Util.Autosave import Autosave
from DAS.CAServerThread import CAServerThread, threads
from beamline_scan import scan_settings, Start, Stop, CommandSequence, Set
from beamline_scan import Delay, Wait, Comment, scan_client, StartForStepping
from beamline_scan import StartForAlignment, StopForAlignment, StartStep
from beamline_scan import Parallel, EndStep
import os
#from matplotlib.sphinxext.plot_directive import template
from os.path import join
#from numpy import rate
prefix = os.environ['BL']    # 'BL5'
pv_prefix = prefix + ':CS:NestedLoops:'


def simulateScan(self):
    simulation = []
    simulation.extend(self.strToAscii('\n'))
    self.setParam('Simulation', simulation)
    self.updatePVs()
    scanCount = 1
    totaltime = 0
        
    for cmds in self.cmdSeqList:
        result = scan_client.simulate(cmds)
        for key,value in result.iteritems():
            if key == 'seconds':
               totaltime += value
                            
            simulation.extend(self.strToAscii(result['simulation']))
            self.setParam('TotalSimTime', self.formatSeconds(totaltime))
            self.setParam('Simulation', simulation)
            self.setParam('Status', 'Scan %d/%d successfully simulated.'%(scanCount, self.numScans))
            self.setParam('Status', 'All scans successfully simulated.')

