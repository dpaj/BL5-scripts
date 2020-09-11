import numpy as np
import matplotlib.pyplot as plt



CNCS = LoadEmptyInstrument(InstrumentName='CNCS', OutputWorkspace='CNCS')

CNCS_solidangle = SolidAngle(CNCS)

solidangle_list = []
for i in range(3,51200):
    solidangle_list.append(CNCS_solidangle.readY(i)[0])

print('solidangle mean={0}'.format(np.mean(solidangle_list)))
print('solidangle std={0}'.format(np.std(solidangle_list)))
print('std/mean={0}'.format(np.std(solidangle_list)/np.mean(solidangle_list)))

print(np.min(solidangle_list))
print(np.max(solidangle_list))


plt.figure()
plt.plot(solidangle_list)
plt.show()