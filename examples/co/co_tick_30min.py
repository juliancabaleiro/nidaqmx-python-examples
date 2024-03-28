"""
Generate a pulse especified in tick's of basetime, 
with 1800 s time ON, 36 s time OFF, with external 1 Hz 
reference signal connected to /Dev1/PFI0

you can't use any internal base time for pulses greater
than 163 s, because the counter can only count up to 16777215.
When the counter overflow raise and error and stop all task.
The slowest time base for this phisical channel is the 
/Dev1/100kHzTimebase.

For this reason use a slower external time base and
the tick pulse generation is the only method to generate
pulses that allows modifying the temporal base. 

pin out
-------
1 Hz TTL signal -> PFI0 (input)
30 min pulse -> PFI 12/P2.4 (output) 
"""

import nidaqmx
import time

system=nidaqmx.system.System.local()
daq_device=system.devices["Dev1"]
#reset the device before to use
daq_device.reset_device()
#co capabilities of the board
counter_names=[ci.name for ci in daq_device.ci_physical_chans]
print("\nList of counter input",counter_names)
print("List of counter output",[co.name for co in daq_device.co_physical_chans])

with nidaqmx.Task(new_task_name="PCI-CO") as co_task:
    #Calculate the ticks for 30 min pulse with 1 Hz time base 
    ton=60*30
    tof=int(0.02*ton)
    tick_on=ton*1
    tick_off=tof*1
    #add ctr0 phisical channel
    co_task.co_channels.add_co_pulse_chan_ticks(
                                                counter="/Dev1/Ctr0",
                                                source_terminal="/Dev1/PFI0",
                                                name_to_assign_to_channel="co_tick_conf",
                                                idle_state=nidaqmx.constants.Level.LOW,
                                                initial_delay=0,
                                                low_ticks=tick_off,
                                                high_ticks=tick_on)

    print("Time base source for counter: ",co_task.co_channels.all.co_ctr_timebase_src)
    print("Counter output terminal: ",co_task.co_channels.all.co_pulse_term)
    
    co_task.start()
    time.sleep(ton+tof+3)
    finish=time.time()
    co_task.stop()

"""
Terminal Output
---------------

List of counter input ['Dev1/ctr0', 'Dev1/ctr1']
List of counter output ['Dev1/ctr0', 'Dev1/ctr1', 'Dev1/freqout']
Time base source for counter:  /Dev1/PFI0
Counter output terminal:  /Dev1/Ctr0Out

"""
