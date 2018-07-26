import numpy as np
from numpy import sin, cos, linalg
from scipy.constants import m_n, h, physical_constants, hbar
J2meV = 1000 * physical_constants['joule-electron volt relationship'][0]
fname = '/datadisk/build/jcns-mantid/dnstof.d_dat'
a=3.55
b=3.55
c=24.778
alpha=90
beta=90
gamma=120 
wavelength=4.2
#twotheta=22.53 #this is two twotheta from dnsplot should be detectornumber*5-det_rota
omega=129.99 + 7.50  # this is omega raw, from dnsplot = Huber - det_rot
h1=[1,1,0] #this is u from dnsplot
h2=[0,0,1] #this is v from dnsplot # but can also accept vector not perpendicular to h1 ## but they cannot be used for plotting then
w1=-43.0 # this is omegaoffset from dnsplot


def dns_inelastic_angle_to_hkl(twotheta, omega, a, b, c,alpha,beta,gamma,h1,h2,w1,wavelength,deltaE):
    #deltaE in meV was not sure which units you prefer in Mantid
    #wavelength in Angstroem
    #twotheta is not 2*theta here!
    # following M. D. Lumsden, J. L. Robertson & M. Yethiraj (2005). UB matrix implementation for inelastic neutron scattering experiments - J. Appl. Cryst. 38, 405-411.
    deltaE=deltaE/J2meV # converts meV to Joule
    twotheta=np.radians(twotheta)
    omega=np.radians(omega) 
    myorientedlattice=OrientedLattice(a,b,c,alpha,beta,gamma) #this defines B matrix
    myorientedlattice.setUFromVectors(h1,h2) # this considers h1 to be at w1=0, we will correct for that later
    w1=np.radians(w1)
    UB=myorientedlattice.getUB()
    R=np.matrix([[cos(w1),0, -sin(w1)], [0, 1 ,0],[sin(w1), 0, cos(w1)]]) # this corrects for omega offset by rotating the U matrix arround y by -w1, 
    UB=np.dot(R,UB)
    myorientedlattice.setUB(UB) 
    UBinv=linalg.inv(UB)  
    ki=np.pi*2/wavelength # incoming wavevector
    kf=np.sqrt(ki**2-deltaE*2.0*m_n/hbar**2*10**-20) #outgoing wavevector # = ki for elastic  ## factor 10**-20 is for converting 1/m^2 to 1/Angstroem^2
    theta=np.arctan((ki-kf*cos(twotheta))/(kf*sin(twotheta))) # 90°- angle of Q to ki # =twotheta/2 for elastic
    omega=omega-theta
    uphi= np.array([-cos(omega),0,-sin(omega)]) # oriented vector of measured reflection in instrument system following Mantid axis definition
    qabs=(ki**2+kf**2-2*ki*kf*cos(twotheta))**0.5 / 2.0 / np.pi # length of Q in inelastic case dived by 2pi #= 2*sin(theta)/wavelength for elastic
    hphi=  qabs*uphi
    hkl=np.dot(UBinv,hphi)   # calculate hkl from orientation in instrument system
    return hkl

v1 = h/(m_n*4.2*1.0e-10)
Ei = J2meV*0.5*m_n*v1*v1

tof = 40.1*np.arange(18,100) + 0.5*40.1
DeltaE = Ei - J2meV*0.5*m_n*(0.85*1.0e+06/tof)**2


for dE in DeltaE:
    data = dns_inelastic_angle_to_hkl(27.5,omega,a,b,c,alpha,beta,gamma,h1,h2,w1,wavelength, deltaE=dE)
    print "0, 0, 0, 4, {0}f, {1}f, {2}f, {3}f,".format(data[0,0],data[0,1],data[0,2], dE)