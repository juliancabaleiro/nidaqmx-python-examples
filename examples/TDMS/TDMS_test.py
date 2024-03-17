"""
Simple adquisition using a TDMS (Technical Data Management Streaming)
and save de adquisition from ai0 and ai1 in data.tdms file.
In this mode the adquisition the board adquire the data and the buffers
trasnfers the adquisition directly to the hard disk.

For open the tdms file you can use a python or excel with NI-add on. 
See the file tdms_view.py
"""
import nidaqmx
import time 

system=nidaqmx.system.System.local()
print("nidaqmx driver version:",system.driver_version)
print("Connected devices:")
print("\nList analog channels: ")
PCI_6133=system.devices["Dev1"]
PCI_6133.reset_device()
for ai in PCI_6133.ai_physical_chans:
    print(ai.name)

with nidaqmx.Task(new_task_name="PCI-TDMS") as tdms_task:
    #add analog input channel
    tdms_task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai0:Dev1/ai1",
                                              min_val=-10.0,
                                              max_val=10.0)
    #Timing adquisition configuration
    tdms_task.timing.cfg_samp_clk_timing(rate=10000,
                                         active_edge=nidaqmx.constants.Edge.RISING,
                                         sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                         samps_per_chan=10000)
    path=r"TDMS\data.tdms"
    #configure de TDMS mode
    #overwrite the existing file with the new and data only can be accesesed from data.tmds
    tdms_task.in_stream.configure_logging(file_path=path,
                                          logging_mode=nidaqmx.constants.LoggingMode.LOG,
                                          operation=nidaqmx.constants.LoggingOperation.CREATE_OR_REPLACE)
        
    tiempo=30
    #start the adquisition in TDMS file
    tdms_task.start()
    time.sleep(tiempo)
    #stop the task and the aduisition
    tdms_task.stop()

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

Generate the data.tdms and data.tdms_index in path, but 
only import data.tdms
"""
