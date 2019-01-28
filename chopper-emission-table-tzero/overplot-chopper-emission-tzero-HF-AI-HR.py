import numpy as np
import matplotlib.pyplot as plt


HR_ei_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/HR_ei_list.npy')
HR_fitted_tzero_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/HR_fitted_tzero_list.npy')
HR_fitted_tzero_error_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/HR_fitted_tzero_error_list.npy')

AI_ei_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/AI_ei_list.npy')
AI_fitted_tzero_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/AI_fitted_tzero_list.npy')
AI_fitted_tzero_error_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/AI_fitted_tzero_error_list.npy')

HF_ei_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/HF_ei_list.npy')
HF_fitted_tzero_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/HF_fitted_tzero_list.npy')
HF_fitted_tzero_error_list = np.load('/SNS/CNCS/shared/BL5-scripts/chopper-emission-table-tzero/HF_fitted_tzero_error_list.npy')

plt.figure()
plt.errorbar(HR_ei_list, HR_fitted_tzero_list, yerr = HR_fitted_tzero_error_list,  label = "HR 2019A", marker = 's')
plt.errorbar(AI_ei_list, AI_fitted_tzero_list, yerr = AI_fitted_tzero_error_list,  label = "HR 2019A", marker = 's')
plt.errorbar(HF_ei_list, HF_fitted_tzero_list, yerr = HF_fitted_tzero_error_list,  label = "HF 2019A", marker = 's')
plt.legend()
plt.xlim([0,85])
plt.ylim([-90,280])
plt.xlabel('Ei (meV)')
plt.ylabel('chopper emission t-zero (microseconds)')
plt.show()

print(HF_ei_list[2])
print(HF_fitted_tzero_list[2])