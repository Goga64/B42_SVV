import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from thrust_og import Thrust
from objects.parameters import universal_const

'''
This file calculates the thrust for stationary measurements using Thrust from thrust.py. It takes the following inputs:
    1. T_st  -->  static (outside) temperature, from which dT (difference in temperature) is calculated for Thrust.compute  [K]
    2. mfl   -->  fuel flow (left engine)   [kg/s]
    3. mfr   -->  fuel flow (right engine)  [kg/s]
    4. hp    -->  pressure altitude         [m]
    5. M     -->  Mach number               [-]
'''

def calc_thrust(T_st, mfl, mfr, hp, M):
    # First, calculate the temperature difference dT for the engines (T_outside - T_ISA)
    T_ISA = np.zeros_like(T_st)
    for j in range(len(T_ISA)):
        T_ISA[j] = universal_const.Temp0 + universal_const.lam*hp[j]                        # Get the ISA temperature for each altitude point
    
    dT = T_st - T_ISA

    # Calculate thrust for left and right engine, as well as the total thrust
    Thr_left_engine = np.ones_like(T_ISA)
    Thr_right_engine = np.ones_like(T_ISA)
    Thr_total = np.ones_like(T_ISA)


    for k in range(len(T_ISA)):
        Thr_left_engine[k] = Thrust.compute(hp[k], M[k], dT[k], mfl[k])                     # Compute left engine thrust
        Thr_right_engine[k] = Thrust.compute(hp[k], M[k], dT[k], mfr[k])                    # Compute right engine thrust
        Thr_total[k] = Thr_left_engine[k] + Thr_right_engine[k]                             # Compute total thrust
    
    return Thr_total
