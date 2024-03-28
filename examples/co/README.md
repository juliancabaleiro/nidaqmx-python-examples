# Counter Output Examples

Here you can find from the different waveform generated with different counter output method from PCI-6133.
The output was measured with and oscilloscope and short BNC wire.

The counter are routed this way, but for example CTR 0 output for PCI-6133 are not specified in DAQ S series user manual    
   
Counter 0 Gate -> PFI 9/P2.1  
Counter 0 Source -> PFI 8/P2.0  
COunter 0 Out -> PFI 12/P2.4 (DAQ M series user manual)  

Counter 1 gate -> PFI 4/CTR 1  
Counter 1 Source -> PFI 3/P1.3  
Counter 1 Out -> PFI 13/P2.5 (DAQ M series user manual)  

## co_single_frec

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/co_frec.png)

## co_tick_pulse

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/co_tick.png)

## co_time_pulse

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/co_time.png)

## Large pulses methods

Differents methods to Generate a large pulses higher than 163 s.
you can't use any internal base time for pulses greater than 163 s, because the counter can only count up to 16777215. When the counter overflow raise and error and stop all task. The slowest time base for this phisical channel is the  /Dev1/100kHzTimebase.  
For this reason use a slower external time base and the tick pulse generation is the only method to generate pulses that allows modifying the temporal base.

### co_tick_30min

Generate 1800 s pulse using externa time base with frecuency of 1 Hz

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/co-tick-30min.png)

### co_tick_30min_2ctr

Generate a pulse especified in tick's of basetime, with 1800 s time ON, 36 s time OFF, using two counters,
one as time base and the other for pulse generation.  
Generate a refence TTL singal to use as frecuency reference with ctr1.  
Generate a 1800 s pulse with crt0.  
The frequency of ctr1 is selected to maximize the count  of ctr0 without overflow, with some tolerance.

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/co_tick_30min_2ctr.png)

### counter output vs waveform generator for 1 Hz TTL

![alt text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/co-vs-waveform.png)
