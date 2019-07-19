from generate_mde import *
from mantid.simpleapi import *

##################################################################################################################
# Reduces raw data from sets of runs specified by list of dictionaries, mde_data_set = define_data_set(**kwargs),
# to corresponding combined mde workspaces, or loads the existing combined mde from a file
# Authors: A. Savici, I. Zaliznyak, March 2019.
##################################################################################################################
def reduce_data_set(mde_data_set, **kwargs):
    convert_to_chi=kwargs.pop('convert_to_chi',False)
    Emin_apply_DB=kwargs.pop('Emin_apply_DB',0.0)
    averageFR=kwargs.pop('AverageFR',14.0)

    for data_set in mde_data_set:
        extra_args={}
        if convert_to_chi:
            data_set['MdeName']=data_set['MdeName']+'_chi'
            path_parts=os.path.splitext(data_set['MdeFileName'])
            data_set['MdeFileName']=path_parts[0]+'_chi'+path_parts[1]
            extra_args={'Temperature':str(data_set['Temperature']), 'Emin_apply_DB':Emin_apply_DB}
        data_set_names=[data_set['MdeName']]
        data_set_filenames=[data_set['MdeFileName']]
            
        for name,fname in zip(data_set_names,data_set_filenames):    
            if not mtd.doesExist(name):
                try:
                    print 'Try loading MDE from '+fname
                    LoadMD(fname,OutputWorkspace=name, LoadHistory=False)
                except:
                    print 'Load failed: generating combined MDE '+name
                    mask_ws=None
                    if 'MaskingDataFile' in data_set:
                        print 'Try loading masking file: '+('None' if data_set['MaskingDataFile'] is None else data_set['MaskingDataFile'])
                        if data_set['MaskingDataFile']:
                            mask_ws=Load(data_set['MaskingDataFile'])
                    instrument_id = data_set['RawDataFolder'].split('/')[2]
                    raw_data_filenames=[data_set['RawDataFolder']+instrument_id+'_{}.nxs.h5'.format(r)for r in data_set['Runs']]
                    generate_mde(raw_data_filenames,
                                 name, 
                                 T0=data_set['T0'], 
                                 Ei=data_set['Ei'], 
                                 MaskWorkspace=mask_ws, 
                                 psda=data_set['psda'], 
                                 averageFR=averageFR,
                                 FilterBadPulsesThreshold=data_set['BadPulsesThreshold'], 
                                 **extra_args)                     
                    SetUB(Workspace=name, **data_set['UBSetup'])
                    SaveMD(InputWorkspace=name,Filename=fname)
                SetUB(Workspace=name, **data_set['UBSetup'])

def test():
    from define_data_set_sample import define_data_set
    mde_data_set=define_data_set()
    reduce_data_set(mde_data_set)
    
if __name__ == "__main__":
    test()
    
