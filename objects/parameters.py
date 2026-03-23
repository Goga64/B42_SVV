import math
pi = math.pi

class universal_const:
    rho0   = 1.2250          # air density at sea level [kg/m^3]
    lam = -0.0065         # temperature gradient in ISA [K/m]
    Temp0  = 288.15          # temperature at sea level in ISA [K]
    R      = 287.05          # specific gas constant [m^2/sec^2K]
    g      = 9.81

    def rho(self, h):
        return self.rho0 * (((1+(self.lam * h / self.Temp0))) ** (-((self.g / (self.lam*self.R)) + 1)))


class geo_const:
    #Standard geometrical:
    S      = 30.00	          # wing area [m^2]
    Sh     = 0.2 * S         # stabiliser area [m^2]
    Sh_S   = Sh / S	          # [ ]
    lh     = 0.71 * 5.968    # tail length [m]
    c      = 2.0569	          # mean aerodynamic cord [m]
    lh_c   = lh / c	          # [ ]
    b      = 15.911	          # wing span [m]
    bh     = 5.791	          # stabiliser span [m]
    A      = b ** 2 / S      # wing aspect ratio [ ]
    Ah     = bh ** 2 / Sh    # stabiliser aspect ratio [ ]
    Vh_V   = 1	          # [ ]
    ih     = -2 * pi / 180   # stabiliser angle of incidence [rad]

    #Airplane inertia:
    KX2    = 0.019 # K_x_squared
    KZ2    = 0.042 # K_z_squared
    KXZ    = 0.002
    KY2    = 1.25 * 1.114 # K_y_squared


class thrust_par:
    fuel_fl = 0.048


class derivatives:
    #Constant:
    def __init__(self):
        self.CXu    = -0.09500
        self.CXa    = +0.47966		# Positive, see FD lecture notes)
        self.CXadot = +0.08330
        self.CXq    = -0.28170
        self.CXde   = -0.03728

        self.CZu    = -0.37616
        self.CZa    = -5.74340
        self.CZadot = -0.00350
        self.CZq    = -5.66290
        self.CZde   = -0.69612

        self.Cm0    = +0.0297
        self.Cmu    = +0.06990
        self.Cmadot = +0.17800
        self.Cmq    = -8.79415
        self.CmTc   = -0.0064

        self.CYb    = -0.7500
        self.CYbdot =  0
        self.CYp    = -0.0304
        self.CYr    = +0.8495
        self.CYda   = -0.0400
        self.CYdr   = +0.2300

        self.Clb    = -0.10260
        self.Clp    = -0.71085
        self.Clr    = +0.23760
        self.Clda   = -0.23088
        self.Cldr   = +0.03440

        self.Cnb    =  +0.1348
        self.Cnbdot =   0
        self.Cnp    =  -0.0602
        self.Cnr    =  -0.2061
        self.Cnda   =  -0.0120
        self.Cndr   =  -0.0939

        temp = vars(self)

        self.key_list = list(temp.keys())
        self.initial_values = list(temp.values())

        self.iterative_par = dict(zip(self.key_list, self.initial_values))




    #Variable:
    def compute_CX0(self, weight, pitch, density, TAS, area):
        return weight * math.sin(pitch) / (0.5 * density * TAS ** 2 * area)

    def compute_CZ0(self, weight, pitch, density, TAS, area):
        return -(weight * math.cos(pitch) / (0.5 * density * TAS ** 2 * area))
