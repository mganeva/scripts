import os

datapath = "/datadisk/data/dns/2018/tof_service/data"
fname = "tof_service_{}.d_dat"

sample_run_numbers = range(653783,653798)
vana_run_numbers = range(653805,653821)    # 15000 rpm
leer_run_numbers = range(653771,653776)

vana2_run_numbers = range(653821,653826)    # 9000 rpm
vana3_run_numbers = range(653826,653831)    # 6000 rpm

normalization = "mon_sum"   # alternatively 'duration'

def load_data(run_numbers, echannel, prefix):
    wslist = []
    for rn in run_numbers:
        infile = fname.format(rn)
        wsname = os.path.splitext(infile)[0]
        LoadDNSLegacy(os.path.join(datapath, infile), Normalization='no', ElasticChannel=echannel, Wavelength=5.7, OutputWorkspace=wsname)
        wslist.append(wsname)
        
    ws = MergeRuns(wslist, SampleLogsSum='mon_sum,duration', OutputWorkspace=prefix)
    return ws
   
 
vana15_1 = load_data(vana_run_numbers[::5], 50, 'vana15_1')
vana15_2 = load_data(vana_run_numbers[1::5], 50, 'vana15_2')
vana15_3 = load_data(vana_run_numbers[2::5], 50, 'vana15_3')
vana15_4 = load_data(vana_run_numbers[3::5], 50, 'vana15_4')
vana15_5 = load_data(vana_run_numbers[4::5], 50, 'vana15_5')

vana09_1 = load_data(vana2_run_numbers[::5], 500, 'vana09_1')
vana09_2 = load_data(vana2_run_numbers[1::5], 500, 'vana09_2')
vana09_3 = load_data(vana2_run_numbers[2::5], 500, 'vana09_3')
vana09_4 = load_data(vana2_run_numbers[3::5], 500, 'vana09_4')
vana09_5 = load_data(vana2_run_numbers[4::5], 500, 'vana09_5')

vana06_1 = load_data(vana3_run_numbers[::5], 230, 'vana06_1')
vana06_2 = load_data(vana3_run_numbers[1::5], 230, 'vana06_2')
vana06_3 = load_data(vana3_run_numbers[2::5], 230, 'vana06_3')
vana06_4 = load_data(vana3_run_numbers[3::5], 230, 'vana06_4')
vana06_5 = load_data(vana3_run_numbers[4::5], 230, 'vana06_5')

vana15_list = [vana15_1, vana15_2, vana15_3, vana15_4, vana15_5]
vana09_list = [vana09_1, vana09_2, vana09_3, vana09_4, vana09_5]
vana06_list = [vana06_1, vana06_2, vana06_3, vana06_4, vana06_5]

# load and merge sample data
vana15_group = GroupWorkspaces(vana15_list)
vana09_group = GroupWorkspaces(vana09_list)
vana06_group = GroupWorkspaces(vana06_list)

# notmalize 
vana15_norm = MonitorEfficiencyCorUser(vana15_group)
vana09_norm = MonitorEfficiencyCorUser(vana09_group)
vana06_norm = MonitorEfficiencyCorUser(vana06_group)

# correct TOF
epptable15 = FindEPP(vana15_norm)
vana15_corr = CorrectTOF(vana15_norm, epptable15)

epptable09= FindEPP(vana09_norm)
vana09_corr = CorrectTOF(vana09_norm, epptable09)

epptable06= FindEPP(vana06_norm)
vana06_corr = CorrectTOF(vana06_norm, epptable06)

# get Ei
# Ei = 2.52   #meV
Ei = vana15_1.getRun().getLogData('Ei').value

# get S(q,w)
vana15_dE = ConvertUnits(vana15_corr, Target='DeltaE', EMode='Direct', EFixed=Ei)
ConvertToDistribution(vana15_dE)
vana15_dE_S = CorrectKiKf(vana15_dE)

vana09_dE = ConvertUnits(vana09_corr, Target='DeltaE', EMode='Direct', EFixed=Ei)
ConvertToDistribution(vana09_dE)
vana09_dE_S = CorrectKiKf(vana09_dE)

vana06_dE = ConvertUnits(vana06_corr, Target='DeltaE', EMode='Direct', EFixed=Ei)
ConvertToDistribution(vana06_dE)
vana06_dE_S = CorrectKiKf(vana06_dE)
# merge to MD
# get min and max values
minvals, maxvals = ConvertToMDMinMaxGlobal(vana15_dE_S[0], '|Q|', 'Direct')
gvana15_mde = ConvertToMD(vana15_dE_S, QDimensions='|Q|', dEAnalysisMode='Direct', PreprocDetectorsWS='-', MinValues=minvals, MaxValues=maxvals)

gvana09_mde = ConvertToMD(vana09_dE_S, QDimensions='|Q|', dEAnalysisMode='Direct', PreprocDetectorsWS='-', MinValues=minvals, MaxValues=maxvals)
gvana06_mde = ConvertToMD(vana06_dE_S, QDimensions='|Q|', dEAnalysisMode='Direct', PreprocDetectorsWS='-', MinValues=minvals, MaxValues=maxvals)

# merge all detector positions together
vana15_mde = MergeMD(gvana15_mde)
vana09_mde = MergeMD(gvana09_mde)
vana06_mde = MergeMD(gvana06_mde)

qmin = 0.1
qmax = 2.1
qstep = 0.02
qbins = int((qmax - qmin)/qstep)
qmax = qmin + qbins*qstep
ad0='|Q|,'+str(qmin)+','+str(qmax)+','+str(qbins)
ymin = -1.0
ymax = 1.0
ystep = 0.01
ybins = int((ymax - ymin)/ystep)
ymax = ymin + ybins*ystep
print(ymax)
ad1='DeltaE,'+str(ymin)+','+str(ymax)+','+str(ybins)
vana15_sqw = BinMD(InputWorkspace=vana15_mde, AlignedDim0=ad0, AlignedDim1=ad1)
vana09_sqw = BinMD(InputWorkspace=vana09_mde, AlignedDim0=ad0, AlignedDim1=ad1)
vana06_sqw = BinMD(InputWorkspace=vana06_mde, AlignedDim0=ad0, AlignedDim1=ad1)

v15 = ConvertMDHistoToMatrixWorkspace(vana15_sqw)
v15_t = Transpose(v15)
v15_sum = SumSpectra(v15_t)

v09 = ConvertMDHistoToMatrixWorkspace(vana09_sqw)
v09_t = Transpose(v09)
v09_sum = SumSpectra(v09_t)

v06 = ConvertMDHistoToMatrixWorkspace(vana06_sqw)
v06_t = Transpose(v06)
v06_sum = SumSpectra(v06_t)