import sys, os
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from analysis.aerodynamic_coefficients import ext_par_coefs, calc_dynamic_pressure, calc_CL, est_CLa, calc_CD, est_CL2_CD, calc_Cmdelta, calc_Cmalpha
from analysis.measurements_read import read_meas_stationary1
from analysis.measurements_scale import convert_measurements

file_xlsx = pd.ExcelFile('analysis/data_ref_2026/PFD_01-03-2020fl1.xlsx')


series1, series1_units = read_meas_stationary1(file_xlsx)
series1_c, series1_c_units = convert_measurements(series1, series1_units)


def test_ext_par_coefs(mass_initital,series1_c):                #doing this one later
    print(f"{ext_par_coefs(mass_initial,series1_c)}")


def test_calc_dynamic_pressure(V, rho):
    q = calc_dynamic_pressure(V,rho)
    q_hand = 8820
    print(f"q: {q}, hand {q_hand}, discrepancy {abs(q - q_hand)}")


def test_calc_cl(V, rho, W):
    cl = calc_CL(W,V,rho)
    cl_hand = 0.22909
    print(f"cl: {cl}, hand {cl_hand}, discrepancy {abs(cl - cl_hand)}")


def test_est_CLa(Cl, alpha):
    result = [0,0,0]
    result[0], result[1], result[2] = est_CLa(Cl,alpha)
    cla_hand = 0.1
    print(f"cla {result[0]}, hand {cla_hand}, discrepancy {abs(result[0] - cla_hand)}")
    cl0_hand = 0.0
    print(f"cl0 {result[1]}, hand {cl0_hand}, discrepancy {abs(result[1] - cl0_hand)}")
    alpha0_hand = 0.0
    print(f"alpha0 {result[2]}, hand {alpha0_hand}, discrepancy {abs(result[2] - alpha0_hand)}")


def test_calc_CD(T, V, rho): 
    cd = calc_CD(T,V,rho)
    cd_hand = 0.037793
    print(f"cl: {cd}, hand {cd_hand}, discrepancy {abs(cd - cd_hand)}")


def test_est_CL2_CD(Cl, Cd):
    result = [0,0,0]
    result[0], result[1], result[2] = est_CL2_CD(Cl,Cd)
    slope_hand = 1
    print(f"slope {result[0]}, hand {slope_hand}, discrepancy {abs(result[0] - slope_hand)}")
    cd0_hand = 0.01
    print(f"cd0 {result[1]}, hand {cd0_hand}, discrepancy {abs(result[1] - cd0_hand)}")
    e_hand = 0.037720
    print(f"e {result[2]}, hand {e_hand}, discrepancy {abs(result[2] - e_hand)}")


def test_calc_Cmdelta(x1, x2, de1, de2, W, V, rho): 
    cmdelta = calc_Cmdelta(x1,x2,de1,de2,W,V,rho)
    cmdelta_hand = -0.11138
    print(f"cl: {cmdelta}, hand {cmdelta_hand}, discrepancy {abs(cmdelta - cmdelta_hand)}")

def test_calc_Cmalpha(de_da, Cmd):    
    cmalpha = calc_Cmalpha(de_da,Cmd)
    cmalpha_hand = -0.001
    print(f"cl: {cmalpha}, hand {cmalpha_hand}, discrepancy {abs(cmalpha - cmalpha_hand)}")





V = 120
rho = 1.225
mass_initial = 6179.068
W = 60616.66
cl_scale = np.array([0,0.1,0.2,0.3,0.4,0.5])
cd_scale = np.array([0.01,0.02,0.03,0.04,0.05,0.06])
alpha_scale = np.array([0,1,2,3,4,5])
T = 10000
x1 = 1
x2 = 2
de1 = 1
de2 = 2
de_da = -0.01
Cmd = -0.1

test_calc_Cmdelta(x1,x2,de1,de2,W,V,rho)