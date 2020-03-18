# this script will look at using quaternian formation from the rotation matrix.
# as such an initial rotation matrix will be constructed from its respective parts
# 03/02/17 - THIS SEEMS TO BE RETURNING THE CORRECT REVERSAL OF THE ANGLES TO WITHIN  10**-16, SO NEGLIGIBLE. nEED TO SEE IF ANY WEIRD DESCREPENCIES WILL ARISE WITH LARGER NUMBERS

# import necessary packages
from math import *
import numpy

# define original euler angles, using intrinsic z-x-z convention. Rot about z, x', z'' by phi1, PHI, phi2 respectively (be careful not to use extrinsic conversion or tait-brian angles)

phi1=1
PHI=6
phi2=4

rot1 = numpy.matrix([[cos(phi1), sin(phi1), 0], [-sin(phi1), cos(phi1), 0], [0, 0, 1]])
rot2 = numpy.matrix([[1, 0, 0], [0, cos(PHI), sin(PHI)], [0, -sin(PHI), cos(PHI)]])
rot3 = numpy.matrix([[cos(phi2), sin(phi2), 0], [-sin(phi2), cos(phi2), 0], [0, 0, 1]])
G = rot3 * rot2 * rot1

#now to convert the rotation matrix into quaternians via matrix to quaternian from wiki
# do not forget that counting starts at 0,0 not 1,1!!!

# q convention follows as r for scalar, i, j, k for relevant directions

qr=0.5*(1+G[0,0]+G[1,1]+G[2,2])**(1/2)

qi=(1/(4*qr))*(G[2,1]-G[1,2])

qj=(1/(4*qr))*(G[0,2]-G[2,0])

qk=(1/(4*qr))*(G[1,0]-G[0,1])

#
# print('qr: ' +str(qr))
#
# print('qi: ' +str(qi))
#
# print('qj: ' +str(qj))
#
# print('qk: ' +str(qk))

# now try to compute the original angles back as rho1 etc.

# by considering A33 of rotation matrix vs quartinian matrix:

RHO = acos(1 - 2*(qi**2) -2*(qj**2))

if PHI >= pi:
   RHO = 2*pi - RHO
else:
   RHO = RHO

rho1 = asin((2*(qi*qk - qj*qr))/(sin(RHO)))

if phi1 > pi/2 and phi1 <= 3*pi/2 :
   rho1 = pi - rho1
elif phi1 > 3*pi/2:
     rho1 = rho1 + 2*pi
else:
     rho1=rho1

rho2 = asin((2*(qi*qk + qj*qr))/(sin(RHO)))

if phi2 > pi/2 and phi2 <= 3*pi/2 :
   rho2 = pi - rho2
elif phi2 > 3*pi/2:
     rho2 = rho2 + 2*pi
else:
     rho2=rho2

print('PHI: ' + str(PHI))
print('RHO: ' + str(RHO))

print('phi1: ' + str(phi1))
print('rho1: ' + str(rho1))

print('phi2: ' + str(phi2))
print('rho2: ' + str(rho2))
# sanity checks

# print('phi1 - rho1: ' + str(phi1 - rho1))
# 
# print('PHI - RHO: ' + str(PHI - RHO))
# 
# print('phi2 - rho2: ' + str(phi2 - rho2))
# 
# # checking if the rotation matrix that is reached is considered equivelant
# 
# rot4 = numpy.matrix([[cos(rho1), sin(rho1), 0], [-sin(rho1), cos(rho1), 0], [0, 0, 1]])
# rot5 = numpy.matrix([[1, 0, 0], [0, cos(RHO), sin(RHO)], [0, -sin(RHO), cos(RHO)]])
# rot6 = numpy.matrix([[cos(rho2), sin(rho2), 0], [-sin(rho2), cos(rho2), 0], [0, 0, 1]])
# R = rot6 * rot5 * rot4
# 
# print (G-R)
# print(R)



# for checking the rotation angle variables

# print('phi1: ' + str(phi1))
#
# print('PHI: ' + str(PHI))
#
# print('phi2: ' + str(phi2))
#
# print('rho1: ' + str(rho1))
#
# print('RHO: ' + str(RHO))
#
# print('rho2: ' + str(rho2))


# variable check of all variables within the system
# import pprint
# pprint.pprint(locals())





























