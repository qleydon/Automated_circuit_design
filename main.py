import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from math import pi as pi

from compensator import Type_2_Compensator
from compensator import Type_3_Compensator
from buck import Buck
import frequency_analysis

#-----------------------------------------------------------------
# Circuit Definition
#-----------------------------------------------------------------
circuit = Buck(supply_voltage=20, output_voltage=5,DI=0.1, op_pos=15, op_neg=-15, L=0.000056, c = 0.000500, ESR=1, r=1, f=10000)
circuit.update_ripple_current()
#-----------------------------------------------------------------
# Compensator Definition
#-----------------------------------------------------------------
comp_2 = Type_2_Compensator()
comp_2.update_frequencies(0.1,20000,1000, 100)

comp_3 = Type_3_Compensator()
comp_3.update_frequencies(0.1,20000,50000,200,1000, 100)
#-----------------------------------------------------------------
# Frequency Analysis
#-----------------------------------------------------------------
frequency_analysis.bode_plot(circuit, comp_2, (0.01, 1000000))