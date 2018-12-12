"""
view the vanadium file
"""

import numpy as np
from mantid.simpleapi import *

#the raw vanadium file was at
#/SNS/CNCS/IPTS-20360/nexus/CNCS_273992.nxs.h5

# Load the vanadium file
vanARCS=LoadNexus(Filename='/SNS/ARCS/shared/autoreduce/vanadium_files/van108467_v3.nxs')

#mask out undesired regions of the detector array
#MaskBTP(Workspace = 'vanARCS', Instrument = 'CNCS', Bank = '35-39')
#MaskBTP(Workspace = 'vanARCS', Instrument = 'CNCS', Pixel = '121-128')
#MaskBTP(Workspace = 'vanARCS', Instrument = 'CNCS', Pixel = '1-8')

#LoadInstrument(Workspace=vanARCS,RewriteSpectraMap=False,Filename='/SNS/CNCS/IPTS-20846/shared/CNCS_Definition_Pajerowski.xml')

# Get a handle for the view
instrument_view = getInstrumentView('vanARCS')

# Set the color map range. If a value beyond that contained in the data is given, the limit will change to the min/max data value.
instrument_view.setColorMapMinValue(0.0)
instrument_view.setColorMapMaxValue(1.5)
# Set whether to use a linear or logarithmic scale.
instrument_view.setScaleType(Layer.Linear)
#instrument_view.setScaleType(Layer.Log10)

# Choose how to view the instrument. Options are: Full3D, Cylindrical_X, Cylindrical_Y, Cylindrical_Z, Spherical_X, Spherical_Y, Spherical_Z (Note: This is not case sensitive)
instrument_view.setViewType('Cylindrical_Y')

# Raise the window
instrument_view.show()

#some instructions for the user
print("instructions:")
print("go the the 'Pick' tab")
print("mouse over the regions of the plot to decide what to mask")
