"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Analog adquisition using external digital start trigger
with window analog comparation

Trigger signal
--------------
TTL, saquare Vpp: 5 V, offset: 2.5 V 

Signal
------
sin 5 Vpk, offset 2.5 V f 5 Hz

Pinout
------
Trigger signal -> PFI0
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

with nidaqmx.Task(new_task_name="PCI-PY") as task:
    #Add analog channels
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai0:Dev1/ai1",
                                         min_val=-10.0,
                                         max_val=10.0,
                                         terminal_config= nidaqmx.constants.TerminalConfiguration.DIFF,
                                         units=nidaqmx.constants.VoltageUnits.VOLTS
                                         )
    
    #Add timming configuration
    task.timing.cfg_samp_clk_timing(rate=10000,
                                    source="OnboardClock",
                                    active_edge=nidaqmx.constants.Edge.RISING,
                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    samps_per_chan=10000)
    
    #start trigger setup
    task.triggers.start_trigger.cfg_dig_edge_start_trig(trigger_source="/Dev1/PFI0",
                                                trigger_edge=nidaqmx.constants.Edge.RISING
                                                )
    #Create a reader object
    reader =stream_readers.AnalogMultiChannelReader(task.in_stream)
    data=np.zeros((2,10000), dtype=np.float64)

    #take measurement
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

Stream_reader many sample length:  (2, 10000)
Some mearuments:  [4.4921875  4.49462891 4.50195312]
Data type:  <class 'numpy.float64'>
"""