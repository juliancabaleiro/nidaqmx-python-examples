"""
Analog acquisition using analog pause trigger with level comparison
in ai0.
When the signal is exceeds 2.5 V, the acquisition stop and when the signal
falls below 2.5 V, the acquisition continues. The reader method append 
the acquisition until acquire the number of samples requested, if the 
method does not achieve the requested number of samples because the 
acquisition has been paused for a long time, you will receive an 
time out error.

Signal and Trigger signal
-------------------------
sin 5 Vpk, offset 2.5 V f 5 Hz
"""

import nidaqmx
from nidaqmx import stream_readers
import numpy as np
import matplotlib.pyplot as plt
import time 

system=nidaqmx.system.System.local()
print("\nList analog channels: ")
PCI_6133=system.devices["Dev1"]
PCI_6133.reset_device()
for ai in PCI_6133.ai_physical_chans:
    print(ai.name)


with nidaqmx.Task(new_task_name="PCI-PY") as task:
    #Add analog channels
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai0",
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
                                    samps_per_chan=10000
                                    ) 

    #Pause trigger setup
    task.triggers.pause_trigger.trig_type=nidaqmx.constants.TriggerType.ANALOG_LEVEL
    task.triggers.pause_trigger.anlg_lvl_src="Dev1/ai0"                                                                                                                                                                                                                                                                                                                                                                                                                                      
    task.triggers.pause_trigger.anlg_lvl_lvl=2.5
    task.triggers.pause_trigger.anlg_lvl_when=nidaqmx.constants.ActiveLevel.ABOVE

    #Create a reader object
    reader =stream_readers.AnalogMultiChannelReader(task.in_stream)
    data=np.zeros((1,50000), dtype=np.float64)
  
    task.start()
    #take measurement
    reader.read_many_sample(data,
                            number_of_samples_per_channel=50000,
                            timeout=20.0
                            )
    task.stop()    

    print("\nStream_reader many sample length: ",data.shape)
    print("Some mearuments: ",data[0:3])
    print("Data type: ",type(data[0]))
    
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

Stream_reader many sample length:  (1, 50000)
Some mearuments:  [-0.00976562 -0.01220703 -0.01220703]
Data type:  <class 'numpy.float64'>
"""

    