"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Adquire analog signal using external CLK and reader method
Without using trigger

external clock -> PFI0 TTL (saquare Vpp: 5 V offset: 2.5 V)
The frecuency of the singal must be the same that 
-> task.timing.cfg_samp_clk_timing(rate=10000
For use internclock especified in add_ai_voltage_chan
-> source="OnboardClock"

Input signal
------------
sin 5 Vpk; offset 2.5 V; f 5 Hz -> ai0
"""

import nidaqmx
from nidaqmx import stream_readers
import numpy as np
import matplotlib.pyplot as plt

system=nidaqmx.system.System.local()
print("\nList analog channels: ")
PCI_6133=system.devices["Dev1"]
PCI_6133.reset_device()
for ai in PCI_6133.ai_physical_chans:
    print(ai.name)

#create a task
with nidaqmx.Task(new_task_name="PCI-PY") as task:
    #add phisical channels
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai0",
                                         min_val=-10.0,
                                         max_val=10.0,
                                         terminal_config= nidaqmx.constants.TerminalConfiguration.DIFF,
                                         units=nidaqmx.constants.VoltageUnits.VOLTS
                                         )
    
    #add timing configuration from the adquisition
    task.timing.cfg_samp_clk_timing(rate=10000,
                                    source="/Dev1/PFI0",
                                    active_edge=nidaqmx.constants.Edge.RISING,
                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    samps_per_chan=10000)

    print("\nSmpling clk source: ",task.timing.samp_clk_src)
    
    #Initialize a reader objetc
    reader =stream_readers.AnalogMultiChannelReader(task.in_stream)
    data=np.zeros((1,10000), dtype=np.float64)

    #read data using reader method
    reader.read_many_sample(data, 
                            number_of_samples_per_channel=10000, 
                            timeout=10.0)

    print("\nStream_reader many sample length: ",data.shape)
    print("Some mearuments: ",data[0,0:3])
    print("Data type: ",type(data[0,0]))

"""
Output
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

Smpling clk source:  /Dev1/PFI0

Stream_reader many sample length:  (1, 10000)
Some mearuments:  [4.86572266 4.86083984 4.86938477]
Data type:  <class 'numpy.float64'>
"""

    
    