instr = van.getInstrument()
sample = instr.getSample()
samplepos = sample.getPos()
beampos = samplepos - source.getPos()
source = instr.getSource()
beampos = samplepos - source.getPos()
#two-theta in degrees of the detector|| times two for positive and negative two-theta|| times circumference of mask || divided by 360 degrees
#detector 36000=281*128+128./2. is in the lowest positive angle side position
#detector 36800=287*128+128./2. is where some direct beam related scattering is seen in a vanadium file (CNCS_273992.nxs.h5)
print('this is a pixel where direct beam is affecting, displayed in embedded picture', 275*128+128/2)
print('observed direct beam', van.getDetector(275*128+128/2).getTwoTheta(samplepos, beampos)*180./3.14159 * 2 * 2 * 3.14159 * 50 / 360., 'mm beamstop')
print('lowest angle detector', van.getDetector(287*128+128/2).getTwoTheta(samplepos, beampos)*180./3.14159 * 2 * 2 * 3.14159 * 50 / 360., 'mm beamstop')
