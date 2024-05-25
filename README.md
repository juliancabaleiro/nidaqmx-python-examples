# nidaqmx-python-examples

This repository provides a lot of examples on how to use a National Instruments DAQ devices with python 3 using the package [nidaqmx](https://nidaqmx-python.readthedocs.io/en/latest/). Most of the examples were developed for a PCI-6133 and some for the PXI-4461, but all devices were programmed in the same way, changing the capabilities of each board.   
The idea is to share examples with the simplest possible use of python so as to not lose focus on the programming flow of the device.

## Overview

To improve measurement systems we need to program different instruments, many can be programmed using [pyvisa](https://pyvisa.readthedocs.io/en/latest/), but NI hardware don't use the IEEE 488.2 or SCPI standard. For this exist different official packages for different instruments, for PCI and PXI devices included in NI DAQ or DAS series there is the [nidaqmx](https://nidaqmx-python.readthedocs.io/en/latest/), for another instruments like NI-scope, SWITCH, DMM etc. there is the [nimi-python](https://nimi-python.readthedocs.io/en/master/) repository.
## How to understand DAQ devices

Typically, the most important features in these boards are acquisition or generation system that have BW ~ 300 kHz but have better accuracy when compared to others intruments. In addition to having peripherals like counter, digital I/O, synchronization buses, etc. There is a lot of documentation on this, but it is not always easy to find, for this reason I provide a list with the reading order for better understanding.

1. The **board specification**, this give you the hardware capabilities of your specific board.
2. The **DAQ series user manual**, this give you an overview of DAQ system structure, general operation, different blocks, all peripherals that can be equiped and your possible uses or combination. Keep in mind that depending on the selected board exist different DAQ series, S-series, M-series, X-series, etc. and different user manuals.
4. The **daqhelp.chm or NI-DAQmx Help**: Here you can find an explanation of how the programming logic is in these boards, the concepts of task, channels, etc. This document typically was installed with the NI drivers, in NI folder.
5. The  **C examples** Here you can find examples on how to program the board in C language. The python package and LabVIEW are wrapper for C library. These can be find some folders up the daq help. 
6. The **DAQmx ANSI C** the documentation for the C library for these devices.

All documents are available in the [NI](https://www.ni.com/docs/en-US/) or in daqmx driver folder.

## Get started

### Installation driver
Download and Install [ni-daqmx-driver](https://www.ni.com/es/support/downloads/drivers/download.ni-daq-mx.html#521556), find your version using the user manual of the device. If it is not the correct one, you can uninstall from NI package manager (this software is installed with the driver) and try with another version. For example for PCI-6133 the daqmx driver is compatible up to version 19.6, later versions do not recognize this board.

### NI MAX check
With the nidaqmx driver, NI-max software is installed (if you didn't have any NI driver previously installed), here in devices and interface you can see all devices connected to the PC and communicate with them. You can do the self-test to check that the communication with the device works and use the test panel to test some device functions.

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/5.png)

### Simulate DAQ device
Sometimes you have to develop code to program a device on a computer that does not have the device connected. For this you can simulate a lot of DAQ devices, this is useful for test configuration, check capabilities and run codes without the devices and without unnecessary errors.  
To do this, follow the steps:  

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/1.png)
![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/2.png)
![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/3.png)
![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/4.png)
![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/5.png)  

Here, you can see different icons between a real PCI-6133 device connected and a simulated PXI-4481.

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/simulated%20and%20real.png)

### Installation python package
With the driver installed and with the device connected or simulated you can install [nidaqmx](https://nidaqmx-python.readthedocs.io/en/latest/) python package, I recommend using a [virtual environment](https://docs.python.org/3/library/venv.html) and install the requeriments.txt with python 3.7.9 32 bits to run the examples.

````shell
python -m pip install nidaqmx
````

### Run test example

Run the test_daqmx.py and see the output, you should see the driver version and the list of all devices on terminal. If everything is working, you are ready to program any daq or das device with python.   
I recommend running the capabilities example to see all the functionalities supported by your device. 

## Contact

For comments, suggestion or anything else, e-mail me at jncabaleiro@gmail.com


