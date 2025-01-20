"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Minimal dash app with multiprocessing.
Dash app start and stop the data visualization and
Subprocess generates data continuosly
Recomended procedure (for avoid some errors prints): Start the code, and open 
in navigator app. Ever start
the app without (old app running started in navigator)
"""
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from multiprocessing import Process, Event, Queue, Semaphore
import numpy as np
import plotly.express as px
import logging
 

def run(config_q,dataout_q,event,start_smp):
    """
    Function to run in a subprocess in parallel with dash app.
    Generates data using numpy for demostration.
    
    Parameters
    ----------
    - config_q : [multiprocessing.queues.Queue]
                 Queue with the setings for the process
    - dataout_q : [multiprocessing.queues.Queue]
                  Queue with the generated data
    - event : [multiprocessing.synchronize.Event] 
              Multiprocess variable to safetly stop the process
    - start_smp : [multiprocessing.synchronize.Semaphore]
                  Sempahore to start stop the process data generation
    """
    #Process start
    #clean the deafult values in queue
    config=config_q.get()
    while(True):
        #Process Main-loop
        if start_smp.acquire(block=False) == True:
            start_smp.release()
            config=config_q.get()
            try:
                #Use of configuration info
                datos=np.ones((1,config["samps"]))
                while True:
                    #Output secuence
                    if event.is_set():
                        print("\nProcess-End proccess")
                        break
                    #inputs change update
                    if start_smp.acquire(block=False) == True:
                        start_smp.release()
                        #Data generation
                        datos=np.sin(2*np.pi*config["frec"]*np.linspace(0,(1/config["frec"])*config["samps"],config["samps"]))
                        datos=datos.reshape((1,config["samps"]))
                        #clean the queue
                        try:
                            dataout_q.get(block=False,timeout=0)
                        except:
                            pass
                        #write data in queue
                        dataout_q.put(datos)
                    else:
                        #Stop the data generation
                        break
            except Exception as e:
                print("task fail")
                print(e)

if __name__ == '__main__':
    #default config
    config_d={
                "samps":10000,
                "frec":10000,
                "range":10,
                "dev":"Dev1/"
        }
    #Multiprocessing definitions
    dataout_q = Queue(maxsize=1)
    config_q = Queue(maxsize=1)
    start_smp = Semaphore(2)
    start_smp.acquire(block=False)
    start_smp.acquire(block=False)
    config_q.put(config_d)
    event = Event()
    process1 = Process(target=run,     
                       args=(config_q,dataout_q,event,start_smp))
    process1.start()

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
 
    #layout
    header=html.H4("Minimal measurement dash app",
                   style={'textAlign': 'center'})
    boton=dbc.Button("Start",
                    color="primary",
                    outline=True,
                    id="start-but",
                    className="m-3")
    inputs=dbc.Row([
            dbc.Label(
                "Sampling frecuency [Hz]", 
                width="auto",
                className="m-3"),
            dbc.Col(
                dbc.Input(
                    type="float",
                    placeholder="10000",
                    value=10000,
                    id="frec-in"),
                    className="me-3"),
            dbc.Label(
                "Buffer samples [#samples]", 
                width="auto",
                className="m-3"),
            dbc.Col(
                dbc.Input(
                    type="int",
                    placeholder="10000",
                    value=10000,
                    id="samps-in"),
                    className="me-3"),
            dbc.Label(
                "Range [V]", 
                width="auto",
                className="m-3"),
            dbc.Col(
                dbc.Input(
                    type="int",
                    placeholder="10",
                    value=10,
                    id="range-in"),
                    className="me-3"),
            dbc.Label(
                "Device", 
                width="auto",
                className="m-3"),
            dbc.Col(
                dbc.Input(
                    type="str",
                    placeholder="Dev1/",
                    value="Dev1/",
                    id="dev-in"),
                    className="me-3"),
        ],align='center',justify="evenly",className="g-2")
    grafico=dcc.Graph(id="plot")
    interval = dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True)

    app.layout = dbc.Container([
        dbc.Card([header,inputs,boton]),
        dbc.Card([grafico,interval])
        ])
    
    #Callbacks
    @app.callback(
        Output("interval","disabled"),
        Input("start-but", "n_clicks"),
        [State("frec-in","value"),
         State("samps-in","value"),
         State("range-in","value"),
         State("dev-in","value")]
    )
    def start_measure(n_clicks,frec,samps,range,dev):
        """
        Start or stop the data generation
        """
        print("start_measure callback")
        config_d={
                "samps":int(samps),
                "frec":float(frec),
                "range":float(range),
                "dev":dev
        }
        if n_clicks == None:
            return True
        if int(n_clicks)%2 == 0:
            #stop the interval
            print("Dash-stop-F")
            start_smp.acquire(block=False)
            result=True
        else:
            #Start the interval
            print("Dash-start-T")
            config_q.put(config_d)
            start_smp.release()
            result=False
        return result
 
    @app.callback(
        Output("plot","figure"),
        Input("interval", "n_intervals"),
        Input("start-but", "n_clicks"),
        State("frec-in","value"),
        prevent_initial_call=True,
    )
    def plot_data(n_intervals,n_click,frec_in):
        """
        Read data and generate the graph 
        """
        if n_intervals >=0:
            data=dataout_q.get()
            t=np.arange(len(data[0]))/float(frec_in)
            n=float(n_intervals)
            fig = px.scatter(x=t,y=data[0]+n)
        if n_click == None:
            fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
            return fig
        if int(n_click)%2 == 0:
            fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
        fig.update_traces(marker_color='#2b8cbe')
        fig.update_layout(
        plot_bgcolor='white',
        xaxis_title="Time [s]",
        yaxis_title="Voltage CH0 [V]",
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='#2d3323',
            linewidth=0.3,
            gridcolor='lightgrey',
            zerolinecolor="black",
            zerolinewidth=0.3
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='#2d3323',
            linewidth=0.3,
            gridcolor='lightgrey',
            zerolinecolor="black",
            zerolinewidth=0.3
        )
        #fig.write_html("file.html")
        print("Dash-plot_data send plot")
        return fig       
    
    print("start the app")
    #To avoid dash server output in terminal
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run_server()