# Dash Examples

Here you can find simple examples of how to use graphical interface **dash** to perform measurements.

## How to launch a Dash app

Only run the desired python file and open the local host printed in the terminal in your internet browser and can interact with the app.  
```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: on
```

## dash_LiveUpdate_nidaqmx.py

This example show a simple live update of data acquired by a simulated PCI board. In this case I transfer the data from the subprocess to dash using [Shared Ctypes Arrays](https://superfastpython.com/multiprocessing-shared-ctypes-in-python/).

![Alt Text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/dash_LiveUpdate_nidaqmx.gif)

With the following diagram you can quickly understand the app.

![Alt Text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/LiveUpdate-diagram.png)

### Use Multiprocessing Queue

I don't recommend using multiprocessing Queue and Dash, I don't know why but it causes the app run slowly, freeze or crash without raising any exeptions. You can test this by comparing it with the following example.

## dash_without_instrument.py

This example shows the use of a dash to create simple continuous measurement **[GUI](https://en.wikipedia.org/wiki/Graphical_user_interface)**. This app does not requiere having the **ni-daq drivers** installed because it generates the data with **numpy**.

![Alt Text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/dash-without-instrument.gif)

The best way to understand it is to use a diagram to see the parts and their relationship.  

![Alt Text](https://github.com/juliancabaleiro/nidaqmx-python-examples/blob/main/doc/images/dash_without_instrument.png)