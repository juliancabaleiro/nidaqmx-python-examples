"""
This example code, list many of the PCI 6133 capabilities.
Creates a task and makes a simple measurement of an analog channel.
"""

import nidaqmx

#class with system properties
system=nidaqmx.system.System.local()

#nidaqmx driver version
print("\nnidaqmx driver version:",system.driver_version)

#List of devices
for device in system.devices:
    print("\nDevice: ", device)

#Create a device object
PCI_6133=system.devices["Dev1"]
print("Object type the device: ", type(PCI_6133))

print("\nNumber of DMA channels: ",PCI_6133.num_dma_chans)

print("\nType of bus communication: ",PCI_6133.bus_type)

print("\nNumber of PCI bus: ",PCI_6133.pci_bus_num)

print("\nPCI slot: ",PCI_6133.pci_dev_num)

print("\nDevice category: ",PCI_6133.product_category)

#print("\nUnique identification code from the hardware: ",PCI_6133.product_num)

print("\nProduct type: ",PCI_6133.product_type)

print("\nMax counter input bits: ", PCI_6133.ci_max_size)

#They must be added previously from NI-MAX, left-click onthe device, configuration
print("\nList of connected accesories: ")
for accesorios in PCI_6133.accessory_product_types:
    print(accesorios)

print("\nList analog channels: ")
for ai in PCI_6133.ai_physical_chans:
    print(ai.name)

#Listados de acoplamiento 
print("\nCoupling supported by the AI-CH")
for cou in PCI_6133.ai_couplings:
    print(cou)

print("\nMaximum sampling rate from a single_chan: ", PCI_6133.ai_max_single_chan_rate)
print("\nMaximum sampling rate from  multi_chan: ", PCI_6133.ai_max_multi_chan_rate)
print("\nMinimun sampling rate supported: ", PCI_6133.ai_min_rate)

print("\nType of analog measurements supported: ")
for ai in PCI_6133.ai_meas_types:
    print(ai)

print("\nTypes of adquisition modes:")
for samp in PCI_6133.ai_samp_modes:
    print(samp)

print("\nSimultaneous sampling supported?: ",PCI_6133.ai_simultaneous_sampling_supported)

#Create a test task
#initialize de task 
task=nidaqmx.Task(new_task_name="PCI-6133")
#add counter input channel from the task
task.ci_channels.add_ci_count_edges_chan(
                                        counter="/Dev1/Ctr1",
                                        name_to_assign_to_channel="Counter_edge",
                                        edge=nidaqmx.constants.Edge.RISING,
                                        initial_count=0,
                                        count_direction=nidaqmx.constants.CountDirection.COUNT_UP
                                        )

print("\n To sincronize usign RTSI change this parameter for RTSI7: ",task.timing.master_timebase_src)
task.stop()
task.close()

print("\nList of supported triggers form analog adquisition task")
for trg in PCI_6133.ai_trig_usage:
    print(trg)

print("\nList of analog output:")
for ao in PCI_6133.ao_physical_chans:
    print(ao)


print("\nSupported measurements from the CounterInput")
for ci in PCI_6133.ci_meas_types:
    print(ci)

print("\nAvailable Counter Input: ")
for ci in PCI_6133.ci_physical_chans:
    print(ci.name)
   
print("\nMaximum time base from counter input: ",PCI_6133.ci_max_timebase)

print("\nSupported sample clk timing for counter input task: ",PCI_6133.ci_samp_clk_supported)

print("\nSupported counter input task Trigger: ")
for trig in PCI_6133.ci_trig_usage:
    print(trig)

print("\nSampling modes supported by Counter Input: ")
for mode in PCI_6133.ci_samp_modes:
    print(mode)

print("\nSupport Clock Timing type for counter input task: ",PCI_6133.ci_samp_clk_supported)

print("\nAvailable digital ports: ")
for port in PCI_6133.di_ports:
    print(port.name)

print("\nSupported Trigger types from Counter Output Task: ")
for trig in PCI_6133.co_trig_usage:
    print(trig)

print("\nAvailabe digital input lines: ")
for di in PCI_6133.di_lines:
    print(di.name)

print("\nMaximum digital sampling rate",PCI_6133.di_max_rate)

print("\nSupported Digital triggers: ",PCI_6133.dig_trig_supported)

print("\nSupported Trigger types from Digital Output Task: ")
for trig in PCI_6133.do_trig_usage:
    print(trig)

print("\nDigital output lines:")
for do in PCI_6133.do_lines:
    print(do.name)

print("\nMaximum digital output rate: ",PCI_6133.do_max_rate)
print("\nDigital output ports: ")
for do in PCI_6133.do_ports:
    print(do.name)

print("\nComplete List of device terminals: ")
for ter in PCI_6133.terminals:
    print(ter)

#Test analog measuremnt
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    dato=task.read()
    print("\nMearuement from Dev/ai1: ", dato)


"""
Output terminal
---------------

nidaqmx driver version: DriverVersion(major_version=19, minor_version=6, update_version=0)

Device:  Device(name=Dev1)

Device:  Device(name=PXI1Slot2)
Object type the device:  <class 'nidaqmx.system.device.Device'>

Number of DMA channels:  3

Type of bus communication:  BusType.PCI

Number of PCI bus:  2

PCI slot:  6

Device category:  ProductCategory.S_SERIES_DAQ

Product type:  PCI-6133

Max counter input bits:  24

List of connected accesories:
BNC-2110

List analog channels:
Dev1/ai0
Dev1/ai1
Dev1/ai2
Dev1/ai3
Dev1/ai4
Dev1/ai5
Dev1/ai6
Dev1/ai7

Coupling supported by the AI-CH
Coupling.DC

Maximum sampling rate from a single_chan:  2500000.0

Maximum sampling rate from  multi_chan:  2500000.0

Minimun sampling rate supported:  0.0059604644775390625

Type of analog measurements supported:
UsageTypeAI.CURRENT
UsageTypeAI.RESISTANCE
UsageTypeAI.STRAIN_STRAIN_GAGE
UsageTypeAI.TEMPERATURE_RTD
UsageTypeAI.TEMPERATURE_THERMISTOR
UsageTypeAI.TEMPERATURE_THERMOCOUPLE
UsageTypeAI.VOLTAGE
UsageTypeAI.VOLTAGE_CUSTOM_WITH_EXCITATION
UsageTypeAI.POSITION_EDDY_CURRENT_PROX_PROBE
UsageTypeAI.ROSETTE_STRAIN_GAGE

Types of adquisition modes:
AcquisitionType.FINITE
AcquisitionType.CONTINUOUS

Simultaneous sampling supported?:  True

 To sincronize usign RTSI change this parameter for RTSI7:  /Dev1/20MHzTimebase

List of supported triggers form analog adquisition task
TriggerUsage.PAUSE
TriggerUsage.REFERENCE
TriggerUsage.START

List of analog output:

Supported measurements from the CounterInput
UsageTypeCI.COUNT_EDGES
UsageTypeCI.FREQUENCY
UsageTypeCI.PERIOD
UsageTypeCI.PULSE_WIDTH_DIGITAL_SEMI_PERIOD
UsageTypeCI.PULSE_WIDTH_DIGITAL

Available Counter Input:
Dev1/ctr0
Dev1/ctr1

Maximum time base from counter input:  20000000.0

Supported sample clk timing for counter input task:  True

Supported counter input task Trigger:
TriggerUsage.PAUSE

Sampling modes supported by Counter Input:
AcquisitionType.FINITE
AcquisitionType.CONTINUOUS
AcquisitionType.HW_TIMED_SINGLE_POINT

Support Clock Timing type for counter input task:  True

Available digital ports:
Dev1/port0

Supported Trigger types from Counter Output Task:
TriggerUsage.PAUSE
TriggerUsage.START

Availabe digital input lines:
Dev1/port0/line0
Dev1/port0/line1
Dev1/port0/line2
Dev1/port0/line3
Dev1/port0/line4
Dev1/port0/line5
Dev1/port0/line6
Dev1/port0/line7

Maximum digital sampling rate 10000000.0

Supported Digital triggers:  True

Supported Trigger types from Digital Output Task:

Digital output lines:
Dev1/port0/line0
Dev1/port0/line1
Dev1/port0/line2
Dev1/port0/line3
Dev1/port0/line4
Dev1/port0/line5
Dev1/port0/line6
Dev1/port0/line7

Maximum digital output rate:  10000000.0

Digital output ports:
Dev1/port0

Complete List of device terminals:
/Dev1/PFI0
/Dev1/PFI1
/Dev1/PFI2
/Dev1/PFI3
/Dev1/PFI4
/Dev1/PFI5
/Dev1/PFI6
/Dev1/PFI7
/Dev1/PFI8
/Dev1/PFI9
/Dev1/RTSI0
/Dev1/RTSI1
/Dev1/RTSI2
/Dev1/RTSI3
/Dev1/RTSI4
/Dev1/RTSI5
/Dev1/RTSI6
/Dev1/RTSI7
/Dev1/ai/SampleClock
/Dev1/ai/StartTrigger
/Dev1/ai/ReferenceTrigger
/Dev1/di/SampleClock
/Dev1/do/SampleClock
/Dev1/20MHzTimebase
/Dev1/ai/PauseTrigger
/Dev1/ai/SampleClockTimebase
/Dev1/AnalogComparisonEvent
/Dev1/Ctr0Out
/Dev1/Ctr0Gate
/Dev1/Ctr0Source
/Dev1/Ctr0InternalOutput
/Dev1/Ctr1Out
/Dev1/Ctr1Gate
/Dev1/Ctr1Source
/Dev1/Ctr1InternalOutput
/Dev1/PairedCtrInternalOutput
/Dev1/PairedCtrOutputPulse
/Dev1/MasterTimebase
/Dev1/100kHzTimebase

Mearuement from Dev/ai1:  -0.0006103515625

"""
