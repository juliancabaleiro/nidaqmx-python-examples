"""
Open the data.tdms file and show all the data.
Print in terminal all the herarchy of the measurement
and some measurement, and then make a very simple plot 
the adquisition with matplot.

File structure .tdms:

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
        channel_name = channel.name
        print("\nChannel name: ", channel_name)
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



