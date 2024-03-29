# TDMS_mult_file

Simple adquisition using a TDMS (Technical Data Management Streaming) and save de adquisition from ai0 in multiple data.tdms files.  
If you have a long measurement the time to open large tdms files can be very long, if you try to slice the data the times don't vary too much.

opening time [s] -> data slice   
&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; 0.0 -> no data extracted    
&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;105 -> 100    
&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;113 -> 10_000    
&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;104 -> 100_000    
&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;116 -> 1_440_000_000 (all data extracted)     
In this mode the adquisition the board adquire the data and the buffers trasnfers the adquisition to hard disk.

## Acquisition with PCI board
![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/TDMS_multifile.png)

