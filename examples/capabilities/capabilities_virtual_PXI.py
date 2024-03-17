"""
This example code, list many of the virtual PXIe-4481  capabilities.
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
PXIe_4481=system.devices["PXI1Slot2"]
print("Object type the device: ", type(PXIe_4481))

print("\nNumber of DMA channels: ",PXIe_4481.num_dma_chans)

print("\nType of bus communication: ",PXIe_4481.bus_type)

print("\nNumber of PCI bus: ",PXIe_4481.pci_bus_num)

print("\nPXI chassis num: ",PXIe_4481.pxi_chassis_num)

print("\nPXI slot: ",PXIe_4481.pxi_slot_num)

print("\nDevice category: ",PXIe_4481.product_category)

#print("\nUnique identification code from the hardware: ",PXIe_4481.product_num)

print("\nProduct type: ",PXIe_4481.product_type)

#They must be added previously from NI-MAX, left-click onthe device, configuration
print("\nList of connected accesories: ")
for accesorios in PXIe_4481.accessory_product_types:
    print(accesorios)

print("\nList analog channels: ")
for ai in PXIe_4481.ai_physical_chans:
    print(ai.name)

#Listados de acoplamiento 
print("\nCoupling supported by the AI-CH")
for cou in PXIe_4481.ai_couplings:
    print(cou)

print("\nMaximum sampling rate from a single_chan: ", PXIe_4481.ai_max_single_chan_rate)
print("\nMaximum sampling rate from  multi_chan: ", PXIe_4481.ai_max_multi_chan_rate)
print("\nMinimun sampling rate supported: ", PXIe_4481.ai_min_rate)

print("\nType of analog measurements supported: ")
for ai in PXIe_4481.ai_meas_types:
    print(ai)

print("\nTypes of adquisition modes:")
for samp in PXIe_4481.ai_samp_modes:
    print(samp)

print("\nSimultaneous sampling supported?: ",PXIe_4481.ai_simultaneous_sampling_supported)

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
for trg in PXIe_4481.ai_trig_usage:
    print(trg)

print("\nList of analog output:")
for ao in PXIe_4481.ao_physical_chans:
    print(ao)


print("\nSupported measurements from the CounterInput")
for ci in PXIe_4481.ci_meas_types:
    print(ci)

print("\nAvailable Counter Input: ")
for ci in PXIe_4481.ci_physical_chans:
    print(ci.name)
   
print("\nModules contained in the chassis", PXIe_4481.chassis_module_devices)

print("\nSupported counter input task Trigger: ")
for trig in PXIe_4481.ci_trig_usage:
    print(trig)

print("\nSampling modes supported by Counter Input: ")
for mode in PXIe_4481.ci_samp_modes:
    print(mode)

print("\nAvailable digital ports: ")
for port in PXIe_4481.di_ports:
    print(port.name)

print("\nSupported Trigger types from Counter Output Task: ")
for trig in PXIe_4481.co_trig_usage:
    print(trig)

print("\nAvailabe digital input lines: ")
for di in PXIe_4481.di_lines:
    print(di.name)

print("\nSupported Digital triggers: ",PXIe_4481.dig_trig_supported)

print("\nSupported Trigger types from Digital Output Task: ")
for trig in PXIe_4481.do_trig_usage:
    print(trig)

print("\nDigital output lines:")
for do in PXIe_4481.do_lines:
    print(do.name)

print("\nDigital output ports: ")
for do in PXIe_4481.do_ports:
    print(do.name)

#more info in NI-MAX device routes flap
print("\nComplete List of device terminals: ")
for ter in PXIe_4481.terminals:
    print(ter)

#Test analog measuremnt
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    dato=task.read()
    print("\nMearuement from Dev/ai1: ", dato)


"""
nidaqmx driver version: DriverVersion(major_version=19, minor_version=6, update_version=0)

Device:  Device(name=Dev1)

Device:  Device(name=PXI1Slot2)
Object type the device:  <class 'nidaqmx.system.device.Device'>

Number of DMA channels:  1

Type of bus communication:  BusType.PXIE

Number of PCI bus:  2147430400

PXI chassis num:  1

PXI slot:  2

Device category:  ProductCategory.DSA

Product type:  PXIe-4481

List of connected accesories:

List analog channels:
PXI1Slot2/ai0
PXI1Slot2/ai1
PXI1Slot2/ai2
PXI1Slot2/ai3
PXI1Slot2/ai4
PXI1Slot2/ai5

Coupling supported by the AI-CH
Coupling.AC
Coupling.DC

Maximum sampling rate from a single_chan:  20000000.0

Maximum sampling rate from  multi_chan:  20000000.0

Minimun sampling rate supported:  100.0

Type of analog measurements supported:
UsageTypeAI.VOLTAGE

Types of adquisition modes:
AcquisitionType.FINITE
AcquisitionType.CONTINUOUS

Simultaneous sampling supported?:  True

 To sincronize usign RTSI change this parameter for RTSI7:  /Dev1/20MHzTimebase

List of supported triggers form analog adquisition task
TriggerUsage.REFERENCE
TriggerUsage.START

List of analog output:

Supported measurements from the CounterInput

Available Counter Input:

Modules contained in the chassis []

Supported counter input task Trigger:

Sampling modes supported by Counter Input:

Available digital ports:

Supported Trigger types from Counter Output Task:

Availabe digital input lines:

Supported Digital triggers:  True

Supported Trigger types from Digital Output Task:

Digital output lines:

Digital output ports:

Complete List of device terminals:
/PXI1Slot2/PFI0
/PXI1Slot2/PXI_Trig0
/PXI1Slot2/PXI_Trig1
/PXI1Slot2/PXI_Trig2
/PXI1Slot2/PXI_Trig3
/PXI1Slot2/PXI_Trig4
/PXI1Slot2/PXI_Trig5
/PXI1Slot2/PXI_Trig6
/PXI1Slot2/PXI_Trig7
/PXI1Slot2/te0/SampleClock
/PXI1Slot2/te0/StartTrigger
/PXI1Slot2/te0/ReferenceTrigger
/PXI1Slot2/te1/SampleClock
/PXI1Slot2/te1/StartTrigger
/PXI1Slot2/te1/ReferenceTrigger
/PXI1Slot2/te2/SampleClock
/PXI1Slot2/te2/StartTrigger
/PXI1Slot2/te2/ReferenceTrigger
/PXI1Slot2/PXIe_DStarA
/PXI1Slot2/PXIe_DStarB
/PXI1Slot2/PXIe_DStarC
/PXI1Slot2/te0/SyncPulse
/PXI1Slot2/te1/SyncPulse
/PXI1Slot2/te2/SyncPulse
/PXI1Slot2/None
/PXI1Slot2/PXIe_Clk100
/PXI1Slot2/AnalogComparisonEvent

Mearuement from Dev/ai1:  -0.0006103515625
"""