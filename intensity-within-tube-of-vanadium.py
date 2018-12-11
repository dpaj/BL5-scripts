import matplotlib.pyplot as plt
import re as re
import numpy as np


van=LoadNexus(Filename='/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/van_277537.nxs')

i=mtd['van'].getInstrument()

pixel_height = float(re.search(r'<ns1:height val="(.*?)"/>', i.getDetector(1000).shape().getShapeXML()).group(1))

pxl_intensity_list = []
for this_detector in range(0,51200):
    pxl_intensity = van.readY(this_detector)[0]
    pxl_intensity_list.append(pxl_intensity)

print('mean pixel intensity=', np.mean(pxl_intensity_list))
print('standard deviation of pixel intensity=', np.std(pxl_intensity_list))

#look at a given tube how does the intensity vary
this_tube_intensity_list = []
tube_number = 200
first_pixel = tube_number * 128
for this_detector in range(first_pixel,first_pixel+128):
    pxl_intensity = van.readY(this_detector)[0]
    this_tube_intensity_list.append(pxl_intensity)

plt.figure()
plt.plot(pixel_height*np.array(range(len(this_tube_intensity_list))),this_tube_intensity_list)
plt.show()