#!/usr/bin/python

#
# TOFTOF
# 
# From raw data to SofQw
#
# Open MantidPlot and launch the IPython console
#

##########################################


filename = '/Users/ganeva/Dropbox/mantid/043880_0000_raw.nxs'
eFixed='31.95477' #1.6A

wsName = 'Vana'

# range in TOF
#vanadiumFRangeLower=7000
#vanadiumFRangeUpper=8500

#maskFile = '/opt/Mantid/instrument/masks/IN5_Mask.xml'
transmission  =  0.95  # Sample transmission
rebiningInEnergy = '-2,0.05,2' # from, step, to
rebiningInQ = '0.1,0.5,8' # from, step, to



##########################################
# 1) Load Sample

Load(Filename=filename,OutputWorkspace=wsName)

# Load Mask
#LoadMask(Instrument='IN5',InputFile=maskFile ,OutputWorkspace='IN5_Mask')
# Apply mask to the detector - data
#MaskDetectors(Workspace=wsName,MaskedWorkspace='IN5_Mask')

#1.3) Do sample - t*EC
MultiplyRange(InputWorkspace=wsName,OutputWorkspace='Data_t',Factor=transmission)

# ; ---------------------------------------------------------------------
# ;
# ; 4) Correction for detector wavelength-efficiency +
# ;    remove flat bkgd.

# Convert from TOF to Energy
ConvertUnits(InputWorkspace='Data_t',OutputWorkspace='Data_c_DeltaE',Target='DeltaE',EMode='Direct')
# Detctor efficiency: only runs for in4,5,6
DetectorEfficiencyCorUser(InputWorkspace='Data_c_DeltaE',OutputWorkspace='Data_c_DeltaE_effc')

# Rebin in energy
Rebin(InputWorkspace='Data_c_DeltaE_effc',OutputWorkspace='Data_DeltaE_Rebin',Params=rebiningInEnergy,PreserveEvents='0')
# SofQW
SofQW3(InputWorkspace='Data_DeltaE_Rebin',OutputWorkspace='Data_DeltaE_SofQW',QAxisBinning=rebiningInQ,EMode='Direct', EFixed=eFixed)
#
CorrectKiKf(InputWorkspace='Data_DeltaE_SofQW',OutputWorkspace='Data_DeltaE_KiKf')

# Those are optional!
#
Transpose(InputWorkspace='Data_DeltaE_KiKf',OutputWorkspace='Data_DeltaE_KiKf_T')
#
Logarithm(InputWorkspace='Data_DeltaE_KiKf_T',OutputWorkspace='Data_DeltaE_KiKf_T_log')

