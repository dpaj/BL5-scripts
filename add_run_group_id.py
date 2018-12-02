sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *


data_directory = '/SNS/CNCS/shared/BL5-example-nxs/'
output_directory = '/SNS/CNCS/shared/BL5-example-nxs/'

run_numbers = [290146]

for run in run_numbers:
    Load(Filename=data_directory+'CNCS_{0}.nxs.h5'.format(run), OutputWorkspace='CNCS_{0}.nxs', LoaderName='LoadEventNexus', LoaderVersion='1')
    AddSampleLog(Workspace='CNCS_{0}.nxs', LogName='run_group_id', LogText='room temp, Ei=12 meV, September, 001 vertical')
    SaveNexus(InputWorkspace='CNCS_{0}.nxs', Filename=output_directory+'CNCS_{0}_mod.nxs.h5'.format(run))
    Load(Filename=output_directory+'CNCS_{0}_mod.nxs.h5'.format(run), OutputWorkspace='CNCS_{0}_mod.nxs')
    #DeleteWorkspace('CNCS_{0}.nxs.h5')