from os import listdir
from os.path import isfile, join, splitext
import re
import numpy as np
import timeit

start_time = timeit.default_timer() 

datapath = "/datadisk/data/dns/2018/tof_service/data"

name_template = 'tof_service_{}.d_dat'
runs = range(562964, 563104)       

#======================
# Parameters of the magnetic single crystal
#=======================
a = 5.497
b = 5.497
c = 13.332
omega_offset = 54.8
u="1,0,0"
v="0,1,0"
alpha=90.0
beta=90.0
gamma=120.0
#theta_min=12.0
#theta_max=110.0

#=======================
# load single crystal data
#=======================
datafiles = [join(datapath, name_template.format(format(i))) for i in runs]

LoadDNSSCD(FileNames=", ".join(datafiles), NormalizationWorkspace='edata_norm', 
                      Normalization='monitor', a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma, 
                      OmegaOffset=omega_offset, hkl1=u, hkl2=v, SaveHuberTo='huber',  ElasticChannel=651,
                      OutputWorkspace='raw_edata')
           
#==========================
# bin the data
#==========================
bvector0 = '[100],unit,1,0,0,0'
bvector1 = '[010],unit,0,1,0,0'
bvector2 = '[001],unit,0,0,1,0'
bvector3='dE,meV,0,0,0,1'
extents = '-1.1,3.3,-3.3,0.75,-40,40,-10,4.64'
bins = '130,80,1,1'

# data and normalizations
raw_data = BinMD('raw_edata', AxisAligned='0', BasisVector0=bvector0, BasisVector1=bvector1, BasisVector2=bvector2,  
                              BasisVector3=bvector3, OutputExtents=extents, OutputBins=bins, NormalizeBasisVectors='0')
data_norm = BinMD('edata_norm', AxisAligned='0', BasisVector0=bvector0, BasisVector1=bvector1, BasisVector2=bvector2,  
                                 BasisVector3=bvector3, OutputExtents=extents, OutputBins=bins, NormalizeBasisVectors='0')
                                 
 #==========================
# normalize and plot
#==========================
data = raw_data/data_norm

import matplotlib.pyplot as plt
from mantid import plots

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
ax.pcolor(data)
ax.set_title('Inelastic Single Crystal')
fig.show()