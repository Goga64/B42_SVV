import sys, os
import numpy as np
from sklearn.linear_model import LinearRegression
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from objects.parameters import universal_const


'''
This file contains additional functions used in calculating the reduced parameters de_r, Ve_r and Fe_r, as well as the relations
between them and de/dalpha.
    1. ext_par_elevator_trim    -->     extract key parameters from the elevator deflection stationary measurements
    2. est_de_dalpha            -->     use linear regression to find the relation between de_r and d_alpha
    3. est_trim_curve           -->     use linreg to estimate the relation between Ve_r and de_r
    4. est_Fe_curve             -->     use linreg estimate Fe_r-Ve_r
'''
# Extract key parameters for elevator trim curve/force curve parameters

def ext_par_elevator_trim(em_c, series2_c, mfs, mass_initial):
    # Get the data from scaled dynamic measurements flight_data_c
    alpha = em_c['a'].to_numpy()             # AoA                      [rad]
    cas = em_c['IAS']                        # CAS                      [m/s]
    TAT = em_c['TAT']                        # TAT                      [K]
    de = em_c['de']                          # Elevator deflection      [rad]
    h = em_c['hp']                           # pressure altitude        [m]
    Fe = em_c['Fe']                          # Stick force              [N]
    FFL = em_c['FFl']                        # Fuel flow (left)         [kg/s]
    FFR = em_c['FFr']                        # Fuel flow (right)        [kg/s]
    FF_standard = np.ones_like(FFL)*mfs      # Standard fuel flow       [kg/s]

    if 'F. used' in em_c.columns and not em_c['F. used'].isna().any():      # Check if the fuel used data is available
        Wf = em_c['F. used'][0:7]
    else:
        Wf = series2_c['Wf'][0:7]                                           # If not, use series2_c

    W = (np.ones_like(Wf)*mass_initial - Wf)*universal_const.g       # AC weight after the fuel burn

    return alpha, cas, TAT, de, h, Fe, FFL, FFR, FF_standard, Wf, W

# Use linear regression to get the slopes for de/dalpha, de_r/Ve_r and Fe_r/Ve_r
def est_de_dalpha(alpha, de_r): 
    alpha = alpha.reshape(-1,1)                                   
    model = LinearRegression()
    model.fit(alpha, de_r)

    slope = model.coef_[0]
    
    return slope

def est_trim_curve(Ve_r, de_r):
    Ve_r = Ve_r.reshape(-1,1)
    model = LinearRegression()
    model.fit(Ve_r, de_r)

    slope = model.coef_[0]
    
    return slope

def est_Fe_curve(Ve_r, Fe_r):
    Ve_r = Ve_r.reshape(-1,1)
    model = LinearRegression()
    model.fit(Ve_r, Fe_r)

    slope = model.coef_[0]
    
    return slope

