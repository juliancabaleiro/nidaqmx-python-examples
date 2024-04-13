"""
Simple adquisition using a TDMS (Technical Data Management Streaming)
and save de adquisition from ai0 in multiple data.tdms files.
In this mode the adquisition the board adquire the data and the buffers
trasnfers the adquisition to hard disk.

The RAM size of 1 CH with fs 800 kHz tmds file are this:
3 min -> 1.07 Gb
2 min -> 732 Mb
1 min -> 366 Mb

It is useful for long adquisition generate multiple tdms files.
For activate this multi file generation only need to specify 
the samps per file.
The samps per file are related with buffer size. If manually 
configuring the buffer size choose a multiple of eigth times the
sector size of the disk. For example, in my case the sector 
is 512 bytes my buffer size is 4096. Here is a list of some values:

samps per ch ideally -> closest buffer samples per file
               10000 -> 12288
               20000 -> 20480
               30000 -> 32768
               40000 -> 40960
               50000 -> 53248

The data in each file not depend the samps_per_chan, only the 
logging_samps_per_file and the time of acquisition

Generate the multiple data.tdms and data.tdms_index files
file  -> #samps
data  -> 12288
data1 -> 12288
data2 -> 12288
data3 -> 12288
data4 -> 4096
"""
import nidaqmx
import time 

system=nidaqmx.system.System.local()
print("Connected devices:")
print("\nList analog channels: ")
PCI_6133=system.devices["Dev1"]
PCI_6133.reset_device()
for ai in PCI_6133.ai_physical_chans:
    print(ai.name)

with nidaqmx.Task(new_task_name="PCI-TDMS") as tdms_task:
    #add analog input channel
    tdms_task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai0",
                                              min_val=-10.0,
                                              max_val=10.0,
                                              terminal_config= nidaqmx.constants.TerminalConfiguration.DIFF,
                                              units=nidaqmx.constants.VoltageUnits.VOLTS)
    #Timing adquisition configuration
    tdms_task.timing.cfg_samp_clk_timing(rate=10000,
                                         active_edge=nidaqmx.constants.Edge.RISING,
                                         sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                         samps_per_chan=10000)

    path=r"public\TDMS\TDMS_mult_file\data.tdms"
    #configure de TDMS mode
    #overwrite the existing file with the new
    tdms_task.in_stream.configure_logging(file_path=path,
                                          logging_mode=nidaqmx.constants.LoggingMode.LOG,
                                          operation=nidaqmx.constants.LoggingOperation.CREATE_OR_REPLACE)
    #samples per channel
    tdms_task.in_stream.logging_samps_per_file=12288

    tiempo=5
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

"""
