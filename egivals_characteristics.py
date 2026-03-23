import numpy as np
from objects.parameters import geo_const, derivatives
from analysis.measurements_reduction import calc_equivalent_velocity
'''
This file contains functions that can be used to compute the characteristics following from
the motion eigenvalues.
    1. calc_eig_period          -->   calculate motion period
    2. calc_eig_T-half          -->   calculate time to half amplitude (phugoid, short period, Dutch roll)
    3. calc_eig_time_const      -->   calculate the time constant (aperiodic motions: aperiodic roll, spiral motion)  
    4. get_characteristics_eig_sym  -->   a true 2-in-1 deal! Get both P and T_half with a single function!

NOTE:   The reader and assignment suggest to scale the eigvals with c/Ve or b/Ve, however based on the numerical results
        I think that our system is not non-dimensional (?), so applying the factor gives funny results.
'''

def calc_eig_period(eigvalue, TAS, rho, par):

    P = np.abs((2*np.pi/eigvalue.imag))
    #Ve = calc_equivalent_velocity(TAS, rho)
    #P *= par/Ve

    return P

def calc_eig_T_half(eigvalue, TAS, rho, par):

    T_half = (np.log(0.50))/(eigvalue.real)

    #Ve = calc_equivalent_velocity(TAS, rho)
    #T_half *= par/Ve

    return T_half

def calc_eig_time_const(eigvalue, TAS, rho, par):

    if eigvalue.imag != 0:
        print('Invalid eigvalue, imaginary part is not zero!')
    else:
        tau = -(1/eigvalue.real)

        #Ve = calc_equivalent_velocity(TAS, rho)
        #tau *= par/Ve

    return tau

def get_characteristics_eig_sym(eigvalue, TAS, rho, par):
    P = calc_eig_period(eigvalue, TAS, rho, par)
    T_half = calc_eig_T_half(eigvalue, TAS, rho, par)

    return P, T_half