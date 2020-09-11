"""

"""

run_number = 318700

LoadEventNexus(Filename='/SNS/CNCS/IPTS-22728/nexus/CNCS_{}.nxs.h5'.format(run_number), OutputWorkspace='CNCS_{}'.format(run_number), LoadMonitors=True)

#uncomment here if you want to look at the TOF data
#SumSpectra(InputWorkspace='CNCS_{}', OutputWorkspace='CNCS_{}_summed')
#Rebin(InputWorkspace='CNCS_{}_summed', OutputWorkspace='CNCS_{}_summed', Params='10')

Rebin(InputWorkspace='CNCS_{}'.format(run_number), OutputWorkspace='CNCS_{}_nxs_Rebin'.format(run_number), Params='49500, 1000, 50500', PreserveEvents=False)

#mask out undesired regions of the detector array
MaskBTP(Workspace = 'CNCS_{}_nxs_Rebin'.format(run_number), Instrument = 'CNCS', Bank = '35-39')
MaskBTP(Workspace = 'CNCS_{}_nxs_Rebin'.format(run_number), Instrument = 'CNCS', Pixel = '121-128')
MaskBTP(Workspace = 'CNCS_{}_nxs_Rebin'.format(run_number), Instrument = 'CNCS', Pixel = '1-8')

#normalize to the value of 1 as always done in DGS group
intensity_array = mtd['CNCS_{}_nxs_Rebin'.format(run_number)].extractY()
intensity_mean = float(intensity_array[intensity_array>0].mean())
CreateSingleValuedWorkspace(OutputWorkspace='intensity_mean_ws',DataValue=intensity_mean)
Divide(LHSWorkspace='CNCS_{}_nxs_Rebin'.format(run_number),RHSWorkspace='intensity_mean_ws',OutputWorkspace='normalized_vanadium') #Divide the vanadium by the mean
#Multiply(LHSWorkspace='reduce',RHSWorkspace='__meanval',OutputWorkspace='reduce') #multiple by the mean of vanadium Normalized data = Data / (Van/meanvan) = Data *meanvan/Van


#save the processed vanadium file
SaveNexus(InputWorkspace="normalized_vanadium", Filename= '/SNS/CNCS/IPTS-22728/shared/autoreduce/processed_van_{}_no_beamstop_30C.nxs'.format(run_number)) 

normalized_vanadium_intensity_array = mtd['normalized_vanadium'].extractY()
normalized_vanadium_intensity_mean = float(normalized_vanadium_intensity_array[normalized_vanadium_intensity_array>0].mean())

print(intensity_mean)
print(normalized_vanadium_intensity_mean)
