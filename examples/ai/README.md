# Analog Input Examples

Here you can find the differents waveforms acquired with different analog input method from PCI-6133.
This board only support differential mode in acquisition mode, if you change to ground refenrence in
BNC-2110 the signal have noise.
## loop_continuos_mode

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/loop_continuous.png)

## ext_clk

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/ext_clk.png)

## adquisition_options

### Task method

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/adqui_task.png)

### stream_reader method

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/adqui_many_samp.png)

## ang_start_trigger

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/adqui_task_trig.png)

## dig_start_trigger

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/adqui_dig_trig.png)

## pause trigger
When the signal is exceeds 2.5 V, the acquisition stop and when the signal
falls below 2.5 V, the acquisition continues. The reader method append 
the acquisition until acquire the number of samples requested, if the 
method does not achieve the requested number of samples because the 
acquisition has been paused for a long time, you will receive an 
time out error.
This boards support a pause trigger see the TDMS_trig too.

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/pause_trig_board.png)

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/pause_trig_scope.png)