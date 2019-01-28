import sys
sys.path.append('/opt/mantidnightly/bin/')
from mantid.simpleapi import *
import matplotlib.pyplot as plt
from mantid import plots
from matplotlib.colors import LogNorm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit



#def gaussian(x, mu, sig):
#    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def gaussian(x, mu, sig, amp):
    return 1./sig/np.sqrt(np.pi*2)*amp*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

dd_mode_dict = {1:9, 0:2, 3:4.4}

#preprocessing V file name
processed_vanadium="/SNS/CNCS/IPTS-22728/shared/autoreduce/processed_van_299736_16degree_beam_stop.nxs"
van = Load(processed_vanadium)

#put in the values in units meV 
Ei_3p32_meV = 3.32
Emin_3p32_meV=-0.5
Emax_3p32_meV=0.9
Estep_3p32_meV=0.005 #this is the step of the nxspe file, will rebin later

#time independent background
tibmin_3p32_meV,tibmax_3p32_meV=SuggestTibCNCS(Ei_3p32_meV)

#define the runs and read in the data
data_folder = '/SNS/CNCS/IPTS-22728/nexus/'
runs_3p32_meV = [299738]
file_names_3p32_meV = [data_folder + 'CNCS_{0}.nxs.h5'.format(r) for r in runs_3p32_meV]
data_3p32_meV = Load('+'.join(file_names_3p32_meV))

#load the monitors
monitor_3p32_mev = LoadNexusMonitors(file_names_3p32_meV[0])

#load the instrument geometry
LoadInstrument(data_3p32_meV,FileName='/SNS/CNCS/shared/geometry/CNCS_Definition_2018B2.xml', RewriteSpectraMap=False)

#detector_height = 2.06
detector_height = data_3p32_meV.getInstrument().getDetector(0).shape().getBoundingBox().width()[1]*128.

#Get Ei (initial energy through choppers), T0 (delay time of emission from source), vi (initially velocity from source)
print("Ei = {} meV".format(data_3p32_meV .getRun()['EnergyRequest'].firstValue()))

mode = data_3p32_meV .run()['DoubleDiskMode'].timeAverageValue()
print("double-disc-mode {0}={1} degree opening".format(mode, dd_mode_dict[mode]))

Ei, _FMP, _FMI, T0 = GetEi(data_3p32_meV)
print("T0 tabled = {} microseconds".format(T0))

tzce = 175.539961298
print("T0 from chopper emission {} microseconds".format(tzce))

vi = 437.393295261*np.sqrt(Ei) #energy in units of meV
print("vi = {} m/s".format(vi))


"""
mon_instr = monitor_CNCS_273899_rebin.getInstrument()

for i in range(mon_instr.nelements()): print(i, mon_instr[i].getName())
(0, 'moderator')
(1, 'sample-position')
(2, 'monitors')
(3, 'detectors')

this is giving the indexation of the instrument

and then monitor has 3 elements...

for i in range(mon_instr[2].nelements()): print(i, mon_instr[2][i].getName())
(0, 'monitor1')
(1, 'monitor2')
(2, 'monitor3')
"""

#Get L1 (distance from source to sample), t1 (time from source to sample)
instr = data_3p32_meV.getInstrument()

monitor1_position = instr[2][0].getPos() #now defunct monitor that is directly in front of chopper 1, the fermi chopper, should be ~6.313 m from the source
monitor2_position = instr[2][1].getPos() #monitor that is directly after chopper 2, the first bandwidth chopper, should be ~7.556 m from the source
monitor3_position = instr[2][2].getPos() #monitor that is directly after choppers 4+5, the double disc choppers, should be ~34.836 m from the source
#monitor3 is the one that is most useful in this case

source_position = instr.getSource().getPos()
sample_position = instr.getSample().getPos()
L1 = np.linalg.norm(sample_position-source_position)
source_to_monitor3 = np.linalg.norm(monitor3_position-source_position)
t1 = L1/vi*1e6 #in microseconds, converted from SI of seconds
t_monitor3_without_T0 = source_to_monitor3/vi*1e6 #the time it takes to get to monitor #3, for the given Ei

print("source coordinates",source_position)
print("monitor3 coordinates", monitor3_position)
print("sample coordinates",sample_position)
print("L1 (distance source to sample) = {} meters".format(L1))
print("Lm3 (distance from source to monitor#3)= {} meters".format(source_to_monitor3))
print("t1 (time source to sample) = {} microseconds".format(t1))
print("tm3 (time to get to monitor#3 without T0 delay) = {} microseconds".format( t_monitor3_without_T0))

#
#calculate ROI (region of interest) taking one pixel as the example
L2 = np.linalg.norm(instr.getDetector(40000).getPos())
print("L2 (distance sample to detector) = {} meters".format(L2))

#the purported design L2 is 3.5 m
L2 = 3.5 #m

#the time expected for the elastic line, is the time to travel L1 and L2 with a speed of vi, plus the T0 offset
#T0 here is from the chopper emission (tzce?)
t_detector_expected = (L1+L2)/vi * 1e6 + T0
print("T0 from MANTID = {} microseconds" .format(T0) )
print("t_detector_expected ((L1+L2)/vi + T0)= {} microseconds".format(t_detector_expected))

#find the ROI (region of interest)
tofbin_min = int(t_detector_expected*.95) 
tofbin_max = int(t_detector_expected*1.05) 
print("binning detector elastic line from times of {} to {} in microseconds".format(tofbin_min,tofbin_max))

tofbin_monitor3_min = int(t_monitor3_without_T0*.95) 
tofbin_monitor3_max = int(t_monitor3_without_T0*1.05) 
print("binning peak at monitor3 from times of {} to {} in microseconds".format(tofbin_monitor3_min, tofbin_monitor3_max))

#Time of flight histogram for the detectors
tofbin_size = 1. #EACH BIN IS 1 microsecond by definition, this is important because later on there is an indexation of array that uses this, do not change it without care!!!
data_3p32_meV_near_elastic = Rebin(InputWorkspace=data_3p32_meV, OutputWorkspace='data_3p32_meV_near_elastic', Params="{0},{1},{2}".format(tofbin_min, tofbin_size, tofbin_max))

#time of flight for the monitors
Rebin(InputWorkspace='monitor_3p32_mev', OutputWorkspace='monitor_3p32_mev', Params="{0},{1},{2}".format(tofbin_monitor3_min, tofbin_size, tofbin_monitor3_max))
monitor_3p32_mev = CropWorkspace(monitor_3p32_mev, StartWorkspaceIndex = 1, EndWorkspaceIndex = 1)

#fit a gaussian to the monitor3 peak, to get the timing_offset

#extract the arrays associated with the time-of-flight spectrum for the monitor3
monitor_3p32_mev_tof = monitor_3p32_mev.extractX()[0]
monitor_3p32_mev_tof = monitor_3p32_mev_tof[:-1] + (monitor_3p32_mev_tof[1]-monitor_3p32_mev_tof[0])/2.
monitor_3p32_mev_intensity = monitor_3p32_mev.extractY()[0]

#get an initial guess for the fit by simply taking the maximum value of the peak
monitor3_height_guess = np.max(monitor_3p32_mev_intensity)
print("monitor3_height_guess = {0}".format(monitor3_height_guess) )
monitor3_peakcenter_guess = monitor_3p32_mev_tof[np.argmax(monitor_3p32_mev_intensity)]
print("monitor3_peakcenter_guess = {0}".format(monitor3_peakcenter_guess) )
monitor3_sigma_guess = 10
print("monitor3_sigma_guess = {0}".format(monitor3_sigma_guess) )


initial_guess = [monitor3_peakcenter_guess, monitor3_sigma_guess, monitor3_height_guess]
popt, pcov = curve_fit(gaussian, monitor_3p32_mev_tof, monitor_3p32_mev_intensity, p0=initial_guess)
popt_names = ['mu', 'sig', 'amp']

monitor_3_fit_mu = popt[0]
monitor_3_fit_sig = popt[1]
monitor_3_fit_amp = popt[2]

print("monitor_3_fit_amp = {}".format(monitor_3_fit_amp) )
print("monitor_3_fit_mu = {}".format(monitor_3_fit_mu) )
print("monitor_3_fit_sig = {}".format(monitor_3_fit_sig) )

timing_offset = monitor_3_fit_mu - t_monitor3_without_T0
print("timing_offset found by peak arrival time at monitor3", timing_offset)
print(tzce)

#
#plot the detector time of flight in the region of interest
print('plotting')
detector_spectrum=SumSpectra(InputWorkspace=data_3p32_meV_near_elastic)

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
ax.plot(detector_spectrum)
ax.legend()
#before a ConvertToMD then, perform a DGS reduction
#make an nxspe-type object

tibmin_3p32_meV,tibmax_3p32_meV=SuggestTibCNCS(Ei)

print(tibmin_3p32_meV,tibmax_3p32_meV)

data_3p32_meV_near_elastic_DGS,_ = DgsReduction(
        SampleInputWorkspace = data_3p32_meV,
        SampleInputMonitorWorkspace = data_3p32_meV,
        EnergyTransferRange = [-0.1, 0.001, 0.9],
        SofPhiEIsDistribution = True, #this will keep the output data as a histogram
        TimeIndepBackgroundSub = True,
        TibTofRangeStart = tibmin_3p32_meV,
        TibTofRangeEnd = tibmax_3p32_meV,
        CorrectKiKf = True,
        DetectorVanadiumInputWorkspace = van,
        UseProcessedDetVan = True,
        IncidentBeamNormalisation='ByCurrent',
        )

data_3p32_meV_near_elastic_MD = ConvertToMD(InputWorkspace=data_3p32_meV_near_elastic_DGS,
             QDimensions='|Q|',
             dEAnalysisMode='Direct')

data_3p32_meV_near_elastic_sqw = BinMD(InputWorkspace=data_3p32_meV_near_elastic_MD,
        AlignedDim0='|Q|,0,1.27,100',
        AlignedDim1='DeltaE,-0.1,0.6,300')

fig_sqw, ax_sqw = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax_sqw.pcolormesh(data_3p32_meV_near_elastic_sqw, norm=LogNorm())
cbar=fig_sqw.colorbar(c)
cbar.set_label('Intensity (arb. units)') #add text to colorbar

fig_mon, ax_mon = plt.subplots(subplot_kw={'projection':'mantid'})
ax_mon.plot(monitor_3p32_mev)
ax_mon.legend()

ax_mon.plot(monitor_3p32_mev_tof, gaussian(monitor_3p32_mev_tof, monitor_3_fit_mu, monitor_3_fit_sig, monitor_3_fit_amp) )
ax_mon.set_xlim([monitor_3_fit_mu-5*monitor_3_fit_sig, monitor_3_fit_mu+5*monitor_3_fit_sig])

plt.show()



#number of histograms
N = data_3p32_meV_near_elastic.getNumberHistograms()
print("number of histograms", N)

def iterL2(pixel_start=0, pixel_end=N, min_counts=20, w = data_3p32_meV_near_elastic):
    for i in range(pixel_start, pixel_end):
        if i%10000==0: print i
        sp = w.getSpectrum(i)
        pixelID = sp.getDetectorIDs()[0]
        spectrum = w.readY(i)
        nominal_L2 = np.linalg.norm(instr.getDetector(pixelID).getPos()) #this is from the geometry file that tells what is the position of the pixel
        tot_counts = np.sum(spectrum)
        if tot_counts == 0:
            yield i, pixelID, nominal_L2, -1, tot_counts # dets not installed
            continue
        nominal_TOF = (L1+nominal_L2)/vi * 1e6 + timing_offset#+ T0
        #
        #
        center_bin = int(nominal_TOF) - tofbin_min #define the center_bin with respect to the tofbin_min, get the estimated time from tofbin_min to expect the peak
        #remember, now indexations and timing is mapped as the binning is 1 microsecond
        bins_to_use_on_each_side = 100
        subset = spectrum[center_bin-bins_to_use_on_each_side: center_bin+bins_to_use_on_each_side]
        center = np.dot(subset, np.arange(center_bin-bins_to_use_on_each_side+.5, center_bin+bins_to_use_on_each_side+.5))/np.sum(subset) #get the center of mass of the elastic line
        t = center + tofbin_min
        L2 = (t - t1 - timing_offset)*vi/1e6
        # assert abs(nominal_L2-L2)/nominal_L2<0.1
        yield i, pixelID, nominal_L2, L2, tot_counts
        continue
        
#calculate the different L2 values of the different detectors
L2s = list(iterL2(min_counts=10, pixel_start=40000, pixel_end=40010, w = data_3p32_meV_near_elastic))

print("for a few different detectors, the L2 values are")
for i in L2s: print(i)

L2s = list(iterL2(min_counts=50))

L2_arr = np.array(L2s)

#plot the old and new L2's
#plt.plot(L2_arr[:, 2], label = 'old values')
#plt.plot(L2_arr[:, 3], label = 'new values')
#plt.plot(L2_arr[:, 2]/L2_arr[:, 3], label = 'difference')
plt.plot(L2_arr[:, 4], label = 'counts')
plt.legend()
plt.show()

print(L2_arr)
print(np.shape(L2_arr))

#
#inspect a detector pack
#pack is a synonym for bank
#pack = 10
pack = 3

plt.figure()
sl = slice(pack*1024, (pack+1)*1024)
view = L2_arr[:, 2][sl].view()
view.shape = 8, 128
plt.subplot(1,3,1)
plt.title('original')
plt.imshow(view.T)
plt.clim(3.35, 3.65)
plt.colorbar()

view = L2_arr[:, 3][sl].view()
view.shape = 8, 128
plt.subplot(1,3,2)
plt.title('new')
plt.imshow(view.T)
plt.clim(3.35, 3.65)
plt.colorbar()


view = L2_arr[:, 3][sl]-L2_arr[:, 2][sl]
view.shape = 8, 128
plt.subplot(1,3,3)
plt.title('diff')
plt.imshow(view.T)
plt.clim(-.015, .015)
plt.colorbar()

plt.show()

#plot the difference between nominal and observed distances for all of the banks
fig_bank_images = plt.figure(figsize=(20,7))
ax_bank_images = plt.gca()
for i in range(0,50):
    print(i)
    pack = i

    sl = slice(pack*1024, (pack+1)*1024)

    view = L2_arr[:, 3][sl]-L2_arr[:, 2][sl]
    view.shape = 8, 128
    plt.subplot(1,51,i+1)
    #plt.title('diff')
    plt.imshow(view.T)
    plt.clim(-.015, .015)
    #plt.xlabel('1')
    #ax_bank_images.set_xticklabels(['']*len([item.get_text() for item in ax_bank_images.get_xticklabels()]))
    #ax_bank_images.set_yticks([])
    plt.axis('off')
    plt.text(0, -10, str(i+1), fontsize=12, rotation = 90)
    if i == 1: plt.text(0, -30, "difference between L2-nominal and L2-calculated for all banks")

#plt.subplot(1,51,51)
#plt.clim(-.015, .015)
#plt.colorbar()

plt.show()

#
#integrate over the x-direction of banks to get lines and plot those for fitting of the y-offset, r-offset, and H-scaling

def my_detector_diff(pixel_index, r0_offset, H_scaled, y_offset):
    H_defined = detector_height #meters
    #pixel_index = np.arange(0,128,1)[10:-10]
    
    nominal_L2_of_pixel = np.sqrt(L2**2 + (H_defined/127.*pixel_index - H_defined/2.)**2)
    
    adjusted_L2_of_pixel = np.sqrt(L2**2 + (H_scaled/127.*pixel_index - H_scaled/2. + y_offset)**2) + r0_offset
    
    L2_diff =  adjusted_L2_of_pixel - nominal_L2_of_pixel 
    
    return L2_diff
    



#plot and fit the differences
print("bank", "r0_offset", "H_scaled", "y_offset")
r0_offset_list = []
H_scaled_list = []
y_offset_list = []
plt.figure(figsize=(7,15))
for j in range(0,50,10):
    plt.subplot(5,1,int(j/10+1))
    for i in range(j,j+10,1):
        #print(i)
        pack = i

        sl = slice(pack*1024, (pack+1)*1024)

        view = L2_arr[:, 3][sl]-L2_arr[:, 2][sl] #the calculated_L2 minus the nominal_L2 (nominal uses the previous instrument geometry file)
        view.shape = 8, 128
        view = view[:,10:-10]
        #print(np.shape(view))
        view = np.sum(view, axis = 0)/8.0
        pixel_indices = np.arange(0,128,1)
        pixel_indices_sliced = pixel_indices[10:-10]
        plt.plot(pixel_indices_sliced, view, '-', label = 'bank'+str(i+1))
        popt, pcov = curve_fit(my_detector_diff, pixel_indices_sliced, view, p0 = (-0.06,  2.25, -0.07))
        r0_offset_list.append(popt[0])
        H_scaled_list.append(popt[1])
        y_offset_list.append(popt[2])
        print(i,popt)


        r0_offset, H_scaled, y_offset = popt
        array_of_128_pixels = np.arange(0,128,1)
        L2_diff = my_detector_diff(array_of_128_pixels, r0_offset, H_scaled, y_offset)

        plt.plot(array_of_128_pixels, L2_diff, 'x')

    plt.legend(fontsize = 'xx-small')
    if j == 20:plt.xlabel('vertical pixel index, summed over tubes')
    plt.ylabel('nominal minus calculated L2 (m)')
    plt.xlabel('pixel index')


plt.figure(figsize=(7,10))
plt.subplot(3,1,1)
plt.title("result of 3 parameter fit of difference data")
plt.plot(np.multiply(r0_offset_list, 100))
plt.ylabel("r0 offset (cm)")
plt.subplot(3,1,2)
plt.plot(H_scaled_list)
plt.ylabel("effective detector height (m)")
print(np.mean(H_scaled_list))
print(np.mean(y_offset_list))
plt.subplot(3,1,3)
plt.plot(np.multiply(y_offset_list,100))
plt.ylabel("vertical offset (cm)")
plt.xlabel("bank")
plt.show()



def my_detector_positions(pixel_index, r0_offset, H_scaled, y_offset):
    L2_of_pixel = np.sqrt(L2**2 + (H_scaled/127.*pixel_index - H_scaled/2. + y_offset)**2) + r0_offset
    return L2_of_pixel

#plot and fit the observation of L2
print("bank", "r0_offset", "H_scaled", "y_offset")
r0_offset_list = []
H_scaled_list = []
y_offset_list = []
plt.figure(figsize=(7,15))
for j in range(0,50,10):
    plt.subplot(5,1,int(j/10+1))
    for i in range(j,j+10,1):
        #print(i)
        pack = i

        sl = slice(pack*1024, (pack+1)*1024)

        view = L2_arr[:, 3][sl] #the calculated_L2
        view.shape = 8, 128
        view = view[:,10:-10]
        #print(np.shape(view))
        view = np.sum(view, axis = 0)/8.0
        pixel_indices = np.arange(0,128,1)
        pixel_indices_sliced = pixel_indices[10:-10]
        plt.plot(pixel_indices_sliced, view, '-', label = 'bank'+str(i+1))
        popt, pcov = curve_fit(my_detector_positions, pixel_indices_sliced, view, p0 = (-6e-3,  2.06, -1e-2))
        r0_offset_list.append(popt[0])
        H_scaled_list.append(popt[1])
        y_offset_list.append(popt[2])
        print(i,popt)


        r0_offset, H_scaled, y_offset = popt
        array_of_128_pixels = np.arange(0,128,1)
        L2_calc = my_detector_positions(array_of_128_pixels, r0_offset, H_scaled, y_offset)

        plt.plot(array_of_128_pixels, L2_calc, 'x')

    plt.legend(fontsize = 'xx-small')
    if j == 20:plt.xlabel('vertical pixel index, summed over tubes')
    plt.ylabel('calculated L2 (m)')
    plt.xlabel('pixel index')


plt.figure(figsize=(7,10))
plt.subplot(3,1,1)
plt.title("result of 3 parameter of calculated data")
plt.plot(np.multiply(r0_offset_list, 100))
plt.ylabel("r0 offset (cm)")
plt.subplot(3,1,2)
plt.plot(H_scaled_list)
plt.ylabel("effective detector height (m)")
print(np.mean(H_scaled_list))
print(np.mean(y_offset_list))
plt.subplot(3,1,3)
plt.plot(np.multiply(y_offset_list,100))
plt.ylabel("vertical offset (cm)")
plt.xlabel("bank")
plt.show()



#now look at summations across the x-direction, to see if there is any rotation about the vertical axis happening
def my_line(x, slope,offset):
    return x*slope+offset

rotation_angle_list = []
plt.figure(figsize=(7,15))
for j in range(0,50,10):
    plt.subplot(5,1,int(j/10+1))
    for i in range(j,j+10,1):
        #print(i)
        pack = i

        sl = slice(pack*1024, (pack+1)*1024)

        view = L2_arr[:, 3][sl] #the calculated_L2
        view.shape = 8, 128
        view = view[:,10:-10]
        #print(np.shape(view))
        view = np.sum(view, axis = 1)/108.
        tube_indices = np.arange(0,8,1)
        tube_distances = np.multiply(0.0254+0.002032, tube_indices)
        tube_distances = tube_distances-np.mean(tube_distances)
        plt.plot(tube_distances, view, 'o-', label = 'bank'+str(i+1))
        plt.legend(fontsize = 'xx-small')
        popt, pcov = curve_fit(my_line, tube_distances, view, p0 = (0,3.5))
        
        print(i,popt, 180./np.pi*np.arctan(popt[0]))
        
        angle_calc = my_line(tube_distances, popt[0], popt[1])
        plt.plot(tube_distances, angle_calc, '--')
        rotation_angle_list.append(180./np.pi*np.arctan(popt[0]))
        plt.xlabel("x distance (m)")
        plt.ylabel("calculated L2 (m)")

plt.figure()
plt.plot(rotation_angle_list)
plt.ylabel("rotation angle about vertical (degrees)")
plt.xlabel("bank")
plt.show()

if 0:
    plt.close('all')
"""
can access the detectors of the instrument instance
1, specify the bank of which there are 50 (0,49)
2, specify the tube within the bank, of which there are 8 (0,7)
3, specify the pixel withink the tube, of which there are 128 (0,127)

instr.getComponentByName("bank50")[0][tube_chosen][pixel_chosen].getName())

so, there are 51200 pixels
alternatively, one can index just linearly by the pixel
so for a given bank there are 8 tubes*(128 pixels/tube) = 1024 pixels per bank
sl = slice(chosen_bank*1024, (chosen_bank+1)*1024)

each bank may change radial distance and rotation about it's center

CNCS_geom_2017B['BankAngle'] = the angle of the bank rotated about its mount
CNCS_geom_2017B['BankDistance']
CNCS_geom_2017B['Bank_xpos']
CNCS_geom_2017B['Bank_ypos']
CNCS_geom_2017B['Bank_zpos']

in this fit, I did 4 parameters that are listed in order of bank
r0_offset_list = is just a radial addition to the overall L2 for a given bank
H_scaled_list = is a scaling of the detector height
y_offset_list = is a scaling of the y-axis vertical offset of the detectors
rotation_angle_list = is the offset for rotation about the y-axis
"""

#try to plot the positions of the banks
CNCS_geom_2018B = np.genfromtxt('/SNS/users/vdp/CNCS/geometry/CNCS_geom_Pajerowski_2018B.txt', names = True)
#CNCS_geom_2018B = np.genfromtxt('/SNS/users/vdp/CNCS/geometry/CNCS_geom_2017B.txt', names = True)
fig_banks = plt.figure()
ax_banks = fig_banks.add_subplot(111, projection='3d')
#ax_banks.set_proj_type('ortho')

#f = open('/SNS/users/vdp/CNCS/2018B-2/CNCS_geom_Pajerowski_2018B-2.txt', 'w')
f = open('CNCS_geom_Pajerowski_2018B-2.txt', 'w')
f.write('BankAngle BankDistance Bank_xpos Bank_ypos Bank_zpos\n')

two_theta_list = []
for idx, chosen_bank in enumerate(range(1,51)):
        xs, ys, zs = instr.getComponentByName("bank"+str(chosen_bank))[0].getPos()
        ax_banks.scatter(xs, ys, zs)
        this_two_theta = 180./np.pi * np.arctan2(xs,zs)
        this_two_theta_rad = np.arctan2(xs,zs)
        two_theta_list.append(this_two_theta)
        xgf = CNCS_geom_2018B['Bank_xpos'][idx]
        ygf = CNCS_geom_2018B['Bank_ypos'][idx]
        zgf = CNCS_geom_2018B['Bank_zpos'][idx]
        rgf = np.sqrt(xgf**2 + zgf**2)
        print(chosen_bank, rgf, CNCS_geom_2018B['BankDistance'][idx], zs,rgf*np.cos(this_two_theta_rad),xs,rgf*np.sin(this_two_theta_rad))
        
        print(chosen_bank, xs, ys, zs, xs-xgf, ys-ygf, zs-zgf, )
        my_this_BankAngle = this_two_theta + rotation_angle_list[idx]
        #my_this_BankDistance = CNCS_geom_2018B['BankDistance'][idx]*1e-2 + r0_offset_list[idx]
        my_this_BankDistance = L2 + r0_offset_list[idx]
        my_this_Bank_xpos = my_this_BankDistance*np.sin(this_two_theta_rad)
        my_this_Bank_ypos = y_offset_list[idx]
        my_this_Bank_zpos = my_this_BankDistance*np.cos(this_two_theta_rad)
        print(chosen_bank, my_this_Bank_xpos, my_this_Bank_ypos, my_this_Bank_zpos)
        my_this_BankDistance = np.sqrt(my_this_Bank_xpos**2+my_this_Bank_ypos**2+my_this_Bank_zpos**2)
        ax_banks.scatter(my_this_Bank_xpos, my_this_Bank_ypos, my_this_Bank_zpos, c="r", marker=r'$\clubsuit$')
        f.write("%s %s %s %s %s\n" % (my_this_BankAngle, my_this_BankDistance*100., my_this_Bank_xpos, my_this_Bank_ypos, my_this_Bank_zpos ))
        
        
f.close()

ax_banks.set_xlabel('X')
ax_banks.set_ylabel('Y')
ax_banks.set_zlabel('Z')
plt.show()

print(instr.getComponentByName("bank50")[0][0][127].getName())
print(instr.getComponentByName("bank50")[0][0][127].getPos())






A = 3.5 #m
h = np.arange(0., 1., 0.1)
x = 0
my_error_thing = A*(h+x) / (2*np.sqrt(2)*(A**2+(h+x)**2)**1.5*np.sqrt(1-A/np.sqrt(A**2+(h+x)**2)))
my_error_thing = my_error_thing * np.pi * 4 / 9.044 * 3.e-2
print(my_error_thing)

#plt.close('all')