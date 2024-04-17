import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from math import pi as pi

from compensator import Type_1_Compensator
from compensator import Type_2_Compensator
from compensator import Type_3_Compensator
from buck import Buck
import frequency_analysis

#-----------------------------------------------------------------
# Path Definition
#-----------------------------------------------------------------
directory = 'C:/Y2024/Automated_circuit_design/models/'
#-----------------------------------------------------------------
# Circuit Definition
#-----------------------------------------------------------------
circuit = Buck(supply_voltage=20, output_voltage=5,DI=0.1, op_pos=15, op_neg=-15, L=0.000056, c = 0.000500, ESR=1, r=1, f=10000)
circuit.update_ripple_current()
frequency_analysis.bode_plot(circuit)
#-----------------------------------------------------------------
# Compensator Definition
#-----------------------------------------------------------------
compensator_type = 3
if(compensator_type == 1):
    comp = Type_1_Compensator()
    comp.update_frequencies(0.1, 100)

elif(compensator_type == 2):
    comp = Type_2_Compensator()
    comp.update_frequencies(0.1,20000,1000, 100)

elif(compensator_type == 3):
    comp = Type_3_Compensator()
    comp.update_frequencies(0.1,20000,50000,200,1000, 100)
#-----------------------------------------------------------------
# Frequency Analysis
#-----------------------------------------------------------------
frequency_analysis.bode_plot(circuit, comp)
LTspice_analysis



