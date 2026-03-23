
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from analysis.thrust_calculation import calc_thrust
from objects.parameters import universal_const
import numpy as np


def test_calc_thrust(inputs, random_deviation):
    print(f"T_st: {inputs[0]}")
    print(f"mfl: {inputs[1]}")
    print(f"mfr: {inputs[2]}")
    print(f"hp: {inputs[3]}")
    print(f"M: {inputs[4]}")
    print(f"dT: {random_deviation}")

    # dT and T_ISA
    T_ISA = np.zeros_like(inputs[0])
    for j in range(len(T_ISA)):
        T_ISA[j] = universal_const.Temp0 + universal_const.lam*inputs[3][j]                        # Get the ISA temperature for each altitude point
    dT = inputs[0] - T_ISA
    print(f"dT deviation: {dT - random_deviation}")

    # Thr_total
    Thr_total = calc_thrust(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4])
    print(f"Thr_total: {Thr_total}")


size = 20
c_hp = np.arange(0, 10000, 500)
random_deviation = np.random.normal(0, 1, size)
c_T_st = universal_const.Temp0*np.ones(size) + universal_const.lam*c_hp + random_deviation
c_mfl = 0.048*np.ones(size)
c_mfr = 0.048*np.ones(size)
c_M = 0.5*np.ones(size)
inputs_calc_thrust = [c_T_st, c_mfl, c_mfr, c_hp, c_M]
test_calc_thrust(inputs_calc_thrust, random_deviation)
