
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from analysis.mass_balance import mass_balance

def test_mass_balance():
    unit = mass_balance()
    print(f"CmTc: {unit.CmTc}")
    print(f"Ws: {unit.Ws}")
    print(f"mfs: {unit.mfs}")
    print(f"gamma: {unit.gamma}")
    print(f"BEW: {unit.BEW}")
    print(f"x_BEM: {unit.x_BEM}")
    print(f"moment_BEW: {unit.moment_BEW}")
    print(f"m_fuel: {unit.m_fuel}")
    print(f"x_fuel: {unit.x_fuel}")
    print(f"moment_fuel: {unit.moment_fuel}")
    print(f"x0: {unit.x0}")
    print(f"x1: {unit.x1}")
    print(f"x2: {unit.x2}")
    print(f"x3: {unit.x3}")
    print(f"xco: {unit.xco}")
    print(f"x_list: {unit.x_list}")
    print(f"n_people: {unit.n_people}")


test_mass_balance()
