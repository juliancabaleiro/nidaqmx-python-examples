"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Aquire data with PCI board in a Subprocess and return the data array to
the main process using Multiprocessing Array in a function aproach.
"""

from multiprocessing import Process, Value, Array, Event
import time
import nidaqmx
from nidaqmx import stream_readers
import numpy as np
from numpy.ctypeslib import as_ctypes

def run(dataA,datos,data,event):
    """
    Function to take measurements.

    Parameters
    ----------

    - dataA : [c_double_Array] 
              Multiprocess shared array
    - datos : [numpy.ndarray]
              Data container with correct dimention
    - data :  [multiprocessing.sharedctypes.Synchronized] 
              Multiprocess shared value
    - event : [multiprocessing.synchronize.Event] 
              Multiprocess variable to safetly stop the process
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
    
    print("\nProcess-before of loop")
    while True:
        #Output secuence
        if event.is_set():
            task.stop()
            task.close()
            print("\nEnd proccess")
            break
        #measure stream_rader method many samples
        reader.read_many_sample(data=datos, 
                               number_of_samples_per_channel=10000, 
                               timeout=10.0)
        data.value=np.mean(datos)
        dataA[:] = datos.reshape(10000,)
        #Also works
        #aux=datos.tolist()
        # for i in range(len(aux[0])):
        #     dataA[i]=aux[0][i]

        print("process measurement",datos[0,1:3])
        print("process Shared array dataA",dataA[1:3])
        print("process Shared array dataA len",len(dataA))

if __name__=="__main__":
    #main process
    datos=np.ones((1,10000))
    datos_t=np.ones((10000,))
    ctype = as_ctypes(datos_t)
    dataA  = Array(ctype._type_, datos_t, lock=False)
    data = Value('f', 14)
    event = Event()
    print("\nmain data Array ",dataA[:3])

    #intilize sub-process
    measure=Process(target=run, args=(dataA,datos,data,event))
    #start subprocess
    measure.start()
    print("main process-state ",measure.is_alive())

    time.sleep(5)

    #safetly process close
    event.set()
    measure.join()
    print("main data Array END ",dataA[1:3])
    print("main process-state ",measure.is_alive())

"""
Output:
-------

main data Array  [1.0, 1.0, 1.0]
main process-state  True

Process-before of loop
process measurement [ 0.04395068 -0.17214015]
process Shared array dataA [0.04395067757294591, -0.1721401538273715]
process Shared array dataA len 10000
process measurement [0.12086436 0.02685875]
process Shared array dataA [0.12086436332560127, 0.02685874740568917]
process Shared array dataA len 10000
process measurement [ 0.         -0.23074106]
process Shared array dataA [0.0, -0.23074105725796604]
process Shared array dataA len 10000

End proccess
main data Array END  [0.0, -0.23074105725796604]
main process-state  False
"""