#first attemt at controlling the EBSD data file, will start by looking to manipulate only columns 11 to 16 so as to now work with too large a system file.

#requires a bit of cleaning up and re-numbering

#now will import math and numpy modules to allow for manipulaion of the matrices

from math import *
import numpy

#first open the datafile
f = open('test_data.txt', 'r')
x = f.readlines() #reads all the lines on a one by one basis into the python interface. This then allows for the manipulation of these lines.

num_lines = sum(1 for line in open('test_data.txt')) #should count the number of lines in the system
# print('The number of lines in the system is: ' + str(num_lines)) #can be uncommented so that a validation line of line numbering comes up

# define range limits, this controls how many of the lines of the file are used.

low = 10 #starts at 10 due to the first 10 lines being text that we do not want to play with
high =num_lines #num_lines should allow for all the lines within the output file to be considered

# y is the changing output variable. This is required so that then it becomes possible to callout variables on a line by line basis.
y={}  #curly brackets allows for the later manipulation of the system
for i in range(low, high): # i refers to the number of the row that we are working on.
      y[str(i-9)] = x[i].split() #i - 9 is used to normalise the y output numbers. The created arrays can be called as y['vi'][x], [x] is an optional argument that allows a specific index in the array to be called.


#let us define the final output as name as 'grain'
# this creates a new variable 'grain' which contains: [grain number, phi1, PHI, phi2]. Should allow for much easier matrix multiplication

grain={}
for i in range(low, high): #sticking to same range as the previous function to allow for easier visibility
    grain[str(i-9)] = [y[str(i-9)][8], y[str(i-9)][0], y[str(i-9)][1], y[str(i-9)][2]]

#attemt to seed the matrixes using the data that is extracted from within the text file one loop step at a time. Will be inputting grain values

Gmatrix={}
for i in range(low, high):
    phi1=float(grain[str(i-9)][1])
    PHI=float(grain[str(i-9)][2])
    phi2=float(grain[str(i-9)][3])
    rot1 = numpy.matrix([[cos(phi1), sin(phi1), 0], [-sin(phi1), cos(phi1), 0], [0, 0, 1]])
    rot2 = numpy.matrix([[1, 0, 0], [0, cos(PHI), sin(PHI)], [0, -sin(PHI), cos(PHI)]])
    rot3 = numpy.matrix([[cos(phi2), sin(phi2), 0], [-sin(phi2), cos(phi2), 0], [0, 0, 1]])
    Gmatrix[str(i-9)] = rot3 * rot2 * rot1
#     print ('G matrix ' + str(i-9) +' is:')
#     print (Gmatrix[str(i-9)])

# print (Gmatrix[str(15)]) #important to not forget to convert the values into string.



# SELF TESTS

#useful pair of lines to view all local variables within the system. BOTH MUST BE UNCOMMENTED FOR THIS TO WORK
# import pprint
# pprint.pprint(locals())

