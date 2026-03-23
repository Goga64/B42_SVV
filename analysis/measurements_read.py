import pandas as pd
import numpy as np
from pymatreader import read_mat


'''
This file reads the measurements from .xlsx and .mat files provided for the assignment.
    1. read_meas_stationary1    -->     read stationary measurements series1
    2. read_meas_stationary2    -->     read stationary measurements series2
    3. read_meas_elevator_trim  -->     read stationary measurements for elevator trim curve
    4. read_meas_dynamic        -->     read dynamic measurements
    5. read_meas_mnb            -->     read mass and balance measurements
'''

#----------------------------------------------Series 1 Measurements-----------------------------------------------------------------
def read_meas_stationary1(file):
    s1 = pd.read_excel(file, sheet_name="averaging", header=None, usecols = list(range(0,9)))      # Read only first 8 columns
    s1.columns = s1.iloc[1]                                                                             # Assign column labels
    s1 = s1.dropna(subset=[s1.columns[2]])                                                              # Drop "empty" rows (check 3rd cell)
    s1 = s1.drop(index = 1)                                                                             # Drop redundant 1st row
    s1 = s1.drop(s1.columns[0], axis = 1)                                                               # Drop 1st column
    s1 = s1.iloc[6::7].reset_index(drop=True)                                                           # Use average values from tests as data points
    s1_units = ['ft', 'kts', 'deg C', 'lbs/hr', 'lbs/hr', 'lbs', 'deg', 'sec']                          # Define units for conversion (they're not defined in this sheet)                   

    return s1, s1_units

#---------------------------------------------Series 2 Measurements--------------------------------------------------------------------
def read_meas_stationary2(file):
    s2 = pd.read_excel(file, sheet_name="averaging", header=None, usecols = list(range(10,22)))    # read Series 2 columns
    s2.columns = s2.iloc[1]                                                                             # Assign col labels
    s2 = s2.drop(s2.columns[0], axis = 1).reset_index(drop=True)                                        # Drop 1st column

    rows1 = np.arange(9,65,8)
    rows2 = [65,73]
    rows = np.concatenate([rows1, rows2])

    s2 = s2.iloc[rows].reset_index(drop=True)

    s2_units = ['deg', 'kts', 'ft', 'deg C', 'N', 'lbs', 'deg', 'lbs/hr', 'lbs/hr', 'deg', 'hh:mm:ss']
    
    return s2, s2_units

#-----------------------------------------------------Elevator Trim Curve Measurements---------------------------------------------------------
def read_meas_elevator_trim(file):
    try:
        em = pd.read_excel(file, sheet_name="Sheet1", header=None, usecols = list(range(3,13)))    # Read the elevator trim measurements table
    except ValueError:
        em = pd.read_excel(file, sheet_name="Overview", header=None, usecols = list(range(3,13)))    # Read the elevator trim measurements table
   
    em.columns = em.iloc[55]                                                                        # Define column headers
    em_units = em.iloc[56]                                                                          # Define units
    em = em.iloc[58:65].reset_index(drop=True)                                                      # Limit to rows of interest


    # The units for this table are specified as [xxx] instead of xxx for other files. We need to convert that for the scaling function
    char1 = ']'
    char2 = '['

    # Remove the square brackets from units
    for j, ele in enumerate(em_units):
            em_units.iloc[j] = ele.replace(char1, '')
    for k, ele in enumerate(em_units):
            em_units.iloc[k] = ele.replace(char2, '')

    return em, em_units

#-----------------------------------------------------------Dynamic Measurements----------------------------------------------------------------

'''
The original data file for dynamic measurements is a .mat file, so I needed a different approach here. Also, it is a set of dictionaries within a
dictionary, so extracting the information requires some extra steps.
'''

def read_meas_dynamic(file_mat, file_txt):
    dyn_contents = read_mat(file_mat)
    fl_data = dyn_contents['flightdata']                            # Isolate the dictionary which contains actual flight data

    keys = open(file_txt, 'r')                                      # Get the parameter list from Dspace Parameters.txt
    lines = keys.read().splitlines()
    keys.close()


    flight_data = pd.DataFrame()                                    # Create an empty dataframe for the flight data... 
    flight_units = []                                               # ... as well as separate lists for units and descriptions
    flight_descr = []

    for line in lines:                                              # Loop over each parameter. Get the values, unit and description
        data = fl_data[line]['data']
        unit = fl_data[line]['units']
        descr = fl_data[line]['description']

        flight_data.insert(len(flight_data.columns), line, data)    # Insert the new column after all existing ones (to keep order)
        flight_units.append(unit)                                   # Append unit and description to their respective lists
        flight_descr.append(descr)
        

    return flight_data, flight_units, flight_descr

#--------------------------------------------------------Mass & Balance Sheet----------------------------------------------------------------
'''
In this part of the file, we're trying to extract information from the mass & balance sheet and general seating information on the AC'''

# Define a function that reads the positions of all people on board and their mass
def read_meas_mnb(file, positions):
    # First, we extract the masses of all people on board (mb)
    try:
        mb = pd.read_excel(file, sheet_name="Sheet1", header=None, usecols = list(range(7,8)))
    except ValueError:
        mb = pd.read_excel(file, sheet_name='Overview', header=None, usecols = list(range(7,8)))

    mb = mb.dropna().reset_index(drop = True)
    mb = mb.drop(index = 0).reset_index(drop=True)
    mb = mb.iloc[0:9]     

    # Now, we create a dataframe with masses and positions of people on board (mnb_data)
    mnb_data = pd.DataFrame()
    mnb_data.insert(0, 'x_position', positions)
    mnb_data.insert(1, 'mass [kg]', mb)
    mnb_data_units = ['in', 'kg']
    
    return mnb_data, mnb_data_units

# Now define a function that reads the measurements related to xcg position from the .xlsx file and tells us who shifted where

def read_meas_xcg(file):
    try:
        df = pd.read_excel(file, sheet_name="Sheet1", header=None, usecols = list(range(3,13)))
    except ValueError:
        df = pd.read_excel(file, sheet_name='Overview', header=None, usecols = list(range(3,13)))

    df = df.iloc[72::].reset_index(drop = True)
    df.columns = df.iloc[0]                                                                            # Define column headers
    df_units = df.iloc[1].values.flatten().tolist()                                                    # Define a list of units
    df = df.iloc[2:4].reset_index(drop = True)
    
    # Again, we have to get rid of the square brackets
    char1 = ']'
    char2 = '['

    for j, ele in enumerate(df_units):
        df_units[j] = ele.replace(char1, '')
    for k, ele in enumerate(df_units):
        df_units[k] = ele.replace(char2, '')
    
    return df, df_units

# Lastly, we want a function that tells us who moved from where to where (this is optional, I did it for fun to play with the position)
# In reality, it's always 3R moving to cockpit as far as I'm aware

def read_position_shift(file, positions):
    try:
        xrow = pd.read_excel(file, sheet_name="Sheet1", header=None, usecols = list(range(0,9)))
    
    except ValueError:
        xrow = pd.read_excel(file, sheet_name= 'Overview', header=None, usecols = list(range(0,9)))

    m_fuel_block = xrow.iloc[17][3]                                                                 # Block fuel mass [kg]
    xp1 = str(xrow.iloc[70][2])                                                                     # Initial position of the moving passenger
    xp2 = str(xrow.iloc[70][7])                                                                     # Final position of the moving passenger

    # Here, we convert the positions into actual numbers
    if '1' in xp1:                                                             # If passenger moves from the 1st row, initial coordinate is x1
        xp1 = positions[3]
    elif '2' in xp1:                                                           # If passenger moves from the 2nd row, initial coordinate is x2
        xp1 = positions[5]
    elif '3' in xp1:                                                           # If passenger moves from the 3rd row, initial coordinate is x3
        xp1 = positions[7]
    else:
        print('The person who moved is not a passenger!')

    # Now, we determine the final position based on the row number or cockpit.
    if '1' in xp2:                                                              
        xp2 = positions[3]
    elif '2' in xp2:
        xp2 = positions[5]
    elif '3' in xp2:
        xp2 = positions[7]
    elif 'Cockpit' in xp2:
        xp2 = positions[0]
    else:
        print('Oh no! The passenger must have jumped out of the plane!')

    x_list = [xp1, xp2]
    x_list_units = ['in', 'in']
    m_fuel_block_units = ['lbs']
    
    return m_fuel_block, m_fuel_block_units, x_list, x_list_units
