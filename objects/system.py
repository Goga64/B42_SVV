import numpy as np
import matplotlib.pyplot as plt
import control.matlab as c
import control as ctrl
from objects.parameters import derivatives, geo_const, universal_const

class dyn_system_sym:
    def __init__(self, W, theta, rho, TAS, Cmde, Cma, ctrl_dict):
        self.der = derivatives()
        self.geo = geo_const()
        self.uni = universal_const()
        self.ctrl_par = ctrl_dict
        self.TAS0 = TAS
        self.Cmde = Cmde
        self.Cma = Cma

        self.CX0 = self.der.compute_CX0(W, theta, rho, TAS, self.geo.S)
        self.CZ0 = self.der.compute_CZ0(W, theta, rho, TAS, self.geo.S)
        self.muc = (W/self.uni.g) / (rho * self.geo.S * self.geo.c)

        self.EOM_const = np.array([[self.ctrl_par['CXu'], self.ctrl_par['CXa'], self.CZ0, self.ctrl_par['CXq']],
                                  [self.ctrl_par['CZu'], self.ctrl_par['CZa'], -self.CX0, self.ctrl_par['CZq'] + 2*self.muc],
                                  [0, 0, 0, 1],
                                  [self.ctrl_par['Cmu'], Cma, 0, self.ctrl_par['Cmq']]])

        self.EOM_D = np.array([[-2*self.muc, 0, 0, 0],
                              [0, (self.ctrl_par['CZadot'] - 2*self.muc), 0, 0],
                              [0, 0, -1, 0],
                              [0, self.ctrl_par['Cmadot'], 0, -2*self.muc*self.geo.KY2]]) * (self.geo.c/TAS)

        self.Ctrl = np.array([[-self.ctrl_par['CXde']],
                               [-self.ctrl_par['CZde']],
                               [0],
                               [Cmde]])



    def update_running(self, W, theta, rho, TAS):
        self.CX0 = self.der.compute_CX0(W, theta, rho, TAS, self.geo.S)
        self.CZ0 = self.der.compute_CZ0(W, theta, rho, TAS, self.geo.S)
        self.muc = (W/self.uni.g) / (rho * self.geo.S * self.geo.c)

        self.EOM_const[0, 2] = self.CZ0
        self.EOM_const[1, 2] = self.CX0
        self.EOM_const[1, 3] = self.ctrl_par['CZq'] + 2*self.muc

        self.EOM_D[0, 0] = (-2*self.muc)* (self.geo.c/self.TAS0)
        self.EOM_D[1, 1] = (self.ctrl_par['CZadot'] - 2*self.muc)* (self.geo.c/self.TAS0)
        self.EOM_D[3, 3] = (-2*self.muc*self.geo.KY2)* (self.geo.c/self.TAS0)


    def update_self(self):
        self.ctrl_par = self.der.iterative_par

        self.EOM_const = np.array([[self.ctrl_par['CXu'], self.ctrl_par['CXa'], self.CZ0, self.ctrl_par['CXq']],
                                  [self.ctrl_par['CZu'], self.ctrl_par['CZa'], -self.CX0, self.ctrl_par['CZq'] + 2*self.muc],
                                  [0, 0, 0, 1],
                                  [self.ctrl_par['Cmu'], self.Cma, 0, self.ctrl_par['Cmq']]])

        self.EOM_D = np.array([[-2*self.muc, 0, 0, 0],
                              [0, (self.ctrl_par['CZadot'] - 2*self.muc), 0, 0],
                              [0, 0, -1, 0],
                              [0, self.ctrl_par['Cmadot'], 0, -2*self.muc*self.geo.KY2]]) * (self.geo.c/self.TAS0)

        self.Ctrl = np.array([[-self.ctrl_par['CXde']],
                               [-self.ctrl_par['CZde']],
                               [0],
                               [self.Cmde]])


    def construct_state_sp(self):
        P_inv = np.linalg.inv(self.EOM_D)
        A = P_inv @ ((-1) * self.EOM_const)
        B = P_inv @ self.Ctrl
        C = np.eye(4)
        D = np.zeros((4, 1))

        return A, B, C, D


    def targeted_iteration(self, y_target, t_array, u_vector, gradient_damping = 0.0075, dC = 0.00001, tol = 2e-3, max_iter = 10000, report=True, update_all=False, summary = True):
        N_par = len(self.der.key_list)
        gradient_data = np.zeros(N_par)
        error = 100.0
        norm = np.mean(y_target**2)

        iteration = 0
        while error > tol:
            iteration += 1
            effect_array = np.zeros(N_par)

            A_current, B_current, C, D = self.construct_state_sp()
            sys_current = c.ss(A_current, B_current, C, D)
            t, y_current = c.lsim(sys_current, u_vector, t_array)
            error = np.mean((y_current - y_target)**2)/norm


            for i, target in enumerate(self.der.key_list):
                initial = self.der.iterative_par[target]

                self.der.iterative_par[target] = initial + dC
                system_change = dyn_system_sym(W, theta, rho, TAS, Cmde, Cma, self.der.iterative_par)
                A_change, B_change, C, D = system_change.construct_state_sp()
                sys_change = c.ss(A_change, B_change, C, D)

                t, y_change = c.lsim(sys_change, u_vector, t_array)
                error_change = np.mean((y_change - y_target)**2)/norm

                dErr_dC = (error_change - error)/dC
                effect_array[i] = dErr_dC

                self.der.iterative_par[target] = initial

            if update_all == True:
                for j in range(N_par):
                    dErr_dC = effect_array[j]
                    temp = self.der.iterative_par[self.der.key_list[j]]
                    self.der.iterative_par[self.der.key_list[j]] = temp - gradient_damping*dErr_dC
                if report == True:
                    print('Updating...')
                    print('Error: ', error)
                    print('___________________________________')
            else:
                j = np.argmax(np.abs(effect_array))
                dErr_dC = effect_array[j]
                self.der.iterative_par[self.der.key_list[j]] -= gradient_damping*dErr_dC
                gradient_data[j] += 1
                if report == True:
                    print(self.der.key_list[j], 'identified to have the greatest effect.')
                    print('Updating...')
                    print('Error: ', error)
                    print('___________________________________')

                if summary == True:
                    plt.figure()
                    sort = np.argsort(gradient_data)
                    gradient_data = gradient_data[sort]
                    sorted_names = np.array(derivative_pars.key_list)[sort]
                    plt.bar(sorted_names, gradient_data)

                    plt.xlabel('Control Parameters')
                    plt.ylabel('Times Updated')
                    plt.title('Visualization of optimization algorithm parameter choices')

                    plt.show()

            if iteration > max_iter:
                break

        self.update_self()



class dyn_system_asym:
    def __init__(self, W, CL, rho, TAS, ctrl_dict):
        self.der = derivatives()
        self.geo = geo_const()
        self.uni = universal_const()
        self.ctrl_par = ctrl_dict
        self.TAS0 = TAS
        self.CL = CL

        self.mub = (W/self.uni.g) / (rho * self.geo.S * self.geo.b)

        self.EOM_const = np.array([[self.ctrl_par['CYb'], CL, self.ctrl_par['CYp'], self.ctrl_par['CYr'] - 4*self.mub],
                                  [0, 0, 1, 0],
                                  [self.ctrl_par['Clb'], 0, self.ctrl_par['Clp'], self.ctrl_par['Clr']],
                                  [self.ctrl_par['Cnb'], 0, self.ctrl_par['Cnp'], self.ctrl_par['Cnr']]])

        self.EOM_D = np.array([[(self.ctrl_par['CYbdot'] - 2*self.mub), 0, 0, 0],
                              [0, -0.5, 0, 0],
                              [0, 0, (-4*self.mub*self.geo.KX2), (4*self.mub*self.geo.KXZ)],
                              [self.ctrl_par['Cnbdot'], 0, (4*self.mub*self.geo.KXZ), (-4*self.mub*self.geo.KZ2)]]) * (self.geo.b/TAS)

        self.Ctrl = np.array([[-self.ctrl_par['CYda'], -self.ctrl_par['CYdr']],
                               [0, 0],
                               [-self.ctrl_par['Clda'], -self.ctrl_par['Cldr']],
                               [-self.ctrl_par['Cnda'], -self.ctrl_par['Cndr']]])



    def update_running(self, W, rho):
        self.mub = (W/self.uni.g) / (rho * self.geo.S * self.geo.b)

        self.EOM_const[0, 3] = self.ctrl_par['CYr'] - 4*self.mub

        self.EOM_D[0, 0] = (self.ctrl_par['CYbdot'] - 2*self.mub) * (self.geo.b/self.TAS0)
        self.EOM_D[2, 2] = (-4*self.mub*self.geo.KX2) * (self.geo.b/self.TAS0)
        self.EOM_D[2, 3] = (4*self.mub*self.geo.KXZ) * (self.geo.b/self.TAS0)
        self.EOM_D[3, 2] = (4*self.mub*self.geo.KXZ) * (self.geo.b/self.TAS0)
        self.EOM_D[3, 3] = (-4*self.mub*self.geo.KZ2) * (self.geo.b/self.TAS0)


    def update_self(self):
        self.ctrl_par = self.der.iterative_par

        self.EOM_const = np.array([[self.ctrl_par['CYb'], self.CL, self.ctrl_par['CYp'], self.ctrl_par['CYr'] - 4*self.mub],
                                  [0, 0, 1, 0],
                                  [self.ctrl_par['Clb'], 0, self.ctrl_par['Clp'], self.ctrl_par['Clr']],
                                  [self.ctrl_par['Cnb'], 0, self.ctrl_par['Cnp'], self.ctrl_par['Cnr']]])

        self.EOM_D = np.array([[(self.ctrl_par['CYbdot'] - 2*self.mub), 0, 0, 0],
                              [0, -0.5, 0, 0],
                              [0, 0, (-4*self.mub*self.geo.KX2), (4*self.mub*self.geo.KXZ)],
                              [self.ctrl_par['Cnbdot'], 0, (4*self.mub*self.geo.KXZ), (-4*self.mub*self.geo.KZ2)]]) * (self.geo.b/self.TAS0)

        self.Ctrl = np.array([[-self.ctrl_par['CYda'], -self.ctrl_par['CYdr']],
                               [0, 0],
                               [-self.ctrl_par['Clda'], -self.ctrl_par['Cldr']],
                               [-self.ctrl_par['Cnda'], -self.ctrl_par['Cndr']]])


    def construct_state_sp(self):
        P_inv = np.linalg.inv(self.EOM_D)
        A = P_inv @ ((-1) * self.EOM_const)
        B = P_inv @ self.Ctrl
        C = np.eye(4)
        D = np.zeros((4, 2))

        return A, B, C, D


    def targeted_iteration(self, y_target, t_array, u_vector, gradient_damping = 0.0075, dC = 0.00001, tol = 2e-3, max_iter = 10000, report=True, update_all=False, summary = True):
        N_par = len(self.der.key_list)
        gradient_data = np.zeros(N_par)
        error = 100.0
        norm = np.mean(y_target**2)

        iteration = 0
        while error > tol:
            iteration += 1
            effect_array = np.zeros(N_par)

            A_current, B_current, C, D = self.construct_state_sp()
            sys_current = c.ss(A_current, B_current, C, D)
            t, y_current = c.lsim(sys_current, u_vector, t_array)
            error = np.mean((y_current - y_target)**2)/norm


            for i, target in enumerate(self.der.key_list):
                initial = self.der.iterative_par[target]

                self.der.iterative_par[target] = initial + dC
                system_change = dyn_system_asym(W, theta, rho, TAS, Cmde, Cma, self.der.iterative_par)
                A_change, B_change, C, D = system_change.construct_state_sp()
                sys_change = c.ss(A_change, B_change, C, D)

                t, y_change = c.lsim(sys_change, u_vector, t_array)
                error_change = np.mean((y_change - y_target)**2)/norm

                dErr_dC = (error_change - error)/dC
                effect_array[i] = dErr_dC

                self.der.iterative_par[target] = initial

            if update_all == True:
                for j in range(N_par):
                    dErr_dC = effect_array[j]
                    temp = self.der.iterative_par[self.der.key_list[j]]
                    self.der.iterative_par[self.der.key_list[j]] = temp - gradient_damping*dErr_dC
                if report == True:
                    print('Updating...')
                    print('Error: ', error)
                    print('___________________________________')
            else:
                j = np.argmax(np.abs(effect_array))
                dErr_dC = effect_array[j]
                self.der.iterative_par[self.der.key_list[j]] -= gradient_damping*dErr_dC
                gradient_data[j] += 1
                if report == True:
                    print(self.der.key_list[j], 'identified to have the greatest effect.')
                    print('Updating...')
                    print('Error: ', error)
                    print('___________________________________')
                if summary == True:
                    plt.figure()
                    sort = np.argsort(gradient_data)
                    gradient_data = gradient_data[sort]
                    sorted_names = np.array(derivative_pars.key_list)[sort]
                    plt.bar(sorted_names, gradient_data)

                    plt.xlabel('Control Parameters')
                    plt.ylabel('Times Updated')
                    plt.title('Visualization of optimization algorithm parameter choices')

                    plt.show()

            if iteration > max_iter:
                break

        self.update_self()
