import sys, os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from objects.parameters import universal_const
from analysis.mass_balance import mass_balance

'''
This file contains functions that allow us to convert airflow characteristics, equivalent velocity and reduced parameters (mostly used in
elevator trim curve / force curve and calculations).
    1. calc_static_pressure
    2. calc_Mach_number
    3. calc_static_temperature
    4. calc_air_density
    5. calc_T_true
    6. calc_V_true
    7. calc_equivalent_velocity
    8. calc_reduced_equivalent_velocity
    9. calc_reduced_stick_force
    10. calc_reduced_elevator_deflection
    11. calc_aerodynamics                      -->      calculates multiple parameters at once with pre-defined functions.
                                                        depending on the use, it can return all parameters or only Ve.
'''


# Define standard parameters from assignment description
Ws = 60500      # [N]
mfs = 0.048     # [kg/s]
gamma = 1.4     # [-]
p0 = universal_const.rho0*universal_const.R*universal_const.Temp0


# Set-up to get p, M, T and rho

def calc_static_pressure(h):
    p = p0*(1+(universal_const.lam*h)/universal_const.Temp0)**(-universal_const.g/(universal_const.lam*universal_const.R))
    return p

def calc_Mach_number(h,Vc):

    h = np.asarray(h, dtype = float)
    Vc = np.asarray(Vc, dtype = float)

    p = calc_static_pressure(h)
    factor1 = 1 + (gamma-1)/(2*gamma)*(universal_const.rho0/p0)*Vc**2
    factor2 = (1 + p0/p*((factor1)**(gamma/(gamma-1))-1))
    factor3 = (2/(gamma-1))*(factor2**((gamma-1)/gamma)-1)
    M = np.sqrt(factor3)
    return M

def calc_static_temperature(TAT, M):
    factor = 1 + (gamma-1)/2*M**2
    Temp = TAT/factor
    return Temp

def calc_air_density(p,T):
    rho = p/(universal_const.R*T)
    return rho

def calc_T_true(h):                                         # Get temperature from altitude
    Temp = universal_const.Temp0 + universal_const.lam*h
    return Temp

def calc_V_true(T, M):                                      # Calculate true airspeed (based on temperature and Mach number)

    T = np.asarray(T, dtype = float)
    a = np.sqrt(mass_balance.gamma*universal_const.R*T)
    Vt = M*a
    return Vt





# Getting the reduced parameters

def calc_equivalent_velocity(V, rho):
    V = np.asarray(V, dtype = float)
    rho = np.asarray(rho, dtype = float)

    Ve = V*np.sqrt(rho/universal_const.rho0)
    return Ve

def calc_reduced_equivalent_velocity(Ve, W):
    Ve = np.asarray(Ve, dtype = float)
    W = np.asarray(W, dtype = float)

    Ve_r = Ve * np.sqrt(Ws/W)
    
    return Ve_r

def calc_reduced_stick_force(Fe, W):
    Fe_r = Fe * (Ws/W)
    return Fe_r

def calc_reduced_elevator_deflection(de_meas, Cmd, CmTc, Tcs, Tc):
    de_r = de_meas - CmTc/Cmd*(Tcs-Tc)
    return de_r


def calc_aerodynamics(hp, V, TAT, Ve_only: bool):
    p = calc_static_pressure(hp)                                                                # static pressure       [Pa]
    M = calc_Mach_number(hp, V)                                                                 # Mach number           [-]
    T_st = calc_static_temperature(TAT, M)                                                      # static temperature    [K]
    rho = calc_air_density(p, T_st)                                                             # air density           [kg/m^3]
    TAS = calc_V_true(TAT, M)                                                                   # True airspeed         [m/s]
    Ve = calc_equivalent_velocity(TAS, rho)                                                     # Equivalent airspeed   [m/s]

    if Ve_only:
        return Ve

    else:
        return T_st, rho, TAS, Ve, M