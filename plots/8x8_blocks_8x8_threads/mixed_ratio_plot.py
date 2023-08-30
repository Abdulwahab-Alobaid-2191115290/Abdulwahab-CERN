#!/usr/bin/python3

# Plot to show the ratio of tbb/cpu perfomance

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

ratioSize = tbbSize
ratioTime = tbbTime/cpuTime
# stdev?

# init mixed plot
fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False, figsize = (15,10), gridspec_kw = {'width_ratios': [1,1]})

# scatter log
ax1.plot(cpuSize, cpuTime, marker="o", label="CPU")
ax1.plot(tbbSize, tbbTime, marker="o", label="TBB", color='orange')
ax1.plot(ratioSize, ratioTime, marker="o", label="TBB/CPU", color='red')

# scatter linear
ax2.plot(cpuSize, cpuTime, marker="o", label="CPU")#, facecolors='none', color='blue')
ax2.plot(tbbSize, tbbTime, marker="o", label="TBB")#, facecolors='none', color='orange')
ax2.plot(ratioSize, ratioTime, marker="o", label="TBB/CPU")#, facecolors='none', color='orange')

# plot error
ax1.errorbar(cpuSize, cpuTime, fmt='o', yerr=cpuStdev, ms=0, capsize=10)
ax1.errorbar(tbbSize, tbbTime, fmt='o', yerr=tbbStdev, ms=0, capsize=10)
# error?? ax1.errorbar(tbbSize, tbbTime, fmt='o', yerr=tbbStdev, ms=0, capsize=10)

ax2.errorbar(cpuSize, cpuTime, fmt='o', yerr=cpuStdev, ms=0, capsize=10)
ax2.errorbar(tbbSize, tbbTime, fmt='o', yerr=tbbStdev, ms=0, capsize=10)

# scale
ax1.set_xscale("log", base=2)
ax1.set_yscale("log", base=10)

#ax2.set_xscale("log", base=2)
#ax2.set_yscale("log", base=10)


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
