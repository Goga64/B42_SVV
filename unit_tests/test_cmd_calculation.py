
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import numpy as np

from analysis.cmd_calculation import ext_par_cmdelta, calc_xcg


def test_ext_par_cmdelta():
    info = {
        'hp': [4000, 2000],
        'IAS': [125, 105],
        'TAT': [130, 110],
        'F. used': [0.4, 0.8],
        'de': [0.03, 0.02]
    }
    m0 = 60000
    hand_calculations = [3000, 115, 120, 0.6, 59999.4]   # hp, IAS, TAT and Fused averages, mfinal

    hp_avg, V_avg, TAT_avg, m_f_used_avg, mass_final, de1, de2 = ext_par_cmdelta(info, m0)
    print(f"hp_avg: {hp_avg}")
    print(f"hand calculation {hand_calculations[0]}, discrepancy {abs(hand_calculations[0]-hp_avg)}")
    print(f"V_avg: {V_avg}")
    print(f"hand calculation {hand_calculations[1]}, discrepancy {abs(hand_calculations[1]-V_avg)}")
    print(f"TAT_avg: {TAT_avg}")
    print(f"hand calculation {hand_calculations[2]}, discrepancy {abs(hand_calculations[2]-TAT_avg)}")
    print(f"m_f_used_avg: {m_f_used_avg}")
    print(f"hand calculation {hand_calculations[3]}, discrepancy {abs(hand_calculations[3]-m_f_used_avg)}")
    print(f"mass_final: {mass_final}")
    print(f"hand calculation {hand_calculations[4]}, discrepancy {abs(hand_calculations[4]-mass_final)}")
    print(f"de1: {de1}")
    print(f"de2: {de2}")



def test_calc_xcg():
    pass



# test_ext_par_cmdelta()
# test_calc_xcg()
