from __future__ import (absolute_import, division, print_function)
# This is a general reduction script to produce an MDEvent workspace in
# Q_sample units, to be used in conjunction with MDNorm
# It works with Mantid 4.0. If nightly is required, uncomment the two lines below.
#import sys
#sys.path.insert(0,"/opt/mantidnightly/bin")
from mantid.simpleapi import *
import numpy


def polarizer_transmission(ws,**kwargs):
    '''
    Hyspec polarizer transmission correction. If used it will
    undo the effect of the attenuation as a function of E_final
    '''
    EFixed=ws.run()['Ei'].value
    #DeltaE-Ei=-Ef
    ws=ScaleX(ws,Factor=-EFixed,Operation="Add")
    ws=ExponentialCorrection(ws,C0=1/0.585,C1=1/10.77,Operation="Multiply") #was 58.5% *exp(-Ef/12.07)
    ws=ScaleX(ws,Factor=EFixed,Operation="Add")
    return ws


def convert_to_chi(ws,temperature, Emin_apply_DB):
    '''
    Utility to convert to chi" above a minimum threshold in DeltaE
    '''
    ws_low=CropWorkspace(ws,XMax=Emin_apply_DB)
    ws_high=CropWorkspace(ws,XMin=Emin_apply_DB)
    ws_high=ApplyDetailedBalance(InputWorkspace=ws_high, Temperature=temperature)
    return ws_low+ws_high


def Ef_correction(ws,psda=0,temperature=None,Emin_apply_DB=None,**kwargs):
    if temperature:
        if Emin_apply_DB is None:
            Emin_apply_DB=ws.readX(0)[0]
        ws=convert_to_chi(ws,temperature, Emin_apply_DB)
    if(psda!=0):
        ws=polarizer_transmission(ws)
    return ws


def detector_geometry_correction(ws,psda=0.):
    '''
    Account for HYSPEC geometry change in polarized mode
    '''
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
    reduce a set of filenames into an md event workspace
    filenames is a list
    """
    Ei_supplied=kwargs.pop('Ei',None)
    T0_supplied=kwargs.pop('T0',None)
    psda_supplied=kwargs.pop('psda',None)
    psda=0
    perform_tib=kwargs.pop('TimeIndepBackgroundSub',None)
    tib_min_supplied=kwargs.pop('Tib_min',None)
    tib_max_supplied=kwargs.pop('Tib_max',None)
    omega_motor_name=kwargs.pop('OmegaMotorName',None)
    E_min_supplied=kwargs.pop('E_min',None)
    E_max_supplied=kwargs.pop('E_max',None)
    mask_workspace=kwargs.pop('MaskWorkspace',None)
    Ef_correction_function_module=kwargs.pop('EfCorrectionFunctionModule','default_Ef_correction')
    filter_pulses_threshold=kwargs.pop('BadPulsesThreshold',None)
    temperature=kwargs.pop('Temperature',None)
    Emin_apply_DB=kwargs.pop('Emin_apply_DB',None)

    config['default.facility'] = "SNS"

    for num,filename in enumerate(filenames):
        logger.warning("Processing file {0}/{1}".format(num+1,len(filenames)))
        data=LoadEventNexus(filename)
        inst_name = data.getInstrument().getName()
        #TODO: check if corectly adjust proton charge
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
        if omega_motor_name:
            SetGoniometer(Workspace=data,Axis0=omega_motor_name+',0,1,0,1')

        run_obj = data.getRun()
        if inst_name in ['HYSPEC', 'CNCS']:
            Ei = Ei_supplied if Ei_supplied else run_obj['EnergyRequest'].getStatistics().mean
            T0=T0_supplied if (T0_supplied is not None) else GetEi(data).Tzero
        else:
            if (Ei_supplied is not None) and (T0_supplied is not None):
                Ei=Ei_supplied
                T0=T0_supplied    
            else:
                data_m = LoadNexusMonitors(filename)
                Ei,T0=GetEiT0atSNS(data_m)

        Emin = E_min_supplied if E_min_supplied else -0.95*Ei
        Emax = E_max_supplied if E_max_supplied else 0.95*Ei
        Erange='{},{},{}'.format(Emin,(Emax-Emin)*0.2,Emax)

        tib = [None,None]

        #HYSPEC specific
        if inst_name == 'HYSPEC':
            #get tofmin and tofmax, and filter out anything else
            msd = run_obj['msd'].getStatistics().mean
            tel = (39000+msd+4500)*1000/numpy.sqrt(Ei/5.227e-6)
            tofmin = tel-1e6/120-470
            tofmax = tel+1e6/120+470
            data = CropWorkspace(InputWorkspace = data, XMin = tofmin, XMax = tofmax)    
            try:
                psda = psda_supplied if (psda_supplied is not None) else run_obj['psda'].getStatistics().mean
            except:
                psda = 0
            data=detector_geometry_correction(data,psda=psda)
            
            if perform_tib is None:
                perform_tib=True
            #TIB limits
            if Ei==15:
                tib=[22000.,23000.]
            else:
                tib = SuggestTibHYSPEC(Ei)
        
        #CNCS specific
        if inst_name == 'CNCS':
            tib = SuggestTibCNCS(Ei)
            if perform_tib is None:
                perform_tib=True
        
        if perform_tib is None:
            perform_tib=False
        tib_min = tib_min_supplied if tib_min_supplied else tib[0]
        tib_max = tib_max_supplied if tib_max_supplied else tib[1]
        
        #convert to energy transfer
        dgs,_=DgsReduction(SampleInputWorkspace=data,
                           SampleInputMonitorWorkspace=data,
                           TimeZeroGuess=T0,
                           IncidentEnergyGuess=Ei,
                           UseIncidentEnergyGuess=True,
                           IncidentBeamNormalisation='None',
                           EnergyTransferRange=Erange,
                           TimeIndepBackgroundSub=perform_tib,
                           TibTofRangeStart=tib_min,
                           TibTofRangeEnd=tib_max,
                           SofPhiEIsDistribution=False)
        dgs=CropWorkspaceForMDNorm(InputWorkspace=dgs, XMin = Emin, XMax = Emax)

        #Ef corrections
        if Ef_correction_function_module!='default_Ef_correction':
            import importlib
            mod = importlib.import_module(Ef_correction_function_module)
            dgs=mod.Ef_correction(dgs,psda=psda,**kwargs)
        else:
            dgs=Ef_correction(dgs,psda=psda,**kwargs)

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
                    PreprocDetectorsWS='-',
                    OutputWorkspace="__{0}_{1}".format(mde_ws_name,num))
        
        
    MergeMD(','.join(["__{}_{}".format(mde_ws_name,num) for num in range(len(filenames))]),
            OutputWorkspace=mde_ws_name)
    DeleteWorkspaces(','.join(["__{}_{}".format(mde_ws_name,num) for num in range(len(filenames))]))        
    DeleteWorkspaces('data,dgs')        



