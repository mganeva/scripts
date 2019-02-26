import numpy as np
from dnstof import *

__author__ = "m.ganeva.fz-juelich.de"

 #-------------------------
# Settings
#-------------------------   
data_path = '/datadisk/data/dns/2018/p13656/data'
#data_path = '/Users/ysu/dns-nicos/tof/00_p13656_EPFL'

n_det_pos = 5   # number of detector positions
data1_runs = [228, 270]   # [from, to]    # low temperature
data2_runs = [273, 294]                          # high temperature
ec_runs = [295, 299]                                
vanadium_runs = [300, 302]                    
data_file_name = 'p13656_557{}.d_dat'

elastic_channel = 658  # channel where the elastic peak is observed
wavelength = 0.0          # neutron wavelength in Angstrom. If 0 will be read from data file.

normalization = "mon_sum"   # alternatively 'duration'

ecFactor = 0.8      # factor to multiply empty can before subtraction =0.8
subtract_empty_can_from_vanadium = True     # put True  if yes or False if no

vanadium_temperature = 290.0  # K

correct_tof = True
delete_raw_data = True

# binning in Q (A^-1)
qmin = 0.38
qmax = 2.65
qstep = 0.025

# binning in Energy Transfer (meV)
dEmin = -2.5
dEmax = 2.5
dEstep = 0.05

 #-------------------------
# Data reduction
#-------------------------   
# set parameters dictionaries, do not change it
params = {'path': data_path, 'fname': data_file_name, 'detpos': n_det_pos, 'e_channel': elastic_channel, 'wavelength': wavelength, 'delete_raw': delete_raw_data}
bins = {'qmin': qmin, 'qmax': qmax, 'qstep': qstep, 'dEmin': dEmin, 'dEmax': dEmax, 'dEstep': dEstep}

# load data
load_data(data1_runs, "raw_data1", params)
load_data(data2_runs, "raw_data2", params)
# load empty can and vanadium data
params['detpos'] = 1      # only 1 detector position for empty can and vanadium, feel free to change it
load_data(ec_runs, "raw_ec", params) 
load_data(vanadium_runs, "raw_vanadium", params)

# normalize
data1 = MonitorEfficiencyCorUser("raw_data1")
data2 = MonitorEfficiencyCorUser("raw_data2")
ec =  MonitorEfficiencyCorUser("raw_ec")
vanadium =  MonitorEfficiencyCorUser("raw_vanadium")

# scale empty can
if ec.getNumberOfEntries() != n_det_pos:
    ecScaled = ecFactor*ec[0]          # only one detector position for empty can
else:
    ecScaled = ecFactor*ec              # n_det_pos detector positions for empty can

# subtract empty can   
data1 = data1- ecScaled
data2 = data2 - ecScaled

if subtract_empty_can_from_vanadium:
    vanadium = vanadium - ecScaled

# check for vanadium detector positions
if vanadium.getNumberOfEntries() != n_det_pos:
    vana = vanadium[0]
else:
    vana = vanadium
    
# detector efficciency correction: compute coefficients
epptable = FindEPP(vana)
coefs = ComputeCalibrationCoefVan(vana, epptable, Temperature=vanadium_temperature)

# get list of bad detectors
if isinstance(coefs, WorkspaceGroup):
    badDetectors = np.where(np.array(coefs[0].extractY()).flatten() <= 0)[0]
else:
    badDetectors = np.where(np.array(coefs.extractY()).flatten() <= 0)[0]
print("Following detectors will be masked: ", badDetectors)
MaskDetectors(data1, DetectorList=badDetectors)
MaskDetectors(data2, DetectorList=badDetectors)

# apply detector efficiency correction
data1 = Divide(data1, coefs)
data2 = Divide(data2, coefs)
vanadium_corr = Divide(vanadium, coefs)

# correct TOF to get EPP at 0 meV
if correct_tof:
    data1 = CorrectTOF(data1, epptable)
    data2 = CorrectTOF(data2, epptable)
    vanadium_corr = CorrectTOF(vanadium_corr, epptable)

# get Ei
Ei = data1[0].getRun().getLogData('Ei').value
print ("Incident Energy is {} meV".format(Ei))

# get S(q,w)
convert_to_dE('data1', Ei)
convert_to_dE('data2', Ei)
convert_to_dE('vanadium_corr', Ei)

# merge al detector positions together
get_sqw('data1_dE_S', 'data1', bins)
get_sqw('data2_dE_S', 'data2', bins)
get_sqw('vanadium_corr_dE_S', 'vanadium', bins)

# difference, I think it is better to subtract already reduced data
data_delta_sqw = mtd['data1_sqw'] - mtd['data2_sqw']

result_sqw = GroupWorkspaces(['data1_sqw', 'data2_sqw', 'data_delta_sqw', 'vanadium_sqw'])
 
