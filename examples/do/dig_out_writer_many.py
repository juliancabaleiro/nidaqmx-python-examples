"""
This example, generate digital pulses trough port0/line0. 
Generate using writer many method.
See the readme to see the digital output waveform. 

I can't correctly set the intial state of the digital output.
"""

import nidaqmx
from nidaqmx import stream_writers
import numpy as np

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

    dig_task.start()
    #Generate secuence
    
    dig_out=np.array([0,1,0,1], dtype=np.uint32)
    writer.write_many_sample_port_uint32(data=dig_out)
    
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