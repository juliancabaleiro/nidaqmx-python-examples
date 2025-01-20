"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Minimal test of the installation nidaqmx drivers.
The PCI-6133 is real device connected to the PC
The PXIe-4481 is a simulated device
"""

import nidaqmx
#Initialize system class
system=nidaqmx.system.System.local()

print("\nVersion of nidaqmx driver:\n",system.driver_version)

#List all Nidaqmx devices in the system
for device in system.devices:
    print("\nDevice:", device)

"""
Output
------

Version of nidaqmx driver:
 DriverVersion(major_version=19, minor_version=6, update_version=0)

Device: Device(name=Dev1)

Device: Device(name=PXI1Slot2)
"""
