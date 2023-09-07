#!/usr/bin/python3
import statistics
from pathlib import Path
import os

directory = './iterations/'


# tbb-kernel-connect-thresh-128-1024-threads.txt

for filename in os.listdir(directory):
    if not filename.endswith('.txt'):
        continue

    with open(os.path.join(directory, filename), 'r') as f:
        lines = f.readlines()
    
    threads = filename.split('-')[5]

    kernels = {}    # { "kernel_1": time_in_nanoseconds, etc.. }
    for l in lines:
        thresh, time = l.split()
        if thresh in kernels:
            kernels[thresh].append(int(time))
        else:
            kernels[thresh] = [int(time)]

    sums = {}   # { "kernel_1": sum_of_time_taken }
    for k in kernels:
       
        if k not in sums:
            sums[k] = 0
        
        for t in kernels[k]:
            sums[k] += t

    avgs = {}   # { "kernel_1": avg_of_time_taken }
    for k in kernels:
        avgs[k] = sums[k]/len(kernels[k])

    
    std = {}   # { "kernel_1": standard_deviation_of_time_taken }
    for k in kernels:
        std[k] = statistics.stdev(kernels[k])
 
    if not Path(f'/home/wahab/backend/pixeltrack/kernel_connect/tbb-kernel-connect/thresh-{thresh}.csv').exists():
        with open(f"thresh-{thresh}.csv", "a") as sf:
            sf.write('thresh,threads,time,stdev\n')
           
    with open(f"thresh-{thresh}.csv", "a") as sf: 
        for k in kernels:
            sf.write(f"{k},{threads},{avgs[k]},{std[k]}\n")




