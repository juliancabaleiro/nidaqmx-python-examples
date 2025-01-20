"""
@author: Julian Cabaleiro
@repository: https://github.com/juliancabaleiro/nidaqmx-python-examples

Aquire data with PCI board in a Subprocess and return the data array to
the main process using Multiprocessing Array in a class aproach.
"""

import multiprocessing
from multiprocessing import Process
from multiprocessing import Value, Array
from multiprocessing import Event
import time
import nidaqmx
from nidaqmx import stream_readers
import numpy as np
from numpy.ctypeslib import as_ctypes

#Create the subprocess class
class CustomProcess(Process):
 #override the constructor
    def __init__(self):
        # execute the base constructor
        Process.__init__(self)
        # initialize shared variables
        self.data = Value('f', 14)
        self.dataA = Array("f", [15 for i in range(10000) ],lock=False)
        #event objetc to share boolean values
        self.event = Event()

    def run(self):
        """
        Method to take measurements.
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
        #stream_rader method many samples
        datos=np.zeros((1,10000), dtype=np.float64)

        print("\nprocess-before of loop")
        while True:
            #Exit secuence
            if self.event.is_set():
                task.stop()
                task.close()
                print("End the process")
                break
            #measure
            reader.read_many_sample(data=datos, 
                                   number_of_samples_per_channel=10000, 
                                   timeout=10.0)
            self.data.value=np.mean(datos)
            self.dataA[:] = datos.reshape(10000,)

            print("process datos",datos[0,1:3])
            print("process dataA",self.dataA[1:3])
            print("process dataA len",len(self.dataA))
            print("process-data update")

#main running
if __name__=="__main__":

    measure=CustomProcess()
    print("main data Array ",measure.dataA[:5])
    #start the process
    measure.start()
    print("main-process-state ",measure.is_alive())
    print("main data ",measure.data.value)
    
    time.sleep(3)

    #safetly process close
    measure.event.set()
    measure.join()
    print("\nmain data Array END ",measure.dataA[:3])

"""
Output
------

main data Array  [15.0, 15.0, 15.0, 15.0, 15.0]
main-process-state  True
main data  14.0

process-before of loop
process datos [ 0.04395068 -0.17214015]
process dataA [0.043950676918029785, -0.17214015126228333]
process dataA len 10000
process-data update
process datos [0.12086436 0.02685875]
process dataA [0.12086436152458191, 0.026858747005462646]
process dataA len 10000
process-data update
End the process

main data Array END  [0.05615919828414917, 0.12086436152458191, 0.026858747005462646]
"""