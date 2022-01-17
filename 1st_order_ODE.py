#! /usr/local/bin/python3.4

# 1st_order_ODE.py
# Create functions that will solve a first order ODE using various numerical methods
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


def euler(ode, interval, step_size, initial_value):
    """Solve for y(x), given ODE dy/dx = f(x) and boundary conditions, over the values in interval"""
    #initialize variables for for loop
    n = 0                                                       # steps
    eu_values = []                                              # list of y values for eu    
    for n in interval:
        eu_values.append(initial_value)                         # append inital value
        y_n = initial_value + step_size * ode(n)                # calculate y_n
        initial_value = y_n                                     # update initial value
        n =+ 1                                                  # update step count
    return eu_values   
#print(eu_values)

def rk(ode, interval, step_size, initial_value):
    """Solve for y(x), given ODE dy/dx = f(x) and boundary conditions, over the values in interval"""
    #initialize variables
    n = 0                                                       # steps
    rk_values = []                                              # list of y values for rk
    for n in interval:
        #calculate slopes and weighted averages
        k_n = ode(n)                                            # slope at n
        k_half = ode(n + (step_size/2))                         # slope at halfway point
        k_avg = (0 * k_n)+ (1 * k_half)                         # weighted average of slopes (for second order)
        #calculate y value using weighted slope average and update count
        rk_values.append(initial_value)                         # append initial value
        y_n  = initial_value + step_size * k_avg                # calculate y_n 
        n =+ 1                                                  # update step count
        initial_value = y_n                                     # update initial value
    return rk_values
#print(rk_values)