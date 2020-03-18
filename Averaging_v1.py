# this is a first attemt at writing a script that defines a function on how to average a quaternian that is in an array form

# I believe that having the quaternians in an array defined as (qr, qi, qj, qk) is easiest, progressing on to (gn, qr, qi, qj, qk) to include the grain number within the system

from math import *
import numpy #key for any kind of matrix work. MUST BE ON A MATHEMATICAL PYTHON DISTRIBUTION SUCH AS ANACONDA

# let us define some random quaternians so that this function can be tested:

q1 = [2, 2, 2, 2]
q2 = [1.0, 1, 1, 1]

# print(q1[1]+q2[1])
# print(q2)


def qsum(x, y): # this will create a functin that can then be later recalled to sum quaternians in form [qr, qi, qj, qk]
    return [(x[0]+y[0]), (x[1]+y[1]), (x[2]+y[2]), (x[3]+y[3])]

q3=qsum(q1, q2)

# print (q3)

# remember that the average of a quaternian is the sum of quaternians devided by the norm of the sum. As such define a norm function:

def qnorm(x):
    return (x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2)**(1/2)

q4 = qnorm(q1)

# print(q4)

def qavg(x,y):
    s=qsum(x,y)
    a=[s[0]/qnorm(s), s[1]/qnorm(s), s[2]/qnorm(s), s[3]/qnorm(s)]
    return a
    
q5=qavg(q1,q2)

print (q5)