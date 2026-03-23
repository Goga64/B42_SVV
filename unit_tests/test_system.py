import sys, os
import pytest
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from objects.system import dyn_system_sym
from objects.parameters import geo_const
from analysis.measurements_read import read_meas_dynamic

W = 60500
theta = 2
rho = 1.225
TAS = 200
Cmde = 0.4
Cma = -0.5

class derivatives:
    #Constant:
    def __init__(self):
        self.CXu    = -0.09500
        self.CXa    = +0.47966	
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
    
d = derivatives()


dyn_syst = dyn_system_sym(W,theta,rho,TAS,Cmde,Cma,d.iterative_par)

def test_muc():
    muc_expected = dyn_syst.muc
    assert muc_expected == pytest.approx(81.58603844)













pytest.main()