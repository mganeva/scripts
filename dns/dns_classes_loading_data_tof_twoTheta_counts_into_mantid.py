import math
import time
import numpy

class input_workspace:
	
	"""Holds the path to an Inputfile to create coressponding workspace and manages actions to do on one 
		inputfile."""
	
	def __init__(self, path_to_input_workspace):
		self.data_location =  path_to_input_workspace
	
	def create_a_Arr_counts_vs_two_theta(self):
	
		"""Creates one Array with the counts summend over time and one array with the angles."""
		
		#Load NeXus file
		ws = LoadEventNexus(self.data_location)
		#h = mantid.getMatrixWorkspace("ws")
		
		#Set data to extract the angles and counts
		samplePos = ws.getInstrument().getSample().getPos()
		beamDirection = V3D(0,0,1)
		m = ws.getNumberHistograms()
		twoTheta0 = ws.getSampleDetails().getLogData("s2").value
	
		#Generate the desired arrays
		countsArr = []
		twoThetaArr = []
	
		#Filling up the arrays with the desired values
		for i in range(m):
			d = ws.getDetector(i)
			if not d.isMonitor():
				#get value for counts
				y = ws.readY(i)
				counts = sum(y)
				#get value for twoTheta
				twoTheta = (d.getTwoTheta(samplePos, beamDirection)*180/math.pi) + float(twoTheta0)
				#twoTheta = ws.getSampleDetails().getLogData("s2").value
				#write value into array
				countsArr.append(counts)
				twoThetaArr.append(twoTheta)
		
		#delete workspace
		print twoThetaArr
		ws.delete()
		return [twoThetaArr, countsArr]

		
	def create_a_Arr_two_theta_vs_tof(self):
		
		"""Extract data to create a workspace counts vs tof vs two theta"""
		
		#Load NeXus file
		ws = LoadEventNexus(self.data_location)
		
		#Set data to extract the angles
		samplePos = ws.getInstrument().getSample().getPos()
		beamDirection = V3D(0,0,1)
		#choose a smaller number for m other wise the execution of create_a_table_couts_vs_two_theta_vs_tof()
		#will take lots of time (see econd loop in create_a_table_couts_vs_two_theta_vs_tof)
		#m = ws.getNumberHistograms()
		m=1000
		twoTheta0 = ws.getSampleDetails().getLogData("s2").value
	
		#Generate the desired array and table
		eventsArr = []
	
		#Filling up the arrays with the desired values
		for i in range(m):
			d = ws.getDetector(i)
			if not d.isMonitor():
				twoTheta =  (d.getTwoTheta(samplePos, beamDirection)*180/math.pi) + float(twoTheta0)
				tof = ws.getEventList(i).getTofs().tolist()
				for j in range(len(tof)): 
					event = [twoTheta, tof[j]] 
					eventsArr.append(event)
		
		ws.delete()
		
		return eventsArr

class input:
	
	"""Holds array of input workspaces we want to analyse and manges the actions to do one a set of
	inputfiles."""
	
	def __init__(self, paths_to_input_workspaces):
		self.input_workspaces = []
		for i in range(len(paths_to_input_workspaces)):
			self.input_workspaces.append(input_workspace(paths_to_input_workspaces[i]))
		
	def create_a_merged_workspace_counts_vs_two_theta(self):
		
		"""Here we create the ws counts vs two theta, group them and further we make 
			a merged ws"""
		
		#Create the first ws 
		ws0_data = self.input_workspaces[0].create_a_Arr_counts_vs_two_theta()
		counts_vs_two_theta0 = CreateWorkspace(ws0_data[0], ws0_data[1])
		counts_vs_two_theta = GroupWorkspaces(InputWorkspaces="counts_vs_two_theta0") 
		countsArr = ws0_data[1]
		twoThetaArr =ws0_data[0]
		
		
		#Create further ws group them and get the merged ws
		for i in range(1, len(self.input_workspaces)): 
			ws_data = self.input_workspaces[i].create_a_Arr_counts_vs_two_theta()
			
			for j in range(len(ws_data[i-1])): 
				countsArr.append(ws_data[1][j]) 
				twoThetaArr.append(ws_data[0][j])
			
			wsname='counts_vs_two_theta%i'%i
			print "wsname=", wsname
			ws = CreateWorkspace(ws_data[0], ws_data[1] , WorkspaceTitle=wsname)
			vars()[wsname] = RenameWorkspace(ws, OutputWorkspace=wsname)
			counts_vs_two_theta = GroupWorkspaces(InputWorkspaces= "counts_vs_two_theta, counts_vs_two_theta%i"%i)
			#counts_vs_two_theta_merged = MergeRuns(InputWorkspaces="counts_vs_two_theta, " +  "counts_vs_two_theta%i"%i)
		
		#add the merged ws to the group
		counts_vs_two_theta_merged = CreateWorkspace(twoThetaArr, countsArr)
		counts_vs_two_theta = GroupWorkspaces(InputWorkspaces= "counts_vs_two_theta, counts_vs_two_theta_merged")
		
	def create_a_table_couts_vs_two_theta_vs_tof(self):
		
		"""Creats a table workspace counts vs tof vs two theta out of the input data"""
		
		#Generate the desired array and table
		eventsArr = []
		twoTheta_tof_countsArr = CreateEmptyTableWorkspace()
		twoTheta_tof_countsArr.addColumn("double", "two_theta")
		twoTheta_tof_countsArr.addColumn("double", "tof")
		twoTheta_tof_countsArr.addColumn("double", "counts")
		
		#Filling up the arrays with the desired values
		for i in range(len(self.input_workspaces)):
			eventArr = self.input_workspaces[i].create_a_Arr_two_theta_vs_tof()
			for j in range(len(eventArr)): eventsArr.append(eventArr[j])
		
		#Counting events and write data into table workspace
		#This takes a lot of time 
		while eventsArr != []:
			
			#count envent
			counts = eventsArr.count(eventsArr[0])
			twoTheta_tof_count =  [eventsArr[0][0], eventsArr[0][1] ,counts] 
			twoTheta_tof_countsArr.addRow(twoTheta_tof_count)
			
			#delete event from eventsArr
			event = eventsArr[0]
			while event in eventsArr: eventsArr.remove(event)
			
		

#input_ws = input(["/home/kilian92/datafiles/dns/test1_event.nxs", "/home/kilian92/datafiles/dns/test2_event.nxs", "/home/kilian92/datafiles/dns/test3_event.nxs"])
#input_ws.create_a_merged_workspace_counts_vs_two_theta()
input = input(["/home/kilian92/datafiles/dns/test1_event.nxs", "/home/kilian92/datafiles/dns/test2_event.nxs", "/home/kilian92/datafiles/dns/test3_event.nxs"])
input.create_a_table_couts_vs_two_theta_vs_tof()
			