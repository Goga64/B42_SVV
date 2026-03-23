import sys, os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from analysis.aerodynamic_coefficients import calc_CL, calc_CD, est_CL2_CD
from analysis.measurements_reduction import calc_static_temperature, calc_static_pressure, calc_Mach_number, calc_air_density, calc_equivalent_velocity, calc_V_true
from thrust_og import Thrust
from analysis.measurements_scale import convert_measurements, lbs_to_kg
from analysis.mass_balance import mass_balance
from objects.parameters import universal_const, geo_const
from analysis.measurements_read import read_meas_stationary1, read_meas_stationary2
from analysis.main_analysis import mb_data

def Temp_Calc(h):
    Temp = universal_const.Temp0 - 0.0065 * h
    return Temp

# Step 1: Import and convert data file to ISA units

file = pd.ExcelFile('analysis/data_ref_2026/PFD_01-03-2020fl1.xlsx')

series1, series1_units = read_meas_stationary1(file)
series2, series2_units = read_meas_stationary2(file)

series1_c, series1_c_units = convert_measurements(series1, series1_units)
series2_c, series2_c_units = convert_measurements(series2, series2_units)

data_source = series1_c

#Step 2: Initialize necessary arrays and introduce constants

CL = np.array([])
CD = np.array([])
CDtemp = np.array([])
SAT = np.array([])

W = mass_balance.BEW * lbs_to_kg + mass_balance.m_fuel * lbs_to_kg + np.sum(mb_data['mass [kg]'][:])    #Initial mass of aircraft                       [kg]
rho0 = universal_const.rho0                                                                             #Air density at at h=0                          [kg/m3]

#Step 3: Calculate CL and temporary CD for use in linear regression used to calculate Oswald number and CD0 and perform regression

for i in range(len(data_source["V"])):
    V = data_source["V"][i]                                                                             #IAS                                            [m/s]
    h = data_source["h"][i]                                                                             #Pressure altitude                              [m]
    TAT = data_source["TAT"][i]                                                                         #Total Air Temperature                          [K]
    m_fl = data_source["FFI"][i]                                                                        #Fuel flow of left engine                       [kg/s]
    m_fr = data_source["FFR"][i]                                                                        #Fuel flow of right engine                      [kg/s]
    Wf_used = data_source['Wf'][i]                                                                      #Total mass of used fuel                        [kg]

    Temp = Temp_Calc(h)                                                                                 #ISA temperature                                [K]
    p = calc_static_pressure(h)                                                                         #ISA pressure                                   [Pa]
    M = calc_Mach_number(h,V)                                                                           #Mach number                                    [-]
    SAT = calc_static_temperature(TAT,M)                                                                #Static Air Temperature                         [K]
    rho_c = calc_air_density(p,SAT)                                                                     #Current air density                            [kg/m3]
    TAS = calc_V_true(TAT, M)                                                                           #True Airspeed                                  [m/s]
    Ve = calc_equivalent_velocity(TAS,rho_c)                                                            #Equivalent Airspeed                            [m/s]
    W_c = (W - Wf_used) * universal_const.g                                                             #Current aircraft weight                        [N]

    Cl = calc_CL(W_c,Ve,rho0)
    CL = np.append(CL,Cl)
    Thr_Total = Thrust.compute(h,M,SAT - Temp,m_fl) + Thrust.compute(h,M,SAT - Temp,m_fr)               #Thrust of both engines                         [N]

    Cdtemp = calc_CD(Thr_Total,Ve,rho0)                                                                 #Temporary Cd for  linear regression purposes   [-]
    CDtemp = np.append(CDtemp,Cdtemp)


Cl2cd, Cd0, e = est_CL2_CD(CL,CDtemp)

#Step 4: Use Cl and coefficients from linear regression to calculate actual Cd

for i in range(len(data_source["V"])):
    Cl = CL[i]

    Cd = Cd0 + (Cl**2)/(np.pi*geo_const.A*e)
    CD = np.append(CD,Cd)

#Step 5: Prepare 

CL = np.sort(CL)
CD = np.sort(CD)

CL_CD = [CL,CD]

plt.plot(CL_CD[0],CL_CD[1])
plt.xlabel('Lift coefficient')
plt.ylabel('Drag coefficient')
plt.show()