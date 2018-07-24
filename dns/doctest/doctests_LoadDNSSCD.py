# doctest1

# data file.
filename = "/datadisk/build/jcns-mantid/build/ExternalData/Testing/Data/UnitTest/dn134011vana.d_dat"

# lattice parameters
a = 5.0855
b = 5.0855
c = 14.0191
omega_offset = 225.0
hkl1="1,0,0"
hkl2="0,0,1"
alpha=90.0
beta=90.0
gamma=120.0

# load data to MDEventWorkspace
ws, ws_norm, huber_ws = LoadDNSSCD(FileNames=filename, NormalizationWorkspace='ws_norm',
                                   Normalization='monitor', a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma,
                                   OmegaOffset=omega_offset, HKL1=hkl1, HKL2=hkl2, SaveHuberTo='huber_ws')

# print output workspace information
print("Output Workspace Type is:  {}".format(ws.id()))
print("It has {0} events and {1} dimensions:".format(ws.getNEvents(), ws.getNumDims()))
for i in range(ws.getNumDims()):
    dimension = ws.getDimension(i)
    print("Dimension {0} has name: {1}, id: {2}, Range: {3:.2f} to {4:.2f} {5}".format(i,
             dimension.getDimensionId(),
             dimension.name,
             dimension.getMinimum(),
             dimension.getMaximum(),
             dimension.getUnits()))

# print information about the table workspace
print ("TableWorkspace '{0}' has {1} row in the column '{2}'.".format(huber_ws.name(),
                                                                         huber_ws.rowCount(),
                                                                         huber_ws.getColumnNames()[0]))
print("It contains sample rotation angle {} degrees".format(huber_ws.cell(0, 0)))


#=======================
#  Example 2
#=======================
filename = "/datadisk/build/jcns-mantid/build/ExternalData/Testing/Data/UnitTest/dn134011vana.d_dat"

# lattice parameters
a = 5.0855
b = 5.0855
c = 14.0191
omega_offset = 225.0
hkl1="1,0,0"
hkl2="0,0,1"
alpha=90.0
beta=90.0
gamma=120.0

# scattering angle limits, degrees
tth_limits = "20,70"

# load data to MDEventWorkspace
ws, ws_norm, huber_ws = LoadDNSSCD(FileNames=filename, NormalizationWorkspace='ws_norm',
                                      Normalization='monitor', a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma,
                                      OmegaOffset=omega_offset, HKL1=hkl1, HKL2=hkl2, TwoThetaLimits=tth_limits)

# print output workspace information
print("Output Workspace Type is:  {}".format(ws.id()))
print("It has {0} events and {1} dimensions.".format(ws.getNEvents(), ws.getNumDims()))

# print normalization workspace information
print("Normalization Workspace Type is:  {}".format(ws_norm.id()))
print("It has {0} events and {1} dimensions.".format(ws_norm.getNEvents(), ws_norm.getNumDims()))

#==========================
# Example 3
#==========================
# data file.
filename = "/datadisk/build/jcns-mantid/build/ExternalData/Testing/Data/UnitTest/dn134011vana.d_dat"

# construct table workspace with 10 raw sample rotation angles from 70 to 170 degrees
table = CreateEmptyTableWorkspace()
table.addColumn( "double", "Huber(degrees)")
for huber in range(70, 170, 10):
       table.addRow([huber])

# lattice parameters
a = 5.0855
b = 5.0855
c = 14.0191
omega_offset = 225.0
hkl1="1,0,0"
hkl2="0,0,1"
alpha=90.0
beta=90.0
gamma=120.0

# load data to MDEventWorkspace
ws, ws_norm, huber_ws = LoadDNSSCD(FileNames=filename, NormalizationWorkspace='ws_norm',
                                      Normalization='monitor', a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma,
                                      OmegaOffset=omega_offset, HKL1=hkl1, HKL2=hkl2, LoadHuberFrom=table)

# print output workspace information
print("Output Workspace Type is:  {}".format(ws.id()))
print("It has {0} events and {1} dimensions.".format(ws.getNEvents(), ws.getNumDims()))

# setting for the BinMD algorithm
bvec0 = '[100],unit,1,0,0,0'
bvec1 = '[001],unit,0,0,1,0'
bvec2 = '[010],unit,0,1,0,0'
bvec3 = 'dE,meV,0,0,0,1'
extents = '-2,1.5,-0.2,6.1,-10,10,-10,4.6'
bins = '10,10,1,1'
# bin the data
data_raw = BinMD(ws, AxisAligned='0', BasisVector0=bvec0, BasisVector1=bvec1,
                    BasisVector2=bvec2, BasisVector3=bvec3, OutputExtents=extents, OutputBins=bins, NormalizeBasisVectors='0')
# bin normalization
data_norm = BinMD(ws_norm, AxisAligned='0', BasisVector0=bvec0, BasisVector1=bvec1,
                     BasisVector2=bvec2, BasisVector3=bvec3, OutputExtents=extents, OutputBins=bins, NormalizeBasisVectors='0')
# normalize data
data = data_raw/data_norm

# print reduced workspace information
print("Reduced Workspace Type is:  {}".format(data.id()))
print("It has {} dimensions.".format(data.getNumDims()))
s =  data.getSignalArray()
print("Signal at some points: {0:.4f}, {1:.4f}, {2:.4f}".format(float(s[7,1][0]), float(s[7,2][0]), float(s[7,3][0])))

