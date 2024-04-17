import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from math import pi as pi

from compensator import Type_1_Compensator
from compensator import Type_2_Compensator
from compensator import Type_3_Compensator
from buck import Buck

def bode_plot(circuit, compensator=None):
    log_array = np.logspace(np.log10(0.1), np.log10(1e6), num=1000)
    if compensator is None:
        circuit.update_sys()
        w_crc, mag_crc, phase_crc = signal.bode(circuit.sys, w=log_array)
        plt.figure()
        plt.semilogx(w_crc, mag_crc, label='Circuit', color='blue')
        plt.title('Bode Plot - Magnitude Response')
        plt.xlabel('Frequency [rad/s]')
        plt.ylabel('Magnitude [dB]')
        plt.grid(True)
        plt.show()

        # Plot phase response (degrees)
        plt.figure()
        plt.semilogx(w_crc, phase_crc, label='Circuit', color='blue')
        plt.title('Bode Plot - Phase Response')
        plt.xlabel('Frequency [rad/s]')
        plt.ylabel('Phase [degrees]')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    else:
        circuit.update_sys()
        compensator.update_sys()
        # Generate frequency response data
        w_crc, mag_crc, phase_crc = signal.bode(circuit.sys, w=log_array)
        w_cmp, mag_cmp, phase_cmp = signal.bode(compensator.sys, w=log_array)

        # combined
        # T(s) = G(s)/(1+G(s)H(s)) = N1*D2 / (D1*D2 + N1*N2)
        #numerator = np.polymul(circuit.numerator, compensator.denominator)
        #denominator = np.polyadd(np.polymul(circuit.numerator, compensator.numerator), np.polymul(circuit.numerator, compensator.numerator))
        numerator = np.polymul(circuit.numerator, compensator.numerator)
        denominator = np.polyadd(np.polymul(circuit.denominator, compensator.denominator), np.polymul(circuit.numerator, compensator.numerator))

        T = signal.TransferFunction(numerator, denominator)
        w_cmb, mag_cmb, phase_cmb = signal.bode(T, w=log_array)

        # Plot magnitude response (dB)
        # Create subplots
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        # Plot magnitude response of the circuit
        axs[0, 0].semilogx(w_crc, mag_crc, label='Circuit', color='blue')
        axs[0, 0].semilogx(w_cmp, mag_cmp, label='Compensator', color='red')
        axs[0, 0].set_title('Circuit Magnitude Response')
        axs[0, 0].set_xlabel('Frequency [rad/s]')
        axs[0, 0].set_ylabel('Magnitude [dB]')
        axs[0, 0].grid(True)

        # Plot phase response of the circuit
        axs[1, 0].semilogx(w_crc, phase_crc, label='Circuit', color='blue')
        axs[0, 0].semilogx(w_cmp, phase_cmp, label='Compensator', color='red')
        axs[1, 0].set_title('Circuit Phase Response')
        axs[1, 0].set_xlabel('Frequency [rad/s]')
        axs[1, 0].set_ylabel('Phase [degrees]')
        axs[1, 0].grid(True)

        # Plot magnitude response of the compensator
        axs[0, 1].semilogx(w_cmb, mag_cmb)
        axs[0, 1].set_title('Compensated Circuit Magnitude Response')
        axs[0, 1].set_xlabel('Frequency [rad/s]')
        axs[0, 1].set_ylabel('Magnitude [dB]')
        axs[0, 1].grid(True)

        # Plot phase response of the compensator
        axs[1, 1].semilogx(w_cmb, phase_cmb)
        axs[1, 1].set_title('Compensated Circuit Phase Response')
        axs[1, 1].set_xlabel('Frequency [rad/s]')
        axs[1, 1].set_ylabel('Phase [degrees]')
        axs[1, 1].grid(True)

        # Adjust layout and display the plot
        plt.tight_layout()
        plt.show()