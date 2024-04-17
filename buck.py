import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from math import pi as pi

class Buck:
    def __init__(self, supply_voltage=20, output_voltage=5,DI=0.1, op_pos=15, op_neg=-15, L=0.000056, c = 0.000500, ESR=1, r=1, f=10000):
        self.supply_voltage = supply_voltage
        self.output_voltage = output_voltage
        self.DI = DI
        self.op_pos = op_pos
        self.op_neg = op_neg
        self.L=L
        self.c = c
        self.ESR = ESR
        self.r = r
        self.f = f
        self.D = supply_voltage / output_voltage

    # use if specified DI
    def update_inductor(self):
        self.L = (self.supply_voltage-self.output_voltage) * self.D / (self.DI*self.f)
        return self.L
    
    #use if specified L
    def update_ripple_current(self):
        self.DI = (self.supply_voltage - self.output_voltage) * self.D / (self.f * self.L)
        return self.DI
    
    #calculate capacitor for steady state
    def update_capacitor_SS(self):
        self.c = self.DI / (8*self.f*self.ESR*self.DI) # DV = ESR*DI
        return self.c

    #calculate capacitor for overshoot
    def update_capacitor_overshoot(self, overshoot):
        self.c = self.DI * self.DI * self.L / (2 * self.output_voltage * overshoot)
        return self.c
    
    def update_sys(self):
        self.numerator = [self.r]
        self.denominator = [self.r * self.c * self.L, self.L, self.r]
        self.sys = signal.TransferFunction(self.numerator, self.denominator)
        # Convert transfer function to zeros, poles, and gain form
        zeros, poles, gain = signal.tf2zpk(self.numerator, self.denominator)

        # Print the extracted zeros, poles, and gain
        print("Zeros:", zeros/1000,"k")
        print("Poles:", poles/1000,"k")
        print("Gain:", gain)

    

