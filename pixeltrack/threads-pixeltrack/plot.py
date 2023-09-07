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
serial  = pd.read_csv("./serial.csv")
tbb  = pd.read_csv("./tbb.csv")
cuda = pd.read_csv("./cuda.csv")

# extract data 
serialThreads = (serial["threads"].values.astype(np.int32))   
serialThroughput = (serial["avg_t"].values.astype(np.float32))
serialUtilization = (serial["avg_u"].values.astype(np.float32))
serialStdev_t= (serial["stdev_t"].values.astype(np.float32))
serialStdev_u= (serial["stdev_u"].values.astype(np.float32))


tbbThreads = (tbb["threads"].values.astype(np.int32))
tbbThroughput = (tbb["avg_t"].values.astype(np.float32))
tbbUtilization = (tbb["avg_u"].values.astype(np.float32))
tbbStdev_t= (tbb["stdev_t"].values.astype(np.float32))
tbbStdev_u= (tbb["stdev_u"].values.astype(np.float32))

cudaThreads = (cuda["threads"].values.astype(np.int32))
cudaThroughput = (cuda["avg_t"].values.astype(np.float32))
cudaUtilization = (cuda["avg_u"].values.astype(np.float32))
cudaStdev_t= (cuda["stdev_t"].values.astype(np.float32))
cudaStdev_u= (cuda["stdev_u"].values.astype(np.float32))


# init mixed plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (15,15), gridspec_kw = {'width_ratios': [0.001,0.001]})
#fig.suptitle("Performance Measurement Between Different Backends", fontthreads=20)

# share axis
if len(sys.argv) == 1:
    ax1.sharey(ax2)
#ax3.sharey(ax4)

# plot
ax1.plot(serialThreads, serialThroughput, marker="o", label="SERIAL")
ax1.plot(tbbThreads, tbbThroughput, marker="o", label="TBB", color='orange')
ax1.plot(cudaThreads, cudaThroughput, marker="o", label="CUDA", color='green')

ax2.plot(serialThreads, serialUtilization, marker="o", label="SERIAL")
ax2.plot(tbbThreads, tbbUtilization, marker="o", label="TBB", color='orange')
ax2.plot(cudaThreads, cudaUtilization, marker="o", label="CUDA", color='green')

# plot error
ax1.errorbar(serialThreads, serialThroughput, fmt='o', yerr=serialStdev_t, ms=0, capsize=10, color="black")
ax1.errorbar(tbbThreads, tbbThroughput, fmt='o', yerr=tbbStdev_t, ms=0, capsize=10, color="black")
ax1.errorbar(cudaThreads, cudaThroughput, fmt='o', yerr=cudaStdev_t, ms=0, capsize=10, color="black")

ax2.errorbar(serialThreads, serialUtilization, fmt='o', yerr=serialStdev_u, ms=0, capsize=10, color="black")
ax2.errorbar(tbbThreads, tbbUtilization, fmt='o', yerr=tbbStdev_u, ms=0, capsize=10, color="black")
ax2.errorbar(cudaThreads, cudaUtilization, fmt='o', yerr=cudaStdev_u, ms=0, capsize=10, color="black")



# specify log scale instead of default "linear"
ax1.set_xscale("log", base=2)
ax1.set_yscale("log", base=10)

ax2.set_xscale("log", base=2)
ax2.set_yscale("log", base=10)

#ax2.set_xscale("linear")
#ax2.set_yscale("linear")


# Titles
ax1.set_title("Throughput events/s With Respect To Threads")
ax2.set_title("Cpu Utilization % With Respect To Threads")


# labels
ax1.set_ylabel("Throughput")
ax1.set_xlabel("Threads")

ax2.set_ylabel("Utilization")
ax2.set_xlabel("Threads")


# setup ticks based on command line arguments
if len(sys.argv) == 2:
    backend = sys.argv[1]
    
    match backend:

        case "tbb":
            plt.suptitle('Plotting TBB Ticks Only')
            ax1.set_yticks(tbbThroughput)
            ax1.set_yticklabels(tbbThroughput)
       
            ax2.set_yticks(tbbUtilization)
            ax2.set_yticklabels(tbbUtilization)
       
            """
            # set horizontal lines
            for y, y8 in zip(tbbThroughput, tbbUtilization):
                ax1.axhline(y = y, color = '#CE80CF', linestyle = 'dashed') 
                ax2.axhline(y = y8, color = '#CE80CF', linestyle = 'dashed')

            for x, y in zip(tbbThroughput, tbbThreads):
                plt.annotate( str(x) + ',yooooooooooooooooo' + str(y), (x,y))
            """

        case "serial":
            plt.suptitle('Plotting SERIAL Ticks Only')
            ax1.set_yticks(serialThroughput)
            ax1.set_yticklabels(serialThroughput)
            
            ax2.set_yticks(serialUtilization)
            ax2.set_yticklabels(serialUtilization)
            
            """
            # set horizontal lines
            for y, y8 in zip(serialThroughput, serialUtilization):
                ax1.axhline(y = y, color = '#CE80CF', linestyle = 'dashed') 
                ax2.axhline(y = y8, color = '#CE80CF', linestyle = 'dashed') 
            """

        case "cuda":
            plt.suptitle('Plotting CUDA Ticks Only')
            ax1.set_yticks(cudaThroughput)
            ax1.set_yticklabels(cudaThroughput)
            
            ax2.set_yticks(cudaUtilization)
            ax2.set_yticklabels(cudaUtilization)
            
            """
            # set horizontal lines
            for y, y8 in zip(cudaThroughput, cudaUtilization):
                ax1.axhline(y = y, color = '#CE80CF', linestyle = 'dashed') 
                ax2.axhline(y = y8, color = '#CE80CF', linestyle = 'dashed') 
            """
  
        case _:
            print("invalid backend passed: ", backend)


# legends
ax1.legend()
ax2.legend()


# axis
ax2.yaxis.set_tick_params(labelleft=True)   # shows lables on the second plot
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

# plot horizontal lines on the ticks for a log scale
lbs = [ 10**i for i in range(1,4) ]
for y in lbs:
    ax1.axhline(y = y, color = 'gray', linestyle = 'dashed') 
    ax2.axhline(y = y, color = 'gray', linestyle = 'dashed') 


# plt
plt.rcParams["keymap.quit"] = ['q']
plt.show()

