#BASED ON THE PARSE AND CONVERSION CODE
#RE-ORDERING OF THE SYSTEM ALLOWS FOR THE ITERATIVE IF LOOPS TO WORK. THIS PROBABLY IS NOT THE PRETTIEST SOLUTION BUT WORKS WHEN ORDERED I THINK
#SOME NAME CHANGES REQUIRED TO FINISH OFF QUATERNIAN FORMING AND CONVERSION STEP
#DO NOT CONVERT BACK INTO EULER ANGLES SINCE THIS REQUIRES THE INPUT TO BE ALL WITHIN THE SAME FORM OF CLUSTER. THIS IS NOT TRUE WITH EBSD DATA AND SO NO RETURN CONVERSION ELIMINATES THIS ERROR
# DO NOT RUN WITH MAIN TEXT FILE AS IT IS HUGE!!!!
from math import *
import numpy as np

#first open the datafile
# use second iteration for current testing, though input path is preferable
# filename = input('Enter EBSD file name for Euler angle averaging:')
# f = open(filename+'.txt', 'r')
# rl = f.readlines() #reads all the lines on a one by one basis into the python interface. This then allows for the manipulation of these lines.
filename = 'test_data2.txt'
f = open(filename, 'r')
rl = f.readlines() #reads all the lines on a one by one basis into the python interface. This then allows for the manipulation of these lines.

num_lines = sum(1 for line in open(filename)) #should count the number of lines in the system
# print('The number of lines in the system is: ' + str(num_lines)) #can be uncommented so that a validation line of line numbering comes up

# define range limits, this controls how many of the lines of the file are used.

low = 10 #starts at 10 due to the first 10 lines being text that we do not want to play with
high =num_lines #num_lines should allow for all the lines within the output file to be considered
l=low-9
h= high-9
# print(high)
# print(h)
# y is the changing output variable. This is required so that then it becomes possible to callout variables on a line by line basis.
ln={}  #curly brackets allows for the later manipulation of the system
for i in range(low, high): # i refers to the number of the row that we are working on.
      ln[str(i-9)] = rl[i].split() #i - 9 is used to normalise the y output numbers. The created lists can be called as ln[x], [x] is an optional argument that allows a specific index in the array to be called.

#let us define the final output as name as 'grain'
# this creates a new variable 'grain' which contains: [grain number, phi1, PHI, phi2]. Should allow for much easier matrix multiplication

eulorig={} #original set of euler angles
for i in range(l, h): #sticking to same range as the previous function to allow for easier visibility
    eulorig[str(i)] = [int(ln[str(i)][8]), float(ln[str(i)][0]), float(ln[str(i)][1]), float(ln[str(i)][2])]


dsets = np.array(eulorig[str(l)])
lc = 2 #line counter
while lc < h:
    dsets = np.vstack([dsets,eulorig[str(lc)]])
    lc = lc + 1

# for i in range(l-1, h-1):
#     print(dsets[i])

dsets=dsets[np.argsort(dsets[:,0])]

# dsets becomes the variable that encapsulates the whole of the data set as an array


# some tinkering required with the remainder of the code. Should work when "eulorig" changed to "dsets"

quart={}

for i in range(l-1, h-1):
    # we must first pull Euler angles, and then convert into a Gmatrix
    phi1=float(dsets[i][1])
    PHI=float(dsets[i][2])
    phi2=float(dsets[i][3])
    rot1 = np.matrix([[cos(phi1), sin(phi1), 0], [-sin(phi1), cos(phi1), 0], [0, 0, 1]])
    rot2 = np.matrix([[1, 0, 0], [0, cos(PHI), sin(PHI)], [0, -sin(PHI), cos(PHI)]])
    rot3 = np.matrix([[cos(phi2), sin(phi2), 0], [-sin(phi2), cos(phi2), 0], [0, 0, 1]])
    G = rot3 * rot2 * rot1
    qr=0.5*(1+G[0,0]+G[1,1]+G[2,2])**(1/2)
    qi=(1/(4*qr))*(G[2,1]-G[1,2])
    qj=(1/(4*qr))*(G[0,2]-G[2,0])
    qk=(1/(4*qr))*(G[1,0]-G[0,1])
    quart[str(i+1)] = [qr, qi, qj, qk, dsets[(i)][0]]
# quaternion conversion now seems to be working for test_data 2 which is the larger file
# prints all created quaternians
# for i in range(300, 350):
#     print ('quart'+str(i)+' = ')
#     print(quart[str(i)])

# time to sum and then average the euler angles

# first defin qsum, qnorm and qavg
def qsum(x, y): # this will create a functin that can then be later recalled to sum quaternians in form [qr, qi, qj, qk]
    return [(x[0]+y[0]), (x[1]+y[1]), (x[2]+y[2]), (x[3]+y[3])]

def qnorm(x):
    return (x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2)**(1/2)

def qavg(s):
    return [s[0]/qnorm(s), s[1]/qnorm(s), s[2]/qnorm(s), s[3]/qnorm(s)]

# for i in range(l,h):      #this simply works as a warning now
#     if qnorm(quart[str(i)]) != 1:
#        print (i)



# averaging the quaternians using the newly defined functions
i=1 #i is total number of lines to consider
c=1 #c is a counter
rt=[0,0,0,0] #running total used to sum quaternians, and then will be used to average the quaternian

GQ={} #the grain quaternian variable, later to be converted back into Eulers
while i <= h:
      if i == h:
           rt = qavg(rt)
           rt.append(i-1) #appends a tracer
           GQ[str(c)]=rt
#            print(rt)
#            print('That is the sum of quaternions for grain ' +str(c))
           i=i+1
      elif c == int(quart[str(i)][4]):
         rt=qsum(rt, quart[str(i)])
         i=i+1
      else:
           rt = qavg(rt)
           rt.append(i-1) #appends a tracer
           GQ[str(c)]=rt
#            print(rt)
#            print('That is the sum of quaternions for grain ' +str(c))
           rt=[0,0,0,0]
           c=c+1

# check to print all the averaged quaternians, and ensure all the wanted grains are being considered
# for i in range(l, int(quart[str(h-1)][4])+1):
#     print ('GQ'+str(i)+' = ')
#     print(GQ[str(i)])

# produce Qmatrix from the averaged Quaternions
Qmatrix={}
for i in range(l, int(quart[str(h-1)][4])+1):
    qr = float(GQ[str(i)][0])
    qi = float(GQ[str(i)][1])
    qj = float(GQ[str(i)][2])
    qk = float(GQ[str(i)][3])
    Qmatrix[str(i)] = np.matrix([[1 - 2*(qj**2)-2*(qk**2), 2*(qi*qj -qk*qr), 2*(qi*qk + qj*qr)], [2*(qi*qj + qk*qr), 1-2*(qi**2)-2*(qk**2), 2*(qj*qk - qi*qr)], [2*(qi*qk -qj*qr), 2*(qi*qr + qj*qk), 1-2*(qi**2)-2*(qj**2)]])

for i in range(l, int(quart[str(h-1)][4])+1):
    print ('Qmatrix'+str(i)+' = ')
    print(Qmatrix[str(i)])
    print(np.linalg.det(Qmatrix[str(i)]))




#CODE END
