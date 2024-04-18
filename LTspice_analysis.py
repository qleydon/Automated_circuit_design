import sys
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from numpy import abs as mag, angle
from PyLTSpice import RawRead

from os.path import join as pathjoin
from PyLTSpice import SimRunner
from PyLTSpice import SpiceEditor
import frequency_analysis

class Spice:
    def __init__(self, directory):
        self.directory = directory
        self.simulator = r"C:/Program Files/LTC/LTspiceXVII/XVIIx64.exe"
        # select spice model
        self.output_folder=pathjoin(directory, 'temp')
        self.voltage_cmd = "PULSE(0 5 1ms 0 0 10ms 0 1)"
        self.runtime = "15m"

    def update_circuit(self, circuit):
        self.circuit = circuit
        self.LTC_circuit = SimRunner(output_folder=self.output_folder)
        self.LTC_circuit.create_netlist(pathjoin(self.directory, 'Buck_AC.asc'))
        self.netlist_circuit = SpiceEditor(pathjoin(self.directory, 'Buck_AC.net'))
        
        '''self.netlist_circuit.set_component_value('L1', str(self.circuit.L))
        self.netlist_circuit.set_component_value('C1', str(self.circuit.c))
        self.netlist_circuit.set_component_value('R1', str(self.circuit.r))'''

        print("L1 =", self.circuit.L,"=", self.engineering_notation(self.circuit.L))
        print("c1 =", self.circuit.c,"=",self.engineering_notation(self.circuit.c))
        self.netlist_circuit.set_component_value('L1', self.engineering_notation(self.circuit.L))
        self.netlist_circuit.set_component_value('C1', self.engineering_notation(self.circuit.c))
        self.netlist_circuit.set_component_value('R1', self.engineering_notation(self.circuit.r))

        self.LTC_circuit.run(self.netlist_circuit)
        raw_file_path = pathjoin(self.output_folder,'Buck_AC_1.raw')
        while not os.path.exists(raw_file_path):
            time.sleep(0.1)  # Wait for a short duration before checking again
        self.plot(raw_file_path, ("V(vout)",))

    def update_compensator(self, comp, plt = True):
        self.comp = comp
        self.LTC_comp = SimRunner(output_folder=self.output_folder)
        
        if(comp.type == 1):
            self.LTC_comp.create_netlist(pathjoin(self.directory, 'Compensator1_AC.asc'))
            self.netlist_comp = SpiceEditor(pathjoin(self.directory, 'Compensator1_AC.net'))
            # update components
            self.netlist_comp.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_comp.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            # run file
            self.LTC_comp.run(self.netlist_comp)
            if plt:
                self.plot(pathjoin(self.output_folder, 'Compensator1_AC_1.raw'), ("V(v_compensated)",))

        elif(comp.type == 2):
            self.LTC_comp.create_netlist(pathjoin(self.directory, 'Compensator2_AC.asc'))
            self.netlist_comp = SpiceEditor(pathjoin(self.directory, 'Compensator2_AC.net'))
            # update components
            self.netlist_comp.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_comp.set_component_value('Rc2', self.engineering_notation(self.comp.r2))
            self.netlist_comp.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            self.netlist_comp.set_component_value('Cc3', self.engineering_notation(self.comp.c3))
            # run file
            self.LTC_comp.run(self.netlist_comp)
            if plt:
                self.plot(pathjoin(self.output_folder, 'Compensator2_AC_1.raw'), ("V(v_compensated)",))

        elif(comp.type == 3):
            self.LTC_comp.create_netlist(pathjoin(self.directory, 'Compensator3_AC.asc'))
            self.netlist_comp = SpiceEditor(pathjoin(self.directory, 'Compensator3_AC.net'))
            # update components
            self.netlist_comp.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_comp.set_component_value('Rc2', self.engineering_notation(self.comp.r2))
            self.netlist_comp.set_component_value('Rc3', self.engineering_notation(self.comp.r3))
            self.netlist_comp.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            self.netlist_comp.set_component_value('Cc2', self.engineering_notation(self.comp.c2))
            self.netlist_comp.set_component_value('Cc3', self.engineering_notation(self.comp.c3))
            # run file
            self.LTC_comp.run(self.netlist_comp)
            if plt:
                self.plot(pathjoin(self.output_folder, 'Compensator3_AC_1.raw'), ("V(v_compensated)",))

    def update_transient_settings(self, voltage_cmd = None, runtime = None):
        if voltage_cmd is not None:
            self.voltage_cmd = voltage_cmd
        
        if runtime is not None:
            self.runtime = runtime
        
    def run_transient(self):
        self.LTC_T = SimRunner(output_folder=self.output_folder)
        
        if(self.comp.type == 1):
            self.LTC_T.create_netlist(pathjoin(self.directory, 'buck_combined_Type_1.asc'))
            self.netlist_T = SpiceEditor(pathjoin(self.directory, 'buck_combined_Type_1.net'))
            # update simulation
            self.netlist_T.set_parameters(Tend = self.runtime)
            self.netlist_T.set_element_model('V2', self.voltage_cmd)
            # update components
            self.netlist_T.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_T.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            # run file
            self.LTC_T.run(self.netlist_T)
            self.plot(pathjoin(self.output_folder, 'buck_combined_Type_1_1.raw'), ("V(vout)","V(v_cmd)"))

        elif(self.comp.type == 2):
            self.LTC_T.create_netlist(pathjoin(self.directory, 'buck_combined_Type_2.asc'))
            self.netlist_T = SpiceEditor(pathjoin(self.directory, 'buck_combined_Type_2.net'))
            # update simulation
            self.netlist_T.set_parameters(Tend = self.runtime)
            self.netlist_T.set_element_model('V2', self.voltage_cmd)
            # update components
            self.netlist_T.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_T.set_component_value('Rc2', self.engineering_notation(self.comp.r2))
            self.netlist_T.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            self.netlist_T.set_component_value('Cc3', self.engineering_notation(self.comp.c3))
            # run file
            self.LTC_T.run(self.netlist_T)
            self.plot(pathjoin(self.output_folder, 'buck_combined_Type_2_1.raw'), ("V(vout)","V(v_cmd)"))

        elif(self.comp.type == 3):
            self.LTC_T.create_netlist(pathjoin(self.directory, 'buck_combined_Type_3.asc'))
            self.netlist_T = SpiceEditor(pathjoin(self.directory, 'buck_combined_Type_3.net'))
            # update simulation
            self.netlist_T.set_parameters(Tend = self.runtime)
            self.netlist_T.set_element_model('V2', self.voltage_cmd)
            # update components
            self.netlist_T.set_component_value('Rc1', self.engineering_notation(self.comp.r1))
            self.netlist_T.set_component_value('Rc2', self.engineering_notation(self.comp.r2))
            self.netlist_T.set_component_value('Rc3', self.engineering_notation(self.comp.r3))
            self.netlist_T.set_component_value('Cc1', self.engineering_notation(self.comp.c1))
            self.netlist_T.set_component_value('Cc2', self.engineering_notation(self.comp.c2))
            self.netlist_T.set_component_value('Cc3', self.engineering_notation(self.comp.c3))
            # run file
            self.LTC_T.run(self.netlist_T)
            self.plot(pathjoin(self.output_folder, 'buck_combined_Type_3_1.raw'), ("V(vout)","V(v_cmd)"))


    def engineering_notation(self, number):
        # Define the suffixes for engineering notation
        suffixes = ['f', 'p', 'n', 'u', 'm', '', 'k', 'Meg', 'G', 'T']

        magnitude = abs(number)
        index = 5  # Start with the default index for '1' (no prefix)
        
        # Check the magnitude to determine the appropriate prefix
        if magnitude >= 1:
            while magnitude >= 1000 and index < len(suffixes) - 1:
                magnitude /= 1000.0
                index += 1
        else:
            while magnitude < 1 and index > 0:
                magnitude *= 1000.0
                index -= 1
        
        # Format the number with the determined prefix
        formatted_number = "{}{}".format(int(magnitude), suffixes[index])
        
        return formatted_number
    
    def what_to_units(self, whattype):
        """Determines the unit to display on the plot Y axis"""
        if 'voltage' in whattype:
            return 'V'
        if 'current' in whattype:
            return 'A'
        
    def plot(self, raw_filename, trace_names):
        LTR = RawRead(raw_filename, trace_names, verbose=True)
        mag_f = None
        phase_f=None
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
                            mag_f=y
                        else:
                            y = angle(y, deg=True)
                            phase_f=y
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

            print("for trace", trace)
            frequency_analysis.find_margins(x, mag_f, -phase_f)


        plt.figlegend()
        plt.show()
    
    def update_file(self, file_name):
        file_name, _ = os.path.splitext(file_name)
        file_name = file_name+".net"
        self.netlist_comp.save_netlist(pathjoin(self.directory, file_name))



