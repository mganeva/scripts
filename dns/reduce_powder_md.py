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

start_time = timeit.default_timer() 

# to avoid automatic data scaling by plotting
config['graph1d.autodistribution'] = 'Off'

datapath = "/datadisk/build/jcns-mantid/dns/JCNS_LabCourse2013/mag"
stdpath = "/datadisk/build/jcns-mantid/dns/JCNS_LabCourse2013/mag/xyz_powder_rc32"


polarisations = ['x', 'y', 'z']
fname="cr192{:03d}003.d_dat"

normalizeto = 'monitor'
two_theta_limits = '4.0,130.0'

# assume dnsplot file order
runs_x_sf = range(1, 31, 6)
runs_x_nsf = range(2, 31, 6)
runs_y_sf = range(3, 31, 6)
runs_y_nsf = range(4, 31, 6)
runs_z_sf = range(5, 31, 6)
runs_z_nsf = range(6, 31, 6)

# load data
edata_xsf, edata_xsf_norm = LoadDNSSCD(", ".join([join(datapath, fname.format(i)) for i in runs_x_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
edata_xnsf, edata_xnsf_norm = LoadDNSSCD(", ".join([join(datapath, fname.format(i)) for i in runs_x_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

edata_ysf, edata_ysf_norm = LoadDNSSCD(", ".join([join(datapath, fname.format(i)) for i in runs_y_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
edata_ynsf, edata_ynsf_norm = LoadDNSSCD(", ".join([join(datapath, fname.format(i)) for i in runs_y_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

edata_zsf, edata_zsf_norm = LoadDNSSCD(", ".join([join(datapath, fname.format(i)) for i in runs_z_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
edata_znsf, edata_znsf_norm = LoadDNSSCD(", ".join([join(datapath, fname.format(i)) for i in runs_z_nsf]), 
                                            Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

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
leer_runs_x_sf = range(31, 61, 6)
leer_runs_x_nsf = range(32, 61, 6)
leer_runs_y_sf = range(33, 61, 6)
leer_runs_y_nsf = range(34, 61, 6)
leer_runs_z_sf = range(35, 61, 6)
leer_runs_z_nsf = range(36, 61, 6)

eleer_xsf, eleer_xsf_norm = LoadDNSSCD(", ".join([join(stdpath, leerfname.format(i)) for i in leer_runs_x_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
eleer_xnsf, eleer_xnsf_norm = LoadDNSSCD(", ".join([join(stdpath, leerfname.format(i)) for i in leer_runs_x_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

eleer_ysf, eleer_ysf_norm = LoadDNSSCD(", ".join([join(stdpath, leerfname.format(i)) for i in leer_runs_y_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
eleer_ynsf, eleer_ynsf_norm = LoadDNSSCD(", ".join([join(stdpath, leerfname.format(i)) for i in leer_runs_y_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

eleer_zsf, eleer_zsf_norm = LoadDNSSCD(", ".join([join(stdpath, leerfname.format(i)) for i in leer_runs_z_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
eleer_znsf, eleer_znsf_norm = LoadDNSSCD(", ".join([join(stdpath, leerfname.format(i)) for i in leer_runs_z_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

# load nicr
nicrfname = "dn125{:03d}nicr.d_dat"
nicr_runs_x_sf = range(13, 43, 6)
nicr_runs_x_nsf = range(14, 43, 6)
nicr_runs_y_sf = range(15, 43, 6)
nicr_runs_y_nsf = range(16, 43, 6)
nicr_runs_z_sf = range(17, 43, 6)
nicr_runs_z_nsf = range(18, 43, 6)

enicr_xsf, enicr_xsf_norm = LoadDNSSCD(", ".join([join(stdpath, nicrfname.format(i)) for i in nicr_runs_x_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
enicr_xnsf, enicr_xnsf_norm = LoadDNSSCD(", ".join([join(stdpath, nicrfname.format(i)) for i in nicr_runs_x_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

enicr_ysf, enicr_ysf_norm = LoadDNSSCD(", ".join([join(stdpath, nicrfname.format(i)) for i in nicr_runs_y_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
enicr_ynsf, enicr_ynsf_norm = LoadDNSSCD(", ".join([join(stdpath, nicrfname.format(i)) for i in nicr_runs_y_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)

enicr_zsf, enicr_zsf_norm = LoadDNSSCD(", ".join([join(stdpath, nicrfname.format(i)) for i in nicr_runs_z_sf]), 
                                       Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)
enicr_znsf, enicr_znsf_norm = LoadDNSSCD(", ".join([join(stdpath, nicrfname.format(i)) for i in nicr_runs_z_nsf]), 
                                         Normalization=normalizeto, LoadAs="raw", TwoThetaLimits=two_theta_limits)


elapsed1 = timeit.default_timer() - start_time
print("MD data loading: ", elapsed1, " seconds")
#==========================
# bin all the data (put on the same grid)
# TODO: make it in a loop
#==========================
ad0 = 'Theta,4.2,61.8,110'
ad1 = 'Omega,0.0,359.0,1'
ad2 = 'TOF,424.0,2000.0,1'

data_x_sf = BinMD(InputWorkspace=edata_xsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_x_sf_norm = BinMD(InputWorkspace=edata_xsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_x_nsf = BinMD(InputWorkspace=edata_xnsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_x_nsf_norm = BinMD(InputWorkspace=edata_xnsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

data_y_sf = BinMD(InputWorkspace=edata_ysf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_y_sf_norm = BinMD(InputWorkspace=edata_ysf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_y_nsf = BinMD(InputWorkspace=edata_ynsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_y_nsf_norm = BinMD(InputWorkspace=edata_ynsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

data_z_sf = BinMD(InputWorkspace=edata_zsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_z_sf_norm = BinMD(InputWorkspace=edata_zsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_z_nsf = BinMD(InputWorkspace=edata_znsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
data_z_nsf_norm = BinMD(InputWorkspace=edata_znsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

# vanadium
raw_vana_sf = BinMD(InputWorkspace=evana_sf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
vana_sf_norm = BinMD(InputWorkspace=evana_sf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
raw_vana_nsf = BinMD(InputWorkspace=evana_nsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
vana_nsf_norm = BinMD(InputWorkspace=evana_nsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

# background
leer_x_sf = BinMD(InputWorkspace=eleer_xsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_x_sf_norm = BinMD(InputWorkspace=eleer_xsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_x_nsf = BinMD(InputWorkspace=eleer_xnsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_x_nsf_norm = BinMD(InputWorkspace=eleer_xnsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

leer_y_sf = BinMD(InputWorkspace=eleer_ysf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_y_sf_norm = BinMD(InputWorkspace=eleer_ysf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_y_nsf = BinMD(InputWorkspace=eleer_ynsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_y_nsf_norm = BinMD(InputWorkspace=eleer_ynsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

leer_z_sf = BinMD(InputWorkspace=eleer_zsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_z_sf_norm = BinMD(InputWorkspace=eleer_zsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_z_nsf = BinMD(InputWorkspace=eleer_znsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
leer_z_nsf_norm = BinMD(InputWorkspace=eleer_znsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

# nicr
raw_nicr_x_sf = BinMD(InputWorkspace=enicr_xsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
nicr_x_sf_norm = BinMD(InputWorkspace=enicr_xsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
raw_nicr_x_nsf = BinMD(InputWorkspace=enicr_xnsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
nicr_x_nsf_norm = BinMD(InputWorkspace=enicr_xnsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)

raw_nicr_y_sf = BinMD(InputWorkspace=enicr_ysf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
nicr_y_sf_norm = BinMD(InputWorkspace=enicr_ysf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
raw_nicr_y_nsf = BinMD(InputWorkspace=enicr_ynsf, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1, AlignedDim2=ad2)
nicr_y_nsf_norm = BinMD(InputWorkspace=enicr_ynsf_norm, AxisAligned=True, AlignedDim0=ad0, AlignedDim1=ad1,AlignedDim2=ad2)

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

for p in polarisations:
    #DivideMD('data_{}_sf_norm'.format(p), 'leer_{}_sf_norm'.format(p),
    #         OutputWorkspace='data_{}_sf_nratio'.format(p))
    #DivideMD('data_{}_nsf_norm'.format(p), 'leer_{}_nsf_norm'.format(p),
    #         OutputWorkspace='data_{}_nsf_nratio'.format(p))
    #MultiplyMD('leer_{}_sf'.format(p), 'data_{}_sf_nratio'.format(p),
    #           OutputWorkspace='bkgd_scaled_{}_sf'.format(p))
    #MultiplyMD('leer_{}_nsf'.format(p), 'data_{}_nsf_nratio'.format(p),
    #           OutputWorkspace='bkgd_scaled_{}_nsf'.format(p))
    #MinusMD('raw_data_{}_sf'.format(p), 'bkgd_scaled_{}_sf'.format(p),
    #        OutputWorkspace='data_{}_sf'.format(p))
    #MinusMD('raw_data_{}_nsf'.format(p), 'bkgd_scaled_{}_nsf'.format(p),
    #        OutputWorkspace='data_{}_nsf'.format(p))
            
    DivideMD('nicr_{}_sf_norm'.format(p), 'leer_{}_sf_norm'.format(p),
             OutputWorkspace='nicr_{}_sf_nratio'.format(p))
    DivideMD('nicr_{}_nsf_norm'.format(p), 'leer_{}_nsf_norm'.format(p),
             OutputWorkspace='nicr_{}_nsf_nratio'.format(p))
    MultiplyMD('leer_{}_sf'.format(p), 'nicr_{}_sf_nratio'.format(p),
               OutputWorkspace='bkgn_scaled_{}_sf'.format(p))
    MultiplyMD('leer_{}_nsf'.format(p), 'nicr_{}_nsf_nratio'.format(p),
               OutputWorkspace='bkgn_scaled_{}_nsf'.format(p))
    MinusMD('raw_nicr_{}_sf'.format(p), 'bkgn_scaled_{}_sf'.format(p),
            OutputWorkspace='nicr_{}_sf'.format(p))
    MinusMD('raw_nicr_{}_nsf'.format(p), 'bkgn_scaled_{}_nsf'.format(p),
            OutputWorkspace='nicr_{}_nsf'.format(p))

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
for p in polarisations:
    MultiplyMD(coef, 'data_{}_sf_norm'.format(p), OutputWorkspace='data_{}_sf_norm'.format(p))
    MultiplyMD(coef, 'data_{}_nsf_norm'.format(p), OutputWorkspace='data_{}_nsf_norm'.format(p))
    
    DivideMD('data_{}_sf'.format(p), 'data_{}_sf_norm'.format(p),
             OutputWorkspace='data_vcorr_{}_sf'.format(p))
    DivideMD('data_{}_nsf'.format(p), 'data_{}_nsf_norm'.format(p),
             OutputWorkspace='data_vcorr_{}_nsf'.format(p))


# flipping ratio correction
for p in polarisations:
    # normalize nicr
    DivideMD('nicr_{}_sf'.format(p), 'nicr_{}_sf_norm'.format(p),
             OutputWorkspace='nnicr_{}_sf'.format(p))
    DivideMD('nicr_{}_nsf'.format(p), 'nicr_{}_nsf_norm'.format(p),
             OutputWorkspace='nnicr_{}_nsf'.format(p))
             
    # 1/k, where k = NSF/SF - 1
    MinusMD('nnicr_{}_nsf'.format(p), 'nnicr_{}_sf'.format(p),
            OutputWorkspace='inverse_fr_divider_{}'.format(p))
    DivideMD('nnicr_{}_sf'.format(p), 'inverse_fr_divider_{}'.format(p),
             OutputWorkspace='inverse_fr_{}'.format(p))
             
    # apply correction
    MinusMD('data_vcorr_{}_nsf'.format(p), 'data_vcorr_{}_sf'.format(p),
            OutputWorkspace='data_nsf_sf_diff_{}'.format(p))
    MultiplyMD('data_nsf_sf_diff_{}'.format(p), 'inverse_fr_{}'.format(p),
               OutputWorkspace='diff_ifr_{}'.format(p))
    MinusMD('data_vcorr_{}_sf'.format(p), 'diff_ifr_{}'.format(p), 
            OutputWorkspace='data_corr_{}_sf'.format(p))
    PlusMD('data_vcorr_{}_nsf'.format(p), 'diff_ifr_{}'.format(p),
           OutputWorkspace='data_corr_{}_nsf'.format(p))

# separate components
xsf_plus_ysf = PlusMD('data_corr_x_sf', 'data_corr_y_sf')
twice_zsf = mtd['data_corr_z_sf']*2
three_zsf = mtd['data_corr_z_sf']*3
half_imag = xsf_plus_ysf - twice_zsf
one_third_inc = three_zsf - xsf_plus_ysf
one_third_inc = one_third_inc*0.5
mag_inc_sum = half_imag + one_third_inc

data_magnetic = half_imag*2
data_spin_incoh = one_third_inc*3
data_nuclear_coh = mtd['data_corr_z_nsf'] - mag_inc_sum

# convert to matrix workspaces
data_magnetic_m = ConvertMDHistoToMatrixWorkspace(data_magnetic, Normalization='NoNormalization')
data_spin_incoh_m = ConvertMDHistoToMatrixWorkspace(data_spin_incoh, Normalization='NoNormalization')
data_nuclear_coh_m = ConvertMDHistoToMatrixWorkspace(data_nuclear_coh, Normalization='NoNormalization')

elapsed = timeit.default_timer() - start_time
print("MD approach total: ", elapsed, " seconds")
print("MD data reduction: ", elapsed - elapsed1, " seconds")

# see plotting documentation at https://docs.mantidproject.org/nightly/api/python/mantid/plots/index.html
fig, ax = plt.subplots()
plots.plotfunctions.errorbar(ax, data_magnetic_m, 'g', specNum=1, label='Magnetic')
plots.plotfunctions.errorbar(ax, data_nuclear_coh_m, 'b', specNum=1, label='Nuclear coherent')
plots.plotfunctions.errorbar(ax, data_spin_incoh_m, 'y', specNum=1, label='Spin incoherent')
ax.legend()
fig.show()