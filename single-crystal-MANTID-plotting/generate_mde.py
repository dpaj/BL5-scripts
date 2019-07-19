import sys
sys.path.insert(0,"/opt/mantidnightly/bin")
from mantid.simpleapi import *
import numpy

def flipping_ratio(angle,**kwargs):
    averageFR=kwargs.pop('AverageFR')
    ampl=kwargs.pop('CosineAmplitudeFR')
    phase=kwargs.pop('CosinePhaseFR')
    return averageFR+ampl*numpy.cos(2*numpy.radians(angle+phase))

def polarizer_transmission(ws,**kwargs):
    EFixed=ws.run()['Ei'].value
    #DeltaE-Ei=-Ef
    ws=ScaleX(ws,Factor=-EFixed,Operation="Add")
    ws=ExponentialCorrection(ws,C0=1/0.585,C1=1/10.77,Operation="Multiply") #was 58.5% *exp(-Ef/12.07)
    ws=ScaleX(ws,Factor=EFixed,Operation="Add")
    return ws

def convert_to_chi(ws,temperature, Emin_apply_DB):
    ws_low=CropWorkspace(ws,XMax=Emin_apply_DB)
    ws_high=CropWorkspace(ws,XMin=Emin_apply_DB)
    ws_high=ApplyDetailedBalance(InputWorkspace=ws_high, Temperature=temperature)
    return ws_low+ws_high

def Ef_correction(ws,psda=0,**kwargs):
    temperature=kwargs.pop('Temperature',None)
    if temperature:
        Emin_apply_DB=kwargs.pop('Emin_apply_DB',ws.readX(0)[0])
        ws=convert_to_chi(ws,temperature, Emin_apply_DB)
    if(psda!=0):
        ws=polarizer_transmission(ws)
    return ws

def detector_geometry_correction(ws,psda=0.):
    if (psda):
        run_obj = ws.getRun()
        psr=run_obj['psr'].getStatistics().mean
        offset=psda*(1.-psr/4200.)
        RotateInstrumentComponent(Workspace=ws,ComponentName='Tank',
                                  X=0, Y=1,Z=0,
                                  Angle=offset,RelativeRotation=1)
    return ws

def generate_mde(filenames,mde_ws_name,**kwargs):
    """
    filenames is a list
    """
    Ei_supplied=kwargs.pop('Ei',None)
    T0_supplied=kwargs.pop('T0',None)
    psda_supplied=kwargs.pop('psda',None)
    tib_min_supplied=kwargs.pop('Tib_min',None)
    tib_max_supplied=kwargs.pop('Tib_max',None)
    omega_motor_name=kwargs.pop('OmegaMotorName',None)
    E_min_supplied=kwargs.pop('E_min',None)
    E_max_supplied=kwargs.pop('E_max',None)
    mask_workspace=kwargs.pop('MaskWorkspace',None)
    Ef_correction_function_module=kwargs.pop('EfCorrectionFunctionModule','default_Ef_correction')
    filter_pulses_threshold=kwargs.pop('FilterBadPulsesThreshold',None)
    
    config['default.facility'] = "SNS"
    FR_C1=[] #FR/(FR-1.)
    FR_C2=[] #1./(FR-1.)
    for num,filename in enumerate(filenames):
        data=LoadEventNexus(filename)
        name = data.getInstrument().getName()
        if len(CheckForSampleLogs(Workspace = data, LogNames = 'pause')) == 0:
            data = FilterByLogValue(InputWorkspace = data, 
                                    LogName = 'pause', 
                                    MinimumValue = -1,
                                    MaximumValue = 0.5)
        if(filter_pulses_threshold):
            data = FilterBadPulses(InputWorkspace = data, LowerCutoff = filter_pulses_threshold)
        if(mask_workspace):
            MaskDetectors(Workspace=data, MaskedWorkspace=mask_workspace)
        else:
            MaskBTP(Workspace=data,Pixel="1-8,121-128")
        print("Goniometer name:")
        print(omega_motor_name)    
        if omega_motor_name:
            SetGoniometer(Workspace=data,Axis0=omega_motor_name+',0,1,0,1')
            
        run_obj = data.getRun()
        if name == 'HYSPEC' or name == 'CNCS':
           Ei = Ei_supplied if Ei_supplied else run_obj['EnergyRequest'].getStatistics().mean
           T0=T0_supplied if T0_supplied else GetEi(data).Tzero
        else:
           data_m=LoadNexusMonitors(filename)
           Ei,T0=GetEiT0atSNS(data_m)
        Emin = E_min_supplied if E_min_supplied else -0.5*Ei
        Emax = E_max_supplied if E_max_supplied else 0.95*Ei
        Erange='{},{},{}'.format(Emin,(Emax-Emin)*0.2,Emax)
        
        #get tofmin and tofmax, and filter out anything else ONLY for HYSPEC
        if name == 'HYSPEC':
           msd = run_obj['msd'].getStatistics().mean
           tel = (39000+msd+4500)*1000/numpy.sqrt(Ei/5.227e-6)
           tofmin = tel-1e6/120-470
           tofmax = tel+1e6/120+470
           data = CropWorkspace(InputWorkspace = data, XMin = tofmin, XMax = tofmax)    

           psda = psda_supplied if (psda_supplied is not None) else run_obj['psda'].getStatistics().mean
           data=detector_geometry_correction(data,psda=psda)
        
        #TIB limits
        if name == 'HYSPEC' and Ei==15:
           tib=[22000.,23000.]
        elif name == 'HYSPEC':
           tib = SuggestTibHYSPEC(Ei)
        elif name == 'CNCS':
           tib = SuggestTibCNCS(Ei) 
        else:
           tib=[0.0,0.1]   
        tib_min= tib_min_supplied if tib_min_supplied else tib[0]
        tib_max= tib_max_supplied if tib_max_supplied else tib[1]
        
        #convert to energy transfer
        if name == 'HYSPEC' or name == 'CNCS':
           dgs,_=DgsReduction(SampleInputWorkspace=data,
                           SampleInputMonitorWorkspace=data,
                           IncidentEnergyGuess=Ei,
                           TimeZeroGuess=T0,
                           UseIncidentEnergyGuess=True,
                           IncidentBeamNormalisation='None',
                           EnergyTransferRange=Erange,
                           TimeIndepBackgroundSub=True,
                           TibTofRangeStart=tib_min,
                           TibTofRangeEnd=tib_max,
                           CorrectKiKf=True,
                           SofPhiEIsDistribution=False)
        else:
           dgs,_=DgsReduction(SampleInputWorkspace=data,
                           SampleInputMonitorWorkspace=data_m,
                           IncidentEnergyGuess=Ei,
                           TimeZeroGuess=T0,
                           UseIncidentEnergyGuess=True,
                           IncidentBeamNormalisation='None',
                           EnergyTransferRange=Erange,
                           TimeIndepBackgroundSub=False,
                           CorrectKiKf=True,
                           SofPhiEIsDistribution=False)
        dgs=CropWorkspaceForMDNorm(InputWorkspace=dgs, XMin = Emin, XMax = Emax)
        
        #Ef corrections
        if name == 'HYSPEC':
           if Ef_correction_function_module=='default_Ef_correction':
               dgs=Ef_correction(dgs,psda=psda,**kwargs)
           elif Ef_correction_function_module=='no_corrections':
               pass
           else:
               import importlib
               mod = importlib.import_module(Ef_correction_function_module)
               dgs=mod.Ef_correction(dgs,psda=psda,**kwargs)

        minValues,maxValues=ConvertToMDMinMaxGlobal(InputWorkspace=dgs,
                                                    QDimensions='Q3D',
                                                    dEAnalysisMode='Direct',
                                                    Q3DFrames='Q')
        ConvertToMD(InputWorkspace=dgs,
                    QDimensions='Q3D',
                    dEAnalysisMode='Direct',
                    Q3DFrames="Q_sample",
                    MinValues=minValues,
                    MaxValues=maxValues,
                    OutputWorkspace="__{0}_{1}".format(mde_ws_name,num))
        
        #Polarisation mode
        if name == 'HYSPEC':
           if(psda!=0):
             FRdict={'AverageFR':9.,'CosineAmplitudeFR':0,'CosinePhaseFR':0}
             for key in FRdict.keys():
                 if kwargs.has_key(key):
                     FRdict[key]=kwargs[key] 
             angle_name=omega_motor_name if omega_motor_name else 'omega'
             angle=run_obj[angle_name].getStatistics().mean
             FR=flipping_ratio(angle,**FRdict)
             C1=CreateSingleValuedWorkspace(FR/(FR-1.))
             MultiplyMD("__{0}_{1}".format(mde_ws_name,num),C1, 
                        OutputWorkspace="__{0}_{1}_FR_C1".format(mde_ws_name,num))
             FR_C1.append("__{0}_{1}_FR_C1".format(mde_ws_name,num))
             C2=CreateSingleValuedWorkspace(1./(FR-1.))
             MultiplyMD("__{0}_{1}".format(mde_ws_name,num),C2, 
                        OutputWorkspace="__{0}_{1}_FR_C2".format(mde_ws_name,num))
             FR_C2.append("__{0}_{1}_FR_C2".format(mde_ws_name,num))
        
    MergeMD(','.join(["__{}_{}".format(mde_ws_name,num) for num in range(len(filenames))]),
            OutputWorkspace=mde_ws_name)
    if FR_C1:
        MergeMD(','.join(FR_C1),OutputWorkspace=mde_ws_name+'_FR_C1')
        MergeMD(','.join(FR_C2),OutputWorkspace=mde_ws_name+'_FR_C2')
            

