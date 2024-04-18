import sys
import matplotlib.pyplot as plt
import os

from os.path import join as pathjoin
import numpy as np
from numpy import abs as mag, angle
from PyLTSpice import RawRead

from PyLTSpice import SimRunner
from PyLTSpice import SpiceEditor
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from math import pi as pi

import compensator
from compensator import Type_1_Compensator
from compensator import Type_2_Compensator
from compensator import Type_3_Compensator
from buck import Buck
import frequency_analysis
from LTspice_analysis import Spice

#-----------------------------------------------------------------
# Path Definition
#-----------------------------------------------------------------
directory = 'C:/Y2024/Automated_circuit_design/models/'
spice = Spice(directory)
#-----------------------------------------------------------------
# Circuit Definition
#-----------------------------------------------------------------
circuit = Buck(supply_voltage=20, output_voltage=5,DI=0.1, op_pos=15, op_neg=-15, L=0.000056, c = 0.000500, ESR=1, r=1, f=10000)
circuit.update_ripple_current()
frequency_analysis.bode_plot(circuit)
spice.update_circuit(circuit)
#-----------------------------------------------------------------
# Compensator Definition
#-----------------------------------------------------------------
while True:
    print("compensators: \nType 1: 1 pole, 0 zeros\nType 2: 2 poles, 1 zero \nType 3: 3 pole, 2 zeros")
    compensator_type = 0
    compensator_type = int(input("compensator type: "))
    #compensator_type = 3
    if compensator_type in (1,2,3):
        break

while True:
    if(compensator_type == 1):
        comp = Type_1_Compensator()
        #fp0 = float(input("pole 0 frequency: "))
        #r1 = float(input("r1 resistance: "))
        #comp.update_frequencies(fp0, r1)
        comp.update_frequencies(0.1, 100)

    elif(compensator_type == 2):
        comp = Type_2_Compensator()
        '''fp0 = float(input("pole 0 frequency: "))
        fp1 = float(input("pole 1 frequency: "))
        fz1 = float(input("zero 1 frequency: "))
        r1 = float(input("r1 resistance: "))
        comp.update_frequencies(fp0,fp1, fz1, r1)'''
        comp.update_frequencies(0.1,20000,1000, 100)

    elif(compensator_type == 3):
        comp = Type_3_Compensator()
        '''fp0 = float(input("pole 0 frequency: "))
        fp1 = float(input("pole 1 frequency: "))
        fp2 = float(input("pole 2 frequency: "))
        fz1 = float(input("zero 1 frequency: "))
        fz2 = float(input("zero 2 frequency: "))
        r1 = float(input("r1 resistance: "))
        comp.update_frequencies(fp0,fp1, fp2, fz1, fz2, r1)'''
        comp.update_frequencies(0.1,20000,50000,200,1000, 100)

    #-----------------------------------------------------------------
    # Frequency Analysis
    #-----------------------------------------------------------------
    frequency_analysis.bode_plot(circuit, comp)

    sim = input("Simulate compensator AC in LTspice? (Y/n)")
    if sim in ("y", "Y", "yes", "Yes", "YES"):
        spice.update_compensator(comp) # automaticly plots
    
    #-----------------------------------------------------------------
    # Transient analysis
    #-----------------------------------------------------------------
    sim_t = input("Simulate Transient analysis in LTspice? (Y/n)")
    if sim_t in ("y", "Y", "yes", "Yes", "YES"):
        spice.update_compensator(comp, False)
        print("current voltage command:", spice.voltage_cmd)
        choice = input("Change voltage command? (Y/n)")
        if choice in ("y", "Y", "yes", "Yes", "YES"):
            voltage_cmd = input("voltage command: ")
        else: 
            voltage_cmd = None
        
        print("current run time:", spice.runtime)
        choice = input("Change run time? (Y/n)")
        if choice in ("y", "Y", "yes", "Yes", "YES"):
            runtime = input("run time: ")
        else: 
            runtime = None
        
        spice.update_transient_settings(voltage_cmd=voltage_cmd, runtime=runtime)
        spice.run_transient()




    c_comp = input("Change compensator? (Y/n)")
    if c_comp in ("y", "Y", "yes", "Yes", "YES"):
        c_type = input("Change compensator type? (Y/n)")
        if c_comp in ("y", "Y", "yes", "Yes", "YES"):
            print("compensators: \nType 1: 1 pole, 0 zeros\nType 2: 2 poles, 1 zero \nType 3: 3 pole, 2 zeros")
            compensator_type = input("compensator type: ")

    else:
        break

update_model = input("save netlist file? (Y/n)")
if update_model in ("y", "Y", "yes", "Yes", "YES"):
    spice.update_compensator(comp, False) # no plot
    file_name = input("enter file name: ") # extension will be handled in function call
    






