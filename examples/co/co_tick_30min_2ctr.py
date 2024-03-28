"""
Generate a pulse especified in tick's of basetime, 
with 1800 s time ON, 36 s time OFF, using two counters,
one as time base and the other for pulse generation.
Generate a refence TTL singal to use as frecuency reference
with ctr1.
Generate a 1800 s pulse with crt0.
The frequency of ctr1 is selected to maximize the count 
of ctr0 without overflow, with some tolerance.

you can't use any internal base time for pulses greater
than 163 s, because the counter can only count up to 16777215.
When the counter overflow raise and error and stop all task.
The slowest time base for this phisical channel is the 
/Dev1/100kHzTimebase.

For this reason use a slower external time base and
the tick pulse generation is the only method to generate
pulses that allows modifying the temporal base. 

Connection
---------
ctr1 output -> PFI13/P2.5 (BNC-2110)
Route PFI13/P2.5 -> USER 1 ((in terminal board))
user 1 (BNC) -> PFI0/P1.0

Output
------
ctr0 output -> PFI12/P2.4 (BNC-2110)
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

with nidaqmx.Task(new_task_name="PCI-CO") as co_task, nidaqmx.Task(new_task_name="PCI-CO1") as co1_task:
    #pulse duration calculation
    ton=60*30
    tof=int(0.02*ton)
    f=8000
    cmax=16000000
    tick_on=f*ton
    tick_off=f*tof
    
    #Configure CTR1 frecuencia reference
    co1_task.co_channels.add_co_pulse_chan_freq(counter="/Dev1/Ctr1",
                                                name_to_assign_to_channel="ctr1_frec_ref",
                                                units=nidaqmx.constants.FrequencyUnits.HZ,
                                                idle_state=nidaqmx.constants.Level.LOW,
                                                initial_delay=0.0,
                                                freq=f,
                                                duty_cycle=0.5)
    
    print("\nTime base source for counter: ",co1_task.co_channels.all.co_ctr_timebase_src)
    print("Counter output terminal: ",co1_task.co_channels.all.co_pulse_term)

    #setup the timing for generate a pulse train while the task is runing
    co1_task.timing.cfg_implicit_timing(
                                        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                        samps_per_chan=100_000)

    #Configure CTR0 pulse trigger
    co_task.co_channels.add_co_pulse_chan_ticks(
                                                counter="/Dev1/Ctr0",
                                                source_terminal="/Dev1/PFI0",
                                                name_to_assign_to_channel="co_tick_conf",
                                                idle_state=nidaqmx.constants.Level.LOW,
                                                initial_delay=0,
                                                low_ticks=tick_off,
                                                high_ticks=tick_on)

    print("\nCTR0 Time base source: ",co_task.co_channels.all.co_ctr_timebase_src)
    print("CTR0 output terminal: ",co_task.co_channels.all.co_pulse_term)

    print("\nCTR1 Time base source: ",co1_task.co_channels.all.co_ctr_timebase_src)
    print("CTR1 output terminal: ",co1_task.co_channels.all.co_pulse_term)
    
    print("\nstart measurement")
    co1_task.start()
    co_task.start()
    start=time.time()
    #generate the pulse
    time.sleep(ton+tof+3)
    finish=time.time()
    co_task.stop()
    co1_task.stop()
    print("\nfinish measurement")
    print("The sleep time: ",finish-start)

"""
Terminal Output
---------------

List of counter input ['Dev1/ctr0', 'Dev1/ctr1']
List of counter output ['Dev1/ctr0', 'Dev1/ctr1', 'Dev1/fre
qout']

Time base source for counter:  /Dev1/MasterTimebase
Counter output terminal:  /Dev1/Ctr1Out

CTR0 Time base source:  /Dev1/PFI0
CTR0 output terminal:  /Dev1/Ctr0Out

CTR1 Time base source:  /Dev1/MasterTimebase
CTR1 output terminal:  /Dev1/Ctr1Out

start measurement

finish measurement
The sleep time:  1839.0035350322723
"""
