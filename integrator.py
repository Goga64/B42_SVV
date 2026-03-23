
import numpy as np


def integration_sym(dt, tfinal, Asym, Bsym, x, TAS, constants, thrust_info, W, rho, h, control_type, dsym):
    v0 = TAS
    steps = int(tfinal//dt + 1)
    t = 0
    t_array_ctrl = np.arange(0, tfinal+dt, dt)
    t_array = np.zeros(steps+1)
    u_array = np.zeros(steps+1)
    alpha_array = np.zeros(steps+1)
    theta_array = np.zeros(steps+1)
    qcV_array = np.zeros(steps+1)
    W_array = np.zeros(steps+1)

    u_array[0] = x[0]
    alpha_array[0] = x[1]
    theta_array[0] = x[2]
    qcV_array[0] = x[3]
    W_array[0] = W


    if control_type == "step":
        de = np.ones(steps)


    for i in range(steps):
        xdot = np.matmul(Asym, x) + Bsym*de[i]
        x += xdot*dt
        t += dt

        t_array[i+1] = t
        u_array[i+1] = x[0]
        alpha_array[i+1] = x[1]
        theta_array[i+1] = x[2]
        qcV_array[i+1] = x[3]

        TAS = v0*(x[0]+1)
        h += TAS*np.sin(x[2] - x[1])
        rho = constants.rho(h)
        W -= thrust_info.fuel_fl*dt
        W_array[i+1] = W
        dsym.update_running(W, x[2], rho, TAS)
        Asym, Bsym, _, _ = dsym.construct_state_sp()
    
    return t_array, u_array, alpha_array, theta_array, qcV_array, W_array


def integration_asym(dt, tfinal, Aasym, Basym, x, TAS, constants, thrust_info, W, rho, aileron_type, rudder_type, dasym):
    v0 = TAS
    steps = int(tfinal//dt + 1)

    t = 0
    t_array = np.zeros(steps+1)
    beta_array = np.zeros(steps+1)
    phi_array = np.zeros(steps+1)
    pbV_array = np.zeros(steps+1)
    rbV_array = np.zeros(steps+1)
    W_array = np.zeros(steps+1)

    beta_array[0] = x[0]
    phi_array[0] = x[1]
    pbV_array[0] = x[2]
    rbV_array[0] = x[3]
    W_array[0] = W


    if aileron_type == "step":
        da = np.ones(steps)
    elif aileron_type == "zero":
        da = np.zeros(steps)

    if rudder_type == "step":
        dr = np.ones(steps)
    elif rudder_type == "zero":
        dr = np.zeros(steps)


    for i in range(steps):
        xdot = np.matmul(Aasym, x) + np.matmul(Basym, np.array([[da[i]], [dr[i]]]))
        x += xdot*dt
        t += dt

        t_array[i+1] = t
        beta_array[i+1] = x[0]
        phi_array[i+1] = x[1]
        pbV_array[i+1] = x[2]
        rbV_array[i+1] = x[3]

        # TAS is assumed constant
        # h is assumed constant, so rho is also maintained
        W -= thrust_info.fuel_fl*dt
        W_array[i+1] = W
        dasym.update_running(W, rho)
        Aasym, Basym, _, _ = dasym.construct_state_sp()
    
    return t_array, beta_array, phi_array, pbV_array, rbV_array, W_array


