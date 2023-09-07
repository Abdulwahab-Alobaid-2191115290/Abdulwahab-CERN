#!/usr/bin/python3

# importing the required module
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplhep as hep
import scipy
import sys
import os
from matplotlib.ticker import ScalarFormatter, FuncFormatter
#https://github.com/eamonnmag.CERN-CSC-2023


# seaborn graph
#sns.set()

def max_arr(arrays):
    return np.max(arrays, axis=None)


directory = '/home/wahab/backend/pixeltrack/kernel_connect/tbb-kernel-connect/'


# init mixed plot
fig, ax1 = plt.subplots(figsize = (30,30))


# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a .txt file
    if filename.endswith('.csv'):

        # read data
        data = pd.read_csv(f"./{filename}")

        # extract data 
        Thresh   = (data["thresh"].values.astype(np.int_))[0]
        Threads   = (data["threads"].values.astype(np.float32))
        Time   = (data["time"].values.astype(np.float32))
        Stdev  = (data["stdev"].values.astype(np.float32))

        # marker size
        msize = 100
        
        if Thresh == 2048:
            ax1.plot(Threads, Time, marker="o", label=f"thresh-{Thresh}", color='black')
        else:
            ax1.plot(Threads, Time, marker="o", label=f"thresh-{Thresh}")

        #ax1.errorbar(Threads, Time, fmt='o', yerr=Stdev, ms=0, capsize=10)

# Titles
ax1.set_title("Time of Execution kernel_connect() with increasing ThreshHold and NumberOfThreads On The TBB Backend")

# labels
ax1.set_ylabel("Time ns")
ax1.set_xlabel("Threads")



ax1.set_yscale("log")
ax1.set_xscale("log", base=2)
#ax1.set_xticks(serialThresh)
#ax1.set_xticklabels(serialThresh)



# legends
ax1.legend()


# axis
#ax2.yaxis.set_tick_params(labelleft=True)   # shows lables on the second plot
#ax4.yaxis.set_tick_params(labelleft=True)   # shows lables on the second plot


"""
# calculate performance
print("Performance difference from serial to tbb: \nUsing equation: (end - start)/start * 100 \nHowever we invert the percentage because of avg_t \n")
perf = 0
for i in range(len(serialThroughput)):

    perf = ((tbbThroughput[i] - serialThroughput[i]) / serialThroughput[i]) * 100
    print("threads < ", serialThreads[i], " >: ", int(perf)*-1, "%")
######
"""

"""
# plot horizontal lines on the ticks for a log scale
lbs = [ 10**i for i in range(1,4) ]
for y in lbs:
    #ax1.axhline(y = y, color = 'gray', linestyle = 'dashed') 
    pass
"""

# Add vertical lines at each x-axis label position
#for i, label in enumerate(ax1.get_xticklabels()):
#    ax1.axvline(x=i, color='#d3d3d3', linestyle='dashed')



# plt
#plt.xticks(rotation="vertical")
plt.rcParams["keymap.quit"] = ['q']
plt.show()

