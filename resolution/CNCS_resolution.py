from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

f_ch41 = 300#180, 240, or 300
f_ch1 = 60

ei = 3.32 #meV
numpoints = 100 #number of points for energy array
numpoints2T = 100 #number of points for angle array
emax = 0.9*ei #maximum energy considered
emin = -2.0*ei #minimum energy considered

qmin=0
qmax=0.05

emev = ei
wl=np.sqrt(81.81/emev)

sample_diameter=6.0
sample_height=40.0

#open_ch41=4
#open_ch42=4

open_ch41=9
open_ch42=9

ki = 2.0*np.pi*np.sqrt(ei)/9.044888 #initial wave-vector
de = (emax-emin)/(numpoints-1.0) #energy spacing
d2T = 135.0/(numpoints2T-1.0)*np.pi/180.0 #two theta spacing

x = np.zeros(numpoints) #energy transfer axis
y = np.zeros(numpoints) #energy resolution axis
dQ = np.zeros((numpoints, numpoints2T)) # Q resolution
y2T = np.zeros(numpoints2T) # 2Theta axis

vi = np.sqrt(ei/5.227)*1000.0 # initial velocity
vi2 = np.power(vi,2)
vi3 = np.power(vi,3)

L1 = 28.23 #distance from FC (Fermi Chopper) to DDC (Double-disc chopper)
L2 = 1.5 #distance from DDC to sample
L3 = 3.5 #distance from sample to detector

#L1+L2+L2 = 33.23 meters

dfi = 135.0/360.0*np.pi/180.0 #135 is the angles covered by detectors, 360 is the number of detectors
mn_over_h = 1.6749e-27/1.05457e-34/1.0e10# neutron mass[kg]/Planck constat [J s] * meter to angstrom conversion
omega = (f_ch41+f_ch41)*2.0*np.pi

#dtm is the time channel width used for the data
#dtc is the uncertainty in time of transmission through the chopper
#dtp is the source pulse width
#dL2 is the uncertainty in the incident path length
#dL3 combines the detector thickness and the uncertainty of scattered path length in the sample

#reproduce case structure for dtm2 and dtc2
#this might be better as a dict
if f_ch1 == 300:
    if f_ch41 == 300:
        if open_ch41 == 9:
            dtm2=2.69e-9
            dtc2=1.820e-9
        elif open_ch41 == 4:
            dtm2=2.69e-9
            dtc2=0.570e-9
        elif open_ch41 == 2:
            dtm2=2.69e-9
            dtc2=0.044e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 240:
        if open_ch41 == 9:
            dtm2=2.69e-9
            dtc2=1.820e-9
        elif open_ch41 == 4:
            dtm2=2.69e-9
            dtc2=0.570e-9
        elif open_ch41 == 2:
            dtm2=2.69e-9
            dtc2=0.044e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 180:
        if open_ch41 == 9:
            dtm2=2.69e-9
            dtc2=1.820e-9
        elif open_ch41 == 4:
            dtm2=2.69e-9
            dtc2=0.570e-9
        elif open_ch41 == 2:
            dtm2=2.69e-9
            dtc2=0.044e-9
        else:
            print("bad open_ch41 value")
            exit()
elif f_ch1 == 240:
    if f_ch41 == 300:
        if open_ch41 == 9:
            dtm2=2.69e-9
            dtc2=1.820e-9
        elif open_ch41 == 4:
            dtm2=2.69e-9
            dtc2=0.570e-9
        elif open_ch41 == 2:
            dtm2=2.69e-9
            dtc2=0.044e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 240:
        if open_ch41 == 9:
            dtm2=2.69e-9
            dtc2=1.820e-9
        elif open_ch41 == 4:
            dtm2=2.69e-9
            dtc2=0.570e-9
        elif open_ch41 == 2:
            dtm2=2.69e-9
            dtc2=0.044e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 180:
        if open_ch41 == 9:
            dtm2=2.69e-9
            dtc2=1.820e-9
        elif open_ch41 == 4:
            dtm2=2.69e-9
            dtc2=0.570e-9
        elif open_ch41 == 2:
            dtm2=2.69e-9
            dtc2=0.044e-9
        else:
            print("bad open_ch41 value")
            exit()
elif f_ch1 == 180:
    if f_ch41 == 300:
        if open_ch41 == 9:
            dtm2=7.607e-9
            dtc2=2.360e-9
        elif open_ch41 == 4:
            dtm2=7.607e-9
            dtc2=0.741e-9
        elif open_ch41 == 2:
            dtm2=7.607e-9
            dtc2=0.097e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 240:
        if open_ch41 == 9:
            dtm2=7.607e-9
            dtc2=3.440e-9
        elif open_ch41 == 4:
            dtm2=7.607e-9
            dtc2=1.206e-9
        elif open_ch41 == 2:
            dtm2=7.607e-9
            dtc2=0.157e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 180:
        if open_ch41 == 9:
            dtm2=7.607e-9
            dtc2=5.954e-9
        elif open_ch41 == 4:
            dtm2=7.607e-9
            dtc2=2.089e-9
        elif open_ch41 == 2:
            dtm2=7.607e-9
            dtc2=0.231e-9
        else:
            print("bad open_ch41 value")
            exit()
elif f_ch1 == 120:
    if f_ch41 == 300:
        if open_ch41 == 9:
            dtm2=10.130e-9
            dtc2=2.360e-9
        elif open_ch41 == 4:
            dtm2=10.130e-9
            dtc2=0.741e-9
        elif open_ch41 == 2:
            dtm2=10.130e-9
            dtc2=0.097e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 240:
        if open_ch41 == 9:
            dtm2=10.130e-9
            dtc2=3.440e-9
        elif open_ch41 == 4:
            dtm2=10.130e-9
            dtc2=1.206e-9
        elif open_ch41 == 2:
            dtm2=10.130e-9
            dtc2=0.157e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 180:
        if open_ch41 == 9:
            dtm2=10.130e-9
            dtc2=5.954e-9
        elif open_ch41 == 4:
            dtm2=10.130e-9
            dtc2=2.089e-9
        elif open_ch41 == 2:
            dtm2=10.130e-9
            dtc2=0.231e-9
        else:
            print("bad open_ch41 value")
            exit()
elif f_ch1 == 60:
    if f_ch41 == 300:
        if open_ch41 == 9:
            dtm2=12.830e-9
            dtc2=2.360e-9
        elif open_ch41 == 4:
            dtm2=12.830e-9
            dtc2=0.741e-9
        elif open_ch41 == 2:
            dtm2=12.830e-9
            dtc2=0.097e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 240:
        if open_ch41 == 9:
            dtm2=12.830e-9
            dtc2=3.440e-9
        elif open_ch41 == 4:
            dtm2=12.830e-9
            dtc2=1.206e-9
        elif open_ch41 == 2:
            dtm2=12.830e-9
            dtc2=0.157e-9
        else:
            print("bad open_ch41 value")
            exit()
    elif f_ch41 == 180:
        if open_ch41 == 9:
            dtm2=12.830e-9
            dtc2=5.954e-9
        elif open_ch41 == 4:
            dtm2=12.830e-9
            dtc2=2.089e-9
        elif open_ch41 == 2:
            dtm2=12.830e-9
            dtc2=0.231e-9
        else:
            print("bad open_ch41 value")
            exit()
else:
    print("bad chopper 1 frequency choice")
    exit()

#energy resolution
for i in range(numpoints):
    ef = (ei-emin)-i*de
    vf = (np.sqrt(ef/5.227)*1000.0) # final velocity
    dtd2 = (0.6*0.001*sample_diameter/vf+0.2*0.001*sample_height/vf)**2
    vf3 = (np.sqrt(ef/5.227)*1000.0)**3 #final velocity^3
    y1 = (vi3/L1  +  L2*vf3/L1/L3)**2*dtm2 #broadening from the time channel width
    y2 = (vi3/L1  +  (L1+L2)*vf3/L1/L3)**2*dtc2 #broadening from the chopper transmission
    y3 = (vf3/L3)**2*dtd2 #broadening from the sample
    y[i] = np.sqrt(y1+y2+y3)*1.6749e-27*6.2415063e21#neutron mass kg, joule-meV relationship
    x[i] = emin+i*de
    print(x[i], y[i])

plt.plot(x,y)
plt.xlabel("Energy transfer (meV)")
plt.ylabel("FWHM (meV)")

#Q-resolution
for i in range(numpoints):
    ef = (ei-emin)-i*de
    kf = 2.0*np.pi*np.sqrt(ef)/9.044888
    vf = (np.sqrt(ef/5.227)*1000.0) #final velocity
    vf2 = (np.sqrt(ef/5.227)*1000.0)**2 #final velocity squared
    dtd2 = (0.6*0.001*sample_diameter/vf+0.2*0.001*sample_height/vf)**2
    for j in range(numpoints2T):
        y2T[j] = 135.0/numpoints2T*j
        tta = 135.0/numpoints2T*j*np.pi/180.0
        QQ = np.sqrt(ki**2 + kf**2 - 2.0*ki*kf*np.cos(tta))
        qx = QQ*np.cos(np.pi/2.0-tta/2.0)
        qy = QQ*np.cos(tta/2.0)
        dqx = mn_over_h*np.sqrt((dtm2/L1**2*(vi2+vf2*L2/L3*np.cos(j*d2T))**2)+dtc2/L1**2*(vi2+vf2*29.73/L3*np.cos(j*d2T))**2 +\
        (vf2/L3*np.cos(j*d2T))**2*dtd2+(vf*np.sin(j*d2T))**2*dfi**2)
        dqy = mn_over_h*np.sqrt((vf2*L2/L1/L3*np.sin(j*d2T))**2*dtm2+(vf2*29.73/L1/L3*np.sin(j*d2T))**2*dtc2/2 +\
        (vf2/L3*np.sin(j*d2T))**2*dtd2+(vf*np.cos(j*d2T))**2*dfi**2+(vi+vf2/L1*29.73/L3*np.sin(j*d2T))**2*dtc2/2)
        dQ[i,j] = 2.0/QQ*np.sqrt(qx**2+dqx**2+qy**2*dqy**2)

plt.figure()
plt.imshow(dQ)
        
plt.show()
