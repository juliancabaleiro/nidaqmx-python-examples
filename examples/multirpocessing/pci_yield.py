"""
Measure using PCI board a return the values using yield.
"""
import nidaqmx
from nidaqmx import stream_readers
import numpy as np


def run(datos):
    """
    Take measurement and return a generator

    Parameters
    ----------
    - datos : [numpy.ndarray]
              Data container with correct dimention
    Yields
    ------
    - datos : [numpy.ndarray]
              Data measured by de PCI board

    """

    #create the task
    task=nidaqmx.Task(new_task_name="PCI-con-cal")
    #add the analog channels
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai0",
                                        min_val=-10.0,
                                        max_val=10.0,
                                        terminal_config= nidaqmx.constants.TerminalConfiguration.DIFF,
                                        units=nidaqmx.constants.VoltageUnits.VOLTS
                                        )
    #add timing configuration from the task
    task.timing.cfg_samp_clk_timing(rate=10000,
                                    source="OnboardClock",
                                    active_edge=nidaqmx.constants.Edge.RISING,
                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    samps_per_chan=10000)
    #intialize a stream reader class
    reader =stream_readers.AnalogMultiChannelReader(task.in_stream)
    
    print("\nPre-yield loop\n")
    while True:
        try:
            #measure stream_rader method many samples
            reader.read_many_sample(data=datos, 
                                   number_of_samples_per_channel=10000, 
                                   timeout=10.0)
            print("pre-yield measurement",datos[0,1:3])
            print("pre-yield measurement len",datos.shape)
            yield datos
        except GeneratorExit:
            print("\nEnd generator")
            task.stop()
            task.close()
            break

if __name__=="__main__":
    #main process
    datos=np.ones((1,10000))
    print("\nStart main process")
    generator=run(datos)
    #take measurement
    for i in range(3):
        data=next(generator)
        print("main measurement",data[0][1:3])
        print("main measurement len",data.shape)
    generator.close()

"""
Output:
-------

Start main process

Pre-yield loop

pre-yield measurement [ 0.04395068 -0.17214015]
pre-yield measurement len (1, 10000)
main measurement [ 0.04395068 -0.17214015]
main measurement len (1, 10000)
pre-yield measurement [0.12086436 0.02685875]
pre-yield measurement len (1, 10000)
main measurement [0.12086436 0.02685875]
main measurement len (1, 10000)
pre-yield measurement [ 0.         -0.23074106]
pre-yield measurement len (1, 10000)
main measurement [ 0.         -0.23074106]
main measurement len (1, 10000)

End generator
"""