import sys, os
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from analysis.aerodynamic_coefficients import calc_CL, calc_CD, est_CL2_CD, est_CLa, calc_Cmdelta, calc_Cmalpha, calc_dynamic_pressure, ext_par_coefs
from analysis.measurements_reduction import calc_reduced_elevator_deflection, calc_reduced_equivalent_velocity, calc_reduced_stick_force, calc_aerodynamics
from analysis.thrust_calculation import calc_thrust
from analysis.measurements_read import read_meas_stationary1, read_meas_stationary2, read_meas_elevator_trim, read_meas_dynamic, read_meas_mnb, read_meas_xcg, read_position_shift
from analysis.measurements_scale import convert_measurements, convert_mass_balance
from analysis.elevator_trim_curve import est_de_dalpha, est_Fe_curve, est_trim_curve, ext_par_elevator_trim
from analysis.cmd_calculation import calc_xcg, ext_par_cmdelta
from objects.parameters import universal_const, geo_const
from analysis.mass_balance import mass_balance


# Define measurement files
print('Choose flight data for which the parameters will be calculated:\n\t (1) data_ref_2026 \n\t (2) Test Flight 2, 10.03.2026')
choice = input('chosen data: ')

if choice == '1' :
    # Reference data
    file_xlsx = pd.ExcelFile('analysis/data_ref_2026/PFD_01-03-2020fl1.xlsx')
    file_mat = 'analysis/data_ref_2026/FTISxprt-20260303_083939.mat'

elif choice == '2':
    # Data from 10.03.2026,  Flight 2
    file_xlsx = pd.ExcelFile('analysis/data_ref_2026/PFD_10-03-2026fl2.xlsx')
    file_mat = 'analysis/data_ref_2026/FTISxprt-20260310_102817.mat'

else:
    print('Invalid choice. Reference data will be used.')
    # Reference data
    file_xlsx = pd.ExcelFile('analysis/data_ref_2026/PFD_01-03-2020fl1.xlsx')
    file_mat = 'analysis/data_ref_2026/FTISxprt-20260303_083939.mat'

# Parameter list
file_txt = 'analysis/data_ref_2026/DSpace Parameters.txt'

# Define measurements data and convert it to SI units
series1, series1_units = read_meas_stationary1(file_xlsx)
series2, series2_units = read_meas_stationary2(file_xlsx)
em, em_units = read_meas_elevator_trim(file_xlsx)
flight_data, flight_data_units, flight_data_descr = read_meas_dynamic(file_mat, file_txt)
mnb_data, mnb_data_units = read_meas_mnb(file_xlsx, mass_balance.x_list)
xcg_data, xcg_units = read_meas_xcg(file_xlsx)
mf_block, mf_block_units, xp_list, xp_units = read_position_shift(file_xlsx, mass_balance.x_list)

series1_c, series1_c_units = convert_measurements(series1, series1_units)
series2_c, series2_c_units = convert_measurements(series2, series2_units)
em_c, em_c_units = convert_measurements(em, em_units)
flight_data_c, flight_data_c_units = convert_measurements(flight_data, flight_data_units)
xcg_data_c, xcg_c_units = convert_measurements(xcg_data, xcg_units)
mf_block_c, mf_block_c_units = convert_measurements(mf_block, mf_block_units)
xp_list_c, xp_c_units = convert_measurements(xp_list, xp_units)
BEW_c, x_BEW_c, moment_fuel_c, m_fuel_c, x_fuel_c, mb_data = convert_mass_balance(mass_balance.BEW, mass_balance.x_BEM, mass_balance.moment_fuel, mf_block, mass_balance.x_fuel, mnb_data)

#----------------------------------------------------------------------------------------------------------------------------------------------------------

mass_initial = BEW_c + m_fuel_c + np.sum(mb_data['mass [kg]'][:])


#-------------------------------------------------------------LIFT AND DRAG COEFFICIENTS--------------------------------------------------------------------

#Extract key parameters from Series1
W, V, hp, Tat, alpha, m_f_dot_l, m_f_dot_r = ext_par_coefs(mass_initial, series1_c)

# Calculate thermodynamic characteristics and thrust for the coefficients
T_st, rho, TAS, Ve, M = calc_aerodynamics(hp, V, Tat, Ve_only = False)
Thr_total = calc_thrust(T_st,m_f_dot_l,m_f_dot_r,hp,M)                                      # Total thrust    [N]

# Calculate the coefficients
Cl = calc_CL(W, Ve, universal_const.rho0)
alpha_aero = alpha
Cl_alpha, Cl0, alpha0 = est_CLa(Cl, alpha)
Cd = calc_CD(Thr_total, Ve, universal_const.rho0)
Cl2_Cd, Cd0, e = est_CL2_CD(Cl, Cd)

#-------------------------------------------------------------CM_DELTA---------------------------------------------------------------

# Get average values from the stationary measurements for xcg shift:
hp_avg, V_avg, TAT_avg, m_f_used_avg, mass_final, de1, de2 = ext_par_cmdelta(xcg_data_c, mass_initial)

# Calculate the equivalent velocity
Ve = calc_aerodynamics(hp_avg, V_avg, TAT_avg, Ve_only = True)

#m_f_used_avg, x_fuel_c, mass_initial, BEW_c, x_BEW_c, mnb_data_c, n_people, xp_list_c)
xcg1 = calc_xcg(m_fuel_c, m_f_used_avg, x_fuel_c, mass_initial, BEW_c, x_BEW_c, mb_data, mass_balance.n_people-1, xp_list_c[0])
xcg2 = calc_xcg(m_fuel_c, m_f_used_avg, x_fuel_c, mass_initial, BEW_c, x_BEW_c, mb_data, mass_balance.n_people-1, xp_list_c[1])

Cmdelta = calc_Cmdelta(xcg1, xcg2, de1, de2, mass_final*universal_const.g, Ve, universal_const.rho0)

#--------------------------------------------------------ELEVATOR TRIM CURVE----------------------------------------------------------------------

alpha_trim, cas, TAT, de, h, Fe, FFL, FFR, FF_standard, Wf, W = ext_par_elevator_trim(em_c, series2_c, mass_balance.mfs, mass_initial)

T_st, rho, TAS, Ve, M = calc_aerodynamics(h, cas, TAT, Ve_only = False)

# Calculate the thrust and standard thrust (based on the standard fuel flow), then extract the coefficients
Thrust = calc_thrust(T_st, FFL, FFR, h, M)
Thrust_s = calc_thrust(T_st, FF_standard, FF_standard,h,M)

Tc = Thrust/(calc_dynamic_pressure(Ve, universal_const.rho0)*geo_const.S)
Tcs = Thrust_s/(calc_dynamic_pressure(Ve, universal_const.rho0)*geo_const.S)

# Get the reduced equivalent velocity Ve_r by applying functions from measurements_reduction.py
Ve_r = calc_reduced_equivalent_velocity(Ve, W)
de_r = calc_reduced_elevator_deflection(de, Cmdelta, mass_balance.CmTc, Tcs, Tc)
Fe_r = calc_reduced_stick_force(Fe, W)

de_dalpha = est_de_dalpha(alpha_trim, de_r)          # de/dalpha
trim = est_trim_curve(Ve_r, Fe_r)               # de_r-Ve_r slope
fe_coef = est_Fe_curve(Ve_r, Fe_r)              # for the force plot

#---------------------------------------------------------CM_ALPHA----------------------------------------------------------------------------
Cmalpha = calc_Cmalpha(de_dalpha, Cmdelta)

#----------------------------------------------------------RESULTS-----------------------------------------------------------------------------
outputs = open('coefs_outputs.txt', 'w')
print(f'Cl_alpha [rad^-1], Cl0 [-], alpha0 [rad], Cd0 [-], e [-], Cm_delta [rad^-1], Cm_alpha [-], mass_initial [kg] \n{Cl_alpha}\n{Cl0}\n{alpha0}\n{Cd0}\n{e}\n{Cmdelta}\n{Cmalpha}\n{mass_initial}', file = outputs)
if choice != '2':
    print('\nSource: data_ref_2026', file=outputs)
else:
    print('\nSource: Test Flight 2, 10.03.2026', file=outputs)

outputs.close()