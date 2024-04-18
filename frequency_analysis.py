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
        find_margins(w_crc, mag_crc, phase_crc)
        # Create a single figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

        # Plot magnitude response
        ax1.semilogx(w_crc, mag_crc, label='Circuit', color='blue')
        ax1.set_title('Bode Plot - Magnitude and Phase Response')
        ax1.set_xlabel('Frequency [rad/s]')
        ax1.set_ylabel('Magnitude [dB]')
        ax1.grid(True)

        # Plot phase response
        ax2.semilogx(w_crc, phase_crc, label='Circuit', color='blue')
        ax2.set_xlabel('Frequency [rad/s]')
        ax2.set_ylabel('Phase [degrees]')
        ax2.grid(True)

        # Add legend and adjust layout
        ax1.legend()
        ax2.legend()
        plt.tight_layout()
        plt.show()

    else:
        circuit.update_sys()
        compensator.update_sys()
        # Generate frequency response data
        w_crc, mag_crc, phase_crc = signal.bode(circuit.sys, w=log_array)
        w_cmp, mag_cmp, phase_cmp = signal.bode(compensator.sys, w=log_array)

        # Plot magnitude response (dB)
        # Create subplots
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        # Plot magnitude response of the circuit
        axs[0, 0].semilogx(w_crc, mag_crc, label='Circuit', color='blue')
        axs[0, 0].set_title('Circuit Magnitude Response')
        axs[0, 0].set_xlabel('Frequency [rad/s]')
        axs[0, 0].set_ylabel('Magnitude [dB]')
        axs[0, 0].grid(True)

        # Plot phase response of the circuit
        axs[1, 0].semilogx(w_crc, phase_crc, label='Circuit', color='blue')
        axs[1, 0].set_title('Circuit Phase Response')
        axs[1, 0].set_xlabel('Frequency [rad/s]')
        axs[1, 0].set_ylabel('Phase [degrees]')
        axs[1, 0].grid(True)

        # Plot magnitude response of the compensator
        axs[0, 1].semilogx(w_cmp, mag_cmp, label='Compensator', color='red')
        axs[0, 1].set_title('Compensator Magnitude Response')
        axs[0, 1].set_xlabel('Frequency [rad/s]')
        axs[0, 1].set_ylabel('Magnitude [dB]')
        axs[0, 1].grid(True)

        # Plot phase response of the compensator
        axs[1, 1].semilogx(w_cmp, phase_cmp, label='Compensator', color='red')
        axs[1, 1].set_title('Compensator Phase Response')
        axs[1, 1].set_xlabel('Frequency [rad/s]')
        axs[1, 1].set_ylabel('Phase [degrees]')
        axs[1, 1].grid(True)

        # Adjust layout and display the plot
        plt.tight_layout()
        plt.show()

def find_margins(w, mag, phase):
    # Find the crossover frequency
    gain_crossover_index = np.argmin(np.abs(mag))  # Index where magnitude is closest to 0 dB
    gain_crossover_frequency = w[gain_crossover_index]

    phase_crossover_index = np.argmin(np.abs(180-phase))  # Index where phase is closest to -180
    gain_crossover_frequency = w[phase_crossover_index]

    # Find the gain margin and phase margin
    if np.abs(mag[gain_crossover_index])> 5:
        phase_margin = np.inf  # Default to infinity if phase margin cannot be determined
    else:
        phase_margin = phase[gain_crossover_index]

    if np.abs(180-phase[phase_crossover_index])> 5:
        gain_margin = np.inf  # Default to infinity if gain margin cannot be determined
    else: 
        gain_margin = mag[phase_crossover_index]

    print("\nFrom Bode plot: ")
    print("Gain Margin:", gain_margin)
    print("Phase Margin:", phase_margin, "degrees")
    print("Gain Crossover Frequency:", gain_crossover_frequency, "rad/s")
    print("Phase Crossover Frequency:", phase_crossover_index, "rad/s")
    