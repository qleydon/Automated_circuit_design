import sys
import matplotlib.pyplot as plt
import os
from os.path import split as pathsplit
from os.path import join as pathjoin
import numpy as np
from numpy import abs as mag, angle
from PyLTSpice import RawRead

from PyLTSpice import SimRunner
from PyLTSpice import SpiceEditor

class Spice:
    def __init__(self, directory):
        self.directory = directory
        self.simulator = r"C:/Program Files/LTC/LTspiceXVII/XVIIx64.exe"
        # select spice model
        self.output_folder=os.path_join(directory, 'temp')

    def update_circuit(self, circuit):
        self.circuit = circuit
        self.LTC_circuit = SimRunner(output_folder=self.output_folder)
        self.LTC_circuit.create_netlist(os.path_join(self.directory, 'Buck_AC.asc'))
        self.netlist_circuit = SpiceEditor(os.path_join(self.directory, 'Buck_AC.net'))
        
        self.netlist_circuit.set_component_value('L1', self.engineering_notation(self.circuit.L))
        self.netlist_circuit.set_component_value('C1', self.engineering_notation(self.circuit.c))
        self.netlist_circuit.set_component_value('R1', self.engineering_notation(self.circuit.r))

        self.LTC_circuit.run()
        self.plot(pathjoin(self.output_folder, 'Buck_AC.raw'), ("V(vout)",))

    def update_compensator(self, comp):
        self.comp = comp
        self.LTC_comp = SimRunner(output_folder=self.output_folder)
        
        if(comp.type == 1):
            self.LTC_comp.create_netlist(os.path_join(self.directory, 'Compensator1_AC.asc'))
            self.netlist_comp = SpiceEditor(os.path_join(self.directory, 'Compensator1_AC.net'))
            # update components
            self.netlist_comp.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_comp.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            # run file
            self.LTC_comp.run()
            self.plot(pathjoin(self.output_folder, 'Compensator1_AC.raw'), ("V(V_compensated)",))

        elif(comp.type == 2):
            self.LTC_comp.create_netlist(os.path_join(self.directory, 'Compensator2_AC.asc'))
            self.netlist_comp = SpiceEditor(os.path_join(self.directory, 'Compensator2_AC.net'))
            # update components
            self.netlist_comp.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_comp.set_component_value('Rc2', self.engineering_notation(self.comp.r2))
            self.netlist_comp.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            self.netlist_comp.set_component_value('Cc3', self.engineering_notation(self.comp.c3))
            # run file
            self.LTC_comp.run()
            self.plot(pathjoin(self.output_folder, 'Compensator2_AC.raw'), ("V(V_compensated)",))

        elif(comp.type == 3):
            self.LTC_comp.create_netlist(os.path_join(self.directory, 'Compensator3_AC.asc'))
            self.netlist_comp = SpiceEditor(os.path_join(self.directory, 'Compensator3_AC.net'))
            # update components
            self.netlist_comp.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_comp.set_component_value('Rc2', self.engineering_notation(self.comp.r2))
            self.netlist_comp.set_component_value('Rc3', self.engineering_notation(self.comp.r3))
            self.netlist_comp.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            self.netlist_comp.set_component_value('Cc2', self.engineering_notation(self.comp.c2))
            self.netlist_comp.set_component_value('Cc3', self.engineering_notation(self.comp.c3))
            # run file
            self.LTC_comp.run()
            self.plot(pathjoin(self.output_folder, 'Compensator3_AC.raw', ("V(V_compensated)",)))

    def engineering_notation(number):
        # Define the suffixes for engineering notation
        suffixes = ['f', 'p', 'n', 'u', 'm', '', 'k', 'Meg', 'G', 'T']

        # Determine the appropriate suffix and corresponding scale factor
        exponent = int((len(str(abs(number))) - 1) / 3)
        suffix_index = exponent + 5
        scale_factor = 10 ** (exponent * 3)

        # Convert the number to engineering notation
        formatted_number = f'{number / scale_factor:.3f}'
        suffix = suffixes[suffix_index]

        # Remove trailing zeros and decimal point if unnecessary
        formatted_number = formatted_number.rstrip('0').rstrip('.') if '.' in formatted_number else formatted_number
        return f'{formatted_number}{suffix}'
    
    def what_to_units(self, whattype):
        """Determines the unit to display on the plot Y axis"""
        if 'voltage' in whattype:
            return 'V'
        if 'current' in whattype:
            return 'A'
        
    def plot(self, raw_filename, trace_names):
        LTR = RawRead(raw_filename, trace_names, verbose=True)

        for param, value in LTR.raw_params.items():
            print("{}: {}{}".format(param, " " * (20 - len(param)), str(value).strip()))

        if trace_names == '*':
            print("Reading all the traces in the raw file")
            trace_names = LTR.get_trace_names()

        traces = [LTR.get_trace(trace) for trace in trace_names]
        if LTR.axis is not None:
            steps_data = LTR.get_steps()
        else:
            steps_data = [0]
        print("Steps read are :", list(steps_data))

        if 'complex' in LTR.flags:
            n_axis = len(traces) * 2
        else:
            n_axis = len(traces)

        fig, axis_set = plt.subplots(n_axis, 1, sharex='all')
        write_labels = True

        for i, trace in enumerate(traces):
            if 'complex' in LTR.flags:
                axises = axis_set[2 * i: 2 * i + 2]  # Returns two axis
            else:
                if n_axis == 1:
                    axises = [axis_set]  # Needs to return a list
                else:
                    axises = axis_set[i:i + 1]  # Returns just one axis but enclosed in a list
            magnitude = True
            for ax in axises:
                ax.grid(True)
                if 'log' in LTR.flags:
                    ax.set_xscale('log')
                for step_i in steps_data:
                    if LTR.axis:
                        x = LTR.get_axis(step_i)
                    else:
                        x = np.arange(LTR.nPoints)
                    y = LTR.get_wave(trace.name, step_i)
                    if 'complex' in LTR.flags:
                        x = mag(x)
                        if magnitude:
                            ax.set_yscale('log')
                            y = mag(y)
                        else:
                            y = angle(y, deg=True)
                    if write_labels:
                        ax.plot(x, y, label=str(steps_data[step_i]))
                    else:
                        ax.plot(x, y)
                write_labels = False

                if 'complex' in LTR.flags:
                    if magnitude:
                        title = f"{trace.name} Mag [db{self.what_to_units(trace.whattype)}]"
                        magnitude = False
                    else:
                        title = f"{trace.name} Phase [deg]"
                else:
                    title = f"{trace.name} [{self.what_to_units(trace.whattype)}]"
                ax.set_title(title)

        plt.figlegend()
        plt.show()

