import matplotlib.pyplot as plt
import re as re
import numpy as np

"""
-rw-r--r-- 1 snsdata users  22M May  7  2018 van_265987.nxs
-rw-rw-r-- 1 snsdata users  28M May 18  2018 van_273266.nxs
-rw-rw-r-- 1 snsdata users  28M May 30  2018 van_273266_oneside.nxs
-rw-r--r-- 1 snsdata users  33M Jun  1  2018 van_273992.nxs
-rw-rw-r-- 1 snsdata users 121M Jul 23 12:26 van_277537.nxs
-rw-r--r-- 1 snsdata users 121M Aug 31 13:51 van_277537_redo.nxs


"""



this_file = '/SNS/CNCS/IPTS-20360/shared/autoreduce/van_277537.nxs'
this_file = '/SNS/CNCS/IPTS-20360/shared/autoreduce/van_273992.nxs'
this_file = '/SNS/CNCS/IPTS-20360/shared/autoreduce/van_273266.nxs'
#this_file = '/SNS/CNCS/IPTS-20360/shared/autoreduce/van_265987.nxs' #crappy data

van=LoadNexus(Filename=this_file)

i=mtd['van'].getInstrument()
sample = instr.getSample()
samplepos = sample.getPos()
beampos = samplepos - source.getPos()
source = instr.getSource()

pixel_height = float(re.search(r'<ns1:height val="(.*?)"/>', i.getDetector(1000).shape().getShapeXML()).group(1))

pxl_intensity_list = []
for this_detector in range(0,51200):
    pxl_intensity = van.readY(this_detector)[0]
    pxl_intensity_list.append(pxl_intensity)

print('mean pixel intensity=', np.mean(pxl_intensity_list))
print('standard deviation of pixel intensity=', np.std(pxl_intensity_list))

#look at a given tube how does the intensity vary
plt.figure()
for tube_number in range(1,400,50):
    #tube_number = 423
    first_pixel = tube_number * 128
    pixel_height = float(re.search(r'<ns1:height val="(.*?)"/>', i.getDetector(first_pixel).shape().getShapeXML()).group(1))
    this_tube_intensity_list = []
    this_tube_solid_angle_list = []
    for this_detector in range(first_pixel,first_pixel+128):
        pxl_intensity = van.readY(this_detector)[0]
        this_tube_intensity_list.append(pxl_intensity)
        this_tube_solid_angle_list.append(van.getDetector(this_detector).solidAngle(samplepos))
        #this_tube_solid_angle_list.append(van.getDetector(this_detector).solidAngle([0,0,0]))


    plt.plot(pixel_height*np.array(range(len(this_tube_intensity_list))),this_tube_intensity_list, 'o', label = 'tube_number='+str(tube_number))
    #ax1.plot(pixel_height*np.array(range(len(this_tube_intensity_list))),np.divide(this_tube_solid_angle_list, np.max(this_tube_solid_angle_list)), label = 'tube_number='+str(tube_number))
    plt.plot(pixel_height*np.array(range(len(this_tube_intensity_list))),np.divide(this_tube_intensity_list,np.divide(this_tube_solid_angle_list, np.max(this_tube_solid_angle_list))), label = 'tube_number='+str(tube_number))
plt.legend(loc = 'botleft')
plt.ylabel('scaled counts')
plt.xlabel('position (m)')
plt.title(this_file)
plt.show()

#plt.close('all')

print(dir(samplepos))