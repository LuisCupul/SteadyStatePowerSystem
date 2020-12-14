# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:19:51 2020

@author: Luis Cupul Sanchez
"""

# Ybus

import scipy.io
import numpy as np

folder = 'Database'
data = 'datastag.mat'

# ---------------------- Read Database ----------------
mat = scipy.io.loadmat(folder +"/" + data)
bus = mat["bus"]
line = mat["line"]

# ---------------------- Parameters ------------------

n = len(bus) #numberof nodes
m = len(line) # number of lines
start = line[:,0]
start = start.astype(int)
end = line[:,1]
end = end.astype(int)
z = line[:,2] + line[:,3]*1j #line impedances
y = bus[:,7] + bus[:,8]*1j #shunt admitances
b = line[:,4] #shunt capacitive susceptances
a = line[:,5] # Turn relationship
y_line = 1/z
Y = np.zeros((n,n), dtype = complex)

for k in range(m): #off diagonal elements
    #print(k)
    if start[k] > 0 and end[k]>0:    
        if a[k] != 0:
            Y[start[k]-1,end[k]-1] = Y[start[k]-1,end[k]-1] - y_line[k]/a[k]
            Y[end[k]-1,start[k]-1] = Y[start[k]-1,end[k]-1]
        else:
            Y[start[k]-1,end[k]-1] = Y[start[k]-1,end[k]-1] - y_line[k]
            Y[end[k]-1,start[k]-1] = Y[start[k]-1,end[k]-1]
# -------- diagonal elements

for k in range(n):
    Y[k,k] = Y[k,k] +y[k]
    #print(k)
    for i in range(m):
        if start[i] == (k + 1) or end[i] == (k + 1):
            if start[i] == (k+1) and a[i] != 0:
                Y[k,k] = Y[k,k] + y_line[i]/a[i] + (b[i]/2)*1j + (1/a[i])*(1/a[i]-1)*y_line[i]
            elif end[i] == (k+1) and a[i] != 0:
                Y[k,k] = Y[k,k] + y_line[i]/a[i] + (b[i]/2)*1j + (1-1/a[i])*y_line[i]
            else:
                Y[k,k] = Y[k,k] + y_line[i] + (b[i]/2)*1j

print(Y)
# -------------- save data matlab ----------------
scipy.io.savemat(folder + '/Ybus_' + data, {'Ybus': Y})

