"""  Newton Raphson Power Flow Solution
Author: Luis Cupul
Date: 06/09/2021
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os



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
        Ybus = np.zeros((self.nbus,self.nbus), dtype= complex)        
        
        for i in range(self.nline): #Off diagonal elements
            if a[i] != 0: #with transformation ratio
                Ybus[ssend[i]-1, eend[i]-1] +=  -y[i]/a[i]
                Ybus[eend[i]-1, ssend[i]-1] = Ybus[ssend[i]-1, eend[i]-1]
            else:
                Ybus[ssend[i]-1, eend[i]-1] += -y[i]
                Ybus[eend[i]-1, ssend[i]-1] = Ybus[ssend[i]-1, eend[i]-1]                                    
                
        for j in range(self.nbus):     # Add shunt admitances to diagonal elements of Ybus       
            Ybus[j,j] += y_bus[j]
            
            for k in range(self.nline):
                if ssend[k] == j+1 or eend[k] == j+1:
                    if a[j] != 0 and a[j] != 1:
                        if ssend[k] == j+1:
                            Ybus[j,j] +=  y[k]/a[k] + b[k]/2 \
                                + (1/a[k])*(1/a[k]-1)*y[k]
                        elif eend[k] == j+1:
                            Ybus[j,j] += y[k]/a[k] + b[k]/2 \
                                + (1-1/a[k])*y[k]                                
                    else:
                        Ybus[j,j] += y[k]/a[k] + b[k]/2
        return(Ybus)
        

        
        
        
        
    
if __name__ == '__main__':
    stag_sys =PowerFlow('datastag.xlsx')
    stag_sys.get_database()
    stag_sys.compute_ybus()

        
    
    
    
    


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
    
