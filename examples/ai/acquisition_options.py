"""
This python example, show differents method to adquire analog signals
with PCI-6133 board.

All measurements were performed with analog input chanel 0.
For add more channels you can change "Dev1/ai0" form 
"Dev1/ai0:5" to add channel 0 to 5
"Dev1/ai0:Dev1/ai2:Dev1/ai4" to add channels 0, 2, 4

The adquisition mode is continouos.
"""

import nidaqmx
from nidaqmx import stream_readers
import numpy as np

#clase que tiene las propiedades
system=nidaqmx.system.System.local()
print("nidaqmx driver version:",system.driver_version)
print("Connected devices:")
for device in system.devices:
    print("Device:", device)

#create the task
with nidaqmx.Task(new_task_name="PCI-PY") as task:
    #add the analog channels
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai0",
                                         min_val=-10.0,
                                         max_val=10.0,
                                         terminal_config= nidaqmx.constants.TerminalConfiguration.DIFF,
                                         units=nidaqmx.constants.VoltageUnits.VOLTS
                                         )
    
    #add timing configuration from the task
    task.timing.cfg_samp_clk_timing(rate=10000,
                                    source="OnboardClock",
                                    active_edge=nidaqmx.constants.Edge.RISING,
                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    samps_per_chan=10000)
    
    #intialize a stream reader class
    reader =stream_readers.AnalogMultiChannelReader(task.in_stream)
    
    #Task methos 10k samples
    med=task.read(10000)
    print("\nTask methos measrument len", len(med))
    print("Some measuremnts:", med[0:3])
    print("Data type: ", type(med[0]))
    
    #stream_reader method only one sample
    data=np.zeros((1,), dtype=np.float64)
    reader.read_one_sample(data, timeout=10)
    print("\nstrem_reader one sample :",data)
    print("Data type: ",type(data))
   
    #stream_rader method many samples
    data=np.zeros((1,10000), dtype=np.float64)
    reader.read_many_sample(data=data, 
                            number_of_samples_per_channel=10000, 
                            timeout=10.0)
    
    print("\nStream_reader many sample length: ",data.shape)
    print("Some mearuments: ",data[0,0:3])
    print("Data type: ",type(data[0]))

"""
Output temrinal
---------------

nidaqmx driver version: DriverVersion(major_version=19, minor_version=6, upda
te_version=0)
Connected devices:
Device: Device(name=Dev1)
Device: Device(name=PXI1Slot2)

Task methos measrument len 10000
Some measuremnts: [-0.286865234375, -0.2880859375, -0.286865234375]
Data type:  <class 'float'>

strem_reader one sample : [-0.20019531]
Data type:  <class 'numpy.ndarray'>

Stream_reader many sample length:  (1, 10000)
Some mearuments:  [-0.20019531 -0.19897461 -0.19775391]
Data type:  <class 'numpy.ndarray'>
"""
