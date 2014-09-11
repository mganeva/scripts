import math
import time
import numpy


def create_a_table_couts_vs_two_theta_vs_tof():
		
		#Load NeXus file
		ws = LoadEventNexus("/home/kilian92/datafiles/dns/test1_event.nxs")
		
		#Set data to extract the angles
		samplePos = ws.getInstrument().getSample().getPos()
		beamDirection = V3D(0,0,1)
		m = ws.getNumberHistograms()
		#m=1000
		twoTheta0 = ws.getSampleDetails().getLogData("s2").value
	
		#Generate the desired array and table
		eventsArr = []
		
		twoTheta_tof_countsArr = CreateEmptyTableWorkspace()
		twoTheta_tof_countsArr.addColumn("double", "two_theta")
		twoTheta_tof_countsArr.addColumn("double", "tof")
		twoTheta_tof_countsArr.addColumn("double", "counts")
	
		#Filling up the arrays with the desired values
		for i in range(m):
			d = ws.getDetector(i)
			if not d.isMonitor():
				twoTheta =  (d.getTwoTheta(samplePos, beamDirection)*180/math.pi) + float(twoTheta0)
				tof = ws.getEventList(i).getTofs().tolist()
				for j in range(len(tof)): 
					event = [twoTheta, tof[j]]
					#print event 
					eventsArr.append(event)
		
		while eventsArr != []:
			counts = eventsArr.count(eventsArr[0])
			twoTheta_tof_count =  [eventsArr[0][0], eventsArr[0][1] ,counts]
			print twoTheta_tof_count 
			event = eventsArr[0]
			while event in eventsArr:
				eventsArr.remove(event)
			twoTheta_tof_countsArr.addRow(twoTheta_tof_count)
		
		
		ws.delete()
		
		
create_a_table_couts_vs_two_theta_vs_tof()