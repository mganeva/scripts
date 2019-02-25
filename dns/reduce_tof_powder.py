import os

datapath = "/datadisk/data/dns/2019/p15778/data"
fname = "p157780000{}_3p5K_15krpm.d_dat"
wavelength=5.7

sample_run_numbers = range(677620,677635)

def load_data(run_numbers, echannel, prefix):
    wslist = []
    for rn in run_numbers:
        infile = fname.format(rn)
        wsname = os.path.splitext(infile)[0]
        LoadDNSLegacy(os.path.join(datapath, infile), Normalization='no', ElasticChannel=echannel, Wavelength=wavelength, OutputWorkspace=wsname)
        wslist.append(wsname)
        
    ws = MergeRuns(wslist, SampleLogsSum='mon_sum,duration', OutputWorkspace=prefix)
    return ws
   
 # this will work only for 5 detector positions numbered consequently
 # otherwise particular list of run numbers to merge has to be specified
data_1 = load_data(sample_run_numbers[::5], 50, 'data_1')            # 1st detector position
data_2 = load_data(sample_run_numbers[1::5], 50, 'data_2')          # 2nd detector position
data_3 = load_data(sample_run_numbers[2::5], 50, 'data_3')          # 3rd detector position
data_4 = load_data(sample_run_numbers[3::5], 50, 'data_4')          # 4th detector position
data_5 = load_data(sample_run_numbers[4::5], 50, 'data_5')          # 5th detector position

data_list = [data_1, data_2, data_3, data_4, data_5]

# load and merge sample data
data_group = GroupWorkspaces(data_list)

# notmalize by monitor counts
data_norm = MonitorEfficiencyCorUser(data_group)

# correct TOF
epptable = FindEPP(data_norm)
data_corr = CorrectTOF(data_norm, epptable)

# get Ei
Ei = data_1.getRun().getLogData('Ei').value

# get S(q,w)
data_dE = ConvertUnits(data_corr, Target='DeltaE', EMode='Direct', EFixed=Ei)
ConvertToDistribution(data_dE)
data_dE_S = CorrectKiKf(data_dE)

# convert to MD
# get min and max values
minvals, maxvals = ConvertToMDMinMaxGlobal(data_dE_S[0], '|Q|', 'Direct')
gdata_mde = ConvertToMD(data_dE_S, QDimensions='|Q|', dEAnalysisMode='Direct', PreprocDetectorsWS='-', MinValues=minvals, MaxValues=maxvals)

# merge all detector positions together
data_mde = MergeMD(gdata_mde)

qmin = 0.1
qmax = 2.1
qstep = 0.02
qbins = int((qmax - qmin)/qstep)
qmax = qmin + qbins*qstep
ad0='|Q|,{qmin},{qmax},{qbins}'.format(qmin=qmin,qmax=qmax,qbins=qbins)   

ymin = -1.0
ymax = 2.0
ystep = 0.01
ybins = int((ymax - ymin)/ystep)
ymax = ymin + ybins*ystep
ad1='DeltaE,{ymin},{ymax},{ybins}'.format(ymin=ymin,ymax=ymax,ybins=ybins) 

# final result
data_sqw = BinMD(InputWorkspace=data_mde, AlignedDim0=ad0, AlignedDim1=ad1)