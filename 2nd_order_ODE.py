#! /usr/local/bin/python3.4


# firstLast_2nd_order_ODE.py
# Create functions that will solve a second order ODE using various numerical methods
# Use only standard Python, no NumPy

#__/\\\\\\\\\\\\\____/\\\\____________/\\\\__/\\\\\\\\\\\\\\\_______________/\\\\\\\\\\______/\\\\\\\_________/\\\_        
# _\/\\\/////////\\\_\/\\\\\\________/\\\\\\_\/\\\///////////______________/\\\///////\\\___/\\\/////\\\___/\\\\\\\_       
#  _\/\\\_______\/\\\_\/\\\//\\\____/\\\//\\\_\/\\\________________________\///______/\\\___/\\\____\//\\\_\/////\\\_      
#   _\/\\\\\\\\\\\\\\__\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\_______________________/\\\//___\/\\\_____\/\\\_____\/\\\_     
#    _\/\\\/////////\\\_\/\\\__\///\\\/___\/\\\_\/\\\///////_______________________\////\\\__\/\\\_____\/\\\_____\/\\\_    
#     _\/\\\_______\/\\\_\/\\\____\///_____\/\\\_\/\\\_________________________________\//\\\_\/\\\_____\/\\\_____\/\\\_   
#      _\/\\\_______\/\\\_\/\\\_____________\/\\\_\/\\\________________________/\\\______/\\\__\//\\\____/\\\______\/\\\_  
#       _\/\\\\\\\\\\\\\/__\/\\\_____________\/\\\_\/\\\\\\\\\\\\\\\___________\///\\\\\\\\\/____\///\\\\\\\/_______\/\\\_ 
#        _\/////////////____\///______________\///__\///////////////______________\/////////________\///////_________\///_ 


def irange(start, stop, step):
    """ Create a generator to iterate over the interval we wish to solve the ODE on
    """
    while start < stop:
        yield start
        start += step


def euler(ode_u1, ode_u2, interval, step_size, initial_value_u1, initial_value_u2):
    #initialize variables for for loop
    n = 0 # steps
    eu_values_1 = []   # list of y values for ode 1
    eu_values_2 = []   # list of y values for ode 2
    u1 = initial_value_u1 # rename initial value 1
    u2 = initial_value_u2 # rename initial value 2
    for n in interval:
        eu_values_1.append(u1) # append initial value ode 1
        eu_values_2.append(u2) # append initial value ode 2
        y_1 = u1 + step_size * ode_u1(n, u1, u2) # calculate y ode 1
        y_2 = u2 + step_size * ode_u2(n, u1, u2) # calculate y ode 2      
        u1 = y_1 # update initial value ode 1
        u2 = y_2 # update initial value ode 2
        n =+ 1   # update step count
    return eu_values_1, eu_values_2               


def rk(ode_u1, ode_u2, interval, step_size, initial_value_u1, initial_value_u2):
    # INITIALIZE VARIABLES
    n = 0 # points
    rk_values = [] # list of y values for rk ode 2                                               
    u = [initial_value] # rename initial value 1
    for n in interval:
        rk_values_1.append(u1) # append values to list of ode 1
        # CALCULATE ALL FIRST SLOPES
        k_i11 = ode_u1(n, u1, u2) # 1,1,1 slope
        h1 = u + (step_size / 2) * k_i11 # update u1 value to be used in halfway point
        # CALCULATE ALL HALF POINT SLOPES 
        k_half11 = ode_u1(n + (step_size/2), h1, h2) # slope 2, 1, 1
        k_half12 = ode_u2(n + (step_size/2), h1, h2) # slope 2, 1, 2
        
        # WEIGHTED AVERAGE OF ALL SLOPES
        k_avg_11 = (k_i11 + k_half11) / 2 # weighted average of slopes 1, 1, 1 and 2, 1, 1
        k_avg_12 = (k_i12 + k_half12) / 2 # weighted average of slopes 1, 1 ,2 and 2, 1, 2
        # CALCULATE Y VALUE USING WEIGHTED AVERAGES
        y_21 = u1 + step_size * k_avg_11 # calculate y for 2, 1
        y_22 = u2 + step_size * k_avg_12 # calculate y for 2, 2
        u1 = y_21 #update initial value
        u2 = y_22 # update initial value
        n =+ 1 # update step count
    return rk_values_1, rk_values_2               
