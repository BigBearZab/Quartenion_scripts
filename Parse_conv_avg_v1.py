# time to get this party started as a combination of the previouisly written scripts

# BASE PROGRAM LOGIC: Grain Eulers -> Quaternians -> Average -> Return to 1 set of Eulers per grain -> Create rotation matrix for the grain

from math import *
import numpy

#first open the datafile
# use second iteration for current testing, though input path is preferable
# filename = input('Enter EBSD file name for Euler angle averaging:')
# f = open(filename+'.txt', 'r')
# rl = f.readlines() #reads all the lines on a one by one basis into the python interface. This then allows for the manipulation of these lines.

f = open('test_data.txt', 'r')
rl = f.readlines() #reads all the lines on a one by one basis into the python interface. This then allows for the manipulation of these lines.

num_lines = sum(1 for line in open('test_data.txt')) #should count the number of lines in the system
# print('The number of lines in the system is: ' + str(num_lines)) #can be uncommented so that a validation line of line numbering comes up

# define range limits, this controls how many of the lines of the file are used.

low = 10 #starts at 10 due to the first 10 lines being text that we do not want to play with
high =num_lines #num_lines should allow for all the lines within the output file to be considered
l=low-9
h=high-9

# y is the changing output variable. This is required so that then it becomes possible to callout variables on a line by line basis.
ln={}  #curly brackets allows for the later manipulation of the system
for i in range(low, high): # i refers to the number of the row that we are working on.
      ln[str(i-9)] = rl[i].split() #i - 9 is used to normalise the y output numbers. The created arrays can be called as ln[x], [x] is an optional argument that allows a specific index in the array to be called.


#let us define the final output as name as 'grain'
# this creates a new variable 'grain' which contains: [grain number, phi1, PHI, phi2]. Should allow for much easier matrix multiplication

eulorig={} #original set of euler angles
for i in range(l, h): #sticking to same range as the previous function to allow for easier visibility
    eulorig[str(i)] = [ln[str(i)][8], ln[str(i)][0], ln[str(i)][1], ln[str(i)][2]]

# now that the variables are saved as a set of euler angles and a grain number we can re-convert this into [gn,q1,q2,q3,q4]

quart={}
Grot={}
for i in range(l, h):
    # we must first pull Euler angles, and then convert into a Gmatrix
    phi1=float(eulorig[str(i)][1])
    PHI=float(eulorig[str(i)][2])
    phi2=float(eulorig[str(i)][3])
    rot1 = numpy.matrix([[cos(phi1), sin(phi1), 0], [-sin(phi1), cos(phi1), 0], [0, 0, 1]])
    rot2 = numpy.matrix([[1, 0, 0], [0, cos(PHI), sin(PHI)], [0, -sin(PHI), cos(PHI)]])
    rot3 = numpy.matrix([[cos(phi2), sin(phi2), 0], [-sin(phi2), cos(phi2), 0], [0, 0, 1]])
    G = rot3 * rot2 * rot1
    Grot[str(i)] = G
    qr=0.5*(1+G[0,0]+G[1,1]+G[2,2])**(1/2)
    qi=(1/(4*qr))*(G[2,1]-G[1,2])
    qj=(1/(4*qr))*(G[0,2]-G[2,0])
    qk=(1/(4*qr))*(G[1,0]-G[0,1])
    quart[str(i)] = [qr, qi, qj, qk, eulorig[str(i)][0]]

# prints all created quaternians
for i in range(l, h):
    print ('Grot'+str(i)+' = ')
    print(Grot[str(i)])

# time to sum and then average the euler angles

# first defin qsum, qnorm and qavg
def qsum(x, y): # this will create a functin that can then be later recalled to sum quaternians in form [qr, qi, qj, qk]
    return [(x[0]+y[0]), (x[1]+y[1]), (x[2]+y[2]), (x[3]+y[3])]

def qnorm(x):
    return (x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2)**(1/2)

def qavg(s):
    return [s[0]/qnorm(s), s[1]/qnorm(s), s[2]/qnorm(s), s[3]/qnorm(s)]

# for i in range(l, h):
#     print ('norm'+str(i)+' = ')
#     print(qnorm(quart[str(i)]))


# the average function here uses a summed quaternian

i=1 #i is total number of lines to consider
c=1 #c is a counter
rt=[0,0,0,0] #running total used to sum quaternians, and then will be used to average the quaternian

#this loop iterates through all the created quaternions, and sums them , followed by averaging them and creating the new variable GQ (grain-quaternion)

GQ={} #the grain quaternian variable, later to be converted back into Eulers
while i <= h:
      if i == h:
           rt = qavg(rt)
           GQ[str(c)]=rt
#            print(rt)
#            print('That is the sum of quaternions for grain ' +str(c))
           i=i+1
      elif c == int(quart[str(i)][4]):
         rt=qsum(rt, quart[str(i)])
         i=i+1
      else:
           rt = qavg(rt)
           GQ[str(c)]=rt
#            print(rt)
#            print('That is the sum of quaternions for grain ' +str(c))
           rt=[0,0,0,0]
           c=c+1

# check to print all the averaged quaternians, and ensure all the wanted grains are being considered
# for i in range(l, int(quart[str(h-1)][4])+1):
#     print ('GQ'+str(i)+' = ')
#     print(GQ[str(i)])


# Rather than converting back, I will generate a rotation matrix in quaternian space to prevent inverse cosine error

GM={} #this will act as our variable for the Grain final averaged rotation matrix

for i in range(l, int(quart[str(h-1)][4])+1):
    qr = float(GQ[str(i)][0])
    qi = float(GQ[str(i)][1])
    qj = float(GQ[str(i)][2])
    qk = float(GQ[str(i)][3])
    GM[str(i)] = numpy.matrix([[1 - 2*(qj**2)-2*(qk**2), 2*(qi*qj -qk*qr), 2*(qi*qk + qj*qr)], [2*(qi*qj + qk*qr), 1-2*(qi**2)-2*(qk**2), 2*(qj*qk - qi*qr)], [2*(qi*qk -qj*qr), 2*(qi*qr + qj*qk), 1-2*(qi**2)-2*(qj**2)]])

for i in range(l, int(quart[str(h-1)][4])+1):
    print ('GM'+str(i)+' = ')
    print(GM[str(i)])

print(Grot[str(24)] - GM[str(7)])
# Time to convert back into Euler angles and finally get this saga over, then maybe add input and output text files and test it on the big daddy

# THIS WILL NEED TO BE LOOKED AT FOR THE DIRECTIONAL CONVERSION BACK TO EULER (ACOS OR ACOS2)
# rho is used instead of phi for ease of coding access

# GE={} #this will act as our variable for the Grain Euler final average angle
#
# for i in range(l, int(quart[str(h-1)][4])+1):
#     qr = GQ[str(i)][0]
#     qi = GQ[str(i)][1]
#     qj = GQ[str(i)][2]
#     qk = GQ[str(i)][3]
#     RHO = acos(1 - 2*(qi**2) -2*(qj**2))
#     rho1 = asin((2*(qi*qk - qj*qr))/(sin(RHO)))
#     rho2 = asin((2*(qi*qk + qj*qr))/(sin(RHO)))
#     GE[str(i)] = [rho1, RHO, rho2]
#
# for i in range(l, int(quart[str(h-1)][4])+1):
#     print ('GE'+str(i)+' = ')
#     print(GE[str(i)])


# struggles to work at full size as only allowed limited scroll back within the cmd, useful check for smaller file sizes
# import pprint
# pprint.pprint(locals())