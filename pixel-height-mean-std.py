import re as re
import numpy as np


van=LoadNexus(Filename='/SNS/CNCS/shared/UsefulMantidScripts_2018/Buckyballs/shared/autoreduce/van_277537.nxs')

i=mtd['van'].getInstrument()
pxl_height_list = []
for this_detector in range(0,51200):
    d=i.getDetector(this_detector)
    s=d.shape()
    pxl_height = float(re.search(r'<ns1:height val="(.*?)"/>', s.getShapeXML()).group(1))
    pxl_height_list.append(pxl_height)

print('mean pixel height=', np.mean(pxl_height_list))
print('standard deviation of pixel height=', np.std(pxl_height_list))

