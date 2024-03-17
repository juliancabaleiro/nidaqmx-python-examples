import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

scope=pd.read_csv("RefCurve_2024-03-07_0_132905.Wfm.csv",delimiter=";",header=None)
scope.info()
#print(scope[0])
x=(2e-6)*np.arange(len(scope[0]))


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.pylab as pl
import matplotlib.colors as mcolors
import matplotlib.style as style

#simulacion y medicion 
fig, ax = plt.subplots()
xpoints = x
ypoints = scope[0]
xmed=x
ymed=scope[1]
#colors = plt.cm.Set1
colors = pl.cm.Set1(np.linspace(0,1,10))
plt.grid(which="both",color='#ececec',zorder=0)
line1, =plt.plot(xpoints, ypoints,color=colors[0],label='Trigger')
plt.ylabel("Amplitud [V]",fontname="Montserrat", fontsize=15)
plt.xlabel("Time [s]", fontname="Montserrat", fontsize=15)
plt.title('TDMS with pulse trigger adquired with osciloscope',fontname="Montserrat", fontsize=15)
line2, =plt.plot(xmed, ymed,color=colors[1],label='Signal')
ax.legend(handles=[line1, line2], fontsize=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
image_format = 'png' # e.g .png, .svg, etc.
image_name = 'tdms_co.png'

plt.show()
fig.savefig(image_name, format=image_format, dpi=1200)
