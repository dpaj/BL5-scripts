import matplotlib.pyplot as plt
import numpy as np
import os


def my_tzero_func(e, e0, e1, e2, e3):
	return e0 - e1*np.log(e) - e2*np.log(e)*np.log(e) - e3*np.log(e)*np.log(e)*np.log(e)

#file_to_write = "paj-emissiontable-2018B.sh"
file_to_write = "/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/paj-emissiontable-2019A.sh"
num_points = int(200)
min_energy = 0.3 #meV
max_energy = 150.0 #meV

#2018 HF parameters = 131.54757872,   53.76763428,  -13.86307494,    2.6780689 
#2019A HF parameters = 222.92561565   62.36876256  -19.26586222    4.01443773
tzerofit_params = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/HF_tzerofit_params.npy')
print(tzerofit_params)

e_list = np.logspace(np.log(min_energy), np.log(max_energy), num_points, base=np.exp(1))
t_zero_list = my_tzero_func(e_list,  tzerofit_params[0], tzerofit_params[1], tzerofit_params[2], tzerofit_params[3] )

e_string = "".join(format(x, "12.5f") for x in e_list)
t_zero_string = "".join(format(x, "12.5f") for x in t_zero_list)


f= open(file_to_write,"w+")

for chopper_index in range(0+1,5+1):
	f.write("caput -a BL5:Chop:Skf"+str(chopper_index)+":EmissionTableT "+str(num_points)+" "+t_zero_string+"\n" )
	f.write("caput -a BL5:Chop:Skf"+str(chopper_index)+":EmissionTableE "+str(num_points)+" "+e_string+"\n" )
	f.write("caput BL5:Chop:Skf"+str(chopper_index)+":EmissionTableSize "+str(num_points)+"\n" )
f.close()

os.chmod(file_to_write,755)

plt.figure()
plt.plot(e_list, t_zero_list, 'x')
plt.show()
