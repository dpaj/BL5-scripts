import numpy as np
import matplotlib.pyplot as plt


def avg_pen_calc(att, L):
    return (att * np.exp(L/att) - L - att ) / (np.exp(L/att) - 1) 

def energy_calc(wavelength):
    return 81.81 / wavelength**2

def wavelength_calc(energy):
    return np.sqrt(81.81 / energy)

def att_calc(wavelength):
    # att is in mm, wavelength is in Angs
    return 20.921/ wavelength

wavelength = np.linspace(1,10,101)
energy = energy_calc(wavelength)
att = 20.921 / wavelength 
L = 25.5 #tube depth in mm

avg_pen = avg_pen_calc(att, L)

plt.figure()
plt.plot(energy, avg_pen)
plt.xlabel('E (meV)')
plt.ylabel('average penetration (mm)')
plt.text(1.00, avg_pen_calc(20.921 /wavelength_calc(1.0), L), '{0:.3f}'.format(avg_pen_calc(20.921 /wavelength_calc(1.0), L)))
plt.text(3.32, avg_pen_calc(20.921 /wavelength_calc(3.32), L), '{0:.3f}'.format(avg_pen_calc(20.921 /wavelength_calc(3.32), L)))
plt.text(12.0, avg_pen_calc(20.921 /wavelength_calc(12.0), L), '{0:.3f}'.format(avg_pen_calc(20.921 /wavelength_calc(12.0), L)))
plt.text(30.0, avg_pen_calc(20.921 /wavelength_calc(30.0), L), '{0:.3f}'.format(avg_pen_calc(20.921 /wavelength_calc(30.0), L)))
plt.text(80.0, avg_pen_calc(20.921 /wavelength_calc(80.0), L), '{0:.3f}'.format(avg_pen_calc(20.921 /wavelength_calc(80.0), L)))
plt.plot([1.00, 3.32, 12.0, 30.0, 80.0], avg_pen_calc(20.921 /wavelength_calc(np.array([1.00, 3.32, 12.0, 30.0, 80.0])), L), 'o')
plt.title('callouts at 1.00, 3.32, 12.0, 30.0, 80.0 meV')
plt.show()
