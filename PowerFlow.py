"""  Newton Raphson Power Flow Solution
Author: Luis Cupul
Date: 06/09/2021
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class PowerFlow:
    """ Class description  
    database, call the xlsx file that store database system,         
    """


    def __init__(self, database):
        self._database = 'C:\\Users\\Luis\\Documents\\Python Scripts\\SteadyStatePowerSystem\\Database\\' +database  # Current directory + database
                        
    
    def get_database(self):
        self._bus = pd.read_excel(self._database, 'bus', header= None).to_numpy()
        self._line = pd.read_excel(self._database, 'line', header= None).to_numpy()
    
    def compute_ybus(self):
        self.nbus, self.nline = len(self._bus), len(self._line)
        z = self._line[:,2] +self._line[:,3]*1j #impedance line, R+jX
        y, y_bus = 1/z, self._bus[:,7] + self._bus[:,8]*1j # Admitance line, bus
        a, b = self._line[:,5 ], self._line[:,4]*1j # turns ratio, capacitive susceptance
        ssend, eend = self._line[:,0].astype(int), self._line[:,1].astype(int)
        self.Ybus = np.zeros((self.nbus,self.nbus), dtype= complex)        
        
        for i in range(self.nline): #Off diagonal elements
            if a[i] != 0: #with transformation ratio
                self.Ybus[ssend[i]-1, eend[i]-1] +=  -y[i]/a[i]
                self.Ybus[eend[i]-1, ssend[i]-1] = self.Ybus[ssend[i]-1, eend[i]-1]
            else:
                self.Ybus[ssend[i]-1, eend[i]-1] += -y[i]
                self.Ybus[eend[i]-1, ssend[i]-1] = self.Ybus[ssend[i]-1, eend[i]-1]                                    
                
        for j in range(self.nbus):     # Add shunt admitances to diagonal elements of Ybus       
            self.Ybus[j,j] += y_bus[j]
            
            for k in range(self.nline):
                if ssend[k] == j+1 or eend[k] == j+1:
                    if a[j] != 0 and a[j] != 1:
                        if ssend[k] == j+1:
                            self.Ybus[j,j] +=  y[k]/a[k] + b[k]/2 \
                                + (1/a[k])*(1/a[k]-1)*y[k]
                        elif eend[k] == j+1:
                            self.Ybus[j,j] += y[k]/a[k] + b[k]/2 \
                                + (1-1/a[k])*y[k]                                
                    else:
                        self.Ybus[j,j] += y[k]/a[k] + b[k]/2
        return self.Ybus
        
    def compute_pq(self, v, ang):
        P, Q = np.zeros(self.nbus), np.zeros(self.nbus)
        dP, dQ = np.zeros(self.nbus), np.zeros(self.nbus)
        
        for i in range(self.nbus):
            P[i] = v[i]*sum(v*np.abs(self.Ybus[:,i])*np.cos(np.angle(self.Ybus[:,i])-ang[i]+ang))
            Q[i] = -v[i]*sum(v*np.abs(self.Ybus[:,i])*np.sin(np.angle(self.Ybus[:,i])-ang[i]+ang))
            
            if self._bus[i, 9] == 2:
                dP[i] = self._bus[i,3] - self._bus[i,5] - P[i]
            elif self._bus[i, 9] == 3:
                dP[i] = self._bus[i,3] - self._bus[i,5] - P[i]
                dQ[i] = self._bus[i,4] - self._bus[i,6] - Q[i]
        return P, Q, dP, dQ
    
    def jacobian(self, v, ang, P, Q):        
        """ comput Jacobian with the current voltajes and angles
        ------------ Input -----------------
        v: current voltaje
        ang: angle of nodes
        P: real power of nodes
        Q: reactive power at each nodes
        
        ------------ Output ----------------
        J: jacobian with dimensions (nbus + nload -1)x(nbus + nload -1)        
        """
        nload = np.count_nonzero(self._bus[:,9]==3)
        j1, j2 = np.zeros((self.nbus-1,self.nbus-1)), np.zeros((self.nbus-1, nload))
        j3, j4 = np.zeros((nload,self.nbus-1)), np.zeros((nload, nload))

        a,c = 0, 0
        e, g = 0, 0
        for i in range(self.nbus):
            if self._bus[i,9] != 1:
                b, d = 0, 0
                f, h = 0, 0
                for j in range(self.nbus):
                    if self._bus[j,9] != 1:                
                        if i == j: # diagonal element
                            j1[a,b] = -Q[i] -(v[i]**2)*np.imag(self.Ybus[i,i])                            
                        else:
                            j1[a,b] = -v[i]*v[j]*np.abs(self.Ybus[i,j])*np.sin(\
                                np.angle(self.Ybus[i,j])-ang[i]+ang[j])
                        b += 1
                                                    
                        if self._bus[i,9] == 3 and self._bus[j,9] == 3:
                            if i == j:
                                j4[c,d] = Q[i] - v[i]*np.imag(self.Ybus[i,i])
                            else:
                                j4[c,d] = -v[i]*np.abs(self.Ybus[i,j])*np.sin(\
                                    np.angle(self.Ybus[i,j])-ang[i]+ang[j])
                            d += 1                     
                    if self._bus[j, 9] == 3:
                        if i == j: # Diagonal elements
                            j2[e,f] = P[i] + (v[i]**2)*np.real(\
                                self.Ybus[i,i])
                        else:
                            j2[e,f] = v[i]*np.abs(self.Ybus[i,j])*np.cos(\
                                np.angle(self.Ybus[i,j])-ang[i]+ang[j])
                        f += 1
                        
                        
                    if self._bus[i,9] == 3 and self._bus[j,9] != 1:
                        if i == j:
                            j3[g,h] = P[i] -(v[i]**2)*np.real(self.Ybus[i,i])
                        else:
                            j3[g,h] = -v[i]*v[j]*np.abs(self.Ybus[i,j])*np.cos(\
                                np.angle(self.Ybus[i,j])-ang[i]+ang[j])
                        h += 1
                a += 1
                e += 1
                if self._bus[i,9] ==3: 
                    c += 1
                    g += 1        
        
        return np.block([[j1, j2],[j3, j4]])    
    
    
        
        
        
                            
                
        
                        

if __name__ == '__main__':
    stag_sys =PowerFlow('datastag.xlsx')
    stag_sys.get_database()
    stag_sys.compute_ybus()
    v = stag_sys._bus[:,1]
    ang = stag_sys._bus[:,2]
    
    P,Q, _,_ = stag_sys.compute_pq(v, ang)
    print(stag_sys.jacobian(v,ang,P,Q))
    
    

        
    
    
    
    


#PowerFlow Solution

"""  Power Flow class

--------------Fields ------------
_database()

------------Behaviors-----------
get_database() -- database
return - bus, line, initial_values (angle, V)

get_ybus -- bus, line
return Ybus

compute_power -Ybus, angle, V
Return P, Q , dP, dQ


compute_jacobian -- P, Q, angle,V
return J

compute_increments(angle,V) -- J, dP, dQ
return  dangle, dV


update() -- dangle, DV
return dV
 """



""" algorithm class (PowerFlow class)
--------------Fields ------------
_database()

init
------------Behaviors-----------

run_itetive algorith -- # of iterations, epsilon(tolerance)
return V,angle


compute powerflow -- V, angle, Ybus

return Power flow between lines

 """


""" 
if __name__ == '__main__':
    stag_sys =PowerFlow('datastag.xlsx')
    stag_sys.get_database()

 """
    
