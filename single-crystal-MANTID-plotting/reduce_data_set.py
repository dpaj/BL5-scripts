from __future__ import (absolute_import, division, print_function)
from generate_mde import *
from mantid.simpleapi import *
import glob

##################################################################################################################
# Reduces raw data from sets of runs specified by list of dictionaries, mde_data_set = define_data_set(**kwargs),
# to corresponding combined mde workspaces, or loads the existing combined mde from a file
# Authors: A. Savici, I. Zaliznyak, March 2019.
##################################################################################################################
def reduce_data_set(mde_data_set, **kwargs):
    convert_to_chi=kwargs.pop('convert_to_chi',False)

    for data_set in mde_data_set:
        name=data_set['MdeName']
        fname=data_set['MdeFileName']
        if convert_to_chi:
            name+='_chi'
            path_parts=os.path.splitext(fname)
            fname=path_parts[0]+'_chi'+path_parts[1]
            
        if not mtd.doesExist(name):
            try:
                print('Try loading MDE from '+fname)
                LoadMD(fname,OutputWorkspace=name, LoadHistory=False)
            except:
                print('Load MDE failed: generating combined MDE '+name)
                mask_ws=None
                if 'MaskingDataFile' in data_set and data_set['MaskingDataFile'] is not None:
                    print('Try loading masking file: {}'.format(data_set['MaskingDataFile']))
                    mask_ws=Load(data_set['MaskingDataFile'])
                    kwargs['MaskWorkspace']='mask_ws'
                patterns=[data_set['RawDataFolder']+'*{}.nxs.h5'.format(r)for r in data_set['Runs']]
                raw_data_filenames=[glob.glob(pattern)[0] for pattern in patterns]
                generate_mde(raw_data_filenames,
                             name,
                             convert_to_chi=convert_to_chi,
                             **kwargs)
                SetUB(Workspace=name, **data_set['UBSetup'])
                SaveMD(InputWorkspace=name,Filename=fname)
            SetUB(Workspace=name, **data_set['UBSetup'])

def test():
    from define_data_set_sample import define_data_set
    mde_data_set=define_data_set()
    reduce_data_set(mde_data_set)
    
if __name__ == "__main__":
    test()
    
