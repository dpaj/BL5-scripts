"""

"""

LoadEventNexus(Filename='/SNS/CNCS/IPTS-21344/nexus/CNCS_277537.nxs.h5', OutputWorkspace='CNCS_277537', LoadMonitors=True)

#uncomment here if you want to look at the TOF data
#SumSpectra(InputWorkspace='CNCS_277537', OutputWorkspace='CNCS_277537_summed')
#Rebin(InputWorkspace='CNCS_277537_summed', OutputWorkspace='CNCS_277537_summed', Params='10')

Rebin(InputWorkspace='CNCS_277537', OutputWorkspace='CNCS_277537_nxs_Rebin', Params='49500, 1000, 50500', PreserveEvents=False)

#mask out undesired regions of the detector array
MaskBTP(Workspace = 'CNCS_277537_nxs_Rebin', Instrument = 'CNCS', Bank = '35-39')
MaskBTP(Workspace = 'CNCS_277537_nxs_Rebin', Instrument = 'CNCS', Pixel = '121-128')
MaskBTP(Workspace = 'CNCS_277537_nxs_Rebin', Instrument = 'CNCS', Pixel = '1-8')

#normalize to the value of 1 as always done in DGS group
intensity_array = mtd['CNCS_277537_nxs_Rebin'].extractY()
intensity_mean = float(intensity_array[intensity_array>0].mean())
CreateSingleValuedWorkspace(OutputWorkspace='intensity_mean_ws',DataValue=intensity_mean)
Divide(LHSWorkspace='CNCS_277537_nxs_Rebin',RHSWorkspace='intensity_mean_ws',OutputWorkspace='normalized_vanadium') #Divide the vanadium by the mean
#Multiply(LHSWorkspace='reduce',RHSWorkspace='__meanval',OutputWorkspace='reduce') #multiple by the mean of vanadium Normalized data = Data / (Van/meanvan) = Data *meanvan/Van


#save the processed vanadium file
SaveNexus(InputWorkspace="normalized_vanadium", Filename= '/SNS/CNCS/IPTS-20360/shared/vanadium_files/custom_processed_van_277537.nxs') 

normalized_vanadium_intensity_array = mtd['normalized_vanadium'].extractY()
normalized_vanadium_intensity_mean = float(normalized_vanadium_intensity_array[normalized_vanadium_intensity_array>0].mean())

print(intensity_mean)
print(normalized_vanadium_intensity_mean)
