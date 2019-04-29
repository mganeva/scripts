# The following line helps with future compatibility with Python 3
# print must now be used as a function, e.g print('Hello','World')
from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *

import matplotlib.pyplot as plt
from mantid import plots

import numpy as np

from os.path import join
import timeit

# to avoid automatic data scaling by plotting
config['graph1d.autodistribution'] = 'Off'

start_time = timeit.default_timer() 

stdpath = "/datadisk/build/jcns-mantid/dns/JCNS_LabCourse2013/standard"

p = 'z'

normalizeto = 'time'
two_theta_limits = '4.0,130.0'

# assume dnsplot file order

# load vanadium
vanafname = "dn135{:03d}vana.d_dat"
vana_runs_sf = range(1, 11, 2)
vana_runs_nsf = range(2, 11, 2)
evana_sf, evana_sf_norm = LoadDNSSCD(", ".join([join(stdpath, vanafname.format(i)) for i in vana_runs_sf]), 
                                     Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
evana_nsf, evana_nsf_norm = LoadDNSSCD(", ".join([join(stdpath, vanafname.format(i)) for i in vana_runs_nsf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
                                         
# load background
leerfname = "dn134{:03d}leer.d_dat"
leer_runs_z_sf = range(35, 61, 6)
leer_runs_z_nsf = range(36, 61, 6)

eleer_zsf, eleer_zsf_norm = LoadDNSSCD(", ".join([join(stdpath, leerfname.format(i)) for i in leer_runs_z_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
eleer_znsf, eleer_znsf_norm = LoadDNSSCD(", ".join([join(stdpath, leerfname.format(i)) for i in leer_runs_z_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

# load nicr
nicrfname = "dn125{:03d}nicr.d_dat"
nicr_runs_z_sf = range(17, 43, 6)
nicr_runs_z_nsf = range(18, 43, 6)

enicr_zsf, enicr_zsf_norm = LoadDNSSCD(", ".join([join(stdpath, nicrfname.format(i)) for i in nicr_runs_z_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
enicr_znsf, enicr_znsf_norm = LoadDNSSCD(", ".join([join(stdpath, nicrfname.format(i)) for i in nicr_runs_z_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)


elapsed1 = timeit.default_timer() - start_time
print("MD data loading: ", elapsed1, " seconds")


#==========================
# bin all the data (put on the same grid)
#==========================
ad0 = 'Theta,4.2,61.8,110'
ad1 = 'Omega,0.0,359.0,1'
ad2 = 'TOF,424.0,2000.0,1'

# vanadium
raw_vana_sf = BinMD(InputWorkspace=evana_sf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
vana_sf_norm = BinMD(InputWorkspace=evana_sf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
raw_vana_nsf = BinMD(InputWorkspace=evana_nsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
vana_nsf_norm = BinMD(InputWorkspace=evana_nsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

# background
leer_z_sf = BinMD(InputWorkspace=eleer_zsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_z_sf_norm = BinMD(InputWorkspace=eleer_zsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_z_nsf = BinMD(InputWorkspace=eleer_znsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_z_nsf_norm = BinMD(InputWorkspace=eleer_znsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

# nicr
raw_nicr_z_sf = BinMD(InputWorkspace=enicr_zsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
nicr_z_sf_norm = BinMD(InputWorkspace=enicr_zsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
raw_nicr_z_nsf = BinMD(InputWorkspace=enicr_znsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
nicr_z_nsf_norm = BinMD(InputWorkspace=enicr_znsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
#==========================
# data reduction
#==========================

# subtract background
vana_sf_nratio = vana_sf_norm/mtd['leer_z_sf_norm']
vana_nsf_nratio = vana_nsf_norm/mtd['leer_z_nsf_norm']
bkgv_scaled_sf = mtd['leer_z_sf']*vana_sf_nratio
bkgv_scaled_nsf = mtd['leer_z_nsf']*vana_nsf_nratio
vana_sf = raw_vana_sf - bkgv_scaled_sf
vana_nsf = raw_vana_nsf - bkgv_scaled_nsf
         
DivideMD('nicr_{}_sf_norm'.format(p), 'leer_{}_sf_norm'.format(p), OutputWorkspace='nicr_{}_sf_nratio'.format(p))
DivideMD('nicr_{}_nsf_norm'.format(p), 'leer_{}_nsf_norm'.format(p),OutputWorkspace='nicr_{}_nsf_nratio'.format(p))
MultiplyMD('leer_{}_sf'.format(p), 'nicr_{}_sf_nratio'.format(p), OutputWorkspace='bkgn_scaled_{}_sf'.format(p))
MultiplyMD('leer_{}_nsf'.format(p), 'nicr_{}_nsf_nratio'.format(p), OutputWorkspace='bkgn_scaled_{}_nsf'.format(p))
MinusMD('raw_nicr_{}_sf'.format(p), 'bkgn_scaled_{}_sf'.format(p), OutputWorkspace='nicr_{}_sf'.format(p))
MinusMD('raw_nicr_{}_nsf'.format(p), 'bkgn_scaled_{}_nsf'.format(p), OutputWorkspace='nicr_{}_nsf'.format(p))

# compute vanadium correction coefficients
vana_sum = vana_sf + vana_nsf
vana_sum_norm = vana_sf_norm + vana_nsf_norm

# this may give NaN if the binning is too fine and vana_sum contains NaNs
vana_total = IntegrateMDHistoWorkspace(vana_sum, P1Bin=[5.0,124.5], P2Bin=[])
vana_total_norm = IntegrateMDHistoWorkspace(vana_sum_norm, P1Bin=[5.0,124.5], P2Bin=[])
#nevents = vana_total.getNumEventsArray()[0][0]
vana_total = CreateSingleValuedWorkspace(DataValue=vana_total.getSignalArray()[0][0][0],
                                         ErrorValue=np.sqrt(vana_total.getErrorSquaredArray()[0][0][0]))
#nevents = vana_total_norm.getNumEventsArray()[0][0]                                         
vana_total_norm = CreateSingleValuedWorkspace(DataValue=vana_total_norm.getSignalArray()[0][0][0],
                                              ErrorValue=np.sqrt(vana_total_norm.getErrorSquaredArray()[0][0][0]))

coef_u = vana_sum/vana_total
coef_norm = vana_sum_norm/vana_total_norm

coef = coef_u/coef_norm

# apply vanadium correction
MultiplyMD(coef, 'vana_sf_norm', OutputWorkspace='vana_sf_norm'.format(p))
MultiplyMD(coef, 'vana_nsf_norm', OutputWorkspace='vana_nsf_norm'.format(p))
DivideMD('vana_sf', 'vana_sf_norm', OutputWorkspace='vana_vcorr_sf'.format(p))
DivideMD('vana_nsf', 'vana_nsf_norm', OutputWorkspace='vana_vcorr_nsf'.format(p))

# for plotting in the workbench
m_vana_sf = ConvertMDHistoToMatrixWorkspace('vana_vcorr_sf', Normalization='NoNormalization')
m_vana_nsf = ConvertMDHistoToMatrixWorkspace('vana_vcorr_nsf', Normalization='NoNormalization')
m_vana_sum = m_vana_nsf + m_vana_sf

# flipping ratio correction

# normalize nicr
DivideMD('nicr_{}_sf'.format(p), 'nicr_{}_sf_norm'.format(p), OutputWorkspace='nnicr_{}_sf'.format(p))
DivideMD('nicr_{}_nsf'.format(p), 'nicr_{}_nsf_norm'.format(p), OutputWorkspace='nnicr_{}_nsf'.format(p))
             
# 1/k, where k = NSF/SF - 1
MinusMD('nnicr_{}_nsf'.format(p), 'nnicr_{}_sf'.format(p),OutputWorkspace='inverse_fr_divider_{}'.format(p))
DivideMD('nnicr_{}_sf'.format(p), 'inverse_fr_divider_{}'.format(p), OutputWorkspace='inverse_fr_{}'.format(p))
             
# apply correction
MinusMD('vana_vcorr_nsf', 'vana_vcorr_sf', OutputWorkspace='vana_nsf_sf_diff')
MultiplyMD('vana_nsf_sf_diff', 'inverse_fr_{}'.format(p), OutputWorkspace='diff_ifr_{}'.format(p))
MinusMD('vana_vcorr_sf', 'diff_ifr_{}'.format(p), OutputWorkspace='vana_corr_sf'.format(p))
PlusMD('vana_vcorr_nsf', 'diff_ifr_{}'.format(p), OutputWorkspace='vana_corr_nsf'.format(p))

# for plotting in the workbench    
m_vana_corr_sf = ConvertMDHistoToMatrixWorkspace('vana_corr_sf', Normalization='NoNormalization')
m_vana_corr_nsf = ConvertMDHistoToMatrixWorkspace('vana_corr_nsf', Normalization='NoNormalization')
m_vana_corr_ratio = m_vana_corr_sf/m_vana_corr_nsf

# v_ratio = DivideMD('vana_corr_sf', 'vana_corr_nsf')
# print(np.round(v_ratio.getSignalArray()))

fig, ax = plt.subplots()
plots.plotfunctions.plot(ax, m_vana_corr_ratio, 'go-', specNum=1, label='Vanadium flipping ratio')
ax.legend()
fig.show()
