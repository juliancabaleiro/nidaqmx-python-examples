"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

This example, generate digital pulses trough port0/line0. 
Generate using the writer one method.
See the readme to see the digital output waveform. 

I can't correctly set the intial state of the digital output.
"""

import nidaqmx
from nidaqmx import stream_writers
import time

system=nidaqmx.system.System.local()
daq_device=system.devices["Dev1"]
#reset the device before to use
daq_device.reset_device()
#see digital capabilities of the board
print("\nAvailabe digital output lines: ")
for di in daq_device.do_lines:
    print(di.name)

with nidaqmx.Task(new_task_name="PCI-do") as dig_task:
    #add digital output channel
    dig_task.do_channels.add_do_chan(
                                        lines="Dev1/port0/line0",
                                        name_to_assign_to_lines="p0o0_gen",
                                        line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE
    )

    #Define the intial state from the output
    dig_task.do_channels.do_line_states_start_state=nidaqmx.constants.Level.LOW
    dig_task.do_channels.do_line_states_done_state=nidaqmx.constants.Level.LOW
    dig_task.do_channels.do_line_states_paused_state=nidaqmx.constants.Level.LOW
    #create a stream writer objet
    writer=stream_writers.DigitalSingleChannelWriter(dig_task.in_stream)
    
    #Writer method
    #generate one value
    dig_task.start()
    
    writer.write_one_sample_one_line(data=0)
    for i in range(10):
        #print(i)
        writer.write_one_sample_one_line(data=1)
        time.sleep(5E-6)
        writer.write_one_sample_one_line(data=0)
   
    dig_task.stop()

"""
Terminal output
---------------

Availabe digital output lines:
Dev1/port0/line0
Dev1/port0/line1
Dev1/port0/line2
Dev1/port0/line3
Dev1/port0/line4
Dev1/port0/line5
Dev1/port0/line6
Dev1/port0/line7
"""