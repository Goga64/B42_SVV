import numpy as np
import pandas as pd

'''
This file converts units from non-SI to SI for the stationary measurements, dynamic measurements, elevator trim curve measurements and the
mass and balance data.
    1. convert_measurements     -->     convert data and units for dataframes, dictionaries, lists etc.
    2. convert_mass_balance     -->     convert mass and balance data 
'''

# Conversion factors
Celsius_to_K = 273.15
deg_to_rad = np.pi/180
ft_to_m = 0.3048
ft_min_to_m_s = ft_to_m/60
kts_to_m_s = 1852/3600
lbs_to_kg = 0.45359237
lbs_hr_to_kg_s = lbs_to_kg/3600
g_to_m_s2 = 9.81
psi_to_Pa = 6894.7572932
in_to_m = 0.0254

#-------------------------------------------------------Conversion Function---------------------------------------------------------------------

'''
This function converts the units for all measurements. It was initially implemented for dynamic measurements only, but I wanted to make life a 
little less painful for the verification team. The basic idea behind how it works is as follows:
    1. Take the data (dataframe) and original units (list) as input,
    2. Get the keys of the flight data,
    3. Create an empty list for new (SI) units,
    4. Loop over each key and do the following:
        4a) Check the unit for the given type of data (get it from the unit list),
        4b) Define a suitable conversion factor,
        4c) Define the new (SI) unit
    5. Determine the type of data (dataframe, dictionary, list etc.)
    6. Loop opver the elements and apply conversion factor.

Some notable exceptions to the rule:
    A) Temperature conversion from deg C to K --> instead of multiplication, define factor as 1 and manually add known constant to the value
    B) Units which I did not convert:
        - N        - %        - ddmmyy        - <no units>
        - g        - mach     - []            - sec
        For these, the factor is automatically set as 1 and the parameter is not converted.
'''

def convert_measurements(data, units):
    units_c = []    

    def define_factor(unit):        
        if unit == 'ft/min':
            factor = ft_min_to_m_s
            unit_c = 'm/s'

        elif unit == 'knots' or unit == 'kts':
            factor = kts_to_m_s
            unit_c = 'm/s'
        
        elif unit == 'ft':
            factor = ft_to_m
            unit_c = 'm'

        elif unit == 'in':
            factor = in_to_m
            unit_c = 'm'
        
        elif unit == 'deg/s':
            factor = deg_to_rad
            unit_c = 'rad/s'

        elif unit == 'lbs':
            factor = lbs_to_kg
            unit_c = 'kg'
        
        elif unit == 'deg':
            factor = deg_to_rad
            unit_c = 'rad'
        
        elif unit == 'psi':
            factor = psi_to_Pa
            unit_c = 'Pa'
        
        elif unit == 'lbs/hr':
            factor = lbs_hr_to_kg_s
            unit_c = 'kg/s'
        
        elif unit == 'deg C' or unit == '°C':
            factor = 1
            unit_c = 'K'

        else:
            factor = 1
            unit_c = str(unit)
    
        return unit_c, factor
    
    if isinstance(data, pd.DataFrame):
        for i, col in enumerate(data.columns):
            unit_c, factor = define_factor(units[i])
            units_c.append(unit_c)

            if unit_c == 'K':
                data[col] = data[col] + Celsius_to_K

            elif col != 'time':
                data[col] *= factor
        return data, units_c
    
    elif isinstance(data, dict):
        keys = list(data,keys)

        for i, key in enumerate(keys):
            unit_c, factor = define_factor(str(units[i]))
            units_c.append(unit_c)

            if unit_c == 'K':
                data[key] += Celsius_to_K

            elif key!= 'time':
                data[key] *= factor
        return data, units_c

    elif isinstance(data, list):

        for i in range(len(data)):
            unit_c, factor = define_factor(str(units[i]))

            if unit_c == 'K':
                data[i] += Celsius_to_K
            
            elif unit_c != 'time':
                data[i] *= factor

        return data, units_c

    else:
        unit_c, factor = define_factor(str(units[0]))
        units_c.append(unit_c)

        if unit_c == 'K':
            data += Celsius_to_K

        else:
            data *= factor

        
        return data, units_c


#----------------------------------------------------------------Mass and Balance------------------------------------------------------------
'''
Mass and balance data are not all neatly organised dataframes, and I was on a time crunch when processing them, so there's a separate function
dedicated to them.
'''

def convert_mass_balance(BEM, x_BEM, moment_fuel, m_fuel_block, x_fuel_block, mnb):
    BEM_c = BEM * lbs_to_kg
    x_BEM_c = x_BEM * in_to_m
    moment_fuel_c = moment_fuel * in_to_m * lbs_to_kg
    m_fuel_block_c = m_fuel_block * lbs_to_kg
    x_fuel_block_c = x_fuel_block * in_to_m

    keys = mnb.keys()
    for i in range(len(keys)):
        key = keys[i]
        if str(key) == 'x_position':
            mnb[key] *= in_to_m 

    return BEM_c, x_BEM_c, moment_fuel_c, m_fuel_block_c, x_fuel_block_c, mnb

