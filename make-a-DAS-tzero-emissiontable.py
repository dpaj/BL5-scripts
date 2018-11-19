import matplotlib.pyplot as plt
import numpy as np


def my_tzero_func(e, e0, e1, e2, e3):
	return e0 - e1*np.log(e) - e2*np.log(e)*np.log(e) - e3*np.log(e)*np.log(e)*np.log(e)

num_points = int(200)
min_energy = 0.3 #meV
max_energy = 150.0 #meV

e_list = np.logspace(np.log(min_energy), np.log(max_energy), num_points, base=np.exp(1))
t_zero_list = my_tzero_func(e_list,  131.54757872,   53.76763428,  -13.86307494,    2.6780689 )

e_string = "".join(format(x, "12.5f") for x in e_list)
t_zero_string = "".join(format(x, "12.5f") for x in t_zero_list)


f= open("paj-emissiontable-2018B.sh","w+")

for chopper_index in range(0+1,5+1):
	f.write("caput -a BL5:Chop:Skf"+str(chopper_index)+":EmissionTableT "+str(num_points)+" "+t_zero_string+"\n" )
	f.write("caput -a BL5:Chop:Skf"+str(chopper_index)+":EmissionTableE "+str(num_points)+" "+e_string+"\n" )
	f.write("caput BL5:Chop:Skf"+str(chopper_index)+":EmissionTableSize "+str(num_points)+"\n" )
f.close()

plt.plot(e_list, t_zero_list, 'x')
plt.show()
