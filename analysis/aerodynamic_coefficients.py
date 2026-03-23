import numpy as np
from sklearn.linear_model import LinearRegression
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from objects.parameters import universal_const, geo_const

'''
This is the file for calculating aerodynamic parameters and coefficients. All formulae used in calculating the lift characteristics,
drag characteristics, Cmdelta, and Cmalpha simply follow the derivations from Chapter 3 of the plan (Analysis of Measurements).
    1. ext_par_coefs            -->     extract key parameters from series1 stationary measurements
    2. calc_dynamic_pressure    -->     self-explanatory
    3. calc_CL
    4. est_CLa
    5. calc_CD
    6. est_CL2_CD
    7. calc_Cmdelta
    8. calc_Cmalpha
'''
# Extract key parameters for calculating the coefficients
def ext_par_coefs(mass_initial, series1_c):
    Wf_used = series1_c['Wf']                                                             # Used fuel [kg]
    W = ((mass_initial - Wf_used)*universal_const.g).tolist()                             # Total weight (initial mass - fuel used)*g [N]

    # Get data from Stationary Measurement 1
    V = series1_c['V'].to_numpy()                                                         # IAS                 [m/s]
    hp = series1_c['h'].to_numpy()                                                        # p. altitude         [m]
    Tat = series1_c['TAT'].to_numpy()                                                     # Total temp.         [K]
    alpha = series1_c['Aoa'].to_numpy()                                                   # AoA                 [rad]
    m_f_dot_l = series1_c['FFI']                                                          # Fuel flow (left)    [kg/s]
    m_f_dot_r = series1_c['FFR']                                                          # Fuel flow (right)   [kg/s]

    return W, V, hp, Tat, alpha, m_f_dot_l, m_f_dot_r


def calc_dynamic_pressure(V, rho):                          # Caculate dynamic pressure (based on true airspeed and altitude)
    q = 0.5*rho*V**2
    return q


# Lift Characteristics

def calc_CL(W, V, rho):                                     # Calculate the CL (based on weight and dynamic pressure)
    Cl = W/(calc_dynamic_pressure(V, rho)*geo_const.S)
    return Cl

def est_CLa(Cl, alpha):                                     # Estimate the Cl-alpha, Cl0 and alpha0 (based on CL and alpha)
    alpha = alpha.reshape(-1,1)
    model = LinearRegression()
    model.fit(alpha,Cl)
    Cla = model.coef_[0]
    Cl0 = model.intercept_
    alpha0 = -Cl0/Cla

    return Cla, Cl0, alpha0

# Drag Characteristics

def calc_CD(T, V, rho):                                     # Calculate CD (based on T = D --> Cd = W/(dynamic pressure*S))
    Cd = T/(calc_dynamic_pressure(V, rho)*geo_const.S)
    return Cd

def est_CL2_CD(Cl, Cd):
    Cl = Cl.reshape(-1,1)
    model = LinearRegression()                              # Estimate the slope of Cl**2-Cd
    model.fit(Cl**2, Cd) 
    slope = model.coef_[0]
    Cd0 = model.intercept_                                 # Estimate Cd0 as the intercept
    e = 1/(np.pi*geo_const.A*slope)                        # Estimate e from slope = 1/(pi*A*e)  --> e = 1/(pi*A*slope)
    return slope, Cd0, e

# Stability derivatives

def calc_Cmdelta(x1, x2, de1, de2, W, V, rho):              # Estimate elevator effectiveness Cmd (based on xcg shift)
    Cn = W/(calc_dynamic_pressure(V,rho)*geo_const.S)
    delta_e = de2-de1
    delta_x = x2-x1

    Cmdelta = -1/delta_e*Cn*(delta_x/geo_const.c)

    return Cmdelta

def calc_Cmalpha(de_da, Cmd):                           # Estimate longitudinal stability (based on trim slope da/de and Cmd)
    Cmalpha = -de_da*Cmd
    
    return Cmalpha