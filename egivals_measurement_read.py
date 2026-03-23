import sys, os
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from analysis.measurements_reduction import calc_static_pressure, calc_air_density
from analysis.measurements_read import read_meas_dynamic
from analysis.measurements_scale import convert_measurements
from objects.parameters import universal_const, geo_const

'''
This file contains functions which take the measurement files and extract data for points when different eigenmotions are initialized.
    1. get_initial_eig_time     -->     Gets the time of when each motion begins and converts it into seconds.
    2. get_initial_eig_pars     -->     Reads the rows corresponding to motion time stamps from the dynamic measurements and extracts
                                        crucial data. For weight, CL, and density, it calculates the parameters using functions from
                                        analysis. Then, it creates a dataframe with the parameters needed to create the ss systems.
'''

def read_analysis_outputs(file):
    f = open(file, 'r')
    lines = f.read().splitlines()
    Cla = float(lines[1])
    Cl0 = float(lines[2])
    alpha0 = float(lines[3])
    Cd0 = float(lines[4])
    e = float(lines[5])
    Cmd = float(lines[6])
    Cma = float(lines[7])
    mass_initial = float(lines[8])
    f.close()

    return Cla, Cma, Cmd, alpha0, mass_initial


def get_initial_eig_time(meas_file):
    try:
        df = pd.read_excel(meas_file, sheet_name="Sheet1", header=None, usecols = list(range(3,10)))
    except ValueError:
        df = pd.read_excel(meas_file, sheet_name="Overview", header=None, usecols = list(range(3,10)))
        
    df = df.iloc[82:].reset_index(drop=True)
    
    t_phugoid = df.iloc[0][3].hour*3600 + df.iloc[0][3].minute*60 + df.iloc[0][3].second
    t_short_period = df.iloc[1][3].hour*3600 + df.iloc[1][3].minute*60 + df.iloc[1][3].second
    t_dutch_roll = df.iloc[0][6].hour*3600 + df.iloc[0][6].minute*60 + df.iloc[0][6].second
    t_aperiodic_roll = df.iloc[0][9].hour*3600 + df.iloc[0][9].minute*60 + df.iloc[0][9].second
    t_spiral = df.iloc[1][9].hour*3600 + df.iloc[1][9].minute*60 + df.iloc[1][9].second

    t = t_phugoid, t_short_period, t_dutch_roll, t_aperiodic_roll, t_spiral

    return t

def get_u_symmetric(file_mat, file_txt):
    flight_data, flight_data_units, flight_data_descr = read_meas_dynamic(file_mat, file_txt)
    flight_data_c, flight_units_c = convert_measurements(flight_data, flight_data_units)


    alpha = flight_data_c['vane_AOA']
    theta = flight_data_c['Ahrs1_Pitch']
    TAS = flight_data_c['Dadc1_tas']
    qc = flight_data_c['Ahrs1_bPitchRate']
    de = flight_data_c['delta_e']

    TAS0 = TAS[0]
    TAS = (TAS - TAS0)/(TAS0 + 1e-5)

    qc *= geo_const.c/(TAS0 + 1e-5)

    y = np.vstack((TAS, alpha, theta, qc)).T

    print(TAS[0], alpha[0], theta[0], qc[0])

    return y, de

def get_initial_eig_pars(file_mat, file_txt, mass_initial, Cl_alpha, alpha0, t):
    flight_data, flight_data_units, flight_data_descr = read_meas_dynamic(file_mat, file_txt)
    flight_data_c, flight_units_c = convert_measurements(flight_data, flight_data_units)

    for i in range(len(flight_data_c)):
        if flight_data_c['time'][i] == t[0]:
            data_phugoid = flight_data_c.iloc[i]
            mf_used = data_phugoid['lh_engine_FU'] + data_phugoid['rh_engine_FU']
            alpha = data_phugoid['vane_AOA']
            hp = data_phugoid['Dadc1_bcAlt']
            T_st = data_phugoid['Dadc1_sat']

            p = calc_static_pressure(hp)
            rho = calc_air_density(p, T_st)

            W_phu = (mass_initial - mf_used)*universal_const.g
            CL_phu = Cl_alpha*(alpha - alpha0)
            rho_phu = rho
            


        elif flight_data_c['time'][i] == t[1]:
            data_short_period = flight_data_c.iloc[i]
            mf_used = data_short_period['lh_engine_FU'] + data_short_period['rh_engine_FU']
            alpha = data_short_period['vane_AOA']
            hp = data_short_period['Dadc1_bcAlt']
            T_st = data_short_period['Dadc1_sat']

            p = calc_static_pressure(hp)
            rho = calc_air_density(p, T_st)

            W_sp = (mass_initial - mf_used)*universal_const.g
            CL_sp = Cl_alpha*(alpha - alpha0)
            rho_sp = rho


        elif flight_data_c['time'][i] == t[2]:
            data_dutch_roll = flight_data_c.iloc[i]
            mf_used = data_dutch_roll['lh_engine_FU'] + data_dutch_roll['rh_engine_FU']
            alpha = data_dutch_roll['vane_AOA']
            hp = data_dutch_roll['Dadc1_bcAlt']
            T_st = data_dutch_roll['Dadc1_sat']

            p = calc_static_pressure(hp)
            rho = calc_air_density(p, T_st)

            W_droll = (mass_initial - mf_used)*universal_const.g
            CL_droll = Cl_alpha*(alpha - alpha0)
            rho_droll = rho

        
        elif flight_data_c['time'][i] == t[3]:
            data_aperiodic_roll = flight_data_c.iloc[i]
            mf_used = data_aperiodic_roll['lh_engine_FU'] + data_aperiodic_roll['rh_engine_FU']
            alpha = data_aperiodic_roll['vane_AOA']
            hp = data_aperiodic_roll['Dadc1_bcAlt']
            T_st = data_aperiodic_roll['Dadc1_sat']

            p = calc_static_pressure(hp)
            rho = calc_air_density(p, T_st)

            W_aroll = (mass_initial - mf_used)*universal_const.g
            CL_aroll = Cl_alpha*(alpha - alpha0)
            rho_aroll = rho


        elif flight_data_c['time'][i] == t[4]:
            data_spiral = flight_data_c.iloc[i]
            mf_used = data_spiral['lh_engine_FU'] + data_spiral['rh_engine_FU']
            alpha = data_spiral['vane_AOA']
            hp = data_spiral['Dadc1_bcAlt']
            T_st = data_spiral['Dadc1_sat']

            p = calc_static_pressure(hp)
            rho = calc_air_density(p, T_st)

            W_spiral = (mass_initial - mf_used)*universal_const.g
            CL_spiral = Cl_alpha*(alpha - alpha0)
            rho_spiral = rho

    df = pd.DataFrame()
    df.insert(0, 'Phugoid', data_phugoid)
    df.insert(1, 'Short Period', data_short_period)
    df.insert(2, 'Dutch Roll', data_dutch_roll)
    df.insert(3, 'Aperiodic Roll', data_aperiodic_roll)
    df.insert(4, 'Spiral', data_spiral)
    df = df.transpose()
    df.insert(1, 'rho [kg/m3]', [rho_phu, rho_sp, rho_droll, rho_aroll, rho_spiral])
    df.insert(1, 'Weight [N]', [W_phu, W_sp, W_droll, W_aroll, W_spiral])
    df.insert(1, 'CL [-]', [CL_phu, CL_sp, CL_droll, CL_aroll, CL_spiral])
    df = df.drop(columns = ['lh_engine_FU', 'rh_engine_FU', 'Dadc1_sat', 'Dadc1_tat', 'Dadc1_cas', 'vane_AOA', 'Dadc1_bcAlt', 'time'])

    return df