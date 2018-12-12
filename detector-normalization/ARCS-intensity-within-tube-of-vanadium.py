import matplotlib.pyplot as plt
import re as re
import numpy as np

"""
-rw-r--r--  1 snsdata users          25M May 26  2018 van107028.nxs
-rw-r--r--  1 snsdata users          25M Jun 14 20:30 van108467.nxs
-rw-r--r--  1 snsdata users          25M Jul 24 17:17 van108467_new.nxs
-rw-r--r--  1 snsdata users          25M Aug 27 12:22 van108467_v2.nxs
-rw-r--r--  1 snsdata users          25M Aug 30 09:59 van108467_v3.nxs
-rw-r--r--  1 snsdata users          26M Sep 17 15:51 van108467_v3_mag01.nxs


/SNS/ARCS/shared/autoreduce/vanadium_files/van107028.nxs
('mean pixel intensity=', 0.99999999999999556)
('standard deviation of pixel intensity=', 0.16479766368845672)

/SNS/ARCS/shared/autoreduce/vanadium_files/van108467.nxs
('mean pixel intensity=', 1.0000000000000084)
('standard deviation of pixel intensity=', 0.13414401005037824)

/SNS/ARCS/shared/autoreduce/vanadium_files/van108467_new.nxs
('mean pixel intensity=', 26.625025143174721)
('standard deviation of pixel intensity=', 3.5599968529697739)

/SNS/ARCS/shared/autoreduce/vanadium_files/van108467_v2.nxs
('mean pixel intensity=', 1.0000000000000084)
('standard deviation of pixel intensity=', 0.13414401005037824)

/SNS/ARCS/shared/autoreduce/vanadium_files/van108467_v3.nxs
('mean pixel intensity=', 26.615501762358758)
('standard deviation of pixel intensity=', 3.5790150256938871)

/SNS/ARCS/shared/autoreduce/vanadium_files/van108467_v3_mag01.nxs
('mean pixel intensity=', 0.999999999999996)
('standard deviation of pixel intensity=', 0.13936920071817882)
"""

this_file = '/SNS/ARCS/shared/autoreduce/vanadium_files/van107028.nxs'
vanARCS=LoadNexus(Filename=this_file)

i=mtd['vanARCS'].getInstrument()

pixel_height = float(re.search(r'<ns1:height val="(.*?)"/>', i.getDetector(1000).shape().getShapeXML()).group(1))

pxl_intensity_list = []
#ARCS has 920 tubes, each with 128 pixels
for this_detector in range(0,920*128):
    pxl_intensity = vanARCS.readY(this_detector)[0]
    if pxl_intensity > 0:
        pxl_intensity_list.append(pxl_intensity)

print('mean pixel intensity=', np.mean(pxl_intensity_list))
print('standard deviation of pixel intensity=', np.std(pxl_intensity_list))

#look at a given tube how does the intensity vary
plt.figure()
#for tube_number in [423, 542, 757, 551]:
for tube_number in range(1,920,100):
    #tube_number = 423
    first_pixel = tube_number * 128
    pixel_height = float(re.search(r'<ns1:height val="(.*?)"/>', i.getDetector(first_pixel).shape().getShapeXML()).group(1))
    this_tube_intensity_list = []
    for this_detector in range(first_pixel,first_pixel+128):
        pxl_intensity = vanARCS.readY(this_detector)[0]
        this_tube_intensity_list.append(pxl_intensity)


    plt.plot(pixel_height*np.array(range(len(this_tube_intensity_list))),this_tube_intensity_list, label = 'tube_number='+str(tube_number))
plt.legend(loc = 'botleft')
plt.ylabel('scaled counts')
plt.xlabel('position (m)')
plt.title(this_file)
plt.show()

#look at a given tube how does the intensity vary
plt.figure()
for tube_number in range(1,920,100):
    #tube_number = 423
    first_pixel = tube_number * 128
    pixel_height = float(re.search(r'<ns1:height val="(.*?)"/>', i.getDetector(first_pixel).shape().getShapeXML()).group(1))
    this_tube_intensity_list = []
    this_tube_solid_angle_list = []
    for this_detector in range(first_pixel,first_pixel+128):
        pxl_intensity = vanARCS.readY(this_detector)[0]
        this_tube_intensity_list.append(pxl_intensity)
        this_tube_solid_angle_list.append(vanARCS.getDetector(this_detector).solidAngle(samplepos))
        #this_tube_solid_angle_list.append(van.getDetector(this_detector).solidAngle([0,0,0]))


    #ax1.plot(pixel_height*np.array(range(len(this_tube_intensity_list))),this_tube_intensity_list, label = 'tube_number='+str(tube_number))
    #ax1.plot(pixel_height*np.array(range(len(this_tube_intensity_list))),np.divide(this_tube_solid_angle_list, np.max(this_tube_solid_angle_list)), label = 'tube_number='+str(tube_number))
    plt.plot(pixel_height*np.array(range(len(this_tube_intensity_list))),np.divide(this_tube_intensity_list,np.divide(this_tube_solid_angle_list, np.max(this_tube_solid_angle_list))), label = 'tube_number='+str(tube_number))
plt.legend(loc = 'botleft')
plt.ylabel('scaled counts')
plt.xlabel('position (m)')
plt.title(this_file)
plt.show()