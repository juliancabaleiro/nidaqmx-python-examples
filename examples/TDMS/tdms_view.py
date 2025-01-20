"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Open the data.tdms file and show all the data.
Print in terminal all the herarchy of the measurement
and some measurement, and then make a very simple plot 
the adquisition with matplot.

Basic File structure .tdms:

<group_name> -> (tipically the name of the task)
 <channel_name> -> [str] (Use the complete phisical channel name, analog input,counter,digital, etc. like Dev/ai1)
    <channel> ->  [numpy.ndarray] (measurement data)
    <properties> -> [dict] (Aditional measurement information)
        NI_Scaling_Status  :  unscaled
        NI_Number_Of_Scales  :  2
        NI_Scale[1]_Scale_Type  :  Linear
        NI_Scale[1]_Linear_Slope  :  0.00030517578125
        NI_Scale[1]_Linear_Y_Intercept  :  0.0
        NI_Scale[1]_Linear_Input_Source  :  0
        NI_ChannelName  :  Dev1/ai0
        unit_string  :  Volts
        NI_UnitDescription  :  Volts
        wf_start_time  :  2024-02-06T17:12:08.552882
        wf_increment  :  9.999999999999999e-05
        wf_start_offset  :  0.0
        wf_samples  :  1
"""

from nptdms import TdmsFile
import matplotlib.pyplot as plt

path=r"TDMS\data.tdms"
tdms_file = TdmsFile.read(path)

for group in tdms_file.groups():
    group_name = group.name
    print("\n\nGroup name: ",group_name)
    for channel in group.channels():
        #vars(channel) or channel.__dict__ to see all atributtes of the class
        
        channel_name = channel.name
        print("\nChannel name: ", channel_name)
        channel_datatype = channel.data_type
        print("Channel datatype: ", channel_datatype)
        channel_len = channel._length
        print("Channel data len: ", channel_len)
        channel_timestamp= channel._raw_timestamps
        print("Channel raw timestamp; ", channel_timestamp)

        properties = channel.properties
        print("\nProperties:")
        for prop_n in properties:
            print(prop_n, " : ", properties[prop_n])
        med=channel[:]
        print("\nSome Measurements:", med[1:3])
        print("Measurement dimention",len(med))
        plt.plot(med)
        plt.ylabel(channel_name)
        plt.title(channel_name)
        plt.show()

"""
Output
------


Group name:  PCI-TDMS

Channel name:  Dev1/ai0
Channel datatype:  <class 'nptdms.types.DaqMxRawData'>
Channel data len:  303104
Channel raw timestamp;  False

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
wf_start_time  :  2024-03-12T16:48:58.827771
wf_increment  :  9.999999999999999e-05
wf_start_offset  :  0.0
wf_samples  :  1

Some Measurements: [4.99633789 4.99755859]
Measurement dimention 303104

<FIRST PLOT>

Channel name:  Dev1/ai1
Channel datatype:  <class 'nptdms.types.DaqMxRawData'>
Channel data len:  303104
Channel raw timestamp;  False

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
wf_start_time  :  2024-03-12T16:48:58.827771
wf_increment  :  9.999999999999999e-05
wf_start_offset  :  0.0
wf_samples  :  1

Some Measurements: [1.00097656 0.99731445]
Measurement dimention 303104

<SECOND PLOT>
"""

"""
channel attributes
------------------

>> print(channel.__dict__)
{'_path': <nptdms.common.ObjectPath object at 0x000001B130AF3990>, 
'properties': OrderedDict([('NI_Scaling_Status', 'unscaled'), 
                           ('NI_Number_Of_Scales', 2), 
                           ('NI_Scale[1]_Scale_Type', 'Linear'), 
                           ('NI_Scale[1]_Linear_Slope', 0.00030517578125), 
                           ('NI_Scale[1]_Linear_Y_Intercept', 0.0), 
                           ('NI_Scale[1]_Linear_Input_Source', 0), 
                           ('NI_ChannelName', 'Dev1/ai0'), 
                           ('unit_string', 'Volts'), 
                           ('NI_UnitDescription', 'Volts'), 
                           ('wf_start_time', numpy.datetime64('2024-03-12T16:48:58.827771')), 
                           ('wf_increment', 9.999999999999999e-05),
                           ('wf_start_offset', 0.0), 
                           ('wf_samples', 1)]),
'_length': 303104, 
'data_type': <class 'nptdms.types.DaqMxRawData'>, 
'scaler_data_types': {0: <class 'nptdms.types.Int16'>}, 
'_group_properties': OrderedDict(),
'_file_properties': OrderedDict([('name', 'data')]), 
'_reader': <nptdms.reader.TdmsReader object at 0x000001B12F849810>, 
'_raw_timestamps': False, 
'_memmap_dir': None, 
'_raw_data': <nptdms.channel_data.DaqmxDataReceiver object at 0x000001B130AFC390>, 
'_cached_chunk': None, 
'_cached_chunk_bounds': None}
"""
