import math
import time
import numpy


def create_a_table_couts_vs_two_theta_vs_tof(path):
		
		#Load NeXus file
		ws = LoadEventNexus(path)
		
		#Set data to extract the angles
		samplePos = ws.getInstrument().getSample().getPos()
		beamDirection = V3D(0,0,1)
		#choose a smaller number for m other wise the execution 
		#will take lots of time (see second loop)
		#m = ws.getNumberHistograms()
		m=1000
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
					eventsArr.append(event)
		
		#Counting events and write data into table workspace
		while eventsArr != []:
			
			#count envent
			counts = eventsArr.count(eventsArr[0])
			twoTheta_tof_count =  [eventsArr[0][0], eventsArr[0][1] ,counts]
			twoTheta_tof_countsArr.addRow(twoTheta_tof_count)
			
			#delete event from eventsArr
			event = eventsArr[0]
			while event in eventsArr:
				eventsArr.remove(event)
			
		
		
		ws.delete()
		
		
create_a_table_couts_vs_two_theta_vs_tof("/home/kilian92/datafiles/dns/test1_event.nxs")