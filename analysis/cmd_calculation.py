import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import numpy as np

'''
This file contains additional functions used in calculating elevator effectiveness (Cm_delta)/
    1. ext_par_cmdelta  --> extract parameters from the xcg stationary measurements
    2. calc_xcg         --> calculate the xcg based on mass and balance parameters and the position of passenger 3R
'''

def ext_par_cmdelta(data, mass_initial):
    hp_avg = np.average([data['hp'][0], data['hp'][1]])
    V_avg = np.average([data['IAS'][0], data['IAS'][1]])
    TAT_avg = np.average([data['TAT'][0], data['TAT'][1]])
    m_f_used_avg = np.average([data['F. used'][0], data['F. used'][1]])
    mass_final = mass_initial - m_f_used_avg
    de1 = data['de'][0]
    de2 = data['de'][1]


    return hp_avg, V_avg, TAT_avg, m_f_used_avg, mass_final, de1, de2


# Calculate the initial xcg
def calc_xcg(m_f_total, m_f_used_avg, x_fuel, mass_initial, BEW, x_BEW, mnb_data, n_people, xp):

    mass =   mass_initial - m_f_used_avg                      # final mass (initial mass - the fuel used)
    m_fuel_final = m_f_total - m_f_used_avg


    moment  =  (BEW * x_BEW +              # mass components multiplied by position (shifted location of passenger 3R)
                 m_fuel_final * x_fuel + 
                 np.sum( mnb_data['mass [kg]'][0:n_people] * mnb_data['x_position'][0:n_people]) +     # First 7 passengers
                 mnb_data['mass [kg]'][n_people] * xp)                                                    # Passenger 3R (new position)

    xcg = moment/mass

    return xcg