import os
import numpy as np

datapath = "/datadisk/build/tof/dns/data/Yixi/"
ndir_run_numbers = range(408994,409000)
ndir9_run_numbers = range(408964,408970)
ndir_fname = "service0000{}ndir.d_dat"
vana_run_numbers = range(409009,409012)
vana7_run_numbers = range(409006,409009)
vana_fname = "service0000{}vana.d_dat"
leer_run_numbers = range(409017,409022)
leer7_run_numbers = range(409012,409017)
leer_fname = "service0000{}leer.d_dat"

normalization = "mon_sum"   # alternatively 'duration'

def load_data(fname, run_numbers, prefix):
    wslist = []
    for rn in run_numbers:
        infile = fname.format(rn)
        wsname = os.path.splitext(infile)[0]
        LoadDNSLegacy(os.path.join(datapath, infile), Normalization='no', ElasticChannel=144, OutputWorkspace=wsname)
        wslist.append(wsname)
    
    ws = MergeRuns(wslist, SampleLogsSum='mon_sum,duration', OutputWorkspace=prefix)
    return ws
    
# load and merge sample data
ndir_raw = load_data(ndir_fname, ndir_run_numbers, "ndir_raw")
ndir9_raw = load_data(ndir_fname, ndir9_run_numbers, "ndir9_raw")

# load and merge vanadium data
vana_raw = load_data(vana_fname, vana_run_numbers, "vana_raw")
vana7_raw = load_data(vana_fname, vana7_run_numbers, "vana7_raw")

# load and merge empty can data
ec_raw = load_data(leer_fname, leer_run_numbers, "ec_raw")
ec7_raw = load_data(leer_fname, leer7_run_numbers, "ec7_raw")

# normalize
norm = ndir_raw.getRun().getLogData(normalization).value
ndir = ndir_raw/norm

norm = ndir9_raw.getRun().getLogData(normalization).value
ndir9 = ndir9_raw/norm

norm = vana_raw.getRun().getLogData(normalization).value
vana = vana_raw/norm

norm = vana7_raw.getRun().getLogData(normalization).value
vana7 = vana7_raw/norm

norm = ec_raw.getRun().getLogData(normalization).value
ec= ec_raw/norm

norm = ec7_raw.getRun().getLogData(normalization).value
ec7= ec7_raw/norm

# group
gndir = GroupWorkspaces([ndir, ndir9])
gvana = GroupWorkspaces([vana, vana7])
gec = GroupWorkspaces([ec, ec7])
for g in [gndir, gvana, gec]:
    MaskDetectors(g, SpectraList=[1])
    
# subtract empty can
ecFactor = 1.0
gndir_subEC = gndir - ecFactor*gec
gvana_subEC = gvana - ecFactor*gec

# normalise to vanadium
epptable = FindEPP(gvana_subEC)
coefs = ComputeCalibrationCoefVan(gvana_subEC, epptable)
for coef_ws in coefs:
    badDetectors = np.where(np.array(coef_ws.extractY()).flatten() <= 0)[0]
    print("Following detectors will be masked: ", badDetectors)
    MaskDetectors(gndir_subEC, DetectorList=badDetectors)

gndir_vcorr = Divide(gndir_subEC, coefs)
gvana_vcorr = Divide(gvana_subEC, coefs)

gndir_corr = CorrectTOF(gndir_vcorr, epptable)
gvana_corr = CorrectTOF(gvana_vcorr, epptable)

# get Ei
Ei = ndir.getRun().getLogData('Ei').value

# get S(q,w)
gndir_dE = ConvertUnits(gndir_corr, Target='DeltaE', EMode='Direct', EFixed=Ei)
ConvertToDistribution(gndir_dE)
gndir_dE_S = CorrectKiKf(gndir_dE)


gvana_dE = ConvertUnits(gvana_corr, Target='DeltaE', EMode='Direct', EFixed=Ei)
ConvertToDistribution(gvana_dE)
gvana_dE_S = CorrectKiKf(gvana_dE)

gec_dE = ConvertUnits(gec, Target='DeltaE', EMode='Direct', EFixed=Ei)
ConvertToDistribution(gec_dE)
gec_dE_S = CorrectKiKf(gec_dE)

# convert to MD
minvals,maxvals=ConvertToMDMinMaxGlobal(gndir_dE_S[0], '|Q|','Direct')
print(minvals)
print(maxvals)

gndir_mde = ConvertToMD(gndir_dE_S, QDimensions='|Q|', dEAnalysisMode='Direct',
                        PreprocDetectorsWS="-", MinValues=minvals, MaxValues=maxvals)
ndir_mde = MergeMD(gndir_mde)
gvana_mde = ConvertToMD(gvana_dE_S, QDimensions='|Q|', dEAnalysisMode='Direct',
                        PreprocDetectorsWS="-", MinValues=minvals, MaxValues=maxvals)
vana_mde = MergeMD(gvana_mde)

xmin = 0.55
xmax = 2.0
xstep = 0.02
xbins = int((xmax - xmin)/xstep)
xmax = xmin + xbins*xstep
ad0='|Q|,'+str(xmin)+','+str(xmax)+','+str(xbins)
ymin = -2.0
ymax = 2.0
ystep = 0.01
ybins = int((ymax - ymin)/ystep)
ymax = ymin + ybins*ystep
ad1='DeltaE,'+str(ymin)+','+str(ymax)+','+str(ybins)
ndir_sqw = BinMD(InputWorkspace=ndir_mde, AlignedDim0=ad0, AlignedDim1=ad1)
ndir0 = RenameWorkspace(gndir_mde[0])
ndir1_sqw = BinMD(InputWorkspace=ndir0, AlignedDim0=ad0, AlignedDim1=ad1)