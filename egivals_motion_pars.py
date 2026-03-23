from objects.parameters import derivatives, geo_const
import objects.system as sys
from egivals_characteristics import calc_eig_time_const, get_characteristics_eig_sym
import numpy as np
import pandas as pd

'''
This file contains all the functions required to get from system parameters to P, T_half (periodic motion) and tau (aperiodic motion).
    1. get_eigvals_sym      -->     Get the data for symmetric eigenmotions, create state space systems for them and extract eigenvalues.
    2. calc_eig_pars_sym    -->     Calculate P and T_half for the Phugoid or short period (depending on chosen bools when function is called).
    3. get_eigvals_asym     -->     get_eigvals_sym, but for asymmetric motion!
    4. calc_eig_pars_asym   -->     calc_eig_pars_sym, but for asymmetric motion! We now get P and T_half for the Dutch Roll, and tau for the
                                    Aperiodic Roll and Spiral!
    5. get_eig_pars_all     -->     Assemble all results into a single dataframe! :D
'''

#-------------------------------------------------------------Symmetric Motion------------------------------------------------------------------

def get_eigvals_sym(data, Cmde, Cma):
    
    # Read the data for Phugoid and Short Period
    data_phu = data.iloc[0]
    data_sp = data.iloc[1]

    # Create dynamic systems for both motions
    sample_sys_sym_phu = sys.dyn_system_sym(data_phu.iloc[1], data_phu.iloc[3], data_phu.iloc[2], data_phu.iloc[4], Cmde, Cma, derivatives().iterative_par)
    sample_sys_sym_sp = sys.dyn_system_sym(data_sp.iloc[1], data_sp.iloc[3], data_sp.iloc[2], data_sp.iloc[4], Cmde, Cma, derivatives().iterative_par)
    
    # Get the A matrix of the constructed state space system
    A_phu, _, _, _ = sample_sys_sym_phu.construct_state_sp()
    A_sp, _, _, _ = sample_sys_sym_sp.construct_state_sp()
    
    # Get the eigenvalues
    eigvals_phu = np.linalg.eig(A_phu).eigenvalues
    eigvals_sp = np.linalg.eig(A_sp).eigenvalues

    return eigvals_phu, eigvals_sp

def calc_eig_pars_sym(eigvals_sym, data, phugoid: bool, short_period: bool):

    # STEP 1: Check if only one eigenmotion is selected (the eigenvalues are unique, we can't do more than one eigenmotion at a time)
    if phugoid and short_period:
        print('Well, it would be nice to limit ourselves to just one eigenmotion at a time. You definitely *can* have too much of a good thing, you know?')
        print('Try again - but this time, choose wisely. Do not be greedy.')

        return    

    # STEP 2: Check if any eigenmotions were chosen at all
    elif not phugoid and not short_period:
        print('No eigenmotion selected, captain. Nothing to report here.')

        return
    
    # STEP 3:   Get the period and T_half for the chosen eigenmotion.
    # STEP 3.1: Check if the eigenvalues are complex --> real eigvals suggest the motion is not symmetric
    else:
        for eig in eigvals_sym:
            if abs(np.imag(eig)) < 1e-9:
                print('Eigenvalues do not correspond to symmetric motion.')
                print(f'Eigenvalue {eig} likely does not have an imaginary part. Please try again.')

                return

        eig_sym_sorted = sorted(eigvals_sym, key = lambda x: abs(np.imag(x)))                               # Sort the eigvals by their imaginary part

    # STEP 3.2: Calculate the P, T_half for the phugoid (lower magnitude of imag component)
        if phugoid:
            eig_phugoid = eig_sym_sorted[0:2]
            P_ph, T_ph = get_characteristics_eig_sym(eig_phugoid[0], data.iloc[0].iloc[4], data.iloc[0].iloc[2], geo_const.c)

            data = {'Motion':       ['Phugoid'],
                    'Eigvalue':     [eig_phugoid[0]],
                    'P [s]':        [P_ph],
                    'T_half [s]':   [T_ph],
                    'tau [s]':      ['-']}

            df = pd.DataFrame(data)        

            return df
    
    # STEP 3.3: Calculate the P, T_half for the Short Period (higher magnitude of imag component)
        if short_period:
            eig_short_period = eig_sym_sorted[2:4]
            P_sp, T_sp = get_characteristics_eig_sym(eig_short_period[0], data.iloc[1].iloc[4], data.iloc[1].iloc[2], geo_const.c)

            data = {'Motion':       ['Short Period'],
                    'Eigvalue':     [eig_short_period[0]],
                    'P [s]':        [P_sp],
                    'T_half [s]':   [T_sp],
                    'tau [s]':      ['-']}

            df = pd.DataFrame(data)        

            return df
    


#-------------------------------------------------------------------Asymmetric Motion------------------------------------------------------------------

def get_eigvals_asym(data):
    
    # Read the data for Dutch Roll, Aperiodic Roll and Spiral
    data_dr = data.iloc[2]
    data_ar = data.iloc[3]
    data_s = data.iloc[4]

    # Create dynamic systems for all eigenmotions
    sample_sys_asym_dr = sys.dyn_system_asym(data_dr.iloc[1], data_dr.iloc[0], data_dr.iloc[2], data_dr.iloc[4], derivatives().iterative_par)
    sample_sys_asym_ar = sys.dyn_system_asym(data_ar.iloc[1], data_ar.iloc[0], data_ar.iloc[2], data_ar.iloc[4], derivatives().iterative_par)
    sample_sys_asym_s = sys.dyn_system_asym(data_s.iloc[1], data_s.iloc[0], data_s.iloc[2], data_s.iloc[4], derivatives().iterative_par)
    
    # Get the A matrices from state space
    A_dr, _, _, _ = sample_sys_asym_dr.construct_state_sp()
    A_ar, _, _, _ = sample_sys_asym_ar.construct_state_sp()
    A_s, _, _, _ = sample_sys_asym_s.construct_state_sp()
    
    # Get the eigenvalues
    eigvals_dr = np.linalg.eig(A_dr).eigenvalues
    eigvals_ar = np.linalg.eig(A_ar).eigenvalues
    eigvals_s = np.linalg.eig(A_s).eigenvalues

    return eigvals_dr, eigvals_ar, eigvals_s


def calc_eig_pars_asym(eigvals_asym, data, dutch_roll: bool, aperiodic_roll: bool, spiral: bool):

# STEP 1: Check if any eigenmotions were selected at all
    if not dutch_roll and not aperiodic_roll and not spiral:
        print('No eigenmotion selected, captain. Nothing to report here.')

        return

# STEP 2: Check if only one eigenmotion was selected
    elif ((dutch_roll and aperiodic_roll) or (dutch_roll and spiral) or (aperiodic_roll and spiral)):
        print('Well, it would be nice to limit ourselves to just one eigenmotion at a time. You definitely *can* have too much of a good thing, you know?')
        print('Try again - but this time, choose wisely. Do not be greedy.')   

        return
    
    else:
        # Initialise lists for complex (Dutch Roll) and real eigenvalues
        eig_dutch_roll = []
        eig_real = []

        for eig in eigvals_asym:                 
            if np.abs(eig.imag) > 1e-9:                                     # Check if the eigenvalue is complex (imag > 0) or real
                eig_dutch_roll.append(eig)                                  # If complex --> Dutch Roll eigenvalue
            else:
                eig_real.append(eig)                                        # If real --> Aperiodic Roll or Spiral

        # Check if there are two real and two complex eigenvalues --> otherwise, the motion may not be asymmetric
        if len(eig_real) < 2:
            print('Caution! There are no real eigenvalues on board! This is likely not asymmetric motion.')
            print('Please reevaluate your life choices and return with some *real* eigenvalues. I mean it.')

        # Sort the real eigenvalues
        eig_real_sorted = sorted(eig_real, key = lambda x: np.abs(np.real(x)))

    # STEP 3:   Calculate the characteristic parameters for the chosen asymmetric eigenmotion
    # STEP 3.1: Get the period and T_half for the Dutch roll (same as for symmetric motions)
        if dutch_roll:
            P_dr, T_dr = get_characteristics_eig_sym(eig_dutch_roll[0], data.iloc[2].iloc[4], data.iloc[2].iloc[2], geo_const.b)

            data = {'Motion':       ['Dutch Roll'],
                    'Eigvalue':     [eig_dutch_roll[0]],
                    'P [s]':        [P_dr],
                    'T_half [s]':   [T_dr],
                    'tau [s]':      ['-']}

            df = pd.DataFrame(data)        

            return df

    # STEP 3.2: Get the time constant for the aperiodic roll (real eigenvalue with higher absolute value)
        if aperiodic_roll:
            eig_aperiodic_roll = np.min(eig_real_sorted)
            tau_ar = calc_eig_time_const(eig_aperiodic_roll, data.iloc[3].iloc[4], data.iloc[3].iloc[2], geo_const.b)

            data = {'Motion':       ['Aperiodic Roll'],
                    'Eigvalue':     [eig_aperiodic_roll],
                    'P [s]':        ['-'],
                    'T_half [s]':   ['-'],
                    'tau [s]':      [tau_ar]}
            
            df = pd.DataFrame(data)

            return df
        
    # STEP 3.3: Get the time constant for the spiral (real eigenvalue with lower absolute value)
        if spiral:
            eig_spiral = np.max(eig_real_sorted)
            tau_s = calc_eig_time_const(eig_spiral, data.iloc[4].iloc[4], data.iloc[4].iloc[2], geo_const.b)

            data = {'Motion':       ['Spiral'],
                    'Eigvalue':     [eig_spiral],
                    'P [s]':        ['-'],
                    'T_half [s]':   ['-'],
                    'tau [s]':      [tau_s]}
            
            df = pd.DataFrame(data)
        
            return df
#-------------------------------------------------------------Assemble all results-----------------------------------------------------------

def get_eig_pars_all(data_phu: pd.DataFrame, data_sp: pd.DataFrame, data_dr: pd.DataFrame, data_ar: pd.DataFrame, data_s: pd.DataFrame):

    df = pd.concat([data_phu, data_sp, data_dr, data_ar, data_s], ignore_index=True)

    return df

