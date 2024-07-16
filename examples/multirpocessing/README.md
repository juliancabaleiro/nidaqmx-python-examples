# Multiprocessing Examples

Here you can find different examples that allow you to know how to run multiple process in parallel in python, implement measurement with real or simulated nidaqmx devices and different ways to pass data between process. Using **multiprocessing** pacakge this is easy to make.      
To learn more about this, I recommend read [Super Fast python-Multiprocessing Guide](https://superfastpython.com/multiprocessing-in-python/).  

## Why parallelize?

When you want to develop a measurement app that make long measurements, continuous measurement or want to do another things at the same time that the measurement were performed, need to parallelize the instrument communication with the main code (analysis, plot, save, GUI, etc.). Depending on your main program, you may receive a timeout error if you do not attend to the instrument correctly, and you may lose the communication with the instrument.   
This can also be useful in cases of using (PyVISA)[https://pyvisa.readthedocs.io/en/latest/] or another package.
