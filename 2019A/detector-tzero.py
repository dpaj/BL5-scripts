import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
from mantid import plots


#processed vanadium file for solid angle and detector normalization
processed_vanadium="/SNS/CNCS/IPTS-22728/shared/autoreduce/processed_van_299824_8degree_beam_stop.nxs"
van = Load(processed_vanadium)


#plt.close('all')
#define the runs and read in the data
data_folder = '/SNS/CNCS/IPTS-22728/nexus/'
data_taking_mode = 'HR'
run_cycle = '2019A'

if data_taking_mode == 'HF':
    runs_list = range(299739, 299766+1) #HF
elif data_taking_mode == 'AI':
    runs_list = range(299767, 299794+1) #AI
elif data_taking_mode == 'HR':
    runs_list = range(299795, 299823+1) #HR
#runs_list = runs_list[0:2]

#load the Event data and the monitors into memory
if 0:
    for this_run in runs_list:
        print(this_run)
        LoadEventNexus(Filename=data_folder + 'CNCS_{0}.nxs.h5'.format(this_run), OutputWorkspace='CNCS_{0}'.format(this_run), LoadMonitors=True)
        LoadInstrument(mtd['CNCS_{0}'.format(this_run)],FileName='/SNS/CNCS/shared/BL5-scripts/config/CNCS_Definition_2019A.xml', RewriteSpectraMap=False)

instr = mtd['CNCS_{0}'.format(runs_list[0])].getInstrument()
monitor3_position = instr[2][2].getPos() #monitor that is directly after choppers 4+5, the double disc choppers, should be ~34.836 m from the source
source_position = instr.getSource().getPos()
source_to_monitor3 = np.linalg.norm(monitor3_position-source_position)
sample_position = instr.getSample().getPos()
L1 = np.linalg.norm(sample_position-source_position)
sample = instr.getSample()

L2_list = []
bank_indices = range(1,51)
for idx, chosen_bank in enumerate(bank_indices):
    bank=instr.getComponentByName("bank"+str(chosen_bank))[0]
    L2_list.append(bank.getDistance(sample))

L2_ave = np.mean(L2_list)
L1_plus_L2 = L1 + L2_ave
D = L1_plus_L2
print(D)

#get the timing for when the elastic line arrives at bm3
plt.figure()
t_monitor3_measured_list = []
t_monitor3_without_T0_list = []
monitor3_tzero_list = []
energy_list = []
for this_run in runs_list:
    this_monitor = mtd['CNCS_{0}_monitors'.format(this_run)]
    this_energy = mtd['CNCS_{0}_monitors'.format(this_run)].getRun()['Energy'].value[0]
    this_vi = 437.393295261 * np.sqrt(this_energy)  
    t_monitor3_without_T0 = source_to_monitor3/this_vi*1e6 #the time it takes to get to monitor #3, for the given Ei
    tofbin_size = 1.
    tofbin_monitor3_min = int(t_monitor3_without_T0*.95) 
    tofbin_monitor3_max = int(t_monitor3_without_T0*1.05) 
    Rebin(InputWorkspace=mtd['CNCS_{0}_monitors'.format(this_run)], OutputWorkspace=mtd['CNCS_{0}_monitors'.format(this_run)], Params="{0},{1},{2}".format(tofbin_monitor3_min, tofbin_size, tofbin_monitor3_max))
    this_monitor = CropWorkspace(InputWorkspace = mtd['CNCS_{0}_monitors'.format(this_run)], OutputWorkspace = mtd['CNCS_{0}_monitors'.format(this_run)], StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)

    #extract the arrays associated with the time-of-flight spectrum for the monitor3
    monitor3_tof = this_monitor.extractX()[0]
    monitor3_tof = monitor3_tof[:-1] + (monitor3_tof[1]-monitor3_tof[0])/2.
    monitor3_intensity = this_monitor.extractY()[0]
    
    plt.plot(monitor3_tof, monitor3_intensity, label = str(this_energy))
    t_monitor3_measured = np.dot(monitor3_tof , monitor3_intensity) / np.sum(monitor3_intensity)
    print(this_energy, t_monitor3_without_T0, t_monitor3_measured, t_monitor3_measured-t_monitor3_without_T0)
    monitor3_tzero_list.append(t_monitor3_measured-t_monitor3_without_T0)
    plt.vlines(x = t_monitor3_measured, ymin = 0, ymax = np.max(monitor3_intensity))
    energy_list.append(this_energy)
plt.legend()
plt.title(data_taking_mode)
plt.xlabel('time (micro-seconds)')
plt.ylabel('monitor#3 counts')
plt.show()

plt.figure()
for idx, this_run in enumerate(runs_list):
    MaskBTP(Workspace = mtd['CNCS_{0}'.format(this_run)], Instrument = 'CNCS', Pixel = '1-8,120-128')
    this_energy = mtd['CNCS_{0}'.format(this_run)].getRun()['Energy'].value[0]
    this_vi = 437.393295261 * np.sqrt(this_energy)  
    try:# SuggestTibCNCS(this_energy):
        tibmin,tibmax=SuggestTibCNCS(this_energy)
    except:
        tibmin,tibmax=SuggestTibCNCS(49.9)
    dgs,_ = DgsReduction(
            SampleInputWorkspace = mtd['CNCS_{0}'.format(this_run)],
            SampleInputMonitorWorkspace = mtd['CNCS_{0}'.format(this_run)],
            EnergyTransferRange = [-0.2*this_energy, 0.001*this_energy, 0.2*this_energy],
            SofPhiEIsDistribution = True, #this will keep the output data as a histogram
            TimeIndepBackgroundSub = True,
            TibTofRangeStart = tibmin,
            TibTofRangeEnd = tibmax,
            CorrectKiKf = True,
            DetectorVanadiumInputWorkspace = van,
            UseProcessedDetVan = True,
            IncidentBeamNormalisation='ByCurrent',
            IncidentEnergyGuess=this_energy, 
            UseIncidentEnergyGuess='1', 
            TimeZeroGuess = monitor3_tzero_list[idx], #use the timing offset by assuming Ei and position of monitor#3 are as engineered
            )
    md = ConvertToMD(InputWorkspace=dgs, QDimensions='|Q|', OutputWorkspace='md')
    this_qmin = 0
    this_qmax = 4*np.pi*np.sin(130./2.*np.pi/180.) / np.sqrt(81.81/this_energy)
    test = BinMD(InputWorkspace='md', AlignedDim0='|Q|,{0},{1},1'.format(this_qmin, this_qmax), AlignedDim1='DeltaE,{0},{1},50'.format(-0.2*this_energy, 0.2*this_energy), OutputWorkspace='test')
    #plt.figure()
    plt.plot(np.linspace(-0.2*this_energy, 0.2*this_energy, 50), test.getSignalArray()[0], label = str(this_energy))
    plt.title(data_taking_mode)
    #plt.show()
    
    Edet_measured = np.dot(np.linspace(-0.2*this_energy, 0.2*this_energy, 50), test.getSignalArray()[0])/np.sum(test.getSignalArray()[0])
    print(this_energy, Edet_measured, Edet_measured/this_energy*100.)
plt.legend()
plt.xlim([-2,2])
plt.xlabel('dE (meV)')
plt.ylabel('detector counts')
plt.show()

np.save('/SNS/CNCS/shared/BL5-scripts/{0}-m3-tzero-{1}.npy'.format(data_taking_mode ,run_cycle),monitor3_tzero_list) #HF
np.save('/SNS/CNCS/shared/BL5-scripts/{0}-ei-tzero-{1}.npy'.format(data_taking_mode ,run_cycle),energy_list) #HF

if 0:
    #get the timing for when the elastic line arrives at the detectors
    det_tzero_list = []
    for idx, this_run in enumerate(runs_list):
        mtd['CNCS_{0}'.format(this_run)]
        this_energy = mtd['CNCS_{0}'.format(this_run)].getRun()['Energy'].value[0]
        this_vi = 437.393295261 * np.sqrt(this_energy)  
        try:# SuggestTibCNCS(this_energy):
            tibmin,tibmax=SuggestTibCNCS(this_energy)
        except:
            tibmin,tibmax=SuggestTibCNCS(49.9)
        #convert the units from time to energy
        MaskBTP(Workspace = mtd['CNCS_{0}'.format(this_run)], Instrument = 'CNCS', Pixel = '1-63,65-128')
        t_elastic_no_offset = D/this_vi*1e6
        det_TOF=Rebin(InputWorkspace=mtd['CNCS_{0}'.format(this_run)],Params='10')
        det_s=SumSpectra(InputWorkspace=det_TOF)
        
        TOF = det_s.readX(0)
        TOF = (TOF[:-1] + TOF[1:])*0.5
        I = det_s.readY(0)
        
        det_t_measured = np.dot(TOF , I)/np.sum(I)
        
        print(this_energy, t_elastic_no_offset, det_t_measured, t_elastic_no_offset-det_t_measured)
        det_tzero_list.append(t_elastic_no_offset-det_t_measured)


    for idx, val in enumerate(energy_list):
        print('{0}, m3 = {1}, det = {2}'.format(val, monitor3_tzero_list[idx], det_tzero_list[idx]))
        

    plt.figure()
    plt.plot(energy_list, monitor3_tzero_list,'.-', label = 'tzero from m3')
    plt.plot(energy_list, det_tzero_list,'.-', label = 'tzero from det')
    plt.legend()
    plt.xlabel('ei (meV)')
    plt.ylabel('t0 (micro-seconds)')
    plt.show()

    print(monitor3_tzero_list)
    print(det_tzero_list)


"""
#get the timing for when the elastic line arrives at the detectors
for idx, this_run in enumerate(runs_list):
    mtd['CNCS_{0}'.format(this_run)]
    this_energy = mtd['CNCS_{0}'.format(this_run)].getRun()['Energy'].value[0]
    this_vi = 437.393295261 * np.sqrt(this_energy)  
    try:# SuggestTibCNCS(this_energy):
        tibmin,tibmax=SuggestTibCNCS(this_energy)
    except:
        tibmin,tibmax=SuggestTibCNCS(49.9)
    #convert the units from time to energy
    dgs,_ = DgsReduction(
            SampleInputWorkspace = mtd['CNCS_{0}'.format(this_run)],
            SampleInputMonitorWorkspace = mtd['CNCS_{0}'.format(this_run)],
            EnergyTransferRange = [-0.2*this_energy, 0.001*this_energy, 0.2*this_energy],
            SofPhiEIsDistribution = True, #this will keep the output data as a histogram
            TimeIndepBackgroundSub = True,
            TibTofRangeStart = tibmin,
            TibTofRangeEnd = tibmax,
            CorrectKiKf = True,
            DetectorVanadiumInputWorkspace = van,
            UseProcessedDetVan = True,
            IncidentBeamNormalisation='ByCurrent',
            IncidentEnergyGuess=this_energy, 
            UseIncidentEnergyGuess='1', 
            TimeZeroGuess = monitor3_tzero_list[idx], #use the timing offset by assuming Ei and position of monitor#3 are as engineered
            )
    md = ConvertToMD(InputWorkspace=dgs, QDimensions='|Q|', OutputWorkspace='md')
    this_qmin = 0
    this_qmax = 4*np.pi*np.sin(130./2.*np.pi/180.) / np.sqrt(81.81/this_energy)
    test = BinMD(InputWorkspace='md', AlignedDim0='|Q|,{0},{1},1'.format(this_qmin, this_qmax), AlignedDim1='DeltaE,{0},{1},50'.format(-0.2*this_energy, 0.2*this_energy), OutputWorkspace='test')
    plt.figure()
    plt.plot(np.linspace(-0.2*this_energy, 0.2*this_energy, 50), test.getSignalArray()[0])
    plt.title(this_energy)
    plt.show()
    
    Edet_measured = np.dot(np.linspace(-0.2*this_energy, 0.2*this_energy, 50), test.getSignalArray()[0])/np.sum(test.getSignalArray()[0])
    print(this_energy, Edet_measured, Edet_measured/this_energy*100.)
    L2_list = []
    bank_indices = range(1,51)
    for idx, chosen_bank in enumerate(bank_indices):
        bank=instr.getComponentByName("bank"+str(chosen_bank))[0]
        L2_list.append(bank.getDistance(sample))

    L2_ave = np.mean(L2_list)
    L1_plus_L2 = L1 + L2_ave
    D = L1_plus_L2
    t_elastic_no_offset = D/this_vi*1e6

"""
