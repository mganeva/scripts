dnsws = Load(Filename='/backup/build/jcns-mantid/datafiles/dns/test_event')
AddSampleLog(Workspace=dnsws,LogName='Ei',LogText='3.0',LogType='Number')
SetUB(Workspace=dnsws,a='1.4165',b='1.4165',c='1.4165',u=[1,0,0],v=[0,1,0])
AddSampleLog(Workspace=dnsws,LogName='Psi',LogText='0.0', LogType='Number Series')
SetGoniometer(Workspace=dnsws, Axis0='Psi,0,1,0,1')
dnsmdws = ConvertToMD(InputWorkspace=dnsws,QDimensions='Q3D',QConversionScales='HKL', dEAnalysisMode='Direct',MinValues=[-3,-3,-3,-1],MaxValues=[3,3,3,3])
plotSlice(dnsmdws, xydim=["[H,0,0]","[0,K,0]"], slicepoint=[0,0], colorscalelog=True )