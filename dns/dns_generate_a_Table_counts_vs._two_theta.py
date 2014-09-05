import math

#Load workspace into Mantid
ws = LoadEventNexus ("/home/kilian92/datafiles/dns/test_event.nxs")

#Set data to generate a table counts vs twoTheta
samplePos = ws.getInstrument().getSample().getPos()
beamDirection = V3D(0,0,1)
m = ws.getNumberHistograms()

#Generate the table
t = newTable("CountsVsTwoTheta", m, 2)

#Filling up table with values
for i in range(m):
   d = ws.getDetector(i)
   if not d.isMonitor():
	   #get value for counts
	   y = ws.readY(i)
	   counts = sum(y)
	   #get value for twoTheta
	   twoTheta = d.getTwoTheta(samplePos, beamDirection)*180/math.pi
	   #write value into table
	   t.setCell(1, i+1, twoTheta)
	   t.setCell(2, i+1, counts)
	   
#Now you can plot the data from the table

