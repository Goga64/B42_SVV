class mass_balance:
    # General constants
    CmTc = -0.0064    # [-]
    Ws = 60500        # [N]
    mfs = 0.048       # [kg/s]
    gamma = 1.4       # [-]

    # All measurements in lbs, in or lbs*in
    BEW = 9197.0                # Basic Empty Weight
    x_BEM = 291.28              # moment arm of BEW
    moment_BEW = 2678893.5      # moment of BEW

    m_fuel = 2675               # Fuel on board
    x_fuel = 285.18             # arm of fuel
    moment_fuel = 762856.5      # moment of fuel

    x0 = 131                   # pilot & 1st officer
    x1 = 214                   # 1st row of passengers
    x2 = 251                   # 2nd row of passengers
    x3 = 288                   # 3rd row of passengers
    xco = 170                  # coordinator

    x_list = [x0, x0, xco, x1, x1, x2, x2, x3, x3]
    n_people = len(x_list)