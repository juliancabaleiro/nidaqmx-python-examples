"""
This code measure analog signal in continuous mode using a for loop mehtod.
It does not lose samples but has a problem with the first point. I
try to solve it in different ways but I couldn't. 
Exist another forms to measure without problems.

Input signal
------------
sin 5 Vpk; offset 2.5 V; f 5 Hz -> ai0

I configure two analog input channels but only uses one.
"""

import nidaqmx
from nidaqmx import stream_readers
import numpy as np

#Intialize the system only for print info about the device
system=nidaqmx.system.System.local()
print("\nList analog channels: ")
PCI_6133=system.devices["Dev1"]
PCI_6133.reset_device()
for ai in PCI_6133.ai_physical_chans:
    print(ai.name)

#create de task to aquire analog signals
with nidaqmx.Task(new_task_name="PCI-PY") as task:
    #add phisical channels
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai0:Dev1/ai1",
                                         min_val=-10.0,
                                         max_val=10.0,
                                         terminal_config= nidaqmx.constants.TerminalConfiguration.DIFF,
                                         units=nidaqmx.constants.VoltageUnits.VOLTS
                                         )
    #COnfigure the adquisition timing
    task.timing.cfg_samp_clk_timing(rate=10000,
                                    source="OnboardClock",
                                    active_edge=nidaqmx.constants.Edge.RISING,
                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    samps_per_chan=10000
                                    )
    #initialize reader object
    reader =stream_readers.AnalogMultiChannelReader(task.in_stream)
    data=np.zeros((2,10000), dtype=np.float64)
    dataA=np.empty([1,1])

    #start de task
    task.start()
    for i in range(5):
        reader.read_many_sample(data, 
                                number_of_samples_per_channel=10000, 
                                timeout=10.0)
        dataA=np.append(dataA,data[0])
    task.stop()

    print("\nStream_reader many sample length: ",dataA.shape)
    print("Some mearuments: ",dataA[0:3])
    print("Data type: ",type(dataA[0]))
        
"""
output
------

List analog channels:
Dev1/ai0
Dev1/ai1
Dev1/ai2
Dev1/ai3
Dev1/ai4
Dev1/ai5
Dev1/ai6
Dev1/ai7

Stream_reader many sample length:  (50001,)
Some mearuments:  [9.         0.75195312 0.74829102]
Data type:  <class 'numpy.float64'>
"""
    
    
