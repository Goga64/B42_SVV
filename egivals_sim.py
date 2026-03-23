import numpy as np

from egivals_motion_pars import get_eigvals_sym, get_eigvals_asym, calc_eig_pars_sym, calc_eig_pars_asym, get_eig_pars_all
from egivals_measurement_read import get_initial_eig_time, get_initial_eig_pars, read_analysis_outputs, get_u_symmetric

'''
This file actually calculates the parameters from system eigenvalues. It returns a dataframe with all your heart desires.
What we should expect:
    1. Phugoid          -->     complex eigval, P < T_half,         tau = None
    2. Short Period     -->     complex eigval, P > T_half,         tau = None
    3. Dutch Roll       -->     complex eigval                      tau = None
    4. Aperiodic Roll   -->     real eigval,    P, T_half = None    tau > 0
    5. Spiral           -->     real eigval,    P, T_half = None    tau < 0

To get the aerodynamic measurements and determine the dataset from which we're taking values, we use:   coefs_output.txt.
To define which parameters from the dynamic measurements we need, we use:                               egivals_parameters.txt
The final characteristic motion parameters for all eigenmotions are stored in:                          egivals_sim_outputs.txt
'''


# READ the file with calculated aerodynamic coefficients to determine which measurement set to use.
file_txt = 'egivals_parameters.txt'
outputs_txt = 'coefs_outputs.txt'
file = open(outputs_txt, 'r')
source = file.readlines()[-1]
file.close()

# If we're using data_ref_2026:
if 'ref' in source:
    meas_file = 'analysis/data_ref_2026/PFD_01-03-2020fl1.xlsx'
    file_mat = 'analysis/data_ref_2026/FTISxprt-20260303_083939.mat'

# If we're using Test Flight 2 from 10.03.2026:
elif '10.03.2026' in source:
    meas_file = 'analysis/data_ref_2026/PFD_10-03-2026fl2.xlsx'
    file_mat = 'analysis/data_ref_2026/FTISxprt-20260310_102817.mat'

# Print a statement if neither set is recognised
else:
    print('I cannot seem to recognise the source of your data. Please try running main_analysis.py again.')


# Get the parameters from the aerodynamic analysis
Cla, Cma, Cmde, alpha0, mass_initial = read_analysis_outputs(outputs_txt)

# Extract the timestamps for each eigenmotion
t = get_initial_eig_time(meas_file)

# Get the parameters corresponding to each eigenmotion
data = get_initial_eig_pars(file_mat, file_txt, mass_initial, Cla, alpha0, t)

# Get the eigenvalues for symmetric flight and calculate their characteristic parameters
eigvals_phu, eigvals_sp = get_eigvals_sym(data, Cmde, Cma)
eigvals_dr, eigvals_ar, eigvals_s = get_eigvals_asym(data)

# Calculate P and T_half or tau (depending on the eigenmotion)
data_phu = calc_eig_pars_sym(eigvals_phu, data, phugoid=True, short_period=False)
data_sp = calc_eig_pars_sym(eigvals_sp, data, phugoid=False, short_period=True)
data_dr = calc_eig_pars_asym(eigvals_dr, data, dutch_roll=True, aperiodic_roll=False, spiral=False)
data_ar = calc_eig_pars_asym(eigvals_ar, data, dutch_roll=False, aperiodic_roll=True, spiral=False)
data_s = calc_eig_pars_asym(eigvals_s, data, dutch_roll=False, aperiodic_roll=False, spiral=True)


# Combine results
eig_all = get_eig_pars_all(data_phu, data_sp, data_dr, data_ar, data_s)


y, u = get_u_symmetric(file_mat, 'analysis/data_ref_2026/DSpace Parameters.txt')



# Store results
outputs = open('egivals_sim_outputs.txt', 'w')

o_coefs = open('coefs_outputs.txt', 'r')                # Indicate which measurement we're using in the final output file
header = o_coefs.readlines()[-1]                        
o_coefs.close()

print(header, file = outputs)                           # Write the measurement source on top of the file                 
print(eig_all, file = outputs)                          # Write the final results
outputs.close()

sim = open('cheeckout.txt', 'w')
print(y, file = sim)
print(u, file = sim)
sim.close()

print(y.shape)


