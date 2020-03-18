from math import *
import numpy

qr =  1                     #float(GQ[str(i)][0])
qi =  0                     #float(GQ[str(i)][1])
qj =  0                     #float(GQ[str(i)][2])
qk =  0                     #float(GQ[str(i)][3])
GM11 = 1 - 2*(qj**2)-2*(qk**2)
GM12 = 2*(qi*qj -qk*qr)
GM13 = 2*(qi*qk + qj*qr)
GM21 = 2*(qi*qj + qk*qr)
GM22 = 1-2*(qi**2)-2*(qk**2)
GM23 = 2*(qj*qk - qi*qr)
GM31 = 2*(qi*qk -qj*qr)
GM32 = 2*(qi*qr + qj*qk)
GM33 = 1-2*(qi**2)-2*(qj**2)
GM = numpy.matrix([[GM11, GM12, GM13], [GM21, GM22, GM23], [GM31, GM32, GM33]])

print (GM)


