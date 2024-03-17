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