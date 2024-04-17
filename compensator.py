import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from math import pi as pi

class Type_1_Compensator:
    def __init__(self):
        self.type = 1

    def update_frequencies(self, fp0,r1):
        self.fp0=fp0
        self.r1=r1
        self.c1 = 1/(2*pi*r1)

    def update_components(self, r1, c1):
        self.r1 = r1
        self.c1 = c1
        self.fp0 = 1/(2*pi*r1*c1)

    def update_sys(self):
        self.numerator = [1,0]
        self.denominator = [self.c1* self.r1]
        self.sys = signal.TransferFunction(self.numerator, self.denominator)

class Type_2_Compensator:
    def __init__(self):
        self.type = 2
    def update_frequencies(self, fp0, fp1, fz1, r1):
        self.fp0=fp0
        self.fp1=fp1
        self.fz1=fz1
        self.r1=r1
        
        self.c1 = 1/(2*pi*r1*fp0)
        self.c3 = fz1 / (2*pi*r1*fp0*fp1)
        self.r2 = fp0 * r1 / fz1

    def update_components(self, r1, r2, c1, c3):
        self.r1 = r1
        self.r2 = r2
        self.c1 = c1
        self.c3 = c3
        self.fp0 = 1/(2*pi*r1*c1)
        self.fp1 = 1/(2*pi*r2*c3)
        self.fz1 = 1/(2*pi*r2*c1)

    def update_sys(self):
        self.numerator = [self.c1 * self.r2, 1]
        self.denominator = [self.r1 * self.c1 * self.c3 * self.r2, (self.c1+ self.c3)*self.r1, 0]
        self.sys = signal.TransferFunction(self.numerator, self.denominator)
        # Convert transfer function to zeros, poles, and gain form
        zeros, poles, gain = signal.tf2zpk(self.numerator, self.denominator)

        # Print the extracted zeros, poles, and gain
        print("Zeros:", zeros/1000,"k")
        print("Poles:", poles/1000,"k")
        print("Gain:", gain)

class Type_3_Compensator:
    def __init__(self):
        self.type = 3

    def update_frequencies(self, fp0, fp1, fp2, fz1, fz2, r1):
        self.fp0=fp0
        self.fp1=fp1
        self.fp2=fp2
        self.fz1=fz1
        self.fz2 = fz2
        self.r1=r1
        
        self.c1 = (fp2-fz2)/(2*pi*r1*fp0*fp2)
        self.c2 = (fp1-fz1)/(2*pi*r1*fp1*fz1)
        self.c3 = (fz2)/(2*pi*r1*fp0*fp2)
        self.r2 = fp0 * fp2 * r1 / ((fp2-fz2)*fz1)
        self.r3 = r1*fz1 / (fp1-fz1)

    def update_components(self, r1, r2,r3, c1, c2, c3):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.fp0 = 1/(2*pi*r1*(c1+c2))
        self.fp1 = 1/(2*pi*r3*c2)
        self.fp2 = 1/(2*pi*r2*(c1*c3/(c1+c3)))
        self.fz1 = 1/(2*pi*(r1+r3)*c2)
        self.fz2 = 1/(2*pi*r2*c1)

    def update_sys(self):
        numerator = [self.c1*self.c2*self.r1*self.r2 + self.c1*self.c2*self.r2 * self.r3, self.c2*(self.r1+self.r2) + self.c1*self.r2, 1]
        #denominator = [self.c1 * self.c2 * self.c3 * self.r1* self.r2 * self.r3, self.r1*self.c1*(self.c2*self.r3 + self.c3 * self.r2 + 1), 0]
        a = self.r1*self.c1
        b = self.c2*self.r3
        c = self.r2*self.c3
        denominator = [a*b*c, a*b+a*c, a, 0]
        self.sys = signal.TransferFunction(numerator, denominator)
        # Convert transfer function to zeros, poles, and gain form
        zeros, poles, gain = signal.tf2zpk(numerator, denominator)

        # Print the extracted zeros, poles, and gain
        print("Zeros:", zeros/1000,"k")
        print("Poles:", poles/1000,"k")
        print("Gain:", gain)


if __name__ == "__main__":
    comp = Type_3_Compensator()
    #comp.update_frequencies(0.1,20000,2000, 100)
    comp.update_frequencies(0.1,20000,50000,200,1000, 100)
    comp.update_sys()

    # Generate frequency response data
    w, mag, phase = signal.bode(comp.sys)

    # Plot magnitude response (dB)
    plt.figure()
    plt.semilogx(w, mag)
    plt.title('Bode Plot - Magnitude Response')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Magnitude [dB]')
    plt.grid(True)
    plt.show()

    # Plot phase response (degrees)
    plt.figure()
    plt.semilogx(w, phase)
    plt.title('Bode Plot - Phase Response')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Phase [degrees]')
    plt.grid(True)
    plt.show()