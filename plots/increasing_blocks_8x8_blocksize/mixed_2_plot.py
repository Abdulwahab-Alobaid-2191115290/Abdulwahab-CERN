#!/usr/bin/python3

# importing the required module
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplhep as hep
import scipy
from matplotlib.ticker import ScalarFormatter, FuncFormatter
#https://github.com/eamonnmag.CERN-CSC-2023

# seaborn graph
#sns.set()

#dataset = sns.load_dataset("flights")

# read data
cpu  = pd.read_csv("cpu.csv")
tbb  = pd.read_csv("tbb.csv")
mt   = pd.read_csv("mt.csv")
cuda = pd.read_csv("cuda.csv")


# extract data
cpuSize = np.sort(cpu["size"].values.astype(np.int32))   # size is x-axis
cpuTime = np.sort(cpu["time"].values.astype(np.float32))
cpuStdev= np.sort(cpu["stdev"].values.astype(np.float32))


tbbSize = np.sort(tbb["size"].values.astype(np.int32))   # size is x-axis
tbbTime = np.sort(tbb["time"].values.astype(np.float32))
tbbStdev= np.sort(tbb["stdev"].values.astype(np.float32))

mtSize = np.sort(mt["size"].values.astype(np.int32))   # size is x-axis
mtTime = np.sort(mt["time"].values.astype(np.float32))
mtStdev= np.sort(mt["stdev"].values.astype(np.float32))

cudaSize = np.sort(cuda["size"].values.astype(np.int32))   # size is x-axis
cudaTime = np.sort(cuda["time"].values.astype(np.float32))
cudaStdev= np.sort(cuda["stdev"].values.astype(np.float32))


# init mixed plot
fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False, figsize = (15,10), gridspec_kw = {'width_ratios': [1,1]})


# make xAxis
#cpuXaxis = np.arange(1, len(cpuSize) + 1)
#cpuXaxis = np.arange(1, len(cpuSize) + 1)
#cpuXaxis = np.arange(1, len(cpuSize) + 1)
#cpuXaxis = np.arange(1, len(cpuSize) + 1)

# setup ticks ' map labels to values '
#ax1.set_xticks(cpuXaxis, cpuSize)
#ax1.set_yticks(cpuTime)
#ax2.set_xticks(cpuTime)
#ax2.set_yticks(cpuTime)

# scatter log
ax1.plot(cpuSize, cpuTime, marker="o", label="CPU")
ax1.plot(tbbSize, tbbTime, marker="o", label="TBB", color='orange')
ax1.plot(mtSize, mtTime, marker="o", label="MT", color='purple')
ax1.plot(cudaSize, cudaTime, marker="o", label="CUDA", color='green')


# scatter linear
ax2.plot(cpuSize, cpuTime, marker="o", label="CPU")#, facecolors='none', color='blue')
ax2.plot(tbbSize, tbbTime, marker="o", label="TBB")#, facecolors='none', color='orange')
ax2.plot(mtSize, mtTime, marker="o", label="MT")#, facecolors='none', color='purple')
ax2.plot(cudaSize, cudaTime, marker="o", label="CUDA")#, facecolors='none', color='red')


# plot error
ax1.errorbar(cpuSize, cpuTime, fmt='o', yerr=cpuStdev, ms=0, capsize=10)
ax1.errorbar(tbbSize, tbbTime, fmt='o', yerr=tbbStdev, ms=0, capsize=10)
ax1.errorbar(mtSize, mtTime, fmt='o', yerr=mtStdev, ms=0, capsize=10)
ax1.errorbar(cudaSize, cudaTime, fmt='o', yerr=cudaStdev, ms=0, capsize=10)

ax2.errorbar(cpuSize, cpuTime, fmt='o', yerr=cpuStdev, ms=0, capsize=10)
ax2.errorbar(tbbSize, tbbTime, fmt='o', yerr=tbbStdev, ms=0, capsize=10)
ax2.errorbar(mtSize, mtTime, fmt='o', yerr=mtStdev, ms=0, capsize=10)
ax2.errorbar(cudaSize, cudaTime, fmt='o', yerr=cudaStdev, ms=0, capsize=10)

# scale
ax1.set_xscale("log", base=2)
ax1.set_yscale("log", base=10)

#ax2.set_xscale("log", base=2)
#ax2.set_yscale("log", base=10)


# annotate
ax1.annotate(xy = (0.04, 0.78), text = "Block Count: variable\nBlock Size: 8x8", fontsize = 20, xycoords = "axes fraction")

# labels
ax1.set_ylabel("Time")
ax1.set_xlabel("Size")

ax2.set_ylabel("Time")
ax2.set_xlabel("Size")

# legends
ax1.legend()
ax2.legend()

# plt
plt.rcParams["keymap.quit"] = ['q']
plt.show()


'''
# plotting strip plot with seaborn
ax = sns.relplot(data=dataset, x="size", y="performance", hue="backend", marker="o", kind="line");

# giving title to the plot
plt.title('MyGraph');

# function to show plot
plt.show()
'''
