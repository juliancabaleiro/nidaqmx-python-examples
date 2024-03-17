"""
This example count edges from TLL signal connected to any PFI or
internal base time that can be routed in ci_count_edges_term. In this case
the counter count edges from internal /Dev1/100kHzTimebase

In timing configuration, only accept external time bases
I can't use start trigger.
"""

import nidaqmx
from nidaqmx import stream_readers
import numpy as np
import time 

system=nidaqmx.system.System.local()
daq_device=system.devices["Dev1"]
#reset the device before to use
daq_device.reset_device()
#see co capabilities of the board
counter_names=[ci.name for ci in daq_device.ci_physical_chans]
print("\nList of counter input",counter_names)
print("List of counter output",[co.name for co in daq_device.co_physical_chans])

with nidaqmx.Task(new_task_name="PCI-PY") as task_ci:
    #add counter input channel
    task_ci.ci_channels.add_ci_count_edges_chan(
                                                counter="/Dev1/Ctr0",
                                                name_to_assign_to_channel="Counter_edge",
                                                edge=nidaqmx.constants.Edge.RISING,
                                                initial_count=0,
                                                count_direction=nidaqmx.constants.CountDirection.COUNT_UP
                                                )
    #Especify the terminal where the signal is conected
    task_ci.ci_channels.all.ci_count_edges_term="/Dev1/100kHzTimebase"
    samps=100000

    #intialize a stream reader object
    reader_ci=stream_readers.CounterReader(task_ci.in_stream)
    data_ci=np.zeros(samps,dtype=np.uint32)

    task_ci.start()
    #obtain the counter measure
    reader_ci.read_many_sample_uint32(
                                        data=data_ci,
                                        number_of_samples_per_channel=samps,
                                        timeout=10.0
                                    )
    task_ci.stop()
    print("\nCounted Value",data_ci[-1])
    print("Counter value length: ",data_ci.shape)
"""
Terminal output
---------------

List of counter input ['Dev1/ctr0', 'Dev1/ctr1']
List of counter output ['Dev1/ctr0', 'Dev1/ctr1', 'Dev1/freqout']

Counted Value 215135
Counter value length:  (100000,)
"""