"""
Create a subprocess that measure with PCI board and put the data in queue 
for be accessed by main process
"""

from multiprocessing import Process, Value, Array, Event, Queue
import time
import nidaqmx
from nidaqmx import stream_readers
import numpy as np
from numpy.ctypeslib import as_ctypes

def run(event,samps=10000,frec=10000,range=10,dev="Dev1/",queue=0):
    """
    Parameters
    ----------
    - event : [multiprocessing.synchronize.Event] 
              Multiprocess variable to safetly stop the process
    - samps : [int]
            Samples to extract
    - frec : [int]
            Frecuency to adquisition system [Hz]
    - range : [int]
            Range to the adquisition board
    - dev : [str]
            string to the path of the device
    - queue : [multiprocessing.queues.Queue]
             Queue to share the measured data between process
    """
    #create the task
    task=nidaqmx.Task()
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
    #intialize a stream reader class
    reader =stream_readers.AnalogMultiChannelReader(task.in_stream)
    datos=np.ones((1,samps))

    print("\nProcess-before of loop")
    while True:
        #Output secuence
        if event.is_set():
            task.stop()
            task.close()
            print("\nProcess-End proccess")
            break
        #measure stream_rader method many samples
        reader.read_many_sample(data=datos, 
                               number_of_samples_per_channel=samps, 
                               timeout=10.0)
        queue.put(datos)
 
#main process
if __name__=="__main__":
    
    event = Event()
    #create a queue 
    queue = Queue()
    #intilize sub-process
    measure=Process(target=run, args=(event,10000,10000,10,"Dev1/",queue))
    #start subprocess
    measure.start()
    print("\nmain process PID :",measure.pid)
    print("main process-state ",measure.is_alive())

    for i in range(3):
        item = queue.get()
        print("main data queue get type ",type(item))
        print("main shape of data", item.shape)
        print("main data ", item[0][:3])

    #safetly process close
    event.set()
    _=queue.get() #if the queue is not consumed, the process not finish
    measure.join() #wait to the process end
    print("main process exit code ",measure.exitcode)
    print("main main process-state ",measure.is_alive())

"""
Output:
-------

main process PID : 2976
main process-state  True

Process-before of loop
main data queue get type  <class 'numpy.ndarray'>
main shape of data (1, 10000)
main data  [-0.30032963  0.04395068 -0.17214015]
main data queue get type  <class 'numpy.ndarray'>
main shape of data (1, 10000)
main data  [0.0561592  0.12086436 0.02685875]
main data queue get type  <class 'numpy.ndarray'>
main shape of data (1, 10000)
main data  [-0.23928702  0.         -0.23074106]

Process-End proccess
main process exit code  0
main main process-state  False
"""