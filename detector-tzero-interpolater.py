import numpy as np
import scipy.interpolate as interp


def tzero_interp(ei = 12, mode = 1):
    """
    ei in meV
    chopper modes: HF = 1, AI = 3, HR = 0
    return a t-zero in microseconds
    """

    run_cycle = '2019A'

    if mode == 1:#HF
        HF_m3_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-m3-tzero-{1}.npy'.format('HF' ,run_cycle))
        HF_ei_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-ei-tzero-{1}.npy'.format('HF',run_cycle))
        HF_interp = interp.interp1d(HF_ei_tzero[::-1], HF_m3_tzero[::-1])
        return HF_interp(ei)
    elif mode == 3:#AI
        AI_m3_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-m3-tzero-{1}.npy'.format('AI' ,run_cycle))
        AI_ei_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-ei-tzero-{1}.npy'.format('AI',run_cycle))
        AI_interp = interp.interp1d(AI_ei_tzero[::-1], AI_m3_tzero[::-1])
        return AI_interp(ei)
    elif mode == 0:#HR
        HR_m3_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-m3-tzero-{1}.npy'.format('HR' ,run_cycle))
        HR_ei_tzero = np.load('/SNS/CNCS/shared/BL5-scripts/{0}-ei-tzero-{1}.npy'.format('HR',run_cycle))
        HR_interp = interp.interp1d(HR_ei_tzero[::-1], HR_m3_tzero[::-1])
        return HR_interp(ei)
    else:#unknown
        return 0
