"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Generate a pulse train, specified in tick's of basetime, 
1 s time ON, 1s time OFF, with /Dev1/100kHzTimebase.
With PCI-6133 through output PFI12/p2.4 

The output is Ctr0Out connected to CTR 0 OUT pin 2 in the pinout of 
the PCI-6133. In the BNC-2110, accessories are routed to the
PFI12/p2.4 (I can't find this in BNC-2110 documentation or DAQ S
serie documentation, but find the output in DAQ M user manuals)

For generating a pulse train, you need to set timing in implicit and 
will generate pulses while the task is running. 
In Sample mode FINITE not work's.
"""

import nidaqmx
import time 

system=nidaqmx.system.System.local()
daq_device=system.devices["Dev1"]
#reset the device before to use
daq_device.reset_device()
#see co capabilities of the board
counter_names=[ci.name for ci in daq_device.ci_physical_chans]
print("\nList of counter input",counter_names)
print("List of counter output",[co.name for co in daq_device.co_physical_chans])

with nidaqmx.Task(new_task_name="PCI-CO") as co_task:
    #add crt0 phisical channel
    co_task.co_channels.add_co_pulse_chan_ticks(
                                                counter="/Dev1/Ctr0",
                                                source_terminal="/Dev1/100kHzTimebase",
                                                name_to_assign_to_channel="hola",
                                                idle_state=nidaqmx.constants.Level.LOW,
                                                initial_delay=0,
                                                low_ticks=100_000,
                                                high_ticks=100_000)
    #setup the timing for generate a pulse train while the task is runing
    co_task.timing.cfg_implicit_timing(
                                        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                        samps_per_chan=100_000
    )

    print("Time base source for counter: ",co_task.co_channels.all.co_ctr_timebase_src)
    print("Counter output terminal: ",co_task.co_channels.all.co_pulse_term)

    co_task.start()
    #generate the pulse
    time.sleep(13)
    co_task.stop()

"""
Terminal Output
---------------

List of counter input ['Dev1/ctr0', 'Dev1/ctr1']
List of counter output ['Dev1/ctr0', 'Dev1/ctr1', 'Dev1/freqout']
Time base source for counter:  /Dev1/100kHzTimebase
Counter output terminal:  /Dev1/Ctr0Out

"""
