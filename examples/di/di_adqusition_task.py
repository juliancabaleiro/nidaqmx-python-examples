"""
Adquire digital signal, using task methods

Digital signal input: 5 Vpk; offset 2.5 V; f 500 Hz;  D 50 %

If you not specify a soruce of timing configuration, the error 
requires an external time base for this application (Status Code: -200303)
But, I try with all internal base time: (see capabilities examples), 
and only this works:
/Dev1/20MHzTimebase
/Dev1/MasterTimebase
/Dev1/100kHzTimebase
External base time in :
/Dev1/PFI0

This can't works for me
/Dev1/ai/SampleClock
/Dev1/di/SampleClock
/Dev1/do/SampleClock
/Dev1/ai/SampleClockTimebase
OnboardClock
"""

import nidaqmx
from nidaqmx import stream_readers
import numpy as np

system=nidaqmx.system.System.local()
daq_device=system.devices["Dev1"]
#reset the device before to use
daq_device.reset_device()
#see digital capabilities of the board
print("\nAvailabe digital input lines: ")
for di in daq_device.di_lines:
    print(di.name)

with nidaqmx.Task(new_task_name="PCI-di") as di_task:
    #add digital input channel
    di_task.di_channels.add_di_chan(
                                    lines="Dev1/port0/line0",
                                    name_to_assign_to_lines="p0o0_adq",
                                    line_grouping=nidaqmx.constants.LineGrouping.CHAN_PER_LINE
                                    )
    #configure timing
    di_task.timing.cfg_samp_clk_timing(
                                        rate=10_000,
                                        source="/Dev1/100kHzTimebase",
                                        active_edge=nidaqmx.constants.Edge.RISING,
                                        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                        samps_per_chan=10_000
                                       )
    #using task method, 
    # return a list
    data=di_task.read(
                        number_of_samples_per_channel=1000,
                        timeout=10.0
                      )
    
    print("\nData length: ", len(data))
    print("Data type: ",type(data[0]))
    print("Some data values: ",data[0:4])

"""
Terminal output
---------------

#task method
Availabe digital input lines:
Dev1/port0/line0
Dev1/port0/line1
Dev1/port0/line2
Dev1/port0/line3
Dev1/port0/line4
Dev1/port0/line5
Dev1/port0/line6
Dev1/port0/line7

Data length:  1000
Data type:  <class 'bool'>
Some data values:  [False, False, False, True]
"""