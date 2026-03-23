
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from objects.parameters import universal_const, geo_const, thrust_par, derivatives


def test_universal_const():
    u = universal_const()
    print(f"rho0: {u.rho0}")
    print(f"lam: {u.lam}")
    print(f"Temp0: {u.Temp0}")
    print(f"R: {u.R}")
    print(f"g: {u.g}")

    h = [0, 1000, 3000, 5000, 7000, 1e9]
    rho_hand_calculation = ["1.225", "1.111596", "0.909004", "0.735953", "0.589314", "inf"]
    for i in range(len(h)):
        rho_pred = u.rho(h[i])
        print(f"rho at {h[i]} = {rho_pred}")
        print(f"hand calculation: {rho_hand_calculation[i]}")
        print(f"discrepancy: {abs(rho_pred - float(rho_hand_calculation[i]))}")


def test_geo_const():
    unit = geo_const()

    # [Sh, Sh_S, lh, lh_c, A, Ah, ih, KY2]
    hand_calculations = [6.0, 0.2, 4.23728, 2.060032087, 8.438664033, 5.589280167, -0.034906585, 1.3925]

    print(f"S: {unit.S}")
    print(f"Sh: {unit.Sh}")
    print(f"hand: {hand_calculations[0]}, discrepancy {abs(unit.Sh - hand_calculations[0])}")
    print(f"Sh_S: {unit.Sh_S}")
    print(f"hand: {hand_calculations[1]}, discrepancy {abs(unit.Sh_S - hand_calculations[1])}")
    print(f"lh: {unit.lh}")
    print(f"hand: {hand_calculations[2]}, discrepancy {abs(unit.lh - hand_calculations[2])}")
    print(f"c: {unit.c}")
    print(f"lh_c: {unit.lh_c}")
    print(f"hand: {hand_calculations[3]}, discrepancy {abs(unit.lh_c - hand_calculations[3])}")
    print(f"b: {unit.b}")
    print(f"bh: {unit.bh}")
    print(f"A: {unit.A}")
    print(f"hand: {hand_calculations[4]}, discrepancy {abs(unit.A - hand_calculations[4])}")
    print(f"Ah: {unit.Ah}")
    print(f"hand: {hand_calculations[5]}, discrepancy {abs(unit.Ah - hand_calculations[5])}")
    print(f"Vh_V: {unit.Vh_V}")
    print(f"ih: {unit.ih}")
    print(f"hand: {hand_calculations[6]}, discrepancy {abs(unit.ih - hand_calculations[6])}")
    print(f"KX2: {unit.KX2}")
    print(f"KZ2: {unit.KZ2}")
    print(f"KXZ: {unit.KXZ}")
    print(f"KY2: {unit.KY2}")
    print(f"hand: {hand_calculations[7]}, discrepancy {abs(unit.KY2 - hand_calculations[7])}")


def test_thrust_par():
    unit = thrust_par()
    print(f"fuel_fl: {unit.fuel_fl}")


def test_derivatives():
    unit = derivatives()
    print(unit.iterative_par)

    weight = 60000
    pitch = 4
    density = 1.225
    TAS = 120
    area = 30
    hand_calculations = [0.015817794, -0.226205]
    pred = [unit.compute_CX0(weight, pitch, density, TAS, area), unit.compute_CZ0(weight, pitch, density, TAS, area)]
    print(f"CX0: {pred[0]}")
    print(f"hand {hand_calculations[0]}, discrepancy {abs(pred[0] - hand_calculations[0])}")
    print(f"CZ0: {pred[1]}")
    print(f"hand {hand_calculations[1]}, discrepancy {abs(pred[1] - hand_calculations[1])}")


# test_universal_const()
# test_geo_const()
# test_thrust_par()
test_derivatives()      # catches error: pitch not consistent as deg/rad
