Hello! This is a file I wrote to explain what is currently happening in the "analysis" folder!
This file was last updated on: 16.03.2026

Right now, we have the following files:
    1.  aerodynamic_coefficients.py
    2.  measurements_read.py
    3.  measurements_scale.py
    4.  measurements_reduction.py
    5.  cmd_calculation.py
    6.  elevator_trim_curve.py
    7.  cmalpha_calculation.py
    8.  drag_polar.py
    9.  thrust_calculation.py
    10. coefs_calculation.py

Let's see what they're all about!

1. aerodynamic_coefficients.py
    What does it do?               Calculates aerodynamic parameters + estimates coefficients
    What can I find there?         functions for: static temperature, TAS, dynamic pressure 
                                                  CL, CL0, alpha0, CL_alpha,
                                                  CD, CD0, e, CL2_CD, 
                                                  Cmdelta, Cmalpha

    Notes:  11/03/2026 According to Andrzej, the linear regression isn't working. Urgent fix!
            12/03/2026 According to Andrzej, the linear regression has been fixed by him.
            15/03/2026 I fixed the linear regression that was not yet fixed by Andrzej. It seems to work, but I'm still unsure if
                       I got the order of parameters right (have to double-check).



2. measurements_read.py
    What does it do?                Reads the .xlsx for stationary measurements and .mat for dynamic measurements.
    What can I find there?          functions for:  reading stationary measurements 1 and 2
                                                    reading dynamic measurements
                                                    reading elevator trim curve measurements
                                                    reading mass and balance data
                                        
                                    series1         --> dataframe with results from stationary measurement 1
                                    series1_units   --> list of units corresponding to series1 (NON-SI!)
                                    series2         --> dataframe with results from stationary measurement 2
                                    series2_units   --> list of units corresponding to series2 (NON-SI!)
                                    flight_data     --> dataframe with results of dynamic measurements
                                    flight_units    --> list of units corresponding to flight_data (NON-SI!)
                                    flight_descr    --> list of descriptions corresponding to flight_data
                                    em              --> dataframe with results from stationary measurements for the elevator trim curve
                                    em_units        --> list of units corresponding to em (NON-SI!)
                                    mass_balance    --> a class containing basic information on mass and balance
                                            |        
                                            |---> mnb_data  --> a dataframe with positions of people on board and their masses
                                            |---> x_list    --> a list of positions of all people on board
                                            |---> BEW, x_BEW, m_fuel, x_m_fuel etc.
                                            |---> xcg_data -->  data on the two datapoints used for delta_xcg (one before the passenger
                                            |                    moves and one after). Conains hp, IAS, alpha, de, detr, Fe, FFl, FFr, F.used, TAT
                                            |---> xcg_units --> a list of units for xcg_data (for unit conversion)
                                            |--->m_fuel_block, xp1, xp2  --> block fuel mass and positions of the moving passenger derived from the .xlsx sheet
                                            
    Notes:  11/03/2026  I need to look again at stationary measurements (will do once we have our measurements).
                        I still have to figure out where to get the xcg shift from for Cmdelta.
            13/03/2026  I know where to get the xcg shift. I just need to confirm the timestamp with the TAs and get the
                        weight array from Matheus.
            14/03/2026  Actually, I now noticed that they provide the mass of fuel that has been used. I may not need Matheus'
                        weight array for this after all (Indeed, it looks like this works perfectly fine. I still need the weight
                        for the trim curve, though).
            16/03/2026  I changed the file so that now most of the reading is done in separate functions to make verification easier.
                        Also, I merged xcg_shift and mass_balance into a single class because even I was getting confused about what data was where.



3. measurements_scale.py
    What does it do?                Converts all measurements to SI units!
    What can I find there?          definition of conversion factors
                                    function for conversion of measurement and units into SI
                                    series1_c       --> scaled stationary measurements, series 1
                                    series1_units_c --> scaled units for series1_c
                                    series2_c       --> scaled stationary measurements, series 2
                                    series2_units_c --> scaled units for series2_c
                                    flight_data_c   --> scaled dynamic measurements
                                    units_c         --> list of SI units corresponding to flight_data_c
                                    em_c            --> scaled stationary measurements for elevator trim curve
                                    em_units        --> list of SI units corresponding to em_c
                                    mnb_data_c      --> a class for scaled mnb_data + xcg_data and xp1, xp2
                                            |
                                            |--->   BEW_c, x_BEW_c, moment_fuel_c, m_fuel_c, x_fuel_c
                                            |--->   xcg_data_c, xcg_units_c --> scaled measurements for xcg shift
                                            |--->   x1, x2 --> positions of the moving passenger [m]
                                            |--->   mass_initial --> initial mass of the AC + passengers

    Notes:  11/03/2026 Some of the units/measurements are not converted (check descriptions in the file for more info).
                        I need a second pair of eyes to verify the conversion.
            16/03/2026  I modified the file so that now stationary, dynamic and elevator trim measurements are all converted with
                        a single function (this will probably make things easier to verify).



4. measurements_reduction.py
    What does it do?                Defines the reduced parameters that we can use to get the trim curve and stick force curve.
    What can I find there?          functions for thermodynamics:   static pressure 
                                                                    Mach number 
                                                                    Static temperature
                                                                    density (also defined in parameters)
                                                                    equivalent velocity

                                    functions for reduced params:   reduced equivalent velocity
                                                                    reduced stick force
                                                                    reduced elevator deflection

    Notes:  11/03/2026  For reduced elevator deflection, we need to look into the Tc, Tcs coefficients.
            13/03/2026  I think Andrzej may be able to get them from thrust.py, but I have to ask him.
            15/03/2026  I think I have the Tc, Tcs now from the .xlsx file.
            16/03/2026  I found an actually critical bug in how the Mach number was calculated - now most of my values in other
                        files seem to make sense!





5. cmd_calculation.py
    What does it do?                Calculates the Cm_delta (elevator effectiveness) based on xcg shift, change in de, weight
                                    and dynamic pressure.
    What can I find there?          xcg1, xcg2 --> initial and final xcg positions
                                    Cmdelta
    
    Notes:  14/03/2026  The current version is almost complete, all I need is the weight of the AC after the fuel burns and we
                        should be good!
                        I found the mass of fuel burned, and I'm getting reasonable results (-1.7 rad^-1). Looks good.
            16/03/2026  After adjusting the thrust and Mach number functions, we're getting -1.36 rad^-1. That's a little more reasonable,
                        but I want to compare with Alex's team.
                        I just found a non-critical bug with the mass for initial x_cg. We now have -1.24 rad^-1, which is even more reasonable!




6. elevator_trim_curve.py
    What does it do?                Calculates the reduced de and velocity to get the de/dalpha coefficient (needed for Cmalpha).
                                    Also, it provides the reduced stick force for the Fe_r-Ve_r plot.
    What can I find there?          functions for:  de/dalpha, de_r-Ve_r slope, Fe_r-Ve_r slope
                                    Ve_r        -->  reduced equivalent velocity
                                    de_r        -->  reduced elevation angle
                                    Fe_r        -->  reduced stick force
                                    trim        -->  the de/dalpha coefficient derived from de_r (linear regression)
                                    force_coef  -->  the Fe_r - Ve_r coefficient (linear regression)
    
    Notes:  14/03/2026  I still need the Tcs and weight array to make the calculations complete.
                        I also need to ask Georgii to construct the plots if he has the time.
            16/03/2025  I think that I fixed the way de/dalpha is calculated, it is now negative and has a reasonable value, but I'm not
                        100% confident that it's correct. Need a second pair of eyes to check.



7. cmalpha_calculation.py
    What does it do?                Calculates Cmalpha based on dalpha/de and Cm_delta from files 5. and 6.
    What can I find there?          Cmalpha

    Notes:  14/03/2026  The value for now is incorrect based on missing inputs for da/de (weight!!!).
            16/03/2026  The value is no longer 100% incorrect, but has not yet been verified.
                        The value has been adjusted and is now more reliable, but I'm still not 100% sold on it.



8. drag_polar.py
    What does it do?                Calculates aerodynamic coefficients (CL, CD, CL_alpha etc.) based on stationary measurements.
    What can I find there?          Cl, Cl0, alpha0, Cd, Cd0, e, Cl_alpha

    Notes:  15/03/2026  I added my own contribution to the file, in order Andrzej or Georgii need the coefficients for their part of work.
            16/03/2025  I left the file because I realised I was messing up Andrzej's work (sorry!)



9. thrust_calculation.py
    What does it do?                Calculates the thrust based on fuel flow, altitude, Mach number and static temperature.
    What can I find there?          function to calculate thrust for both engines and sum it to get the total thrust

    Notes:  15/03/2026 This didn't really need to be a separate file, but since I needed the thrust calculation for both elevator_trim_curve.py and drag_polar.py,
                        I decided that creating thrust_calculation.py would make it easier to keep track on where to find this function.
                        I still need to estimate the weight for the reduced elevator deflection and reduced stick force!!!
            16/03/2026  Found a sign bug and fixed it.



10. coefs_calculation.py
    What does it do?                Calculates the aerodynamic coefficients based on functions defined in aerodynamic_coefficients.py, stationary measurements
                                    (series 1), and mass and balance data.
    What can I find there?          Values for: Cl, Cl_alpha, Cl0, alpha0, Cl^2_Cd, Cd, Cd0, e

    Notes:  16/03/2026  I created this file to not mess up Andrzej's work in drag_polar.py.
                        So far, the values seem alright, but I need to confirm with Alex's team if they're correct because I'm not 100% confident.