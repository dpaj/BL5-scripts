#!/usr/bin/env python
from __future__ import print_function

'''
Adds an attribute: flag_name="run-metadata" 
And its content to every first entry in a hdf file
'''


import sys
from shutil import copyfile

import h5py


def main(filename_input, filename_output, flag_content,
         flag_name="run-metadata"):

    # Copy the file first: This is not working!
    # copyfile(filename_input, filename_output)
    f = h5py.File(filename_output, 'a')
    # If there's multiple entries let's add the flag to all entries
    for entry in f.keys():
       f[entry].attrs[flag_name] = flag_content


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: <input file> <output file> <flag content>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
