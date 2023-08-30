#!/usr/bin/python3

# importing the required module
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplhep as hep
import scipy
import sys
from matplotlib.ticker import ScalarFormatter, FuncFormatter
#https://github.com/eamonnmag.CERN-CSC-2023


# seaborn graph
#sns.set()

def max_arr(arrays):
    return np.max(arrays, axis=None)


# read data
serial  = pd.read_csv("./serial-kernels.csv")
tbb  = pd.read_csv("./tbb-kernels.csv")
cuda  = pd.read_csv("./cuda-kernels.csv")

# extract data 
serialTime   = (serial["time"].values.astype(np.float32))
serialStdev  = (serial["stdev"].values.astype(np.float32))

tbbTime   = (tbb["time"].values.astype(np.float32))
tbbStdev  = (tbb["stdev"].values.astype(np.float32))

cudaTime   = (cuda["time"].values.astype(np.float32))
cudaStdev  = (cuda["stdev"].values.astype(np.float32))


#ratioThreads = tbbThreads
#ratioThroughput = serialThroughput/tbbThroughput


# init mixed plot
fig, ax1 = plt.subplots(figsize = (30,30))

# marker size
msize = 100
# plot - x-axis is always the number of threads
ax1.scatter(serial["kernel"], serialTime, marker="o", s=msize, label="SERIAL")
ax1.scatter(tbb["kernel"], tbbTime, marker="o", s=msize, label="TBB", color='orange')
ax1.scatter(cuda["kernel"], cudaTime, marker="o", s=msize, label="CUDA", color='green')

# plot error
ax1.errorbar(serial["kernel"], serialTime, fmt='o', yerr=serialStdev, ms=0, capsize=10, color="black")
ax1.errorbar(tbb["kernel"], tbbTime, fmt='o', yerr=tbbStdev, ms=0, capsize=10, color="black")
ax1.errorbar(cuda["kernel"], cudaTime, fmt='o', yerr=cudaStdev, ms=0, capsize=10, color="black")

# Titles
ax1.set_title("Time of Execution of Kernels")

# labels
ax1.set_ylabel("Time ns")
ax1.set_xlabel("Kernels")

ax1.set_yscale("log", base=10)
#ax1.set_yscale("linear")
#ax1.set_yticklabels(serialTime)


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
for i, label in enumerate(ax1.get_xticklabels()):
    ax1.axvline(x=i, color='#d3d3d3', linestyle='dashed')

# plt
plt.xticks(rotation="vertical")
plt.rcParams["keymap.quit"] = ['q']
plt.show()

