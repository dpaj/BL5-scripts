import numpy as np
import matplotlib.pyplot as plt


E = 12.00 #meV
timing_offset = 10


v = 437.393295261 * np.sqrt(E)

Ddet = 39.76621861 #meters
Ddet = 3.5 #meters

print(v)

time_from_v = np.divide(Ddet, v)*1e6 + timing_offset
print(time_from_v)

v_from_time = np.divide(Ddet , (time_from_v*1e-6))

e_from_v = v_from_time**2 / (437.393295261)**2

print('at {} meV, for a {} micro-second timing offset, there is a {} meV (dE/E={}%) shift in energy of the elastic line'.format(E, timing_offset,e_from_v-E, (e_from_v-E)/E*100))