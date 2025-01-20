"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Simple live update using dash and NIDAQmx with simulated PCI board.
The objective is obtain a fluid live update.
Use a subprocess to control the instrument and communicate with dash
usign shared array.

This form to send the figure is more efficently.
The app is branded because exist unknown conflict with
multiprocessing Queue, remove this and the app work well
"""

import nidaqmx
from nidaqmx import stream_readers
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import plotly.graph_objs as go
from collections import deque
from multiprocessing import Process, Array
from numpy.ctypeslib import as_ctypes
import numpy as np
import logging

#dash app declaration
app = dash.Dash(__name__)
#layout
app.layout = html.Div([
    html.H1("Live Update NI-DAQmx Simulated PCI-6133 Board",
               style={'textAlign': 'center'}),
    dcc.Graph(id='live-graph',
              animate=False),
    dcc.Interval(id='graph-update',
                 interval=1*500),
])

#Callback
@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    """
    Read the data from shared array, build the figure and
    send it to the app
    """
    #read the from sahred array
    X=dataB
    Y=dataA

    data = go.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis_title="Time [s]",
                                                yaxis_title="Voltage [V]",)}

def run(dataA,dataB,dev, range, frec, samps):
    """
    Suprocess function, Communicate with the instrument
    adcquire the data and put it in a shared array
    """
    print("\nProcess Start")
    #Initialize the instrument
    task=nidaqmx.Task()
    
    try:
        #add the analog channels
        task.ai_channels.add_ai_voltage_chan(physical_channel=dev+"ai0",
                                            min_val=-1*float(range),
                                            max_val=float(range),
                                            terminal_config= nidaqmx.constants.TerminalConfiguration.DIFF,
                                            units=nidaqmx.constants.VoltageUnits.VOLTS
                                            )
        #add timing configuration from the task
        task.timing.cfg_samp_clk_timing(rate=frec,
                                        source="OnboardClock",
                                        active_edge=nidaqmx.constants.Edge.RISING,
                                        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                        samps_per_chan=samps)
        #initialize a stream reader class
        reader =stream_readers.AnalogMultiChannelReader(task.in_stream)
        datos=np.ones((1,samps))

        dataB[:] = np.arange(0,samps)*(1/frec)
        aux=0
        while(1):
            aux=aux+1
            reader.read_many_sample(data=datos, 
                                    number_of_samples_per_channel=samps, 
                                    timeout=10.0)
            # Simulated PCI board always gives the same waveform only change a slow noise
            # In this way you can see the updated graph
            dataA[:] = datos[0][:]+aux 
    except Exception as e:
        task.stop()
        task.close()
        print("task fail")
        print(e)

if __name__ == '__main__':
    print("\nstart the main")
    #User constants
    dev= "Dev1/"
    range=10.0
    frec=10_000.0
    samps=10_000

    datos_t=np.ones((samps,))
    ctype = as_ctypes(datos_t)
    dataA  = Array(ctype._type_, datos_t, lock=False)
    dataB  = Array(ctype._type_, datos_t, lock=False)
    process1 = Process(target=run,     
                       args=(dataA,dataB,dev, range, frec, samps))
    #start the subproces
    process1.start()
    #To avoid unecessary prints
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    #Start dash app
    app.run_server(debug=False)

"""
Output
------

start the main
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'dash_LiveUpdate_nidaqmx'
 * Debug mode: off

Process Start
"""