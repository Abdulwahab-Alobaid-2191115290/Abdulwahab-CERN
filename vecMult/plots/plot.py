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


#CONSTANT

# seaborn graph
#sns.set()

def max_arr(arrays):
    return np.max(arrays, axis=None)


# read data
    # constant
cpu  = pd.read_csv("./increasing_blocks_8x8_blocksize_csv/cpu.csv")
tbb  = pd.read_csv("./increasing_blocks_8x8_blocksize_csv/tbb.csv")
mt   = pd.read_csv("./increasing_blocks_8x8_blocksize_csv/mt.csv")
cuda = pd.read_csv("./increasing_blocks_8x8_blocksize_csv/cuda.csv")
    # 8x8
cpu8  = pd.read_csv("./8x8_blocks_8x8_threads_csv/cpu.csv")
tbb8  = pd.read_csv("./8x8_blocks_8x8_threads_csv/tbb.csv")
mt8   = pd.read_csv("./8x8_blocks_8x8_threads_csv/mt.csv")
cuda8 = pd.read_csv("./8x8_blocks_8x8_threads_csv/cuda.csv")


# extract data
    # constant
cpuSize = (cpu["size"].values.astype(np.int32))   # size is x-axis
cpuTime = (cpu["time"].values.astype(np.float32)) # time is y-axis
cpuStdev= (cpu["stdev"].values.astype(np.float32))

tbbSize = (tbb["size"].values.astype(np.int32))
tbbTime = (tbb["time"].values.astype(np.float32))
tbbStdev= (tbb["stdev"].values.astype(np.float32))

mtSize = (mt["size"].values.astype(np.int32))   
mtTime = (mt["time"].values.astype(np.float32))
mtStdev= (mt["stdev"].values.astype(np.float32))

cudaSize = (cuda["size"].values.astype(np.int32))
cudaTime = (cuda["time"].values.astype(np.float32))
cudaStdev= (cuda["stdev"].values.astype(np.float32))

ratioSize = tbbSize
ratioTime = cpuTime/tbbTime
    # 8x8
cpuSize8 = (cpu8["size"].values.astype(np.int32))   # size is x-axis
cpuTime8 = (cpu8["time"].values.astype(np.float32))
cpuStdev8= (cpu8["stdev"].values.astype(np.float32))


tbbSize8 = (tbb8["size"].values.astype(np.int32))   # size is x-axis
tbbTime8 = (tbb8["time"].values.astype(np.float32))
tbbStdev8= (tbb8["stdev"].values.astype(np.float32))

mtSize8 = (mt8["size"].values.astype(np.int32))   # size is x-axis
mtTime8 = (mt8["time"].values.astype(np.float32))
mtStdev8= (mt8["stdev"].values.astype(np.float32))

cudaSize8 = (cuda8["size"].values.astype(np.int32))   # size is x-axis
cudaTime8 = (cuda8["time"].values.astype(np.float32))
cudaStdev8= (cuda8["stdev"].values.astype(np.float32))

ratioSize8 = tbbSize8
ratioTime8 = cpuTime8/tbbTime8



# init mixed plot
fig, ((ax1, ax2),(ax3,ax4)) = plt.subplots(2, 2, figsize = (15,15), gridspec_kw = {'width_ratios': [0.001,0.001]})
#fig.suptitle("Performance Measurement Between Different Backends", fontsize=20)

# share axis
ax1.sharey(ax2)
ax3.sharey(ax4)


# plot
    # constant
ax1.plot(cpuSize, cpuTime, marker="o", label="CPU")
ax1.plot(tbbSize, tbbTime, marker="o", label="TBB", color='orange')
ax1.plot(mtSize, mtTime, marker="o", label="MT", color='purple')
ax1.plot(cudaSize, cudaTime, marker="o", label="CUDA", color='green')
    # ratio
ax3.plot(ratioSize, ratioTime, marker="o", label="CPU/TBB", color="red")#, facecolors='none', color='orange')

    # 8x8
ax2.plot(cpuSize8, cpuTime8, marker="o", label="CPU")
ax2.plot(tbbSize8, tbbTime8, marker="o", label="TBB", color='orange')
ax2.plot(mtSize8, mtTime8, marker="o", label="MT", color='purple')
ax2.plot(cudaSize8, cudaTime8, marker="o", label="CUDA", color='green')
    # ratio
ax4.plot(ratioSize8, ratioTime8, marker="o", label="CPU/TBB", color="red")#, facecolors='none', color='orange')


# plot error
    # constant
ax1.errorbar(cpuSize, cpuTime, fmt='o', yerr=cpuStdev, ms=0, capsize=10, color="black")
ax1.errorbar(tbbSize, tbbTime, fmt='o', yerr=tbbStdev, ms=0, capsize=10, color="black")
ax1.errorbar(mtSize, mtTime, fmt='o', yerr=mtStdev, ms=0, capsize=10, color="black")
ax1.errorbar(cudaSize, cudaTime, fmt='o', yerr=cudaStdev, ms=0, capsize=10, color="black")

    # 8x8
ax2.errorbar(cpuSize8, cpuTime8, fmt='o', yerr=cpuStdev8, ms=0, capsize=10, color="black")
ax2.errorbar(tbbSize8, tbbTime8, fmt='o', yerr=tbbStdev8, ms=0, capsize=10, color="black")
ax2.errorbar(mtSize8, mtTime8, fmt='o', yerr=mtStdev8, ms=0, capsize=10, color="black")
ax2.errorbar(cudaSize8, cudaTime8, fmt='o', yerr=cudaStdev8, ms=0, capsize=10, color="black")


# specify log scale instead of default "linear"
ax1.set_xscale("log", base=2)
ax1.set_yscale("log", base=10)

ax2.set_xscale("log", base=2)
ax2.set_yscale("log", base=10)


ax3.set_xscale("log", base=2)
ax4.set_xscale("log", base=2)


# Titles
ax1.set_title("Block Count: increasing\nBlock Size: 8x8")
ax2.set_title("Block Count: 8x8\nBlock Size: 8x8")
ax3.set_title("CPU-TBB Ratio")
ax4.set_title("CPU-TBB Ratio")


# labels
ax1.set_ylabel("Time")
ax1.set_xlabel("Size")

ax2.set_ylabel("Time")
ax2.set_xlabel("Size")



# setup ticks based on command line arguments

#y = np.concatenate((cpuTime, tbbTime, mtTime, cudaTime))  makes the plot crowded

#ax3.set_yticks(ratioTime)
#ax3.set_yticklabels(ratioTime)

#ax4.set_yticks(ratioTime8)
#ax4.set_yticklabels(ratioTime8)

if len(sys.argv) == 2:
    backend = sys.argv[1]
    
    match backend:

        case "tbb":
            plt.suptitle('Plotting TBB Ticks Only')
            ax1.set_yticks(tbbTime)
            ax1.set_yticklabels(tbbTime)
       #     ax2.set_yticks(tbbTime8)
       #     ax2.set_yticklabels(tbbTime8)
            # set horizontal lines
            for y, y8 in zip(tbbTime, tbbTime8):
                ax1.axhline(y = y, color = '#CE80CF', linestyle = 'dashed') 
                ax2.axhline(y = y8, color = '#CE80CF', linestyle = 'dashed')

            for x, y in zip(tbbTime, tbbSize):
                plt.annotate( str(x) + ',yooooooooooooooooo' + str(y), (x,y))
        
        case "cpu":
            plt.suptitle('Plotting CPU Ticks Only')
            ax1.set_yticks(cpuTime)
            ax1.set_yticklabels(cpuTime)
            ax2.set_yticks(cpuTime8)
            ax2.set_yticklabels(cpuTime8)
            # set horizontal lines
            for y, y8 in zip(cpuTime, cpuTime8):
                ax1.axhline(y = y, color = '#CE80CF', linestyle = 'dashed') 
                ax2.axhline(y = y8, color = '#CE80CF', linestyle = 'dashed') 
        
        case "mt":
            plt.suptitle('Plotting MT Ticks Only')
            ax1.set_yticks(mtTime)
            ax1.set_yticklabels(mtTime)
            ax2.set_yticks(mtTime8)
            ax2.set_yticklabels(mtTime8)
            # set horizontal lines
            for y, y8 in zip(mtTime, mtTime8):
                ax1.axhline(y = y, color = '#CE80CF', linestyle = 'dashed') 
                ax2.axhline(y = y8, color = '#CE80CF', linestyle = 'dashed') 
 
        case "cuda":
            plt.suptitle('Plotting CUDA Ticks Only')
            ax1.set_yticks(cudaTime)
            ax1.set_yticklabels(cudaTime)
            ax2.set_yticks(cudaTime8)
            ax2.set_yticklabels(cudaTime8)
            # set horizontal lines
            for y, y8 in zip(cudaTime, cudaTime8):
                ax1.axhline(y = y, color = '#CE80CF', linestyle = 'dashed') 
                ax2.axhline(y = y8, color = '#CE80CF', linestyle = 'dashed') 
 
  
        case _:
            print("invalid backend passed: ", backend)


# legends
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()


# axis
ax2.yaxis.set_tick_params(labelleft=True)   # shows lables on the second plot
ax4.yaxis.set_tick_params(labelleft=True)   # shows lables on the second plot


# plot horizontal lines on the ticks for the linear scale
lbs = [ 10**i for i in range(2,9) ]
for y in lbs:
    ax1.axhline(y = y, color = 'gray', linestyle = 'dashed') 
    ax2.axhline(y = y, color = 'gray', linestyle = 'dashed') 

# plot horizontal lines on the ticks for the linear scale
lbs = [ 10*i for i in range(1,5) ]
for y in lbs:
    ax3.axhline(y = y, color = 'gray', linestyle = 'dashed') 
    ax4.axhline(y = y, color = 'gray', linestyle = 'dashed') 



# plt
plt.rcParams["keymap.quit"] = ['q']
plt.show()

