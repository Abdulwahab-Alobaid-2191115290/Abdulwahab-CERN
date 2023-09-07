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
serialThresh   = (serial["thresh"].values.astype(np.float32))
serialTime   = (serial["time"].values.astype(np.float32))
serialStdev  = (serial["stdev"].values.astype(np.float32))

tbbThresh   = (tbb["thresh"].values.astype(np.float32))
tbbTime   = (tbb["time"].values.astype(np.float32))
tbbStdev  = (tbb["stdev"].values.astype(np.float32))

cudaThresh   = (cuda["thresh"].values.astype(np.float32))
cudaTime   = (cuda["time"].values.astype(np.float32))
cudaStdev  = (cuda["stdev"].values.astype(np.float32))


#ratioThreads = tbbThreads
#ratioThroughput = serialThroughput/tbbThroughput


# init mixed plot
fig, ax1 = plt.subplots(figsize = (30,30))

# marker size
msize = 100
# plot - x-axis is always the number of threads
#ax1.scatter(serialThresh, serialTime, marker="o", s=msize, label="SERIAL")
ax1.plot(serialThresh, serialTime, marker="o", label="SERIAL")
#ax1.scatter(tbbThresh, tbbTime, marker="o", s=msize, label="TBB", color='orange')
ax1.plot(tbbThresh, tbbTime, marker="o", label="TBB", color='orange')
ax1.plot(cudaThresh, cudaTime, marker="o", label="CUDA", color='green')

# plot error
#ax1.errorbar(serialThresh, serialTime, fmt='o', yerr=serialStdev, ms=0, capsize=10, color="black")
#ax1.errorbar(tbbThresh, tbbTime, fmt='o', yerr=tbbStdev, ms=0, capsize=10, color="black")

# Titles
ax1.set_title("Time of Execution kernel_connect() with increasing ThreshHold")

# labels
ax1.set_ylabel("Time ns")
ax1.set_xlabel("ThreshHold")

min_tbb = min(tbbTime)
max_tbb = max(tbbTime)
min_serial = min(serialTime)
max_serial = max(serialTime)
max_cuda = max(cudaTime)
min_cuda = min(cudaTime)

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


ax1.axhline(y=min_tbb, color='green', linestyle='dashed')
ax1.axhline(y=max_tbb, color='red', linestyle='dashed')

ax1.axhline(y=min_cuda, color='green', linestyle='dashed')
ax1.axhline(y=max_cuda, color='red', linestyle='dashed')

ax1.axhline(y=min_serial, color='green', linestyle='dashed')
ax1.axhline(y=max_serial, color='red', linestyle='dashed')

# plt
#plt.xticks(rotation="vertical")
plt.rcParams["keymap.quit"] = ['q']
plt.show()

