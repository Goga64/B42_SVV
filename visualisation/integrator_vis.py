import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

from integrator import integration_sym, integration_asym
from matplotlib.collections import LineCollection
from simulation_const import *
import objects.system as syst


from matplotlib.legend_handler import HandlerLineCollection
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D


import matplotlib.colors as colors
import matplotlib


from matplotlib.lines import Line2D

font = {'family' : "Times New Roman",
        'size'   : 14}

matplotlib.rc('font', **font)



class HandlerColormap(HandlerLineCollection):

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height,
                       fontsize, trans):

        cmap = orig_handle.cmap
        norm = orig_handle.norm

        x = np.linspace(0, width, 100)
        y = np.full_like(x, height / 2)

        points = np.array([x, y]).T.reshape(-1,1,2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(np.linspace(norm.vmin, norm.vmax, 100))
        lc.set_linewidth(3)
        lc.set_transform(trans)

        return [lc]



def plotting(control_arrays, t_array_asym, arrays, names, t_contorl, figname):

    diff_lst = np.abs(np.array(control_arrays, dtype=float) - np.array(arrays, dtype=float)) 
    cmap = plt.get_cmap('jet')
    fontsizelst = [16, 16, 18, 18]


    index = 0
    fig, ax = plt.subplots(2,2, figsize=(16, 10), dpi=100)
    fig.text(0.5, 0.94, figname, ha='center', fontsize = 26)
    for i in range(2):
        for j in range(2):
            if asym_select[index]:
                diff = diff_lst[index]
                norm = colors.Normalize(vmin=np.min(diff_lst[index]), vmax=np.max(diff_lst[index]))

                # reference line (dashed)
                ref_line, = ax[i,j].plot(
                    t_array_asym, arrays[index],
                    color="0.7", linestyle='--',
                    label=names[index]+" Numerical Integrator"
                )
                #ax[i,j].set_title(names[index])

                # control line (colored)
                x = np.array(t_contorl)
                y = np.array(control_arrays[index])

                points = np.array([x, y]).T.reshape(-1,1,2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)

                lc = LineCollection(segments, cmap=cmap, norm=norm)
                lc.set_array(diff[:-1])
                lc.set_linewidth(2)
                ax[i,j].add_collection(lc)

                # legend with rainbow line
                ax[i,j].legend(
                    handles=[ref_line, lc],
                    labels=["Numerical Integrator", " Control Responce"],
                    handler_map={LineCollection: HandlerColormap()}
                )

                # axes limits
                #ax[i,j].set_xlim(x.min() - 0.05*x.min(), x.max() + 0.05*x.max())
                #ax[i,j].set_ylim(y.min() - 0.2*y.min(), y.max() + 0.2*y.max())
                ax[i,j].margins(0.01)
                ax[i,j].set_xlabel("Time [s]", fontsize = 16)
                ax[i,j].set_ylabel(names[index], fontsize = fontsizelst[index])
                # colorbar per subplot
                cbar = fig.colorbar(lc, ax=ax[i,j], norm = norm)
                cbar.ax.set_title("Difference", pad=8, x = 2)
                
            index += 1

    plt.show()
    fig.savefig('visualisation/outputs/'+ figname +' TAS = '+ str(TAS)+' t = '+str(tfinal)+'dt ='+str(dt)+'.png', dpi=300)


def symetric_integrator(selection, control_modes):
    x_sym = np.array([[u], [alpha], [theta], [qcV]])
    dsym = syst.dyn_system_sym(W, theta, rho, TAS, Cmde, Cma, deriv.iterative_par)
    Asym, Bsym, _, _ = dsym.construct_state_sp()
    t_array_sym, u_array, alpha_array, theta_array, qcV_array, W_array = integration_sym(dt, tfinal, Asym, Bsym, x_sym, TAS, constants, thrust_info, W, rho, h, control_modes[0], dsym)

    arrays = [u_array, alpha_array, theta_array, qcV_array]
    names = ["u_array", "alpha_array", "theta_array", "qcV_array"]

    for i in range(len(arrays)):
        if selection[i]:
            plt.plot(t_array_sym, arrays[i], label = names[i])
        
    plt.xlabel("Time")
    plt.ylabel("Y")
    plt.legend()
    plt.show()



def asymetric_integrator(selection, control_modes):
    x_asym = np.array([[beta], [phi], [pbV], [rbV]])
    dasym = syst.dyn_system_asym(W, CL, rho, TAS, deriv.iterative_par)
    Aasym, Basym, _, _ = dasym.construct_state_sp()
    t_array_asym, beta_array, phi_array, pbV_array, rbV_array, W_array = integration_asym(dt, tfinal, Aasym, Basym, x_asym, TAS, constants, thrust_info, W, rho, control_modes[1], control_modes[2], dasym)
    print("Eigenvalues of asymetric A matrix")
    print(np.linalg.eig(Aasym))
    arrays = [beta_array, phi_array, pbV_array, rbV_array]
    names = ["beta_array", "phi_array", "pbV_array", "rbV_array"]

    for i in range(len(arrays)):
        if selection[i]:
            plt.plot(t_array_asym, arrays[i], label = names[i])
        
    plt.xlabel("Time")
    plt.ylabel("Y")
    plt.legend()
    plt.show()


def ruddercomp(asym_select, control_modes,figname):
    from responses import Ya12, Ya22, Ya32, Ya42, t_contorl
    control_arrays = [Ya12, Ya22, Ya32, Ya42]


    x_asym = np.array([[beta], [phi], [pbV], [rbV]])
    dasym = syst.dyn_system_asym(W, CL, rho, TAS, deriv.iterative_par)
    Aasym, Basym, _, _ = dasym.construct_state_sp()
    t_array_asym, beta_array, phi_array, pbV_array, rbV_array, W_array = integration_asym(dt, tfinal, Aasym, Basym, x_asym, TAS, constants, thrust_info, W, rho, control_modes[0], control_modes[1], dasym)
    arrays = [beta_array, phi_array, pbV_array, rbV_array]
    names = [r"$\beta$"+"[deg]", r"$\varphi$"+"[deg]", r"$\frac{pb}{2V}$", r"$\frac{rb}{2V}$"]
    
    plotting(control_arrays, t_array_asym, arrays, names, t_contorl, figname)


def aileroncomp(asym_select, control_modes, figname):
    from responses import Ya11, Ya21, Ya31, Ya41, t_contorl
    control_arrays = [Ya11, Ya21, Ya31, Ya41]


    x_asym = np.array([[beta], [phi], [pbV], [rbV]])
    dasym = syst.dyn_system_asym(W, CL, rho, TAS, deriv.iterative_par)
    Aasym, Basym, _, _ = dasym.construct_state_sp()
    t_array_asym, beta_array, phi_array, pbV_array, rbV_array, W_array = integration_asym(dt, tfinal, Aasym, Basym, x_asym, TAS, constants, thrust_info, W, rho, control_modes[0], control_modes[1], dasym)
    arrays = [beta_array, phi_array, pbV_array, rbV_array]
    names = [r"$\beta$"+"[deg]", r"$\varphi$"+"[deg]", r"$\frac{pb}{2V}$", r"$\frac{rb}{2V}$"]
    
    plotting(control_arrays, t_array_asym, arrays, names, t_contorl, figname)




def bothcomp(asym_select, control_modes, figname):
    from responses import Ya_sim1, Ya_sim2, Ya_sim3, Ya_sim4, t_contorl
    control_arrays = [Ya_sim1, Ya_sim2, Ya_sim3, Ya_sim4]


    x_asym = np.array([[beta], [phi], [pbV], [rbV]])
    dasym = syst.dyn_system_asym(W, CL, rho, TAS, deriv.iterative_par)
    Aasym, Basym, _, _ = dasym.construct_state_sp()
    t_array_asym, beta_array, phi_array, pbV_array, rbV_array, W_array = integration_asym(dt, tfinal, Aasym, Basym, x_asym, TAS, constants, thrust_info, W, rho, control_modes[0], control_modes[1], dasym)
    arrays = [beta_array, phi_array, pbV_array, rbV_array]
    names = [r"$\beta$"+"[deg]", r"$\varphi$"+"[deg]", r"$\frac{pb}{2V}$", r"$\frac{rb}{2V}$"]
    
    plotting(control_arrays, t_array_asym, arrays, names, t_contorl, figname)

    
control_modes = ["step", "step", "zero"]        # elevator, aileron, rudder

sym_select = [False, True, False, True]
asym_select = [True, True, True, True]

control_mode_rudder = ["zero", "step"]
asym_select_rudder = [True, True, True, True]

control_mode_ail = ["step", "zero"]
asym_select_ail = [True, True, True, True]

control_mode_both = ["step", "step"]
asym_select_both = [True, True, True, True]






#symetric_integrator(sym_select, control_modes)
#asymetric_integrator(asym_select, control_modes)



ruddercomp(asym_select_rudder, control_mode_rudder, "Rudder")
aileroncomp(asym_select_ail, control_mode_ail, "Aileron")
bothcomp(asym_select_both, control_mode_both, "Aileron & Rudder")
