"""
Adquire analog waveform with ai0, ai1 in TDMS mode. 
Using start trigger and pause trigger for the adquisition
Generate a trigger pulse by hardware with counter output ctr0.

Signal
------
sin 5 Vpk; offset 2.5 V; frecuency 0.5 Hz

Trigger pulse
-------------
square 5 Vpk; offset 2.5 V; Ton 10 s; Toff 1 s

Pin out with BNC-2110
---------------------
PFI4 -> star trigger (input)
PFI5 -> pause trigger (input)
ai0 -> signal (input)
ai1 -> Pulse trigger (input)
PFI12/P2.4 -> ctr0 (Output)

Connection with BNC-2110
------------------------
PFI5 and PFI4 -> USER 2 (in terminal board)
PFI12/P2.4 -> USER 2 (BNC) and ai1
signal -> ai0
"""

import nidaqmx
import time 
from nptdms import TdmsFile

system=nidaqmx.system.System.local()
print("Connected devices:")
print("\nList analog channels: ")
PCI_6133=system.devices["Dev1"]
PCI_6133.reset_device()
for ai in PCI_6133.ai_physical_chans:
    print(ai.name)

with nidaqmx.Task(new_task_name="PCI-CO") as co_task, nidaqmx.Task(new_task_name="PCI-AI") as ai_task:
    
    #configuro el ctr0 para usar de trigger
    co_task.co_channels.add_co_pulse_chan_time(
                                                counter="/Dev1/Ctr0",
                                                name_to_assign_to_channel="hola",
                                                units=nidaqmx.constants.TimeUnits.SECONDS,
                                                idle_state=nidaqmx.constants.Level.LOW,
                                                initial_delay=0.0,
                                                low_time=1.0,
                                                high_time=10.0)
    
    #Configuro la adquisicion
    ai_task.ai_channels.add_ai_voltage_chan("Dev1/ai0:1",min_val=-10.0,max_val=10.0) #Dev1/ai0:4
    frecuencia=800_000
    ai_task.timing.cfg_samp_clk_timing(rate=frecuencia,
                                           active_edge=nidaqmx.constants.Edge.RISING,
                                           sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                           samps_per_chan=frecuencia)
   
    #start trigger digital
    ai_task.triggers.start_trigger.cfg_dig_edge_start_trig(
                                                        trigger_source="/Dev1/PFI4",
                                                        trigger_edge=nidaqmx.constants.Edge.RISING
    )
    
    #Configuro el trigger pause que para la adquisicion (no soportart un trigger pause por edge)
    ai_task.triggers.pause_trigger.trig_type=nidaqmx.constants.TriggerType.DIGITAL_LEVEL
    ai_task.triggers.pause_trigger.dig_lvl_src="/Dev1/PFI5"                                                                                                                                                                                                                                                                                                                                                                                                                                      
    ai_task.triggers.pause_trigger.dig_lvl_when=nidaqmx.constants.Level.LOW
    
    path=r"TDMS\TDMS_trig\data_tdms_co.tdms"

    ai_task.in_stream.configure_logging(file_path=path,
                           logging_mode=nidaqmx.constants.LoggingMode.LOG,
                           operation=nidaqmx.constants.LoggingOperation.CREATE_OR_REPLACE)
    
    #inicio la secuencia
    ai_task.start()
    co_task.start()
    time.sleep(25)
    co_task.stop()
    ai_task.stop()

#Open the data_tdms_co.tdms to see data
tdms_file = TdmsFile.read(path)

for group in tdms_file.groups():
    group_name = group.name
    print("\n\nGroup name: ",group_name)
    for channel in group.channels():
        channel_name = channel.name
        print("\nChannel name: ", channel_name)
        properties = channel.properties
        print("\nProperties:")
        for prop_n in properties:
            print(prop_n, " : ", properties[prop_n])
        med=channel[:]
        print("\nSome Measurements:", med[1:3])
        print("Measurement dimension",len(med))      
        
"""
Output
------

Connected devices:

List analog channels:
Dev1/ai0
Dev1/ai1
Dev1/ai2
Dev1/ai3
Dev1/ai4
Dev1/ai5
Dev1/ai6
Dev1/ai7


Group name:  PCI-AI

Channel name:  Dev1/ai0

Properties:
NI_Scaling_Status  :  unscaled
NI_Number_Of_Scales  :  2
NI_Scale[1]_Scale_Type  :  Linear
NI_Scale[1]_Linear_Slope  :  0.00030517578125
NI_Scale[1]_Linear_Y_Intercept  :  0.0
NI_Scale[1]_Linear_Input_Source  :  0
NI_ChannelName  :  Dev1/ai0
unit_string  :  Volts
NI_UnitDescription  :  Volts
wf_start_time  :  2024-03-13T11:18:26.821775
wf_increment  :  1.249999999999949e-06
wf_start_offset  :  0.0
wf_samples  :  1

Some Measurements: [2.62573242 2.62695312]
Measurement dimension 8000000

Channel name:  Dev1/ai1

Properties:
NI_Scaling_Status  :  unscaled
NI_Number_Of_Scales  :  2
NI_Scale[1]_Scale_Type  :  Linear
NI_Scale[1]_Linear_Slope  :  0.00030517578125
NI_Scale[1]_Linear_Y_Intercept  :  0.0
NI_Scale[1]_Linear_Input_Source  :  0
NI_ChannelName  :  Dev1/ai1
unit_string  :  Volts
NI_UnitDescription  :  Volts
wf_start_time  :  2024-03-13T11:18:26.821775
wf_increment  :  1.249999999999949e-06
wf_start_offset  :  0.0
wf_samples  :  1

Some Measurements: [4.89624023 4.89868164]
Measurement dimension 8000000
"""