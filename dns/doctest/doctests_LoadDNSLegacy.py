import os
#===================================
# example 1 --- load diffraction mode file
#==================================
datapath = "/datadisk/build/jcns-mantid/build/ExternalData/Testing/Data/UnitTest/"

# data file.
#datafiles = 'dn134011vana.d_dat,dnstof.d_dat'
datafile = os.path.join(datapath, "dn134011vana.d_dat")

# Load dataset
ws = LoadDNSLegacy(datafile, Normalization='monitor')

print("This workspace has {} dimensions and has {} histograms.".format(ws.getNumDims(), ws.getNumberHistograms()))

#==========================================
# example 2 --- load TOF file and find elastic channel
#==========================================
datapath = "/datadisk/build/jcns-mantid/build/ExternalData/Testing/Data/UnitTest/"

# data file.
datafile = os.path.join(datapath, "dnstof.d_dat")

# Load dataset
ws = LoadDNSLegacy(datafile, Normalization='no')
print("This workspace has {} dimensions and has {} histograms.\n".format(ws.getNumDims(), ws.getNumberHistograms()))

# sum spectra over all detectors
ws_sum = SumSpectra(ws)
# perform fit
peak_center, sigma = FitGaussian(ws_sum, 0)
print("Elastic peak center is at {} microseconds and has sigma={}.\n".format(round(peak_center), round(sigma)))
# calculate the elastic channel number
channel_width = ws.getRun().getProperty("channel_width").value
tof1 = ws.getRun().getProperty("TOF1").value
t_delay = ws.getRun().getProperty("delay_time").value
epp = round((peak_center - t_delay - tof1)/channel_width)

print("The channel width is {} microseconds.\n".format(channel_width))
print("The elastic channel number is: {}.\n".format(epp))

#================================================
# example 3 --- load TOF file and specify the elastic channel
#================================================
datapath = "/datadisk/build/jcns-mantid/build/ExternalData/Testing/Data/UnitTest/"

# data file.
datafile = os.path.join(datapath, "dnstof.d_dat")

# Load dataset
ws = LoadDNSLegacy(datafile, ElasticChannel=65, Normalization='no')

# let's check that the elastic peak is at the right position
from scipy.constants import m_n, h

l1 = 0.4     # distance from chopper to sample, m
l2 = 0.85   # distance from sample to detector, m
wavelength = ws.getRun().getProperty("wavelength").value   # neutron wavelength, Angstrom

# neutron velocity
velocity = h/(m_n*wavelength*1e-10)

# calculate elastic TOF (total)
tof2_elastic = 1e+06*l2/velocity
tof1 = ws.getRun().getProperty("TOF1").value
t_delay = ws.getRun().getProperty("delay_time").value
tof_elastic = t_delay + tof1 + tof2_elastic
print ("Calculated elastic TOF: {} microseconds".format(round(tof_elastic)))

# get elastic TOF from file
ws_sum = SumSpectra(ws)
peak_center, sigma = FitGaussian(ws_sum, 0)
print ("Elastic TOF in the workspace: {} microseconds".format(round(peak_center)))

# compare difference to the channel width
channel_width = ws.getRun().getProperty("channel_width").value
print("Difference = {} microseconds < channel width = {} microseconds."
           .format(round(tof_elastic - peak_center), channel_width, round(sigma)))
channel_width = ws.getRun().getProperty("channel_width").value