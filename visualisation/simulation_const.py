from objects.parameters import universal_const, geo_const, thrust_par, derivatives

constants = universal_const()
geometry = geo_const()
thrust_info = thrust_par()
deriv = derivatives()


theta = 0.17
TAS = 180
Cmde = 0.025
Cma = 0.02
W = 60500
h = 4000
alpha = 2.0
u = 0.0
qcV = 0.0

rho = constants.rho(h)

CL = W/(0.5*rho*(TAS**2)*geometry.S)


# Asymetric
beta = 0.0
phi = 0.0
pbV = 0.0
rbV = 0.0


# Integrator
dt = 0.01
tfinal = 5
