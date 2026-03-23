# WIP system response from state space matrices

import scipy as sc
import numpy as np
import control.matlab as c
import matplotlib.pyplot as plt 
from objects.parameters import *
from objects.system import dyn_system_sym, dyn_system_asym
import control as ctrl
from matplotlib.pyplot import figure



import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib

# Matrices for the state space systems:
from visualisation.simulation_const import *


font = {'family' : "Times New Roman",
        'size'   : 14}
matplotlib.rc('font', **font)

SymmetricSystem = dyn_system_sym(W, theta, rho, TAS, Cmde, Cma, deriv.iterative_par) # Class object

AsymmetricSystem = dyn_system_asym(W, CL, rho, TAS, deriv.iterative_par) # Class object

# Symmetric
A_s, B_s, C_s, D_s = SymmetricSystem.construct_state_sp() # Single input, 4 outputs

    # Input: elevator deflection
    # Outputs: u^, alpha, theta, q(c^bar/V)


# Asymmetric 
A_a, B_a, C_a, D_a = AsymmetricSystem.construct_state_sp() # Two inputs, 4 outputs

    # Input: rudder deflection and aileron deflection

    # Outputs: beta, phi, pbV, rbV



# Function to get all the responses from matrices and chosen time period and time step
def responses(A_s, B_s, C_s, D_s, A_a, B_a, C_a, D_a, T, dt):

    t = np.arange(0, T+dt, dt) # Time array for ploting (should be different for every dt)




    ##### Symmetric: #####

    # Create state space system

    ss_symmetric_main = c.ss(A_s, B_s, np.eye(4), np.zeros((4,1)))

    # Create transferfunction for state space system

    TF_symmetric_main = c.tf(ss_symmetric_main)

    # Extract relationship from input to outputs

    HS11 = TF_symmetric_main[0, 0]
    HS21 = TF_symmetric_main[1, 0]
    HS31 = TF_symmetric_main[2, 0]
    HS41 = TF_symmetric_main[3, 0]


    # Apply step response to each indevidualy

    Ys11, T11 = c.step(HS11, t)
    Ys21, T21 = c.step(HS21, t)
    Ys31, T31 = c.step(HS31, t)
    Ys41, T41 = c.step(HS41, t)

    # Apply impulse response to each indevidualy

    IYs11, T11 = c.impulse(HS11, t)
    IYs21, T21 = c.impulse(HS21, t)
    IYs31, T31 = c.impulse(HS31, t)
    IYs41, T41 = c.impulse(HS41, t)


    ##### Asymmetric: #####

    # Create state space system

    ss_asymmetric_main = c.ss(A_a, B_a, np.eye(4), np.zeros((4,2)))

    # Create transferfunction for state space system

    TF_asymmetric_main = c.tf(ss_asymmetric_main)

    # Extract relationship from input to outputs

    # ailerons
    Ha11 = TF_asymmetric_main[0, 0].minreal()
    Ha21 = TF_asymmetric_main[1, 0].minreal()
    Ha31 = TF_asymmetric_main[2, 0].minreal()
    Ha41 = TF_asymmetric_main[3, 0].minreal()

    # rudder
    Ha12 = TF_asymmetric_main[0, 1].minreal()
    Ha22 = TF_asymmetric_main[1, 1].minreal()
    Ha32 = TF_asymmetric_main[2, 1].minreal()
    Ha42 = TF_asymmetric_main[3, 1].minreal()


    # Apply step response to each indevidualy

    # Step
    Ya11, T11 = c.step(Ha11, t)
    Ya21, T21 = c.step(Ha21, t)
    Ya31, T31 = c.step(Ha31, t)
    Ya41, T41 = c.step(Ha41, t)

    Ya12, T11 = c.step(Ha12, t)
    Ya22, T21 = c.step(Ha22, t)
    Ya32, T31 = c.step(Ha32, t)
    Ya42, T41 = c.step(Ha42, t)

    # Impulse
    IYa11, T11 = c.impulse(Ha11, t)
    IYa21, T21 = c.impulse(Ha21, t)
    IYa31, T31 = c.impulse(Ha31, t)
    IYa41, T41 = c.impulse(Ha41, t)

    IYa12, T11 = c.impulse(Ha12, t)
    IYa22, T21 = c.impulse(Ha22, t)
    IYa32, T31 = c.impulse(Ha32, t)
    IYa42, T41 = c.impulse(Ha42, t)

    # Apply step response to both inputs simultaneously using forced response

    # Step inputs to both rudder and ailerons

    u1 = np.ones_like(t)
    u2 = np.ones_like(t)

    # Simultaneous input

    U_simultaneous = np.vstack((u1, u2))

    # Performing the forced responsse for each indevidual output from both inputs 

    Tsim, Ysim = ctrl.forced_response(ss_asymmetric_main, t, U_simultaneous)

    Ya_sim1 = Ysim[0]
    Ya_sim2 = Ysim[1]
    Ya_sim3 = Ysim[2]
    Ya_sim4 = Ysim[3]

    # Giga dictionary from hell (has all the responses and time array)
    outputs = {}

    outputs['Ys11'] = Ys11
    outputs['Ys21'] = Ys21
    outputs['Ys31'] = Ys31
    outputs['Ys41'] = Ys41

    outputs['IYs11'] = IYs11
    outputs['IYs21'] = IYs21
    outputs['IYs31'] = IYs31
    outputs['IYs41'] = IYs41

    outputs['Ya11'] = Ya11
    outputs['Ya21'] = Ya21
    outputs['Ya31'] = Ya31
    outputs['Ya41'] = Ya41

    outputs['Ya12'] = Ya12
    outputs['Ya22'] = Ya22
    outputs['Ya32'] = Ya32
    outputs['Ya42'] = Ya42

    outputs['IYa11'] = IYa11
    outputs['IYa21'] = IYa21
    outputs['IYa31'] = IYa31
    outputs['IYa41'] = IYa41

    outputs['IYa12'] = IYa12
    outputs['IYa22'] = IYa22
    outputs['IYa32'] = IYa32
    outputs['IYa42'] = IYa42

    outputs['Ya_sim1'] = Ya_sim1
    outputs['Ya_sim2'] = Ya_sim2
    outputs['Ya_sim3'] = Ya_sim3
    outputs['Ya_sim4'] = Ya_sim4

    outputs['t'] = t

    return outputs




def plotting(ax, A_s, B_s, C_s, D_s, A_a, B_a, C_a, D_a, T, dt, norm, cmap):

    outputs = responses(A_s, B_s, C_s, D_s, A_a, B_a, C_a, D_a, T, dt)

    # map dt → color
    color = cmap(norm(dt))

    ax.plot(outputs['t'], outputs['IYa12'], label=f'dt = {dt}', color=color, linewidth = 2, marker = 'o', markersize = 3)



time_steps = [0.01, 0.1, 0.25, 0.5]
#time_steps = np.arange(0.05, 0.5, 0.0125) #art mode

fig, ax = plt.subplots(figsize=(16, 10))

norm = mcolors.Normalize(vmin=min(time_steps), vmax=max(time_steps))
cmap = plt.get_cmap('cool')

# plot all lines
for dt in time_steps:
    plotting(ax, A_s, B_s, C_s, D_s, A_a, B_a, C_a, D_a, tfinal, dt, norm, cmap)

# create ONE colorbar
sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Time step [s]', fontsize = 18)

ax.set_title("Rudder Impulse Responce")
ax.set_xlabel("Time [s]", fontsize = 16)
ax.set_ylabel(r"$\beta$"+"[deg]", fontsize = 18)


ax.legend()
plt.tight_layout()
plt.show()

fig.savefig('visualisation/outputs/dt_diffe_vis.png', dpi=300)

##### Eigen Values #####


