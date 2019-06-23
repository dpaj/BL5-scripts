empty_with_BM4 = Load(Filename='/SNS/CNCS/IPTS-22728/nexus/CNCS_308318.nxs.h5')

LoadInstrument(empty_with_BM4,FileName='/SNS/CNCS/shared/BL5-scripts/detector-positions/CNCS_Definition-addBM4-pre2019B.xml', RewriteSpectraMap=False)

BM1_pos = empty_with_BM4.getInstrument()[2][0].getPos()
BM2_pos = empty_with_BM4.getInstrument()[2][1].getPos()
BM3_pos = empty_with_BM4.getInstrument()[2][2].getPos()
BM4_pos = empty_with_BM4.getInstrument()[2][3].getPos()

print("BM1 position = {} meters from sample".format(BM1_pos))
print("BM2 position = {} meters from sample".format(BM2_pos))
print("BM3 position = {} meters from sample".format(BM3_pos))
print("BM4 position = {} meters from sample".format(BM4_pos))
