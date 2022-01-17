#! /usr/local/bin/python3.4


# firstLast_HH.py
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

#collaborated with Adriana Rotger 
import numpy as np

def vmp_eq_26(step, Vnmh):
    """
    f(step, Vnmh) = dVm/dt

    Parameters
    ----------
    step : scalar
        current time point
    Vnmh : list [vm, n, m, h]
        list of variables in the f function
    Returns
    -------
    f = dvm/dt

    """
    Cm = 1              # membrane current
    Vna = -115          # sodium voltage
    Vk = 12             # potassium voltage
    Vl = -10.613        # leakage voltage
    gna_bar = 120       # sodium conductance (constant)
    gk_bar = 36         # potassium conductance (constant)
    gl_bar = 0.3        # leakage conductance (constant)
    
    """
    enter your code here
    """
    #assign variables from Vnmh list and assume I = 0
    Vm = Vnmh[0]    # membrane voltage
    n = Vnmh[1]     # potassium activation probability
    m = Vnmh[2]     # sodium activation probability
    h = Vnmh[3]     # sodium inactivation probability
    
    """
    Eq 26 => I = Cm * dVm/dt +gk * n^4 * (V-Vk) + gna * m^3 * h *(V-Vna) + gl (V-Vl)
    assuming steady state we can say I = 0
    Solve for dVm/dt = f
    """  
    #Eq 26
    f = (-(gk_bar * n ** 4) * (Vm - Vk) - (gna_bar * m ** 3 * h) * (Vm-Vna) - gl_bar * (Vm - Vl)) / Cm
    
    return f

def np_eq_7(step, Vnmh):
    """

    f(step, Vnmh) = dn/dt

    Parameters
    ----------
    step : scalar
        current time point
    Vnmh : list
        [vm, n, m, h]

    Returns
    -------
    f = dn/dt


    enter your code here
    """
    #assign variables from Vnmh list
    Vm = Vnmh[0]    # membrane voltage
    n = Vnmh[1]     # potassium activation 
    """
    Eq 7  => dn/dt = alpha_n (1 - n) - beta_n * n
    Eq 12 => alpha_n = 0.01 * (Vm + 10)/(e^((Vm+10)/10 - 1))
    Eq 13 => beta_n = 0.125 * e^ (Vm/80)
    """
    alpha_n = 0.01 * (Vm + 10) / (np.exp(((Vm + 10) / 10)) - 1)     #Eq 12
    beta_n = 0.125 * np.exp(Vm / 80)                                #Eq 13
    
    # f = dn/dt
    f = alpha_n *(1 - n) - beta_n * n                               #Eq 7

    return f

def mp_eq_15(step, Vnmh):
    """
    f(step, Vnmh) = dm/dt

    Parameters
    ----------
    step : scalar
        current time point
    values : list
        [vm, n, m, h]

    Returns
    -------
    f = dm/dt

    enter your code here
    """
    #assign variables from Vnmh list
    Vm = Vnmh[0]    # membrane voltage
    m = Vnmh[2]     # sodium activation

    """ 
    Eq 15 => dm/dt = alpha_m * (1-m) - beta_m* m
    Eq 20 => alpha_m = 0.1* (Vm + 25) / (e^((Vm+25)/10 - 1))
    Eq 21 => beta_m = 4 * e ^(Vm / 18)
    """
    
    alpha_m = 0.1* (Vm + 25) / (np.exp(((Vm + 25) / 10)) - 1)   #Eq 20
    beta_m = 4 * np.exp(Vm / 18)                                #Eq 21
    
    # f = dm/dt
    f = alpha_m * (1 - m) - beta_m * m                          #Eq 15
    return f
    
def hp_eq_16(step, Vnmh):
    """
    f(step, Vnmh) = dh/dt

    Parameters
    ----------
    step : scalar
        current time point
    values : list
        [vm, n, m, h]

    Returns
    -------
    f = dh/dt
    
    enter your code here
    """
    #assign variables from Vnmh list
    Vm = Vnmh[0]
    h = Vnmh[3]
    """
    Eq 16 => dh/dt = alpha_h * (1-h) - beta_h * h
    Eq 23 => alpha_h = 0.07 * e^(Vm / 20)
    Eq 24 => beta_h = 1 / (e^((Vm + 30)/ 10 + 1)
    """
    alpha_h = 0.07 * np.exp(Vm / 20)                        #Eq 23
    beta_h = 1 / (np.exp(((Vm + 30)/ 10)) + 1)              #Eq 24
    
    # f = dh/dt
    f = alpha_h * (1 - h) - beta_h * h                      #Eq 16
    return f
